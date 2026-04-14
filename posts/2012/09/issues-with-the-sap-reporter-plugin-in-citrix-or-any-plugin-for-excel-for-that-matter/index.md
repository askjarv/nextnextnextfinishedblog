---
title: "Issues with the SAP Reporter Plugin in Citrix (or any plugin for Excel for that matter)?"
date: 2012-09-09
---

Here's a super quick fix for something that was working for admin/the installer, but not any of the other users who are logged in to Citrix -

Create a new group policy object (called Citrix SAP Reporter Policy or similar) and apply it to the XenApp 6.5 server OU to run a user login script – the script (and associated registry file) is below:

**Regimport.bat**

REG QUERY HKEY\_CURRENT\_USER\\Software\\Microsoft\\Office\\Excel\\Addins\\IXXLReporter.AddIn /v FriendlyName

IF %errorlevel%==0 GOTO skip\_reg\_inport

regedit.exe /s \\\\domain.local\\SysVol\\domain.local\\Policies\\{SCRIPTY-BIT}\\User\\Scripts\\Logon\\setupcitrixreporter.reg

:skip\_reg\_inport

**Registry File:**

Windows Registry Editor Version 5.00

\[HKEY\_CURRENT\_USER\\Software\\Microsoft\\Office\\Excel\\Addins\\IXXLReporter.AddIn\]

"FriendlyName"="SAP Business One XL Reporter"

"Description"="SAP Business One XL Reporter COM Add-in for Excel"

"LoadBehavior"=dword:00000003

"CommandLineSafe"=dword:00000000
