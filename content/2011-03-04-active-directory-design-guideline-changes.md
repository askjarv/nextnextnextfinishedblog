---
title: "Active Directory Design Guideline Changes"
date: 2011-03-04
categories: 
  - "active-directory"
tags: 
  - "dns"
  - "domain"
---

Hi folks,

After a bit of reading, best practice for Active Directory domain design and operations now suggests:

1\. Only use Active Directory DNS domain names which you can register publically (and ideally, are already registered) – this means no more “company.local” DNS domain names

2\. Don’t bother with empty forest root (“placeholder”) domains – they don’t help with migrations, demergers, security or anything else and are just a waste of two good Windows licences

3\. Don’t create a Windows virtual machine template without SYSPREPing it first – otherwise, if it ends up being a DC, you’ve had it

4\. NEVER snapshot a domain controller

5\. NEVER clone a domain controller
