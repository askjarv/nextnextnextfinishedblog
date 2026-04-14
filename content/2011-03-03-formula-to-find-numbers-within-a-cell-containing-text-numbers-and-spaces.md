---
title: "Formula to find numbers within a cell containing text, numbers and spaces."
date: 2011-03-03
categories: 
  - "microsoft-office"
tags: 
  - "excel"
  - "formula"
---

I need a formula that will locate only numbers within a text/number cell (i.e. HSS 3x2 11GA) and then use those numbers to calculate certain values.

For example: One cell, A1, has HSS 4x2 11GA, in cell C1 I would like a formula to calculate ((4\*2^3)/32)\*(11/0.5), having found the 4,2 and 11 values from A1. I would also like to click and drag this formula down the C column.

**Answer** You need a VBA User-defined Function. Press Alt/F11, use Insert/Module, copy/paste this in: Function Getno(rg As Range, no As Integer) As Integer temp = rg.Value For i = 1 To Len(temp) ch = Mid(temp, i, 1) Select Case ch Case "0" To "9" Case Else If i = 1 Then temp = " " & Mid(temp, 2) ElseIf i = Len(temp) Then temp = Left(temp, i - 1) & " " Else temp = Left(temp, i - 1) & " " & Mid(temp, i + 1) End If End Select Next Getno = Split(Application.Trim(temp), " ")(no - 1) End Function

Not, go back to the worksheet, and, assuming the text is in A1, enter this in B1: =Getno(A1,1) to get the 1st #, =Getno(A1,2) for the 2nd, etc. So you can use =((getno(A1,1)\*getno(A2,2)^3)/32)\*(getno(A1,3)/0.5)
