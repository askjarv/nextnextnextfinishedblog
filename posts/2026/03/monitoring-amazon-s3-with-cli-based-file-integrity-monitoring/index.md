---
title: "Monitoring Amazon S3 with CLI-Based File Integrity Monitoring"
date: 2026-03-27
categories: 
  - "cloud"
  - "fim"
  - "tripwire-enterprise"
tags: 
  - "aws"
  - "s3"
  - "tripwire"
coverImage: "pexels-photo-6169029.jpeg"
---

Cloud object storage introduces a subtle but critical challenge for File Integrity Monitoring (FIM):  
there is no “file system” in the traditional sense. But that doesn't mean you shouldn't be monitoring it (given it's even more exposed than your on-premise architecture in many cases, I'd argue, you actually be monitoring it _more_) and it definitely doesn't mean that you can't be effective using Tripwire Enterprise to monitor it.

This post outlines a pragmatic approach to monitoring **Amazon S3** and **Azure Blob Storage** using:

- **AWS CLI**

- **Azure CLI**

- Structured command outputs suitable for ingestion into a FIM platform (i.e. Tripwire Enterprise!)

### Why CLI-Based Monitoring Works Well

First off, this is a chance for me to remind everyone that Tripwire Enterprise's flexibility really shines through because of our Command Output Capture Rules - rules that let you capture the output of a command or a script and use it to determine if anything has changed.

Using CLI commands as a data source provides:

- Deterministic, scriptable outputs - easy to test outside of TE, then deploy directly (and benefit from TE's own rule monitoring so you know when a rule's script configuration has been changed)

- No reliance on cloud-native alerting pipelines - reducing the risk of accidental (or deliberate) tampering

- Cross-cloud consistency in approach - ensuring that if you're multi-platform, you remain covered.

### Architecture Overview

At a high level, here's how this type of monitoring works

- A designated "collection" **node** executes CLI commands using Tripwire Enterprise's rules (defining what you're capturing for monitoring) and tasks (defining when the node gathers your monitoring info)

- **Outputs** are captured (I tend to prefer JSON here, as it's easier to do side-by-side comparisons in TE, as well as to process with policies (though, I will concede, that might be because I've never come to love xpath which TE is quite happy with too!))

- **Drift** is detected via comparison of the outputs over multiple **check tasks** (/time)

This is works especially well where:

- You need **vendor-agnostic monitoring patterns**

- Native cloud logging is inconsistent

- You want **centralised compliance visibility**

## Monitoring Amazon S3

### Prerequisites

Install and configure the AWS CLI on your collection node:

```
aws configure
```

Ensure the IAM identity has at least:

- `s3:ListBucket`

- `s3:GetBucketPolicy`

- `s3:GetBucketAcl`

- `s3:GetBucketEncryption`

- `s3:GetPublicAccessBlock`

- `s3:GetBucketVersioning`

and that you have suitable network access in place.

### AWS S3 Monitoring CLI Rules

Starting with some basics - detecting your buckets:

aws s3api list-buckets --output json

This is helpful, even if you're creating buckets regularly, since you can supress alerts (setting severity to zero) but use it to correlate other changes (i.e. new bucket = new permission set)

#### Public Access Block for all buckets

OK, a simple but important one next - checking public access - since we want to do this for all buckets, rather than just one, we're into the world of scripted command output capture rules (rather than one liners) and, as a result, we may need to use a different syntax if our collection node is Windows (PowerShell) or Linux (Bash) - so here's both

```
#!/usr/bin/env bash
set -u
for BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=public-access-block ==="
  aws s3api get-public-access-block --bucket "$BUCKET" --output json 2>&1
  echo
done
```

Or PowerShell:

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"
foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=public-access-block ==="
    aws s3api get-public-access-block --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

#### Bucket encryption for all buckets

Encryption is key! So here's the Bash and PowerShell versions

```
#!/usr/bin/env bash
set -u

for BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=encryption ==="
  aws s3api get-bucket-encryption --bucket "$BUCKET" --output json 2>&1
  echo
done
```

or

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"

foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=encryption ==="
    aws s3api get-bucket-encryption --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

#### Bucket versioning

```
#!/usr/bin/env bash
set -u

for BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=versioning ==="
  aws s3api get-bucket-versioning --bucket "$BUCKET" --output json 2>&1
  echo
done
```

or powershell

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"

foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=versioning ==="
    aws s3api get-bucket-versioning --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

#### Bucket logging

Bash

```
#!/usr/bin/env bash
set -ufor BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=logging ==="
  aws s3api get-bucket-logging --bucket "$BUCKET" --output json 2>&1
  echo
done
```

PowerShell

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=logging ==="
    aws s3api get-bucket-logging --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

#### Bucket ACL for all buckets

Bash version:

```
#!/usr/bin/env bash
set -ufor BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=acl ==="
  aws s3api get-bucket-acl --bucket "$BUCKET" --output json 2>&1
  echo
done
```

PowerShell

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=acl ==="
    aws s3api get-bucket-acl --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

#### Bucket policy for all buckets

Bash

```
#!/usr/bin/env bash
set -ufor BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=policy ==="
  aws s3api get-bucket-policy --bucket "$BUCKET" --output json 2>&1
  echo
done
```

PowerShell

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=policy ==="
    aws s3api get-bucket-policy --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

#### Bucket policy status for all buckets

This can be useful if you want to identify whether a bucket is considered publicly accessible by policy evaluation.

Bash

```
#!/usr/bin/env bash
set -ufor BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=policy-status ==="
  aws s3api get-bucket-policy-status --bucket "$BUCKET" --output json 2>&1
  echo
done
```

PowerShell

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=policy-status ==="
    aws s3api get-bucket-policy-status --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

* * *

#### Bucket ownership controls for all buckets

This is a good modern check for S3, especially where ACL usage should be constrained.

Bash

```
#!/usr/bin/env bash
set -ufor BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=ownership-controls ==="
  aws s3api get-bucket-ownership-controls --bucket "$BUCKET" --output json 2>&1
  echo
done
```

PowerShell

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=ownership-controls ==="
    aws s3api get-bucket-ownership-controls --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

* * *

#### Bucket website configuration for all buckets

This is useful because accidental or unauthorised static website exposure can matter.

Bash

```
#!/usr/bin/env bash
set -ufor BUCKET in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do
  echo "=== bucket=$BUCKET check=website ==="
  aws s3api get-bucket-website --bucket "$BUCKET" --output json 2>&1
  echo
done
```

PowerShell

```
$Buckets = (aws s3api list-buckets --query "Buckets[].Name" --output text 2>&1) -split "`t"foreach ($Bucket in $Buckets) {
    Write-Output "=== bucket=$Bucket check=website ==="
    aws s3api get-bucket-website --bucket $Bucket --output json 2>&1
    Write-Output ""
}
```

I'll be back again soon with some options for Azure CLI!
