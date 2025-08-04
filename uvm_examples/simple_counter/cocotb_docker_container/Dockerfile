FROM debian:bookworm-slim

RUN apt-get update

# Install python packages and git
RUN apt-get install -y python3 \
    python3-venv \
    python3-pip \
    libpython3-dev \
    make \
    nano \
    git 

# Install build packages for nvc
RUN apt-get install -y build-essential automake autoconf \
flex check llvm-dev pkg-config zlib1g-dev libdw-dev \
libffi-dev libzstd-dev

# Clone and build nvc
RUN git clone https://github.com/nickg/nvc

WORKDIR /nvc/

RUN ./autogen.sh
RUN mkdir build

WORKDIR /nvc/build

RUN ../configure
RUN make
RUN make install

WORKDIR /

# Setup cocotb and run
RUN mkdir cocotb

COPY ext_files ./cocotb/

RUN cd cocotb

RUN python3 -m venv venv

RUN ./venv/bin/pip3 install cocotb
RUN ./venv/bin/pip3 install fastcrc
RUN ./venv/bin/pip3 install pyuvm

COPY config_files/Makefile.nvc /venv/lib64/python3.11/site-packages/cocotb/share/makefiles/simulators/

ENV PATH="/venv/bin:$PATH"

WORKDIR /cocotb/Testbench/

