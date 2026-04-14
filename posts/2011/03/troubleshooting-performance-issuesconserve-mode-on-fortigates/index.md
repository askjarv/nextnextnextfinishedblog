---
title: "Troubleshooting Performance issues/conserve mode on FortiGates"
date: 2011-03-03
categories: 
  - "fortigate"
tags: 
  - "cli"
  - "conserve-mode"
  - "fortios"
  - "performance"
---

For those of you that don’t know you can use the ‘_get system performance top_ _<delay> <max\_lines>’_ command from the Fortigate CLI console to view the top running processes, and you can sort them by memory usage by pressing _‘m’_, in order to assess what is causing the high memory usage on the device.

_Note: This command was introduced from FortiOS firmware v4.0 MR2 and onwards._

For more information on how to use this command and how to assess the output please see page 109 on [http://docs.fortinet.com/fgt/handbook/fortigate-troubleshooting-40-mr2.pdf](http://docs.fortinet.com/fgt/handbook/fortigate-troubleshooting-40-mr2.pdf)

You can also use the commands:

Diag sys top

to show processes and

Diag sys kill 9 <PID> ?

to kill processes.
