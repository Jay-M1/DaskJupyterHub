FROM rockylinux:9

RUN useradd -m -u 1000 jovyan

RUN dnf -y swap curl-minimal curl

RUN curl -fsSL https://get.htcondor.org | /bin/bash -s -- --no-dry-run


RUN dnf -y install python3 git
RUN python3 -m ensurepip --default-pip
RUN python3 -m pip install --upgrade pip
RUN pip3 install dask-gateway dask-gateway-server[local]
RUN pip install git+https://github.com/giffels/dask-gateway-htcondor.git
RUN pip install "SQLAlchemy<2.0"

RUN dnf clean all

EXPOSE 9618

WORKDIR /work

COPY . .

RUN chmod +x start.sh

RUN dnf install -y sudo

CMD ["./start.sh"]
