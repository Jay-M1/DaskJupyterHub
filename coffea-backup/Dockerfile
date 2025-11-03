FROM coffeateam/coffea-base-almalinux9@sha256:0199f2f3014499fc6518e4dc1fd9da21d7ba0e544e8b8dc184a1afee056ab72b

RUN python3.10 -m venv /opt/python310-venv
COPY requirements.txt .
RUN /opt/python310-venv/bin/pip install --upgrade pip && \
    /opt/python310-venv/bin/pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/python310-venv/bin:$PATH"
