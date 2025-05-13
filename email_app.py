import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Email configuration from environment variables
EMAIL_CONFIG = {
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "sender_email": os.getenv("SENDER_EMAIL"),
    "sender_password": os.getenv("SENDER_PASSWORD")
}

def send_email(to_email: str, subject: str, html_content: str) -> None:
    """
    Function to send email using SMTP
    """
    try:
        # Validate email configuration
        if not all([EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"]]):
            raise Exception("Sender email or password not configured in .env file")

        # Create MIME message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG["sender_email"]
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach HTML content
        msg.attach(MIMEText(html_content, 'html'))

        # Connect to SMTP server
        with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
            server.starttls()  # Enable TLS
            server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
            server.send_message(msg)

    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

# Streamlit UI for sending emails
st.title("Ky'ra Email Sending App")

with st.form("email_form"):
    to_email = st.text_input("Recipient Email", placeholder="recipient@example.com")
    subject = st.text_input("Subject", placeholder="Enter email subject")
    html_content = st.text_area("HTML Content", placeholder="Enter HTML content for the email")
    submitted = st.form_submit_button("Send Email")

    if submitted:
        if not to_email or not subject or not html_content:
            st.error("All fields are required.")
        else:
            try:
                send_email(to_email, subject, html_content)
                st.success(f"✅ Email sent successfully to {to_email}")
            except Exception as e:
                st.error(f"❌ Failed to send email: {str(e)}")

# Instructions for running the app
st.markdown("""
### How to Run the App
1. Save this code in a file named `email_app.py`.
2. Create a `.env` file in the same directory with the following content:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_specific_password
```
   Replace `your_email@gmail.com` with your email and `your_app_specific_password` with an app-specific password (e.g., for Gmail, generate one in your Google Account settings).
3. Install required packages:
   ```bash
   pip install streamlit python-dotenv
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run email_app.py
   ```
5. Open the provided URL (usually `http://localhost:8501`) in your browser.
""")