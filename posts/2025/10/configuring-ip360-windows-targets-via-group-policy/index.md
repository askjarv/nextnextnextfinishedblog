---
title: "Configuring IP360 Windows targets via group policy"
date: 2025-10-14
categories: 
  - "ip360"
tags: 
  - "tripwire"
---

Group Policy is the typical/preferred method of setting many of the requirements for Tripwire IP360 vulnerability scanning and whilst the official endpoint guide is helpful with identifying various settings, it can take time to map many of the settings to the specific GPO setting... and unfortunately not all of the settings required can be set by group policy without a bit of effort (as the settings aren't exposed as objects that can be configured). To help alleviate this issue, this page includes attachments of:

- an export of an example group policy

- an example vbs script (that can be ran via Group policy!)

that will enable a Windows device to be scanned by IP360 - I hope you find it useful!
