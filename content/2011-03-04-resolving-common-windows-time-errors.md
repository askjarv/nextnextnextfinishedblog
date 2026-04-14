---
title: "Resolving common windows time errors"
date: 2011-03-04
tags: 
  - "ntp"
  - "time"
  - "windows"
---

Time is critical to many elements within a domain because it can impact trusts between machines which is a key(spud pun intended) to authentication and access control.

There will be a few alerts and one will look like this:

_Event Log: System Event Source: W32Time Event ID: 29 Research   
Severity: Error   
Details: The time provider NtpClient is configured to acquire time from one or more   
time sources, however none of the sources are currently accessible.   
No attempt to contact a source will be made for 960 minutes.   
NtpClient has no source of accurate time._

This means that the host has a source of time but cannot reach it. You can determine a hosts time source with the following command:

NET TIME /QUERYSNTP

Often this will be time.windows.com,0x1 which is bogus. Domain members should generally have no time source because they will sync with a server further up the time hierarchy. To reset the time source to default you can do the following:

NET STOP W32TIME

W32TM /UNREGISTER

W32TM /REGISTER

NET START W32TIME

W32TM /RESYNC

All domains do require a valid time source though, for the most part this should be the PDC for the domain. If you see the PDC experience the above then you must determine whether the time source is valid with:

NET TIME /QUERYSNTP

And if not set it with:

NET TIME /SETSNTP:UK.POOL.NTP.ORG

After setting this restart the Windows Time Service:

NET STOP W32TIME && NET START W32TIME

And check the event logs to see if there are any issues, if there are remember that this host needs to have a NAT’d outbound rule which allows UDP 123 to at least UK.POOL.NTP.ORG.
