---
title: "Sometimes it's the simplest things..."
date: 2011-10-26
categories: 
  - "powershell"
  - "scripts"
  - "windows"
tags: 
  - "citrix"
  - "dos"
  - "for-loop"
  - "script"
  - "uptime"
---

I have been fighting with trying to get a list of my Citrix servers from the command line into a text document for later parsing in a number of other scripts- I quickly found this article - [http://www.brianmadden.com/forums/t/21550.aspx](http://www.brianmadden.com/forums/t/21550.aspx) but try as I might I ran around in circles trying to get it to output correctly - that was when I realised I was being silly and need to use:

[for /f "tokens=1 skip=3" %%i in ('qfarm /load') do echo %%i >> C:\\servers.txt](http://www.brianmadden.com/forums/t/21550.aspx) to pipe EACH LINE when it's ran as a BATCH FILE (not from the command line, which makes it look like it's piping the name AND the name of the output document to the results!).

Simple things, eh.

For the nosy amongst you, I've been using this text file, for, amongst other things, to check some general server stuff which I'll be posting over the next few days- let's start with an easy one- a uptime checker using the list from the batch file above:

```
function WMIDateStringToDate($Bootup) {  

    [System.Management.ManagementDateTimeconverter]::ToDateTime($Bootup)  

}  

 

# Main script  

$Servers = Get-Content "c:\ps\servers.txt" 
Remove-Item c:\ps\uptime.txt

foreach ($Computer in $Servers)

{

$computers = Get-WMIObject -class Win32_OperatingSystem -computer $computer  

 

foreach ($system in $computers) {  

    $Bootup = $system.LastBootUpTime  

    $LastBootUpTime = WMIDateStringToDate($Bootup)  

    $now = Get-Date  

    $Uptime = $now - $lastBootUpTime  

    $d = $Uptime.Days  

    $h = $Uptime.Hours  

    $m = $uptime.Minutes  

    $ms= $uptime.Milliseconds  

 

   $uptimes = "$Computer has been up for: {0} days, {1} hours, {2}.{3} minutes" -f $d,$h,$m,$ms  
#If $d > 7 then
#write-eventlog -logname Application -eventID 6969 -entrytype Information -message "MyApp added a user-requested feature to the display." -category 1 -rawdata 10,20

}   

$output = "c:\ps\uptime.txt"

$Uptimes >>$output

}

$message = New-Object System.Net.Mail.MailMessage –ArgumentList CHudson@dartgroup.co.uk, ("dartusers@bluechip.uk.com,jez.eling@bluechip.uk.com,chudson@dartgroup.co.uk"), 'Citrix Uptime', "Please find attached the Citrix uptime results"
$attachment = New-Object System.Net.Mail.Attachment –ArgumentList c:\ps\uptime.txt, 'text/plain'
$message.Attachments.Add($attachment)
$smtp = New-Object System.Net.Mail.SMTPClient –ArgumentList dgexcas01
$smtp.Send($message)

Remove-Variable  * -Scope Global -ErrorAction SilentlyContinue
```
