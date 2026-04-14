---
title: "Identity is the New OS: Rethinking Security Boundaries in the Cloud"
date: 2026-04-03
categories: 
  - "cloud"
  - "tripwire-enterprise"
tags: 
  - "aws"
  - "azure"
  - "tripwire"
coverImage: "pexels-photo-5561909.jpeg"
---

In traditional infrastructure, the operating system was the security boundary.

- You hardened the OS

- You monitored file integrity

- You controlled access via local users and groups

With the move to cloud platforms like AWS and Azure, that boundary has fundamentally shifted, often making identity the primary control plane. So whilst an EC2 instance or VM can be ephemeral, containers may exist for seconds and serverless functions don’t even expose an OS, it's identity that persists - and IAM **policies** become crown jewels. Tripwire Enterprise has long known that just monitoring files or systems alone isn't enough (hence we've got functionality for auditing traditional identity structures such as Active Directory) - but in a cloud era building rules to monitoring your IAM policies is is important since:

- They define _what is allowed_

- They define _blast radius_

- They define _attack paths_

If an attacker gains access to an overly permissive identity, the OS no longer matters - so let's talk a bit about the whys and hows of monitoring IAM with TE.

* * *

### Why Identity is the New Security Boundary

When I talk about rules in Tripwire, I often want to say _why_ I'm monitoring something first. So let’s translate IAM change monitoring parallels we might want to consider:

| Traditional Risk | Cloud Equivalent |
| --- | --- |
| Root access to server | Admin IAM role |
| SUID binary abuse | Privilege escalation via IAM |
| Weak file permissions | Wildcard IAM policies |
| Local persistence | Token reuse / role chaining |

With the control plane now API-driven, and IAM as the gatekeeper something like this IAM policy

```
{  "Effect": "Allow",  "Action": "*",  "Resource": "*"}
```

becomes

> “root access to the entire cloud estate”

So we'd better make sure that our monitoring is covering _both._

Now most FIM/SCM tooling, including traditional Tripwire deployments, tends to focus on:

- Files

- Registry

- OS configurations

But in cloud environments, the equivalent of `/etc/sudoers` looks more like:

- AWS IAM policies

- Azure RBAC role assignments

- Identity trust relationships

* * *

### Tripwire Enterprise Approach: Treat IAM as Configuration State

Fortunately Tripwire Enterprise is up to the challenge. In fact, it's not massively different from the model we've always used for change detection and policy evaluation - it's just the object that's monitored that changes.

- **Object monitored** ( IAM configuration output )

- **Change detection** ( CLI output comparison )

- **Policy evaluation** ( Regex-based validation )

* * *

## Architecture Overview

[![](images/image-2.png)](https://nextnextnextfinished.wordpress.com/wp-content/uploads/2026/03/image-2.png)

### Flow

1. Tripwire executes CLI commands via:
    - Agent (Linux/Windows)
    
    - Agentless SSH

3. CLI tools (such as AWSCLI or AzureCLI) outputs IAM configuration

5. Output stored as element version

7. Policy tests evaluate:
    - Wildcards
    
    - Escalation paths

9. Pass/Fail recorded in TE

So let's have a look at an approach that could work for AWS.

* * *

### AWS Implementation

#### 1\. A general "Extract IAM Policies Rule" rule

This is a good starting place for change monitoring:

```
aws iam list-policies --scope Local --query 'Policies[].Arn' --output text | tr '\t' '\n' | while read policy; do  aws iam get-policy-version \    --policy-arn "$policy" \    --version-id $(aws iam get-policy --policy-arn "$policy" --query 'Policy.DefaultVersionId' --output text) \    --query 'PolicyVersion.Document' \    --output jsondone
```

#### 2\. Detect Wildcards (PASS/FAIL Output)

Taking it a step further though, we can start building "pass/fail" policy output:

```
aws iam list-policies --scope Local --query 'Policies[].Arn' --output text | tr '\t' '\n' | while read policy; do  doc=$(aws iam get-policy-version \    --policy-arn "$policy" \    --version-id $(aws iam get-policy --policy-arn "$policy" --query 'Policy.DefaultVersionId' --output text) \    --query 'PolicyVersion.Document' \    --output json)  if echo "$doc" | grep -q '"Action": "\*"\|"Resource": "\*"'; then    echo "FAIL | $policy | Wildcard detected in Action or Resource"  else    echo "PASS | $policy | No wildcards detected"  fidone
```

#### 3\. Detect Privilege Escalation Paths

And we can go further for common escalation escalation indicators such as :

- `iam:PassRole`

- `sts:AssumeRole`

- `iam:AttachRolePolicy`

- `iam:PutRolePolicy`

```
ESCALATION_ACTIONS="iam:PassRole|sts:AssumeRole|iam:AttachRolePolicy|iam:PutRolePolicy"aws iam list-policies --scope Local --query 'Policies[].Arn' --output text | tr '\t' '\n' | while read policy; do  doc=$(aws iam get-policy-version \    --policy-arn "$policy" \    --version-id $(aws iam get-policy --policy-arn "$policy" --query 'Policy.DefaultVersionId' --output text) \    --query 'PolicyVersion.Document' \    --output json)  if echo "$doc" | grep -Eiq "$ESCALATION_ACTIONS"; then    echo "FAIL | $policy | Potential privilege escalation permissions detected"  else    echo "PASS | $policy | No escalation paths detected"  fidone
```

* * *

### Azure Implementation

Similar to AWS, we can audit Azure easily with Command Output Capture Rules to:

#### 1\. Extract Role Assignments

```
az role assignment list --all --query '[].{principal:principalName, role:roleDefinitionName, scope:scope}' --output json
```

#### 2\. Detect Wildcard Permissions

Azure wildcards typically appear in custom roles.

```
az role definition list --custom-role-only true --output json | jq -c '.[]' | while read role; do  if echo "$role" | grep -q '"actions":.*"\*"'; then    name=$(echo "$role" | jq -r '.roleName')    echo "FAIL | $name | Wildcard action detected"  else    name=$(echo "$role" | jq -r '.roleName')    echo "PASS | $name | No wildcard actions"  fidone
```

#### 3\. Detect Privilege Escalation Risks

Look for:

- `Microsoft.Authorization/*`

- Role assignment write permissions

```
az role definition list --custom-role-only true --output json | jq -c '.[]' | while read role; do  if echo "$role" | grep -Eiq 'Microsoft.Authorization/roleAssignments/write'; then    name=$(echo "$role" | jq -r '.roleName')    echo "FAIL | $name | Role can assign privileges (escalation risk)"  else    name=$(echo "$role" | jq -r '.roleName')    echo "PASS | $name | No privilege escalation actions"  fidone
```

### Tripwire Enterprise Policy Tests (Regex Examples)

You can map the script output into TE policy tests like:

| Policy Test Name | Regex (PASS condition) |
| --- | --- |
| No wildcard actions | `^PASS \| .* \| No wildcards detected$` |
| No escalation paths | `^PASS \| .* \| No escalation paths detected$` |

### Fail Condition (captured output)

```
^FAIL \| (?<policy>.*?) \| (?<reason>.*)$
```

This allows:

- Reporting by policy

- Clear audit trail

- Direct remediation targeting

* * *

## Why All This Matters

If you only monitor:

- OS drift

- File changes

…but ignore IAM you may end up monitoring symptoms, and not the causes. And remember that attackers don’t need persistence on disk if they can:

- Create new roles

- Assume privileged identities

- Modify policies dynamically

The OS used to be the castle but it's quickly become just a disposable container for many cloud first environments - but to I'm hoping this post highlights how Tripwire doesn't stop at the file system (especially if you're talking with myself or one of the consultancy team!) - IAM is just another audit surface that you can monitor.
