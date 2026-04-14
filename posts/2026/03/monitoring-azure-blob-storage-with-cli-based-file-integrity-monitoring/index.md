---
title: "Monitoring Azure Blob Storage with CLI-Based File Integrity Monitoring"
date: 2026-03-31
categories: 
  - "fim"
  - "tripwire-enterprise"
tags: 
  - "azure"
  - "tripwire"
coverImage: "pexels-photo-4170172.jpeg"
---

Continuing my previous post about cloud storage monitoring, I'm back with the "Azure edition" today. I'll skip the preamble about why this is important and get straight to the commands this time (but stay tuned about some additional considerations that are relevant to both AWS and Azure):

## Prerequisites

Install and authenticate Azure CLI:

```
az login
```

Ensure access to:

- Storage accounts

- Containers

- Role assignments (if required)

* * *

## Core Azure Storage Checks

### List Storage Accounts

```
az storage account list --output json
```

* * *

### Check Secure Transfer Requirement

```
az storage account show \  --name mystorageaccount \  --resource-group myrg \  --query "enableHttpsTrafficOnly"
```

* * *

### Blob Service Properties

```
az storage account blob-service-properties show \  --account-name mystorageaccount \  --output json
```

* * *

### Container Access Level

```
az storage container show \  --name mycontainer \  --account-name mystorageaccount \  --auth-mode login \  --output json
```

* * *

### Encryption Settings

```
az storage account show \  --name mystorageaccount \  --query "encryption"
```

* * *

### Network Rules

```
az storage account network-rule list \  --account-name mystorageaccount \  --resource-group myrg \  --output json
```

* * *

### Key Design Considerations (for both Azure and AWS!)

Plan your commands and verify your output - to be effective you're going to want to work out how to make these useful change indicators... so when using commands like these you'll want to:

### 1\. Normalize Output

- Prefer `--output json` or output formats that lend themselves to "one change per line" (fortunately TE's change viewer gives you good context for changes when using the difference viewer)

- Strip timestamps if present so you're not just logging a timestamp being present (I'd blog about useful regex for filters here, but I'm confident anyone can find some solid regex's for date/timestamp formats these days!)

* * *

### 2\. Scope Carefully

Avoid brute-force scanning all buckets/accounts every run if it's not necessary. Instead:

- Tag or label monitored resources that make sense to monitor for your goals - just as with traditional file monitoring, less is often more!

- Maintain a scoped inventory list - use TE's reporting (such as Change Audit Coverage) to help here too!

- Iterate deterministically

* * *

### 3\. Handle Missing Configurations

Some APIs return errors if a feature is not enabled - e.g.

```
An error occurred (ServerSideEncryptionConfigurationNotFoundError)
```

This **is itself a signal** and should be captured but consider how you report on these - perhaps respond to .\*error.\* content with actions that alert the appropriate people.

* * *

### 4\. Cross-Cloud Consistency

You’ll notice strong parallels:

| Control | AWS S3 | Azure Blob |
| --- | --- | --- |
| Encryption | SSE-S3 / KMS | Storage Service Encryption |
| Public Access | ACL / Policy | Container access level |
| Network Restriction | Bucket policy / VPC | Network rules |
| Logging | Access logging | Diagnostic settings |

This allows you to build **portable monitoring patterns -** not just one off approaches.

* * *

### "Files" aren't just on your file system

This whole approach is all about making your monitoring work beyond your disks:

- Monitoring **non-agent systems** is important - but having a consistent approach if you've got a hybrid setup is important (especially when it comes to audit season, as well as helping to avoid "tool overload")

- Capturing **cloud-native drift** isn't difficult - it could be a dozen or so simple rules that get you from no visibility to deep knowledge in an afternoon.

- Extending FIM into **control plane configuration** makes sense - especially when it means you get to keep the same reports for your more traditional, on-prem platforms and correlate changes across platforms/vendors.

- Creating **auditable baselines across cloud providers** by leveraging platform agnostic options (like TE!).
