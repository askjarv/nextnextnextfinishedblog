---
title: "using windows scheduler to run powershell scripts"
date: 2011-03-03
categories: 
  - "powershell"
tags: 
  - "windows"
---

Allow scripts to run by running

`set-executionpolicy RemoteSigned`

from the powershell first

Create your script (C:\\myscript.ps1)

Create a batch file with

`powershell -command "& 'C:\MyScript.ps1' "`

Add to scheduled tasks!
