import os
from typing import TYPE_CHECKING

from traitlets.config import Configurable

if TYPE_CHECKING:
    c = Configurable()

# Configure the gateway to use HTCondor
c.DaskGateway.backend_class = ( 
            "dask_gateway_htcondor.htcondor.HTCondorBackend"
            )
c.DaskGateway.public_url = "https://bms1.etp.kit.edu/clusters/"

# The resource limits for a worker
c.HTCondorClusterConfig.worker_memory = '2 G'
c.HTCondorClusterConfig.worker_cores = 1

# Increase startup timeouts to 5 min (600 seconds) each
c.HTCondorBackend.cluster_start_timeout = 6000000000000000000000 # for job sched
c.HTCondorBackend.worker_start_timeout = 6000000000000000000000

# Automatically shut down clusters idle for more than 1 hour (no active tasks)
c.HTCondorClusterConfig.idle_timeout = 3600

c.HTCondorClusterConfig.docker_image = "uhsur/coffea-base-almalinux9:latest"
c.HTCondorClusterConfig.extra_jdl = {
    "accounting_group": "dask",
    "requirements": '(HasDocker == true)',
}
c.HTCondorClusterConfig.staging_directory = "/var/lib/dask-gateway/{username}/"
c.HTCondorClusterConfig.htcondor_staging_directory = "/var/lib/dask-gateway/{username}/htcondor/"
c.HTCondorClusterConfig.tls_worker_node_prefix_path = ""
c.HTCondorBackend.scheduler_docker_image = "uhsur/coffea-base-almalinux9:latest"
c.HTCondorBackend.scheduler_universe = "docker"

c.DaskGateway.authenticator_class = "dask_gateway_server.auth.JupyterHubAuthenticator"
c.JupyterHubAuthenticator.jupyterhub_api_token = os.getenv("JUPYTERHUB_API_TOKEN")
c.JupyterHubAuthenticator.jupyterhub_api_url = "http://127.0.0.1:8555/hub/api"
