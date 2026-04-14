---
title: "Missing ICA Session Performance Counters on XenApp 6 / High CPU usage from VMware Tools Service"
date: 2011-03-03
tags: 
  - "citrix"
  - "perfomance-counters"
  - "vmware"
  - "xenapp"
---

We've seen instances of high CPU utilisation from the "VMware Tools Service" on our 4 XenApp 6 whereby over time the CPU usage will grow after a reboot- as such this can typically be resolved temporarily by a reboot. The longer term fix appears to revolve around rebuilding the performance counters for XenApp- something Citrix has identifed here:

[http://support.citrix.com/article/CTX127151](http://support.citrix.com/article/CTX127151)

On a XenApp 6 Server, after applying a XenApp 6 hotfix, the Performance Counter for _ICA Session_ is removed. This can have an adverse effect on the operation of tools and processes which rely on these performance counters, such as HDX Experience Monitor for XenApp (CTX126491 - [HDX Experience Monitor for XenApp](http://support.citrix.com/article/CTX126491)) and EdgeSight System Monitoring tools.

Resolution: Apply the Limited Release Hotfix XA600W2K8R2X64023, CTX127269 – [LIMITED RELEASE - Hotfix XA600W2K8R2X64023 - For Citrix XenApp 6.0 for Windows Server 2008 R2 - English](http://support.citrix.com/article/CTX127269) to resolve the issue. Although the recommended fix is to apply the above mentioned hotfix, the following steps may be followed to manually resolve the issue each time another hotfix is installed of applying the above hotfix:

- Reregister the ICA Session Performance Counters by running the following command on the XenApp server effected: **regsvr32 c:\\windows\\system32\\icaperf.dll** 
    
    This command reregisters the performance counters in question.

- Before installing a hotfix, back up the registry hive **HKLM\\System\\CurrentControlSet\\Services\\CitrixICA** and restore it once the hotfix has been applied.
