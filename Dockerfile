FROM frinx/netconf-testtool:latest as TESTTOOL

FROM python:2.7-alpine
LABEL org.opencontainers.image.source="https://github.com/FRINXio/sample-topology"

RUN apk add git

# Install dependencies for cryptography
RUN apk add gcc musl-dev python-dev libffi-dev openssl-dev cargo

RUN apk add --no-cache --upgrade bash
RUN apk add --update openssh
RUN apk add --update iptables
RUN apk add --no-cache netcat-openbsd

# Install dependencies for ncclient
RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt

RUN apk add ulogd

# Java 17
# Using Microsoft's Java 17 compatible with alpine (musl) linux
RUN wget https://aka.ms/download-jdk/microsoft-jdk-17.0.7-alpine-x64.tar.gz
RUN tar -xzvf microsoft-jdk-17.0.7-alpine-x64.tar.gz
RUN ln -sf /jdk-17.0.7+7/bin/java /bin/java

WORKDIR /sample-topology

COPY ./requirements.txt ./requirements.txt

# cli testtool source
RUN pip install typing
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/FRINXio/yang-schemas.git schemas
RUN git clone --branch v6.0.0 https://github.com/FRINXio/cli-testtool.git

COPY ./ ./

# netconf testtool binary
COPY --from=TESTTOOL /opt/netconf-testtool-executable.jar ./netconf-testtool/netconf-testtool.jar
RUN chmod +r ./netconf-testtool/netconf-testtool.jar
