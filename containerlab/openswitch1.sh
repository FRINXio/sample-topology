#!/bin/bash

# remove existing bridges
ovs-vsctl del-br R1_OLT
ovs-vsctl del-br R2_CMTS

# adding two bridges
ovs-vsctl add-br R1_OLT
ovs-vsctl add-br R2_CMTS
