---
title: "Posting a Tripwire IP360 ASPL update with Python"
date: 2025-10-24
categories: 
  - "ip360"
  - "scripts"
tags: 
  - "python"
  - "tripwire"
---

This one initially threw me, so I figured I'd post the script here for others in case they run into issues:

```
#-*- coding: utf-8 -*-
"""
@author: Chris Hudson
"""
"""
DEPENDENCIES:
"""
""" Required for sys calls such as exit() """
import sys
""" Required to do all HTTP request calls to the API: Run 'pip install requests' to add this to your Python
installation. """
import requests
import urllib3
from requests.auth import HTTPDigestAuth
import json
"""
GLOBAL VARIABLES:
"""
# These are the static parameters needed for the IP360 environment connection
IP360HOST="YourVnEHostname"
IP360USERNAME="UsernameHere"
IP360PASS="PasswordHere"
IP360BASEURL="https://"+IP360HOST+"/rest/v1"
# Set up Session() to not show warnings/errors for the self-signed cert
s = requests.Session() s.verify = False
urllib3.disable_warnings()
s.headers.update({
 "accept": "application/json, text/plain",
 "X-Requested-With": "required",
 "referer": "https://"+IP360HOST+"/rest/v1/updates"
})
# Do a login:
payload = {"login" : IP360USERNAME, "password" : IP360PASS, "do": "auth"}
login = s.post(url="https://%s/index.ice" % (IP360HOST), data=payload)
# For demo purposes, we initially make a call to retrieve the current update status
response = s.get(url="%s/updates/status" % (IP360BASEURL))
print(response.content)
# Posting a new ASPL
# In order to do a POST, we most set the CSRF token we got for the session
myheaders = s.headers
myheaders.update({'X-CSRFToken': login.cookies.get('csrftoken')})
# Now we can pass the ASPL/Ontology we wish to send - we should open this as a binary (rb) and make sure the
"name" is set appropraitely
files = {'file': ('vert-ontology-4-943.noarch.rpm', open('vert-ontology-4-943.noarch.rpm', 'rb'))}
# Now we can post to the API
response = s.post(url="%s/updates" % (IP360BASEURL), files=files, headers=myheaders)
print(response.content)
# Clean up and close the session
response.connection.close()
```
