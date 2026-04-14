---
title: "TE Rules for Multi-registry based checks"
tags: 
  - "policy-compliance"
  - "powershell"
  - "tripwire-enterprise"
draft: true
---

A common request I come across is that users want to evaluate _all_ values are present in a Tripwire Enterprise Policy test, but no additional "bad" values in TE registry checks (SNMP server lists, or TLS settings, etc). Given that TE's policy engine isn't very good at this, I figured I'd share the COCR Script I'm tending to use these days along with a simple "does not contain" WARN type policy test

```
# For a given key path, enumerate all values and their data, then check if they match the $approved IPS array, and if one is missing or not approved, write a warning to the console.$KeyPath = "HKCU:\MyKey"$approvedIPs = @("192.168.1.1", "127.0.0.1")$foundIPs = @()Function Get-RegistryKeyPropertiesAndValues {Param([Parameter(Mandatory = $true)][string]$path)Push-LocationSet-Location -Path $pathGet-Item . |Select-Object -ExpandProperty property |ForEach-Object {New-Object psobject -Property @{“property” = $_;“Value” = (Get-ItemProperty -Path . -Name $_).$_} }Pop-Location}$KeysToAssess = Get-RegistryKeyPropertiesAndValues -path $KeyPath$KeysToAssess | ForEach-Object {# Check if the value is an approved IP$Value = $_.Value$Key = $_.propertyif ($approvedIPs -notcontains $_.Value) {Write-Host "$Value (in $Key) is not an approved IP address" -ForegroundColor Red}else {# Add to the list of found IPsWrite-host "$Value (in $Key) is an approved IP address" -ForegroundColor Green$foundIPs = $foundIPs + $_.Value}}Check if any approved IPs are missing$approvedIPs | ForEach-Object {if ($foundIPs -notcontains $_) {Write-Host "Warning: $_ is missing from the registry" -ForegroundColor Red}}
```
