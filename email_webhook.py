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

    #Executive-Friendly Body + Technical Audit Log
    body = f"""Hello Team,

AgentShield Sentinel has detected a runtime security event that requires review.


EXECUTIVE SUMMARY
--------------------------------------------------
Alert Type:       {rule}
Severity Level:   {priority}
Status:           Logged & Contained in Sandbox Environment
Impact Assessment: Low (Isolated inside sandbox container)

Action Required:
No immediate operational downtime has occurred. The security team is auditing the command sequence listed below.


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
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())  # Fixed: sendmail instead of send_mail
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