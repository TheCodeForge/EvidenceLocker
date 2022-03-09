import requests
import time

from flask import *

from evidencelocker.__main__ import app

def send_mail(to_address, subject, html, plaintext=None, files={}, from_address="TEL <noreply@mail.theevidencelocker.org>"):
    
    url="https://api.mailgun.net/v3/mail.theevidencelocker.org/messages"

    data={
        "to": [to_address],
        "from": from_address,
        "subject": subject,
        "text": plaintext,
        "html": html
    }

    return requests.post(
        url,
        auth=(
            "api", app.config["MAILGUN_KEY"]
            )
        data=data,
        files=[("attachment", (k, files[k])) for k in files]
        )
