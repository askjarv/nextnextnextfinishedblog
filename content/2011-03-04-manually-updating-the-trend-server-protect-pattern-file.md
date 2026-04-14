---
title: "Manually updating the Trend Server-protect pattern file"
date: 2011-03-04
categories: 
  - "trend"
tags: 
  - "pattern-file"
  - "serverprotect"
---

Manual update the pattern file using this procedure:

1\. Download the [latest Official Pattern Release (OPR)/Controlled Pattern Release (CPR)](http://www.trendmicro.com/download/pattern-cpr-disclaimer.asp). The pattern file will have two values.

o The standard pattern number (XXX)

o The new pattern file numbering format (W.XXX.YY). W represents the generation number, XXX represents the actual pattern file number and YY represents the pattern file build number or control release. For more information, visit the [NPF Web site](http://www.trendmicro.com/npf).

2\. On the Information Server, save the pattern file (you downloaded from the Web site) as vsapiXXX.zip (where XXX is the pattern file number you are downloading) to the \\…\\SpntShare\\Pattern directory. (e.g., C:\\Program Files\\Trend\\Sprotect\\SpntShare\\Pattern).

3\. On the ServerProtect Information Server, open the server.ini file in the \\Program Files\\Trend\\Sprotect\\SpntShare directory.

4\. Under the \[PATTERN\] section, change the MergeCount and P.4.MergeCount values to have a value equal to zero (0).

5\. Change the Version value to equal the current pattern file number you downloaded from Step 2.

6\. Change the P.4. value so that it reflects the correct pattern file number you are updating (i.e., \\pattern\\vsapiXXX.zip), the correct name for new pattern file format, and the correct size of the zip file. The line should look like the following:

P.4=pattern/vsapiXXX,zip, WXXXYY, ZZZZZZZ  
Where

§ W is the pattern generation number

§ XXX is the pattern file number

§ YY is the current pattern file release version

§ ZZZZZZZ is the size of the zip file. This is the Size value and not the Size on disk value.

7\. Change the Path\_VSAPI value so that it reflects the correct pattern file number you are updating (\\pattern\\vsapiXXX.zip) and the correct size of the ZIP file. The line should look like this:

Path\_VSAPI=pattern/vsapiXXX.zip, ZZZZZZZ  
Where

§ XXX is the pattern file number

§ ZZZZZZZ is the size of the ZIP file. This is the Size value and not the Size on disk value.

8\. Save the changes you have made to the server.ini file.

9\. Open the ServerProtect Management Console and click the **Do** >**Update menu items** to view the new pattern file information.

At this point, the ServerProtect Information Server can perform a pattern deployment to all Normal Server(s) using the Deploy Now method or the Deploy Task method.

Taken from: [http://esupport.trendmicro.com/Pages/Manually-updating-the-pattern-file-on-ServerProtect-for-NT-5.58.aspx](http://esupport.trendmicro.com/Pages/Manually-updating-the-pattern-file-on-ServerProtect-for-NT-5.58.aspx)
