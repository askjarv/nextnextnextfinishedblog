---
title: "Determine Memory DIMM usage on ESX host without agents"
date: 2011-03-04
tags: 
  - "esx"
  - "hardware"
  - "vmware"
---

This “occasionally” pops up as a request, the following worked for me:

[http://kb.vmware.com/kb/1002404](http://kb.vmware.com/kb/1002404)

specifically:

1\. putty to ESX host

2\. login

3\. type “_su –_“ to elevate your status

4\. type “_dmidecode | less_” and keep pressing space until the info is on screen

It’s worth configuring capture on putty to make this easier, simply enable logging and type “_dmidecode_” then retrieve the data from the log file.
