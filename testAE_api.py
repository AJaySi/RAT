# Let's stick to python 3.x. import nothing from future
#!/usr/bin/python3

# PeP8 recommends importing all at the top.
import argparse
import sys
import logging
from colorlog import ColoredFormatter
from codecs import decode

# Internal testframe libraries
from lib.httpie_lib import abstract_http
from lib.run_tests import run_tcs
from lib.lib_utils import modify_tc_url

# Parse the arguments and/or display help message
def parsearg_help(logger):
    """ 
    Parse the command line argument and do as commanded. 
    Check is the testframework is being used as command line tool or as a test suite runner. 
    Parameters: 
    Run with -h option to list all the paramters to control the test tool. 
    Returns: 
    N/A 
    
    """
    parser=argparse.ArgumentParser(
        prog='testAE_api',
        usage='%(prog)s <METHOD> <URL> [REQUEST_ITEM [REQUEST_ITEM]]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        #formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='\
                This test tool does command line API validation, automation and runs regression test suites.\n\
                As a unit test tool, it automate your cmd-line test cases.\n\
                API Tests like return status, header type, response time, body content are done by default,\n\
                for each method.',
        epilog="\
                GET method Example: %(prog)s get https://httpbin.org/\n\
                RUN Example: %(prog)s run kafka : This will run all existing kafka API test cases.\n\
                RECORD Example: %(prog)s get http://httpbin.org/get --record\n\
                MODIFY TCs: %(prog)s --modify 34.10.12.23=192.10.32.34\n\
                Note : Read README for details of recording your unit tests for regression.\n"
    )

    # Define the type of rest method.
    parser.add_argument(
        "METHOD",
        # I need this for logic, but removing below limitation will also remove one more 
        # paramters. hmmm, usuability is inversely proportional to number of steps/arguments.
        nargs=1,
        default="GET",
        choices=['get', 'post', 'put', 'delete', 'run', 'modify'],
        help="Any One REST methods - [get | post | put | delete].\n\
            'run' Option: is used to run existing test suites like regression, unit, kafka et al.\n\
            'modify' Option: Does an exact match & replace. Useful in cases when modifying TCs in bulk."
    )

    # Define the URL to request on, resource location.
    parser.add_argument(
        "URL",
        default='all',
        nargs=1,
        help="Provide URL to use with REST Method.\n"
    )

    # Mention the request items with the methods.
    parser.add_argument(
        "-j", "--json",
        required=False,
        default=None,
        nargs=1,
        help="Provide request items to get,put,post,delete.\n\
        Provide a JSON payload with request.\n"
    )

    # Specify this option to record your command line tests.
    parser.add_argument(
        "-r", "--record",
        required=False,
        action='store_true',
        help="Specify this option to automate your command line tests\
        with this framework. Modify the main_config file for endpoint test requirements\
        This help record test cases to execute later as regression or unit tests.\
        Ex: %(prog)s get http://endpoint --record"
    )

    # If nothing is given then you need help.
    if len(sys.argv)==1:
        print("Display the help message. Please read the README.\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    logger.info("Number of arguments: {} and {}".format(len(sys.argv), str(args)))

    # This is the interactive, cURL replacement logic. We will be abstracting httpie here and encourage 
    # adoptability and familiarity with this tool.
    # Note: This tool should be easier to use than cURL.
    if (args.METHOD and args.URL):
        # Stringing the list from prompt. But, why, when there is only one method, url.
        method_str = ''.join(args.METHOD)
        url_str = ''.join(args.URL)
        request_item = ''
        # Below are optional arguments and need to be dealt with.
        # Converting list to string.
        if args.json is not None:
            request_item = ' '.join(args.json)

        # For running test suites.
        if ('run' in args.METHOD):
            run_tcs(url_str, logger)
        # For recording the TCs.
        elif(args.record and ('run' not in args.METHOD)):
            args.record = True
            abstract_http(method_str, url_str, request_item, args.record)
        # For Modifying recorded TC values in Bulk.
        elif('modify' in args.METHOD):
            logger.info("Modifying TC_url config values, for all files in 'testcases' directory.")
            # TBD: Support multiple values to change in TC file.
            modify_str = ' '.join(args.URL)
            modify_tc_url(modify_str, logger)
            exit(1)
        # Run as command line tool, No Recording.
        else:
            args.record = False
            abstract_http(method_str, url_str, request_item, args.record)


# Let's wakeup and decide what needs to be done.            
if __name__ == '__main__':
    """ INIT : This is an interactive test framework, use help to know more """
    # Check command line options and do as commanded.
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-s%(reset)s- %(asctime)s -[%(filename)s:]- %(reset)s%(blue)s%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    parsearg_help(logger)    

