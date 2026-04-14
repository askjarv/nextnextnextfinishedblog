---
title: "Load issues after upgrading ESX on Virtual XenApp6 Servers"
date: 2012-09-09
---

After doing an upgrade (from ESX4 to ESX 5) the first thing you ought to be thinking of is updating VMware tools- sure ICA/RDP should "handle" the desktop OK - but up-to-date VMware tools is beyond good practice/common sense- it's critical to ensure things "behave"- however, I've now seen a couple of instances whereby after doing the upgrade to 'tools the server will stay at 10000 load and not allow log ons- this seems to be fixed by:

1.       Uninstall VMware tools all together

2.       Reinstall VMware tools and deselect ‘Volume Shadow Copy Services Support’ (you cannot just remove this from the original install it must be uninstalled first)

3.       Open Performance monitor

4.       Close performance monitor

5.       Open a command prompt and type “lodctr.exe /r” (this rebuilds the performance counters that the VMware tools issue has corrupted)

6.       Restart the IMA

You should now see (after about a minute) the ‘qfarm /load’ status of your server return to normal.

Thanks to a colleague to pointing this one out to me!
