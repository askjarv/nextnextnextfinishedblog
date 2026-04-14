---
title: "Installing drivers for 32 bit clients on 64 bit servers."
date: 2011-03-04
categories: 
  - "windows"
tags: 
  - "drivers"
  - "printers"
  - "servers"
  - "windows-2008"
  - "x64"
  - "x86"
---

Installing drivers for 32 bit clients on 64 bit servers.

\- Install the Printer as normal with the x64 driver

\- Go into Printer Properties

\- Sharing Tab

\- Additional Drivers

\- Check x86 and click OK

\- Find driver… at this point choose options A or B

A) Find a driver with a driver name that EXACTLY matches the x64 driver version

B) Edit an x86 driver ini file so that the driver name EXACTLY matches the x64 driver version

In this case we had to edit the driver name so that it read \*\*\* PCL6 rather than \*\*\* PCL 6 (removed the space).
