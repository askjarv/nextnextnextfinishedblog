---
title: "Blackberry Express Gone - ActiveSync for all those who don't want to spend more money"
date: 2013-03-01
tags: 
  - "bes"
  - "bes-express"
  - "blackberry"
  - "blackberry-10"
  - "blackberry-os-10"
---

I've been working with my first client migrating to Blackberry OS 10 and I'll admit to getting a warm and fuzzy feeling knowing that they finally support ActiveSync- what I hadn't realised, as this customer was an existing BES Express user, was that BES Express is no longer supported (you must upgrade to the latest version of Enterprise server, which no longer includes a free version (beyond a 60 day trial))- alongside some other interesting caveats:

- > For enterprise mobile device management, BlackBerry 10 devices will require the new BlackBerry Enterprise Server 10 (BES 10).
    
- > BES 10 is not backwards compatible with existing BlackBerry phones, so companies transitioning to BlackBerry 10 will have to run legacy BES 5 and BES 10 servers in parallel during the changeover.
    
- > To simplify this setup for administrators, BES 10 will feature a unified console that can manage existing BES 5 servers.
    
- > BES 5 is a mature product - while new feature development will cease beyond version 5.04, support for BES 5 in enterprise will continue for years to come.
    
- > BES 10, which is an extension of RIM's existing [Mobile Fusion](http://crackberry.com/tags/mobile-fusion "Mobile Fusion") solution, can also manage Android and iOS devices allowing administrators to manage all of an enterprise's mobile devices within one dashboard.
    
- > For individuals and "bring your own device" users, Blackberry 10 can sync directly using ActiveSync (Exchange, Gmail), for email, calendar, and contacts, without the need for BES 10.
    

> http://crackberry.com/clearing-confusion-bes-and-blackberry-10

(also worth a read is: http://uk.blackberry.com/content/dam/blackBerry/pdf/BlackBerry\_Enterprise\_Service\_10\_FAQ.pdf)

What this also means is that ActiveSync is "self managed" rather than centrally managed, and puts it (as far as I can see) into the "personal hub" rather than the "business hub"- which is a bit of a PITA for those with OCD and desire to actually use the devices as you'd expect (I'd say at least a good 80% of Active Sync setups are not personal!).

To rub salt in the wound, moving a user across I also came across a weird quirk - contacts not syncing correctly. This article here suggests a possible cause and workaround: http://btsc.webapps.blackberry.com/btsc/viewdocument.do?noCount=true&externalId=KB33578.

In the end, I had to do a quick backup from the original device, then use MagicBerry (http://menastep.com/pages/magicberry.php) to convert the BBB backup file into a IPD list from which I could then use the Contracts Extractor here: https://sourceforge.net/projects/bb-contact-extr/  to extract them into a document I could then import into Outlook (phew!). A bit of a gotcha.

None of this was helped by a further issue where some unusual field choices meant that some contacts (created on an old Blackberry Torch) meant that phone numbers that appeared as clear as day on the original device would not show up (with the number in place) on the new device once copied across (and that was without using the crazy import process noted above)!

Ah well, these things are sent to test us!
