import boto3
from appsyncclient import AppSyncClient
import os
import json

import logging,base64

logger = logging.getLogger("realtime-aws-secretsmngr")

class RealTimeAwsSecretsMngr():
    def __init__(self,**kargs):
        self.region = kargs.get("region")
        self.secretId = kargs.get("secretId")

        if(self.secretId == None or self.region == None):
            logger.error("secretId and region required")
            raise Exception("configuration error")

        self.client = AppSyncClient(**kargs)
        self.botoclient = boto3.client("secretsmanager",region_name=self.region)

    def subscribe(self,callback):
        response = self.botoclient.get_secret_value(SecretId=self.secretId)
        secretString = response.get("SecretString")
        callback(secretString)

        secretString = secretString.replace("\"","\\\"")
        query = json.dumps({"query": "subscription {\n  updatedResource(id:\"arn:aws:secretsmanager:::"+self.secretId+"\") {\n    id\n    data\n  }\n}\n"})

        def secretcallback(client, userdata, msg):
            logger.debug("New data received : "+str(msg))
            callbackdatab64 = json.loads(msg.payload).get("data",{}).get("updatedResource",{}).get("data")
            logger.debug(callbackdatab64)
            try:
                callbackdata = base64.b64decode(callbackdatab64.encode("utf-8"))
                logger.debug(f"decoded successfully {callbackdata}")
                callback(callbackdata.decode("utf-8"))
            except Exception as e:
                logger.error(str(e))

        response = self.client.execute(data=query,callback=secretcallback)
