import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--ip", action="store", default="192.168.1.19", help="The ip address of DUT"
    )
    parser.addoption(
        "--model", action="store", default="auto", help="The model of DUT, one of 'cc48', '3smi', 'qsmi', 'r211', and '8u2i', default auto"
    )


@pytest.fixture(scope='module')
def getip(request):
    return request.config.getoption("--ip")


@pytest.fixture(scope='module')
def getmodel(request):
    return request.config.getoption("--model")


capmanager = None
@pytest.fixture(scope='module', autouse=True)
def get_capmanager(pytestconfig):
    global capmanager
    capmanager = pytestconfig.pluginmanager.getplugin('capturemanager')



