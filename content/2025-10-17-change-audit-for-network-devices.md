---
title: "Change Audit for Network Devices"
date: 2025-10-17
categories: 
  - "fim"
tags: 
  - "tripwire"
---

I often post over on the Tripwire/Fortra bIog about the importance of monitoring, but don't typically talk about the "technical ins and outs" of how I approach and think about Change Audit so I'm hoping to start a series of posts about File Integrity Monitoring (FIM) aka Change Audit (an important term since today we won't be talking about "files" necessarily, but rather "live" configurations that we might want to audit). I'll also hopefully start adding some posts around my other more common areas of monitoring such as Vulnerability Management (VM), and Security Configuration Management (SCM, or policy compliance... we do love our terms in IT security, don't we!?).

## Why this matters?

ln regulated and security-conscious environments, the ability to detect unauthorized or unintended changes to network devices is critical. Change audit and integrity monitoring are well-established disciplines in servers and endpoints, but applying the same principles to firewalls, routers, and switches requires a slightly different approach but a homogenous approach to "change audit" in general is important.

One of the most effective techniques that Tripwire Enterprise tends to focus on is what we call "Command Output Validation Rules" though you might see or think of more generically as command output comparison—running specific “show” or “get” commands against a device, capturing the output, and comparing it against a trusted baseline. Any difference can then be flagged as a potential configuration drift, service-impacting change, or even a security risk.

## Why Command-Based Integrity Monitoring?

Most enterprise network devices expose their configuration and runtime state via CLI commands - pulling data from "mini-config databases" or from memory/a protected file system. By defining a list of appropriate commands that should not change frequently, administrators can build an integrity monitoring profile that reveals:

- Unauthorized configuration changes (e.g., firewall rules added or removed without change control).

- Service-impacting modifications (e.g., routing table differences, interface status changes).

- Security exposures (e.g., new administrative accounts or relaxed password requirements).

Note this isn't just about ensuring secure configs, it's about ensuring secure processes and service availability. Unsurprisingly then, this approach also aligns with well-recognized standards:

- PCI DSS v4.0 Requirement 11.5.2 calls for file integrity monitoring or change-detection mechanisms to ensure critical configurations are not altered without authorization.

- CIS Benchmarks for firewalls (including Palo Alto Networks, Cisco, and Check Point) recommend regular validation of system and security configuration settings against a secure baseline.

## Choosing the Right Commands

Ok, so let's get to the "technical" part. The key to this whole approach is to select deterministic commands—those that yield stable output unless a meaningful configuration or state change has occurred. Commands that include ephemeral values like uptime, session counters, or CPU utilization are not suitable for integrity monitoring, because they will always differ and offer "low value".

Instead, focus on commands that:

- Reflect the configuration state of the device.

- Represent security policies or access controls.

- Expose critical system settings like SNMP strings, NTP servers, or authentication sources.

- Show interface and routing configuration where unauthorized changes could disrupt service.

With that in mind, examples of unsuitable commands I've seen people sometimes run:

- show system info (contains uptime, dynamic session counts).

- show session all (sessions constantly change).

whereas here's examples of suitable commands:

- show config running (running configuration snapshot).

- show admins/users (administrative accounts and roles).

- show network interface all (interface IPs and link states).

- show deviceconfig system (system-level settings like DNS, NTP, banners).

Now there is a caveat here - thanks to Tripwire policy tooling and regex based filtering, some of those earlier unsuitable commands might still be used but only with a bit of extra effort - for example we might use that _show system info_ command but filter via regex the dynamic data out or use regex just to select, say, firmware versions we can identify changes tied to a software update (or capture an inventory of versions that can prove super helpful to confirm patching and/or identify if you're at risk of, say, a zero day vulnerability

## An Actual Example: Palo Alto Firewalls

Let’s walk through a few example commands on a Palo Alto Networks firewall and how they could be used in a change audit framework.

1. Running Configuration

> show config running

Purpose: Captures the live configuration of the device.

Audit Use: Any deviation from the baseline should trigger review. Even small differences (e.g., security rule order) can materially impact traffic flow.

Standard Mapping: PCI DSS 11.5.2 (critical configuration integrity), CIS Palo Alto Benchmark section 1.1.

2. Administrator Accounts

> show admins all

Purpose: Lists all local and remote admin accounts with their roles.

Audit Use: Detects unauthorized creation of admin accounts or role escalation.

Standard Mapping: PCI DSS 7 (restrict access to system components and cardholder data).

3. Interfaces and Zones

> show network interface all  
> show zone

Purpose: Captures the assignment of IPs, physical/logical interfaces, and their security zones.

Audit Use: Highlights unexpected changes in segmentation—potentially exposing sensitive networks.

Standard Mapping: CIS Benchmark 3.1 (secure zone definitions), PCI DSS 1 (segmentation and firewall requirements).

4. System Services (NTP, DNS, Logging)

> show deviceconfig system

Purpose: Shows core services such as NTP servers, DNS configuration, syslog destinations, banners, and hostnames.

Audit Use: Detects redirection of logs (security gap) or changes to NTP/DNS that could affect trust and time synchronization.

Standard Mapping: CIS Benchmark 1.2 (configure time synchronization), PCI DSS 10 (logging integrity).

5. Security Rules

> show running security-policy

Purpose: Extracts the active firewall rulebase.

Audit Use: Ensures no rules are added, removed, or reordered outside of change control.

Standard Mapping: PCI DSS 1.2 (firewall configuration management), CIS Benchmark 4.x (secure ACLs).

## Building a Monitoring Framework

With those commands in mind we can then start to consider what a basic monitoring framework can achieve next so we can start to build "business" goals for our monitoring that can further define what's useful out of those commands to capture for change audit.

Baseline Capture: After initial hardening and approval, capture the baseline output of each selected command. Store this securely in your monitoring system.

Regular Polling: At defined intervals (daily, weekly, or aligned with change windows), rerun the commands and compare outputs against the baseline.

Exception Handling: Integrate with your change management process. If an authorized change has been made, update the baseline after validation.

Alerting & Reporting: Trigger alerts on unauthorized deviations and report regularly for compliance evidence.

## Interpreting Differences

Not every difference is equal. Some may indicate service impact (e.g., an interface moved zones) while others may represent a security impact (e.g., new admin account created). Thus, once you've got your framework in place, a useful approach is to categorize alerts into a few different "buckets" e.g.:

- Security-critical: new admin accounts, security rules changes, altered logging destinations.

- Service-critical: routing changes, interface reassignments.

- Informational/compliance aligned: hostname or banner updates.

By triaging changes in this way to respond to quickly to material risks while maintaining audit evidence for all detected modifications - again, this is something Tripwire is particularly good at helping out with. You can even tie specific change alert types to different notification routes - changes that impact operations versus security can then end up with the "right person".

## Hard to argue with **simple**, **flexible** _and_ **insightful**

Command output comparison is, to my mind, a powerful, low-cost way to extend integrity monitoring principles to network devices. By carefully selecting commands that reflect stable, security- or service-relevant configuration data, administrators can meet regulatory requirements (PCI DSS, CIS Benchmarks), strengthen their change management processes, and detect potentially dangerous drift before it causes downtime or a breach.

When done right, this approach provides both compliance assurance and operational resilience—key goals for any modern security program. And, if you're not sure what's what, don't forget that consultants like myself have (literal) years of experience in delivering value around these functions so don't be afriad to reach out)!
