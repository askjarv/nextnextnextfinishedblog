---
title: "TAPI &ldquo;Call Contact&rdquo; in Outlook on Windows 7 with Lync Installed"
date: 2011-03-03
categories: 
  - "microsoft-office"
tags: 
  - "lync"
  - "office-2010"
  - "tapi"
---

When I installed Lync on my Windows 7 Laptop the Tapi dialing feature didn’t work anymore.  
After some research I found a [forum presenting the Solution](http://tek-tips.com/viewthread.cfm?qid=1619910&page=25) - as so often it is only a question of adding a registry Key:

HKEY\_LOCAL\_MACHINE\\SOFTWARE\\Microsoft\\Office\\Outlook\\Call Integration needs a DWORD called TAPIOVERRIDE with Value = 1

\[HKEY\_LOCAL\_MACHINE\\SOFTWARE\\Microsoft\\Office\\Outlook\\Call Integration\]  
"TAPIOVERRIDE"=dword:00000001

And off you go – after a short restart you can again Dial via TAPI from Outlook 2010!

[![clip\_image002](images/clip_image002.gif "clip_image002")](http://blog.lieberlieber.com/wp-content/uploads/image86.png)
