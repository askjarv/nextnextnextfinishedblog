---
title: "Outlook Deployment on Citrix via Transofmraiton Files"
date: 2011-03-03
tags: 
  - "citrix"
  - "office-2003"
---

Create mst using ORK toolkit - [http://office.microsoft.com/en-us/office-2003-resource-kit/CH001149686.aspx](http://office.microsoft.com/en-us/office-2003-resource-kit/CH001149686.aspx)

Run this command to install office on Citrix server – this could overwrite existing mail profiles so use with caution! – only generally do this when a clean install of office on ts/ctx server

[\\\\Office2003](///\\Office2003) MSI\\setup.exe" TRANSFORMS="[\\\\advantage\\deployment\\GPO\\Office2000 MSI\\NoOutlook.MST](///\\advantage\deployment\GPO\Office2000%20MSI\NoOutlook.MST)" /qb

NB: Change path to mst
