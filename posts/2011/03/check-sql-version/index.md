---
title: "Check SQL Version"
date: 2011-03-03
categories: 
  - "sql"
---

Guys,

If you need to check the version number (eg. 9.0.3042) so you can verify what SQL service pack is installed…

[![clip\_image002](images/clip_image002_thumb1.jpg "clip_image002")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0021.jpg)

You can run the following SQL script:

SELECT  SERVERPROPERTY('productversion'), SERVERPROPERTY ('productlevel'), SERVERPROPERTY ('edition')

[![clip\_image004](images/clip_image004_thumb1.jpg "clip_image004")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0041.jpg)

and check the version number via this link:

[http://www.sqlsecurity.com/FAQs/SQLServerVersionDatabase/tabid/63/Default.aspx](http://www.sqlsecurity.com/FAQs/SQLServerVersionDatabase/tabid/63/Default.aspx)
