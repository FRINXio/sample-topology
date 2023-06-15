# Sample topology 

### devices file

You can specify requered cli and netconf devices in devices.csv file. 

- protocol - cli/netconf
- device_name - name of simulated device. In the case of a cli device, it is necessary that the name matches the config file
- port - port of simulated device
- schema_name - netconf device specific value. Need to match with schemas name
- count_of_devices - netconf device specific value. Count of devices
- starting_port - netconf device specific value. First port of netconf testool

