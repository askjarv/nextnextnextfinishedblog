---
title: "Adding drivers to a WDS image- easier than you might first think"
date: 2012-01-22
---

WDS is a great time saver- but for some reason the documentation for it on the web sometimes lacks simple to follow guides- which means you waste time trying to help people do the simplest of things with it sometimes- hopefully the below will help you save some time!

- Connect to your WDS server
- Grab your drivers from the web and **extract** them to a folder (all too easy to leave them in a zip or executable!). Ensure they’re appropriate for the version of windows you are deploying (e.g. 64 bit).
- Open up the WDS console.
- Expand the servers area, then your server group and select drivers. Right click and chose Add Driver Package…

[![WDS Console](images/image006.png "WDS Console")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/wds01.png)WDS Console - Add Driver

-  It’s often easiest to point it to the directory, rather than a specific INF in case the driver has multiple components, so select “Select all driver packages from a fodler and click browse to find the extraction path from the step above.

[![Insert Driver](images/image014.jpg "Insert Driver")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/image014.jpg)

-  Click next, and allow it to find the driver packages

[![Select Drivers](images/image015.jpg "Select Drivers")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/wds02.jpg)

-  Click next once you’ve got the packages you want and next to add them to the server:

[![Confirm Selection](images/image011.png "Confirm Selection")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/wds03.png)

-  It’ll start adding them in the WDS driver collection.

[![Installing](images/image012.png "Installing")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/wds04.png)

-  Once that’s done, you can add it to a group (which makes it easier to identify old drivers, etc) – if one doesn’t exist, you can create one to reflect the laptop details (like the one in the example below)

[![Select Driver Group](images/image007.png "Select Driver Group")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/wds004.png)

-  Click next and you’re done- you can untick the modify the filters for this group now and click finish to get straight into action.

[![Modify Filters](images/image019.jpg "Modify Filters")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/wds07.jpg)

- Once added, you need to insert the driver into the boot image. Before that, though, you should back up the image- so expand Boot image then right click on the Windows Setup X86 and chose EXPORT IMAGE to save a copy of the image (date mark it for easy reference).
-  Then right click again on the image from before and chose add driver packages to image:

[![Apply to image](images/image0161.png "Apply to image")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/wds0008.png)

- In order to find the driver packages you want, click on the Add button, and chose the attribute type and set it to driver group name and equal to. Then, in the drop down box below, you can simply pick the driver group we created earlier and click add and ok. Then click on search for packages and it’ll pull back all the drivers you just added.

[![Apply Driver Group](images/image017.png "Apply Driver Group")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2012/01/wds00009.png)

-   Simply click on next, then next again and it’ll mount and insert the driver image details. Once complete, you should be ready to go
