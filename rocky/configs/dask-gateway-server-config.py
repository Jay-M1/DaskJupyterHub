# Configure the gateway to use HTCondor
c.DaskGateway.backend_class = ( # type: ignore[name-defined]
            "dask_gateway_htcondor.htcondor.HTCondorBackend"
            )

# The resource limits for a worker
c.HTCondorClusterConfig.worker_memory = '16 G' # type: ignore[name-defined]
c.HTCondorClusterConfig.worker_cores = 8 # type: ignore[name-defined]

# Increase startup timeouts to 5 min (600 seconds) each
c.HTCondorBackend.cluster_start_timeout = 600 # type: ignore[name-defined]
c.HTCondorBackend.worker_start_timeout = 600 # type: ignore[name-defined]

c.HTCondorClusterConfig.docker_image = "uhsur/coffea-base-almalinux9:latest" # type: ignore[name-defined]
c.HTCondorClusterConfig.extra_jdl = {"accounting_group": "dask"} # type: ignore[name-defined]
c.HTCondorClusterConfig.staging_directory = "/tmp/dask/.dask-gateway/" # type: ignore[name-defined]
c.HTCondorClusterConfig.tls_worker_node_prefix_path = "" # type: ignore[name-defined]

