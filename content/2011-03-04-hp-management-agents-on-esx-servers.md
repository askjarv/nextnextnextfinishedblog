---
title: "HP Management Agents on ESX servers"
date: 2011-03-04
tags: 
  - "esx"
  - "hardware"
  - "hp"
  - "snmp"
  - "vmware"
---

Hello All,

I have been advised that installing the HP Management Agents on an ESX server will install an element called the CMAFCAD(Compaq Management Agent Fibre Channel Adaptor Daemon) which is only actually intended for use with the following adaptors:

HP StorageWorks Modular Smart Array (MSA) 1000

HP StorageWorks Modular Smart Array (MSA) 1500

HP StorageWorks Modular Smart Array (MSA) 2000

The result is a flooded log file, memory issues and problems accessing storage. The walkthrough to disable this element is here:

[http://h20000.www2.hp.com/bizsupport/TechSupport/Document.jsp?lang=en&cc=us&objectID=c01519875&jumpid=reg\_R1002\_USEN](http://h20000.www2.hp.com/bizsupport/TechSupport/Document.jsp?lang=en&cc=us&objectID=c01519875&jumpid=reg_R1002_USEN)

Interestingly this is out of date. Where it references “/opt/compaq/cma.conf” it may mean “/opt/hp/hp-snmp-agents/cma.conf” and when it asks you to stop and start the services the command is "service hp-snmp-agents stop/start" not “service hpasm stop/start”.

It is important to stop the services before editing the file because if you do not then the restart command will exclude the element you want to stop and you will be forced to reboot or stop the process manually.

To stop the process manually you can identify the PID with “ps –auxwww | grep cmafcad” and then perform a kill -9 on the returned PID for instance:

[![clip\_image002](images/clip_image002_thumb5.jpg "clip_image002")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0027.jpg)

In the above example the PS command returned 2 PIDs, ignore the one which is the GREP command itself, in this case the correct process was 4114.
