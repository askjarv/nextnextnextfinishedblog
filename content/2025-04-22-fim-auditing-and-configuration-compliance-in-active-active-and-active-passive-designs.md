---
title: "FIM, Auditing, and Configuration Compliance in Active-Active and Active-Passive Designs"
date: 2025-04-22
tags: 
  - "tripwire"
---

In a lot of environments I walk into, clustering is treated as a resilience problem - but not always as a security one. We're busy designing for uptime, failover, scale, etc... but we don’t always design for _consistency of trust_ across the cluster (especially for on premise deployments where there's a lot more variables at play in my experience). In doing so we, we expose ourselves to risk

* * *

## The Misconception

There’s a common assumption:

- **Active-active clusters**: “everything is live, so everything must be secured”

- **Active-passive clusters**: “only the active node matters right now”

That second assumption is where risk creeps in because, from a security standpoint, a passive node is not inactive - it’s just "waiting". Waiting to take over your production traffic, to execute the same critical workloads you were running before seamlessly, to become the new “trusted” state (a term we use a lot with Tripwire Enterprise and change monitoring.

That why if your passive infrastructure is not continuously monitored and validated (consistently and alongside your active nodes), you’ve effectively built a pre-positioned attack vector into your architecture (and one that will often expose you to the most risk when you're already potentially fighting another fire that started a failover too).

* * *

## The Real Risk: Drift + Failover = Exposure

In real terms, you want to consider what happens during a failover to justify your monitoring stance:

### The Scenario: Active-Passive Cluster Failover

- Node A (active) is hardened, monitored, compliant

- Node B (passive) is:
    - Missing patches
    
    - Has config drift
    
    - Has unauthorised changes (or worse, persistence mechanisms)

Everything looks fine… until failover.

Now Node B becomes active.

And suddenly:

- Your compliance posture changes instantly

- Your monitoring baselines are invalid

- Potentially compromised state becomes production reality

This is not theoretical - this is a common failure mode I see a lot of the time in the real world.

* * *

## Why FIM and Auditing Must Be Cluster-Wide

### 1\. Trust Must Be Symmetrical

Clusters are built on the assumption of **equivalence between nodes**.

If Node B cannot be trusted to behave identically to Node A:

- Your failover is not safe

- Your resilience is compromised

- Your security model is inconsistent

**FIM (File Integrity Monitoring)** ensures:

- Critical binaries, configs, and system files remain consistent

- Drift is detected _before_ failover happens

* * *

### 2\. Drift Doesn’t Care About Node State

Configuration drift occurs regardless of:

- Node role (active/passive)

- Workload assignment

- Traffic patterns

Common causes:

- Manual changes during maintenance

- Automation gaps

- Patch inconsistencies

- “temporary” fixes that become permanent

Without continuous monitoring:

- Passive nodes silently diverge

- Baselines become meaningless

* * *

### 3\. Attackers Target the Quiet Parts of Your Estate

If I were attacking your environment, I wouldn’t go for the most monitored system.

I’d go for:

- The standby node

- The DR environment

- The “not currently in use” infrastructure

Why?

Because:

- It’s often less monitored

- Changes go unnoticed

- It provides a clean pivot point into production

A compromised passive node is effectively a time-delayed breach. And it's not just me - compromised backup infrastructure has become an increasingly common attack vector and we need to remember that the backup of your crown jewels is, in effect, just a set of crown jewels.

* * *

### 4\. Compliance Doesn’t Pause for Failover

From an audit and regulatory standpoint:

There is no distinction between:

- “active system”

- “standby system”

If it can process production workloads, it must:

- Meet configuration standards

- Be continuously audited

- Provide evidential integrity

Otherwise, you end up in a position where:

- You pass audits during normal operation

- You fail them the moment failover occurs

* * *

## Active-Active Isn’t Immune Either

It’s tempting to assume active-active setups are safer because everything is “live”.

But the same issues apply:

- Nodes can still drift independently

- Load distribution can mask inconsistent states

- Partial compromise can spread laterally

Without FIM and configuration compliance:

- You lose the guarantee that nodes are equivalent

- You risk inconsistent behaviour under load

- You introduce non-deterministic failure modes

* * *

## What “Good” Looks Like

A properly secured cluster treats **every node as production-ready at all times**.

### Minimum baseline:

- **FIM applied to all nodes**
    - Critical OS paths
    
    - Application configs
    
    - Cluster configuration files

- **Continuous auditing**
    - Not scheduled “once a day” checks
    
    - Near real-time or frequent validation

- **Configuration compliance enforcement**
    - CIS / internal hardening baselines
    
    - Drift detection + remediation workflows

- **Consistent policy application**
    - No “reduced monitoring” for passive nodes
    
    - No exceptions for DR environments

* * *

## The Design Principle to Take Away

If a node can _ever_ become active, it must be treated as active **all the time**.

That means:

- Monitored

- Audited

- Validated

- Trusted

Anything less introduces a gap between:

- **Resilience architecture**

- **Security architecture**

And that gap is exactly where failures - and breaches - tend to occur.

* * *

## Final Thought

Clustering is about removing single points of failure.

But if your security controls only apply to part of the cluster, you’ve just moved the single point of failure somewhere less visible.

And that’s significantly worse.

Because it won’t fail loudly.

It will fail quietly - right at the moment you need it most.
