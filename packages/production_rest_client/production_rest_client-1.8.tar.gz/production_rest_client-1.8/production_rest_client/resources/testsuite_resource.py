# coding=utf-8
# pylint: disable=import-error,eval-used
import json
from resources.models.helper import rest_get_call
from resources.models.helper import rest_post_json_call
from resources.models.helper import rest_delete_call


class TestSuiteResource(object):

    def __init__(self, host, port, session, time_out):
        self.host = host
        self.port = port
        self.session = session
        self.time_out = time_out

    def list(self, filter_):
        """
        :param filter_: string, filter_ condition
        :return: list, return list result
        """
        url_ = "http://{0}:{1}/ts/{2}".format(self.host, self.port, filter_)
        result = rest_get_call(url_, self.session, self.time_out)
        return result["resource"]

    def run(self, test_suite, mode="sync"):
        """
        :param test_suite: which test suite need to run
        :param  mode: sync or async, run test suite
        :return: list, return the test suite run results. include each test case in test suite
        """
        data = {"ts": test_suite, "mode": mode}
        url_ = "http://{0}:{1}/ts".format(self.host, self.port)
        result = rest_post_json_call(url_, self.session, json.dumps(data), self.time_out)
        return result["resource"]

    def get_async_result(self, key):
        url_ = "http://{0}:{1}/ts/results/{2}".format(self.host, self.port, key)
        result = rest_get_call(url_, self.session, self.time_out)
        return result["resource"]

    def stop_tests(self):
        url_ = "http://{0}:{1}/ts".format(self.host, self.port)
        result = rest_delete_call(url_, self.session, self.time_out)
        return result["resource"]

    def get_test_lists(self, test_suite_name):
        url_ = "http://{0}:{1}/ts/testlist/{2}".format(self.host, self.port, test_suite_name)
        result = rest_get_call(url_, self.session, self.time_out)
        result["resource"]["data"] = [eval(item) for item in result["resource"]["data"]]
        return result["resource"]
