---
title: "Bookmarklet's to speed up your Tripwire Enterprise searches"
tags: 
  - "javascript"
  - "te"
  - "tripwire-enterprise"
draft: true
---

Need to find a node quickly? Maybe just double check if an IP exists but want to save a few clicks (Nodes > Node Search)? Well, how about using bookmarklets? They take seconds to setup (and leverage the Link In Context (aka Saved Search URLs) so are a great way to demo to clients how useful a saved search can be)… here's how:

# Setup

1. Right click on the Bookmark bar and chose "New Bookmark"

3. Enter the name you want for the Bookmarklet and copy and paste the text from the below options for either Search By IP or Search By Name:

- Search by IP:

```
javascript:mylocation=window.location.hostname,console.log(mylocation),myip=prompt('Hostname to search for',10),location.href=('https://'+mylocation+'/console/lic.search.cmd?lic=true&managerId=nodeManager&pageId=nodeManager.nodeFinderPage&searchCriteria='+(encodeURIComponent('%7B"search.serverNode.remoteHost.op"%3A3%2C"search.serverNode.remoteHost"%3A"')+myip+(encodeURIComponent('"%2C"search.node.severityRange.maxValue"%3A"10000"%2C"selectedSearchType"%3A"node"%2C"criteria.searchExecuted"%3Atrue%2C"search.node.severityRange.minValue"%3A"0"%7D'))))
```

- Search by name:

```
javascript:mylocation=window.location.hostname,console.log(mylocation),myhost=prompt('Hostname to search for','TE'),location.href=('https://'+mylocation+'/console/lic.search.cmd?lic=true&managerId=nodeManager&pageId=nodeManager.nodeFinderPage&searchCriteria='+(encodeURIComponent('%7B"search.node.name"%3A"')+myhost+(encodeURIComponent('"%2C"search.node.severityRange.maxValue"%3A"10000"%2C"selectedSearchType"%3A"node"%2C"search.node.name.op"%3A3%2C"criteria.searchExecuted"%3Atrue%2C"search.node.severityRange.minValue"%3A"0"%7D'))))
```

# Using it

Ensure you are logged in to Tripwire Enterprise with a window open on the Tripwire Enterprise console webpage! When you click on the bookmarket it will prompt you for a IP/name to search for and then return you to a node search page with the results

![Image](images/a39a99e2-d639-4784-a1d3-98cd18369347)
