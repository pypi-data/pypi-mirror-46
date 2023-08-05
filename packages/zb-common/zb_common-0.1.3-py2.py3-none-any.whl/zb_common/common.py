from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import int
from builtins import chr
from builtins import object
from future import standard_library
standard_library.install_aliases()
import os
import uuid
import configparser
from slackclient import SlackClient

class Util(object):

    def __init__(self, cfg_path, component_name = None):
        self.component_name = component_name
        self.conf = configparser.ConfigParser()
        self.conf.read(cfg_path)
        self.sc = None
        slack_token = os.environ.get("SLACK_API_TOKEN", None)
        if slack_token != None:
            self.sc = SlackClient(slack_token)

    def get_env_value(self, key, section):
        return os.getenv("{}_{}".format(section, key), self.conf.get(section, key))

    def getSecondsSinceEpoch(self):
        return int(time.time())

    def getMillisecondsSinceEpoch(self):
        return int(1000 * self.getSecondsSinceEpoch())

    def get_random_id_32(self):
        return uuid.uuid4().hex

    def slack_log(self, channel_id, message):
        if self.component_name != None:
            message = "{}:{}".format(self.component_name, message)
        self.sc.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message
        )

    def get_E164_US_phone_number(self, us_phone_number):
        cleansed_ph_num = ''.join([i for i in us_phone_number if i == '+' or (i >= chr(48) and i <= chr(57))])
        if cleansed_ph_num.startswith("+"):
            return cleansed_ph_num
        return "+1{}".format(cleansed_ph_num)
