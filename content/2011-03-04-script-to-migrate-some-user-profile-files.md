---
title: "Script to migrate some user profile files"
date: 2011-03-04
categories: 
  - "scripts"
tags: 
  - "citrix"
  - "profiles"
  - "terminal-services"
---

I’ve knocked together a quick script that copies

· Signatures

· Favourites

· Desktop Items

From old Citrix Profile to new Citrix Profile

You still need to select the signature in Outlook, but at least the files are all there to choose from:

@echo off

IF EXIST "\\\\bluechip.local\\TSProfilesNew$\\%username%\\NTUSER.DAT" SET OLDPROFILE=\\\\bluechip.local\\TSProfilesNew$\\%username%  
IF EXIST "\\\\bluechip.local\\TSProfilesNew$\\%username%.BLUECHIP\\NTUSER.DAT" SET OLDPROFILE=\\\\bluechip.local\\TSProfilesNew$\\%username%.BLUECHIP

IF NOT DEFINED OLDPROFILE GOTO THE\_END

ECHO.  
ECHO. Old Profile Detected As  
ECHO. %OLDPROFILE%  
ECHO.

XCOPY /D /E /C /Y "%OLDPROFILE%\\Application Data\\Microsoft\\Signatures" "%USERPROFILE%\\AppData\\Roaming\\Microsoft\\Signatures"

XCOPY /D /E /C /Y "%OLDPROFILE%\\Desktop" "%USERPROFILE%\\Desktop"

XCOPY /D /E /C /Y "%OLDPROFILE%\\Favorites" "%USERPROFILE%\\Favorites"

:The\_End
