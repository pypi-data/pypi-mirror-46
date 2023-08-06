# coding=utf-8
# pylint: disable=import-error
import json
from resources.models.helper import rest_post_json_call


class OperationResource(object):

    def __init__(self, host, port, session, time_out):
        self.host = host
        self.port = port
        self.session = session
        self.time_out = time_out

    def upgrade(self, fw_path, device_index=1, slot=2):
        data = {"operate_name":"upgrade", "fw": fw_path, "device_index":device_index, "slot":slot}
        url_ = "http://{0}:{1}/operation".format(self.host, self.port)
        result = rest_post_json_call(url_, self.session, json.dumps(data), self.time_out)
        return result["resource"]
