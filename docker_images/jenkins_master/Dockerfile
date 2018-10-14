FROM jenkinsci/blueocean

USER root
RUN echo http://dl-2.alpinelinux.org/alpine/edge/community/ >> /etc/apk/repositories
RUN apk --no-cache add shadow
RUN groupadd -g 497 dockergroup
RUN usermod -aG 497 jenkins
USER jenkins