import qrcode
import io
import base64

from .hashes import *
from .countries import COUNTRY_CODES
from evidencelocker.classes import *

from flask import session, g

from evidencelocker.__main__ import app

@app.template_filter('qrcode_img_data')
def qrcode_filter(x):
  
    mem=io.BytesIO()
    qr=qrcode.QRCode()
    qr.add_data(x)
    img=qr.make_image(
        fill_color="#2589bd",
        back_color="white",
    )
    img.save(
        mem, 
        format="PNG"
    )
    mem.seek(0)
    
    data=base64.b64encode(mem.read()).decode('ascii')
    return f"data:image/png;base64,{data}"

@app.template_filter('full_link')
def full_link(x):

    return f"https://{app.config['SERVER_NAME']}{'/' if not x.startswith('/') else ''}{x}"

@app.template_filter('nonce')
def nonce(x):
    return generate_hash(f"{session.get('session_id')}+{x}")

@app.template_filter('logged_out_token')
def logged_out_token(x):
    return logged_out_csrf_token()


@app.template_filter('CC')
def country_code_filter(x):

    if not x:
        return COUNTRY_CODES

    else:
        return COUNTRY_CODES[x]

@app.template_filter("agency_count")
def agency_count_filter(x):

    return g.db.query(Agency).filter_by(country_code=x).count()