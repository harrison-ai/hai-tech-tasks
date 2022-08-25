"""
A fictional proof of concept FastAPI Restful API

This code should not be considered production ready and is for demonstration purposes only
"""

import json
import logging
from datetime import datetime
from uuid import UUID

import boto3
import botocore
from fastapi import FastAPI, status
from pydantic import BaseSettings, Field


logger = logging.getLogger("uvicorn.error")


class Settings(BaseSettings):
    ddb_endpoint_url: str = Field(..., env="DDB_ENDPOINT_URL")
    aws_region: str = Field(..., env="AWS_REGION")
    ddb_table_name: str = Field(..., env="DDB_TABLE_NAME")


class DDB:
    def __init__(self):
        """AWS DynamoDB Resource Wrapper"""

        settings = Settings()

        self.resource = boto3.resource(
            "dynamodb",
            endpoint_url=settings.ddb_endpoint_url,
            region_name=settings.aws_region,
        )
        self.table = self.resource.Table(settings.ddb_table_name)

    def is_active(self):
        """Given a table name, determine if the table is in an ACTIVE state"""

        try:
            resp = self.table.table_status
            if resp == "ACTIVE":
                return True

        except self.table.meta.client.exceptions.ResourceNotFoundException as err:
            logger.error(err)

        return False

    def get_item(self, id):
        """Get a single item from the DynamoDB table"""

        resp = self.table.get_item(Key={"uuid": str(id)}, ConsistentRead=True)

        if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
            return None

        if "Item" in resp:
            return resp["Item"]

    def put_item(self, id):
        """Put a single item to the DynamoDB table"""

        resp = self.table.put_item(
            Item={"uuid": str(id), "ts": datetime.now().isoformat()}
        )

        if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
            return None

        return id

    def scan(self):
        """Scan the entire DynamoDB table
        Please note that this is for demonstration purpposes only
        and the use of the scan command is generally not recommended
        """

        resp = self.table.scan()

        if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
            return None

        return resp["Items"]

    def delete_item(self, item):
        """Delete an item from DynamoDB Table"""

        resp = self.table.delete_item(Key={"uuid": item})

        return resp


app = FastAPI()

table = DDB()


@app.on_event("startup")
def startup():
    """Runs on application startup to determine if database is ready for use"""

    status = table.is_active()

    if not status:
        logger.error("Unable to find the DynamoDB table; have you deployed it?")


@app.get("/")
async def root():
    """Hello World no op"""

    return {"Hello": "World"}


@app.get("/objects")
async def get_all_objects():
    """Return all objects"""

    resp = table.scan()

    return {"objects": resp}


@app.get("/object/{id}")
async def get_object(id: UUID):
    """Get an object"""

    resp = table.get_item(id)

    if resp:
        return {"object": resp}

    else:
        return {"object": {}}


@app.put("/object/{id}", status_code=status.HTTP_201_CREATED)
async def put_object(id: UUID):
    """Put an object"""

    resp = table.put_item(id)

    return {"object": resp}


@app.delete("/objects")
async def delete_objects():
    """Delete all objects"""

    resp = table.scan()

    for item in resp:
        table.delete_item(item["uuid"])

    return {"msg": "Objects deleted"}
