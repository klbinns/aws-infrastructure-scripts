FROM gradle

RUN apt-get update && apt-get install -y \ 
    python-pip \
    && pip --no-input install awscli \
    && apt-get -y autoremove && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd -u 1000 -s /bin/bash -d /home/jenkins -m -G sudo -U jenkins \
    && echo "jenkins ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER jenkins