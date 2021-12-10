# Club App Backend
## Description
This is the backend implementation for the Club App project

## Technologies Used
- Python 3.9
- Github Actions
- Serverless Framework
- AWS

## Set Up for Development
1. Download the project:
```git
git clone https://github.com/benny568/cloudca.git
```
2. Navigate to project root:
```git
cd cloudca
```
3. Install dependencies:
```git
make setup
```
4. Running Tests:
```git
make tests
```
## Deploy to AWS

Deploy the project to AWS:
```
$ serverless deploy
```

After running deploy, you should see output similar to:

```bash
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
........
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service aws-python.zip file to S3 (711.23 KB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
.................................
Serverless: Stack update finished...
Service Information
service: aws-python
stage: dev
region: us-east-1
stack: aws-python-dev
resources: 6
functions:
  api: aws-python-dev-hello
layers:
  None
```

## Invocation

After successful deployment, you can invoke the deployed function by using the following command:

```bash
serverless invoke --function {function_name}
```

Which should result in response similar to the following:

```json
{
    "statusCode": 200,
    "body": "{\"message\": \"Go Serverless v2.0! Your function executed successfully!\", \"input\": {}}"
}
```
