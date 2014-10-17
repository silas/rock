FROM centos:centos7

MAINTAINER RockStack <packages@rockstack.org>

RUN rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-2.noarch.rpm
RUN rpm -Uvh http://dl.rockstack.org/rpm/stable/el/rock-release.rpm

RUN yum install -y \
    rock \
    rock-devtools \
    rock-runtime-node08 \
    rock-runtime-node010 \
    rock-runtime-perl518 \
    rock-runtime-perl520 \
    rock-runtime-php54 \
    rock-runtime-php55 \
    rock-runtime-python27 \
    rock-runtime-python34 \
    rock-runtime-ruby20 \
    rock-runtime-ruby21
