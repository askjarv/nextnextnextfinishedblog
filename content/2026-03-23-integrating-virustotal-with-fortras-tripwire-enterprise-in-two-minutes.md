---
title: "Integrating VirusTotal with Fortra's Tripwire Enterprise in two minutes"
date: 2026-03-23
categories: 
  - "api"
  - "fim"
  - "scripts"
  - "tripwire"
tags: 
  - "scripting"
  - "tripwire-enterprise"
  - "virustotal"
coverImage: "pexels-photo-3679490.jpeg"
---

One of Tripwire Enterprise's greatest strengths is the ability to quickly and easily take action in response to changes either automatically or during a review by an administrator... and one of the most common requests I see from clients is "how can I know whether this is a good change or a bad change" (which is a far bigger topic than I'll cover here today!). One way to helping answer that question is checking against threat resources - like VirusTotal's excellent API.

Assuming you are running TE on Windows (I'll maybe share the Linux version of this sometime if others are interested!) we know we'll likely want to get at VirusTotal's API in a "Windows'y" way... And, kindly, VirusTotal have shared a solid PowerShell script for checking a hash from the CLI already:

[https://github.com/cbshearer/get-VTFileReport/blob/master/get-VTFileReport.psm1](https://github.com/cbshearer/get-VTFileReport/blob/master/get-VTFileReport.psm1)

```
## Search VirusTotal for a file hash
## Chris Shearer
## 26-Aug-2020
## VirusTotal Public API: https://developers.virustotal.com/reference#file-report

Function get-VTFileReport 
{
    ## Accept CLI parameters
        param ([Parameter(Mandatory=$true)] [array]$h)

    ## Get your own VT API key here: https://www.virustotal.com/gui/join-us
        $VTApiKey = "xxxxxxxxxxxxxx"

    ## Set TLS 1.2
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

    ## Samples
        if ($h) {$samples = $h}
        else {write-host -f magenta "No hash found, exiting."}

    ## Loop through hashes
        foreach ($hash in $samples)
            {
                ## Set sleep value to respect API limits (4/min) - https://developers.virustotal.com/v3.0/reference#public-vs-premium-api
                    if ($samples.count -ge 4) {$sleepTime = 15}
                    else {$sleepTime = 1 }
                
                ## Submit the hash!
                    $VTbody = @{resource = $hash; apikey = $VTApiKey}
                    $VTresult = Invoke-RestMethod -Method GET -Uri 'https://www.virustotal.com/vtapi/v2/file/report' -Body $VTbody

                ## Calculate percentage if there is a result
                    if ($VTresult.positives -ge 1) {
                        $VTpct = (($VTresult.positives) / ($VTresult.total)) * 100
                        $VTpct = [math]::Round($VTpct,2)
                    }
                    else {
                        $VTpct = 0
                    }
                ## Custom Object for data output
                    [PSCustomObject]@{
                        resource    = $VTresult.resource
                        scan_date   = $VTresult.scan_date
                        positives   = $VTresult.positives
                        total       = $VTresult.total
                        permalink   = $VTresult.permalink
                        percent     = $VTpct
                    }
                    
                    Start-Sleep -seconds $sleepTime
             
            }
    }

    Export-ModuleMember -Function get-VTFileReport
```

And from this we can easily build our own Tripwire Execution action... but first, let's do some prep work in TE:

1. First off, we want to create somewhere to store the results so it's easy to access in the UI - I'll use Virus\_Total\_Results\_URL so we can add a link to see the full report - but you can also just capture, say, positives or precents. To do this, it's as simple as going to Settings > Custom Properties > Version Property and clicking "New" and creating a new text variable. I tend to set a default value of "Not Scanned" so it's clear whether or not I've done a scan against a particular file version at any point of time.

3. For authentication, we can use some basic auth for a user account - get your username and password and encoded them as a Base64 for the TE API - i.e. echo -n "username:password" | base64  
    NB: I'd highly suggest giving this user very little access to minimise the risk of reusing the credentials to do anything else!

5. If you've not already done so, you'll want to ensure that you've enable HTTPS access to the TE console from any endpoints you wish to run the action against so they can add results directly to the TE API.

7. Next is the important bit- we'll take the API call for VirusTotal, combine it with the data we've collected from a TE check/change, and pass the results to the TE API... We can start by creating a new Action of the type "Command Execution". For the command itself - we can use:

```
powershell -command "$md5=(Get-FileHash -Path %v -Algorithm MD5).Hash.ToLower(); $vt=Invoke-RestMethod -Method Post -Uri https://www.virustotal.com/vtapi/v2/file/report -Body @{apikey='YOURVISRUSTOTALAPIKEY';resource=$md5}; $url=$vt.permalink; [Net.ServicePointManager]::ServerCertificateValidationCallback={$true}; Invoke-RestMethod -Method Post -Uri https://teconsole.munchkin-justice.ts.net:8443/api/v1/versions/%c/customProperties/VirusTotalResultsURL -Headers @{Authorization='YOURTEAPIKEY';Accept='application/json';'X-Requested-With'='XMLHttpRequest'} -ContentType 'application/json' -Body (@{value=$url} | ConvertTo-Json -Compress)"
```

Since Execution actions are "one liners" it's worth breaking down what this is doing:

- _powershell -command_ tells TE that it should run a PowerShell command (since we use "cmd" as the native Windows shell)

- _$md5=(Get-FileHash -Path %v -Algorithm MD5).Hash.ToLower();_ this line gets us a hash (MD5 in this case) from the element version file path that changed (%v) for us to send to VirusTotal

- _$vt=Invoke-RestMethod -Method Post -Uri https://www.virustotal.com/vtapi/v2/file/report -Body {apikey='YOURVISRUSTOTALAPIKEY';resource=$md5}; $url=$vt.permalink;_ now we can request a report from VirusTotal - we're keeping the permalink returned so we can go straight to the report from TE.

- _\[Net.ServicePointManager\]::ServerCertificateValidationCallback={$true};_ just a bit of cert validation to make sure we're sending data where we think we are!

- _Invoke-RestMethod -Method Post -Uri https://YOURTECONSOLEHOST/api/v1/versions/%c/customProperties/VirusTotalResultsURL -Headers @{Authorization='YOURTEAPIKEY';Accept='application/json';'X-Requested-With'='XMLHttpRequest'} -ContentType 'application/json' -Body (@{value=$url} | ConvertTo-Json -Compress)" :_ finally, we're taking the result and posting it back to the element version id (%c) via TE's API endpoint

We can associate actions with a rule (or a task - though typically rule makes more sense here since we probably don't want to do this for all changed elements)... or we can trigger it directly in the UI by selecting one or more changed elements in the GUI and running the action against them - quick, easy and super useful.
