---
title: "File Integrity Monitoring - Handling Unexpected Changes"
date: 2015-01-03
categories: 
  - "fim"
tags: 
  - "process"
  - "security"
---

With last year's security breaches reaching new heights in the general media, security of IT assets has never been more important. Many of you will know I've recently moved into an IT consultancy role in the security sector, and I wanted to start a series on various security processes that can be adopted to improve your security profile.

File Integrity Monitoring is a key part of most good security practices - but how do you manage FIM? From scripts that notify on critical file changes to full product suites dedicated to FIM and on to data leak protection products, there's various tools that will enable you to achieve FIM but few businesses share their practices for how best to manage the products once they're in place - so just what should you do when your FIM product highlights a change - and just how robust a process do you have around your FIM alerts?

Of course, there's no one system fits all - customisation to your business needs is essential, but at it's most basic you'll have:

- Alert
- Assessment
- Response

Each of these can phases can be further broken down and additional steps and processes and documentation added to give you a robust system - consideration might need to be given, for example, to when alerts should be generated (priorities, owner of the system, etc), to whom should the alert be sent, and by what means (email, SMS, IM could all be used, and in each case you may want to have resiliency).

So rather than get bogged down in ALL the possible customisations for now, let's take a look an example workflow which I've proposed to a client recently - I won't use anything product specific, so it's easy to adapt to your own needs with some minor changes depending on your logging tool - and may even make you think about how to enhance or customise your logging in the future:

- Initial Detection: Unexpected Change detected. Email notification generation.
- Initial Assessment: Assessment of initial Information captured by FIM product (Timestamp, Owner, File Path, File Contents (if applicable)). If unidentified proceed to secondary analysis, otherwise go to step 7.
- Detailed Data Capture: Add additional data if possible from Tripwire Enterprise by expanding the monitored path, monitored elements (hash, etc) to get a better picture of the source of the change.
- Security Analysis: initial threat verification achieved through AV scans, etc.
- Application Assessment: Use other tools to identify the associated application (SysInternals, etc) to evaluate the
    1. Source Application (what application triggers the change)
    2. Source Application Event (what EVENT within the application triggers the change)
    3. Exception scenarios (in what cases that the exception doesn’t occur).
- Vendor engagement (if file generation is classified as a bug, or errant/unexplainable behaviour and deemed to be sufficiently undesirable)
- Revaluation and rule tuning/configuration as required.

As you can see, even a basic workflow should include detailed assessment and response steps- I'll go on into greater depth on each of these in a future post.
