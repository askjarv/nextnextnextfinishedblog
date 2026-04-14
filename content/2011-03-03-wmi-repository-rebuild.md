---
title: "WMI repository rebuild"
date: 2011-03-03
categories: 
  - "windows"
tags: 
  - "wmi"
---

If you ever come across a Windows 200x Server system with a WMI repository that’s shot to pieces (with “Not found” or similar errors even when you try to connect to WMI Control locally) then here’s a simple but effective batch file that will delete and rebuild that repository for you quickly and easily:

net stop winmgmt

c:

cd %systemroot%\\system32\\wbem

rd /S /Q repository

regsvr32 /s %systemroot%\\system32\\scecli.dll

regsvr32 /s %systemroot%\\system32\\userenv.dll

mofcomp cimwin32.mof

mofcomp cimwin32.mfl

mofcomp rsop.mof

mofcomp rsop.mfl

for /f %%s in ('dir /b /s \*.dll') do regsvr32 /s %%s

for /f %%s in ('dir /b \*.mof') do mofcomp %%s

for /f %%s in ('dir /b \*.mfl') do mofcomp %%s

echo DONE reboot

pause

Theoretically, the server requires a reboot to complete this repository rebuild successfully, but under Windows 2008 at least that shouldn’t actually be required – Windows 2003 typically isn’t quite so forgiving though.
