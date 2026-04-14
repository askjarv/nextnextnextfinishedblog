---
title: "Windows 7 failing to boot after SP1 install - fatal error code c0000034"
date: 2011-03-30
categories: 
  - "windows"
tags: 
  - "sp1"
  - "windows-7"
---

Windows 7 failing to boot after SP1 install - fatal error code c0000034 INSTRUCTIONS:

01\. Reboot your computer while it's starting up.

02\. When your computer starts up again, choose the option "Launch Startup Repair"  --> PIC: http://notebooks.com/wp-content/uploads/2011/01/Recov-1.jpg

03\. When the Startup repair starts, click cancel.

04\. After you click cancel it will show a box. Click "Don't Send"  --> PIC: http://i52.tinypic.com/xgjriw.png

05\. Click the link "View advanced options for recovery and support"

06\. In the new window click Command Prompt at the bottom.--> PIC: http://i51.tinypic.com/50imu8.png

07\. In Command Prompt type this and press enter: %windir%\\system32\\notepad.exe

08\. Notepad will open. In notepad go to File-->Open.

09\. Change the type of files notepad views from .txt to All Files (see pic)--> PIC: http://i51.tinypic.com/35nd74z.png

10\. Now in Notepad, go to C:\\Windows\\winsxs\\ (or whichever drive Windows is installed on)

11\. In that folder, find pending.xml and make a copy of it

12\. Now open the original pending.xml (it will load really slow because the file is huge)

13\. Press CNTRL+F and search for the following exactly: 0000000000000000.cdf-ms

14\. Delete the following text (yours will be a little different):<Checkpoint/><DeleteFile path="\\SystemRoot\\WinSxS\\FileMaps\\\_0000000000000000.cdf-ms"/><MoveFile source="\\SystemRoot\\WinSxS\\Temp\\PendingRenames\\e56db1db48d4cb0199440000b01de419.\_0000000000000000.cdf-ms" destination="\\SystemRoot\\WinSxS\\FileMaps\\\_0000000000000000.cdf-ms"/>

\--> PIC: http://i54.tinypic.com/adzpzp.png

Your PC might not have all 3 sections of code (<Checkpoint>, <DeleteFile>, <MoveFile>). Just make sure you delete section "Checkpoint" and whatever other sections have "000000000000000.cdf-ms". They will be right next to eachother.

15\. Save the file, close notepad, close command prompt, restart your computer.

Once your computer starts up, do a normal startup (it may stall for 5-10 minutes at the "starting windows" screen, but leave it going) and the Service Pack will install some more stuff and restart a few times and then everything should be working! For some people, it reverts everything and cancels the service pack installation. For other people, the service pack installation completes. Either result is better than not starting at all!
