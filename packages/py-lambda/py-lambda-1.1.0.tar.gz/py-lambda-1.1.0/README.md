# AWS-ALB-lambda-python

Framework for load-balancer and lambda function.

To learn more about writing AWS Lambda functions in python, go to [the official documentation](https://docs.aws.amazon.com/lambda/latest/dg/services-alb.html)

Blogs about AWS lambda and python is [here](https://aws.amazon.com/blogs/networking-and-content-delivery/lambda-functions-as-targets-for-application-load-balancers/)


[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![serverless](http://public.serverless.com/badges/v3.svg)](4)
[![Pyhton-Lambda-Doc](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](1)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](5)
[![PyPI version fury.io](https://badge.fury.io/py/ansicolortags.svg)](7)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](2)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](2)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](3)
[![Pyhton Lambda](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://docs.aws.amazon.com/lambda/latest/dg/services-alb.html)
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

[1]: https://docs.aws.amazon.com/lambda/latest/dg/services-alb.html
[2]: https://aws.amazon.com/blogs/networking-and-content-delivery/lambda-functions-as-targets-for-application-load-balancers/
[3]: https://github.com/aws-samples/serverless-sinatra-sample
[4]: https://docs.aws.amazon.com/lambda/latest/dg/services-alb.html
[5]: https://www.python.org/
[6]: https://pypi.python.org/
[7]: https://pypi.python.org/pypi/ajayau404/
[8]: https://pypi.python.org/pypi/ansicolortags/

# Getting Started

This is the AWS lambda framework written in python. When the lambda function is triggered by ALB or API-Gateway the event variable that contain all the required info will be sent to the init function. By default this init function will be in lambda_function.py and the name will be lambda_handler. This framework contains the code from which you can call the functions that are required according to the path given the request.

This source code contain the following files:
* **lambda_function** : Contains the code that will be triggered by ALB or API-Gateway etc.
* **request** : Contains the request object which is created from the event that is send as an input.
* **response** : Contains the object that should be sent back from lambda function to ALB.
* **lambda_mapping** : Is the file that contain the mapping for the routes. Add your routes in here.
* **all_functions** : Contain the function contains the respective code that can be used for the given path.
* **test_LambdaHandler** : Contains the test code that can be usedfortesting all the functions.

``` Python
## lambda_function.py

import lambda_function as lf

EVENT_FROM_ALB = {  "body": u"", 
	u"requestContext": 
	{u"elb": 
		{
			u"targetGroupArn": u"arn:aws:elb:ap-region-1:11:targetgroup/FROM_TARGET-GROUP/abc"
		}
	}, 
	u"queryStringParameters": {"a":1}, 
	u"httpMethod": u"GET", 
	u"headers": 
	{
		u"via": u"2.0 test.cloudfront.net (CloudFront)", 
		u"accept-language": u"en-US,en;q=0.5", 
		u"cloudfront-viewer-country": u"IN", 
		u"accept": u"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
		u"upgrade-insecure-requests": u"1", 
		u"cloudfront-is-mobile-viewer": u"false", 
		u"accept-encoding": u"gzip, deflate, br", 
		u"x-forwarded-port": u"443", 
		u"user-agent": u"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/", 
		u"cache-control": u"no-cache", 
		u"te": u"trailers", 
		u"cloudfront-is-desktop-viewer": u"true", 
		u"cloudfront-is-smarttv-viewer": u"false", 
		u"x-forwarded-for": u"192.168.1.1, 1.1.1.1", 
		u"x-amzn-trace-id": u"Root=1-5c0a5a83-123344", 
		u"host": u"clib.fyers.in", 
		u"x-forwarded-proto": u"https", 
		u"x-amz-cf-id": u"abc==", 
		u"pragma": u"no-cache", 
		u"connection": u"Keep-Alive", 
		u"cloudfront-is-tablet-viewer": u"false", 
		u"cloudfront-forwarded-proto": u"https"
	}, 
	u"path": u"/Some_ramdom_path/345/", 
	u"isBase64Encoded": False
}

RESOURCE_PREFIX = ""
EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/abc'
EVENT_FROM_ALB["httpMethod"] = "GET"

resp = lf.lambda_handler(event=EVENT_FROM_ALB,context= "some_context")
print(resp)
```
