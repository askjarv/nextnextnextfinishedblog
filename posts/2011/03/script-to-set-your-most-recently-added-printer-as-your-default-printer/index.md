---
title: "Script to set your most recently added printer as your default printer"
date: 2011-03-30
categories: 
  - "scripts"
  - "terminal-services"
tags: 
  - "citrix"
  - "printer"
  - "printing"
  - "script"
---

Here's a quick script to set your most recently added printer as your default printer

Set WshNetwork = WScript.CreateObject("WScript.Network")

Set oPrinters = WshNetwork.EnumPrinterConnections For i = 0 to oPrinters.Count - 1 Step 2

Device = oPrinters.Item(i+1) Next WshNetwork.SetDefaultPrinter Device
