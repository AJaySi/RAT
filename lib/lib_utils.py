#!/usr/bin/python3

# Import required libraries.
import subprocess
import sys, re
import os.path
import shutil
from configparser import ConfigParser
import json
#from logs.logtest import logger

###################################################
#
# Common package for util functions required by the test framework.
# Having a common functionality will aid in easier maintenance and extendibility.
# Collection of common util type and helper functions.
#
###################################################

# Common Function to run command line tools.
def fireon_cmdprmt(firecmd, logger):
    # Display it for manual inspection.
    # Redirection not allowed on windows: '<' is a problem.
    # Check os type and fire through 'cmd /c'
    #if os.name == 'nt':

    try:
        proc = subprocess.Popen(firecmd,shell=True)
    except subprocess.CalledProcessError as e:
        logger.error("Failed to execute command with Error: {}".format(e))
    # print the output of the child process to stdout
    proc.communicate()
    if (proc.returncode != 0):
        logger.error("Exit: Check by directly firing on command prompt: {}.".format(firecmd))
        sys.exit(1)
    # TBD: capture and return stdout and/or stderr to the calling function.
    return(0)


# Common function to read config paramters and return the desired values
def get_conf_vals(search_for, conf_file='main_config.ini'):
    # There will be separate logic for reading from main_config and TC configs.
    config = ConfigParser()
    # Preserve case of the config paramters.
    config.optionxform=str
    # Load the correct config file to read.
    try:
        # Absolute paths are needed to make it work on platforms. No escaping.
        conffile = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', conf_file))
        config.read(conffile)
    except:
            # FIXME: Need to exit, keeping it open for framework development.
            print("Failed to read the config file.")
    if(search_for == 'run_tests'):
        try:
            config.optionxform=str
            config.read(conf_file)
        except Exception as e:
            print("Failed to Read the config file: {}".format(conf_file))
        return(dict(config.items('framework_required')))
    # Get config file values for running performance tests.
    elif (search_for == 'performance'):
        try:
            vus = config.get('performance', 'num_users')
            duration = config.get('performance', 'test_duration')
            to_run = config.get('performance', 'run_perf_tests')
            return(vus, duration, to_run)
        except Exception as e:
            print("Error: Unable to read values from the config file: {}\n Error: {}".format(conffile, e))
    # For returning all main_config.ini values of section 'test_header'
    elif (search_for == 'header'):
        return(dict(config.items('test_header')))
    # Return expected body content for the response.
    elif (search_for == 'body'):
        return(dict(config.items('test_body')))
    # Return parameters required for recording a TC.
    elif (search_for == 'record'):
        return (dict(config.items('framework_required')))
    # Return login credentials.
    elif (search_for == 'login'):
        return(config.get('framework_required', 'credentials'))


# Common helper function to move around in directories, make file,
# move them and copy them.
def move_to_dir(tc_name, tc_dir, logger):
    # To avoid creating a new dir everytime, first check dir exists, if not then create new.
    # Downside: Testers wont change the config parameter and misc folder will get full.
    # Check if given folder already exists in 'testcases' directory.

    # Check if user given directory exists or needs to be created.
    ts_dir = os.path.join(os.path.dirname(__file__), '..', 'testcases')
    tc_dir_name = os.path.join(ts_dir, tc_dir)
    if not (os.path.isdir(os.path.join(ts_dir, tc_dir))):
        logger.warn("Creating a new directory to store TC. Its a bad idea to create a directory per TC.\n")
        # Make a new directory in the framework 'testcases' dir.
        # Check, if it exists then simply the conf as TC there.
        try:
            os.mkdir(tc_dir_name)
        except OSError:
            # except OSError as exc:
            logger.error("Unable to make directory {} at location {}".format(ts_dir, tc_dir_name))
    else:
        # The directory already exists, just copy the mani_config.ini into a
        # file named as the new TC name.
        logger.info("Directory Exists: {}, Copy the TC ini file in it.".format(ts_dir))
        # Let's hardcode ini here, no need to specify in conf file.
        
    copy_to = os.path.join(tc_dir_name, tc_name) + '.ini'
    # Check if the file already exists, then prompt for unique TC name and exit.
    if not os.path.isfile(copy_to):
        copy_from = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main_config.ini'))
        logger.info("Copy main config:{} to: {}".format(copy_from, copy_to))
        try:
            shutil.copyfile(copy_from, copy_to)
            #return (copy_to)
        except shutil.Error:
            logger.error("Failed to copy:{} to: {} with errors:{}".format(copy_from, copy_to, shutil.Error))
        return (copy_to)
    else:
        logger.critical("Exit_TC_Exists: Try with a unique TC name in main_config.ini file.\n")
        sys.exit(1)


# Common helper function to write to config/ini files.
def write_to_config(write_vals, logger):

    # First, we need to move the file to its desired location and then
    # write to it. This way we will always keep the main_config.ini clean
    # and healthy.
    rcd_tc_name = move_to_dir(write_vals['TC_name'], write_vals['TC_dir_name'], logger)
    logger.info("Update/Record TC values: {} in directory: {}".format(write_vals, rcd_tc_name))

    # The main_config.ini is now recorded as TC for regression runs.
    # We will now write main_config.ini framework_required section into it.
    # Rewrite the TC [framework_required] section.
    config = ConfigParser()
    config.optionxform=str
    config.read(rcd_tc_name)

    for (key, val) in write_vals.items():
        logger.info('Writing following framework_required TC values {} : {}'.format(
            key, write_vals[key]))
        config.set('framework_required', key, val)
    #config.set('framework_required', 'tc_url', write_vals['tc_url'])
    try:
        with open(rcd_tc_name, 'w') as conf_file:
            config.write(conf_file)
    except EnvironmentError as e:
        logger.critical("Exit: Failed to write to the TC File: {}".format(e))

# Function to modify stale param from REST API URL.
def modify_tc_url(modify_val, logger):
    """
    Common utility function to modify stale TC values in bulk.
    The testcases directory contains TCs, which are .ini file,
    Do an exact match of the TC_url value separated by '/' and then replace.
    """
    if ('=' not in modify_val):
        logger.error("Requires '=' where RHS gets substituted with LHS: {}.".format(modify_val))
        exit(1)
    else:
        # Split it into LHS, the value to compare and RHS, the value to substitute.
        rhslhs = modify_val.split('=')
    ts_dir = os.path.join(os.path.dirname(__file__), '..', 'testcases')
    tc_list = getListOfFiles(ts_dir)
    if tc_list:
        logger.info("Following TC files will be modified: {}".format(tc_list))
        for a_tc in tc_list:
            config = ConfigParser()
            config.optionxform=str
            config.read(a_tc)
            # Read the TC_url param from config file.
            tc_url = config.get('framework_required', 'TC_url')
            
            if (rhslhs[0] not in tc_url):
                logger.error("No match found for string: '{}' in config file for TC_url:{}.".format(rhslhs[0], tc_url))
            else:
                replcd_str = tc_url.replace(rhslhs[0], rhslhs[1])
                logger.info("Write replace/new string: {}: with old: {}".format(tc_url, replcd_str))
                config.set('framework_required', 'TC_url', replcd_str)
            
            # Commit changes per TC file.
            try:
                with open(a_tc, 'w') as conf_file:
                    config.write(conf_file)
            except EnvironmentError as e:
                logger.critical("Exit: Failed to write/modify the TC File: {}".format(e))

    else:
        logger.error("There are no TC files in directory: {}".format(ts_dir))

# List all contents, for logging on displaying on stdout.
#print("List all contents")
# for section in config.seictions():
#    print("Section: %s" % section)
#    for options in config.options(section):
#        print("x %s:::%s:::%s" % (options,
#                                  config.get(section, options),
#                                  str(type(options))))


# For the given path, get the List of all files in the directory tree 
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles