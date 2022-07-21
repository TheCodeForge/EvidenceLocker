import qrcode
import qrcode.image.svg
import io
import base64
import pprint
from urllib.parse import urlparse, urlunparse

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

@app.template_filter('qrcode_svg')
def qrcode_filter(x):
  
    qr=qrcode.QRCode(image_factory = qrcode.image.svg.SvgPathImage)
    qr.add_data(x)
    img=qr.make_image(
        fill_color="#2589bd",
        back_color="white",
    )
    return f"data:image/svg+xml;utf8,{img.to_string()}"

@app.template_filter('full_link')
def full_link(x):
    return urlunparse(urlparse(x)._replace(scheme=f"http{ 's' if app.config['FORCE_HTTPS'] else '' }", netloc=app.config['SERVER_NAME']))

@app.template_filter('nonce')
def nonce(x):
    return generate_hash(f"{session.get('session_id')}+{x}")

@app.template_filter("path_token")
def path_token(x, user):
    return generate_hash(f"{user.id}+{user.public_link_nonce}+{x}")

@app.template_filter("add_token_param")
def add_token_param(x, user):
    parsed_url=urlparse(x)
    return urlunparse(parsed_url._replace(query=f"token={generate_hash(f'{user.id}+{user.public_link_nonce}+{parsed_url.path}')}"))

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

@app.template_filter('pprint')
def pprint_filter(x):

    return pprint.pformat(x)

@app.template_filter("crypto_data")
def crypto_data_filter(x):

    return {
        "btc": {
            "name": "Bitcoin",
            "addr": "37fctBbwVHwkMoF97FzvUHhurncMfwEqV4"
        },
        "eth": {
            "name": "Ether",
            "addr": "0xf7378b181fa40e447a18f05efff5713c1519318b",
            "text": "The following Ethereum blockchain tokens are also accepted at this address:\n\n* BAND\n* BAT\n* COMP\n* MKR"
        },
        "bch": {
            "name": "Bitcoin Cash",
            "addr": "qrpqs09gqdzpdpxj7kj2nuskpaaxum32rsjrlustyu"
        },
        "xmr": {
            "name": "Monero",
            "addr": "481Zwedy6ydWGSBKBFZ5dCAV1DuMHTc7Y4xNSwYd63VHcfKf9bmpvoUXVognjjbb6fQA8pQXRgqUHcEJ88so62iqFxXaTyY"
        },
        "ltc": {
            "name": "LiteCoin",
            "addr": "M8NePw5tQgSGKm2jEHkvr8CmxHJfjkdoQ7"
        },
        "xlm": {
            "name": "Stellar Lumen",
            "addr": "GCXONVKCJRTTA46N4ML35TAJYRMIV7NBA4TXNKM7CWLZJTSOQ3U5MGBB"
        }
    }