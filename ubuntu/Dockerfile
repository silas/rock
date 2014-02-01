FROM ubuntu:12.04

MAINTAINER RockStack <packages@rockstack.org>

RUN echo "deb http://us.archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y curl

RUN curl -so /tmp/rock-release-precise.deb http://dl.rockstack.org/deb/rock-release-precise.deb && \
    dpkg -i /tmp/rock-release-precise.deb && \
    rm -f /tmp/rock-release-precise.deb

RUN apt-get update
RUN apt-get install -y \
    rock \
    rock-devtools \
    rock-runtime-node08 \
    rock-runtime-node010 \
    rock-runtime-perl516 \
    rock-runtime-perl518 \
    rock-runtime-php54 \
    rock-runtime-php55 \
    rock-runtime-python27 \
    rock-runtime-python33 \
    rock-runtime-ruby19 \
    rock-runtime-ruby20 \
    rock-runtime-ruby21
