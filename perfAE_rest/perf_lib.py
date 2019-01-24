#!/usr/bin/python3

import subprocess
from lib.lib_utils import fireon_cmdprmt, get_conf_vals

# This function runs the k6 tool with the given url.
# This function should be part of utils or another library.
def run_perf(method, url_item, logger):
    print("Measure response time of this API: {}: {}".format(url_item, method))
    (vus, duration, run_perf_test) = get_conf_vals('performance')

    # The load variables should be exposed through command line invocation and config file driven.
    # Most of the k6 functionality can be thus abstracted and config driven through this framework.
    # The need to know javascript for k6 needs to be minimal/negligible.
    k6_common = "k6 run -u {} -d {} -e AE_URL={} ".format(vus, duration, url_item)
    method = method.upper()
    if (method == 'GET'):
        perf_cmd = k6_common + 'perfAE_rest/ae_perf_get.js'
    elif(method == 'POST'):
        perf_cmd = k6_common + 'perfAE_rest/ae_perf_post.js'
    elif(method == 'DELETE'):
        perf_cmd = k6_common + 'perfAE_rest/ae_perf_delete.js'
    elif(method == 'PUT'):
        perf_cmd = k6_common + 'perfAE_rest/ae_perf_put.js'
    else:
        print("Note: Request method type is required for benchmarking.")

    print("k6 Command for benchmarking: {}".format(perf_cmd))
    fireon_cmdprmt(perf_cmd, logger)

    # Performance tests are additional and not mandatory requirement.
    # The framework is not strict here and just displays the statics on stdout.
    # The framework is not opiniated here and only advisory.
