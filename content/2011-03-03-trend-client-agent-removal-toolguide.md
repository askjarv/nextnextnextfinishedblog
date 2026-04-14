---
title: "Trend Client Agent Removal Tool/Guide"
date: 2011-03-03
categories: 
  - "trend"
tags: 
  - "uninstall"
---

Unsure if this is old news but the Trend agent can be a real pain to get off some client machines when an upgrade fails. There are guides to removing it manually on both XP and Vista but it is rather time consuming and doesn’t always work. Trend has provided an automatic removal tool that worked instead. It may be best to use this tool first which saves a lot of time and effort. Regardless here are the manual uninstall guides:

XP: [http://esupport.trendmicro.com/7/Manually-removing-the-ClientServer-Security-Agent.aspx](http://esupport.trendmicro.com/7/Manually-removing-the-ClientServer-Security-Agent.aspx)

Vista/Win7: [http://esupport.trendmicro.com/3/Manually-uninstalling-the-ClientServer-Security-Agent-from-a-computer.aspx](http://esupport.trendmicro.com/3/Manually-uninstalling-the-ClientServer-Security-Agent-from-a-computer.aspx)

**OR** use the tool I've popped up here: http://www.mediafire.com/?tp17w7afzchugd4 . Just run the Uninstall.bat and type ‘Y’ when asked to reboot.

README BELOW:

\----------------------------------------------------------------------------------------------------------

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

\*\*\* Security Agent Removal Toolset 1.0 \*\*\*

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

Purpose:

Remove or Stop Security Agents to facilitate WFBS 7 debugging.

Supported client:

WFBS Client/Server Security Agent 5.0

WFBS Client/Server Security Agent 5.1

WFBS Client/Server Security Agent 6.0

WFBS Security Agent 7.0

How to Use:

To remove client:

1\. Log on to Windows as Administrator or any account with Administrators

privilege.

2\. On Windows Vista/7/2008, right click on "Unisntall.bat" and select "Run

As Administrator". Agree to the UAC dialog that appears.

On Windows XP/2003, just double click "Uninstall.bat".

3\. Wait a few minutes until this message appear:

\--------------------------------------------------------

Do you want to reboot now? (Y/N)

Type "N\[Enter\]" if you do not want to reboot right now. Some drivers will

not be removed until reboot.

Type "Y\[Enter\]", the computer will start to count down 30 seconds. After the

count down ends, The computer will restart.

\*Note\*: The remove client tool will stop client automatically. You don't

need to run "Stop.bat" before running "Unisntall.bat".

To stop running client:

1\. Log on to Windows as Administrator or any account with Administrators

privilege.

2\. On Windows Vista/7/2008, right click on "Stop.bat" and select "Run

As Administrator". Agree to the UAC dialog that appears.

On Windows XP/2003, just double click "Stop.bat".

3\. The program ends after the client is stopped.

Known Issues:

1\. Some directories in AMSP directory can not be cleaned:

C:\\Program Files\\Trend Micro\\AMSP\\temp\\TMFBE

Manual editing of the direcotry's security property is required to remove

the directory. The directory does not block re-installation of WFBS

Security Agent 7.0.

2\. If certain applications are running, some files could not be removed. The

application may cause this include:

\* Internet Explorer

\* Firefox

\* Windows Live Mail

\* Windows Mail

\* Outlook

\* Outlook Express

Please either close these applications before remove client ro remove

remaining files after reboot.
