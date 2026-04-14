---
title: "IIS with multiple versions of asp.net"
date: 2011-03-03
categories: 
  - "iis"
tags: 
  - "asp-net"
---

It is not possible to run two different versions of ASP.NET in the same IIS process. Please use the IIS Administration Tool to reconfigure your server to run the application in a separate process.

Is as below:

Log into IIS,

Create a new Application pool - (i.e. Remote Workplace)

Browse to the remote site under websites,

Right click, properties, and browse to virtual directory,

Move the application pool to our newly created pool,

Click ok.

Test remote connectivity to remote workplace.

In this specific case, this did not require an issreset to work.

Just in case you come across this again.

Further details as to the cause are found at:

[http://weblogs.asp.net/owscott/archive/2006/01/26/Running-multiple-versions-of-the-Framework-in-ASP.NET.aspx](http://weblogs.asp.net/owscott/archive/2006/01/26/Running-multiple-versions-of-the-Framework-in-ASP.NET.aspx)
