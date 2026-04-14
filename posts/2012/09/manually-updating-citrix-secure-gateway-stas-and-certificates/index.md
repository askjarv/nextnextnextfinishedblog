---
title: "Manually updating Citrix Secure Gateway STA's and Certificates"
date: 2012-09-30
tags: 
  - "citrix"
  - "sta"
  - "xenapp"
---

I recently had a problem updating a certificate for Citrix XenApp Essentials where by the web interface had been updated, and broken, and Secure Gateway used to try and stick the whole thing together- unfortunately  when the time came to update the certificate, it wouldn't play ball- the wizard would error claiming that port 443 was in use (it was- by Secure Gateway!) and, even if the service stopped, and no process running, it thought it couldn't continue. Fortunately, with a bit of leg work I managed to get round this by...

In the install directory of Secure Gateway, you'll find a .ini file which contains the setup (everything you set during the CSG wizard) - in here I found the thumbprint of the original certificate - you can check the thumbprint of a SSL certificate easily enough if you view the properties of a certificate - you can then verify you're original cert thumbprint, and your new one, and simply swap the values over. Bare in mind that modifying the config is not meant to be done by home- re-running the wizard will overwrite any settings!

To make things more difficult... even after this, I had a further issue- for some reason the STA would error- despite nothing having changed. Looking in my original ini file I spotted that the STA was called "SERVERNAME-XXXXX"... Hm- when you install a Citrix server, it automatically generates a STA (Secure Ticketing Authority ID)- and it would normally read as something along the lines of STA1111111111 etc where 1 would be random alphanumerical characters- I hadn't seen a hyphen in one before (for those who are interested, when you use Citrix servers in combination with lets say a Citrix Access Gateway or Secure Gateway, you have to add the Citrix STA ID to the CAG/SG as a token to identified why servers can be used for "resource identification"- everytime you reinstall a Citrix server you have to add these STA ID's to the CAG or AAC (depending on what you’re using) etc. for it to work at all!). 

Fortunately I found the CtxSta.config file in C:\\Program Files\\Citrix\\System32. And, upon opening the file I found something like this:

\[GlobalConfig\]UID=STA3A920721B00E TicketVersion=10 TicketTimeout=100000 MaxTickets=100000 LogLevel=0 MaxLogCount=10 MaxLogSize=20 LogDir=C:\\Program Files\\Citrix\\system32\\

You can edit the UID Number to whatever you like (keep the same amount of characters) as long as it's letters or numbers- my hyphen was therefore a oddity- once removed though, CSG was happy with the STA again and I could get going!
