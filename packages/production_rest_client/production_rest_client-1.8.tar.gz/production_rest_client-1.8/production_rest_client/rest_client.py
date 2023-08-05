# coding=utf-8
# pylint: disable=wrong-import-position, relative-import
import sys
import os
import requests
sys.path.append(os.path.join(os.path.dirname(__file__)))
from resources.testsuite_resource import TestSuiteResource
from resources.testcase_resource import TestCaseResource
from resources.operation_resource import OperationResource
from resources.state_resource import StateResource


class RestClient(object):

    def __init__(self, host, port=5000, time_out=5):
        __session = requests.Session()
        self.test_suite = TestSuiteResource(host, port, __session, time_out=time_out)
        self.test_case = TestCaseResource(host, port, __session, time_out=time_out)
        self.operation = OperationResource(host, port, __session, time_out=time_out)
        self.state = StateResource(host, port, __session, time_out=time_out)

if __name__ == '__main__':
    RC = RestClient("172.29.130.138")
    print(RC.test_suite.get_test_lists("fio"))
    # print(RC.test_case.list("fio"))
    # print(RC.test_case.run("test_fio_linux:TestFioLinux.test_rand_read", "async"))
    # print(RC.test_case.get_async_result("sjalvKeaDY"))
    # print(RC.test_case.stop_tests())
