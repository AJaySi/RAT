#!/usr/bin/python3
import sys
import os.path
from configparser import ConfigParser

# Internal libraries.
from .lib_utils import get_conf_vals
from .httpie_lib import abstract_http

#-----------------------------------------------------------
# Common library to execute AE REST APIs test suites.
# As a common framework it should be able to run regression, sanity, functional,
# unit and performance tests in a automated, regular fashion. 
#-----------------------------------------------------------

# Funtion to decide which test suite to run.
def run_tcs(tcgroup, logger):
    # Call appropriate functions based on the type of test suite to run.
    # Check if the named directory exists.
    tc_root_dir = os.path.join(os.path.dirname(__file__), '..', 'testcases')

    # Logic to run 'All' Test cases or 'all' testcases in the given directory.
    # We want to recursively list all directories and then all the TCs in them,
    # When 'all' keyword is given we will execute all TCs in subsidrectories
    # present under 'testcases/'. The same logic is extended for specific test suites
    # like kafka, this will run all TCs under kafka directories and its subdirectories.
    # The basic logic is to change the root dir, depending on what needs to be run.
    if tcgroup.lower() == 'all'.lower():
        logger.info("Running All TCs")
    else:
        tc_root_dir = os.path.join(tc_root_dir, tcgroup)
        # Check if given dirname exists under 'testcases/'
        if not (os.path.isdir(tc_root_dir)):
            logger.error("Couldn't find '{}' in 'testcases' directory: {}. \nPlease copy/create TC dir in testcases folder.".format(tcgroup, tc_root_dir))
            sys.exit(1)
        else:
            logger.info("Running TCs from '{}' directory.".format(tcgroup))
    
    # We now know the directory exists. Lets get all the TC files to execute.
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(tc_root_dir):
        # Making a list of files with absolute path.
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        #listOfdirs += [dirname for dirname in dirnames]

    # Validate if each file has required parameters set.
    listOftcs = valid_config(listOfFiles)

    # just because I hate writing long monolithic functions. Lets call another one.
    run_valid_tcs(listOftcs, logger)
    logger.info("Total Number of valid TCs to execute: {}".format(len(listOftcs)))

# Common function to run TC, read config values, stuff defaults for missing values.
def run_valid_tcs(tclist, logger):
    # The TC file are now valid, so lets fire them and do the tests.
    print("TC_LiST:{}".format(tclist))
    for tc_execute in tclist:
        tc_dict = get_conf_vals("run_tests", tc_execute)
        logger.info("====================== TC START ===================\n")
        logger.info("Running TC: {}".format(tc_dict))

        try:
            abstract_http(tc_dict['TC_method'], tc_dict['TC_url'], tc_dict['TC_payload_items'])
        except KeyError:
            logger.warn("The config file is not well formed. Please compare with 'main_config.ini'")

        logger.info("====================== TC DONE ====================")

# Common function to check if the filename contains the 'framework_required'
# section. Consider only files with this section for test execution.
def valid_config(tcnames):
    """
    A valid TC config file should have the section 'framework_required'.
    Also, checks if the url_test is given or not.
    This makes the test framework very flexible with minimal requirement to
    get started. It only requires, preferably, an *.ini file with one parameter 
    "tc_url=http://fakehost.url" 
    """
    valid_tc_lst = list()
    for tcname in tcnames:
        config = ConfigParser()
        config.read(tcname)

        try:
            # If the given section exists, and contains the given option, 
            # return True; otherwise return False. 
            # If the specified section is None or an empty string, DEFAULT is assumed.
            if (config.has_option('framework_required', 'TC_url') and config.get('framework_required', 'TC_url')): 
                # Framework will Assume GET method, if none given.
                #config.has_option('framework_required', 'tc_method')
                valid_tc_lst.append(tcname)
            else:
                print("Skipping Test Case file: {}.\nIt does not have required section and tc_url option.".format(tcname))

        except Exception:
            # It is TC writer responsibility to at least give a URL to test on.
            continue

    # Return a list of valid TCs file that will be executed.
    return (valid_tc_lst)