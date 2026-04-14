---
title: "How to expand the range of ports in ISA to allow HTTPS over ports other than 443"
date: 2011-03-03
categories: 
  - "isa-server"
tags: 
  - "isa-server-2004"
  - "isa-server-2006"
  - "ssl"
---

If you ever have to set up ISA to allow ports other than 443 to accept SSL it’s a bit crazy – you need a third party app (note, this isn’t the case if you’re doing port redirection)- full instructions here ([http://www.isaserver.org/articles/2004tunnelportrange.html](http://www.isaserver.org/articles/2004tunnelportrange.html)) but to summarise:

 

“This application provides an easy to use graphical interface that allows you to extend the SSL tunnel port range. The figure below shows what the GUI for this application looks like.

 

Just enter the first port and last port you want to include in the SSL tunnel port range in the **LowPort** and **HighPort** text boxes and click the **Add Tunnel Range** button. Then click the **Refresh** button to see the new SSL tunnel port range in the list.

 

Note that if you have unbound the Web Proxy filter from the HTTP protocol, then Firewall and SecureNAT client connections made through the ISA firewall will not be redirected to the Web Proxy Filter. In this case, you can create a Protocol Definition for the alternate SSL port and then create an Access Rule allowing outbound access to that protocol.”

 

FYI: The link they give on the page for the utility is WRONG- it’s actually: [http://www.isatools.org/tools/ISAtrpe.zip](http://www.isatools.org/tools/ISAtrpe.zip) , but I’ve attached it for your reference!

 

This also works on ISA 2006- but is untested (and potentially unrequired) on TMG.
