---
title: "Architecture Anti-Patterns"
date: 2026-02-17
categories: 
  - "fim"
  - "sc"
tags: 
  - "architecture"
  - "tripwire"
---

File Integrity Monitoring (FIM) and Security Configuration Management (SCM) platforms like the ones I currently work with at Fortra are deceptively simple on the surface: deploy/configure endpoints, define rules/assessments, schedule tasks, evaluate results, report.

In practice, however, architectural missteps turn what should be a high-signal assurance capability into an expensive noise generator for far too many - and it's probably the biggest challenge I still see in projects today (and, to be honest, I've seen plenty of non-FIM and SCM security projects that suffer similarly, but for today I'll focus on FIM/SCM though I may revisit for a VM/EDR post at somepoint!)

Below, then, are some of the more common architectural anti-patterns I've observed in enterprise FIM/SCM implementations - along with why they fail and what the alternatives look like.

## Too Many Policies

### The Anti-Pattern

Hundreds (sometimes thousands) of overlapping policies are deployed because:

- Every benchmark is imported (CIS, NIST, ISO, internal standards)

- Each team wants its own view

- No rationalisation or deduplication occurs

- No policy lifecycle governance exists

### Why It Fails

Architecturally, this creates:

- **Policy sprawl**

- Redundant checks across nodes

- Duplicate rule execution

- Increased scan duration

- Conflicting evaluation logic

- Unmaintainable exception management

More importantly, **signal dilution** occurs. When everything is “critical,” nothing is.

### Better Architecture

- Abstract reusable rule libraries - Tripwire fortunately provides lots of these - but consider too how you approach application monitoring rules such that they are easily transferable between apps so you've got a consistent approach across your organisation!

- Create baseline policies aligned to node class (e.g., Windows Server, RHEL MySQL, Kubernetes Worker, etc). That makes things a lot easier to spot gaps and ensures you're thinking about "device types" and "applications" consistently.

- Consider separating:
    - Operational policies
    
    - Security hardening
    
    - Compliance mapping overlays  
        ... and if you're only doing one of these, consider if the others are necessary/beneficial

- Implement a policy review board and lifecycle process -work out in advance how you plan to evaluate and off/onboard policies ove time.

I encourage you to think in terms of _control objectives_, not just benchmark imports to tick a box...

## Compliance-Only Thinking

### The Anti-Pattern

FIM/SCM is deployed only to “pass audit.”

Common patterns:

- Policies enabled only during audit windows

- Checks mapped exclusively to external standards

- No integration into SOC or incident response

- No threat-informed tuning

### Why It Fails

Compliance validation ≠ security assurance.

FIM and SCM provide:

- Change detection

- Privilege misuse detection

- Drift detection

- Baseline deviation analysis

When scoped only for compliance:

- High-risk operational drift goes unnoticed.

- Threat actors modifying configurations are missed.

- Controls are reactive instead of preventative.

This creates an illusion of security maturity without operational security impact. Sure, on day one, SCM is great, giving binary feedback on state - but _actual_ maturity takes work (but delivers _actual_ gains in turn).

### Better Architecture

- Map FIM alerts into (SIEM) workflows so that your teams actually act on alerts.

- Prioritise high-risk paths (e.g., authentication configs, sudoers, domain policies, etc.). If you don't know what your "crown jewels" are, starting working that out now!

- Align with threat models (e.g., ransomware TTPs targeting backups or logging configs) - MITRE ATT&CK does a great job (and Fortra's Tripwire tools fortunately have good overlap here with MITRE ATT&CK forensic audit and compliance rules to help you get going!).

- Use compliance as a _additional reporting layer_, not the primary design driver.

Design for resilience and detection first and then you audit reporting can become a by-product or "additional benefit" on top.

## Alert Fatigue

### The Anti-Pattern

Default rule sets are enabled with minimal tuning or thought.

The result:

- Thousands of file change alerts per day

- Recurring patch-cycle noise

- Log rotation alerts

- Temporary file churn

- No prioritisation

Eventually:

- Alerts are ignored

- Email notifications are disabled

- SOC disengages

- Executive confidence declines

### Why It Fails

From a systems engineering perspective:

- High false-positive rates degrade trust.

- Cognitive overload reduces detection probability.

- Mean time to acknowledge increases.

- True positives are buried in noise.

The monitoring system becomes entropy.

### Better Architecture

- Implement baselining and drift tolerance.

- Separate:
    - Informational telemetry
    
    - Policy violations
    
    - High-risk change alerts

- Use suppression rules for known maintenance windows.

- Apply risk scoring.

- Route alerts via tiered triage (not raw email).

Architecturally, alerts should be rare, actionable, and prioritised. Programs for continuous improvement, however, should be in place to make sure those alerts are tuned frequently and your posture is actually improve based on insights gathered from the toolset.

# My Final (Opinionated!) Thought

Security does not have “tools you install”. Security is about building **control ecosystems** embedded into operational, security, and governance workflows. As a result, you should be architecting them like critical infrastructure:

- With clear ownership.

- With defined fault domains.

- With lifecycle governance.

- With detection intent.

When designed correctly, they become high-fidelity sensors of configuration risk and operational drift. When designed poorly, they become background noise - and eventually, shelfware. The difference is architectural discipline - so don't forget to speak to your consultancy team about how to make sure you're being effective with your deployments (there's a reason why our teams consultancy often makes the difference between achieving ROI and just ticking the audit compliance box).
