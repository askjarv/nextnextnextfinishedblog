---
title: "little known Clariion facts and trivia :-)"
date: 2011-03-03
categories: 
  - "emc"
tags: 
  - "san"
---

You may know this already but I was chatting with an EMC engineer this morning and he gave me some details which are quite useful.  Apparently, there are specific, hard set IP settings on all CX3’s and CX4’s which provide back door access methods for EMC engineers only. 

These are:

SPA – 128.221.1.250

SPB – 128.221.1.251

Subnet Mask – 255.255.255.248

Set your laptop to 128.221.1.249

You can get in there and have full access to change or recover unknown/lost settings.

Also, connecting with a console cable and connecting to [http://192.168.1.1/setup](http://192.168.1.1/setup) will take you to a menu where you can apparently see all network settings, do resets and recovery of admin details, etc.

CTRL-SHIFT-F12 allows you to enter Engineering Mode, and the password is “**messner**”

Why messner? [http://spiralbound.net/blog/2007/10/17/little-known-clariion-facts-and-trivia](http://spiralbound.net/blog/2007/10/17/little-known-clariion-facts-and-trivia)

Enjoy!
