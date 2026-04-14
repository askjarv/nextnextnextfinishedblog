---
title: "Exchange 2007 - SSL without a UCC Certificate"
date: 2011-03-04
categories: 
  - "exchange"
tags: 
  - "autodiscover"
  - "exchange-2007"
  - "exchange-2010"
  - "ucc"
---

##### I've had this conversation several times recently.  I thought I'd take time to blog about it.  It shouldn't take very long!

**_MYTH: You need to buy a UCC SSL Certificate in order to use Exchange 2007_**

What is a UCC SSL Certificate?  In essence, it is a single certificate that allows multiple common names / domains - different than a "wildcard" certificate where each secured domain has the same root.

Here's what we do, and what I've done for a dozen or more Exchange 2007 installs over the last couple of years.  Three easy steps :)

**_Step 1 - SSL Certificate_**I buy my SSL certificates from [Rapid SSL Online](http://www.rapidsslonline.com/).  Why?  They are rapid, and relatively cheap.  They aren't the cheapest I'm sure, but I can go from CSR to Certificate install in about 3 minutes.  That's rapid and worth it to me.  And, it's less than $20 for an SSL cert.  So, you're gonna follow your "normal" SSL procedures to get a certificate installed on IIS to work with Exchange OWA/Outlook Anywhere/etc. - no, I'm not going to walk you through this.  You can find tons of documentation out there.

Our mail server is SSL secured via the FQDN/CN of "mail01.lifechurch.tv." even though our internal domain is NOT "lifechurch.tv" - it doesn't matter.  SSL Secure yourself based on the FQDN you want your OWA/Outlook Anywhere clients to use.

**_Step 2 - What about Auto Discover?  How do I configure DNS then?_**Well, this is the part that leads to the myth I believe.  Many "early" Exchange 2007 adopters had to use UCC to handle the certificate issues that arose with a DNS "A" record of _autodiscover.domain.com_ - but that is no longer the case, and hasn't been for about two years now.  You can read about it on the [Exchange Team Blog](http://msexchangeteam.com/archive/2007/09/21/447067.aspx) or in the [actual technet whitepaper](http://technet.microsoft.com/en-us/library/bb332063.aspx) from October 2007.

So, what does that mean?  How do I handle autodiscover without UCC?

**_Internal/AD DNS_**I create a DNS SRV record pointing to "mail01.lifechurch.tv" - because that's how my SSL certificate works.  It looks like this:

[![clip\_image002](images/clip_image0025.jpg "clip_image002")](http://www.darylhunter.me/.a/6a00e5500aa93388330120a5722f04970b-pi)

\_.autodiscover.\_tcp.domain.com - for port tcp443 - pointing to mail01.lifechurch.tv

**_External/Public DNS_**  
I create a similar DNS SRV record under the "lifechurch.tv" DNS zone.  I use [DNS Made Easy](http://www.dnsmadeeasy.com/) - it's awesome.  Here's what it looks like:

[![clip\_image004](images/clip_image0044.jpg "clip_image004")](http://www.darylhunter.me/.a/6a00e5500aa93388330120a5c8c68c970c-pi)

Look familiar?  It's identical to the one above it.

**_Step 3 - DNS Doctoring/Rewriting_**  
This is where you may run into problems.  I use a Cisco ASA Cluster for my firewall.  When I create my NAT entries, I have the opportunity to rewrite the DNS resolution.  Let me explain.

From my house, if I ping mail01.lifechurch.tv - I get a public 12.x.x.x address.

From inside my network, behind my firewall using DNS Doctoring - I get a 10.x.x.x address.  I'm not using split brain DNS.  I'm using DNS Made Easy.  The Cisco ASA rewrites that.  All it takes is a single firewall command.

static (Inside,Outside) 12.x.x.x 10.x.x.x 255.255.255.255 dns

That's it.  That static NAT entry, combined with the "dns" attribute, will handle the rewrite for me.

I know some of you may be using Microsoft ISA, or Sonicwall, or other firewalls.  I'm not sure if they will handle this rewrite for you.  I've heard of people using host files to handle that, and that may work for you.  But, for Cisco firewalls, it's a single command - built-in functionality.

Anyway, that's that for today's episode of Exchange 2007 UCC/SSL MYTH-busters :)
