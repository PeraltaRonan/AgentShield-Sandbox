import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- SMTP Configuration ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ronan.peralta9@gmail.com"
SENDER_PASSWORD = "uurs veiw tsxi swvm"  # App Password
RECIPIENT_EMAIL = "peralta.ronan04@gmail.com"

def send_security_email(falco_data):
    rule = falco_data.get("rule", "Unknown Anomaly")
    priority = falco_data.get("priority", "WARNING").upper()
    output = falco_data.get("output", "No details provided.")
    output_fields = falco_data.get("output_fields", {})

    subject = f"[{priority}] AgentShield Security Alert: {rule}"

    # Determine badge color based on severity
    badge_color = "#dc3545" if priority in ["CRITICAL", "ERROR"] else "#ffc107"
    badge_text_color = "#ffffff" if priority in ["CRITICAL", "ERROR"] else "#212529"

    # HTML Email Template
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 20px; }}
            .card {{ max-width: 650px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e1e4e8; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
            .header {{ background-color: #0d1117; color: #ffffff; padding: 24px; text-align: left; border-bottom: 3px solid {badge_color}; }}
            .header h2 {{ margin: 0; font-size: 20px; font-weight: 600; letter-spacing: -0.3px; }}
            .badge {{ display: inline-block; background-color: {badge_color}; color: {badge_text_color}; padding: 4px 10px; font-size: 11px; font-weight: 700; border-radius: 12px; text-transform: uppercase; margin-top: 8px; }}
            .content {{ padding: 24px; color: #24292e; line-height: 1.5; }}
            .section-title {{ font-size: 12px; font-weight: 700; text-transform: uppercase; color: #586069; margin-bottom: 12px; letter-spacing: 0.5px; }}
            .data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            .data-table td {{ padding: 10px 12px; border-bottom: 1px solid #e1e4e8; font-size: 14px; }}
            .data-table td.label {{ font-weight: 600; color: #444d56; width: 35%; background-color: #f8f9fa; }}
            .log-box {{ background-color: #0d1117; color: #7ee787; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 12px; padding: 16px; border-radius: 6px; overflow-x: auto; white-space: pre-wrap; word-break: break-all; margin-top: 8px; }}
            .footer {{ background-color: #fafbfc; border-top: 1px solid #e1e4e8; padding: 16px 24px; text-align: center; font-size: 12px; color: #6a737d; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <h2>🛡️ AgentShield Security Event</h2>
                <span class="badge">{priority}</span>
            </div>
            <div class="content">
                <div class="section-title">Executive Summary</div>
                <table class="data-table">
                    <tr><td class="label">Alert Rule</td><td><strong>{rule}</strong></td></tr>
                    <tr><td class="label">Status</td><td><span style="color: #28a745; font-weight: 600;">Captured & Contained</span></td></tr>
                    <tr><td class="label">Impact Assessment</td><td>Isolated within Sandbox Environment</td></tr>
                </table>

                <div class="section-title">Telemetry Audit Details</div>
                <table class="data-table">
                    <tr><td class="label">Container</td><td><code>{output_fields.get('container.name', 'N/A')}</code></td></tr>
                    <tr><td class="label">Executed Process</td><td><code>{output_fields.get('proc.name', 'N/A')}</code></td></tr>
                    <tr><td class="label">Command Line</td><td><code>{output_fields.get('proc.cmdline', 'N/A')}</code></td></tr>
                    <tr><td class="label">User Mapping</td><td><code>{output_fields.get('user.name', 'N/A')}</code></td></tr>
                </table>

                <div class="section-title">Raw System Call Log</div>
                <div class="log-box">{output}</div>
            </div>
            <div class="footer">
                AgentShield Sentinel • Kernel Telemetry Dispatch • Automated SOC Alert
            </div>
        </div>
    </body>
    </html>
    """

    # Construct Multipart Message (HTML + Plaintext fallback)
    msg = MIMEMultipart("alternative")
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    # Fallback plain text for old mail clients
    plain_text = f"[{priority}] AgentShield Alert: {rule}\n\nDetails:\n{output}"
    
    msg.attach(MIMEText(plain_text, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print(f"[+] Formatted security email successfully dispatched to {RECIPIENT_EMAIL}")
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