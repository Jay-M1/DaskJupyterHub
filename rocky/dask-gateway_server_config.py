# Configure the gateway to use PBS
c.DaskGateway.backend_class = (
    "dask_gateway_htcondor.htcondor.HTCondorBackend"
)

# The resource limits for a worker
c.HTCondorClusterConfig.worker_memory = '16 G'
c.HTCondorClusterConfig.worker_cores = 8

# Increase startup timeouts to 5 min (600 seconds) each
c.HTCondorBackend.cluster_start_timeout = 600
c.HTCondorBackend.worker_start_timeout = 600

c.HTCondorClusterConfig.docker_image = "giffels/coffea-dask-cc7-gateway"
c.HTCondorClusterConfig.extra_jdl = {"accounting_group": "dask"}
c.HTCondorClusterConfig.staging_directory = "/tmp/dask/.dask-gateway/"
c.HTCondorClusterConfig.tls_worker_node_prefix_path = ""

print(">>> custom config executed")
