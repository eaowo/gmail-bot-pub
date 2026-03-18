async def send(message, author, receiver_email, channel_id):
    import smtplib
    import ssl
    import os
    from dotenv import load_dotenv
    load_dotenv()
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "emaildiscordbot1@gmail.com"
    password = os.getenv('password')
    # password = input("Type your password and press enter: ")

    # Create a secure SSL context
    context = ssl.create_default_context()
    server = None

    html_content = f"""
    <div>{author}: {message}</div>
    <div style="margin-top:20px; padding:10px; border:1px solid #ccc; border-radius:10px; width:fit-content; font-size:12px;">
        Channel ID: {channel_id}
    </div>
    """

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Family Group Chat"
        msg.attach(MIMEText(html_content, 'html'))
        server.send_message(msg)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        if server:
            server.quit()