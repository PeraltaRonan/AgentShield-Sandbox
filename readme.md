###### AgentShield: Container Isolation & eBPF Runtime Security


##  Project Overview
When autonomous AI agents execute tasks, they are frequently granted access to local shell environments and system utilities. As highlighted in recent security research, agents can exploit environment flaws, escape sandboxes, and make unauthorized calls to external resources.

**AgentShield** addresses this vulnerability by combining hard container isolation with kernel-level eBPF detection. Rather than relying solely on prompt-based guardrails, AgentShield enforces strict operating system boundaries and monitors system call behavior in real time.


## Why was AgentShield Sandbox built?
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
****Webhook Engine** | **Python 3 & Flask (email_webhook.py)**	Real-time HTTP POST listener processing JSON security event payloads from Falco |
**Notification Engine** |	**SMTP via TLS (Gmail API)** |	Automated email dispatch routing executive summaries and raw telemetry audit logs |



## Architecture & File Structure

AgentShield-Sandbox/
├── .github/
│   └── workflows/
│       └── validate-configs.yml                       # CI/CD workflow to validate Compose and YAML syntax
├── rules/
│   └── falco_rules.local.yaml                         # Custom Falco eBPF detection rules
|
|
├── Screenshots/
│   ├── AI-Agent(Attacker).JPG                         # Pre-attack execution screenshot
│   ├── CICD Pipeline-workflow.JPG                     # CI/CD GitHub Actions workflow verification screenshot
│   ├── Falco_Live_initialized(BEFORE ATTACKS).JPG     # Baseline Falco kernel listener screenshot
│   ├── Falco_terminal(AFTER ATTACKS WITH ALERTS).JPG  # Triggered alert telemetry log screenshot
│   └── sanbox_security_ audit_passed.JPG              # Sandbox security compliance report screenshot
|
|
├── scripts/
│   └── simulate_escape.sh                             # Automated attack execution & testing script
├── docker-compose.yml                                 # Hardened container sandbox definition
├── email_webhook.py                                   # Python Flask listener & SMTP dispatch server
└── readme.md                                          # Main project documentation
```
```
## System Workflow

**Hardened Execution** - The AI agent operates strictly inside a locked-down container with dropped Linux capabilities (cap_drop: [ALL]), a read-only root file system, and unprivileged user mappings (1000:1000).

**eBPF Kernel Monitoring** -Falco monitors execve system calls directly at the Linux kernel boundary.

**Detection & Webhook Relay** - If the agent spawns an unauthorized binary (e.g., /bin/sh, curl), Falco intercepts the system call, constructs a JSON payload, and posts it via HTTP Webhook to port 5000.

**Automated Incident Response** - The Flask server (email_webhook.py) captures the webhook payload and automatically sends an authenticated SMTP security alert email to the SOC team.


---

## File Structure
| :--- | :--- |
| **1. AI-AGENT** *(Pre-Attack)* | [AI-Agent(Attacker).JPG](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/AI-Agent(Attacker).JPG) |




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

### HOW TO RUN ###

## To Run Web Server:
###### Step 1
*Go on wsl terminal*
Type:
  python3 email_webhook.py


###### Step 2
## For Terminal 1:
-Open up another Ubuntu():

*How to activate Falco Detection:*
Navigated through AgentShield folder:
    cd~/AgentShield

    Type: start-falco

###### Step 3
## For Terminal 2:
-Open up another Ubuntu(Acts like an AI Agent(Attacker)):

*How to activate attack:*
Navigated through AgentShield folder:

```bash
Type: ubuntu
>
Type cd AgentShield
>
sudo bash ./scripts/simulate_escape.sh
>
```



## Expected Telemetry Output From Terminal 2:

When an unauthorized command execution occurs inside the sandbox, Falco triggers a kernel-level alert logged via `journalctl`:

```text
[CRITICAL ALERT] Agent Sandbox Anomaly! Process=sh Command=sh -c whoami User=1000 Container=agentshield_sandbox
```

Email of *audit* will be sent through receipent.
| **Webhook Email Audit**  | [email-audit-webhook.JPG](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/email-audit_webhook.JPG) |



### Stage 5 - CI/CD Pipeline - Webhook -


 # Writing Rules & Automation-
- Added security rules by configuring Falco to listen for any suspicious activity.
  Or hav running unexpected privilege checks inside a sandbox.

- Created a file under Python tto add a lightweight Flask application that acts like a reciever.
 Opens port 5000 to process any incoming JSON alerts.

- Created a shell script to spin up the target container, and execute any unexpected commands to trigger the system intentionality.

# Environment Setup
- Installed  Python3 Pip using - (sudo apt update && sudo apt install -y python3-pip)
- Installed Flask dependency using - (pip install flask --break-system-packages) or (sudo apt install python3-flask)
- Allow script execution permissions on my AgentShield repositoryscripts using  - (chmod +x ./scripts/simulate_escape.sh)

App Password = uurs veiw tsxi swvm


## Screenshots of Audit:

| Evidence Phase | Github Link |
| :--- | :--- |
| **1. AI-AGENT** *(Pre-Attack)* | [AI-Agent(Attacker).JPG](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/AI-Agent(Attacker).JPG) |
| **2. Falco Live Initialized** *(BEFORE ATTACKS)* | [Falco Live Initialized(BEFORE ATTACKS)](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/Falco_Live_initialized(BEFORE%20ATTACKS).JPG) |
| **3. Falco_terminal(AFTER ATTACKS WITH ALERTS)** | [Falco_terminal(AFTER ATTACKS WITH ALERTS)](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/Falco_terminal(AFTER%20ATTACKS%20WITH%20ALERTS).JPG) |
| **4. Sandbox Security_ Audit Passed** *(Pre-Attack)* | [Sandbox Security_ Audit Passed](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/sanbox_security_%20audit_passed.JPG) |
| **5. CI/CD Pipeline Workflow**  | [CI/CD-Pipeline.JPG](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/CICD%20Pipeline-workflow.JPG) |
| **6. Webhook Email Audit**  | [email-audit-webhook.JPG](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/email-audit_webhook.JPG) |
| **7. File Structure**  | [file_structure.JPG](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/file_structure.JPG) |
| **8. Github Workflow**  | [github-workflow](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/github-workflow.JPG) |
| **9. WSL2 Terminal Push Pipeline**  | [wsl-terminal-push-pipeline-proof.JPG](https://github.com/PeraltaRonan/AgentShield-Sandbox/blob/main/Screenshots/wsl-terminal-push-pipeline-proof.JPG) |