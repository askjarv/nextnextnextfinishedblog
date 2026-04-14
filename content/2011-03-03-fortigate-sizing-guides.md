---
title: "Fortigate sizing guides"
date: 2011-03-03
categories: 
  - "fortigate"
---

Please be aware that using the model number to determine the device capacity should **not** be done.  You should be using the Product Sizing Tool available within the partner portal ([https://competitive.myfortinet.com/product\_sizing](https://competitive.myfortinet.com/product_sizing)).

[![clip\_image001](images/clip_image001_thumb.jpg "clip_image001")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image001.jpg)

Below is a PowerPoint slide showing what Fortinet suggest at present…

[![clip\_image003](images/clip_image003_thumb.gif "clip_image003")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image003.gif)

Another factor should also be considered is the “Web Proxy”, which is not shown in either the Sizing Tool or Slide.  If planning to use this, you’ll need to times the user count by 4 as the feature uses a greater amount of processing time and memory.

The “Web Proxy” can be used in place of ISA, IWSS, etc. and now can be utilised from Citrix XenApp environment at a per user basis.

· System > Network > Interface = Choose the relevant interface, select “Enable Explicit Web Proxy”

[![clip\_image004](images/clip_image004_thumb2.jpg "clip_image004")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0042.jpg)

· System > Network > Web Proxy = Enable “Enable Explicit Web Proxy” and choose preferences such as port etc…

[![clip\_image005](images/clip_image005_thumb1.jpg "clip_image005")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0051.jpg)

+

· Firewall > Policy > Policy= Create new policy from source “Web-Proxy”

[![clip\_image006](images/clip_image006_thumb1.jpg "clip_image006")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0061.jpg)
