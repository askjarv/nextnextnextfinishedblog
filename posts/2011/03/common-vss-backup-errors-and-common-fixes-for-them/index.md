---
title: "Common VSS backup errors and common fixes for them"
date: 2011-03-03
categories: 
  - "backup-exec"
tags: 
  - "vss"
---

Useful for VSS issues:

Suggestion 1: Install VSS rollup update

\------------------------------------------------

940349 Availability of a Volume Shadow Copy Service (VSS) update rollup

package for Windows Server 2003 to resolve some VSS snapshot issues

[http://support.microsoft.com/default.aspx?scid=kb;EN-US;940349](http://support.microsoft.com/default.aspx?scid=kb;EN-US;940349)

Suggestion 2: Configure MinDiffAreaFileSize registry key

\----------------------------------------------------------------------

This problem may occur when the shadow copy storage area is used up. Please

ensure that you have installed the latest SBS updates; in addition, please

perform the following steps to configure higher MinDiffAreaFileSize

registry value.

a. Click Start -> Run, type "regedit" in the text box, and press Enter.

b. Locate the following registry key:

HKEY\_LOCAL\_MACHINE\\SYSTEM\\CurrentControlSet\\Services\\VolSnap

c. On the Edit menu, pointed to New, and then clicked DWORD value.

d. Typed MinDiffAreaFileSize , and then pressed ENTER.

e. On the Edit menu, clicked Modify.

f. Changed the size to 3000 (decimal), and then click OK.

g. Reboot the server to test this issue again.

For more information, please refer to the following Microsoft Knowledge

Base article:

826936 Time-out errors occur in Volume Shadow Copy service writers, and

shadow copies are lost during backup and during times when there are high

levels of input/output

[http://support.microsoft.com/default.aspx?scid=kb;EN-US;826936](http://support.microsoft.com/default.aspx?scid=kb;EN-US;826936)

Suggestion 3: Reset VSS configuration

\-------------------------------------------------

If this problem continues, please perform the following steps to reset VSS

configuration:

1\. Go into control panel and reset the com configuration.

a. In control panel click "add remove programs".

b. Click "Add remove windows components".

c. Click the "Next" button (windows will re-initialize the COM

configuration).

2\. Look in "Component Services" MMC and make sure that the MS Shadow Copy

Provider does not show up as a COM+ application. The software provider

should NOT show up in Component Services on Windows 2003 and above. If it

is, you will have trouble initializing the VSS coordinator and provider

instances.

a. In the Component Services MMC, navigate to "Component Services\\My

Computer\\COM+ Applications\\"

b. View the properties of the "MS Software Shadow Copy Provider" if it

exists. In the "advanced" tab, uncheck the "Disable deletion" checkbox and

then delete the "MS Software Shadow Copy Provider" from COM+ Applications.

3\. Run FIXVSS03.BAT to reset VSS configuration.

rem FILENAME: FIXVSS03.BAT

rem

net stop "System Event Notification"

net stop "COM+ Event System"

net stop "Microsoft Software Shadow Copy Provider "

net stop "Volume Shadow Copy"

cd /d %windir%\\system32

net stop vss

net stop swprv

regsvr32 /s ole32.dll

regsvr32 /s oleaut32.dll

regsvr32 /s vss\_ps.dll

vssvc /register

regsvr32 /s /i swprv.dll

regsvr32 /s /i eventcls.dll

regsvr32 /s es.dll

regsvr32 /s stdprov.dll

regsvr32 /s vssui.dll

regsvr32 /s msxml.dll

regsvr32 /s msxml3.dll

regsvr32 /s msxml4.dll

Cd /d %systemroot%\\syswow64

regsvr32 /s ole32.dll

regsvr32 /s vss\_ps.dll

regsvr32 /s es.dll

regsvr32 /s stdprov.dll

regsvr32 /s msxml3.dll

regsvr32 /s msxml.dll

regsvr32 /s msxml4.dll

net start "COM+ Event System"

4\. Disable VSS tracing if it is enabled.

887013 How to enable the Volume Shadow Copy service's debug tracing

features in Microsoft Windows Server 2003

[http://support.microsoft.com/default.aspx?scid=kb;EN-US;887013](http://support.microsoft.com/default.aspx?scid=kb;EN-US;887013)

5\. Reboot the system to bring all writers into a stable state.

How to enable the Volume Shadow Copy service's debug tracing features in

Microsoft Windows Server 2003

[http://support.microsoft.com/kb/887013](http://support.microsoft.com/kb/887013)
