---
title: "Windows 10 - quick and easy"
date: 2014-10-02
tags: 
  - "opinion"
  - "screencast"
  - "windows-10"
coverImage: "icons.jpg"
---

Well, after fighting with the usual bandwidth issues (especially bad in the UK- I believe they're typically more consistent in the US where there's presumably more (and closer) content repositories) Windows 10 the ISO is on my machine and I've done a very quick video using Jing to show the installation process in VMware Workstation (10.0.3 seems happy to pretend 10 is Windows 8 in case you were wondering).

**Watch the screencast here: [http://screencast.com/t/qCEeJNdIej](http://screencast.com/t/qCEeJNdIej "Watch the Video of the install in VMware workstation!")**

The install process is pretty much identical to Windows 8 - and took just over 5 minutes on my machine. After that, VMware tools was happy to install, and display drivers, networking, etc all worked happily - gone are the days of quirky driver problems straight out the door.

Initial thoughts?

- The new start menu is nice (but oddly didn't show any apps when I first started up (although that could be down to the low initial resolution I had pre-VMware tools install), although not radically different from Windows 7 or 8 beforehand (that, oddly enough, might be a feat in itself as it feels strangely familiar straight away).
- The new flat icons are nice, but weird - Microsoft will likely never achieve Apple's "consistent" icon design language - too many apps (many historical) will have 3D effects, shadows, etc that break (IE currently looks odd next to the flat mail and Explorer icons) - but it's an interesting design move (given Google's Material design language move too)- certainly the illusion of depth adds nothing on the old icons (until we all start using VR versions of the OS can peak at the icon at different angles!) ...

[![Windows 10 - Icons - Consistency out the Window!](images/icons.jpg)](https://nextnextnextfinished.wordpress.com/wp-content/uploads/2014/10/icons.jpg)

- ... at the moment the ultimate effect is inconsistent (see my comment yesterday about two control-panels - an issue which persists in 8.1, two years after it's original release) - there's a desperate need for a common design pratice (why is search, and the new desktop alignment icon, set in white and other icons in colour?!)
- Windows 8 Apps certainly have some odd quirks in "Windowed" mode - there's double scroll bars in the store and apps continue to scroll horizontally rather than vertically (especially odd now when using a scroll wheel to go down, and especially quirky when there's no real reason to think that left to right makes more sense than top to bottom) - but I guess these apps are still early days and are far from the end product.
- Signing in with my Microsoft account is tidy and simple- my desktop backgrounds from Windows 8 are instantly back in play which is nice- I hope everything about the upgrade process is as seamless as this (certainly, on first inspection, my mail accounts, and IE preferences seem to have come across nicely).
- Clicking around has made me spot the option to swap the command prompt with powershell when pressing Win+X or right clicking on the start menu which is present in 8 - I like this ... but seriously Microsoft, new Command Prompt functions (CTRL-V, CTRL-C) (which are present in the PowerShell, just in case you're wondering) ought to be activated by default (they weren't for me!).
- Interestingly, on the command prompt bit again, these new options are labelled as experimental:

\[caption id="attachment\_448" align="aligncenter" width="421"\][![Windows 10 - Command Prompt - Experimental Tab](images/capture.jpg)](https://nextnextnextfinished.wordpress.com/wp-content/uploads/2014/10/capture.jpg) Windows 10 - Command Prompt - Experimental Tab.\[/caption\]

- It'll be interesting to see if Experimental comes across to the production builds (seems unlikely, but if MS is planning progressive, always updating, Chrome/Firefox style rolling upgrades it could be that we will see this in the "mainline" OS) - I wonder if we'll be able to control this (as a sys-admin) via Group Policy- it would be fun to think we could "block" experimental tabs for users when we want a consistent environment (for training, ease of use, etc) but enable them for power users...

I hope to have more thoughts on the OS soon after I've done a bit more exploring!
