import requests
import time

from flask import *

from evidencelocker.__main__ import app

def _send_mail(to_address, subject, html, plaintext=None, files={}):
    
    url="https://api.mailgun.net/v3/mail.theevidencelocker.org/messages"

    data={
        "to": [to_address],
        "from": "TEL <noreply@mail.theevidencelocker.org>",
        "subject": subject,
        "text": plaintext,
        "html": html
    }

    return requests.post(
        url,
        auth=(
            "api", app.config["MAILGUN_KEY"]
            ),
        data=data,
        files=[("attachment", (k, files[k])) for k in files]
        )

def send_email(user, template_name, subject, files={}, **kwargs):

    return _send_mail(
        to_address = user.email,
        subject=subject,
        html = render_template(
            f"mail/{template_name}.html",
            user=user,
            **kwargs
            ),
        files=files
        )