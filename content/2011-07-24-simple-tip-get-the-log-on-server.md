---
title: "Simple tip- get the log on server"
date: 2011-07-24
---

Trying to troubleshot a group policy replication issue but not sure where to start? Seeing weird behaviour on some clients, but unable to pin point which server is causing the problem? Just need to verify which DC you connected to on logon? You can get this from the (under-rated IMHO) command, SET. Set brings back a whole bunch of information.

Unforunately, there's a downside to that- too much information to quickly see what you're looking for- it's just one line- LOGONSERVER that you're looking for- so use our friend "findstr" to filter straight down to what you want:

set | findstr "LOGONSERVER"

gives you the bit you want - in a quick and easy way!
