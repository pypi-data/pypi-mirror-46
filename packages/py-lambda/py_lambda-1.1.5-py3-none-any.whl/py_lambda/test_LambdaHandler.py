#!/usr/bin/env python

import sys, os, json, time
import lambda_function as lh
import request as Req
import response as Res

EVENT_FROM_ALB = {
					u"body": u"", 
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
						u"user-agent": u"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0", 
						u"cache-control": u"no-cache", 
						u"te": u"trailers", 
						u"cloudfront-is-desktop-viewer": u"true", 
						u"cloudfront-is-smarttv-viewer": u"false", 
						u"x-forwarded-for": u"119.82.100.218, 70.132.7.73", 
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

def testRequest():
	## Normal request
	print("************** Normal request **************")
	reqObj = Req.Request(EVENT_FROM_ALB)
	print("Path List:",reqObj.getPathList())
	print("Path Str:",reqObj.getPathStr())
	print("Req method:",reqObj.httpMeth())
	print("Req from ALB:",reqObj.isAlb())
	print("Cookies:",reqObj.getCookies())
	print("Query params by input list:",reqObj.getQueryParams(['a']))
	print("Query params all:",reqObj.getAllQueryParam())
	print("Base64 encooded:",reqObj.isBase64())

	## Remove alb
	print("************** ALB removed **************")
	del(EVENT_FROM_ALB["requestContext"])
	print("Req from ALB:",reqObj.isAlb())
	# print("EVENT_FROM_ALB:", EVENT_FROM_ALB)

def testResp():
	respObj = Res.Response()
	print("respObj:", respObj())
	respObj.setError()
	print("respObj:", respObj())
	respObj.setResp()
	print("respObj:", respObj())
	respObj.setResp(respBody={'a':1, 'b':2})
	print("respObj:", respObj())
	# respObj.setContentType("application/json")
	# print("respObj:", respObj())
	respObj.setHeader("Access-Control-Allow-Origin", "*")
	print("respObj:", respObj())

def testOptions():
	EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/test'
	EVENT_FROM_ALB["httpMethod"] = "OPTIONS"
	EVENT_FROM_ALB["headers"]["referer"] = "http://domain1.com"
	resp = lh.lambda_handler(event=EVENT_FROM_ALB,context= "some_context")
	print(resp)

def testPath():
	EVENT_FROM_ALB["headers"]["referer"] = "http://domain1.com"

	## Invalid method
	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/test'
	# EVENT_FROM_ALB["httpMethod"] = "POST"
	
	## Invalid resource
	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/invalid'
	# EVENT_FROM_ALB["httpMethod"] = "GET"

	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/test/123/invalid'
	# EVENT_FROM_ALB["httpMethod"] = "GET"
	
	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+''
	# EVENT_FROM_ALB["httpMethod"] = "DELETE"

	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/test'
	# EVENT_FROM_ALB["httpMethod"] = "POST"

	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/test/123'
	# EVENT_FROM_ALB["httpMethod"] = "POST"

	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/abc'
	# EVENT_FROM_ALB["httpMethod"] = "DELETE"

	## Valid method
	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+''
	# EVENT_FROM_ALB["httpMethod"] = "GET"

	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+''
	# EVENT_FROM_ALB["httpMethod"] = "POST"

	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/test'
	# EVENT_FROM_ALB["httpMethod"] = "GET"
	
	## User-id validation
	# EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/test/123'
	# EVENT_FROM_ALB["httpMethod"] = "GET"

	EVENT_FROM_ALB["path"]= RESOURCE_PREFIX+'/abc'
	EVENT_FROM_ALB["httpMethod"] = "GET"

	resp = lh.lambda_handler(event=EVENT_FROM_ALB,context= "some_context")
	print(resp)

def main():
    # testOptions()
    testPath()
	# resp = lh.lambda_handler(event=EVENT_FROM_ALB,context= "some_context")
	# print(resp)

if __name__ == "__main__":
	main()