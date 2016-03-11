FROM ubuntu:14.04
MAINTAINER Dan Leehr <dan.leehr@duke.edu>

# fetchChromSizes can use mysql, wget, or FTP
RUN apt-get update && apt-get install -y \
  curl \
  wget \
  bedtools

WORKDIR /usr/local/bin

# Fetch tools from hgdownload and place in /usr/local/bin
RUN curl -SLO http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/bedToBigBed
RUN curl -SLO http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/fetchChromSizes
RUN curl -SLO http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/hubCheck
RUN chmod +x *

# Install python dependencies
RUN apt-get install -y \
  python2.7 \
  python-dev \
  python-pip \
  build-essential \
  libyaml-dev

# Install python requirements before rest of code, to avoid unnecessary cache invalidations
RUN mkdir -p /opt/TrackHubGenerator
COPY python/requirements.txt /opt/TrackHubGenerator/requirements.txt
RUN pip install -r /opt/TrackHubGenerator/requirements.txt

# Add local code
COPY . /opt/TrackHubGenerator

WORKDIR /opt/TrackHubGenerator/
ENV PATH /opt/TrackHubGenerator:$PATH
CMD ["make"]
