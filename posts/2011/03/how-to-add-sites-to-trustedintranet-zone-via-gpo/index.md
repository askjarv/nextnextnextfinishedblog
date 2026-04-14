---
title: "How to add sites to trusted/intranet zone via GPO"
date: 2011-03-03
categories: 
  - "internet-explorer"
tags: 
  - "group-policy"
---

To create a policy to add a site to the **Trusted Sites** [security](http://www.windowsitpro.com/article/tips/jsi-tip-6644-how-can-i-use-group-policy-to-add-a-site-to-the-trusted-sites-zone-.aspx) zone:

01\. Log on as a member of the **Domain Admins** group.

02\. Open the **Active Directory Users and [Computers](http://www.windowsitpro.com/article/tips/jsi-tip-6644-how-can-i-use-group-policy-to-add-a-site-to-the-trusted-sites-zone-.aspx)** **MMC** snap-in.

03\. Right-click the domain or Organizational Unit where you want to create the **GPO** and press **Properties**.

04\. Select the **Group Policy** tab.

05\. Press **New**.

06\. Type a name for the new **GPO** and press **Enter**.

07\. To prevent the policy from being applied to some users or groups, press **Properties**. Select the **Security** tab. Add the user or group that you want to prevent from having this policy and clear the **Read** and the **Apply Group Policy** boxes in the **Allow** column. Press **OK**.

08\. Press the **Edit** button.

09\. Navigate through **User Configuration / Windows Settings / [InternetExplorer](http://www.windowsitpro.com/article/tips/jsi-tip-6644-how-can-i-use-group-policy-to-add-a-site-to-the-trusted-sites-zone-.aspx) Maintenance / Security**.

10\. Right-click **Security Zones and Content Ratings** in the right-hand pane and press **Properties**.

11\. Select **Import the current security zones and privacy settings**. If prompted, press **Continue**.

12\. Press **Modify Settings**.

13\. Select **Trusted Sites** and press the **Sites** button.

14\. Type the full URL of the site you wish to add and press **Add**.

15\. Press **Close** (or **OK**) and **OK**.

16\. Press **Close** (or **OK**) until all dialog boxes are closed, and close any snap-in windows.

17\. Allow sufficient time for the policy to propagate throughout the domain.

**NOTE:** See [How can I manually add a site to the **Trusted Sites** zone?](http://www.windowsitpro.com/article/jsifaq/jsi-tip-6643-how-can-i-manually-add-a-site-to-the-trusted-sites-zone-.aspx)
