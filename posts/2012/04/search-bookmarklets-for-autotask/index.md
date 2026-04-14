---
title: "Search Bookmarklets for Autotask"
date: 2012-04-04
tags: 
  - "autotask"
---

Hi All,

Not sure if this is off any use to anyone, but I figured I should share the two bookmarklets I've written to make it easier to find tickets and projects in Autotask (**www.autotask.net**):

[AT Ticket Search](https://community.autotask.com/forums/AddPost.aspx?ForumID=12 "TicketSearch") - Searches for the highlighted text in your Autotask ticket list

[AT Project Search](https://community.autotask.com/forums/AddPost.aspx?ForumID=12 "AT Project Search")\- Searches for whatever text is highlighted in your browser against your Autotask Project number list (useful if you have a couple of related projects).

\- just drag and drop the links above into your bookmarks bar and then, when you highlight some text, or a project number in a page, click on the required bookmark to search for the ticket or project number

The actual bookmark  javascript details are below for reference:

Ticket Search: javascript:q = "" + (window.getSelection ? window.getSelection() : document.getSelection ? document.getSelection() : document.selection.createRange().text); if (!q) q = prompt("Search for tickets with the words", ""); if (q!=null) location="[http://ww4.Autotask.net/serviceDesk/TicketsList/search\_requests.asp?TopNavSearch=1&Action=Generate&nc=1&searchtext](http://ww4.autotask.net/serviceDesk/TicketsList/search_requests.asp?TopNavSearch=1&Action=Generate&nc=1&searchtext)\=" + escape(q).replace(/ /g, "+"); void 0

Project Number Search: javascript:q = "" + (window.getSelection ? window.getSelection() : document.getSelection ? document.getSelection() : document.selection.createRange().text); if (!q) q = prompt("Search words", ""); if (q!=null) location="https://ww4.autotask.net/projects/views/listview/projWinBot.asp?projectnumber=" + escape(q).replace(/ /g, "+"); void 0
