clone this:
`git clone https://github.com/hellt/vrnetlab && cd vrnetlab`

for deployment use this files:
`vrnetlab/xrv9k`

original file `common/vrnetlab.py`
replace by adjusted file attached in this folder

original file `vrnetlab/xrv9k/docker/launch.py`
replace by adjusted file attached in this folder

.qcow2 should be in this format:
`xrv9k-fullk9-x-5.3.4.qcow2`




1. first add R1_OLT and R2_CMTS before deploying topology
   `sudo ./openswitch1.sh`

2. deploy topology by:
   `sudo containerlab deploy --topo frinx_topo_1.yml`

3. configure LLDP on switches by:
   `sudo ./openswitch2.sh`

4. deploy graph by:
   `containerlab graph -t frinx_topo_1.yml`

5. open `http://127.0.0.1:50080/` in browser

6. for destroying lab use:
   `sudo containerlab destroy --topo frinx_topo_1.yml`



useful commands:

from nokia, check LLDP by:
`A:admin@R1_PE2# show system lldp neighbor`

from cisco:
`RP/0/0/CPU0:R2_CPE2#show lldp neighbors`

for deleting openvswitch port use:
`sudo ovs-vsctl del-port ovsp1`

for deleting openvswitch bridge use:
`sudo ovs-vsctl del-br R2_CMTS`

for manual adding port(this will be done by deploying topology):
`ovs-vsctl add-port R1_OLT ovsp1`

for show openvswitch:
`sudo ovs-vsctl show`

for filtering uuid:
`sudo ovs-vsctl --columns=_uuid list AutoAttach`
