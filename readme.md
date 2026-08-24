###### AgentShield: Container Isolation & eBPF Runtime Security


##  Project Overview
When autonomous AI agents execute tasks, they are frequently granted access to local shell environments and system utilities. As highlighted in recent security research, agents can exploit environment flaws, escape sandboxes, and make unauthorized calls to external resources.

**AgentShield** addresses this vulnerability by combining hard container isolation with kernel-level eBPF detection. Rather than relying solely on prompt-based guardrails, AgentShield enforces strict operating system boundaries and monitors system call behavior in real time.


## Why was AgentShield Sanbox built?
The BBC article covers "The Great Sandbox Escape", where an autonomous AI model got evaluated by OpenAI and broke containment and also launched a real world cyberattack against Hugging Face. It marks a major breakthrough in cybersecurity due to it showing the first real case of an artifical intellgience model breaking out of its test environment at its machine speec without its human direction This proves that AI agents themselves are new, active threat vectors that traditional human-focused security simply isn't built to handle. The most important thing is that it grounds AI safety in practical engineering problems like container isolation, proxy zero-day vulnerabilties, and strict network egress control.

## Technology Stack & Requirements

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Operating System** | **Ubuntu via WSL2** | Host environment for Linux kernel interface and Docker runtime |
| **Containerization** | **Docker & Docker Compose v2** | Environment isolation and privilege dropping for non-deterministic agent code |
| **Runtime Security** | **Falco (Modern eBPF)** | Out-of-band kernel telemetry to capture unauthorized `execve` system calls |
| **System Logging** | **Systemd / `journalctl`** | Host log extraction for immediate event auditing |
| **Automation & Alerting** | **Bash (simulate_escape.sh) & Python** | Automated attack simulation and HTTP webhook receiver script for SOC SIEM telemetry integration |
| **CI/CD Pipeline** | **GitHub Actions** | Automated YAML syntax verification and Docker Compose configuration linting on push |




## Architecture & File Structure

AgentShield/
├── .github/
│   └── workflows/
│       └── validate-configs.yml    # CI/CD workflow to validate Compose and YAML syntax
|
|
|
├── rules/
│   └── falco_rules.local.yaml      # Custom Falco eBPF detection rules
├── scripts/
│   └── simulate_escape.sh          # Automated test execution and alerting script
├── .gitignore                      # Environment and temporary log exclusions
├── docker-compose.yml              # Hardened container sandbox definition
├── LICENSE                         # Open-source license (MIT)
└── README.md                       # Main project documentation
```

## System Workflow
1. **Hardened Execution:** The AI agent operates strictly inside a locked-down container with dropped Linux capabilities (`cap_drop: [ALL]`), a read-only root file system, and unprivileged user mappings (`1000:1000`).
2. **eBPF Kernel Monitoring:** Falco monitors `execve` system calls directly at the Linux kernel boundary.
3. **Detection & Alerting:** If the agent spawns an unauthorized binary (e.g., `/bin/sh`, `curl`), Falco intercepts the system call and generates an immediate critical event in host system logs.


## Quick Start Guide

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

## Expected Telemetry Output

When an unauthorized command execution occurs inside the sandbox, Falco triggers a kernel-level alert logged via `journalctl`:

```text
[CRITICAL ALERT] Agent Sandbox Anomaly! Process=sh Command=sh -c whoami User=1000 Container=agentshield_sandbox
```


## Stage 1 - Infrastructure Setup-

- Updated system packages
- Installed a docker, git and essential build tools( needed to install additional files to run docker)
- enable docker service inside WSL2
- Add my user to the docker group( additional linux packages was needed to be installed)


## Stage 2 - Creating a workspace-
- Implemented a (Sandbox) inside docker using bash through nano.
- Implemented (Detection Rules) inside docker using bash through nano.
- Implemented (Test Script) inside docker using bash through nano.

## Stage 3 - Enforcing Security & Execution
- Trust Falco's GPG key
- Add Falco Repo int apt sources
- update repos and install falco

- Add same Detection Rules from 
- Run Falco with Modern eBPF Engine(eBPF Engine is a small software system inside Linux Kernel.Safely runs customer small programs and acts like a fast programmablelater for monitoring, network, and security.)

## Stage 4 - Triggering the ALERT:

## For Terminal 1:
-Open up another Ubuntu():

*How to activate Falco Detection:*
Navigated through AgentShield folder:
    cd~/AgentShield

    Type: start-falco


## For Terminal 2:
-Open up another Ubuntu(Acts like an AI Agent(Attacker)):

*How to activate attack:*
Navigated through AgentShield folder:
    cd~/AgentShield

```bash
chmod +x scripts/simulate_escape.sh
./scripts/simulate_escape.sh
```

## Expected Telemetry Output

When an unauthorized command execution occurs inside the sandbox, Falco triggers a kernel-level alert logged via `journalctl`:

```text
[CRITICAL ALERT] Agent Sandbox Anomaly! Process=sh Command=sh -c whoami User=1000 Container=agentshield_sandbox
```



## Stage 5 - CI/CD Pipeline-

## Stage 6 - Webhook -


## Screenshots of Audit:

    | Evidence Phase | Interactive Github Link | Preview |
    | :--- | :--- | :--- |
    | **1. AI-AGENT** *(Pre-Attack)* | (Screenshots/Falco_Live_initialized(BEFORE%20ATTACKS).jpeg) | <a href="https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/AI-Agent(Attacker).JPG">AI-Agent(Attacker).JPG</a> |
    | **1. Falco Live Initialized** *(BEFORE ATTACKS)* | (Screenshots/Falco_Live_initialized(BEFORE%20ATTACKS).jpeg) | <a href="https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/Falco_Live_initialized(BEFORE%20ATTACKS).JPG">Falco Live Initialized(BEFORE ATTACKS)</a> |
    | **1.Falco_terminal(AFTER ATTACKS WITH ALERTS)** | (Screenshots/Falco_Live_initialized(BEFORE%20ATTACKS).jpeg) | <a href="https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/Falco_terminal(AFTER%20ATTACKS%20WITH%20ALERTS).JPG">Falco_terminal(AFTER ATTACKS WITH ALERTS)</a> |
    | **1. Sandbox Security_ Audit Passed** *(Pre-Attack)* | (Screenshots/Falco_Live_initialized(BEFORE%20ATTACKS).jpeg) | <a href="https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/sanbox_security_%20audit_passed.JPG">Sandbox Security_ Audit Passed</a> |

