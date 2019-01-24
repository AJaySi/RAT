#!/usr/bin/python3

from .lib_utils import get_conf_vals, write_to_config
# FIXME: Need to rework the logging. Only for demo.
#from logs.logtest import setup_logger
#logger = setup_logger()

# ---------------------------------------------------
# Common function to convert/automate the test cases run by this tool
# on the command prompt. This library supports the --record feature of
# the tool. We will basically freeze, copy the 'main_config.ini' into a
# 'testcases' directory as a new testcase.
# ---------------------------------------------------

# Common function to copy the existing main_config.ini and record in
# a different directory as a new TC.
# Record the given command line values as TC inputs.


def record_tc_config(method, url, items, logger):
    logger.info("Record following REST method: {}, URL: {} and request items: {}".format(
        method, url, items))

    # First make a copy of the main_config.ini file and leave it as it is.
    # At this point we do not know the directory or have kept it constant to kafka.

    # There are 2 choices to decide the location of the TCs. We can take it from config file
    # or ask the user interactively on the prompt. Asking interactively seems a better choice now.
    logger.info("Everything by default goes to folder 'testAE_api/testcases'")
    #tc_name = input("Give a name to your new TC: EX: kafka_register_TC.ini")
    #tc_dir = input("Enter the name of directory to put into. Check 'testcases' directory")
    record_val = get_conf_vals("record")

    # Populate the main_config.ini as TC values for automated running.
    # Below values are required by the framework.
    for key, val in record_val.items():
        # It is case sensitive.
        if ('TC_url' in key):
            record_val[key] = url
        elif ('TC_method' in key):
            record_val[key] = method
        elif('TC_payload_items' in key):
            record_val[key] = items
        elif ('TC_name' in key):
            # Check if TC name is given.
            if (val == ''):
                # Maybe, Default values should be taken instead of asking on the prompt.
                record_val[key] = input(
                    "##** INPUT Required: Please input/give a name to your TC:: ")
        elif ('TC_dir_name' in key):
            if (val == ''):
                record_val[key] = input(
                    "##** INPUT Required: Please enter directory name.: Ex: Kafka_tests: ")

    # Record the config values as TCs.
    write_to_config(record_val, logger)
