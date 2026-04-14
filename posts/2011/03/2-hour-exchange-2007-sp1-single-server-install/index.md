---
title: "2 Hour Exchange 2007 SP1 Single Server Install"
date: 2011-03-04
categories: 
  - "exchange"
tags: 
  - "exchange-2007"
  - "guide"
  - "install"
---

##### A Newbies Guide to Getting Exchange Configured  
By Ian Matthews, Up & Running Technologies Inc, April 19, 2008   
Last Updated October 1, 2009

You should know four things before you start:

a. I am a definite newbie to Exchange, which is why this I thought I could do a good job creating this documentation for newbies.

b. I am writing this primarily for myself as a cookbook for future Exchange installations.  It is provided WITHOUT WARRENTY OR GUARANTY OF ANY SORT.  USE AT YOUR OWN RISK!

c. It will take longer than two hours to complete because of the delays waiting for your Certificate.  However, the actual work can be completed in the stated time.

d. You need to have a basic knowledge of Windows, Active Directory, and mail servers to get through this.

e. Be sure to check out our page on adding Footers/Disclaimers, Adding Junk Email Retention Policies, Attachment Size Limits, Backup/Restore Exchange 2007, Export to .PST, and use common easy scripts.  All of this and more is on our [**A Newbies Guide to Configuring Exchange - ADVANCED TOPICS**](http://www.commodore.ca/windows/exchange/exchange_2007_advanced_topics.htm)

The idea is to create down and dirty, point form instructions on how to get Exchange 2007 FULLY operational with just two hours of work.  To make this more difficult, I did my install on a Windows Server 2008 64 bit platform but I believe these instructions will function on Vista 64 bit or Server 2003 64 bit.  Yes, 64 Bit is required for Exchange 2007 in production.  The 32 bit version is for test labs only and is NOT supported by Microsoft. 

The other thing I did to make this more realistic, is to name the internal domain something completely different from the email domain (i.e. CORPDOMAIN.LOCAL vs ABCDEDOMAIN.COM). 

Lets get to it.

**A - PREWORK:**

1\. Install Windows 2008 64 Bit on a new box and run Microsoft Update to patch it to whatever is current.

2\. Make sure IPv6 is DISABLED PRIOR to the install of Exchange.  NOTE: Unchecking the IPv6 checkbox on the network card, will not cut it.  See [THIS](http://technet.microsoft.com/en-us/library/cc671176.aspx) and [THIS](http://support.microsoft.com/kb/952842) and [THIS](http://technet.microsoft.com/en-us/library/dd439392.aspx) for details..

3\. If the server is not already a Domain Controller, you need to run DCPROMO to make it so.  Exchange 2007 must be on a network with Active Directory.  DCPROMO will install required DNS for most config's.

4\. There are 4 DNS changes you should make:

o Create your EXTERNAL DNS' MX records for the email domains in question to point to this new Exchange Server's IP Address

o Create an A Record in DNS for AUTODISCOVER.YOURMAILDOMAIN.COM for your servers IP

o Create a REVERSE LOOKUP (RDNS) entry for your Exchange servers IP 

o Create a Sender Policy Framework ([SPF](http://en.wikipedia.org/wiki/Sender_Policy_Framework)) entry for your Exchange servers IP

Note that **only the MX record is required** to get Exchange to function.  The last three are NOT required but you will likley want them so why not do it now?  Also you will have to wait for those settings to replicate throughout the internet (usually 12 hours). 

o For example, if your internal domain is CORPDOMAIN.LOCAL and your email domain is ABCDEDOMAIN.COM, you need to make sure that whoever is hosting the "authoritative DNS" for ABCDEDOMAIN.COM has an MX (i.e Mail Exchanger) record as well as an "A" record for AUTODISCOVER.ABCDEDOMAIN.COM, pointed to your new Exchange servers IP address.

5\. I ran my Server 08 live on the internet, relying solely on its integrated firewall.  This is great for testing because when you install Exchange, it will automatically open required the holes in the firewall.  If you have an external/hardware/real firewall you will need to poke your own holes in it!

**B - EXCHANGE INSTALL:**

1\. Install "Exchange Service Pack 1"

o This is largely a "click next" affair but but it will perform a pile of "preinstallation checks" to make you have the prerequisites; you won't.  So just do exactly what it tells you.  For example it will tell you to install IIS and IIS 6 MANAGEMENT CONSOLE, so do that.  Below are screen shots of my test servers ROLES and also a shot of IIS7 FEATURES.

§ The one additional FEATURE to what is Exchange tells you to do is RPC OVER HTTP.  I will mention it later, so if you don't install it now, don't worry about it

[![clip\_image001](images/clip_image0013.jpg "clip_image001")](http://www.commodore.ca/windows/exchange/server2008_roles_for_exchange_2007.jpg)[![clip\_image002](images/clip_image0024.jpg "clip_image002")](http://www.commodore.ca/windows/exchange/iis7_services_for_exchange.jpg)

o Ignore the following error: (as per [Microsoft article 556055](http://support.microsoft.com/kb/556055))  
Warning: Setup cannot detect an SMTP or Send connector with an address space of '\*'.  
Mail flow to the Internet may not work properly.".

o Service Pack 1 for Exchange is the FULL version of Exchange, not a bunch of new hot fix binary bits and so you can install it directly.  You do not need to install Exchange 07 and then patch it.  If that isn't clear enough know that Windows Server 08 will not let you install the original RTM version of Exchange 2007.

o This process will require at least one reboot after installing pre-req's.

2\. Run Microsoft Update and make sure it includes [Roll Up 1 for SP1](http://www.microsoft.com/Downloads/details.aspx?familyid=C29A6AA8-CA44-43EA-A88F-7500C4BD3D31&displaylang=en) and then reboot.

3\. Users created in ACTIVE DIRECTORY USERS AND COMPUTERS do not have email accounts automatically created for them.  As such you may want to create new users via RECEPIENT CONFIGURATION, NEW MAILBOX.  
[![clip\_image003](images/clip_image0031.jpg "clip_image003")](http://www.commodore.ca/windows/exchange/exchange_2007_new_user.jpg)

4\. From the server surf to [https://127.0.0.1/owa/](https://127.0.0.1/owa/) (this is the **O**utlook **W**eb **A**ccess page) and sign in as ADMINISTRATOR (or the account you created in step 3) to make sure the core is functional then log out.  From a different PC surf to [https://mail.yourdomain.com/owa](https://your) .

o At this point you won't be able to do much other than see that your Exchange is installed properly.

5\. Go to ORGANIZATION CONFIGURATION, HUB TRANSPORT, ACCEPTED DOMAINS, and set the default.

6\. Go to ORGANIZATION CONFIGURATION, HUB TRANSPORT, EMAIL ADDRESS POLICIES and create a entry for your primary domain.

7\. Create a wild card (\*) SEND CONNECTOR (As per Microsoft article [556055](http://support.microsoft.com/kb/556055\)))

8\. Exchange Server 2007 Hub Transport, by default, allow only secure authenticated connections.  If you don't have an Edge server in front of the Hub Transport server (i.e. you are setting up Exchange to function completely from a single server, like we are in this article) , you will need tell Exchange to accept anonymous connections from other mail servers and clients on the web.  
You **cannot** set this change through GUI (only when creating new connectors), so you'll need to open the Exchange Management Shell and enter (just copy and paste this text then go back and edit the <SERVERNAME> :

**_set-ReceiveConnector "Default <Servername>" -permissiongroups:"ExchangeUsers,ExchangeServers,ExchangeLegacyServers,AnonymousUsers"_**

o Be sure sure to get rid of the < and > brackets:

o [http://forums.msexchange.org/m\_1800412705/mpage\_1/key\_/tm.htm](http://forums.msexchange.org/m_1800412705/mpage_1/key_/tm.htm) [http://forums.microsoft.com/TechNet/ShowPost.aspx?PostID=703467&SiteID=17](http://forums.microsoft.com/TechNet/ShowPost.aspx?PostID=703467&SiteID=17)

9\. Surf to the OWA site (i.e. [https://127.0.0.1/owa](https://127.0.0.1/owa)) and send an email to a remote address then reply to that message and make sure you receive it back

**C - OUTLOOK ANYWHERE:**

**Outlook Anywhere, which was named RPC OVER HTTP in Exchange 2003 SP2, is the system that lets you connect Outlook clients to your inhouse Exchange server without first requiring a VPN.  This will be important for your mobile workers.**

1\. If you did not already install RPC OVER HTTP as mentioned in step 1 in the section above, now is the time.   Simply launch Server 2008 Server Manager, click on FEATURES then ADD FEATURE.  When you are done your FEATURES should look like.  
[![clip\_image004](images/clip_image0043.jpg "clip_image004")](http://www.commodore.ca/windows/exchange/server2008_roles_for_exchange_2007.jpg)

2\. SERVER CONFIGURATION, CLIENT ACCESS, OUTLOOK ANYWHERE WIZARD, in the Action Pane on the FAR RIGHT and choose BASIC AUTHENTICATION.  (This is safe because we will encrypt your communications later on in the process.)  
[![clip\_image005](images/clip_image0052.jpg "clip_image005")](http://www.commodore.ca/windows/exchange/outlook_anywhere.jpg)

3\. The following is the hardest part of this whole adventure; buying the certificate!  You need a real cert to allow Outlook clients to connect.  Exchange 2007 uses a new type of cert alternately called a Universal Communications Certificate (UCC) or Subject Alternative Name (SAN) certificate.   All this means is that you can bundle more than one domain name into a single cert. 

o If you don't know what you are doing with certificates or Exchange 2007, [read this](http://www.msexchange.org/articles_tutorials/exchange-server-2007/mobility-client-access/securing-exchange-2007-client-access-server-3rd-party-san-certificate.html) excellent explanation but do NOT carry out the instructions because they skip over the installation of an "Intermediate Certificate" which will be required by most of us.

o From my experience, blog reading and conversations with Microsoft support staff, I suggest you buy your cert from [GoDaddy.com](https://www.godaddy.com/gdshop/ssl/ssl.asp) .  I found GoDaddy's process and seriously cluttered webpages to be quite difficult to follow, but they have three things going for them: they are the second cheapest I can find; they have free dedicated, qualified, SSL PHONE support (480-505-8852); and as an added bonus their certs actually work!   
[![clip\_image006](images/clip_image0062.jpg "clip_image006")](http://www.commodore.ca/windows/exchange/godaddy_ucc_san_cert_for_exchange2007.jpg)  
The biggest question is: What names do you put into this multi-name cert, and here is the answer:

|   Description   |   Example   |
| --- | --- |
|   Mx record   Root domain name   Autodiscover record   Local server FQDN   Server Host Name   |   mail.commodore.ca   commodore.ca   autodiscover.commodore.ca   svr08box.insidecorpdomain.local   svr08box   |

· The next question is: How do I create the Certificate Request (CSR)?  I was going to type the command directly into the Exchange Power Shell (as per the help files) but an MS Exchange Support tech, suggested I use [this site](https://www.digicert.com/easy-csr/exchange2007.htm) to create the command line for me:  
[![clip\_image007](images/clip_image0071.jpg "clip_image007")](http://www.commodore.ca/windows/exchange/digicert_ucc_exchange_2007_csr_generator.jpg)

· As per the DigiCert instructions, just "Click Start > Programs > Microsoft Exchange Server 2007 > Exchange Management Shell Paste the New-ExchangeCertificate command from this page into the Exchange Management Shell window and press Enter Your CSR file should now be in C:\\ on your server (as named by the -Path option in the command itself.)"

· Go to [GoDaddy.com](https://www.godaddy.com/gdshop/ssl/ssl.asp) and spend an hour trying to figure out their pages and processes to submit the CSR and receive the cert.  Note that at the end of their process it says that they have just sent you an email which you are required to open and respond to in order to receive your cert... ya, they haven't.  After three phone calls and 9 hours, my email showed up.

o NOTE: When you are submitting the CSR to GoDaddy, you will be prompted (at the bottom right of the page) to select the type of server this cert will be used on.  Even though Exchange CSR's are not generated using IIS, you must select IIS.

· If you used GoDaddy you will have to install and "Intermediate Certificate"  (also called a "Chained Certificate".  This is an additional step, not covered in most explanations/blogs/help files.  Fortunately it is quite easy to complete:  
[![clip\_image008](images/clip_image008.jpg "clip_image008")](http://www.commodore.ca/windows/exchange/godaddy_intermediate_cert_install.jpg) [![clip\_image009](images/clip_image0091.jpg "clip_image009")](http://www.commodore.ca/windows/exchange/intermediate_certificate_import.JPG)

o **DO NOT** follow the UCC CERTIFICATE INSTALLATION instructions as the end of this screen shot. Just see the next bullet for an easier way.  The text [instructions are here](https://certs.godaddy.com/ExchangeServer_alt.go) and GoDaddy updated their [Exchange cert instructions](http://help.godaddy.com/topic/742/article/4877) in Sept 2009 and they are also now "correct".

· After you get your cert, launch the Exchange Power Shell and type the following to install and enable the cert, in one fell swoop:  
**_Import-ExchangeCertificate –Path c:\\<MYCERT>.p7b | Enable-ExchangeCertificate –Services "SMTP, IMAP, IIS, POP"_**When this is complete run:**_  
**Get-ExchangeCertificate | FL**  
_**and make sure everything looks as you expect

4\. After your UCC Certificate (and any required Intermediate Certificates) are installed, you can try surfing to your Outlook Web Access site [https://mail.yourdomain.com/owa](https://your) and confirm that the UCC  certificate is operational.  
[![clip\_image010](images/clip_image0101.jpg "clip_image010")](http://www.commodore.ca/windows/exchange/owa_exchange_2007_cert.jpg)  
You can also easily check your connectivity using [www.testexchangeconnectivity.com](https://www.testexchangeconnectivity.com/Default.aspx) .

5\. Next you need to configure your Outlook clients.  I used Outlook 2007 exclusively but the process is apparently the same for Outlook 2007 if it has SP2. Start a new Outlook profile and get start a NEW ACCOUNT.  Then there are two ways to finish:

o MANUAL: Choose to manually configure my settings. Select EXCHANGE, type in the external name of your mail server (i.e. mail.commodore.ca ) and your username (i.e. fwillis), click MORE SETTINGS set the PROXY settings to what you see in the screen shot below (obviously adjusting the name for your domain).   
[![clip\_image011](images/clip_image0111.jpg "clip_image011")](http://www.commodore.ca/windows/exchange/outlook_2007_configuration_exchange_2007_using_proxy_.jpg)  
The odd setting is ONLY CONNECT TO SERVERS WITH THE PRINCPLE NAME... and using a setting beginning with msstd://mail.abcdedomaincom  .  On the off chance you care, MSSTD in an acronym for Microsoft Standard Form.  
When you click OK and close the dialog boxes, you will be prompted to sign in and your servername will become underscored.

o AUTODISCOVER:  If you just let Outlook 2007 try to perform an autoconfig, it should create all of the above settings for you (yes, including the proxy).  If your autoconfig is not working, make sure you have a DNS A Record for AUTODISCOVER.YOURMAILDOMAIN.COM.

Thats all folks!  Wasn't that easy and fun for the whole family? 

**D - EXCHANGE ANTISPAM:**

1\. Start Exchange Power Shell, change into the file location where Exchange was installed and then into the SCRIPTS folder.  Then run:  
**_Install-AntispamAgents.ps1_**and restart the MISCROSOFT EXCHANGE TRANSPORT SERVICE.  See [this](http://www.petri.co.il/install-anti-spam-exchange-2007.htm) and [this](http://support.microsoft.com/kb/555924) for more details if you need them.

2\. Go to the ORGANIZATION CONFIGURATION and then HUB TRANSPORT and find the ANTISPAM tab and double click on IP BLOCK LIST PROVIDERS (a.k.a. RBL, Real-Time Blackhole Lists, DNSRBL, Real-Time Block Lists) and add a few such as:  
[![clip\_image012](images/clip_image012.gif "clip_image012")](http://www.commodore.ca/windows/exchange/exchange_2007_antispam_rbl.gif)  
I suggest you also read up on each RBL (like [SpamHaus' ZEN server](http://www.spamhaus.org/zen/index.lasso)) to make sure you understood what it is blocking. 

3\. A few hours later (or the next day) you should check to see if the blocking is doing anything by starting the Exchange Power Shell, change into the file location where Exchange was installed and then into the SCRIPTS folder and running:  
**_get-AntispamTopRBLProviders.ps1_**  and then  **_get-AntispamTopRecipients.ps1  
_**[![clip\_image013](images/clip_image013.gif "clip_image013")](http://www.commodore.ca/windows/exchange/exchange2007_antispam_counts_script.gif)  
You can see from my example that NJABL did not stop a single message after two days of use so I removed it from the IP BLOCK LIST PROVIDERS .  Note that there are many excellent AntiSpam scripts in this folder and you should play with them all.

4\. You should also review the ORGANIZATION CONFIGURATION, HUB TRANSPORT, ANTISPAM, SENDER CONFIDENCE item.  I made no changes to mine and all seems well, but you should understand what it does.

5\. Run Microsoft/Windows Update and notice that there is a EXCHANGE SERVER SPAM DEF'N patch that comes out apparently every day.  I have installed this update on mine server several times now without incident.

6\. If you have more questions about [MS' AntiSpam, this is the offiicial guide](http://technet.microsoft.com/en-us/library/aa996604\(EXCHG.80\).aspx).

I like [Greylisting](http://www.pcmag.com/encyclopedia_term/0,2542,t=greylisting&i=55541,00.asp) to handle spam but I do not use it on Exchange because Exchange 07 does not natively support it and much to my surprise and to Microsoft's credit, I just don't needed it!  If you want Greylisting you need an add-on product and two free ones are recommended (by associates of mine):

1\. [JEPs](http://www.proxmea.com/index.php?q=node/11) which looks pretty damn good to me

2\. [ASSP](http://assp.sourceforge.net/) which I understand to be more complex and requires PERL, but does a good job.

If you like to buy your antispam, [this page](http://www.msexchange.org/articles/Server_Based_Antispam_Comparison.html) provides a nice grid of AntiSpam software options and costs.

**E - POP3:**

On the off chance you care about POP3, follow these three simple steps:

1\. Start the MICROSOFT EXCHANGE POP3 Service on the Server  
[![clip\_image014](images/clip_image0141.jpg "clip_image014")](http://www.commodore.ca/windows/exchange/pop3_services_server.JPG)

2\. If you want to block POP3 users from using "Exchange mail" disable MAPI.  This is step is only required if you want to use the Outlook 2007 AUTOCONFIGURE feature (or you just don't want POP users burning up storage on your server)  
[![clip\_image015](images/clip_image0151.jpg "clip_image015")](http://www.commodore.ca/windows/exchange/disable_exchange_mapi_server.JPG)

3\. If you followed step 2 then when you create a new mail account in Outlook, the autoconfigure will take care of the rest.  If you did not follow step 2, then you will setup the POP account like any other and then go into your Advanced Account Settings and turn on MY OUTGOING SERVER REQUIRES AUTHENTICATION and THIS SERVER REQUIRES ENCRYPTED SSL CONNECTION  
[![clip\_image016](images/clip_image0161.jpg "clip_image016")](http://www.commodore.ca/windows/exchange/smtp_requires_authentication_client.JPG) [![clip\_image017](images/clip_image0171.jpg "clip_image017")](http://www.commodore.ca/windows/exchange/pop3_encrypted_connection_client.JPG)

**F - VERIFICATION:**

After you have everything running to your satisfaction you should run a couple of simple and fast system checks:

1\. In the Exchange Management Console, click TOOLBOX, BEST PRACTICES ANALYZER, approve any updates and checks that it wants to do and then click GO TO WELCOME SCREEN.  Then start a HEALTH CHECK as per the obvious screen shots below.  Be sure to read the results and make whatever changes it suggests.  
[![clip\_image018](images/clip_image018.jpg "clip_image018")](http://www.commodore.ca/windows/exchange/BPA-NewScan.jpg)[![clip\_image019](images/clip_image0191.jpg "clip_image019")](http://www.commodore.ca/windows/exchange/BPA-HealthCheck.jpg)

2\. In the Exchange Management Shell, you should run:  
**_get-OrganizationConfig_**and then you should run:**_  
**Test-SystemHealth**  
_**and make sure everything looks as you expect it should.
