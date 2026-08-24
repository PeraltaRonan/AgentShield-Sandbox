# AgentShield: Container Isolation & eBPF Runtime Security

> **A zero-trust sandbox and kernel-level runtime monitoring architecture built on Linux (Ubuntu/Kali) to prevent Agentic AI sandbox escapes, unauthorized shell executions, and lateral network movement.**

---

## 📌 Project Overview

When autonomous AI agents execute tasks, they are frequently granted access to local shell environments and system utilities. As highlighted in recent security research, agents can exploit environment flaws, escape sandboxes, and make unauthorized calls to external resources.

**AgentShield** addresses this vulnerability by combining hard container isolation with kernel-level eBPF detection. Rather than relying solely on prompt-based guardrails, AgentShield enforces strict operating system boundaries and monitors system call behavior in real time.

---

## 🛠️ Technology Stack & Requirements

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Operating System** | **Ubuntu / Kali Linux (Native, VM, or WSL2)** | Host environment for Linux kernel interface and Docker runtime |
| **Containerization** | **Docker & Docker Compose v2** | Environment isolation and privilege dropping for non-deterministic agent code |
| **Runtime Security** | **Falco (Modern eBPF)** | Out-of-band kernel telemetry to capture unauthorized `execve` system calls |
| **System Logging** | **Systemd / `journalctl`** | Host log extraction for immediate event auditing |

---

## 🏗️ Architecture & File Structure

```text
AgentShield/
├── .github/
│   └── workflows/
│       └── validate-configs.yml    # CI/CD workflow to validate Compose and YAML syntax
├── rules/
│   └── falco_rules.local.yaml      # Custom Falco eBPF detection rules
├── scripts/
│   └── simulate_escape.sh          # Automated test execution and alerting script
├── .gitignore                      # Environment and temporary log exclusions
├── docker-compose.yml              # Hardened container sandbox definition
├── LICENSE                         # Open-source license (MIT)
└── README.md                       # Main project documentation
```

### System Workflow
1. **Hardened Execution:** The AI agent operates strictly inside a locked-down container with dropped Linux capabilities (`cap_drop: [ALL]`), a read-only root file system, and unprivileged user mappings (`1000:1000`).
2. **eBPF Kernel Monitoring:** Falco monitors `execve` system calls directly at the Linux kernel boundary.
3. **Detection & Alerting:** If the agent spawns an unauthorized binary (e.g., `/bin/sh`, `curl`), Falco intercepts the system call and generates an immediate critical event in host system logs.

---

## 🚀 Quick Start Guide

### 1. Initialize Workspace & Configuration
```bash
mkdir -p AgentShield/rules AgentShield/scripts AgentShield/.github/workflows
cd AgentShield
```

### 2. Hardened Sandbox Setup (`docker-compose.yml`)
```yaml
version: '3.8'

services:
  agentshield_sandbox:
    image: python:3.11-slim
    container_name: agentshield_sandbox
    command: sleep infinity
    read_only: true
    user: "1000:1000"
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    mem_limit: 512m
    cpus: 0.5
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64m
```

### 3. Falco Detection Rule (`rules/falco_rules.local.yaml`)
```yaml
- rule: AgentShield Sandbox Escape Attempt
  desc: Detects unexpected process execution inside the restricted agent sandbox
  condition: >
    container.name = "agentshield_sandbox" and
    evt.type = execve and
    proc.name in (bash, sh, zsh, nc, nmap, curl, wget)
  output: >
    [CRITICAL ALERT] Agent Sandbox Anomaly!
    Process=%proc.name | Command=%proc.cmdline | User=%user.name | Container=%container.name
  priority: WARNING
```

### 4. Run Testing Script
```bash
chmod +x scripts/simulate_escape.sh
./scripts/simulate_escape.sh
```

---

## 🧪 Expected Telemetry Output

When an unauthorized command execution occurs inside the sandbox, Falco triggers a kernel-level alert logged via `journalctl`:

```text
[CRITICAL ALERT] Agent Sandbox Anomaly! Process=sh Command=sh -c whoami User=1000 Container=agentshield_sandbox
```


Docker Container- 

-Updated system packages
- Installed a docker, git and essential build tools
- enable docker service inside WSL2
- Add my user to the docker group