---
title: "How to troubleshoot an IIS &quot;Event ID: 1009&quot; error."
date: 2011-03-04
categories: 
  - "iis"
tags: 
  - "error"
---

**How to troubleshoot an IIS "Event ID: 1009" error.**

An error that most IIS 6.0 administrators have probably encountered is "Event ID: 1009" which usually leads to a "503 Service Unavailable" error being displayed in a browser. "503" usually indicates the Application Pool has been disabled for some reason. The IIS support team frequently gets support calls to help resolve this issue and over the years I have compiled a list of steps I use to troubleshoot this. If the following information seems too confusing please let me know and I'll clarify any confusing points. The follow list is broken down into different sections for the various "exit codes" that are in the Event 1009.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

\*\*\* Problem Description \*\*\*  
Many times when an IIS6 application pool terminates the following will be logged.

  1. The Name of the App Pool  
  2. The PID  
  3. The exit code.  
The **_exit code_** is the most useful part of the event entry.

  Event Type: Warning  
  Event Source: W3SVC  
  Event Category: None  
  Event ID: 1009  
  Date:  1/29/2004  
  Time:  10:01:14 AM  
  User:  N/A  
  Computer: COMPUTERNAME  
  Description:  
  A process serving application pool 'DefaultAppPool' terminated unexpectedly. The  
process id was '3908'. The process exit code was '0x80'.

<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

\*\*\* Resolution \*\*\*

Constants:

// the WAS killed the worker process  
#define KILLED\_WORKER\_PROCESS\_EXIT\_CODE 0xFFFFFFFD

// the worker process exited ok  
#define CLEAN\_WORKER\_PROCESS\_EXIT\_CODE  0xFFFFFFFE

// the worker process exited due to a fatal error  
#define ERROR\_WORKER\_PROCESS\_EXIT\_CODE  0xFFFFFFFF

\----------------------------------------------------------- 
Concepts that apply to exit codes of both 0x80 and 0xffffffff  
  · Make sure "Network Service" and "IWAM\_MACHINE" are members of IIS\_WPG  
  · If a custom identity is being used for the app pool ensure it is in IIS\_WPG  
  · Make sure that IIS\_WPG is included somehow in these User Rights assignments  
(example: Everyone group includes IIS\_WPG so that is sufficient)  
      a. Access this computer from network  
      b. Log on as batch job  
      c. Bypass traverse checking  
  · Ensure that IIS\_WPG or members of that group are not in any of the  
corresponding "Deny" User Rights  
  · Ensure that "NT AUTHORITY\\Authenticated Users" and "NT AUTHORITY\\Interactive"  
are part of the "Users" group.  
  · Use FileMon.exe and RegMon.exe to identify ACC DENIED's.  
  · If customer has more than ~60 app pools with unique identities, set the  
following key:  
      HKLM\\System\\CurrentControlSet\\Services\\W3SVC\\Parameters\\UseSharedWPDesktop  
(REG\_DWORD with value of 1)  
\----------------------------------------------------------- 
The process exit code was '0x80'.  
  In certain cases when w3wp.exe goes away IIS will attempt to determine the exit code by calling the "GetExitCodeProcess" API.  
  If the reason cannot be determined by this API then the code returned is 0x80. 
  "0x80" means "ERROR\_WAIT\_NO\_CHILDREN" which means "There are no child processes to wait for"

  This _typically_ means the W3WP.exe never started at all which could be User-Rights related or  
NTFS permissions.  
  If it is NTFS permissions, that means the AppPool identity doesn't have read  
permission to the w3wp.exe file and/or supporting DLLs  
  - Use FileMon to troubleshoot  
  If it is User Rights related then the AppPool identity failed to logon.  
  - Check the 3 User Rights listed above.  
\----------------------------------------------------------- 
The process exit code was '0xffffffff'.  
  Means the W3WP.exe process partially started but could not load a dependancy for  
some reason.  
  This is either permissions/security related or due to mismatched DLL's.  
  Try running the AppPool as "Local System"  
  - If this works it is a permissions problem for the AppPool Identity. Check the  
following "Scenarios" section then follow the "concepts" section above  
  - If this fails using System it is a mismatch or missing DLL problem. Check  
scenario #1 below then follow the "Loader Snaps" section

Scenarios for 0xffffffff

  1. The first thing that should be checked is whether a Windows Service pack is installed  
    - If it is, verify that "c:\\windows\\System32\\instsrv\\w3core.dll" is either the  
RTM version or SP1 version.  
    - If it is the RTM version then reapplying the service pack should fix the problem.

  2. Is this IIS server a DC and have you reinstalled IIS on another DC?  
    I have had two cases where there was a permissions failure reading nodes in the  
metabase  
    When installing IIS it creates an IIS\_WPG group with a somewhat random SID.  
    Permissions in the metabase are then set using this unique version of  
IIS\_WPG.  
    When removing IIS on a DC it will delete the IIS\_WPG group, if Win2k3 SP1 is  
not installed, which is used by all the other DC's running IIS  
    When then adding IIS back on to this DC, a new IIS\_WPG group is created that  
has a new SID  
    The pre-existing permissions (older SID) in the other metabases will have  
"Unknown User" for the permissions and spawning W3WP.exe under anything other than  
SYSTEM will fail with 0xffffffff  
    - I found this by enabling Tracing then searching through source code.  
    - If you get a Debug Trace using DbgView.exe look for a line that says:  
        w3core!W3\_SERVER::Initialize \[\\w3server.cxx @ 526\]:Error reading  
UseDigestSSP property.  hr = 80070005  
    - However It would be easy enough to skip Debug Tracing and just look at the  
following nodes using Metabase Explorer.  
    - IIS\_WPG needs permissions to the following nodes:  
      1. MachineName - Read  
      2. w3svc/1/Filters (or any other filters node) - Read/Write  
      3. w3svc/AppPools - Special (Query Unsecure Property)

  3. Has the customer modified default DCOM security?  
    - We have run into an issue where the customer had modified  
the default Launch and Activation Permissions in Component Services.  
    - The customer removed Local Launch and Local Activation for the Everyone  
group.  
    - Here is the section of loader snaps output that is a hint of this scenario:

LDR: LdrGetProcedureAddress by NAME - CoMarshalInterface  
LDR: LdrGetProcedureAddress by NAME - CoUnmarshalInterface  
LDR: LdrGetProcedureAddress by NAME - CoReleaseMarshalData  
(15c8.914): Unknown exception - code 80070005 (first chance)  
LDR: UNINIT LIST  
          (1) \[iisres.dll\] c:\\windows\\system32\\inetsrv\\iisres.dll (0) deinit 0  
LDR: Unmapping \[iisres.dll\]  
LDR: Derefcount IISMAP.dll (0)

\----------------------------------------------------------- 
The process exit code was '0xc0000005'.  
  This is a crash.  
  Troubleshoot using a Debugger. (Debug Diagnostics)  
\----------------------------------------------------------- 
The process exit code was '0xff'.  
  Process shut down "gracefully" for some reason.  
  Troubleshoot as a crash and see who called TerminateProcess or ExitProcess.  
\----------------------------------------------------------- 
The process exit code was '0x0'.  
  This would be typical if you had w3wp.exe configured to launch under a debugger  
and you never did a "Go" in the debugger windows.  
  Launch gflags.exe and clear the debugger setting for w3wp.exe  
\----------------------------------------------------------- 
Loader Snaps Section - These steps are not for getting memory dumps. This explains  
how to easily get the reason that a module (DLL) failed to load which is one reason for a 0xffffffff.

  1. Send customer "gflags.exe" (can be obtained from Debugging Tools for  
Windows)  
  2. Double-click gflags.exe  
  3. Go to the "Image File" tab  
  4. Enter "w3wp.exe" for the image then press "tab"  
  5. Put a check in "Show loader snaps"  
  6. Put a check in "Debugger" and enter  
        "NTSD.exe -logo c:\\temp\\LDR.log -g -G -r 0" (<-- that is a zero)  
  7. Ensure the folder from the previous step has adequate read/write permissions  
for the Identity that is launching the AppPool.  
  8. Ensure that the AppPool is enabled  
  9. Reproduce the problem. - At this point w3wp.exe should spawn under NTSD.exe,  
write to the log, then shut down.  
  10. Have customer send the LoaderSnaps.log output found in the c:\\temp folder.  
  11. Search for the text of "exception" or "failed" (you'll probably find what you  
want near the end of the log)  
  12. Lookup the listed error number using err.exe or hrplus.exe. The DLL that it  
is having trouble on is the line just previous to the "exception/failed" line.  
  13. Take the logical steps to address whatever the error is describing.

  Notes - Don't forget to reverse these settings when done.  
            - If you identify a DLL that is the wrong version usually simply  
reapplying the relevant hotfix or service pack will resolve the issue.
