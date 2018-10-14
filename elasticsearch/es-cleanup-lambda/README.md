# AWS Lambda Elasticsearch Index Cleanup

## Overview
This AWS Lambda function allows you to delete the old Elasticsearch indexes using SigV4Auth authentication. You configure the AWS Elasticsearch Access Policy authorizing the Lambda Role or the AWS Account number instead of using the IP address whitelist.

## Getting Started
### How To install

Configure in a proper way the IAM policy inside `json_file/es_policy.json` and `json_file/trust_policy.json`

Create the IAM Role

```bash
$ aws iam create-role --role-name es-cleanup-lambda \
	--assume-role-policy-document file://json_file/trust_policy.json

```

```bash
$ aws iam put-role-policy --role-name es-cleanup-lambda \
    --policy-name es_cleanup \
    --policy-document file://json_file/es_policy.json
```

``` bash
$ aws iam attach-role-policy \
	--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole \
	--role-name es-cleanup-lambda
```

Create your Lambda package

```bash
$ zip es-cleanup-lambda.zip es-cleanup.py
```


### Lambda deployment
Using awscli you can create your AWS function and set the proper IAM role with the right Account ID

```bash
$ export AWS_DEFAULT_REGION=eu-west-1
$ ESENDPOINT="search-es-demo-zveqnhnhjqm5flntemgmx5iuya.eu-west-1.es.amazonaws.com" #ES endpoint

$ aws lambda create-function \
	--function-name es-cleanup-lambda \
	--environment Variables={es_endpoint=$ESENDPOINT} \
	--zip-file fileb://es-cleanup-lambda.zip \
	--description "Elastichsearch Index Cleanup" \
	--role arn:aws:iam::123456789012:role/es-cleanup-lambda \
	--handler es-cleanup.lambda_handler \
	--runtime python2.7 \
	--timeout 180
```

Create your AWS Cloudwatch rule to run it periodically:

```bash
$ aws events put-rule \
	--name my-scheduled-rule \
	--schedule-expression 'cron(0 1 * * ? *)'
    
    
$ aws lambda add-permission \
	--function-name es-cleanup-lambda \
	--statement-id my-scheduled-event \
	--action 'lambda:InvokeFunction' \
	--principal events.amazonaws.com \
	--source-arn arn:aws:events:eu-west-1:123456789012:rule/my-scheduled-rule    
    
    
$ aws events put-targets \
	--rule my-scheduled-rule \
	--targets file://json_file/cloudwatch-target.json
```

IMPORTANT:

In order to make this work, I needed to to run this Lambda function inside the VPC and subnet the ES instance runs in. Additionally, I needed to use the same security groups as the ES proxy server is using.

### Lambda configuration and OS parameters

Using AWS environment variable you can easily modify the behaviour of the Lambda function

| Variable Name | Example Value | Description | Default Value | Required | 
| --- | --- | --- | --- |  --- |
| es_endpoint | search-es-demo-zveqnhnhjqm5flntemgmx5iuya.eu-west-1.es.amazonaws.com  | AWS ES fqdn | `None` | True | 
| index |  `logstash,cwl` | Index/indices to process comma separated, with `all` every index will be processed except `.kibana` | `all` | False |
| index_format  | `%Y.%m.%d` | Combined with `index` varible is used to evaluate the index age | `%Y.%m.%d` |  False | 
| delete_after | `7` | Numbers of days to preserve | `15` |  False | 
| sns_alert | `arn:aws:sns:eu-west-1:123456789012:sns-alert` | SNS ARN to pusblish any alert | | False |

