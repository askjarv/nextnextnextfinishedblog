---
title: "Citrix Receiver 3.1 does not Allow you to Add Non-Secure URL"
date: 2013-06-12
tags: 
  - "citrix"
  - "clients"
  - "receiver"
---

A very annoying one I come across quite often where the internal web interface is an insecure site can be resolved with a quick registry change (that said, there's no reason why you shouldn't just "re-apply" you SSL cert or securely publish you Citrix apps internally!):

Citrix Receiver 3.1 does not allow you to add a non-secure URL.

![](images/1CTX131857-1.gif)

**Cause**

The default configuration requires SSL for secure communication to your store.

**Resolution**

You can resolve this issue by modifying the client registry.

**Caution**! This procedure requires you to edit the registry. Using Registry Editor incorrectly can cause serious problems that might require you to reinstall your operating system. Citrix cannot guarantee that problems resulting from the incorrect use of Registry Editor can be solved. Use Registry Editor at your own risk. Back up the registry before you edit it.

Under HKEY\_LOCAL\_MACHINE\\SOFTWARE\\Citrix\\Dazzle

REG\_SZ: AllowAddStore

Value: A

**Note**: Changing the value to **A** allows you to add non-secure URLs.
