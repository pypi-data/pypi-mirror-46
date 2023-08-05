import boto3
from appsyncclient import AppSyncClient
import os
import json

import logging
import base64

from pspring import Configuration
from .dynamodb import DynamoDBTable

logger = logging.getLogger(__name__)

config = Configuration.getConfig(__name__)

class RealTimeDynamoDB():
    def __init__(self,**kargs):
        self.tableName = kargs.get("tableName") or config.getProperty("tableName")
        self.primaryKey = kargs.get("primaryKey") or config.getProperty("primaryKey")
        self.primaryKeyName = kargs.get("primaryKeyName") or config.getProperty("primaryKeyName")
        self.sortKey = kargs.get("sortKey") or config.getProperty("sortKey")
        self.sortKeyName = kargs.get("sortKeyName") or config.getProperty("sortKeyName")
        self.region = kargs.get("region") or config.getProperty("region")
        self.configColumnName = kargs.get("configColumnName") or config.getProperty("configColumnName")

        @DynamoDBTable(
            tableName=self.tableName,
            primaryKey=self.primaryKeyName,
            sortKey=self.sortKeyName,
            region=self.region
        )
        class DynamoTable():
            pass
        self.table = DynamoTable()
        self.config = {}

        self.apiId = kargs.get("apiId") or config.getProperty("apiId")

        if(self.tableName == None or self.primaryKey == None or self.sortKey == None):
            logger.error("tableName,primaryKey and sortKey required")
            raise Exception("configuration error")
        self.client = AppSyncClient(region=self.region,apiId=self.apiId)

    def getValue(self):
        dynamoContent = self.table.get(self.primaryKey,scope=self.sortKey,column=self.configColumnName)
        return str(dynamoContent)

    def subscribe(self,callback):
        contents = self.getValue()
        callback(contents)
        id = "arn:aws:dynamodb:::"+self.tableName+":"+self.primaryKey
        if self.sortKey != None:
            id = id + ":"+self.sortKey
        query = json.dumps({"query": "subscription {\n  updatedResource(id:\""+id+"\") {\n    id\n    data\n  }\n}\n"})

        def secretcallback(client, userdata, msg):
            logger.debug("New data received : "+str(msg))
            callbackdatab64 = json.loads(msg.payload).get("data",{}).get("updatedResource",{}).get("data")
            logger.debug(callbackdatab64)
            if ( self.configColumnName != None ):
                try:
                    callbackdata = base64.b64decode(callbackdatab64.encode())
                    logger.debug(f"decoded successfully {callbackdata}")
                    callbackdatacolumn = json.loads(callbackdata.decode()).get(self.configColumnName)
                except Exception as e:
                    logger.error(str(e))
                

            callback(callbackdatacolumn)

        response = self.client.execute(data=query,callback=secretcallback)
