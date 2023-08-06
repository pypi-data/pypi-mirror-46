#!/usr/bin/env python
import sys, os, json, time
import funct_defines as funDef

## VALID_DOMAINS contain list of domain names that should be considerd as valid.
VALID_DOMAINS 		= ["domain1.com", "domain2.org"] ## google.com, testdomain.org
## VALID_SUB_DOMAINS contain list of sub-domains that should be considered as valid.
VALID_SUB_DOMAINS	= ["subdomain1", "subdomain2"] ## subdomain1.test.com, subdomain2.test.com

def validateDomain(inpDomain, allSubDom = True):
	"""
	[Function]	: 	Validates the input domain with the list of valid domains in the constants VALID_DOMAINS and list of valid sub-domains in the constant VALID_SUB_DOMAINS.
	[Input]		: 	inpDomain	-> String contain input domian.
					allSubDom	-> Validate all the subdomains. 
	"""
	inpDomain = str(inpDomain)
	# if not isinstance(inpDomain, str):
	# 	return {funDef.FUNCTION_STAT:funDef.FAIL, funDef.FUNCTION_CODE:funDef.ERROR_C_INV_INP, funDef.FUNCTION_MSG:"Invalid input type"}
	
	if inpDomain.lower().startswith("http://"):
		inpDomain = inpDomain[7:]
	if inpDomain.lower().startswith("https://"):
		inpDomain = inpDomain[8:]
	domCName = inpDomain
	domainPtr = inpDomain.find('/')
	if domainPtr > 1:
		domCName = inpDomain[:domainPtr]
	domCName = domCName.lower()
	## Check for main domain and all the other allowed domains
	if domCName in VALID_DOMAINS:
		return {funDef.FUNCTION_STAT:funDef.SUCCESS, funDef.FUNCTION_DATA:domCName, funDef.FUNCTION_MSG:""}
	
	## Validate sub domains
	splitDomain = domCName.split(".")
	if len(splitDomain) < 3:
		return {funDef.FUNCTION_STAT:funDef.FAIL, funDef.FUNCTION_CODE:funDef.ERROR_C_INV_INP, funDef.FUNCTION_MSG:"Invalid subdomain: %s"%(domCName)}
	
	## the suffix has to be *.test.com
	if splitDomain[-2] != "domain1" and splitDomain[-1] != "com": ## Validate the domain
		return {funDef.FUNCTION_STAT:funDef.FAIL, funDef.FUNCTION_CODE:funDef.ERROR_C_INV_INP, funDef.FUNCTION_MSG:"Invalid subdomain: %s"%(domCName)}
	
	## Success of all the subdomain
	if allSubDom:
		return {funDef.FUNCTION_STAT:funDef.SUCCESS, funDef.FUNCTION_DATA:domCName, funDef.FUNCTION_MSG:""}

	## Validate only specific sub domains
	subDomain = '.'.join(splitDomain[:-2])
	if subDomain in VALID_SUB_DOMAINS:
		return {funDef.FUNCTION_STAT:funDef.SUCCESS, funDef.FUNCTION_DATA:domCName, funDef.FUNCTION_MSG:""}
		
	return {funDef.FUNCTION_STAT:funDef.FAIL, funDef.FUNCTION_CODE:funDef.ERROR_C_INV_INP, funDef.FUNCTION_MSG:"Invalid subdomain: %s"%(domCName)}

def main():
	None

if __name__ == "__main__":
	main()