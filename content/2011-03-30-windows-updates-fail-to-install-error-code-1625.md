---
title: "Windows Updates fail to install - Error code: 1625"
date: 2011-03-30
categories: 
  - "wsus"
tags: 
  - "patch"
---

If you get caught out by the (vague) error of "Windows Updates fail to install - Error code: 1625", after much searching I found this solution worked in most scenarios:

**

start > run regedit

**

Browse the registry to **HKLM\\Software\\Policies\\Microsoft\\Windows\\Installer**

**Create: DisableMSI**

Type: REG\_DWORD 　value = 0 　 (0 should allow you to install it was originally 1)

(In my case the value had been set to 2 so I changed it to 0)
