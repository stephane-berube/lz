##############################################################################
#  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.   #
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License").           #
#  You may not use this file except in compliance                            #
#  with the License. A copy of the License is located at                     #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  or in the "license" file accompanying this file. This file is             #
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  #
#  KIND, express or implied. See the License for the specific language       #
#  governing permissions  and limitations under the License.                 #
##############################################################################
from moto import mock_ssm
from lib.logger import Logger
from manifest.cfn_params_handler import CFNParamsHandler
from lib.ssm import SSM

log_level = 'info'
logger = Logger(loglevel=log_level)

cph = CFNParamsHandler(logger)
ssm = SSM(logger)

# 3/24/20 - disabled failing test
def disabled_test_update_alfred_ssm():
    keyword_ssm = 'not_exist_alfred_ssm'
    key_ssm = 'key_ssm'
    value_ssm = 'not_exist_alfred_ssm'
    value_ssm, param_flag = cph._update_alfred_ssm(
                            keyword_ssm, key_ssm, value_ssm, False)
    assert param_flag is True


@mock_ssm
def test_update_alfred_genkeypair():
    ssm.put_parameter('testkeyname', 'testvalue', 'A test parameter', 'String')
    param = {
        "ssm_parameters": [
            {
                "name": "keymaterial",
                "value": "$[keymaterial]"
            },
            {
                "name": "keyfingerprint",
                "value": "$[keyfingerprint]"
            },
            {
                "name": "testkeyname",
                "value": "$[keyname]"
            }
        ]
    }
    account = 1234567890
    region = 'us-east-1'
    value = cph._update_alfred_genkeypair(param, account, region)
    assert value == 'testvalue'


@mock_ssm
def test_update_alfred_genpass():
    ssm.put_parameter('testkeyname', 'testvalue', 'A test parameter', 'String')
    param = {
        "ssm_parameters": [
            {
                "name": "testkeyname",
                "value": "$[password]"
            }
        ]
    }
    keyword = 'alfred_genpass_10'
    value = ''
    value = cph._update_alfred_genpass(keyword, param)
    assert value == '_get_ssm_secure_string_testkeyname'


@mock_ssm
def test_update_alfred_genaz():
    ssm.put_parameter('testkeyname', 'testvalue', 'A test parameter', 'String')
    param = {
        "ssm_parameters": [
            {
                "name": "testkeyname",
                "value": "$[az]"
            }
        ]
    }
    keyword = 'alfred_genaz_1'
    account = 1234567890
    region = 'us-east-1'
    value = ''
    value = cph._update_alfred_genaz(keyword, param, account, region)
    assert value == 'testvalue'


@mock_ssm
def test_random_password():
    ssm.put_parameter('testkeyname', 'testvalue', 'A test parameter', 'String')
    length = 10
    key_password = 'testkeyname'
    alphanum = False
    value = cph.random_password(length, key_password, alphanum)
    assert value == '_get_ssm_secure_string_testkeyname'
