FROM centos:centos7

MAINTAINER RockStack <packages@rockstack.org>

RUN yum install epel-release -y
RUN rpm -Uvh http://dl.rockstack.org/rpm/stable/el/rock-release.rpm

RUN yum install -y \
    rock \
    rock-devtools \
    rock-runtime-node010 \
    rock-runtime-node012 \
    rock-runtime-perl518 \
    rock-runtime-perl520 \
    rock-runtime-php54 \
    rock-runtime-php55 \
    rock-runtime-python27 \
    rock-runtime-python34 \
    rock-runtime-ruby20 \
    rock-runtime-ruby21 \
    rock-runtime-ruby22
