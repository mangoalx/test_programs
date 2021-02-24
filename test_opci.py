# -*- coding: UTF-8 -*-
import pytest
import time
from . import ssh_wrapper
from .opci_helper import *
import json
from pytest_testrail.plugin import pytestrail
import sys
# from .conftest import *


# For initialize cap_text before starting each test case.
# it is autouse so apply to each case, and with a function scope
@pytest.fixture(autouse=True)
def cap_init():
    pytest.cap_text = ''
#    print("cap fixture created")


# read out captured stdout content
# @pytest.fixture(scope='module')
def cap_get(capsys):
    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)
#    globals()['cap_text'] = out
#    pytest.cap_text = out
    return out


# Function used to set cap_text, which will be add to comment in the report
def cap_set(capout):
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


@pytestrail.case('C18342')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.debug
def test_power_sensors(model, capsys):
    set_brightness(ssh_client, 100)              # set max brightness before measure power
    results = read_power(ssh_client)
    print(results)
    passed, name = (result_in_range(results, model))
    if passed:
        print("Test passed successfully!")
    else:
        print("Test failed on " + name)
    cap_set(cap_get(capsys))
    assert passed, "test failed"


# @pytestrail.case('C1')
@pytest.mark.sanity
@pytest.mark.smoke
#@pytest.mark.debug
@pytest.mark.skip
def test_forceupdate():
    cmd = "curl -i -H \"Content-Type: application/json\" -X POST -d '{\"update\": true}' \
    http://127.0.0.1:5000/sysinfo/forceupdate"
    r = ssh_client.execute(cmd, 30)         # allow timeout 20 seconds for forceupdate to finish
    assert r['retval'] == 0 and r['err'] == ''


@pytestrail.case('C18466')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.debug
def test_reset_button():
    errors = []
    cmd = "curl http://127.0.0.1:5000/sysinfo/resetbutton"
    r = ssh_client.execute(cmd)
#    if r['retval'] == 0 and json.loads(r['out'])['Reset Button'] == 1:
# could add test to check reset button 1 -> 0 -> 1 sequence
# display 'press' message then check 0, 'release' message then check 1
    assert r['retval'] == 0 and json.loads(r['out'])['Reset Button'] in ['1', '0']


@pytestrail.case('C18349')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.debug
def test_selftest():
    cmd = "curl http://127.0.0.1:5000/sysinfo/selftest"
    r = ssh_client.execute(cmd)
    print()
    print(r['out'])
    cap_set(r['out'])
    assert r['retval'] == 0 and json.loads(r['out'])['status'] == 'Success'


# @pytestrail.case('C1')
@pytest.mark.sanity
@pytest.mark.smoke
def test_model(model):
    cmd = "curl http://127.0.0.1:5000/sysinfo/model"
    r = ssh_client.execute(cmd)

    print(json.loads(r['out'])['Model'])
    assert r['retval'] == 0 and json.loads(r['out'])['Model'] == model_partno[model]


# @pytestrail.case('C1')
@pytest.mark.sanity
@pytest.mark.smoke
def test_sn(model):
    cmd = "curl http://127.0.0.1:5000/sysinfo/SN"
    r = ssh_client.execute(cmd)
    print(json.loads(r['out'])['Serial Number'])
    assert r['retval'] == 0


@pytestrail.case('C18347')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.debug
def test_apps():
    cmd = "curl http://127.0.0.1:5000/sysinfo/apps"
    r = ssh_client.execute(cmd)
    print(r['out'])
    cap_set(r['out'])
    assert r['retval'] == 0


@pytestrail.case('C18348', '18346')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.debug
def test_status():
    cmd = "curl http://127.0.0.1:5000/sysinfo/status"
    r = ssh_client.execute(cmd)
    print(json.loads(r['out'])['status'])
    cap_set(json.loads(r['out'])['status'])
    assert r['retval'] == 0


Orientations = ["normal", "left", "inverted", "right"]
# @pytestrail.case('C1')
@pytest.mark.sanity
@pytest.mark.smoke
# @pytest.mark.debug
@pytest.mark.skip
def test_orientation():
    origin = read_orientation(ssh_client)
    if origin is None:
        pytest.fail("Read orientation failed!")
    else:
        result = Results.retest
        while result == Results.retest:
            pause("\nStarting Orientation test, ")
            x = range(4)
            for i in x:
                set_orientation(ssh_client, Orientations[i])
                print(Orientations[i])


#            for orient in Orientations:
#                set_orientation(ssh_client, orient)
                time.sleep(5)
            result = read_result("Did the orientation test go well? ")
        set_orientation(ssh_client, origin)
        #        result = read_result("Please enter the result (pass/fail/retest/skip):", pytestconfig)
        if result == Results.skipped:
            pytest.skip("User selected skip!")
        if result == Results.failed:
            pytest.fail("User said it failed")


Brightness = [0,20,40,60,80,100]
@pytestrail.case('C18341')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.debug
def test_brightness():
    origin = read_brightness(ssh_client)
    if origin is None:
        pytest.fail("Read brightness failed!")
    else:
        print(origin)
        result = Results.retest
        while result == Results.retest:
            pause("\nStarting brightness test, ")
            x = range(len(Brightness))
            for i in x:
                set_brightness(ssh_client, Brightness[i])
                print(Brightness[i])
                time.sleep(5)
            result = read_result("Did the brightness test go well? ")
        set_brightness(ssh_client, origin)
        if result == Results.skipped:
            pytest.skip("User selected to skip!")
        if result == Results.failed:
            pytest.fail("User found it failed")

@pytestrail.case('C18343', 'C18344')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.debug
def test_Sensors(model, capsys):
    results = read_sensors(ssh_client)
    print(results)
    passed, names = (sensors_ok(results, model))
    if passed:
        print("Test passed successfully!")
    else:
        print("Test failed on " + names)
    cap_set(cap_get(capsys))
    assert passed


@pytestrail.case('C5310')
@pytest.mark.skip
@pytest.mark.hw
#@pytest.mark.debug
def test_mac():
    cmd = "cat /sys/class/net/eth0/address;cat /sys/class/net/wlan0/address;hcitool dev"
    r = ssh_client.execute(cmd)
    print()
    print(r['out'])
    print("Please check the mac address, to make sure they are continuous and match the lable/csv")
    assert r['retval'] == 0


#@pytestrail.case('C18346')
@pytest.mark.hw
#@pytest.mark.debug
def test_cputemp():
    cmd = "cat /sys/class/hwmon/hwmon1/temp*_input"
    r = ssh_client.execute(cmd)
    print()
    print(r['out'])
    print("Please check the temperatures are normal")
    assert r['retval'] == 0


@pytestrail.case('C18345')
@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.debug
def test_reboot():			# put it to the last, otherwise a not comletely finished reboot may affect other test cases
    cmdReboot = "curl -i -H \"Content-Type: application/json\" -X POST -d '{\"reboot\": true}' \
    http://127.0.0.1:5000/sysinfo/powercycle"
    ssh_client.execute(cmdReboot)
    time.sleep(5)
    if ssh_client.is_alive():
        assert False
    else:
        start = time.time()
        while not ssh_client.revive():
            time.sleep(2)
            end = time.time()
            if (end - start) > 300:          # 5 minutes maximum to wait
                break
        assert ssh_client.is_alive()



