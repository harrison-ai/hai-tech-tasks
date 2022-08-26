#  HAI Platform DevOps Tech Task

## Overview

We would like to deploy a small restful Python based HTTP API as a Proof of Concept, and would like our engineers to be able to run this API on their local deveopment machines using Docker Compose.  The API interacts with AWS DynamoDB, and is able to insert items into a DynamoDB table and retrieve them back again.  Items (or objects) in the API are identified by a UUID, a version 4 UUID to be specific.

In order to run locally, we wish to use the downloadable version of DynamoDB Local.  We have also provided a small Terraform module which can be used to deploy the DynamoDB table.  There is no requirement to persist the DynamoDB table to disk.


## Instructions

You are required to create the Docker Compose stack that engineers will run on their local development machines, along with a few other missing items:


1. Create the Dockerfile for the Python HTTP API.
2. Create the `docker-compose.yml` file for the complete stack.
3. The HTTP API should be accessible directly from the host OS.
4. Use the supplied terraform module to deploy DynamoDB Local.

You will require the following information to create the Dockerfile and Docker Compose stack:

- The API script itself, `main.py`.
- The required dependencies are listed in `requirements.txt`
- The command to run the docker container:  `uvicorn main:app --host "0.0.0.0" --port "8080"`
- The API requires the following environment variables configured:
    - DDB_ENDPOINT_URL (The DynamoDB Local endpoint)
    - DDB_TABLE_NAME (The name of the DynamoDB Local table)
    - AWS_REGION
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY


Create a git repo containing your solution and push it to Github. We'll provide you with a few specific github `@user` handles to share it with the team you're working with.

We will clone your repo and deploy your solution ourselves, adding and retrieving items from the API in order to test it.

## API Usage

To interact with the API and ensure it is working as intended, you can issue the following commands against it.

> Note that objects in the API are identified by Version 4 UUID's, which you will need to generate yourself.


### Add an object into the API

```
~ curl -X PUT <api-endpoint>:8080/object/457b8e8b-4691-47c0-b1d9-d423de0ad603

{"object":"457b8e8b-4691-47c0-b1d9-d423de0ad603"}
```


### Retrieve the object back from the API

```
~ curl <api-endpoint>:8080/object/457b8e8b-4691-47c0-b1d9-d423de0ad603

{"object":{"uuid":"457b8e8b-4691-47c0-b1d9-d423de0ad603","ts":"2022-08-25T12:06:56.563581"}}
```


### Retrieve all objects from the API


```
~ curl <api-endpoint>:8080/objects

{"objects":[{"uuid":"457b8e8b-4691-47c0-b1d9-d423de0ad603","ts":"2022-08-25T12:06:56.563581"},{"uuid":"7224d691-5c69-4741-bbaf-78f1972ce07d","ts":"2022-08-25T12:09:06.029340"},{"uuid":"103dd625-d455-4f66-86c5-0b2a165a228f","ts":"2022-08-25T12:08:04.409429"},{"uuid":"702ae388-378b-492a-90b3-d29fe03b2acb","ts":"2022-08-25T12:09:07.106006"}]}
```


### Delete all objects from the API

```
~ curl -X DELETE <api-endpoint>:8080/objects

{"msg": "Objects deleted"}
```

> Tip:  JQ is useful to format the output:


```
~ curl -s <api-endpoint>:8080/objects | jq

{
  "objects": [
    {
      "uuid": "457b8e8b-4691-47c0-b1d9-d423de0ad603",
      "ts": "2022-08-25T12:06:56.563581"
    },
    {
      "uuid": "7224d691-5c69-4741-bbaf-78f1972ce07d",
      "ts": "2022-08-25T12:09:06.029340"
    },
    {
      "uuid": "103dd625-d455-4f66-86c5-0b2a165a228f",
      "ts": "2022-08-25T12:08:04.409429"
    },
    {
      "uuid": "702ae388-378b-492a-90b3-d29fe03b2acb",
      "ts": "2022-08-25T12:09:07.106006"
    }
  ]
}
```


## Terraform AWS Provider

Use this as a starting point to get the Terraform AWS provider communicating with DynamoDB Local:

See also [official documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/custom-service-endpoints#dynamodb-local)

```
provider "aws" {

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    dynamodb = "http://<dynamodb local endpoint>:8000"
  }
}
```
