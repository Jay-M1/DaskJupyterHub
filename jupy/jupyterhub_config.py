import os

c = get_config() # type: ignore[name-defined]  # noqa: F821

# Set the JupyterHub IP and port
c.JupyterHub.bind_url = 'http://0.0.0.0:8555'
c.JupyterHub.hub_connect_ip = 'jupyterhub'

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
_key_file = "/srv/jupyterhub/auth_state.key"
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

# Specify the Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Set the Docker image for single-user servers
c.DockerSpawner.image = 'jnotebook_image'
#c.DockerSpawner.notebook_dir = '/home/{username}/work'
# Remove containers once they are stopped
c.DockerSpawner.remove = False # True??
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'jupyterhub-htcondor_jupyternet' # jupyeternet???
c.Spawner.debug = True
#c.DockerSpawner.debug = True
#c.DockerSpawner.cmd = ["start-notebook.sh"]

c.DockerSpawner.volumes = {
    '/home/{username}':  '/home/{username}'
}
c.DockerSpawner.extra_create_kwargs = {
    "user": "root" # Can also be an integer UID
}

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
    # Route gateway traffic through nginx so dashboard links are HTTPS, not port 8000
    spawner.environment["DASK_GATEWAY__ADDRESS"] = "https://bms1.etp.kit.edu"
    spawner.environment["DASK_GATEWAY__PROXY_ADDRESS"] = "gateway://bms1.etp.kit.edu:8000"
    spawner.environment["DASK_GATEWAY__AUTH__TYPE"] = "jupyterhub"

c.Spawner.pre_spawn_hook = define_environment
