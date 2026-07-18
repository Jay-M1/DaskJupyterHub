import os
from typing import TYPE_CHECKING

from traitlets.config import Configurable

from dask_gateway_server.options import Float, Integer, Options

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

# Per-cluster options the user can pick in the notebook via gateway.cluster_options().
# Default worker_gpus = 0 -> normal CPU worker, no GPU is requested.
def options_handler(options):
    return {
        "worker_cores": options.worker_cores,
        "worker_memory": f"{options.worker_memory} G",
        "worker_gpus": options.worker_gpus,
    }

c.Backend.cluster_options = Options(
    Integer("worker_cores", default=1, min=1, max=8, label="Cores per worker"),
    Float("worker_memory", default=2, min=1, max=32, label="Memory per worker (GiB)"),
    Integer("worker_gpus", default=0, min=0, max=1, label="GPUs per worker"),
    handler=options_handler,
)

# Increase startup timeouts to 5 min (600 seconds) each
c.HTCondorBackend.cluster_start_timeout = 6000000000000000000000 # for job sched
c.HTCondorBackend.worker_start_timeout = 6000000000000000000000

# Automatically shut down clusters idle for more than 1 hour (no active tasks)
c.HTCondorClusterConfig.idle_timeout = 3600

c.HTCondorClusterConfig.docker_image = "uhsur/coffea-base-almalinux9:2026-07-09"
c.HTCondorClusterConfig.extra_jdl = {
    "accounting_group": "dask",
    "requirements": '(HasDocker == true)',
}
# GPU workers run on the NEMO GPU drones. Those provide no Docker (only
# Apptainer), so the backend submits them in the container universe with a
# docker:// image URL (see dask-gateway-htcondor). These entries override
# extra_jdl for GPU workers:
# - requirements: replaces the HasDocker constraint, GPU drones have no Docker
# - +RemoteJob / +RequestWalltime: NEMO START requirements, without them the
#   job never matches a NEMO drone
# - request_disk: apptainer pulls and converts the docker image inside the
#   job scratch directory
# - container_image: GPU workers use the -gpu image variant (same Python
#   stack as the base image plus CuPy), built from coffea-gpu/Dockerfile
c.HTCondorClusterConfig.gpu_extra_jdl = {
    "requirements": "True",
    "request_disk": "25 GB",
    "+RemoteJob": "True",
    "+RequestWalltime": "7200",
    "container_image": "docker://uhsur/coffea-base-almalinux9:2026-07-10-gpu",
}
c.HTCondorClusterConfig.staging_directory = "/var/lib/dask-gateway/{username}/"
c.HTCondorClusterConfig.htcondor_staging_directory = "/var/lib/dask-gateway/{username}/htcondor/"
c.HTCondorClusterConfig.tls_worker_node_prefix_path = ""
c.HTCondorBackend.scheduler_docker_image = "uhsur/coffea-base-almalinux9:2026-07-09"
c.HTCondorBackend.scheduler_universe = "docker"

c.DaskGateway.authenticator_class = "dask_gateway_server.auth.JupyterHubAuthenticator"
c.JupyterHubAuthenticator.jupyterhub_api_token = os.getenv("JUPYTERHUB_API_TOKEN")
c.JupyterHubAuthenticator.jupyterhub_api_url = "http://127.0.0.1:8555/hub/api"
