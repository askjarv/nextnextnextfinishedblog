---
title: "Monitoring Containers - A FIM perspective"
date: 2026-03-10
tags: 
  - "openshift"
  - "rhel"
  - "tripwire"
---

One of the common asks I get as a consultant at the moment is how best to approach monitoring containers with "FIM"... but modern Kubernetes/container platforms (e.g. **Red Hat OpenShift**) change a lot of the assumptions that traditional host-based security monitoring relied on since nodes (a term Tripwire were ahead of the game with using heavily!) are often ephemeral, the configuration is declarative, and workloads may scale dynamically meaning "change" in many forms can be common.

When implementing **File Integrity Monitoring (FIM)** with Tripwire Enterprise then it is important to align the monitoring approach with the **operational model of the cluster**. In practice, OpenShift environments I've worked on monitoring typically fall into one of two architectural patterns:

1. **Immutable infrastructure clusters** (MachineConfig-driven nodes)

3. **Mutable host-integrated clusters** (nodes behave more like traditional RHEL servers)

Each pattern benefits from a different Tripwire monitoring strategy so let's start by defining how your containers are setup...

* * *

## Understanding the OpenShift Node Model

OpenShift clusters are built on top of Red Hat OpenShift and frequently use **MachineConfigPools (MCPs)** to define node configuration.

When nodes are rebuilt or replaced, the cluster applies the defined machine configuration automatically. This means:

- Nodes may be **replaced rather than patched**

- Configuration drift should be **extremely rare**

- Most expected changes occur via **cluster upgrades or deployments**

However, not all environments are fully immutable. Some clusters run workloads that directly interact with the host operating system, requiring a more traditional monitoring model.

* * *

# Approach 1 - Immutable OpenShift Monitoring

This model is ideal when nodes are **fully managed via MachineConfigPools** and configuration drift should effectively never occur.

### Typical Characteristics

This approach works best when:

- Worker nodes are managed by **MachineConfigPools**

- Node replacement is common (autoscaling, upgrades)

- The cluster follows **immutable infrastructure principles**

- Only a small set of **critical host paths should ever change**

Examples of these critical files include:

- SSH configuration

- kubelet configuration

- CRI-O container runtime configuration

- System binaries

- Core OS configuration files

### Tripwire Monitoring Strategy

In this architecture, Tripwire monitoring may be deployed as a **node-level sidecar container**.

The key elements are:

**Node FIM Sidecar**

- One monitoring pod scheduled per node

- Host paths mounted **read-only**

- Monitoring focuses on **host OS drift**

Example monitored paths might include:

```
/etc/ssh//etc/kubernetes//etc/crio//usr/bin//usr/sbin//etc/systemd/
```

**Event Forwarding**

The sidecar:

1. Monitors file changes locally...

3. Emits change events...

5. Sends them to a central sink...

7. ...Where the **Tripwire Axon agent** collects and forwards them to Tripwire Enterprise

This design ensures:

- Monitoring **survives node replacement**

- Monitoring **scales automatically with the cluster**

- No persistent host agent installation is required

### Benefits

This approach aligns well with immutable infrastructure principles:

- **Minimal operational overhead**

- **No host modifications**

- **Automatic scaling with node count**

- **High signal-to-noise ratio** because drift should rarely occur

In practice, any detected change becomes **high-confidence evidence of configuration drift or a potential compromise**, as well as providing a robust audit history.

* * *

# Approach 2 - Mutable / Host-Integrated Workloads

Not every OpenShift cluster follows a strict immutable pattern.

Some environments run **host-integrated workloads** where legitimate changes occur at the host level.

Examples include:

- Custom device plugins

- Storage modules

- Host networking configurations

- Legacy monitoring agents

- Hardware integrations

- Vendor-provided host utilities

In these environments, nodes behave more like traditional **RHEL servers**, and direct host monitoring becomes more appropriate.

### Tripwire Monitoring Strategy

In this model, Tripwire performs monitoring via **SSH from a trusted node**.

Typically:

- A **Tripwire Axon agent** runs on a cluster management host or master node

- The agent enumerates cluster nodes

- It connects to worker nodes via **SSH**

- Configuration and file state are collected remotely

Example workflow:

1. Axon agent discovers cluster nodes

3. The agent connects via SSH

5. Critical files are enumerated

7. Tripwire Enterprise evaluates integrity and configuration state

### Benefits

This model provides:

- **Deep visibility into mutable host configurations**

- Flexibility when **legitimate host changes occur**

- Integration with existing **RHEL operations models**

While it requires SSH connectivity, it also allows Tripwire to evaluate a broader set of host state data.

* * *

# Designing the Monitoring Scope

Regardless of the approach selected, one of the most important steps in the implementation is defining the **critical audit scope**.

Questions to answer include:

- Which files represent **security-critical state**?

- Are there **per-pod configuration differences**?

- Are application components writing to shared host paths?

- Which changes are **expected vs suspicious**?

In many environments, differences between pods or node roles can be handled by defining **clear start and stop points** in the monitored filesystem hierarchy.

Tripwire policies can then focus on the **specific directories that represent security-critical configuration**, rather than attempting to monitor the entire node filesystem.

* * *

# Accounting for Dynamic Workflows

OpenShift clusters introduce several dynamic processes that must be understood during implementation.

Examples include:

- Pod autoscaling

- Rolling deployments

- Cluster upgrades

- MachineConfig updates

- Node replacement

Each of these workflows may introduce **expected file changes**.

During the Tripwire design phase, it is essential to map these workflows so that monitoring policies reflect **how the platform actually operates**.

Without this step, organizations often experience **false positives during normal deployments**.

* * *

# Designing the Change Review Process

Tripwire Enterprise provides strong change review capabilities, but they must be aligned with the **expected operational lifecycle of the platform**.

Typical workflows include:

**Deployment Promotion**

When a valid application update occurs, the Tripwire change can be:

- reviewed

- validated

- promoted to the new baseline

**Version Deprecation**

When older pod versions are retired, corresponding file states may need to be removed from the expected baseline.

**Automated Promotions**

In some environments, promotions may be automatically tied to:

- CI/CD pipelines

- cluster upgrade workflows

- release management systems

This ensures the Tripwire baseline always reflects the **approved state of the platform**.

* * *

# Choosing the Right Approach

Selecting the right monitoring model ultimately depends on how the OpenShift environment is operated.

| Architecture Type | Recommended Approach |
| --- | --- |
| Immutable infrastructure | Sidecar FIM monitoring |
| Node replacement common | Sidecar FIM monitoring |
| Minimal host changes | Sidecar FIM monitoring |
| Host-integrated applications | SSH enumeration |
| Frequent legitimate host updates | SSH enumeration |
| Traditional RHEL operations | SSH enumeration |

Many environments also implement **a hybrid model**, where immutable worker nodes use the sidecar approach while specialized nodes are monitored via SSH.

* * *

# Final Thoughts

OpenShift changes how infrastructure behaves, but it does not eliminate the need for **host integrity monitoring**.

By aligning monitoring architecture with the cluster’s operational model, organizations can ensure that **Tripwire Enterprise delivers high-value security insights without operational friction**.

The key to success is not simply deploying monitoring technology, but **designing the monitoring scope, workflows, and review processes around the realities of the platform**.

When done correctly, Tripwire becomes a powerful mechanism for detecting:

- configuration drift

- unauthorized changes

- compromised nodes

- security policy violations

\- whilst remaining compatible with the dynamic nature of modern container platforms.
