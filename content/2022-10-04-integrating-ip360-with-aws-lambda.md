---
title: "Integrating IP360 with AWS Lambda"
date: 2022-10-04
categories: 
  - "api"
  - "ip360"
  - "python"
tags: 
  - "tripwire"
---

I built the below script to allow users to easily scale our vulnerability management monitoring of servers deployed in AWS with automated exceptions being pulled from an S3 bucket and automatically added to Tripwire IP360 via a AWS Lambda call:

```
import boto3
from botocore.config import Config
import os
from base64 import b64decode
from botocore.exceptions import ClientError
import requests
import urllib3
import json
import uuid
import ipaddress
import struct
import time
import os
import sys
import argparse
"""
Functions - AWS
"""
def GET_EXCEPTION_AWS_S3(s3_bucket,filename):
 # Set up session not show warnings/errors for the self-signed cert
 s3 = boto3.resource('s3',verify=False)
 # Capture some info about session in case it's required
 client = boto3.client("sts")
 account_id = client.get_caller_identity()["Account"]
 verified_ip_list = []
 # Get data
 try:
 obj = s3.Object(s3_bucket,filename)
 body = obj.get()['Body'].read()
 print("Retrieved")
 if (body != ""):
 # Content exists, validate format
 ip_list = body.decode("utf-8").split("\r\n")
 for ip in ip_list:
 try:
 ipaddress.ip_address(ip)
 verified_ip_list.append(ip)
 except:
 print("Not a valid IP")
 return verified_ip_list
 except:
 print("Failed to retrieve data as "+ str(account_id))
"""
Functions - IP360
"""
# Set up Session() to not show warnings/errors for the self-signed cert
session = requests.Session()
session.verify = False
urllib3.disable_warnings()
session.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required"
})
def ip360baseurl(ip360vnehost):
 ip360baseurl = "https://"+ip360vnehost+"/rest/v1"
 return ip360baseurl
def GET_IP360_NETWORK(network_name,ip360vnehost,ip360username,ip360password):
 with requests.Session() as s:
 s.verify = False
 urllib3.disable_warnings()
 s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "Referer": ip360baseurl(ip360vnehost)
 })
 # Login
 try:
 payload = {"login" : ip360username, "password" : ip360password, "auth_type" : "internal",
"auth_server_id" : "0", "do": "auth"}
 login = s.post(url="https://%s/index.ice" % (ip360vnehost), data=payload)
 except:
 print("Failed log in - check credentials and network access")
 # Check for existing network
 try:
 network = s.get(url="https://%s/rest/v1/networks?name=%s" % (ip360vnehost,network_name))
 return network
 except:
 print("Network not found")
def GET_IP360_POOL(pool_name,ip360vnehost,ip360username,ip360password):
 with requests.Session() as s:
 s.verify = False
 urllib3.disable_warnings()
 s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "Referer": ip360baseurl(ip360vnehost)
 })
 # Login
 try:
 payload = {"login" : ip360username, "password" : ip360password, "auth_type" : "internal",
"auth_server_id" : "0", "do": "auth"}
 login = s.post(url="https://%s/index.ice" % (ip360vnehost), data=payload)
 except:
 print("Failed log in - check credentials and network access")
 # Check for existing network
 try:
 pool = s.get(url="https://%s/rest/v1/appliance_pools?name=%s" % (ip360vnehost,pool_name))
 return pool
 except:
 print("Pool not found")
def GET_IP360_SCAN_PROFILE(profile_name,ip360vnehost,ip360username,ip360password):
 with requests.Session() as s:
 s.verify = False
 urllib3.disable_warnings()
 s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "Referer": ip360baseurl(ip360vnehost)
 })
 # Login
 try:
 payload = {"login" : ip360username, "password" : ip360password, "auth_type" : "internal",
"auth_server_id" : "0", "do": "auth"}
 login = s.post(url="https://%s/index.ice" % (ip360vnehost), data=payload)
 except:
 print("Failed log in - check credentials and network access")
 # Check for existing network
 try:
 profile = s.get(url="https://%s/rest/v1/scan_profiles?search=%s" % (ip360vnehost,profile_name))
 return profile
 except:
 print("Scan Profile not found")
def GET_IP360_CREDENTIAL(credential_name,ip360vnehost,ip360username,ip360password):
 with requests.Session() as s:
 s.verify = False
 urllib3.disable_warnings()
 s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "Referer": ip360baseurl(ip360vnehost)
 })
 # Login
 try:
 payload = {"login" : ip360username, "password" : ip360password, "auth_type" : "internal",
"auth_server_id" : "0", "do": "auth"}
 login = s.post(url="https://%s/index.ice" % (ip360vnehost), data=payload)
 except:
 print("Failed log in - check credentials and network access")
 # Check for existing network
 try:
 credential = s.get(url="https://%s/rest/v1/credentials?name=%s" % (ip360vnehost,credential_name))
 return credential
 except:
 print("Scan Profile not found")
def SET_IP360_NETWORK(network_name,included_ips,ip360vnehost,ip360username,ip360password):
 with requests.Session() as s:
 # !!! Disables SSL validation for self signed certs- NOT RECOMMENDED !!!
 s.verify = False
 urllib3.disable_warnings()
 s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "Referer": ip360baseurl(ip360vnehost)
 })
 # Login
 try:
 payload = {"login" : ip360username, "password" : ip360password, "auth_type" : "internal",
"auth_server_id" : "0", "do": "auth"}
 login = s.post(url="https://%s/index.ice" % (ip360vnehost), data=payload)
 except:
 print("Failed log in - check credentials and network access")
 # Check for existing network
 networks = s.get(url="https://%s/rest/v1/networks?search=%s" % (ip360vnehost,network_name))
 #print("Matching name network found (count):"+json.loads(networks.content)["count"])
 if (json.loads(networks.content)["count"] > 0):
 # If we get this far, the network exists, so we need to patch it instead:
 print("Existing network with matching name found, updating")
 networks = json.loads(networks.content)
 network_to_update = networks["results"][0]
 payload = {
 "url": network_to_update["url"],
 "name": network_to_update["name"],
 "asset_value": network_to_update["asset_value"],
 #"notes": network_to_update["notes"]+". Updated by API",
 "include_ips": network_to_update["include_ips"]+ "," + included_ips,
 #"exclude_ips": network_to_update["exclude_ips"]+ "," + excluded_ips,
 "exclude_ips": "",
 "virtual_hosts": [],
 "network_type": "default",
 "effective_ranges": network_to_update["effective_ranges"],
 }
 try:
 patch_network = s.patch(url=network_to_update["url"], data=payload, auth=(ip360username,
ip360password))
 except:
 print("Failed to update existing network: "+ network_name +", check permissions/network
configuration")
 else:
 # Post a new network :
 payload = {
 "name": network_name,
 "active": True,
 "notes": "Created by API",
 "include_ips": included_ips,
 #"exclude_ips": excluded_ips,
 "exclude_ips": "",
 "host_tracking": "{\"correlation_threshold\": 90, \"correlation_method\": \"Static IP\", \"
correlation_values\": {\"DNS Name\": 0.0, \"OS Fingerprint\": 0.0, \"NetBIOS Name\": 0.0, \"Apparent MAC
Address\": 0.0, \"Port Signature\": 0.0, \"IP Address\": 100.0, \"Operating System\": 0.0}}",
 }
 print("Network config:")
 print(payload)
 try:
 post_new_network = s.post(url="%s/networks" % (ip360baseurl(ip360vnehost)), data=payload, auth=
(ip360username,ip360password))
 print("Added new network: "+network_name)
 except:
 print("Failed to add a new network - check access and network parameters")
 print("Adding/updating network complete for "+network_name)
def REPLACE_IP360_NETWORK(network_name,included_ips,excluded_ips,ip360vnehost,ip360username,ip360password):
 with requests.Session() as s:
 s.verify = False
 urllib3.disable_warnings()
 s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "Referer": ip360baseurl(ip360vnehost)
 })
 try:
 payload = {"login" : ip360username, "password" : ip360password, "auth_type" : "internal",
"auth_server_id" : "0", "do": "auth"}
 login = s.post(url="https://%s/index.ice" % (ip360vnehost), data=payload)
 except:
 print("Failed log in - check credentials and network access")
 networks = s.get(url="https://%s/rest/v1/networks?search=%s" % (ip360vnehost,network_name), auth=
(ip360username, ip360password))
 if (json.loads(networks.content)["count"] > 0):
 # network exists - so remove it first
 print("Removing existing duplicate network")
 networks = json.loads(networks.content)
 network_to_update = networks["results"][0]
 payload = {
 "url": network_to_update["url"],
 "name": network_to_update["name"],
 }
 try:
 delete_network = s.delete(url=network_to_update["url"], data=payload, auth=(ip360username,
ip360password))
 except:
 print("Failed to remove existing network: "+ network_name +", check scan task is not in
progress / locked")
 payload = {
 "name": network_name,
 "active": True,
 "notes": "Created by API",
 "include_ips": included_ips,
 "exclude_ips": excluded_ips,
 "host_tracking": "{\"correlation_threshold\": 90, \"correlation_method\": \"Static IP\", \"
correlation_values\": {\"DNS Name\": 0.0, \"OS Fingerprint\": 0.0, \"NetBIOS Name\": 0.0, \"Apparent MAC
Address\": 0.0, \"Port Signature\": 0.0, \"IP Address\": 100.0, \"Operating System\": 0.0}}",
 }
 print(payload)
 try:
 post_new_network = s.post(url="%s/networks" % (ip360baseurl(ip360vnehost)), data=payload, auth=
(ip360username,ip360password))
 print("Added new network: "+network_name)
 except:
 print("Failed to add a new network - check access and network parameters")
def EXECUTE_IP360_ADHOC_SCAN(network,pool,scanprofile,ip360vnehost,ip360username,ip360password):
 network_set = GET_IP360_NETWORK(network,ip360vnehost,ip360username,ip360password)
 pool_set = GET_IP360_POOL(pool,ip360vnehost,ip360username,ip360password)
 profile_set = GET_IP360_SCAN_PROFILE(scanprofile,ip360vnehost,ip360username,ip360password)
 print("Sending ahoc scan request to %s as %s" % (ip360baseurl(ip360vnehost), ip360username))
 PAYLOAD={
 "debug": False,
 "name": "Adhoc Automated Scan",
 "network": json.loads(network_set.content)["results"][0]["url"],
 "pool": json.loads(pool_set.content)["results"][0]["url"],
 "scan_profile": json.loads(profile_set.content)["results"][0]["url"],
 "special_scan": False
 }
 postscan = session.post(url="%s/audits" % (ip360baseurl(ip360vnehost)), auth=(ip360username, ip360password),
json=PAYLOAD)
 print(postscan.content)
 postscan.connection.close()
def SET_IP360_SCHEDULED_SCAN(network,pool,scanprofile,ip360vnehost,ip360username,ip360password):
 # Get Network
 network_set = GET_IP360_NETWORK(network,ip360vnehost,ip360username,ip360password)
 # Get appliance pool
 pool_set = GET_IP360_POOL(pool,ip360vnehost,ip360username,ip360password)
 # Get scan profile
 profile_set = GET_IP360_SCAN_PROFILE(scanprofile,ip360vnehost,ip360username,ip360password)
 # Check for existing scan
 config_name = "Auto-" + json.loads(network_set.content)["results"][0]["name"] + json.loads(profile_set.
content)["results"][0]["name"] + " Scan"
 scheduledscans = session.get(url="https://%s/rest/v1/scan_configs?name=%s" % (ip360vnehost,config_name),
auth=(ip360username, ip360password))
 # Unforunately filtering for network names isn't consistent in older versions of IP360, so we need to check
our scan names to verify it doesn't already exist
 for scans in json.loads(scheduledscans.content)["results"]:
 if (scans["name"] == config_name):
 # Update existing scheduled scan
 print("Scheduled Scan already exists - no action taken")
 break
 else:
 # Post scheduled scan
 print("Sending scan scheduling request to %s as %s" % (ip360baseurl(ip360vnehost), ip360username))
 PAYLOAD={
 "active": True,
 "name": "Auto-" + json.loads(network_set.content)["results"][0]["name"] + json.loads
(profile_set.content)["results"][0]["name"] + " Scan",
 "network": json.loads(network_set.content)["results"][0]["url"],
 "pool": json.loads(pool_set.content)["results"][0]["url"],
 "scan_profile": json.loads(profile_set.content)["results"][0]["url"],
 }
 postscan = session.post(url="%s/scan_configs" % (ip360baseurl(ip360vnehost)), auth=(ip360username,
ip360password),json=PAYLOAD)
 postscan.connection.close()
def SET_IP360_CREDENTIAL(credential_name,credential_username,credential_password,credential_domain,
credential_auth_algo,ip360network,exceptionip,ip360vnehost,ip360username,ip360password):
 with requests.Session() as s:
 # !!! Disables SSL validation for self signed certs- NOT RECOMMENDED !!!
 s.verify = False
 urllib3.disable_warnings()
 s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "Referer": ip360baseurl(ip360vnehost)
 })
 payload = {"login" : ip360username, "password" : ip360password, "auth_type" : "internal",
"auth_server_id" : "0", "do": "auth"}
 login = s.post(url="https://%s/index.ice" % (ip360vnehost), data=payload)
 payload = {"name":credential_name, "username":credential_username, "password":credential_password,
"domain":credential_domain, "minimum_auth_algorithm":credential_auth_algo}
 try:
 POSTCREDS = s.post(url="%s/credential/windows" % (ip360baseurl(ip360vnehost)), data=payload, auth=
(ip360username,ip360password))
 JSONCREDS = json.loads(POSTCREDS.text)
 payload = {"credential": JSONCREDS["url"], "network": ip360network, "ip_ranges": exceptionip}
 try:
 POSTCREDBIND = s.post(url="%s/credential/bindings" % (ip360baseurl(ip360vnehost)),
data=payload, auth=(ip360username,ip360password))
 except:
 print("Failed to bind credential to a network")
 except:
 print("Failed to add credential to IP360")
 print("Finished!")
def BIND_IP360_CREDENTIAL(credential_name,ip360network,ipbind,ip360vnehost,ip360username,ip360password):
 with requests.Session() as s:
 # !!! Disables SSL validation for self signed certs- NOT RECOMMENDED !!!
 s.verify = False
 urllib3.disable_warnings()
 s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "Referer": ip360baseurl(ip360vnehost)
 })
 payload = {"login" : ip360username, "password" : ip360password, "auth_type" : "internal",
"auth_server_id" : "0", "do": "auth"}
 login = s.post(url="https://%s/index.ice" % (ip360vnehost), data=payload)
 credential = GET_IP360_CREDENTIAL(credential_name,ip360vnehost,ip360username,ip360password)
 network = GET_IP360_NETWORK(ip360network,ip360vnehost,ip360username,ip360password)
 JSONnetwork = json.loads(network.text)
 JSONCREDS = json.loads(credential.text)
 payload = {"credential": JSONCREDS["results"][0]["url"], "network": JSONnetwork["results"][0]["url"],
"ip_ranges": ipbind}
 try:
 POSTCREDBIND = s.post(url="%s/credential/bindings" % (ip360baseurl(ip360vnehost)), data=payload,
auth=(ip360username,ip360password))
 except:
 print("Failed to post credential")
 print("Finished!")
def initiate_adhoc_scan(network,pool,range,scanprofile,ip360baseurl,ip360username,ip360password):
 print("Sending ahoc scan request to %s as %s" % (ip360username, ip360password))
 PAYLOAD={
 "debug": False,
 "name":"Test100",
 "network":ip360baseurl+"/networks/3",
 "pool":ip360baseurl+"/appliance_pools/1",
 "range": range,
 "scan_profile": ip360baseurl+"/scan_profiles/5",
 "scan_profile_type": "Discovery",
 "scan_type": "Partial",
 "special_scan": False
 }
 postscan = session.post(url="%s/audits" % (ip360baseurl), auth=(ip360username, ip360password),json=PAYLOAD)
 print(postscan.content)
 postscan.connection.close()
def DO_IP360_ADHOC_SCAN(network,iptoscan,pool,scanprofile,ip360vnehost,ip360username,ip360password):
 # Get Network
 network_set = GET_IP360_NETWORK(network,ip360vnehost,ip360username,ip360password)
 # Get appliance pool
 pool_set = GET_IP360_POOL(pool,ip360vnehost,ip360username,ip360password)
 # Get scan profile
 profile_set = GET_IP360_SCAN_PROFILE(scanprofile,ip360vnehost,ip360username,ip360password)
 # Check for existing scan
 config_name = "Auto-" + json.loads(network_set.content)["results"][0]["name"] + json.loads(profile_set.
content)["results"][0]["name"] + " Scan"
 # Post scheduled scan
 print("Sending scan scheduling request to %s as %s" % (ip360baseurl(ip360vnehost), ip360username))
 PAYLOAD={
 "debug":False,
 "name": "Auto-" + json.loads(network_set.content)["results"][0]["name"] + json.loads
(profile_set.content)["results"][0]["name"] + " Scan",
 "network": json.loads(network_set.content)["results"][0]["url"],
 "range":iptoscan,
 "pool": json.loads(pool_set.content)["results"][0]["url"],
 "scan_profile": json.loads(profile_set.content)["results"][0]["url"],
 "scan_type": "Partial",
 "special_scan": False
 }
 try:
 postscan = session.post(url="%s/audits" % (ip360baseurl(ip360vnehost)), auth=(ip360username,
ip360password),json=PAYLOAD)
 except:
 print("Failed to create Adhoc Scan")
 postscan.connection.close()
def get_secret():
 secret_name = "/tripwire/vnepw"
 region_name = "eu-west-1"
 # Create a Secrets Manager client
 sm_session = boto3.session.Session()
 sm_client = sm_session.client(
 service_name='secretsmanager',
 region_name=region_name,
 config=Config(
 proxies={'https': os.environ['PROXY']}
 )
 )
 #Get the secret password from Secrets Manager
 try:
 get_secret_value_response = sm_client.get_secret_value(
 SecretId=secret_name
 )
 except ClientError as e:
 print(e)
 if e.response['Error']['Code'] == 'DecryptionFailureException':
 # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
 # Deal with the exception here, and/or rethrow at your discretion.
 raise e
 elif e.response['Error']['Code'] == 'InternalServiceErrorException':
 # An error occurred on the server side.
 # Deal with the exception here, and/or rethrow at your discretion.
 raise e
 elif e.response['Error']['Code'] == 'InvalidParameterException':
 # You provided an invalid value for a parameter.
 # Deal with the exception here, and/or rethrow at your discretion.
 raise e
 elif e.response['Error']['Code'] == 'InvalidRequestException':
 # You provided a parameter value that is not valid for the current state of the resource.
 # Deal with the exception here, and/or rethrow at your discretion.
 raise e
 elif e.response['Error']['Code'] == 'ResourceNotFoundException':
 # We can't find the resource that you asked for.
 # Deal with the exception here, and/or rethrow at your discretion.
 raise e
 else:
 # Decrypts secret using the associated KMS CMK.
 # Depending on whether the secret is a string or binary, one of these fields will be populated.
 if 'SecretString' in get_secret_value_response:
 secret = get_secret_value_response['SecretString']
 return secret
 else:
 decodedBinarySecret = base64.b64decode(get_secret_value_response['SecretBinary'])
 return decodedBinarySecret
def lambda_handler(event, context):
 DEBUG = os.environ['DEBUG']
 VNEIP = os.environ['VNEIP']
 IP360DP = os.environ['IP360DP']
 IP360PROFILE = os.environ['IP360PROFILE']
 IP360NETWORK = os.environ['IP360NETWORK']
 VNEUSER = os.environ['VNEUSER']
 CUSTOMERS = os.environ['CUSTOMERS'].split(",")
 MPCAWSEXCEPTIONLIST = os.environ['MPCAWSEXCEPTIONLIST'].split(",")
 EXCEPTIONLISTBUCKET = os.environ['EXCEPTIONLISTBUCKET']
 ENVIRONMENT = os.environ['ENVIRONMENT']
 IPSCANLIST = []
 try:
 SINGLE_IP = event['SingleIP']
 except:
 SINGLE_IP = 'NOIP'
 IPSCANLIST = []
 if DEBUG == "True":
 print (SINGLE_IP)
 # setup connection to AWS
 kms_client = boto3.client(
 'kms',
 config=Config(
 proxies={'https': os.environ['PROXY']}
 )
 )
 sts_client = boto3.client(
 'sts',
 config=Config(
 proxies={'https': os.environ['PROXY']}
 )
 )
 if SINGLE_IP == "NOIP":
 # event contains all information about uploaded object
 if DEBUG == "True":
 print("Event :", event)
 # Bucket Name where file was uploaded
 source_bucket_name = event['Records'][0]['s3']['bucket']['name']
 # Filename of object (with path)
 file_key_name = event['Records'][0]['s3']['object']['key']
 if DEBUG == "True":
 print (source_bucket_name)
 print (file_key_name)
 # Read the exception list
 s3_exceptionlist_Resource=boto3.resource(
 's3',
 config=Config(
 proxies={'https': os.environ['PROXY']}
 ),
 )
 s3_exceptionlist_obj = s3_exceptionlist_Resource.Object(EXCEPTIONLISTBUCKET, 'tripwire_exceptions.txt')
 exceptionlist = s3_exceptionlist_obj.get()['Body'].read().decode('utf-8').splitlines()
 print(exceptionlist)
 # Read the post patching input file
 s3_post_patching_Resource=boto3.resource(
 's3',
 config=Config(
 proxies={'https': os.environ['PROXY']}
 )
 )
 s3_post_patching_obj = s3_post_patching_Resource.Object(source_bucket_name, file_key_name)
 post_patching_scanlist = s3_post_patching_obj.get()['Body'].read().decode('utf-8').splitlines()
 #print (post_patching_scanlist)
 for post_patching_scanline in post_patching_scanlist:
 if post_patching_scanline != "":
 CUSTOMERCODE = post_patching_scanline.split(',')[0]
 FQDN = post_patching_scanline.split(',')[1]
 IP_ADDRESS = post_patching_scanline.split(',')[2]
 if CUSTOMERCODE.upper() in CUSTOMERS:
 if IP_ADDRESS not in exceptionlist:
 if FQDN not in MPCAWSEXCEPTIONLIST:
 if DEBUG == "True":
 print ("IP: " + IP_ADDRESS + " FQDN: " + FQDN)
 IPSCANLIST.append(IP_ADDRESS)
 else:
 IPSCANLIST.append(SINGLE_IP)
 #Check scan list
 if DEBUG == "True":
 print (IPSCANLIST)
 IPCOMMASEPERATED = ""
 for IP in IPSCANLIST:
 IPCOMMASEPERATED = IPCOMMASEPERATED + IP + ","
 IPCOMMASEPERATED = IPCOMMASEPERATED[:-1]
 if DEBUG == "True":
 print (IPCOMMASEPERATED)
 if ENVIRONMENT == "QA":
 #Check connectivity to VNE
 response = requests.get('https://' + VNEIP, verify=False)
 print ("VNE connection status code: " + str(response.status_code))
 else:
 #Get the secret password from Secrets Manager
 ip360password = (json.loads(get_secret()))['VNEPassword']
 REPLACE_IP360_NETWORK(IP360NETWORK,IPCOMMASEPERATED,"",VNEIP,VNEUSER,ip360password)
 EXECUTE_IP360_ADHOC_SCAN(IP360NETWORK,IP360DP,IP360PROFILE,VNEIP,VNEUSER,ip360password)
 print ("Tripwire scan initiated")
```
