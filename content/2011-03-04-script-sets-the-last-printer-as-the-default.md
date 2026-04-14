---
title: "Script sets the last printer as the default"
date: 2011-03-04
categories: 
  - "scripts"
tags: 
  - "printers"
  - "vbs"
---

Script to set the last loaded printer as the default printer

Set WshNetwork = WScript.CreateObject("WScript.Network")  
Set oPrinters = WshNetwork.EnumPrinterConnections  
For i = 0 to oPrinters.Count - 1 Step 2   
  Device = oPrinters.Item(i+1)   
Next  
WshNetwork.SetDefaultPrinter Device
