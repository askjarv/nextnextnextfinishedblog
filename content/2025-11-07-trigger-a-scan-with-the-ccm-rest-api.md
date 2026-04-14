---
title: "Trigger a scan with the CCM REST API"
date: 2025-11-07
categories: 
  - "ccm"
  - "powershell"
tags: 
  - "tripwire"
---

On the theme of recent posts about scripting (and automating scanning - if you're still doing this manually, you're doing something wrong IMHO!), here's a useful script I put together to help demo how to trigger a compliance scan with Tripwire's Configuration Compliance Manager

```
# Details to connect to CCM server - remember the CCM API must be enabled in the management server XML first
and IIS installed!
$servername = "YOUR-CCM-SERVER"
$RESTAPIUser = "api_account"
$RESTAPIPassword = "api_password"
# Device name you want to scan and scan profile you wish to run
$devicetoscan = "serverMcServer"
$scantoapply = "AdvancedScan"
# Encode credentials to use as part of our header apyload
$baseURL = "https://"+$servername+":443/api/v1"
$Header = @{"Authorization" = "Basic "+[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes
($RESTAPIUser+":"+$RESTAPIPassword)); "Origin" = "https://$servername"}
$Type = "application/json"
# Disable SSL Verification (assuming you don't trust the CCM server
if (-not ([System.Management.Automation.PSTypeName]'ServerCertificateValidationCallback').Type)
 {$certCallback = @"
 using System;
 using System.Net;
 using System.Net.Security;
 using System.Security.Cryptography.X509Certificates;
 public class ServerCertificateValidationCallback
 {public static void Ignore()
 {if(ServicePointManager.ServerCertificateValidationCallback ==null)
 {ServicePointManager.ServerCertificateValidationCallback += delegate
 (Object obj,
 X509Certificate certificate,
 X509Chain chain,
 SslPolicyErrors errors
 )
 {return true;};
 }
 }
 }
 "@
 Add-Type $certCallback
}
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;
[ServerCertificateValidationCallback]::Ignore()
# Get an asset (it's ID and associated network id)
try
 {
 $get_asset_url = $baseurl+"/asset/"
 $assets = Invoke-RestMethod -Uri $get_asset_url -Headers $Header -Method Get -ContentType $Type
 $target_asset_id = $assets | where hostname -eq $devicetoscan | select -ExpandProperty id
 $target_network_id = $assets | where hostname -eq $devicetoscan | select -ExpandProperty networkProfile
| select -ExpandProperty id
 }
Catch
 {$_.Exception.ToString()
 $error[0] | Format-List -Force
 }
# Get a list of scan tasks for the device and then select the required scan
try
 {
 $get_asset_scan_config_Url = $baseurl+"/asset/"+$target_asset_id+"/scantasks"
 $scans = Invoke-RestMethod -Uri $get_asset_scan_config_Url -Headers $Header -Method Get -ContentType $Type
 $scan_to_do = $scans | where name -eq $scantoapply | select -ExpandProperty id
 }
Catch
 {$_.Exception.ToString()
 $error[0] | Format-List -Force
 }
# Post the scan requirement
# First, create our payload for the API:
$body = @{
 asset = @{
 id = $target_asset_id
 };
 networkProfile = @{
 id = $target_network_id
 };
} | ConvertTo-Json
# Try scanning
Try
 {
 $scan_asset = Invoke-RestMethod -Uri "$baseURL/scantask/$scan_to_do/instances" -Headers $Header -Method
Post -ContentType $Type -Body $body
 }
Catch
 {
 $_.Exception.ToString()
 $error[0] | Format-List -Force
 }
```
