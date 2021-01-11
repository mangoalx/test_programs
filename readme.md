opci test project
    ? power sensor limits for all models
    ? how to check if a sn good
    ? how to judge status good
    ? error process for helper functions
    - test cases for opci automatic test
    * testrail integration
    * config file to specify project number, user account, etc.
    * command line option to specify run id, model no, etc.
    + move power test sub_functions to opci_helper.py
    + set backlight to max before test power
    * set timeout 30s for forceUpdate test
    # pytest.fail() or skip() can be called from sub-functions
    # use autouse fixture to initialize global object
    * multi-reading then average for power sensor test
    
    # power limit check only report first failure, use a list
    
    
    