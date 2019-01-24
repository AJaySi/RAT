// Import k6 functionality
import http from "k6/http";
import { sleep, group, check } from "k6";

/*
Define defaults for number of virtual users to create with "vus: 100" parameter.
Define total duration of time to run the tests or test suite for with "duration:" paramter.
Define default thresholds and checks for the tests to run at suite level.

This gives ADM/AE REST performance, stress and load testing capability at the command prompt.

*/
export let options = {
    // The number of virtual k6 users to simulate.
    //vus: ${__ENV.VIR_USR_NUM},
    vus: 5,
    // Define and set test duration for all tests.
    //duration: "'${__ENV.RUN_FOR}'",
    duration: "3s",
    // Define thresholds and pass/fail checks with k6.
    //thresholds: {
        // At all page group level, Fail, if any request takes more than 500ms.
        //"group_duration{group:::Checkout Functional performance testing::Checkout}": [ "avg<500" ],
        // 95% of all checks at the group level has to be PASSing.
        //"checks": [ "rate>0.95" ]
   //}
};

export default function() {
   var r = http.post(`${__ENV.AE_URL}`);
   check(r, {
      //Common test validations to do for all AE rest apis going through this framework. 
      "Test1: POST Response status is 200": (r) => r.status === 200,
      "Test2: HTTP protocol is HTTP/2": (r) => r.proto === "HTTP/2.0",
      "Test3: Check for the correct verb - GET": (r) => r.json().args.verb === "POST",
      "Test4: Check if unauthorized header present": (r) => r.body.indexOf("Unauthorized") === -1,
      "Test5: Check if body size is greater than 0kb": (r) => r.body.length > 0,
      "Test6: Check content type is json": (res) => res.headers['Content-Type'] === "application/json",
      "Test7: Check API usuability by list message": (res) => res.headers['message'] === "*",
   });
}