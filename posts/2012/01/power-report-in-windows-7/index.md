---
title: "Power Report in Windows 7"
date: 2012-01-05
---

Microsoft has a lovely set of commands available from the command line to do with power- no the place you'd often look for power options. One of my new favourites is

PowerCfg -energy

Which generates a really rather nice HTML report with suggestions on how to optimise your power usage on your machine!

Note to the wise: this needs to be ran from an elevated command prompt- I'd also recommend that you run it from a half decent path, like your desktop, rather than the default, system32, as the resulting file is generated locally unless your specific it with the _\-output "C:\\pathhere_ parameter!
