---
title: "Sharepoint 2010 on Server 2012 R2"
date: 2014-10-15
categories: 
  - "server-2012-r2"
tags: 
  - "powershell"
  - "sharepoint"
  - "sharepoint-2010"
coverImage: "sharepoint2010logooficial.jpg"
---

Sharepoint 2010 is not anywhere near as easy to love as Sharepoint 2013, but there's plenty of places still running 2010 so if you need to create a quick lab setup it's tempting to throw in a quick installation now and again- fortunately, Microsoft are happy for you to run it on Server 2012 (so you don't have to go entirely back in time!)- [Http://blogs.technet.com/b/stefan\_gossner/archive/2014/05/03/sharepoint-2010-sp2-and-windows-server-2012-r2.aspx](http://blogs.technet.com/b/stefan_gossner/archive/2014/05/03/sharepoint-2010-sp2-and-windows-server-2012-r2.aspx  "SharePoint 2010 SP2 and Windows Server 2012 R2") 

but there are a couple of gotcha's I ran into the other day - namely the points outlined in the link above- which I'll highlight some key phrases from for ease of reference:

> Starting May 1st, 2014 SharePoint 2010 SP2 **slipstream media on [VLSC](https://www.microsoft.com/Licensing/servicecenter/default.aspx) and [MSDN](http://msdn.microsoft.com/) can be used to install SharePoint 2010 on Windows Server 2012 R2**.
> 
> **Only SP2 slipstream installations are supported** on Windows Server 2012 R2 - you cannot first install RTM or SP1 and then SP2.
> 
> Also be aware that **OS in place upgrade is NOT supported** with SharePoint 2010. You need to perform a **fresh installation of SharePoint 2010 SP2 slipstream** on top of Windows Server 2012 R2.

OK, with those gotcha's out the way (and presumably you've dug out the correct media!) - you'll want to dive straight in... only to find the pre-req wizard, which previously kindly guided you through the install quickly, doesn't play ball (at least in my experiences to date) with 2012 - fair enough I guess - throw in some extra 2012 .Net problems and you'll find the whole "supported on" element not quite as easy as you might like- so I put together a quick deployment powershell "script" (set of commands really) here to grab your relevant patches, pre-reqs, and install alongside the relevant OS roles and features (some of these aren't strictly requirements, but useful IMHO for Sharepoint deployments):

* * *

> \# Install Pre-reqs for Sharepoint 2010 on Windows Server 2012 R2! # No log files written except the defaults # Set up some bits - install path mkdir C:\\source #Identity Foundation Add-WindowsFeature windows-identity-foundation #Microsoft Sync Framework Runtime 1.0 SP1 (x64) wget http://download.microsoft.com/download/E/0/0/E0060D8F-2354-4871-9596-DC78538799CC/Synchronization.msi -outfile C:\\Source\\MSSnyc.msi C:\\source\\sync.msi /q #SQL wget http://download.microsoft.com/download/c/2/8/c28cc7df-c9d2-453b-9292-ae7d242dfeca/SQLEXPR\_x64\_ENU.exe -outfile C:\\source\\sqlexp2008.exe C:\\source\\setup.exe /QS /ACTION=Install /FEATURES=SQL,SDK /INSTANCENAME=MSSQLSERVER /SQLSVCACCOUNT="NT AUTHORITY\\Network Service" /SQLSYSADMINACCOUNTS="Users" /AGTSVCACCOUNT="NT AUTHORITY\\Network Service" #Filter Pack wget http://download.microsoft.com/download/0/A/2/0A28BBFA-CBFA-4C03-A739-30CCA5E21659/FilterPack64bit.exe -outfile C:\\source\\filter.exe C:\\source\\filter.exe /q # IIS DISM.EXE /enable-feature /online /featureName:IIS-WebServerRole /featureName:IIS-WebServer # ASPNET DISM.EXE /enable-feature /all /online /featureName:NetFx3 DISM.EXE /enable-feature /all /online /featureName:NetFx3ServerFeatures DISM.EXE /enable-feature /all /online /featureName:IIS-ISAPIFilter DISM.EXE /enable-feature /all /online /featureName:IIS-ISAPIExtensions DISM.EXE /enable-feature /all /online /featureName:IIS-ApplicationDevelopment DISM.EXE /enable-feature /all /online /featureName:IIS-ASPNET DISM.EXE /enable-feature /all /online /featureName:IIS-NetFxExtensibility DISM.EXE /enable-feature /all /online /featureName:IIS-WindowsAuthentication add-windowsfeature Web-CGI # IIS Manamagement Compatibility DISM.EXE /enable-feature /all /online /featureName:IIS-ManagementService DISM.EXE /enable-feature /all /online /featureName:IIS-IIS6ManagementCompatibility DISM.EXE /enable-feature /all /online /featureName:IIS-Metabase DISM.EXE /enable-feature /all /online /featurename:netfx4extended-aspnet45 # net Framework 3.5 Service Pack (NB: this presumes D drive has the Windows Server 2012 media inserted!) # AS a side note, this plays up if you have KB2966828 installed (at time of writing) so instlal before updating or uninstall! so the next line will check if it's there for you! Get-Hotfix | where hotfixid -eq KB2966828 dism /online /enable-feature /featurename:netfx3 /all /source:d:\\sources\\sxs # Chart Controls wget http://download.microsoft.com/download/c/c/4/cc4dcac6-ea60-4868-a8e0-62a8510aa747/MSChart.exe -outfile:C:\\Source\\MSChart.exe C:\\source\\mschart.exe /q

* * *

I hope that helps someone out there!
