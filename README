#-------------------
#  How to Install: 
#-------------------

1). Prerequisites:
a). 3.x Python
b). 'pip' or better still 'pipenv'

2). Install pipenv or create a virtual environment with venv.
3). Move into the project directory and do the following:

a). cd $project_dir/; pipenv shell to spwan a new virtual environment.
b). Do 'pipenv install .' 
c). If using 'pip' : cd $project_dir; pip install -r requirements.txt

#-------------------
# How to Run:
#-------------------

1). First thing is to check the command line help of the tool. 
Fire: python testAE_api -h

2). To Run New API tests from command line, fire:

a). python testAE_api get http://httpbin.org/get
Note: One can use REST methods/verbs like GET, POST, PUT, DELETE
Example:python testAE_api.py post http://xxx.xxxx.xx.xx:8080/api/v1/views/versions/3.0.0/instances/tables -j create_table

b). With JSON payload:- python testAE_api.py method URL -j file.json

3). To Record a TC with --record option: 
python testAE_api.py method URL -j file.json --record
Note: Give TC_name in 'main_config.ini' file

4). To Run Existing TCs from 'testcases' folder:

a). Example: python testAE_api run test_suite_name
NOte: test_suite_name should exist in 'testcases' directory, containing TC files.

b). Example: python testAE_api run performance
Note: This will run all the TCs recorded into 'performance' subdir of 'testcases' directory.
 

-------------------------------------------------------------------------------------------------------------
# The Boring Stuff:

PROBLEM STATEMENT:
A Command line test framework for API testing. Flexible and adaptable for all present/future test requirements.
Unit tests with cURL & Httpie (command line validations) are lost and not transferable.
Require least learning curve to also get the sanity/unit level testing automated, using config file.
Use best of familiar tools to provide features required for REST API test frameworks.
Due to presence of automated unit tests, the test team concentrates on higher value test cases.

cURL/Httpie facilitates manual testing of rest validation, cURL/Httpie based unit test cases are lost and not captured in test framework for regression.
The general test pattern for API testing involves, sending request method verbs with payloads and validating with API's response. 

GOALS
Motivations for the common tool
Many of the same test tools are utilized in different projects, by different testers.
The learnings from each project are lost and not reused in subsequent projects.
Having few REST API testing experts is more viable option and reusing automation to get started quickly,
Design a framework to start testing cycle with Automation and Not manual testing.
Record learnings in the framework rather than being people specific/dependent. 
Lower test cost and resource for all projects.

SPECIFICATIONS
Present Implementation and Features details
This is a REST API testing framework which works on the (1)command line, (2)records them and (3)runs regression test suites.
Command line API validation require manual inspection of request response with tools like cURL Or httpie. This framework's command line capability comes from httpie tool, assertions from apirift, mocking from mockito and performance, scale testing from k6.io
We are presenting able to automate API test cases with our framework with only config file changes. This reduces the amount of library code changes for adding/removing test cases. 
Test assertion support for matching strings in response body and header is present and supported through config files.
The framework is capable of running performance, stress, load and REST web server testing.
Our framework is integrated with k6.io and gives Performance(stress, load) at the command prompt, unlike cURL. 
We are also integrating security testing features to our test framework.

---------------------------------------------------------------------------------------------------------
# Tool Help Message:

Display the help message. Please read the README.

usage: testAE_api <METHOD> <URL> [REQUEST_ITEM [REQUEST_ITEM]]

                This test tool does command line API validation, automation and runs regression test suites.
                As a unit test tool, it automate your cmd-line test cases.
                API Tests like return status, header type, response time, body content are done by default,
                for each method.

positional arguments:
  {get,post,put,delete,run,modify}
                        Any One REST methods - [get | post | put | delete].
                        'run' Option: is used to run existing test suites like
                        regression, unit, kafka et al. 'modify' Option: Does
                        an exact match & replace. Useful in cases when
                        modifying TCs in bulk.
  URL                   Provide URL to use with REST Method.

optional arguments:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  Provide request items to get,put,post,delete. Provide
                        a JSON payload with request.
  -r, --record          Specify this option to automate your command line
                        tests with this framework. Modify the main_config file
                        for endpoint test requirements This help record test
                        cases to execute later as regression or unit tests.
                        Ex: testAE_api get http://endpoint --record

                GET method Example: testAE_api get https://httpbin.org/
                RUN Example: testAE_api run kafka : This will run all existing kafka API test cases.
                RECORD Example: testAE_api get http://httpbin.org/get --record
                MODIFY TCs: testAE_api --modify 34.10.12.23=192.10.32.34
                Note : Read README for details of recording your unit tests for regression.