---
title: "Rebuild performance counters"
date: 2011-03-03
tags: 
  - "windows"
---

This was a new one on me as it isn’t an issue I’ve seen before, but I just stumbled across a server with a set of corrupt Windows performance counters – All counters were listed as random integer values (i.e. 10965) instead of their normal descriptive names (i.e. % Processor Time), which obviously makes them worse than useless and gets my VIM senses tingling. Or something.

Thankfully, the fix for this issue is a piece of cake, and involves a single line at the command prompt:

**lodctr /r C:\\Windows\\System32\\PerfStringBackup.ini**

(For x64-based systems, this would be **lodctr /r C:\\Windows\\SysWOW64\\PerfStringBackup.ini** instead by the way)

This usually takes a few minutes to process, but restores all performance counter data from a working backup and should solve the issue.
