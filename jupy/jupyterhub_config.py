import pwd
import os
import warnings

c = get_config() # type: ignore[name-defined]

# Set the JupyterHub IP and port
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
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
c.CryptKeeper.keys = [os.urandom(32)]

# Allow all users to log in
c.Authenticator.allow_all = True

# Specify the Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Set the Docker image for single-user servers
c.DockerSpawner.image = 'jnotebook_image'
#c.DockerSpawner.notebook_dir = '/home/{username}/work'

# Remove containers once they are stopped
c.DockerSpawner.remove = False
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'my_jupyterhub_jupyternet'
c.Spawner.debug = True
#c.DockerSpawner.debug = True
#c.DockerSpawner.cmd = ["start-notebook.sh"]

# Define the environment variables for the user
async def define_environment(spawner):
    auth_state = await spawner.user.get_auth_state()
    warnings.warn(f"---------------------> {auth_state}")
    spawner.environment["NB_UID"] = str(auth_state["user_attributes"]["uidNumber"][0])
    spawner.environment["NB_GID"] = str(auth_state["user_attributes"]["gidNumber"][0])
    spawner.environment["NB_USER"] = str(auth_state["user_attributes"]["uid"][0])

c.Spawner.pre_spawn_hook = define_environment
