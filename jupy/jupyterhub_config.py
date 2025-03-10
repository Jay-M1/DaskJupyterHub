c = get_config()

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

# Allow all users to log in
c.Authenticator.allow_all = True

# Specify the Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Set the Docker image for single-user servers
c.DockerSpawner.image = 'jupyter/base-notebook:latest'
c.DockerSpawner.notebook_dir = '/home/jovyan/work'

# Remove containers once they are stopped
c.DockerSpawner.remove = False
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'my_jupyterhub_jupyternet'
c.Spawner.debug = True
