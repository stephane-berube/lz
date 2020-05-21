###################################################################################################################### 
#  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           #
#                                                                                                                    # 
#  Licensed under the Apache License Version 2.0 (the "License"). You may not use this file except in compliance     # 
#  with the License. A copy of the License is located at                                                             # 
#                                                                                                                    # 
#      http://www.apache.org/licenses/                                                                               # 
#                                                                                                                    # 
#  or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES # 
#  OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    # 
#  and limitations under the License.                                                                                # 
######################################################################################################################
#!/bin/python
import boto3
import inspect
import json
from lib.decimal_encoder import DecimalEncoder

class SNS(object):
    def __init__(self, logger, **kwargs):
        self.logger = logger
        if kwargs is not None:
            if kwargs.get('credentials') is None:
                logger.debug("Setting up CFN BOTO3 Client with default credentials")
                self.sns_client = boto3.client('sns')
            else:
                logger.debug("Setting up CFN BOTO3 Client with ASSUMED ROLE credentials")
                cred = kwargs.get('credentials')
                region = kwargs.get('region', None)

                if region:
                    self.sns_client = boto3.client('sns', region_name=region,
                                                   aws_access_key_id=cred.get('AccessKeyId'),
                                                   aws_secret_access_key=cred.get('SecretAccessKey'),
                                                   aws_session_token=cred.get('SessionToken')
                                                   )
                else:
                    self.sns_client = boto3.client('sns',
                                                   aws_access_key_id=cred.get('AccessKeyId'),
                                                   aws_secret_access_key=cred.get('SecretAccessKey'),
                                                   aws_session_token=cred.get('SessionToken')
                                                   )


    def publish(self, topic_arn, message, subject):
        try:
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject
            )
            return response

        except Exception as e:
            message = {'FILE': __file__.split('/')[-1], 'CLASS': self.__class__.__name__,
                       'METHOD': inspect.stack()[0][3], 'EXCEPTION': str(e)}
            self.logger.exception(message)
            raise
