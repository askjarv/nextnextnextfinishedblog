---
title: "Finding Physical NIC Port using MS iSCSI Initiators"
date: 2011-03-03
categories: 
  - "network"
tags: 
  - "nic"
  - "qlogic"
---

I had to check the MS iSCSI Initiator and find which port on the back of a QLogic card was used.

\- Launch MS iSCSI Initiator

\- Targets, Select Connected Target Name and click Details

\- Select Identifier under Sessions and click Connections

\- Note the Source Port (This is linked to the Interface IP)

\- Launch Device Manager

\- Expand SCSI and RAID Controllers

\- Select QLogic iSCSI Adapter and check the TCP/IP Settings in the adapter properties (Match the IP as noted above, if not check any additional QLogic Adapters)

\- Select the General Tab and check the Location section (This Lists the Device PCI slot, device and function)

\- The Function should reference the physical port on the QLogic card
