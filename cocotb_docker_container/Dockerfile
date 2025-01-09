FROM debian:bookworm-slim

RUN apt-get update

RUN apt-get install -y python3 \
    python3-venv \
    python3-pip \
    libpython3-dev \
    ghdl \
    make \
    nano


RUN mkdir cocotb

COPY ext_files ./cocotb/

RUN cd cocotb

RUN python3 -m venv venv

RUN ./venv/bin/pip3 install cocotb

RUN . ./venv/bin/activate

RUN cd cocotb/Testbench/

