---
title: "How to list all ports that are listening for TCP/UDP traffic"
date: 2011-03-03
categories: 
  - "network"
tags: 
  - "cli"
  - "windows"
---

From the command line it's possible list all ports that are listening for TCP/UDP traffic with the command:

netstat -ano

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

You can use | (pipe) to filter your results to make things easier - for example to find the service using port 80:

netstat -ano | findstr 80
