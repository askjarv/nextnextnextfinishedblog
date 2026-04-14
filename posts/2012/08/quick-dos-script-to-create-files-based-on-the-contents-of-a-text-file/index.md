---
title: "Quick DOS script to create files based on the contents of a text file"
date: 2012-08-09
categories: 
  - "scripts"
tags: 
  - "dos"
  - "text"
---

There's plenty of times where I find myself thinking that there must be an easy way of doing a dull and repetive task- for example, creating a bunch of files based on a CSV file - so the line below will simply take a text document (x.txt) and create new files with the contents of each line in the document in the same directory with the same name:

> for /f "tokens=\*" %l in (x.txt) do @type nul > "%l.txt"
