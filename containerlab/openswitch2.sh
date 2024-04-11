#!/bin/bash


# enable LLDP on each port

ovs-vsctl set interface R1_OLT lldp:enable=true
# port from R1_OLT to R1_CPE1
ovs-vsctl set interface ovsp1 lldp:enable=true
# port from R1_OLT to R1_CPE2
ovs-vsctl set interface ovsp2 lldp:enable=true
# port from R1_OLT to R1_PE2
ovs-vsctl set interface ovsp3 lldp:enable=true

ovs-vsctl set interface R1_CMTS lldp:enable=true
# port from R1_CMTS to R2_CPE1
ovs-vsctl set interface ovsp4 lldp:enable=true
# port from R1_CMTS to R2_CPE2
ovs-vsctl set interface ovsp5 lldp:enable=true
# port from R1_CMTS to R2_PE1
ovs-vsctl set interface ovsp6 lldp:enable=true


# add mapping to bridges
ovs-vsctl add-aa-mapping R1_OLT 0 0
ovs-vsctl add-aa-mapping R1_CMTS 0 0


# add name visible in LLDP table 
ovs-vsctl set AutoAttach R1_OLT system_name="R1_OLT"
ovs-vsctl set AutoAttach R1_CMTS system_name="R1_CMTS"
