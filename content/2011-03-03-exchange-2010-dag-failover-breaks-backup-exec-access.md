---
title: "Exchange 2010 DAG FAILOVER breaks backup exec access"
date: 2011-03-03
categories: 
  - "exchange"
tags: 
  - "backup"
  - "dag"
  - "exchange-2010"
---

Just had the issue below , Exchange failover not as seamless as suggested (pre SP1) . This does not effect end users as mail is still online

[![clip\_image001](images/clip_image001_thumb1.jpg "clip_image001")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0011.jpg)

This is however nothing to do with the Remote agent and is actually a bug in Exchange 2010 pre SP1.   You need to Check Cluster manager and then under Cluster Resources you will notice the Cluster is offline. It will not allow you to bring online Although you should never touch the failover clustering for Exchange DAG setup . You have to make an exception for the workaround on the link below . There is the usual padding and 3 options that achieve the same result.

[http://blogs.technet.com/b/timmcmic/archive/2010/05/12/cluster-core-resources-fail-to-come-online-on-some-exchange-2010-database-availability-group-dag-nodes.aspx](http://blogs.technet.com/b/timmcmic/archive/2010/05/12/cluster-core-resources-fail-to-come-online-on-some-exchange-2010-database-availability-group-dag-nodes.aspx)

I did as follows and all was good.

**_Windows 2008 / Windows 2008 R2 – Using Failover Cluster Management Tool_**

The network state can be reset using Failover Cluster Manager

- Launch Failover Cluster Management
- Expand the cluster \\ networks.

[![clip\_image003](images/clip_image0031.gif "clip_image003")](http://blogs.technet.com/blogfiles/timmcmic/WindowsLiveWriter/ClusterCoreResourcesfailtocomeonlineons_83A6/image_14.png)

- Get the properties of the cluster network in question.
- Uncheck the box to “Allow clients to connect through this network”.

[![clip\_image005](images/clip_image005.gif "clip_image005")](http://blogs.technet.com/blogfiles/timmcmic/WindowsLiveWriter/ClusterCoreResourcesfailtocomeonlineons_83A6/image_16.png)

- Press <apply> - you will be prompted with the following – select OK.

[![clip\_image007](images/clip_image007.gif "clip_image007")](http://blogs.technet.com/blogfiles/timmcmic/WindowsLiveWriter/ClusterCoreResourcesfailtocomeonlineons_83A6/image_18.png)

- Press <OK> to exist the properties pane.
- The network is disabled for “Allow clients to connect through this network”. 

Next we need to enable the network for “Allow clients to connect through this network”.

- Get the properties of the cluster network.
- Check the box to “Allow clients to connect through this network”.

[![clip\_image009](images/clip_image009.gif "clip_image009")](http://blogs.technet.com/blogfiles/timmcmic/WindowsLiveWriter/ClusterCoreResourcesfailtocomeonlineons_83A6/image_20.png)

- Press <apply> – you will be prompted with the following – select OK.

[![clip\_image011](images/clip_image011.gif "clip_image011")](http://blogs.technet.com/blogfiles/timmcmic/WindowsLiveWriter/ClusterCoreResourcesfailtocomeonlineons_83A6/image_22.png)

- Press <OK> to exist the properties pane.
