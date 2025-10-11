# backend/email_utils.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from .schemas import Settings


settings = Settings()  # Load settings from .env file

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS
)

async def send_anonymous_email(recipient: str, subject: str, body: str):
    """
    Sends a plain-text email to the recipient without exposing the sender's email.
    Works with Gmail App Passwords.
    """
    fm = FastMail(conf)

    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype="plain"  # plain text
    )

    try:
        await fm.send_message(message)
        print(f"✅ Email successfully sent to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise e
