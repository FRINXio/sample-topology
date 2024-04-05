#!/bin/bash


ovs-vsctl add-br R1_OLT
ovs-vsctl add-br R1_CMTS


ovs-vsctl add-port R1_OLT ovsp1
ovs-vsctl add-port R1_OLT ovsp2
ovs-vsctl add-port R1_OLT ovsp3

ovs-vsctl add-port R1_CMTS ovsp4
ovs-vsctl add-port R1_CMTS ovsp5 
ovs-vsctl add-port R1_CMTS ovsp6

ovs-vsctl show
