---
title: "Windows Installer verbose log analyser (WILOGUTL.EXE)"
date: 2011-03-03
tags: 
  - "install"
  - "log"
  - "tools"
  - "windows"
---

The Windows Installer Software Development Kit (SDK) contains a utility called WiLogUtl.exe, or the Windows Installer Verbose Log Analyzer. This utility finds any errors in the log file and gives some other information (which is probably only useful to someone experienced with MSI packages).

The utility also contains three HTML help files that give more information on certain error codes that occur. The utility is contained in the [Microsoft Windows Platform SDK](http://www.microsoft.com/downloads/details.aspx?FamilyId=A55B6B43-E24F-4EA3-A93E-40C0EC4F68E5&displaylang=en).

When the utility starts, an initial screen appears:

[![clip\_image001](images/clip_image001_thumb.gif "clip_image001")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0011.gif)

Here you can see that we have browsed to an MSI install log, and that the utility shows us the first several lines. Clicking the **Analyze** button gives you more detailed look at the file:

[![clip\_image002](images/clip_image002_thumb.gif "clip_image002")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0021.gif)

The top window shows the error. You can also see that this is error number 2 of 6. You can use the **Previous** and **Next** buttons to look at all the errors. At the bottom-right corner of the window, you can see three buttons that show you the HTML help files.
