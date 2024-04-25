#!/bin/bash

# enable LLDP on each port
ovs-vsctl set interface R1_OLT lldp:enable=true
# port from R1_OLT to R1_CPE1
ovs-vsctl set interface ovsp1 lldp:enable=true
# port from R1_OLT to R1_CPE2
ovs-vsctl set interface ovsp2 lldp:enable=true
# port from R1_OLT to R1_PE2
ovs-vsctl set interface ovsp3 lldp:enable=true

ovs-vsctl set interface R2_CMTS lldp:enable=true
# port from R2_CMTS to R2_CPE1
ovs-vsctl set interface ovsp4 lldp:enable=true
# port from R2_CMTS to R2_CPE2
ovs-vsctl set interface ovsp5 lldp:enable=true
# port from R2_CMTS to R2_PE1
ovs-vsctl set interface ovsp6 lldp:enable=true

# add mapping to bridges
ovs-vsctl add-aa-mapping R1_OLT 0 0
ovs-vsctl add-aa-mapping R2_CMTS 0 0

# add name visible in LLDP table 
ovs-vsctl set AutoAttach R1_OLT system_name="R1_OLT"
ovs-vsctl set AutoAttach R2_CMTS system_name="R2_CMTS"

ovs-vsctl set AutoAttach R1_OLT system_description="Region1_PE2_switch"
ovs-vsctl set AutoAttach R2_CMTS system_description="Region2_PE1_switch"

# set VLAN access ports
ovs-vsctl clear port ovsp1 trunks
ovs-vsctl clear port ovsp2 trunks
ovs-vsctl clear port ovsp4 trunks
ovs-vsctl clear port ovsp5 trunks

ovs-vsctl set port ovsp1 vlan_mode=access
ovs-vsctl set port ovsp2 vlan_mode=access
ovs-vsctl set port ovsp4 vlan_mode=access
ovs-vsctl set port ovsp5 vlan_mode=access

ovs-vsctl set port ovsp1 tag=10
ovs-vsctl set port ovsp2 tag=20
ovs-vsctl set port ovsp4 tag=10
ovs-vsctl set port ovsp5 tag=20

# set VLAN trunk ports
ovs-vsctl clear port ovsp3 trunks
ovs-vsctl clear port ovsp6 trunks

ovs-vsctl set port ovsp3 trunks=10,20
ovs-vsctl set port ovsp6 trunks=10,20

ovs-vsctl set port ovsp3 vlan_mode=trunk
ovs-vsctl set port ovsp6 vlan_mode=trunk
