async def check_email(user_email):
    import email
    import imaplib
    import os
    from dotenv import load_dotenv
    load_dotenv()

    EMAIL = 'emaildiscordbot1@gmail.com'
    PASSWORD = os.getenv('password')
    SERVER = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select()
    status, data = mail.search(None, f'(FROM "{user_email}")', 'UNSEEN')
    mail_ids = data[0].split()
    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                print(message)
                return message
    return None

def getChannelId(message: str) -> int:
    id = '67'
    lines = message.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("> Channel ID: "):
            id = line[14:]
            return int(id)
    return id

async def extract_original(text: str) -> str:
    lines = text.splitlines()
    original = []

    for line in lines:
        line = line.strip()  # remove extra spaces at start/end
        # Skip reply headers
        if line.startswith("On ") and "wrote:" in line:
            continue
        if line.startswith("> Channel ID: "):
            break
        if line:  # ignore empty lines
            original.append(line)

    return "\n".join(original)