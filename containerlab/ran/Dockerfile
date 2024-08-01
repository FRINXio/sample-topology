FROM ubuntu

# Builds a software only BTS from srsran project
# This bts does not require any hardware, since it is built with zeroMQ as a "mock" for radio traffic
# Note that srsran can be installed into ubuntu as a package, but that package does not support the zermoMQ mock

# from https://docs.srsran.com/projects/4g/en/latest/general/source/1_installation.html
RUN apt-get update && \
	apt-get install -y libzmq3-dev build-essential git libtool pkg-config fftw3 fftw3-dev libmbedtls-dev libsctp-dev libboost-program-options-dev libconfig++-dev cmake

# from https://docs.srsran.com/projects/4g/en/next/app_notes/source/zeromq/source/index.html
WORKDIR /root/

RUN git clone https://github.com/srsRAN/srsRAN_4G.git
WORKDIR /root/srsRAN_4G
RUN mkdir build
WORKDIR /root/srsRAN_4G/build
RUN cmake ../
RUN make -j8
RUN make install

RUN srsran_install_configs.sh user

RUN apt-get update && \
	apt-get install -y lldpd

CMD lldpd; ./srsenb/src/srsenb --rf.device_name=zmq --rf.device_args="fail_on_disconnect=true,tx_port=tcp://*:2000,rx_port=tcp://localhost:2001,id=enb,base_srate=23.04e6"
