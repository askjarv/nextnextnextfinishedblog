---
title: "QNAP recovery"
date: 2012-09-09
tags: 
  - "qnap"
  - "recovery"
---

You also hope to never have to search for a "recovery guide"- but an accidental reset (when all appeared lost as a hard-drive and failed and my QNAP failed to start) got me "back up" but without my data- so imagine my dismay when I couldn't find any data on the disk... and then couldn't find how to recovery the disk content from my QNAP T209 Pro.... after a lot hunting, I finally found a great PDF - I've recreated it here "just in case" it ever goes missing (although I hope I'll buy myself a new NAS before that day comes around!):

1\. Create a boot CD from this .iso file: http://us1.qnap.com/Storage/tsd/live-cd-2010-10-08.(TS-x19P+\_Recovery).iso

2\. Connect the hard disk from TS-109/209 to your computer via direct SATA connection, or USB external box. 3. Reboot your computer and change primary booting device to CD. Save and exit. 4. Upon rebooting is completed, enter User name = **root** and password = **root**

5\. Use the following command to find out which device is the TS-109/209 hard disk **fdisk –l** Typically, you'll be looking at /dev/sdb is the TS-109/209 as the hard disk.

and /dev/sdb3 is where the data is - we'll carry on with this for the example, although you may want to move around using **cd** and **ls** to check the contents/list your drives. 6. Mount the data partition **/dev/sdb3 on /mediamount –t ext3 /dev/sdb3 /media/ -o extents,mballoc,delalloc**

7\. Mount the hard disk inside your computer so that you can copy data to it. **mount /dev/sda1 /mnt/** 8. Use the command **df** and you should be able to see both devices are mounted.

9\. You are ready to copy your data now. Enter the directory where your files will be copied to. cd /mnt You can then use the following command to copy everything inside your cht\_office\_2003\_pro folder into /mnt, including the files inside the sub\_directories rsync -rav /media/Public/xxxx.file .

You can check by using the command **ls** to list your folder content.
