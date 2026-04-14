---
title: "VBS Script to detect OS version"
date: 2011-03-04
categories: 
  - "scripts"
tags: 
  - "os"
  - "vbs"
  - "x64"
  - "x86"
---

Here is a nice little script that may help you out in the future for any reason, mine was Trend.

I have recently installed Trend and have created a Remote Deployment package that comes in either x64 or x86 variety. In order to save time for anyone deploying the software I have created a script to go with it that detects what version of OS you are running and then runs the correct installer.

Copy the below to a new notepad file and save as .vbs in the same folder as the x64 and x86 installation packages. Change the filenames to whatever you like between the “” after objShell.Run.

Set objShell = CreateObject("WScript.Shell")

osType = objShell.ExpandEnvironmentStrings("%PROCESSOR\_ARCHITECTURE%")

If osType = "x86" Then

           objShell.Run "deployclientx86.msi"

ElseIf osType = "AMD64" Then

           objShell.Run "deployclientx64.msi"

Else

           '\*shrug\*

End If

Simple but effective… Hope this helps.

Wes
