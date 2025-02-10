FROM rockylinux:9

RUN dnf update -y && \
    dnf install -y python3 python3-pip && \
    dnf clean all

# HTCondor
# RUN rpm --import http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor
# RUN dnf install -y https://research.cs.wisc.edu/htcondor/repo/24.x/htcondor-release-current.el9.noarch.rpm
# RUN dnf -y install epel-release && dnf clean all
# RUN dnf config-manager --set-enabled powertools
# RUN dnf -y install condor  && dnf clean all
RUN curl -o /tmp/RPM-GPG-KEY-HTCondor http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor && \
    rpm --import /tmp/RPM-GPG-KEY-HTCondor && \
    rm /tmp/RPM-GPG-KEY-HTCondor

RUN dnf install -y https://research.cs.wisc.edu/htcondor/repo/23.x/el9/x86_64/release/htcondor-release-23.x-1.el9.noarch.rpm
RUN dnf -y install epel-release && dnf clean all
RUN dnf config-manager --set-enabled powertools
RUN dnf -y install condor  && dnf clean all

# gateway
RUN pip3 install --no-cache-dir dask-gateway dask[distributed] notebook
# EXPOSE 8000 8786 8787

WORKDIR /app

CMD ["/bin/bash"]
