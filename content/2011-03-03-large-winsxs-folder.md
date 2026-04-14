---
title: "Large WinSXS folder"
date: 2011-03-03
tags: 
  - "disk"
  - "tool"
  - "utility"
  - "windows"
---

Cleaning up disks is a pain- and often you find your server has a large %systemroot%\\WinSxS folder (we’ve seen over 11.3GB!)

In a nutshell, the Windows SxS directory represents the “installation and servicing state” of all system components and solves a number of issues in legacy Windows related to installation, servicing and reliability.  It is not possible to delete or remove files from this folder other than what the ‘COMCLN.exe’ program can safety remove, as  removing files effects the reliably of windows and the services it provides and it would affect all operating system components and the ability to update or configure optional components on the system and helps avoid uninstall issues with other programs

The following two links explain the engineering behind the WinSxS folder…

· [http://blogs.technet.com/b/askcore/archive/2008/09/17/what-is-the-winsxs-directory-in-windows-2008-and-windows-vista-and-why-is-it-so-large.aspx](http://blogs.technet.com/b/askcore/archive/2008/09/17/what-is-the-winsxs-directory-in-windows-2008-and-windows-vista-and-why-is-it-so-large.aspx)

· [http://blogs.msdn.com/b/e7/archive/2008/11/19/disk-space.aspx](http://blogs.msdn.com/b/e7/archive/2008/11/19/disk-space.aspx)

and there is a command-line program called COMPCLN.exe which  removes old service pack files.
