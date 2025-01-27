c = get_config()

# Set the JupyterHub IP and port
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.JupyterHub.hub_connect_ip = 'jupyterhub'
#c.JupyterHub.bind_url = 'http://

# Use authentication
c.JupyterHub.authenticator_class = "dummy"
# c.JupyterHub.authenticator_class = "LDAPAuthenticator"
# c.LDAPAuthenticator.server_address = "ldap.etp.kit.edu"
# c.LDAPAuthenticator.server_port = 636
# c.LDAPAuthenticator.tls_strategy = "on_connect" jj
# c.LDAPAuthenticator.lookup_dn = False
# c.LDAPAuthenticator.user_search_base ="dc=ekp,dc=physik,dc=uni-karlsruhe,dc=de"
# c.LDAPAuthenticator.bind_dn_template = ["uid={username},ou=people,dc=ekp,dc=physik,dc=uni-karlsruhe,dc=de"]

# Allow all users to log in
c.Authenticator.allow_all = True

# Disable XSRF protection (for testing purposes only)
# c.JupyterHub.disable_check_xsrf = True

# Specify the Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Set the Docker image for single-user servers
c.DockerSpawner.image = 'jupyter/base-notebook:latest'

#c.DockerSpawner.host_ip = '0.0.0.0'
#c.DockerSpawner.port = 8000
#c.DockerSpawner.args = ['--hub-api-url=http://127.0.0.1:8000/hub/api']
#c.DockerSpawner.hub_connect_url = "http://127.0.0.1:8000/hub/api"
# Set the notebook directory
c.DockerSpawner.notebook_dir = '/home/jovyan/work'

# Remove containers once they are stopped
c.DockerSpawner.remove = False
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'my_jupyterhub_jupyternet'
c.Spawner.debug = True
#c.Spawner.hub_ip_connect = '0.0.0.0'
#c.Spawner.hub_port_connect = 8000

#c.JupyterHub.hub_connect_url = 'http://0.0.0.0:8000'
""""
docker-compose down
docker-compose build
docker-compose up -d
"""

c.JupyterHub.api_tokens = {
    'cb96523ac867a52adc059df779f443d5ad56c7163c28fd17d9688fb31da0e5ca': 'jmustafi'
}

# ldap jupyter auth nutzen für sssd
# 