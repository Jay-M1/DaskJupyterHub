import os
from typing import TYPE_CHECKING

from traitlets.config import Configurable

if TYPE_CHECKING:
    c = Configurable()

# Configure the gateway to use HTCondor
c.DaskGateway.backend_class = ( 
            "dask_gateway_htcondor.htcondor.HTCondorBackend"
            )
c.DaskGateway.public_url = "http://lx5:8000"

# The resource limits for a worker
c.HTCondorClusterConfig.worker_memory = '16 G'
c.HTCondorClusterConfig.worker_cores = 8

# Increase startup timeouts to 5 min (600 seconds) each
c.HTCondorBackend.cluster_start_timeout = 600
c.HTCondorBackend.worker_start_timeout = 600

c.HTCondorClusterConfig.docker_image = "uhsur/coffea-base-almalinux9:latest"
c.HTCondorClusterConfig.extra_jdl = {
    "accounting_group": "dask",
    "requirements": '(HasDocker == true)',
    "log":    "/var/lib/condor/dask/job.$(ClusterId).$(ProcId).log",
    "output": "/var/lib/condor/dask/job.$(ClusterId).$(ProcId).out",
    "error":  "/var/lib/condor/dask/job.$(ClusterId).$(ProcId).err",
}
c.HTCondorClusterConfig.staging_directory = "/tmp/.dask-gateway/"
c.HTCondorClusterConfig.tls_worker_node_prefix_path = ""
c.HTCondorBackend.scheduler_docker_image = "uhsur/coffea-base-almalinux9:latest"
c.HTCondorBackend.scheduler_universe = "docker"

c.DaskGateway.authenticator_class = "dask_gateway_server.auth.JupyterHubAuthenticator"
c.JupyterHubAuthenticator.jupyterhub_api_token = os.getenv("JUPYTERHUB_API_TOKEN")
c.JupyterHubAuthenticator.jupyterhub_api_url = "http://lx5.etp.kit.edu:8555/hub/api"
