---
date: 2011-03-03
tags: 
  - "alerts"
  - "snmp"
  - "vmware"
---

I’ve seen this a few times now, where SNMP traps are being sent from vCenter even though there is no matching alarm on the management console. I haven’t managed to identify the main cause but find restarting the “VMware ESX Management services” on the relevant ESX host and the “VMware VirtualCenter Server” service appear to resolve the problem.

![](images/2.jpg "Services")

\[root@esx01 init.d\]# **service mgmt-vmware restart**

Stopping VMware ESX Management services:

VMware ESX Host Agent Watchdog \[ OK \]

VMware ESX Host Agent \[ OK \]

Starting VMware ESX Management services:

VMware ESX Host Agent (background) \[ OK \]

Availability report startup (background) \[ OK \]

\[root@esx01 init.d\]# **service vmware-vpxa restart**

Stopping vmware-vpxa: \[ OK \]

Starting vmware-vpxa: \[ OK \]

\[root@esx01 init.d\]#

 

![](images/3.jpg "VMware SNMP")

 

 

Additionally, if you acknowledge any alarms in vCenter it will stop sending the SNMP traps until a new condition is met. Therefore, be sure that you want to do this!
