#!/usr/bin/python3

import subprocess
import re
from perfAE_rest.perf_lib import run_perf
from .lib_utils import get_conf_vals
from apiritif import http
import json

# --------------------------------------------------
# A library package to test rest api for common errors and assuring it meets restful standards.
# Following check will be done for every rest api and depending on rest methods.
# --------------------------------------------------

# Common function to check the response status code.
# Helps in debugging as error codes are captured and reason failure displayed.
# 1). Check response code as :
# 1xx Informational response
# 2xx Success
# 3xx Redirection
# 4xx Client errors
# 5xx Server errors


def api_test_assertions(method, url, logger,payload=''):

    # Gives useful information for debugging and narrowing down the kind of response code error.
    # Returns: N/A : Maybe later return the error message to the user.

    auth_data=('admin','admin')
    header={'X-Requested-By':'ambari','Content-type':'application/json'}
    method = method.upper()

    if (method == 'GET'):
        logger.info("Start test asserts on the API GET Method for URL: {}".format(url))
        response = http.get(url,auth=auth_data,header=header)
    elif (method == 'POST'):
        logger.info("Start test asserts on API POST method for URL: {}".format(url))
        response = http.post(url,auth=auth_data,headers=header,data=payload)
    elif (method == 'PUT'):
        logger.info("Start test asserts on API PUT method for URL: {}".format(url))
        if payload!='':
            response = http.put(url,auth=auth_data,headers=header,data=payload)
        else:
            response = http.put(url,auth=auth_data,headers=header)
    elif (method == 'DELETE'):
        logger.info("Start test asserts on API DELETE method for URL: {}".format(url))
        response = http.delete(url,auth=auth_data,headers=header)

    # Another long if-elif, but this is needed to print back precise error and
    # save debugging time, by precise error failure cases.
    try:
        if(response.assert_2xx() or response.assert_status_code(200)):
            logger.info("PASS: The response code was a Success. Expected Result: 2xx")
        elif(response.assert_3xx()):
            logger.error("FAIL: Redirection error occured. Request failed. Actual Result: 3xx")
        elif(response.assert_4xx()):
            logger.error("FAIL: Client error occured. Check request sent. Actual Result: 4xx")
        elif(response.assert_5xx()):
            logger.error("FAIL: Server error occured. Server does not recognise request. Actual Result: 5xx")
    except:
        logger.critical("Fail: Unexpected response code.\n")
        #sys.exit(1)

    # Use the response methods assert_header() like below to extend for all checks in the response header.
    # Test if OK is present in response.
    if (response.assert_ok()):
        logger.info("PASS: Response has OK as expected result.")
    else:
        logger.error("FAIL: Expected OK in the response not found.\n")

    # Validate the response request header contents.
    validate_header(response, logger)

    # Validate the response body with expected results.
    validate_body(response, logger) 


# Common function to do all the response body content.
def validate_body(response, logger):
    print("validate body")

    # Test asserts for validating expected contents in body of response.
    body_tests = get_conf_vals("body")

    # Assert if following key-val are present in header or not.
    for (h_key, h_value) in body_tests.items():
        try:
            #response.assert_in_headers(h_key, h_value)
            response.assert_in_body(h_key, h_value)
            logger.info("PASS: The response body has valid '{}: {}' set.".format(h_key, h_value))
        except Exception as e:
            logger.error("FAIL: Expected '{}: {}' in response Body.\nError:{}\n".format(h_key, h_value, e))


# Common function to do all the header validations.
def validate_header(response, logger):

    # Test if response has a valid header, as per test requirements.
    # assert that response has header with given value
    # response.assert_header_value(header, value)
    # All relevant header checks here, specific to test requirements.
    logger.info("Start Header response assertion testing, values taken from config file.")
    head_tests = get_conf_vals("header")

    # Assert if following key-val are present in header or not.
    for (h_key, h_value) in head_tests.items():
        try:
            #response.assert_in_headers(h_key, h_value)
            response.assert_header_value(h_key, h_value)
            logger.info("PASS: The header response has valid '{}: {}' set.".format(h_key, h_value))
        except Exception as e:
            logger.error("FAIL: Invalid response header. Expected '{}: {}'.\n Error:{}\n".format(
                h_key, h_value, e))


# Main function to do rest api assertion and performance testing.
def test_api(method, url, logger,payload=''):
    perf = get_conf_vals("performance")
    if ('yes' in perf[2]):
        # Run Performance testing to benchmark REST API method with k6.
        run_perf(method, url, logger)
        
    # Run all the assertion tests on the given url with respect to its method.
    #api_test_assertions(method, url,logger,payload)
