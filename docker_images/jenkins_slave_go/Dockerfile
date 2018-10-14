FROM library/debian:stretch-slim

ENV GO_VERSION=1.9.2 \
    GOPATH=/opt/gopath \
    GOROOT=/opt/go \
    PKG_CONFIG_PATH=/usr/lib/pkgconfig
ENV PATH=$PATH:$GOROOT/bin:$GOPATH/bin

WORKDIR /opt

RUN apt-get update -qq \
    && apt-get dist-upgrade -qqy \
    && apt-get install -y --no-install-recommends \
    apt-transport-https \
    build-essential \
    bzip2 \
    ca-certificates \
    curl \
    git \
    gnupg2 \  
    jq \   
    libffi-dev \
    libssl-dev \
    libtool \
    libltdl-dev \
    libvips \
    libvips-dev \
    libyaml-0-2 \
    libyaml-dev \
    openssl \
    pkg-config \
    python-dev python3-dev python-pip python-yaml \
    software-properties-common \
    wget \
    && wget -q https://storage.googleapis.com/golang/go${GO_VERSION}.linux-amd64.tar.gz \
    && tar zxf go${GO_VERSION}.linux-amd64.tar.gz && rm go${GO_VERSION}.linux-amd64.tar.gz \    
    && mkdir /opt/gopath \
    && go get golang.org/x/tools/cmd/goimports \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/debian \
     $(lsb_release -cs) \
     stable" \
    && groupadd -g 497 docker \
    && apt-get update && apt-get install -y docker-ce \
    && wget -O /usr/bin/ec2metadata http://s3.amazonaws.com/ec2metadata/ec2-metadata \
    && chmod u+x /usr/bin/ec2metadata \
    && curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
    && chmod +x ./kubectl && mv ./kubectl /usr/local/bin/kubectl \
    && curl -LO https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64 && chmod +x kops-linux-amd64 && mv kops-linux-amd64 /usr/local/bin/kops \
    && apt-get -y autoremove && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

RUN  pip install --upgrade pip \
     && pip install setuptools wheel
RUN  pip install behave nose docker-compose awscli

RUN go get github.com/jstemmer/go-junit-report \
    && go get github.com/stretchr/testify/assert \
    && go get github.com/axw/gocov/gocov \
    && go get github.com/AlekSi/gocov-xml

COPY s3-cli /usr/bin/s3cli

RUN useradd -u 1000 -s /bin/bash -d /home/jenkins -m -G docker,sudo -U jenkins \
    && echo "jenkins ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER jenkins