# RAN resources

This folder contains resources related to running RAN network on top of the frinx containerlab topology


## SRSRAN

This is currently using the SRSRAN open-source implementation of a RAN network (software only)

https://docs.srsran.com/projects/4g/en/latest/index.html


### BTS

A base station can be built from the provided Dockerfile.
The dockerfile builds the BTS software that can be run without a real hardware radios. It uses a zero MQ internally.
It also runs LLDP.

Resources:
https://docs.srsran.com/projects/4g/en/next/app_notes/source/zeromq/source/index.html

#### How to

1. build the container `docker build -t bts .` (takes a long time)
2. Add to containerlab topology:
```
  nodes:
    bts1:
      image: bts
      kind: linux
      mgmt-ipv4: 172.20.20.201

...

  - endpoints: ["srsenb:eth1", "R1_PE1:eth4"]

```





// TODO add the backend/core services from SRSRAN behind our datacenter PE
// TODO add a client "device" from the SRSRAN connected to the BTS
