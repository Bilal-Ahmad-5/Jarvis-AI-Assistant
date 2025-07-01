import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

# 1. CONFIGURATION
# ───────────────────────────────────────────────────────────────
# You can hardcode these (not recommended) or export as env vars:
SMTP_HOST    = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT    = int(os.getenv("SMTP_PORT", 587))
SMTP_USER    =  "muhammad.bilal.05.07.09@gmail.com"
SMTP_PASSWORD = "yywomlkfypolzabj"


def send_email():

    SENDER       = SMTP_USER
    RECIPIENTS   = input("Enter Recipients").split(",")
    SUBJECT      = input("Enter Subject")
    # 2. BUILD THE MESSAGE
    # ───────────────────────────────────────────────────────────────
    msg = EmailMessage()
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(RECIPIENTS)
    msg["Subject"] = SUBJECT

    # prompt = "You are an AI email generator, take user query and make a well organized emails according to the user query./n user query:{query}. /n You must have to genrate a ready to send email, there will be no change in your genrated email. So make the final emailto send."

    # query = input("Enter Query")
    # text_body = llm.invoke(prompt.format(query=query)).content
    text_body = input("Enter Email Message")
    msg.set_content(text_body)

    # 3. ATTACH FILES (optional)
    # ───────────────────────────────────────────────────────────────
    files_to_attach = [
        "reports/summary.pdf",
        "images/chart.png"
    ]
    for file_path in files_to_attach:
        path = Path(file_path)
        if not path.exists():
            print(f"⚠️ Warning: attachment not found: {path}")
            continue

        maintype, subtype = ("application", "octet-stream")
        if path.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
            maintype, subtype = ("image", path.suffix.replace(".", ""))
        elif path.suffix.lower() == ".pdf":
            maintype, subtype = ("application", "pdf")

        data = path.read_bytes()
        msg.add_attachment(data,
                          maintype=maintype,
                          subtype=subtype,
                          filename=path.name)

    # 4. SEND THE MESSAGE
    # ───────────────────────────────────────────────────────────────
    def e_send(message: EmailMessage):
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            # Upgrade to secure TLS
            server.starttls(context=context)
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
            print("✅ Email sent successfully!")

    if __name__ == "__main__":
        # sanity check
        if not (SMTP_USER and SMTP_PASSWORD):
            print("❌ Please set SMTP_USER and SMTP_PASSWORD as environment variables.")
            exit(1)
        e_send(msg)
