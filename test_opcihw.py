# -*- coding: UTF-8 -*-
import pytest
import time
from . import ssh_wrapper
from .opci_helper import *
import json
from pytest_testrail.plugin import pytestrail
import sys
cap = "initial cap"


@pytest.fixture(autouse=True)
def cap_init():
    pytest.cap_text = ''
#    print("cap fixture created")


#@pytest.fixture(scope='module')
def cap_get(capsys):
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
#    globals()['cap_text'] = out
#    pytest.cap_text = out
    return out


def cap_set(capout):
#    globals()['cap_text'] = out
    pytest.cap_text = capout
    return capout


# Get ssh_wrapper client
ssh_client = None


@pytest.fixture(autouse=True, scope='module')
def get_ssh_client(getip,request):
    """Get ssh client object"""
    global ssh_client
    ssh_client = ssh_wrapper.SshClient(getip)

    def fin():
        ssh_client.close()
    request.addfinalizer(fin)
#    return ssh_client


model_partno={'qsmi': 'VEN026QSNWM00', 'r211': 'VEN026QSNWM50', '3smi': 'VEN032FSNWM00', 'cc48smi': 'VEN048CSVWM00', '8u2i': 'VEN075ULPWB10'}
'''
Get the key from dictionary which has the given value
'''
def getKeysByValue(dictOfElements, valueToFind):
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            return item[0]
    return "unknown"


# Get Model no.
@pytest.fixture(scope='module')
def model(getmodel):
    """Get device model number"""
    if getmodel == "auto":
        cmd = "curl http://127.0.0.1:5000/sysinfo/model"
        r = ssh_client.execute(cmd)
        m = json.loads(r['out'])['Model']
        return getKeysByValue(model_partno, m)
    else:
        return getmodel


#@pytestrail.case('C4055')
@pytestrail.case('C0')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.hw
def test_reset_button():
    cmd = "curl http://127.0.0.1:5000/sysinfo/resetbutton"
    r = ssh_client.execute(cmd)
    print(json.loads(r['out'])['Reset Button'])
    assert r['retval'] == 0 and json.loads(r['out'])['Reset Button'] in ['1','0']


@pytestrail.case('C0')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.hw
def test_sn(model):
    cmd = "curl http://127.0.0.1:5000/sysinfo/SN"
    r = ssh_client.execute(cmd)
    print(json.loads(r['out'])['Serial Number'])
    assert r['retval'] == 0


@pytestrail.case('C5310')
@pytest.mark.hw
@pytest.mark.debug
def test_mac(capsys):
    cmd = "cat /sys/class/net/eth0/address;cat /sys/class/net/wlan0/address;hcitool dev"
    r = ssh_client.execute(cmd)
    print(r['out'])
    print("Please check the mac address, to make sure they are continuous and match the lable/csv")
    cap_set(cap_get(capsys))
    assert r['retval'] == 0


@pytestrail.case('C4061')
@pytest.mark.hw
@pytest.mark.debug
def test_cputemp():
    cmd = "cat /sys/class/hwmon/hwmon1/temp*_input"
    r = ssh_client.execute(cmd)
    print()
    print(r['out'])
    print("Please check the temperatures are normal")
    cap_set(r['out'])
    assert r['retval'] == 0


