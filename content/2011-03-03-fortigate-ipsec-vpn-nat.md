---
title: "FortiGate IPSec VPN NAT"
date: 2011-03-03
categories: 
  - "fortigate"
tags: 
  - "fortinet"
  - "ipsec-vpn"
---

This may be useful when dealing with IPSec VPN between two customers, basically allows you to NAT your source address to one provided by the remote LAN administrator.

**Tunnel Mode**

config vpn ipsec phase2

edit <phase2>

set use-natip disable

end

config firewall policy

edit <ipsec policy>

set natip <ip> <subnet>

end

**Interface Mode**

Create IP pool <ip> <subnet> Interface = internal

On specific policy…

Enable NAT

Select the IP pool created
