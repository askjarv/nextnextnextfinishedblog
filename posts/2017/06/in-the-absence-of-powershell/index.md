---
title: "In the absence of Powershell..."
date: 2017-06-28
---

Every so often I come across some older machines that I need to script and forget how much I take for granted the power (sorry) of powershell. Here's a useful command for when you next run into Windows Server 2003 and want nicely formatted disk information (yes, it's still around, along with XP, 2000 and, good heavens, NT too):

Get Disk Space (C drive)

```
WMIC LOGICALDISK GET Name,Size,FreeSpace | find /i "C:"
```

or just

```
WMIC LOGICALDISK GET Name,Size,FreeSpace
```

for all drives.
