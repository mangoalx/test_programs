#import pytest
import json
from enum import Enum
from . import conftest
#from tests import conftest


# enum for result from user input 1(passed) 2(blocked) 3(untested) 4(retest) 5(failed)
class Results(Enum):
    passed = 1
    retest = 4
    failed = 5
    skipped = 0
""" should check if all limits were checked, if data is less than limits, it should not pass"""
# Function to read all power sensor data, return an object


def read_power(ssh):
    url = "curl http://127.0.0.1:5000/power"
    r = ssh.execute(url)
    if r['retval'] != 0:
        print("Error:", r['err'])
    else:
        sensors = json.loads(r['out'])['Power sensor list']
        result = []
        for sensor in sensors:
            cmd = url + '/' + sensor
            r = ssh.execute(cmd)
            if r['retval'] != 0:
                print("Error:", r['err'])
            else:
                jdata = json.loads(r['out'])
                result.append({"Name": sensor, 'Data': {"Voltage": jdata['voltage'], "Current": jdata['current'], "Power": jdata['power']}})
        return result


eu2iPowerLimits = {'12V': {'Voltage': {'Min': 11500, 'Max': 12500}, 'Current': {'Min': 1200, 'Max': 2500}, 'Power': {'Min': 12000000, 'Max': 30000000}},
                   '5V': {'Voltage': {'Min': 4750, 'Max': 5250}, 'Current': {'Min': 800, 'Max': 2800}, 'Power': {'Min': 4000000, 'Max': 14000000}},
                   '24V': {'Voltage': {'Min': 22800, 'Max': 25200}, 'Current': {'Min': 800, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}},
                   # 'reddriver': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1000, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}},
                   'PRT-24V': {'Voltage': {'Min': 22800, 'Max': 25200}, 'Current': {'Min': 5000, 'Max': 25000}, 'Power': {'Min': 20000000, 'Max': 500000000}}
                   }
cc48PowerLimits = {'10V': {'Voltage': {'Min': 11500, 'Max': 12500}, 'Current': {'Min': 400, 'Max': 500}, 'Power': {'Min': 4800000, 'Max': 6000000}},
                   '5V': {'Voltage': {'Min': 4750, 'Max': 5250}, 'Current': {'Min': 800, 'Max': 2800}, 'Power': {'Min': 4000000, 'Max': 14000000}},
                   '24V': {'Voltage': {'Min': 22800, 'Max': 25200}, 'Current': {'Min': 2000, 'Max': 4000}, 'Power': {'Min': 48000000, 'Max': 100000000}},
                   'leddriver_left_side': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1000, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}},
                   'leddriver_right_side': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1000, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}},
                   'TCON-12V': {'Voltage': {'Min': 11000, 'Max': 13500}, 'Current': {'Min': 250, 'Max': 400}, 'Power': {'Min': 3000000, 'Max': 5000000}}
                   }
qsmiPowerLimits = {'10V': {'Voltage': {'Min': 9500, 'Max': 10500}, 'Current': {'Min': 300, 'Max': 800}, 'Power': {'Min': 2500000, 'Max': 8000000}},
                   '5V': {'Voltage': {'Min': 4750, 'Max': 5250}, 'Current': {'Min': 800, 'Max': 2000}, 'Power': {'Min': 4000000, 'Max': 10000000}},
                   '24V': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1500, 'Max': 3000}, 'Power': {'Min': 24000000, 'Max': 70000000}},
                   'DPC-10V': {'Voltage': {'Min': 9500, 'Max': 10500}, 'Current': {'Min': 150, 'Max': 350}, 'Power': {'Min': 1500000, 'Max': 3500000}},
                   'leddriver': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1000, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}}
                   }
tsmiPowerLimits = {'10V': {'Voltage': {'Min': 11500, 'Max': 12500}, 'Current': {'Min': 350, 'Max': 680}, 'Power': {'Min': 3600000, 'Max': 8400000}},
                   '5V': {'Voltage': {'Min': 4750, 'Max': 5250}, 'Current': {'Min': 800, 'Max': 2000}, 'Power': {'Min': 4000000, 'Max': 8000000}},
                   '24V': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1500, 'Max': 3000}, 'Power': {'Min': 24000000, 'Max': 70000000}},
                   'TCON-12V': {'Voltage': {'Min': 11000, 'Max': 13500}, 'Current': {'Min': 50, 'Max': 200}, 'Power': {'Min': 600000, 'Max': 2400000}},
                   # 'reddriver': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1000, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}},
                   'leddriver': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1000, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}}
                   }
r211PowerLimits = {'10V': {'Voltage': {'Min': 9500, 'Max': 10500}, 'Current': {'Min': 500, 'Max': 900}, 'Power': {'Min': 5000000, 'Max': 10000000}},
                   '5V': {'Voltage': {'Min': 4750, 'Max': 5250}, 'Current': {'Min': 800, 'Max': 2500}, 'Power': {'Min': 4000000, 'Max': 12000000}},
                   '24V': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1500, 'Max': 3000}, 'Power': {'Min': 24000000, 'Max': 70000000}},
                   # 'reddriver': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1000, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}},
                   'leddriver': {'Voltage': {'Min': 21600, 'Max': 26200}, 'Current': {'Min': 1000, 'Max': 2000}, 'Power': {'Min': 20000000, 'Max': 50000000}}
                   }
model_limits = {'qsmi': qsmiPowerLimits, '3smi': tsmiPowerLimits, '8u2i': eu2iPowerLimits, 'r211': r211PowerLimits, 'cc48smi': cc48PowerLimits}
# Function to compare if the data are in range


def in_range(data, limit):
    return limit['Min'] <= data <= limit['Max']


def dic_in_range(dic_d, dic_l):
    for key in dic_d:
        # when test temperature or humidity we may append split('.')[0], only take inter part
        if not in_range(int(dic_d[key].split(' ')[0]), dic_l[key]):
            return False
    return True


def result_in_range(results, model):
    names = []
    limits = model_limits[model]
    for result in results:
        name = result['Name']
        names.append(name)
        dic_data = result['Data']
        dic_limit = limits[name]
        if not dic_in_range(dic_data, dic_limit):
            return False, name
    for keyname in limits:                          # check all key in limits appeared in results
        if not keyname in names:
            return False, keyname
    return True, None


def read_brightness(ssh):
    cmd_brightness = "curl http://127.0.0.1:5000/display/backlight"
#    print(cmd_brightness)
    r = ssh.execute(cmd_brightness)
#    print(r)
    if r['retval'] != 0:
        print("Error:", r['err'])
    return int(json.loads(r['out'])['brightness'] + 0.5)


def set_brightness(ssh, brightness):
    if brightness == 0:
        power = "off"
    else:
        power = "on"
    cmd_brightness = "curl -i -H \"Content-Type: application/json\" -X PATCH -d '{\"power\": \"" \
                     + power + "\", \"brightness\": \"" + str(brightness) \
                     + "\"}' http://127.0.0.1:5000/display/backlight"
#    print(cmd_brightness)
    r = ssh.execute(cmd_brightness)
#    print(r)
    if r['retval'] != 0:
        print("Error:", r['err'])
    return r
    '''
    if r['retval'] != 0:
        print("Error:", r['err'])
    else:
        sensors = json.loads(r['out'])['Power sensor list']
        result = []
        for sensor in sensors:
            cmd = url + '/' + sensor
            r = ssh.execute(cmd)
            if r['retval'] != 0:
                print("Error:", r['err'])
            else:
                jdata = json.loads(r['out'])
                result.append({"Name": sensor, 'Data': {"Voltage": jdata['voltage'], "Current": jdata['current'], "Power": jdata['power']}})
        return result
{'retval': 0, 'out': 'HTTP/1.0 200 OK\r\r\nContent-Type: application/json\r\r\nContent-Length: 32\r\r\nServer: Werkzeug/1.0.0 Python/3.5.3\r\r\nDate: Thu, 04 Jun 2020 02:31:17 GMT\r\r\n\r\r\n{"brightness":100,"power":"on"}\r\n', 'err': ''}'''


def set_orientation(ssh, orientation):
    cmd_orientation = "curl -i -H \"Content-Type: application/json\" -X POST -d '{\"orientation\": \"" \
                     + orientation + "\"}' http://127.0.0.1:5000/sysinfo/orientation"
#    print(cmd_orientation)
    r = ssh.execute(cmd_orientation)
#    print(r)
    if r['retval'] != 0:
        print("Error:", r['err'])
    return r


def read_orientation(ssh):
    cmd_read_orientation = "curl http://127.0.0.1:5000/sysinfo/orientation"
#    print(cmd_orientation)
    r = ssh.execute(cmd_read_orientation)
#    print(r)
    if r['retval'] != 0:
        print("Error:", r['err'])
    return json.loads(r['out'])['orientation']


def read_input(prompt):
    conftest.capmanager.suspend_global_capture(in_=True)
    r = input(prompt)
    conftest.capmanager.resume_global_capture()
    return r


def pause(prompt):
    conftest.capmanager.suspend_global_capture(in_=True)
    prompt += "Press Enter to continue ..."
    input(prompt)
    conftest.capmanager.resume_global_capture()


# read user input result, return skip, retest, pass, fail
def read_result(prompt):
    prompt = prompt + "Please enter the result (Pass/Fail/Retest/Skip):"
    conftest.capmanager.suspend_global_capture(in_=True)
    ret = None
    while ret == None:
        r = input(prompt)
        if len(r) > 0:
            if r[0] in "rR":
                ret = Results.retest
            if r[0] in ['p', 'P']:
                ret = Results.passed
            if r[0] in ['f', 'F']:
                ret = Results.failed
            if r[0] in ['s', 'S']:
                ret = Results.skipped
    conftest.capmanager.resume_global_capture()
    return ret


def read_sensors(ssh):
    url = "curl http://127.0.0.1:5000/environment/sensors"
    r = ssh.execute(url)
    if r['retval'] != 0:
        print("Error:", r['err'])
    else:
        sensors = json.loads(r['out'])['Environment sensor list']
        results = []
        for sensor in sensors:
            cmd = url + '/' + sensor
            r = ssh.execute(cmd)
            if r['retval'] != 0:
                print("Error:", r['err'])
            else:
                jdata = json.loads(r['out'])
                print(jdata)
                results.append({"Name": sensor, 'driverLoaded': jdata['driverLoaded']})
        return results


def sensors_ok(results, model):
    names = []
    fail_names = []
    for result in results:
        name = result['Name']
        names.append(name)
        if not result['driverLoaded']:
            fail_names.append(name)
    for keyname in Model_sensors[model]:                          # check all key in limits appeared in results
        if not keyname in names:
            fail_names.append(keyname)
    return not fail_names, fail_names


Model_sensors = {'qsmi': ["ALS", "temperatureHumidity", "accelerometer", "temperature"], \
                 '3smi': ["ALS", "temperatureHumidity", "accelerometer", "temperature"], \
                 '8u2i': ["ALS", "temperatureHumidity", "accelerometer"], \
                 'r211': ["temperatureHumidity", "accelerometer", "temperature"], \
                 'cc48smi': ["ALS", "temperatureHumidity", "accelerometer", "temperature"]}

