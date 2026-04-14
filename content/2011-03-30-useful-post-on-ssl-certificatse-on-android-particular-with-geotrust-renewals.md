---
title: "Useful post on SSL certificatse on Android (particular with Geotrust renewals)"
date: 2011-03-30
categories: 
  - "iis"
  - "windows"
tags: 
  - "android"
  - "certificates"
  - "geotrust"
---

It would appear as if the new root CA from Geotrust isn't natively trusted on Android devices - which means you can get cert errors even if your client facing cert seems 100% ok (this also appears to effect Windows Mobile 6.5) - basically there's a missing link in the chain- this link in the forums goes through the implications and the fix.

http://code.google.com/p/android/issues/detail?id=10985

Basically, you'll be looking to install the intermediary cert on your server:

[https://knowledge.geotrust.com/support/knowledge-base/index?page=content&actp=CROSSLINK&id=SO15687](https://knowledge.geotrust.com/support/knowledge-base/index?page=content&actp=CROSSLINK&id=SO15687)

which isn't too much hassle for compatibility with your mobile devices again!
