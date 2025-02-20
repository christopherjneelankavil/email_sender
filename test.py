import csv
import qrcode
import smtplib
import os
from email.message import EmailMessage

# Email credentials
SMTP_SERVER = "smtp.gmail.com"  # Change if using another provider (if not using google smtp)
SMTP_PORT = 587
SENDER_EMAIL = ""  # Replace with your email (hackathena email id)
SENDER_PASSWORD = ""  # Use App Password (enable 2 factor auth and generate app password from account settings)

list_csv = []

def read_csv(file_path):
    """Reads CSV file and stores data in list_csv."""
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row if present
        for row in csv_reader:
            list_csv.append(row)

def generate_qr(data, filename):
    """Generates a QR code with the given data and saves it as filename."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

def send_email(receiver_email, name, qr_filename):
    """Sends an email with the QR code attachment and a custom message."""
    try:
        msg = EmailMessage()
        msg["Subject"] = "Hackathon Selection & QR Code for Registration"
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        # Email body (HTML)
        email_body = f"""
        <html>
        <body>
            <p>Hi <b>{name}</b>,</p>
            <p><b>This is a test message for testing purposes</b></p>
            <p>🎉 You are selected for the hackathon! 🎉</p>
            <p>We eagerly await your project submission.</p>
            <p>Please use the QR code attached below for your registration.</p>
            <br>
            <p>Best regards,</p>
            <p><b>Hackathon Team</b></p>
        </body>
        </html>
        """
        
        msg.set_content(f"Hi {name},\nYou are selected for the hackathon!\nWe eagerly await your project.\nUse the QR provided below for registration.", subtype='plain')
        msg.add_alternative(email_body, subtype="html")

        # Attach QR code
        with open(qr_filename, "rb") as f:
            msg.add_attachment(f.read(), maintype="image", subtype="png", filename=qr_filename)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"Email sent to {receiver_email}")

    except Exception as e:
        print(f"Failed to send email to {receiver_email}: {e}")

# Main execution
read_csv("Book1.csv")

for i, row in enumerate(list_csv, start=1):
    try:
        user_id, name, email = row
        qr_filename = f'qrcode_{i}.png'
        
        # Generate QR code
        generate_qr(user_id, qr_filename)
        
        # Send email with QR code attachment
        send_email(email, name, qr_filename)

        # Delete the QR code after sending
        os.remove(qr_filename)
    
    except Exception as e:
        print(f"Error processing row {i}: {e}")
