#!/usr/bin/env python
import lambda_defines as ld
import all_Functions as allFun

"""
Specify all the URL-mappings (routings) in this.

Depending on the mapping the request will be forwarded to a given function in the mapping according to 
the URL path that has been provided.

When the URL is in REST format then use ld.URL_REST_ID_STR in the mapping to indicate the REST-ID
/user/123/
To indicate user id as 123 use ld.URL_REST_ID_STR.
empty string "" in the mapping will be maping to exact path of the request.
"""
FUNCT_MAPPING = {
	"": {"": allFun.index},
	"test": {
		"": allFun.test,
		ld.URL_REST_ID_STR:{
			"": allFun.testUserId,
		},
	},
	"abc":{
		"": allFun.abc,
	},
}

if __name__ == "__main__":
	None