FROM ubuntu:14.04
MAINTAINER Dan Leehr <dan.leehr@duke.edu>

# fetchChromSizes can use mysql, wget, or FTP
RUN apt-get update && apt-get install -y \
  curl \
  wget \
  bedtools

WORKDIR /usr/local/bin

# Fetch tools from hgdownload and place in /usr/local/bin
RUN curl -SLO http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/bedGraphToBigWig
RUN curl -SLO http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/fetchChromSizes
RUN curl -SLO http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/hubCheck
RUN curl -SLO http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/liftOver
RUN chmod +x *

# Install python dependencies
RUN apt-get install -y \
  python3 \
  python3-dev \
  python3-pip \
  build-essential \
  libyaml-dev

# Add local code
RUN mkdir -p /opt/TrackHubGenerator
COPY . /opt/TrackHubGenerator
WORKDIR /opt/TrackHubGenerator/python

RUN pip3 install -r requirements.txt

WORKDIR /opt/TrackHubGenerator/
ENV PATH /opt/TrackHubGenerator:$PATH
CMD ["make"]
