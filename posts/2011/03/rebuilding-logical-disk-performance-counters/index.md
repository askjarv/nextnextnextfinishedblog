---
title: "Rebuilding logical disk performance counters"
date: 2011-03-30
tags: 
  - "monitoring"
  - "performance-counters"
  - "windows"
---

Guys,

If you ever need to monitor logical disk performance counters (for free space as a percentage, in Megabytes and so on) and find that those counters and those counters alone either aren’t working or simply aren’t present, then you might want to bear in mind the following possible fixes:

- At a command prompt, typing **diskperf –yv** will activate logical disk monitoring if it isn’t already enabled – this is turned on by default under Windows 2003 and 2008 Server, but is _disabled_ by default in Windows 2000. Running this command will also confirm the current state of logical counter activation anyway, but if you are enabling counters with this command then you’ll need a reboot afterwards for the change to take place.
- If logical disk counters still don’t appear in PerfMon, then check the following Registry location: **HKEY\_LOCAL\_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\PerfDisk\\Performance** – if there is a key within this folder named **DisablePerformanceCounters**, ensure that it is set to **0** to enable logical disk counters.
- If logical disk counters appear in PerfMon but not via WMI (you can see what performance counters are available over WMI by using the **perfmon /wmi** switch), then you can reinstate these counters with the following simple command: **wmiadap /f** – this parses and refreshes all WMI performance counter classes on the system.

One or a combination of these commands should fix your problem – if not, you’re probably looking at a complete rebuild of WMI most likely. Happy monitoring!
