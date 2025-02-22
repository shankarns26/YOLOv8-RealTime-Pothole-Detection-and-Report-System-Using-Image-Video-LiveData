from email.message import EmailMessage
import ssl
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email(cont_dic, mail_receiver, is_video=False):
    # Get email credentials from environment variables
    mail_sender = os.getenv('EMAIL_SENDER', 'potholedetection06@gmail.com')
    mail_password = os.getenv('EMAIL_PASSWORD', 'bnoffqdwtcxsfhfm')

    # Create the multipart message
    msg = MIMEMultipart()
    msg['From'] = mail_sender
    msg['To'] = mail_receiver
    msg['Subject'] = 'Pothole Detection Report'

    # Email body
    body = f"Potholes are identified at location: {cont_dic['location']}.\nRoad Type: {cont_dic['highway_type']}\nPothole Size: {cont_dic['size']}\nPosition: {cont_dic['position']}\n\nPlease take necessary actions."
    msg.attach(MIMEText(body, 'plain'))

    if is_video:
        # Attach the processed video if it exists
        video_path = "results/processed.mp4"
        if os.path.exists(video_path):
            with open(video_path, 'rb') as f:
                video_data = f.read()
                video_attachment = MIMEApplication(video_data, _subtype="mp4")
                video_attachment.add_header('Content-Disposition', 'attachment', filename='pothole_detection.mp4')
                msg.attach(video_attachment)
    else:
        # Attach the pothole image if it exists
        image_path = "results/image_result.jpg"
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img_data = f.read()
                image = MIMEImage(img_data, name="pothole_detected.jpg")
                msg.attach(image)

    # Establish a secure SSL connection and send the email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(mail_sender, mail_password)
            smtp.sendmail(mail_sender, mail_receiver, msg.as_string())
            print(f"Email sent successfully with {'video' if is_video else 'image'} attachment!")
    except Exception as e:
        print(f"Error sending email: {e}")
