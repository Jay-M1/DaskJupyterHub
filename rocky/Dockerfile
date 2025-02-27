FROM rockylinux:9

RUN dnf -y swap curl-minimal curl

RUN curl -fsSL https://get.htcondor.org | /bin/bash -s -- --no-dry-run

RUN dnf -y install python3
RUN python3 -m ensurepip --default-pip
RUN python3 -m pip install --upgrade pip
RUN pip3 install dask-gateway

RUN dnf clean all

EXPOSE 9618

WORKDIR /work

COPY . .

ENTRYPOINT ["/usr/sbin/condor_master", "-f"]
