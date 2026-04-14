---
title: "Excel IP to Sortable Number function"
date: 2011-03-03
categories: 
  - "microsoft-office"
tags: 
  - "excel"
  - "formula"
---

Excel formula to allow formatting IP’s in such away that will allow you to sort numerically:

 

\=((VALUE(LEFT(C2, FIND(".", C2)-1)))\*256^3)+((VALUE(MID(C2, FIND(".", C2)+1, FIND(".", C2, FIND(".", C2)+1)-FIND(".", C2)-1)))\*256^2)+((VALUE(MID(C2, FIND(".", C2, FIND(".", C2)+1)+1, FIND(".", C2, FIND(".", C2, FIND(".", C2)+1)+1)-FIND(".", C2, FIND(".", C2)+1)-1)))\*256)+(VALUE(RIGHT(C2, LEN(C2)-FIND(".", C2, FIND(".", C2, FIND(".", C2)+1)+1))))
