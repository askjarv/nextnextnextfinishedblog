---
title: "BT DNS MAIL ROUTING"
date: 2011-03-03
categories: 
  - "exchange"
tags: 
  - "dns"
  - "email"
  - "mail"
---

I have just spent a while sorting out an issue with a customer.

The customer has recently migrated from Nildram over to BT, when they did this they stopped receiving emails from people with BTConnect accounts.

Any one with a BT Connect account would get a NDR similar to below:

Your message did not reach some or all of the intended recipients.

Subject: Test

Sent: 20/01/2011 11:02

The following recipient(s) could not be reached:

[X@X.Co.UK](mailto:X@X.Co.UK) on 20/01/2011 11:02

  The e-mail account does not exist at the organization this message was sent to. Check the e-mail address, or contact the recipient directly to find out the correct address.

  <HESA02UKER.HE.LOCAL #5.1.1>

After an amount of research it became apparent that the issue was not so much with the BTConnect sender as the Domain DNS registration.

This customer has 2, one worked one did not.

A call to BT proved fruitless, but I stumbled across an old email in the clients BTConnect email addy (comes free with the ADSL provision):

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

Subject

Confirmation of your domain zone update

Discussion Thread

Response (Ian Lorimer) 11/17/2010 09:57 AM

Dear X,

Thank you for your email dated 17/11/10 regarding your domain.

As you have pointed the primary MX record on your domain name away from BT's mail server (ibmr.btconnect.com) to [X@x.co.uk](mailto:X@x.co.uk), we have updated the domain name on your account to reflect this.

If you have any further queries please feel free to reply to myself and I will endeavour to find a resolution to your enquiry.

Best Regards,

Ian Lorimer

BT Business Domain Name Services Team

Customer (Change This) 11/17/2010 09:13 AM

BT Domains Centre

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

DEAR X

You have recently changed your zone records for X.X.CO.UK

The new zone record is: -

Type Key Value Priority (MX)

A \* 216.21.224.203

A @ 209.235.144.9

CNAME www web08.rocktime.net

MX @ MAIL.X.Co.UK 5

A mail 81.142.110.252

Best wishes

BT DOMAINS TEAM

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

So I contacted these guys back with the addresses in the mail ([btnamesadmin@btnames.com](mailto:btnamesadmin@btnames.com) & [repoints\_zone\_DNS@btconnect.com](mailto:repoints_zone_DNS@btconnect.com)) and asked them for assistance.  Within an hour the problem was resolved and the issue according to the DNS team is:

Subject      

Confirmation of your domain zone update                     

Discussion Thread    

Response (Ian Lorimer)                 01/20/2011 01:12 PM                  

Dear X,

Your reference number is 101117-000161.

Basically what happens is when a domain name is Transferred into BT it's setup on our internal systems for WEB/MAIL.

When you update the MX records our system has to be up updated to reflect you are using your own Mail Server, and shows as WEB/RELAY.

When the system shows as WEB/MAIL and not WEB/RELAY it causes problems within the BT Network and that was the problem.

Best Regards

Ian Lorimer

BT Domain Name Services Team

Hopefully this information will help with similar issues.
