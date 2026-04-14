---
title: "Veeam Powershell"
date: 2013-06-03
---

Sometimes things are simple... and sometimes Google answers the question for you! I was having issues getting started with scripting my Veeam server (to generate reports for a customer in a custom format) - I only realized after a minute of stupidity that I was missing the Powershell add-in. Despite "repairing" my install and making sure the component was there, ensuring Powershell 2.0 and .net 4.5 were ok I found myself googling around and found the script - "Install-VeeamToolkit.ps1" in the installation folder, default location "C:\\Program Files\\Veeam\\Backup and Replication" - running this instantly saved my bacon and let me start running my lovely reporting scripts!
