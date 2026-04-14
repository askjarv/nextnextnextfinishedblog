---
title: "Exploring the Tripwire IP360 API with Python 3"
date: 2020-05-21
tags: 
  - "api"
  - "python3"
  - "tripwire"
---

I've been busy re-familiarizing myself with Python now that Python 3 has tweaked the syntax just enough that I kept getting frustrated that I had to double check my syntax! At the same time, Tripwire has added some great new functionality in the REST API for Tripwire IP360, the Vulnerability Management solution, and it seemed natural to start building up a repository of useful scripts exploring and leveraging the Tripwire IP360 API as a result.

Getting Started

So let's get start with some simple functionality - logging in and getting some basic data out of the API.

First off, there's a few useful imports we'll end up using (I think this will cover all of my goals so whilst I may not use all these features in this post, we'll likely come back and use these in time!):

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

""" Required to do all HTTP request calls to the API: Run 'pip install requests' to add this to your Python installation. """
import requests
import urllib3

""" Not explicitly required, but definitely polite to be able to not echo password input from the user. """
import getpass

""" Required to confirm server hostname exists and is resolveable and validate IP's"""
import socket,struct

""" Required to pull SSL certs down from the TE console """
#import ssl

""" Required to decode and display content of SSL certs for verification """
#import OpenSSL

import json

```

OK, now we have our pre-reqs in place, I'm going to define some variables we'll use for our connection for our testing - of course, you'll want these to to reflect your IP360 instance. Note that I'm taking the IP360 host and creating a new string with the full URL for the REST API - **"https://"+IP360HOST+"/rest/v1"**

```
"""
GLOBAL VARIABLES:
"""
# These are the static parameters needed for the IP360 environment connection
IP360HOST="192.168.0.72"
IP360USERNAME="ip360@tripwire.com"
IP360PASS="Tripwire"
IP360BASEURL="https://"+IP360HOST+"/rest/v1"
```

With our variables and imports done, I can get ready to connect. My lab environment is using a self-signed cert (I replace it regularly, although I do realise that's no excuse for not using a proper cert!) - to handle the SSL errors I'll use the following:

```
"""
BEGIN CODE:
"""

# Set up Session() to not show warnings/errors for the self-signed cert
session = requests.Session()
session.verify = False
urllib3.disable_warnings()
session.headers.update({
    "accept": "application/json, text/plain",
    "X-Requested-With": "required"
})
```

OK - let's try getting some data! The following code snippets will gather users, networks, scan profiles and scan configs - some of the most common things you'd be interested in gathering:

```
# Get users
response = session.get(url="%s/users" % (IP360BASEURL), auth=(IP360USERNAME, IP360PASS))
response.connection.close()

# Get networks
networks = session.get(url="%s/networks" % (IP360BASEURL), auth=(IP360USERNAME, IP360PASS))
networks.connection.close()

# Get Scan Profiles
profiles = session.get(url="%s/scan_profiles" % (IP360BASEURL), auth=(IP360USERNAME, IP360PASS))
profiles.connection.close()

# Get Scan Configs
configs = session.get(url="%s/scan_configs" % (IP360BASEURL), auth=(IP360USERNAME, IP360PASS))
configs.connection.close()
```

And that's it - let's leave it for today - I'll be back with more soon!
