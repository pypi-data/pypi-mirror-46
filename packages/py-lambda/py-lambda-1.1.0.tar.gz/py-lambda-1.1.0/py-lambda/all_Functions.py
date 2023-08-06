#!/usr/bin/env python
def index(req, resp):
	if req.httpMeth() == "GET":
		resp.setResp(respBody = "This is index GET")
	elif req.httpMeth() == "POST":
		resp.setResp(respBody = "This is index POST", httpCode = 202, httpCodeStr = "202 OK")
	else:
		resp.setError(respBody = "Method not found", httpCode = 404, httpCodeStr = "404 ERROR")

def test(req, resp):
	if req.httpMeth() == "GET":
		resp.setResp(respBody = "This is test GET" )

def testUserId(req, resp):
	if req.httpMeth() == "GET":
		resp.setResp(respBody = "This is testUserId GET")

def abc(req, resp):
	if req.httpMeth() == "GET":
		resp.setResp(respBody = "This is abc GET")
