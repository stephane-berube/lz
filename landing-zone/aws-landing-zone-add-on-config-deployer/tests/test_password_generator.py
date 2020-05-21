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
from lib.password_generator import random_pwd_generator
import re


def test_random_pwd_generator():
    random_pwd_no_additional_string = random_pwd_generator(10, 'a')
    assert len(re.sub('([^0-9])','',random_pwd_no_additional_string)) >= 2
    assert random_pwd_no_additional_string[8:] == "aa"
    assert len(random_pwd_no_additional_string) == 10
