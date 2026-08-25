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
### 1. Hardened Sandbox Setup (`docker-compose.yml`)
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

### 2. Falco Detection Rule (`rules/falco_rules.local.yaml`)
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

### 3. Implementation CI/CD Pipeline('.github/workflows/validate-configs.yml')
```yaml
mkdir -p .github/workflows
cat << 'EOF' > .github/workflows/validate-configs.yml
name: Validate AgentShield Security Configurations

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  validate-configs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install PyYAML
        run: pip install pyyaml

      - name: Validate All YAML Files
        run: |
          python3 -c "
          import os, sys, yaml

          yaml_files = []
          for root, dirs, files in os.walk('.'):
              if '.github' in root or '.git' in root:
                  continue
              for f in files:
                  if f.endswith('.yaml') or f.endswith('.yml'):
                      yaml_files.append(os.path.join(root, f))

          if not yaml_files:
              print('[-] Error: No YAML files found in the repo!')
              sys.exit(1)

          for f_path in yaml_files:
              try:
                  yaml.safe_load(open(f_path))
                  print(f'[+] Valid YAML syntax: {f_path}')
              except Exception as e:
                  print(f'[-] Invalid YAML syntax in {f_path}: {e}')
                  sys.exit(1)
          "

      - name: Validate Docker Compose
        run: |
          COMPOSE_FILE=$(find . -name "docker-compose.yml" -o -name "docker-compose.yaml" -print -quit)
          if [ -n "$COMPOSE_FILE" ]; then
            echo "[+] Found Docker Compose at: $COMPOSE_FILE"
            docker compose -f "$COMPOSE_FILE" config -q
            echo "[+] Docker Compose syntax is valid!"
          else
            echo "[!] No docker-compose file found, skipping step."
          fi
EOF
```

### 4. Email Webhook Receiver('email_webhook.py')

```py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

app = Flask(__name__)

#SMTP Configuration 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ronan.peralta9@gmail.com"
SENDER_PASSWORD = "uurs veiw tsxi swvm"  # App Password
RECIPIENT_EMAIL = "peralta.ronan04@gmail.com"

def send_security_email(falco_data):
    rule = falco_data.get("rule", "Unknown Anomaly")
    priority = falco_data.get("priority", "WARNING")
    output = falco_data.get("output", "No details provided.")
    output_fields = falco_data.get("output_fields", {})

    subject = f"[{priority}] AgentShield Security Alert: {rule}"

    body = f"""Hello Team,

AgentShield Sentinel has detected a runtime security event that requires review.

--------------------------------------------------
EXECUTIVE SUMMARY
--------------------------------------------------
Alert Type:       {rule}
Severity Level:   {priority}
Status:           Logged & Contained in Sandbox Environment
Impact Assessment: Low (Isolated inside sandbox container)

Action Required:
No immediate operational downtime has occurred. The security team is auditing the command sequence listed below.

--------------------------------------------------
TECHNICAL AUDIT LOG (FOR ENGINEERING / AUDIT)
--------------------------------------------------
Raw Event Details:
{output}

Container Name:    {output_fields.get('container.name', 'N/A')}
Executed Command:  {output_fields.get('proc.cmdline', 'N/A')}
User:              {output_fields.get('user.name', 'N/A')}
Event Type:        {output_fields.get('evt.type', 'N/A')}

-- 
AgentShield Automated Security System
"""

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print(f"[+] Security email successfully dispatched to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    data = request.json
    if data:
        send_security_email(data)
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    print("[+] Starting Email Webhook Server on port 5000...")
    app.run(host='0.0.0.0', port=5000)

```
