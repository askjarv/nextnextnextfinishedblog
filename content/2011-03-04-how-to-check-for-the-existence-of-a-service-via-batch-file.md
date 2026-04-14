---
title: "How to check for the existence of a service via batch file"
date: 2011-03-04
categories: 
  - "scripts"
---

net start | find "Trend Micro Client/Server Security Agent RealTime Scan" > nul 2>&1

if not .%errorlevel%.==.0. [\\\\server\\ofcscan\\autopcc.exe](///\\server\ofcscan\autopcc.exe)
