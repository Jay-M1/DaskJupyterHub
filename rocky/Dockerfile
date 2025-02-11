# FROM rockylinux:9

# RUN dnf update -y && \
#     dnf install -y python3 python3-pip && \
#     dnf install -y pcre2-tools && \
#     dnf clean all

# # HTCondor
# RUN update-crypto-policies --set LEGACY
# RUN rpm --import http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor
# RUN dnf install -y https://research.cs.wisc.edu/htcondor/repo/24.x/htcondor-release-current.el9.noarch.rpm
# RUN dnf -y install epel-release && dnf clean all
# # RUN dnf config-manager --set-enabled powertools
# RUN dnf -y install condor  && dnf clean all
# RUN update-crypto-policies --set LEGACY

# # gateway
# RUN pip3 install --no-cache-dir dask-gateway dask[distributed] notebook
# # EXPOSE 8000 8786 8787

# WORKDIR /app

# CMD ["/bin/bash", "-c", \
#     "update-crypto-policies --set LEGACY && /bin/bash"]

# Use the official Rocky Linux 9 image as the base
# Use the official Rocky Linux 9 image as the base
# Use the official Rocky Linux 9 image as the base
FROM rockylinux:9

# Replace curl-minimal with the full curl package
RUN dnf -y swap curl-minimal curl && dnf clean all

# Install HTCondor using the official installation script
RUN curl -fsSL https://get.htcondor.org | /bin/bash -s -- --no-dry-run

# Expose necessary ports (if any)
EXPOSE 9618

WORKDIR /work

COPY . .

# Set the entrypoint to start HTCondor
ENTRYPOINT ["/usr/sbin/condor_master", "-f"]

