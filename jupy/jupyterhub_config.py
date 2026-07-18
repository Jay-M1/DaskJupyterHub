import os

from batchspawner import CondorSpawner
from traitlets import Unicode, default

c = get_config() # type: ignore[name-defined]  # noqa: F821

# Persist all hub state on a named docker volume mounted at
# /srv/jupyterhub/state (see docker-compose.yml). Without this the SQLite DB,
# the cookie secret and the auth_state crypt key live only inside the
# container's writable layer, so every `docker compose up --build`/recreate
# starts from an empty DB. That orphans all running single-user servers: their
# JUPYTERHUB_API_TOKEN is no longer in the DB, so dask-gateway's JupyterHub
# auth (which resolves the token via /hub/api/authorizations/token/<t>) gets a
# 404 and returns 401 to the notebook. Keeping the DB on a volume lets running
# servers survive hub restarts and rebuilds. The state dir holds secrets
# (tokens, cookie secret) and lives outside the git repo, so nothing sensitive
# can be committed.
_STATE_DIR = "/srv/jupyterhub/state"
os.makedirs(_STATE_DIR, exist_ok=True)
c.JupyterHub.db_url = "sqlite:///%s/jupyterhub.sqlite" % _STATE_DIR
c.JupyterHub.cookie_secret_file = "%s/jupyterhub_cookie_secret" % _STATE_DIR

# Set the JupyterHub IP and port
c.JupyterHub.bind_url = 'http://0.0.0.0:8555'

# Use authentication
c.JupyterHub.authenticator_class = "LDAPAuthenticator"
c.LDAPAuthenticator.server_address = "ldap.etp.kit.edu"
c.LDAPAuthenticator.server_port = 636
c.LDAPAuthenticator.tls_strategy = "on_connect"
c.LDAPAuthenticator.lookup_dn = False
c.LDAPAuthenticator.user_search_base ="dc=ekp,dc=physik,dc=uni-karlsruhe,dc=de"
c.LDAPAuthenticator.bind_dn_template = ["uid={username},ou=people,dc=ekp,dc=physik,dc=uni-karlsruhe,dc=de"]
c.LDAPAuthenticator.enable_auth_state = True
c.LDAPAuthenticator.auth_state_attributes = ["uid", "uidNumber", "gidNumber"]
_key_file = "%s/auth_state.key" % _STATE_DIR
if os.path.exists(_key_file):
    with open(_key_file, "rb") as _f:
        _key = _f.read()
else:
    _key = os.urandom(32)
    with open(_key_file, "wb") as _f:
        _f.write(_key)
c.CryptKeeper.keys = [_key]

# Allow all valid LDAP users to log in
c.Authenticator.allow_all = True

c.Spawner.debug = True
c.Spawner.start_timeout = 300

# JupyterHub's default is 127.0.0.1, which makes the notebook server on the
# execute node unreachable from the Hub ("Connection refused"). Safe to set
# globally: batchspawner overwrites self.ip with the job's execute host after
# submission, so the Hub still connects to the right address.
c.Spawner.ip = "0.0.0.0"

# Notebook servers run as HTCondor batch jobs (vanilla universe with
# +WantContainer/+ContainerImage) instead of as Docker containers on bms1
# itself. Despite +HookKeyword = "SINGULARITY", the ETP execute nodes run
# these container jobs via Docker, not Apptainer (verified with
# condor_ssh_to_job: the job's process tree sits under containerd-shim), as
# the real submitting LDAP uid, so no root/gosu is involved and start.sh
# runs fine. Docker's default bridge networking would put the job into its
# own network namespace (unreachable from bms1), hence
# docker_network_type = host in the JDL, same as the dask workers in
# rocky/dask-gateway-htcondor/. Explicit docker universe was ruled out
# earlier for the root/gosu reason; the container-universe path makes that
# moot. Verified empirically with throwaway condor_submit test jobs
# (~/nb_test on bms1).
#
# Pinned tag, not :latest: the execute nodes never re-pull a tag they
# already have cached, so pushing a new image under the same tag silently
# does nothing. Rolling out an image update means: push under a new tag,
# change this line, restart the hub.
NOTEBOOK_IMAGE = "docker://uhsur/jupyterhub-notebook:2026-07-08"


class HTCondorNotebookSpawner(CondorSpawner):
    req_memory = Unicode("4096", help="Memory (MB) requested for the notebook job").tag(config=True)
    req_nprocs = Unicode("2", help="CPUs requested for the notebook job").tag(config=True)
    req_environment = Unicode(help="semicolon-joined KEY=VALUE env for the job").tag(config=True)

    # The Hub runs as root, so this "sudo -n -u <user>" needs no sudoers.d
    # entry (root invoking sudo to become anyone always succeeds). This
    # matches dask-gateway-server's own privilege-drop mechanism
    # (do_as_user() in dask_gateway_server/backends/jobqueue/base.py, used
    # by htrocky) rather than batchspawner's default "sudo -E -u {username}"
    # (drops -E: HTCondor's FS pool auth needs the real uid, and identity
    # switch alone via a plain os.seteuid() wrapper was tried first and
    # does NOT satisfy it — only a real sudo-performed setuid does, because
    # it changes the process's real uid, not just its effective uid).
    exec_prefix = Unicode("sudo -n -u {username} -H")

    batch_script = Unicode("""
universe = vanilla
executable = /bin/sh
transfer_executable = false
# cd $HOME: without it the server starts in the HTCondor scratch dir and
# JupyterLab's file browser and terminals root there instead of the home dir
arguments = "-c 'cd $HOME && exec {cmd}'"
should_transfer_files = YES
when_to_transfer_output = ON_EXIT_OR_EVICT
initialdir = {homedir}
output = {homedir}/.jupyterhub.condor.out
error = {homedir}/.jupyterhub.condor.err
log = {homedir}/.jupyterhub.condor.log
request_cpus = {nprocs}
request_memory = {memory}
+ContainerImage = "{docker_image}"
+WantContainer = true
+WantDockerImage = true
+HookKeyword = "SINGULARITY"
docker_network_type = host
environment = {environment}
{options}
queue
""").tag(config=True)

    req_docker_image = Unicode(NOTEBOOK_IMAGE).tag(config=True)

    def get_env(self):
        env = super().get_env()
        # The Hub's internal API (hub_port, 8081 by default) was only ever
        # reachable within the jupyternet overlay network; execute nodes
        # can't reach it ("Network is unreachable" from batchspawner-
        # singleuser's registration call). Route just these two URLs
        # through the already-open public HTTPS path (nginx -> proxy:8555
        # -> hub) instead. Deliberately done here rather than via
        # c.JupyterHub.hub_connect_url: that trait is shared with the
        # proxy's own internal routing to the Hub (Hub.url returns
        # connect_url when set, and the proxy uses Hub.url too), so setting
        # it globally broke the proxy's "/" route to the Hub itself.
        hub_public_api = "https://bms1.etp.kit.edu/hub/api"
        env["JUPYTERHUB_API_URL"] = hub_public_api
        env["JUPYTERHUB_ACTIVITY_URL"] = f"{hub_public_api}/users/{self.user.name}/activity"
        return env

    @default("req_homedir")
    def _req_homedir_default(self):
        # Base class default shells out to pwd.getpwnam(self.user.name) on
        # the *Hub's* local passwd db — LDAP users aren't in it. This
        # matches the DockerSpawner-era home directory convention instead.
        return f"/home/{self.user.name}"

    @default("req_environment")
    def _req_environment_default(self):
        env = self.get_env()
        # jnotebook_image bakes ENV HOME=/home/jovyan (docker-stacks
        # default); point it at the real, auto-mounted LDAP home dir
        # instead so start.sh's privilege-drop hooks and the notebook
        # itself operate on the right directory (verified in ~/nb_test).
        env["HOME"] = self.req_homedir
        return ";".join(f"{k}={v}" for k, v in env.items())


c.JupyterHub.spawner_class = HTCondorNotebookSpawner

api_token = os.environ.get("JUPYTERHUB_API_TOKEN")
if not api_token:
    raise ValueError("JUPYTERHUB_API_TOKEN environment variable must be set")

c.JupyterHub.services = [
    {"name": "dask-gateway", "api_token": api_token}
]

# Define the environment variables for the user
async def define_environment(spawner):
    auth_state = await spawner.user.get_auth_state()
    if auth_state is None:
        raise RuntimeError("auth_state unavailable — please log out and log back in")
    spawner.environment["NB_UID"] = str(auth_state["user_attributes"]["uidNumber"][0])
    spawner.environment["NB_GID"] = str(auth_state["user_attributes"]["gidNumber"][0])
    spawner.environment["NB_USER"] = str(auth_state["user_attributes"]["uid"][0])
    # API calls go direct (port 8000 is reachable within ETP subnet)
    # public_address overrides what's used for dashboard links → routes through nginx/443
    spawner.environment["DASK_GATEWAY__ADDRESS"] = "http://bms1.etp.kit.edu:8000"
    spawner.environment["DASK_GATEWAY__PUBLIC_ADDRESS"] = "https://bms1.etp.kit.edu/clusters/"
    spawner.environment["DASK_GATEWAY__PROXY_ADDRESS"] = "gateway://bms1.etp.kit.edu:8000"
    spawner.environment["DASK_GATEWAY__AUTH__TYPE"] = "jupyterhub"

c.Spawner.pre_spawn_hook = define_environment
