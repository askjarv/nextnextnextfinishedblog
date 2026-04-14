---
title: "RE: Citrix Published apps opening in full desktop - Solved"
date: 2011-03-04
tags: 
  - "citrix"
---

Updated:

A hotfix for the problem that described is available as described on [http://support.microsoft.com/kb/969851](http://support.microsoft.com/kb/969851)

  
Citrix Published apps opening in full desktop - Solved

This issue has been affecting a number of users in for a while- when opening a Citrix published application will open a full Citrix desktop instead. This is due to a check box within the ad profile set to start program at logon.

It is due to a bug within AD and when amended from a 2003 AD it can corrupt the object and this option will display differently from a 2008 AD.

To resolve this, ensure the option shown in the attachment “Start the following program at logon” is **UNCHECKED.** Because of the corruption to the object this can only be shown from a 2003 AD as the 2008 AD will show this option as unchecked.

This option to load a program at startup will override any other request (including the published application) and because there is no program specified it will open the explorer shell instead.
