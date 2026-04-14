---
title: "SQL Service pack install failure"
date: 2011-03-30
categories: 
  - "sql"
  - "wsus"
tags: 
  - "service-pack"
  - "update"
---

The SQL service packs seem to always fail more often than most when installing patches but if you do get a failure try checking all SQL related services and making sure that none of them are disabled; if they are then set them to manual.

MSSQL$....

SQLAgent$.....

SQL Server…..

The most common catch we've found is the  "MSSQL$SBSMONITORING" service that is often disabled (as it's unused)  and after being set to manual the service pack which failed previously installs successfully!
