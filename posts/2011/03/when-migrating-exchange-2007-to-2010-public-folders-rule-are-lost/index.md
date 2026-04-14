---
title: "When Migrating Exchange 2007 to 2010 Public folders rule are lost"
date: 2011-03-03
categories: 
  - "exchange"
tags: 
  - "exchange-2007"
  - "exchange-2010"
  - "public-folders"
---

An issue I came across that had been caused by the migration of Public Folders from Exchange 2007 to Exchange 2010 which is resolved here:

[http://blog.samkendall.net/2010/09/07/exchange-2007-to-2010-migration-public-folder-issue-fix/](http://blog.samkendall.net/2010/09/07/exchange-2007-to-2010-migration-public-folder-issue-fix/)

In essence any mail enabled folder that came across was failing to receive e-mail with the error:

[![clip\_image001](images/clip_image001_thumb2.jpg "clip_image001")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0012.jpg)

This is resolved by remove the empty Servers container in ADSIEDIT under the old Exchange Organisation
