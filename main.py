import csv
import os
import socket
import time
import logging
import sys
from ncclient import manager
from ncclient.xml_ import to_ele

NETCONF_TESTTOOL_PATH = "./netconf-testtool/netconf-testtool.jar"
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)
LOG = logging.getLogger(__name__)

def readCsvFile():
    LOG.info("Reading csv file")
    with open('devices.csv', 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def prepareProcesses(data):
    LOG.info("Preparing processes commands")
    processes = []
    JAVA_ARGS = os.getenv('JAVA_ARGS', "-Xmx5G")
    for device in data:
        if device["protocol"] == "cli":
            processes.append("python2.7 cli-testtool/mockdevice.py 0.0.0.0 {} 1 ssh /sample-topology/configs/cli/{}.json".format(device["port"],device["device_name"]))
        elif device["protocol"] == "netconf":
            command = "java {} -jar {} --schemas-dir schemas/{} --md-sal true --device-count {} --starting-port {}".format(JAVA_ARGS, NETCONF_TESTTOOL_PATH, device["schema_name"], device["count_of_devices"], device["starting_port"])
            if command not in processes:
                processes.append(command)
    return processes

def runProcesses(processes):
    for process in processes:
        LOG.info("Executing command: {}".format(process))
        os.system("{} &".format(process))

def pushConfigToNetconfTesttool(devices):
    for device in devices:
        if device["protocol"] == "netconf":
            LOG.info("Trying connect to a device {}".format(device["device_name"]))
            if not is_device_available(os.getenv('DOCKER_GWBRIDGE_IP', 'localhost'), device["port"], device["device_name"]):
                LOG.error("Cannot connect to a device {}".format(device["device_name"]))
                sys.exit(1)

            LOG.info("Updating config for device {}".format(device["device_name"]))
            config_file = "configs/netconf/{}/config.xml".format(device["device_name"])
            if os.path.isfile(config_file):
                if not push_config_to_device(device["port"], config_file):
                    LOG.error("Failed updating config for device {}".format(device["device_name"]))
            else:
                LOG.error("Cannot find config for device {}".format(device["device_name"]))

            operation_data_list = get_operation_files_path(device["device_name"])
            for operation_data in operation_data_list:
                LOG.info("pushing operation data: {}".format(str(operation_data)))
                push_operation_data_to_device(device["port"], operation_data)
            LOG.info("Device {} is ready".format(device["device_name"]))

def push_operation_data_to_device(port, operation_data):
    m = manager.connect(host=os.getenv('DOCKER_GWBRIDGE_IP', 'localhost'), port=port, username="frinx",
                        password="frinx", hostkey_verify=False)

    netconf_operation_data = open(str(operation_data)).read()
    netconf_operation_data = to_ele(netconf_operation_data)

    edit_oper = m.dispatch(to_ele(netconf_operation_data))
    m.commit()

    LOG.info(edit_oper)
    m.close_session()

def get_operation_files_path(device_name):
    operation_files_path = []
    for (root,dirs,files) in os.walk("configs/netconf/{}".format(device_name), topdown=True):
        for file in files:
            if file != "config.xml":
                operation_files_path.append("{}/{}".format(root, file))
    return operation_files_path

def push_config_to_device(port, config_file):
    LOG.info("Pushig config to device port: {}".format(str(port)))
    m = manager.connect(host=os.getenv('DOCKER_GWBRIDGE_IP'), port=port, username="frinx",
                        password="frinx", hostkey_verify=False)

    netconf_config = open(str(config_file)).read()
    edit_config = m.edit_config(netconf_config, target="candidate")
    m.commit()

    LOG.info(edit_config)
    m.close_session()
    if "ok" in str(edit_config):
        return True
    else:
        return False

def is_device_available(ip, port, device_name="unknown", attempts=1080):
    """
    Try connect to a device if its running
    There is default 1080 attempts (which is around 540sec=9min) one attempt take cca 0.5 sec
    - True: device is running
    - False: all attempts have been use device cannot be founded
    """
    attempt = 0
    while attempt <= attempts:
        attempt += 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, int(port)))
        if attempt % 20 == 0:
            LOG.info("Trying connect to a device {}. Attempts {}/{}".format(device_name, str(attempt), str(attempts)))
        if result == 0:
            sock.close()
            return True
        else:
            sock.close()
            time.sleep(0.5)
            continue
    return False

def createReadyFile():
    with open('/tmp/healthy', 'w') as f:
        f.write('sample-topology is ready!')

if __name__ == "__main__":
    devices = readCsvFile()
    processes = prepareProcesses(devices)
    runProcesses(processes)
    pushConfigToNetconfTesttool(devices)
    createReadyFile()
    os.system("sleep infinity")
