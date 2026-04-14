---
title: "PDF SPam on the rise- how to filter"
date: 2011-03-03
categories: 
  - "anti-spam"
tags: 
  - "antispam"
  - "mail-filter"
---

PDF Email Spam on the rise

I have been getting lots of emails lately that have most of the time no text whatsoever but a pdf attachment with titles such as report.pdf, article.pdf or bill.pdf. Those are real pdf files and if you open them you see that they contain - you guessed it already didn’t you - spam.

If I want to be a little bit more precise they contain spam about shares and claim that if you buy them you will receive highest returns. The pdf contains normally between three and four pages and only the first page is about the subject that they want you to react on.

The other pages contain random sentences put together to irritate antispam routines and make the pdf look like a new message all the time and not the same. If we put all of this together we see a new type of spam that consists of the following:

1\. Emails with pdf attachments

2\. Random senders

3\. Several names for the pdf files

4\. Sometimes with body

5\. Sometimes with subject

6\. The pdf has several pages

7\. Only the first page is relevant to the spammer and contains stock information

8\. The other pages consist of random sentences to avoid spam filters.

Here is a little trick on how to make Thunderbird’s spam filter recognize the pdf spam and move it right into a special folder:

Method 1:

If you analyze the header of the pdf spam emails you see that most use the User-Agent Thunderbird 1.5.0.12. We will now create a new message filter to move pdf files directly into a newly created folder if the User-Agent is Thunderbird 1.5.0.12.

Click on Tools > Message Filters.

Select a mail account from the list and click on New.

Name the Filter accordingly, something like PDF Spam will do.

Check Match all of the following

Choose Customize from the first pulldown menu

Add “User-Agent”

leave “contains” in the second field

write “Thunderbird 1.5.0.12″ in the last field (without the “”)

Click on the + icon

Choose Body from the pulldown menu

“contains” stays where it is

write “.pdf” in the last field

go to Perform these actions

Select “Move Message to” and choose a folder from the second pulldown menu. You could create a new folder named Spam for instance in Thunderbird.

This message will move all messages that have the User-Agent Thunderbird 1.5.0.12 and a pdf attachment to a folder named spam.

This method is working fine at the moment but will stop working as soon as the spammer is changing the User-Agent of his client.

Method 2:

The following method is also using message filters but works without adding the User-Agent variable which makes it a more general method to fight pdf spam.

Click on Tools > Message Filters.

Select a mail account from the list and click on New.

Name the Filter accordingly, something like PDF Spam 2 will do.

Check Match all of the following

Select “From”

Select “Isn’t in my address book”

Select “Personal address book”

Click on the + icon

Choose Body from the pulldown menu

“contains” stays where it is

write “.pdf” in the last field

Select to move the message again to a newly created folder in Thunderbird.
