---
title: "Fortigate Dual Ping Peer gateways"
date: 2011-03-30
categories: 
  - "fortigate"
tags: 
  - "gateway"
  - "ping"
  - "pingpeer"
---

Following some successful testing I have determined that adding two ping servers, reduces the amount of false positives for the Fortigate alert, PING PEER down

The below commands can be used to update the device.　 The catch being that this only can be set and seen at CLI level.

config system interface

edit WAN1

set gwdetect enable

set detectserver 8.8.8.8 208.67.222.222 next edit WAN2

set gwdetect enable

set detectserver 8.8.8.8 208.67.222.222 next

end
