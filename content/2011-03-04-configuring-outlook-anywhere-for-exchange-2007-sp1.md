---
title: "Configuring Outlook Anywhere for Exchange 2007 SP1"
date: 2011-03-04
categories: 
  - "exchange"
tags: 
  - "exchange-2007"
  - "outlook-anywhere"
  - "rpc-https"
---

Exchange 2007 has rebranded rpc/https which is now called Outlook Anywhere and has even made some slight modification from RTM to Exchange 2007 SP1. +  
[http://msexchangeteam.com/archive/2007/11/08/447484.aspx](http://msexchangeteam.com/archive/2007/11/08/447484.aspx)

When utlizing Outlook 2007 the autodiscover service is heavily tied into Outlook anywhere functionality, I am going to reference a previous posting that explains those functions in detail.  
[http://exchange-genie.blogspot.com/2007/07/autodiscover-ad-attribute.html](http://exchange-genie.blogspot.com/2007/07/autodiscover-ad-attribute.html)

With Exchange 2007 in order to allow clients remote access to the mail system you will need to install an Exchange 2007 CAS server which will allow clients to access thier mail via Imap,Pop,OWA,Active Sync, and Rpc/https (outlook anywhere).

For this article I am going to skip the installation of each server role and just work with the configuration. The lab consists of 1 DC, 1 CAS/Hub and 1 MBX server running Windows 2003 and Exchange 2007 SP1.

[![](images/rpc_proxy.jpg)](http://2.bp.blogspot.com/_jG-efUpJ7Oc/R-rtPie74OI/AAAAAAAAAr8/pgCGZ3anNmo/s1600-h/rpc_proxy.jpg)

Rpc/http was first introduced with Exchange 2003 and has been renamed with Exchange 2007 to Outlook Anywhere. In order to use this functionality with Exchange we must install the RPC over HTTP Proxy networking component on a server (recommened on your Exchange server).

What does this network componet do for us?  
RpcProxy.dll is an Internet Server API (ISAPI) that runs in Internet Information Services (IIS). RpcProxy.dll listens for activity on the RPC virtual directory

The rpcproxy.dll requires authentication and will not pass anonymous request even if IIS is configured for anonymous authentication.

When an Outlook clients typicaly communicates with an Exchange server the client attempts to connect via Mapi Rpc, with Rpc/http Outlook makes a http connection to the rpc proxy server which strips the http and send the rpc request to tha appropriate Exchange server.

**Installing Rpc/http networking componet:**  
1\. From the Add/Remove programs select Windows components  
2\. Select Networking Services then details  
[![](images/i1.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/i1.jpg)  
3\. Select Rpc over http proxy -> OK  
[![](images/i2.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/i2.jpg)  
4\. Click Next to start the installation  
5\. Click Finish to complete the installation

How do we verify the installation?  
1\. Validate you have 2 virtual directories installed called RPC and RPC with Cert  
The 2 new virtual directories points to C:\\WINDOWS\\System32\\RpcProxy which is the location of the rpcproxy.dll  
[![](images/v1.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/v1.jpg)[![](images/v2.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/v2.jpg)  
2\. Verify the RPC Proxy server extension is allowed in IIS (this will be enabled after you install the component)  
[![](images/v3.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/v3.jpg)  
Later we will look at a tool called rpc dump that can be used to troubleshoot connectivity problems.

After we have installed our CAS server we need to enable Outlook Anywhere which can be done in 1 of two ways, 1. EMS (command line) or 2. EMC (gui)

**1\. EMS**  
To work with Outlook anywhere via EMS we would use the the following set of commands Get-OutlookAnywhere,Set-OutlookAnywhere,Enable-OutlookAnywhere.

A. Open EMS  
B. Now we will use the Enable-OutlookAnywhere command to enable this feature  
–The following switches are available for the command  
\*\* Pre SP1  
Enable-OutlookAnywhere -DefaultAuthenticationMethod -ExternalHostname -SSLOffloading <$true $false> \[-Confirm \[\]\] \[-DomainController \] \[-Server \] \[-TemplateInstance \] \[-WhatIf \[\]\]  
\*\* Post SP1  
Enable-OutlookAnywhere -ClientAuthenticationMethod -ExternalHostname -SSLOffloading <$true $false> \[-Confirm \[\]\] \[-DomainController \] \[-IISAuthenticationMethods \] \[-Server \] \[-TemplateInstance \]\[-WhatIf \[\]\]

For this demo I used the following command  
\[PS\] C:\\>Enable-OutlookAnywhere -Server vmcashub -SSLOffloading:$false -ExternalHostname vmcashub.vn.local -ClientAuthenticationMethod basic -IISAuthenticationMethods basic  
[![](images/ems-en1.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/ems-en1.jpg)  
\*Note if you use the defaultauthenticationmethod is will override the clientauth and IISAuth \*\*  
\*Setting the ClientAuthMethod is what autodiscover will user to configure the client\*

Enable-OutlookAnywhere  
[http://technet.microsoft.com/en-us/library/bb124993%28EXCHG.80%29.aspx](http://technet.microsoft.com/en-us/library/bb124993%28EXCHG.80%29.aspx)

We can ouse the Get-OutlookAnywhere command to view our configuration  
Get-OutlookAnywhere  
[http://technet.microsoft.com/en-us/library/bb124263%28EXCHG.80%29.aspx](http://technet.microsoft.com/en-us/library/bb124263%28EXCHG.80%29.aspx)

Once we have enable Outlook Anywhere any future modification will be done with the Set-OutlookAnywhere command (i.e. changing authentication)  
Set-OutlookAnywhere [http://technet.microsoft.com/en-us/library/bb123545%28EXCHG.80%29.aspx](http://technet.microsoft.com/en-us/library/bb123545%28EXCHG.80%29.aspx)

**2\. EMC  
**a. Open EMC –> Server configuration –> client Access Server  
b. Select the CAS server you want to enable  
c. Click the button to Enable Outlook Anywhere  
[![](images/emc1.jpg)](http://4.bp.blogspot.com/_jG-efUpJ7Oc/R89DCpxkTbI/AAAAAAAAArU/HIeUkJzdsNU/s1600-h/emc1.jpg)  
d. Enter the External name that clients will use to connect to your Exchange Server, note this name should match the name on your certificate. Select the authentication method of choice  
[![](images/emcbasic.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/emcbasic.jpg)  
e. On the Completion Wizard Click finish  
[![](images/emc2.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/emc2.jpg)  
As you saw there is very little configuration when enabling Outlook Anywhere we have 3 options  
1\. Url 2. authentication and 3. Enable SSL offloading

Once we have Enabled Outlook Anywhere we can validate the registry key has configured correct ports for communication to our mailbox servers. Note only the name listed in the key can be used by clients to connect and you will notice there is no IP address listed so testing via IP will fail through the rpc proxy.

1\. Click start Run  
2\. Regedit – this will open the registry editor  
3\. HKEY\_LOCAL\_MACHINE\\Software\\Microsoft\\Rpc\\RpcProxy  
4\. Notice the Dword called Enabled set to 1  
5\. There is a String value called “ValidPorts”  
VMMBX1**:6001-6002**;VMMBX1:**6004**;vmmbx1.vm.local:**6001-6002**;vmmbx1.vm.local:

**6004**

**[![](images/regedit.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/regedit.jpg)  
\*\*Note if the port are not listed it could take up to 15 minutes to update or you can restart the Microsoft Exchange Service Host \*\*  
we can see that the rpc proxy connects to our mailbox server on the following port 6001-6002 and 6004. Each port is defined below**

Microsoft Exchange Information Store service: **6001  
**referral service of DSProxy: **6002  
**proxy service of DSProxy: **6004**  
Active Directory (if the global catalog server and Exchange Server are on the same server): **6004**

In our client testing we can validate the proxy making connections to our mailbox server with these ports.

**Configure a client:**  
Manually  
1\. Create a New profile  
2\. check the manually configure box at the bottom  
[![](images/11.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/11.jpg)

3\. Select Microsoft Exchange

[![](images/21.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/21.jpg)

4\. Input your mailbox server name (this could be FQDN or Netbios Name)

[![](images/31.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/31.jpg)

5\. Click the “More settings” button

6\. Select the connections tab

[![](images/4.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/4.jpg)

7\. Check the box “Connect to Microsoft Exchange using HTTP” -> Exchange Proxy Settings

[![](images/5.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/5.jpg)

8\. Input the url of your Outlook Anywhere server, check the appropriate authentication

[![](images/6.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/6.jpg)

9\. Click OK and finish the profile  
2\. Autodiscover  
\*\* if autodiscover is not working please refer to my blog on autodiscover \*\*  
[http://exchange-genie.blogspot.com/2007/07/autodiscover-ad-attribute.html](http://exchange-genie.blogspot.com/2007/07/autodiscover-ad-attribute.html)

1\. Click Add  
[![](images/1.jpg)](http://4.bp.blogspot.com/_jG-efUpJ7Oc/R_jQ9ie74hI/AAAAAAAAAuU/Mi1yoHsV5zg/s1600-h/1.jpg)

2\. Give a name for the profile  
[![](images/22.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/22.jpg)

3\. Input the display name and users email address and password  
\*\*Note a domain logged on user will auto populate the information\*\*  
[![](images/32.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/32.jpg)

5\. Logon to your mailbox  
[![](images/41.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/41.jpg)

6\. Click Finish  
[![](images/51.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/51.jpg)  
**Validation:  
**That we have installed all the components we need to do some testing to validate we have access to our mail.

**Check Outlook connection status:**  
1\. Log onto Outlook  
2\. in the System tray hold the CTRL key and right click the Outlook icon  
3\. select connection status  
[![](images/stat1.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/stat1.jpg)

You can see our connection shows https, which validates we are going through the CAS server and proxying our connection.

**Netstat:  
**We can use netstat to show our connection for each hop Client-> CAS -> Mbx -> DC

Open a command windows on the CAS server and type netstat -na  
[![](images/stat2.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/stat2.jpg)

You can see from the screen shot above that our client 192.168.1.5 is making connections are port 443 to our CAS server 192.168.1.101

As noted in the connections window from Outlook you can see that the Outlook client makes multiple connections to the CAS server on port 443 and this is validated in the netstat

CAS -> MBX  
On the mailbox server open a command window and type Netstat -na

The first item to note is our mailbox server listening on ports 6001,6002, and 6004 which is the ports used by rpc/http to make connections  
[![](images/mbxlisten.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/mbxlisten.jpg)

Below you can see our mbx server 192.168.1.102 receiving connections on port 6001 and 6004 from our CAS server 192.168.1.101  
[![](images/cas2mbx600x.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/cas2mbx600x.jpg)

MBX -> DC  
On our domain controller we can see Ldap 389 and GC 3268 ports with connections from both our CAS server and MBX server.  
[![](images/dc2casandmbx.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/dc2casandmbx.jpg)

**Packet Captures:  
**We can use a tool like NetMon or WireShark to perform network captures on each hop as well to validate our traffic between each node. We must note this is encrypted traffic so we will only see sessions between the nodes

This capture is run on the XP client and we can see TLS communication between our client 192.168.1.5 and our CAS 192.168.1.101  
[![](images/client-cas.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/client-cas.jpg)

This capture show communication from the CAS 192.168.101 to the mailbox server on port 6001/6004

See the highlighted section showing a destination port 6001 from the CAS to the MBX server  
[![](images/cas-mbx1.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/cas-mbx1.jpg)

See the highlighted section showing a destination port 6004 from the CAS to the MBX server  
[![](images/6004.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/6004.jpg)

Mailbox Server -> DC/GC  
Below we can see our mailbox server making connections to the DC Ldap port 389  
[![](images/ldap.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/ldap.jpg)

**RPCPing:**

RpcPing is a utility that we can use to troubleshoot or validate that our rpc proxy is working properly.  
Rpc ping is a command line tool that can be found in the Windows 2003 resource kit[http://www.microsoft.com/downloads/details.aspx?FamilyID=9d467a69-57ff-4ae7-96ee-b18c4790cffd&DisplayLang=en](http://www.microsoft.com/downloads/details.aspx?FamilyID=9d467a69-57ff-4ae7-96ee-b18c4790cffd&DisplayLang=en) We can use this tool to test rpc connectivity through an rpc proxy server which is used for Outlook Anywhere.

You can use this MS article to assist with this utility [http://support.microsoft.com/kb/831051](http://support.microsoft.com/kb/831051)

1\. Open a command line to the resource kit directory

[![](images/1.jpg)](http://3.bp.blogspot.com/_jG-efUpJ7Oc/SA6HxRc9fdI/AAAAAAAAAvM/Yv-7YXmEZXU/s1600-h/1.jpg)

2\. Lets connect to port 6001 =store

rpcping -t ncacn\_http -s vmmbx1.vm.local -o RpcProxy=mail.vm.local -P “brian.tirch,vm.local,\*” -I “brian.tirch,vm.local,\*” -H 1 -F 3 -v 3 -B msstd:mail.vm.local -e 6001 -u 10 -a connect

[![](images/23.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/23.jpg)

You can see we make a successful connection  
[![](images/33.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/33.jpg)

3\. Lets connect to port 6004 =DsProxy

rpcping -t ncacn\_http -s vmmbx1.vm.local -o RpcProxy=mail.vm.local -P “brian.tirch,vm.local,\*” -I “brian.tirch,vm.local,\*” -H 1 -F 3 -v 3 -B msstd:mail.vm.local -e 6004 -u 10 -a connect

[![](images/42.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/42.jpg)

You can see we make a successful connection  
[![](images/52.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/52.jpg)

These tests show us that we are properly connecting through the rpc proxy server to the correct ports associated with Outlook Anywhere.

reference the above MS article for a break down of the switches.

**PerfMon:  
**Windows 2008 has added some additional perf counters that we can use with Rpc/Proxy that can assist in identifying connectivity and user load.

[![](images/perf.jpg)](http://nextnextnextfinished.wordpress.com/wp-content/uploads/2011/03/perf.jpg)

**common issues:**  
1\. Certificates – If the client machine does not trust the certificate that is being presented it will fail to connect. So if you are using self signed or self issued certificates you will need to deploy them to each client machine

[http://technet.microsoft.com/en-us/library/bb124149%28EXCHG.80%29.aspx](http://technet.microsoft.com/en-us/library/bb124149%28EXCHG.80%29.aspx)

[http://www.exchange-genie.com/2008/02/configuring-outlook-anywhere-for-exchange-2007-sp1/](http://www.exchange-genie.com/2008/02/configuring-outlook-anywhere-for-exchange-2007-sp1/)
