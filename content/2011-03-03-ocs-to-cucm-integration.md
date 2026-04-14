---
title: "OCS to CUCM integration"
date: 2011-03-03
categories: 
  - "cisco-unified-call-manager"
  - "ocs"
tags: 
  - "cisco-call-manager"
  - "cucm"
  - "lync"
  - "voip"
---

##### Direct SIP: Cisco Unified Communications Manager 7.1

[![clip\_image001](images/clip_image001.gif "clip_image001")](http://blogs.technet.com/members/JBRD/)[DrRez](http://blogs.technet.com/members/JBRD/)

12 Oct 2010 7:26 AM

· Comments [0](http://blogs.technet.com/b/drrez/archive/2010/10/12/direct-sip-cisco-unified-communications-manager-7-1.aspx#comments)

_If you’re looking for an introduction about how to configure Cisco Unified Communications Manager (CUCM) version 7.1.3 with Office Communications Server 2007 R2, this article will help you. The proper way to connect and interoperate the two products is to set up a Direct SIP connection in Office Communications Server. On the Cisco side, this is referred to as a SIP trunk. This article covers how to configure a SIP trunk in CUCM 7.1._

**Author:** [Curtis Johnstone](http://blogs.technet.com/b/nexthop/p/contributors.aspx), [John Johnson](http://blogs.technet.com/b/nexthop/p/contributors.aspx), [Rui Maximo](http://blogs.technet.com/b/nexthop/p/contributors.aspx)

**Publication date:** August 2010

**Product version:** Office Communications Server 2007 R2

If you’re looking for an introduction about how to configure Cisco Unified Communications Manager (CUCM) version 7.1.3 with Office Communications Server 2007 R2, this article will help you. The proper way to connect and interoperate the two products is to set up a Direct SIP connection in Office Communications Server’s parlance. In Cisco’s parlance, this is referred to as a _SIP trunk_. So, when discussing the configuration of CUCM, we’ll refer to this connection as a SIP trunk. When explaining the configuration of the Office Communications Server, we’ll refer to this connection as a _Direct SIP_.

If you’re trying to connect CUCM with Office Communications Server 2007 R2, you probably already have CUCM deployed in your environment for all your IP phones and CUCM configured to route all external calls to the PSTN through a PSTN trunk. In this case, you’ll want to configure Office Communications Server 2007 R2 Enterprise Voice to route external calls to the PSTN through the CUCM PSTN trunk. Calls between Communicator users and Cisco IP phone users should be possible by using each user’s unique extension number, and users are accessible via externally routable direct inward dialing (DID). This is illustrated in Figure 1.

**Figure 1. Routing of calls between Communicator users and Cisco IP phone users**  
[![clip\_image002](images/clip_image002_thumb.jpg "clip_image002")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image002.jpg)

It is worth clarifying that a new range of phone numbers assigned to Communicator endpoints must be defined in CUCM. This new range needs to be separate from any existing number range used for Cisco desk phone endpoints. For end users who have both a Cisco desk phone and a Communicator client, the same number cannot be used for inbound and outbound dialing. This restriction exists because call routing for Communicator clients in CUCM is achieved by creating a new SIP trunk that is used only for Communicator endpoints. Multiple device endpoints cannot share the same number when the call routing is defined on different SIP trunks.

For details about Office Communications Server telephony integration, including options for the coexistence of specific features, see "[Integrating Telephony with Office Communications Server 2007 and 2007 R2](http://go.microsoft.com/fwlink/?LinkId=133655)".

There are two parts to interoperating the two products: configuring CUCM and configuring Office Communications Server. The high level steps for configuring CUCM are as follows:

1\. Create a partition.

2\. Create a calling search space.

3\. Define translation patterns.

4\. Provision a SIP trunk.

5\. Set up route pattern.

The following sections describe the CUCM configuration steps in more detail. For details about how to configure Direct SIP on Office Communications Server 2007 R2 Mediation Server, see [Direct SIP: Configuring Mediation Server](http://technet.microsoft.com/en-us/library/ee862410.aspx).

###### Configuring Cisco Unified Communications Manager 7.1.3

Let’s dive into the configuration steps for CUCM. The connectivity between CUCM and the Mediation Server is referred to as SIP trunk to conform to Cisco’s terminology.

###### Create a Partition

A CUCM partition contains a list of route patterns. Partitions facilitate call routing by dividing the route plan into logical subsets that are based on organization, location, and call type. For details about partitions, see "Partitions and Calling Search Spaces" in the CUCM System Guide.

This partition is specific to the SIP trunk that connects Office Communications Server to CUCM. It will store route pattern and translation pattern rules that are specific to handling incoming traffic to CUCM from the Mediation Server. For our example, this partition is named "OCSIncoming".

To create a CUCM partition

1\. From your CUCM Administration console, click **Call Routing**, click **Class of Control**, and then click **Partition** (Figure 2).

**Figure 2. Opening the partitions screen**  
[![clip\_image003](images/clip_image003_thumb.jpg "clip_image003")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image003.jpg)

2\. Click **Add New** to create a new partition as showing in Figure 3.

**Figure 3. Adding a new partition**  
[![clip\_image004](images/clip_image004_thumb.jpg "clip_image004")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image004.jpg)

3\. In the **Name** field, specify the name of the partition and a description as shown in Figure 4. We’ve specified "OCSIncoming, OCSIncoming".

**Figure 4. Name and description of the partition**  
[![clip\_image005](images/clip_image005_thumb.jpg "clip_image005")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image005.jpg)

4\. Click **Save**, and then click **Find** to verify that the partition was created. The new partition should appear in the result set as shown in Figure 5.

**Figure 5. New partition successfully created**  
[![clip\_image006](images/clip_image006_thumb.jpg "clip_image006")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image006.jpg)

5\. To view the configuration, click the new partition name (Figure 6).

**Figure 6. Partition information**  
[![clip\_image007](images/clip_image007_thumb.jpg "clip_image007")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image007.jpg)

|   **[![clip\_image008](images/clip_image008_thumb.gif "clip_image008")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image008.gif)****Note:**   |
| --- |
|   Whether a partition is required in a particular environment may depend on the rules required. Verify this with your CUCM administrator.   |

###### Create a Calling Search Space

A CUCM calling search space is an ordered list of route partitions. Calling search spaces determine which partitions and the order in which they are searched when CUCM routes a call. In our example, this calling search space is named "OCSIncoming" and is assigned to the OCSIncoming partition created earlier.

**To create a calling search space**

1\. From the CUCM Administration console, click **Call Routing**, click **Class of Control**, and then click **Calling Search Space** (Figure 7).

**Figure 7. Opening the Calling Search Space Configuration screen**  
[![clip\_image009](images/clip_image009_thumb.jpg "clip_image009")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image009.jpg)

2\. Click **Add New** to create a new calling search space. Specify a name for the calling search space. In our example, the new calling search space is "OCSIncoming".

3\. Select the OCSIncoming partition, and then click the down arrow to move it to the **Selected Partitions** area to assign this calling search space to the OCSIncoming partition (Figure 8).

**Figure 8. Assigning the OCSIncoming calling search space to the OCSIncoming partition**  
[![clip\_image010](images/clip_image010_thumb.jpg "clip_image010")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image010.jpg)

4\. Click **Save** to insert this calling search space into the CUCM configuration.

###### Define Translation Patterns

Next, translation patterns must be defined and assigned to the newly created partition. Translation patterns manipulate dial strings before a call is routed.

The translation patterns we’ll define are specific for handling inbound calls to the CUCM that come from Office Communications Server. A translation pattern converts dial strings for calls sent by the Mediation Server where the TO field matches the pattern. CUCM then uses the translated dial string to determine how to route the call.

One or more translation patterns must be defined depending on your needs. At a minimum, you need to define at least two translation patterns:

- A translation pattern for incoming calls from Office Communications Server that are destined for the PSTN. This allows Office Communicator users who are enabled for Enterprise Voice to dial out externally.
- A translation pattern for incoming calls from Office Communications Server that are destined for CUCM-assigned phone numbers. This allows Office Communicator users to dial Cisco phones within the organization.

If users are allowed to dial international numbers, you have to define a third translation pattern. Consider creating translation patterns for emergency numbers (for example, 911).

**Office Communications Server to PSTN Translation Pattern**

The first translation pattern (called 33.xxxxxxxxx, which means the TO string starting with 33 followed by 9 digits as shown in Figure 9) transforms all calls from Office Communications Server that are destined to a domestic PSTN number.

On your CUCM Administration console, click **Call Routing**, click **Translation Pattern** (Figure 9), and then click **Add New** to create a new translation pattern configuration.

**Figure 9. Opening the Translation Pattern Configuration screen**  
[![clip\_image011](images/clip_image011_thumb.jpg "clip_image011")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image011.jpg)

The translation pattern is assigned to the OCSIncoming partition that you previously created.

The period (.) is a separator that indicates that all digits before the period are to be discarded. This separator is used in the **Called Party Transformations** section (see Figure 10) when the **Discard Digits** setting is set to **PreDot**. In our example, 33 will be removed from the dial string. For North America and the Caribbean, the **Numbering Plan** should be set to **NANP** as shown in Figure 10. NANP is the standard PSTN numbering plan for North America and the Caribbean. Configuring incoming call routing for other geographic regions requires a **Numbering Plan** setting that is standard for that region.

For the FROM field, the last 9 digits are retained. The country prefix (which is 33 for France) is stripped from the E.164 calling party dial string and is presented to the PSTN in the required format, 16986xxxx. In this case, the translation pattern transforms the dial string from 3316986xxxx to 16986xxxx.

For the TO field, the pattern strips the leading 33 and adds 00 as a prefix to the remaining string. The translation pattern transforms the dial string from 33xxxxxxxxx to 00xxxxxxxxx, where the first 0 is the outside line prefix that is required to obtain an outside line on CUCM.

**Figure 10. Configuring a new translation pattern**  
[![clip\_image012](images/clip_image012_thumb.jpg "clip_image012")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image012.jpg)

**Office Communications Server to CUCM Translation Pattern**

The second translation pattern (in this example, 3316986xxxx) transforms all calls from Office Communications Server that are destined for a CUCM assigned number. The translation pattern is assigned to the OCSIncoming partition that you created earlier. Because all calls from Office Communications Server will likely be in RFC 3966 format, calls in this example are prefixed by the country code, 33 for France, and then followed by the prefix for all numbers that are assigned to Cisco IP phones, 16986, in the enterprise. This pattern is applied to calls where the TO field matches the pattern, 3316986xxxx. Because CUCM selects translation patterns on the basis of the best match, this translation pattern will be selected instead of the first translation pattern.

In our example, this translation pattern translates dial strings for calls sent by the Mediation Server where the TO field matches the pattern, 3316986xxxx. It strips all leading digits from TO and FROM fields and retains only the last 4 digits, xxxx. Dial strings with the pattern 3316986xxxx are translated to dial strings of the form xxxx. As shown in Figure 11, this translation is performed on the number of the user being called (TO field) and on the caller’s number (FROM field). The caller-id information originates from the line URI attribute of the Communicator caller, which is defined as a user property in Active Directory. This caller-id is formatted by any matching Office Communications Server normalization rules before being matched against the CUCM translation patterns.

|   **[![clip\_image008\[1\]](images/clip_image0081_thumb.gif "clip_image008[1]")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image0081.gif)****Note:**   |
| --- |
|   If the CUCM Simultaneous Ring feature is used, and the caller has a Cisco Remote Destination Profile set up with their Office Communications Server line URI attribute in the “Destination Number” field, the caller’s number will be mapped to their corresponding Cisco line number.   |

**Figure 11. Office Communications Server to CUCM translation pattern**  
[![clip\_image013](images/clip_image013_thumb.jpg "clip_image013")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image013.jpg)

###### Provision a SIP Trunk

A SIP trunk to the Mediation Server is created on the CUCM and is assigned the OCSIncoming calling search space that was created earlier. The SIP trunk uses SIP over TCP, which requires port 5060.

The CUCM SIP trunk is established to the IP address of the Mediation Server that represents the gateway listening IP address. The Mediation Server must be configured with two IP addresses. One IP address connects to the Office Communications Server infrastructure; the other IP address connects to the CUCM, which represents the gateway.

If you’re not sure which IP address is the gateway listening IP address for your Mediation Server, see Figure 4 in the article [Direct SIP: Configuring Mediation Server](http://technet.microsoft.com/en-us/library/ee862410.aspx).

In our example, the trunk name is Trunk\_to\_OCS, and the Mediation Server’s gateway listening IP address is 192.168.0.105.

**To create a new SIP trunk**

1\. On the CUCM Administration console, click **Device**, and then click **Trunk** (Figure 12).

**Figure 12. Adding a new trunk**  
[![clip\_image014](images/clip_image014_thumb.jpg "clip_image014")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image014.jpg)

2\. Click **Add New**, and then on the **Trunk Type** list, select **SIP Trunk**. Select **SIP** as the **Device Protocol**, and then click **Next** (Figure 13).

**Figure 13. Configuring the SIP trunk**  
[![clip\_image015](images/clip_image015_thumb.jpg "clip_image015")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image015.jpg)

3\. Specify the **Device Name** (in our example, Trunk\_to\_OCS), the **Calling Search Space** (in our example, OCSIncoming), the **Rerouting Calling Search Space** (in our example, OCSIncoming), the **Destination Address** to match the Mediation Server gateway listening IP address (in our example, 192.168.0.105), and **Destination Port** (in our example, 5060).  
Table 1 lists the required Trunk Configuration settings and their values (Figure 14).

**Table 1. Required Trunk Configuration settings**  
[![clip\_image016](images/clip_image016_thumb.jpg "clip_image016")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image016.jpg)

To successfully communicate with the Mediation Server, CUCM must use the codec, G.711. The device pool default setting in CUCM 7.1 is configured to use the G.711 codec. The Device Pool setting shown in Table 1 and Figure 14 should be set to "Default". If your CUCM default device pool does not use G.711 as the codec, you will need to use a device pool that uses G.711.

**Figure 14. Trunk Configuration settings**  
[![clip\_image017](images/clip_image017_thumb.jpg "clip_image017")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image017.jpg)

4\. Click **Save**, and then reset the trunk by clicking the **Reset** icon at the top of the **Trunk Configuration** page to activate the SIP trunk changes.

[![clip\_image018](images/clip_image018_thumb.gif "clip_image018")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image018.gif) Set Up Route Pattern: CUCM to Office Communications Server

Route patterns are designed for routing calls from CUCM to the Mediation Server over the SIP trunk so that users who are using a Cisco IP phone can call Office Communicator users. The route patterns determine which calls are sent to the SIP trunk based on a pattern match of the phone number in the TO field. Route patterns can also perform transformations of the dial strings for the TO and the FROM fields.

**To set up the route pattern**

1\. From the CUCM Administration console, click **Call Routing**, click **Route/Hunt**, and then click **Route Pattern** (Figure 15).

2\. Click Add New, and then configure the route pattern.

**Figure 15. Opening the Route Pattern screen**  
[![clip\_image019](images/clip_image019_thumb.jpg "clip_image019")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image019.jpg)

For example, if you want users who are using a Cisco IP phone to be able to dial an Office Communicator user using a 4-digit extension, create a route pattern that is associated to the Trunk\_to\_OCS SIP trunk that you created earlier that instructs CUCM to route to the Mediation Server all calls that match the TO dial string with the pattern xxxx. In this case, no transformation of the dial strings in the TO and the FROM fields is necessary. This route pattern configuration is illustrated in Figure 16.

**Figure 16. Route pattern**  
[![clip\_image020](images/clip_image020_thumb.jpg "clip_image020")](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/clip_image020.jpg)

You will need to define multiple CUCM routing patterns if you have different Office Communications Server numbering formats for specific offices or geographic locations.

That completes your introduction to configuring a SIP trunk on Cisco’s Unified Communications Manager (also known as CallManager).

###### Additional Resources

To learn more, check out the following articles:

- [Direct SIP: Cisco Unified Communications Manager 6.1](http://technet.microsoft.com/en-us/library/ee862409.aspx)
- [Setting up the Cisco Call Manager 4.2.1 for "Direct SIP with IP-PBX"](http://go.microsoft.com/fwlink/?LinkId=178442)
- [Direct SIP with IP-PBX in Office Communications Server 2007](http://go.microsoft.com/fwlink/?LinkId=178443)
- [Microsoft and Cisco: Joint Interoperability Support Statement](http://go.microsoft.com/fwlink/?LinkId=178900)
