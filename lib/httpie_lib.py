#!/usr/bin/python3

import subprocess
import sys
import json
# Internal libraries.
from .rest_assertions import test_api
from .lib_utils import fireon_cmdprmt, get_conf_vals
from .record_lib import record_tc_config
from logs.logtest import logger

# ----------------------------------------------------------
# Purpose of this library: This is a wrapper for httpie, which is a cURL alternative.
# Although, either using cURL or httpie on command prompt helps do quick-dirty testing,
# it suffers from the loss of automated, repeated test cases.
# This library will is written to abstract the learning curve of httpie and make it possible
# to automate command like unit tests into this framework.
# ----------------------------------------------------------

def abstract_http(method, url, items, record_tc=False):
    """ 
    Summary:
    Function to abstract, wrap and fire and test the given http command.
    Everything goes to stdout, no logging, similar to curl based unit testing.
    Description:
    Abstracts learning curve involed with yet another test tool. 
    Parameters: 
    Expects a http command string parsed from the command of main program. See help menu. 
    Returns: 
    N/A 
    """
    # First do the test asssertions checking and uri benchmarking.
    #####BY punam

    if items!='':
        item_data=json.load(open(items))
        json_data=json.dumps(item_data)
        logger.info("Running http assertions on URL: {} for request_item:{}".format(url, json_data))
        # Exception handling by called function.
        test_api(method, url,logger,json_data)
    else:
        test_api(method, url,logger)

    # The below defaults needs to be exported to a config file.
    # You most likely want use the --ignore-stdin option to disable it.
    # It instructs HTTPie to exit with an error if the HTTP status is one of 3xx, 4xx, or 5xx.
    # You can use --json, -j to explicitly set Accept to application/json
    # Spaces accounted for.
    users = get_conf_vals('login')
    header=' X-Requested-By:testAE_api' 
    default_vars = " --all --check-status --ignore-stdin -a " + users

    method_verb = method.upper()
    # Make http command based on the type of request method.
    # Doing below reduces one input on the command prompt.
    if (method_verb == 'GET'):
        http_cmd = "http " + default_vars + " GET "
    elif(method_verb == 'POST'):
        http_cmd = "http " + default_vars + " POST "
    elif(method_verb == 'PUT'):
        http_cmd = "http " + default_vars + " PUT "
    elif(method_verb == 'DELETE'):
        http_cmd = "http " + default_vars + " DELETE "
    http_cmd = http_cmd + " {}".format(url) + " {}".format(header) 
    if items != '':
        http_cmd = http_cmd + ' < ' + items

    logger.info("HTTP Command Used: {}".format(http_cmd))
    # Fire the httpie command with all the options and check status.
    if (fireon_cmdprmt(http_cmd, logger) == 0):
        logger.info("Use 'main_config.ini' to add/modify the tests. Scroll-up for more info.")
        logger.info("Convert to automated TC by rerunning the test tool with '--record' option.")
        # Now that the rest method is success, lets test that API
    else:
        logger.error("Exit: Failed htttp command, check httpie command usage")
        sys.exit(1)

    # Check if the record TC option is set/True.
    # At this point in code, the TC has been run and validated.
    # We need to check/enforce only passing TCs are recorded.
    # If not, they become maintenance headache.
    if (record_tc == True):
        logger.info("############## RECORD TC ################")
        logger.info("Recording TC with given options for future automated runs.\n")
        record_tc_config(method, url, items, logger)
