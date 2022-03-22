import sass
from flask import *

from evidencelocker.decorators.auth import *
from evidencelocker.__main__ import app

@app.get('/')
@logged_in_desired
def home(user):
    if user and user.type_id.startswith('v'):
        return redirect(user.permalink)
        
    return render_template(
        "home.html",
        user=user
        )

@app.get("/help/<pagename>")
@logged_in_desired
def help(user, pagename):
    
    if pagename=="donate":
        
        return render_template(
            'help/donate.html',
            user=user,
            btc='37fctBbwVHwkMoF97FzvUHhurncMfwEqV4',
            eth='0xf7378b181fa40e447a18f05efff5713c1519318b',
            bch='qrpqs09gqdzpdpxj7kj2nuskpaaxum32rsjrlustyu',
            xmr='481Zwedy6ydWGSBKBFZ5dCAV1DuMHTc7Y4xNSwYd63VHcfKf9bmpvoUXVognjjbb6fQA8pQXRgqUHcEJ88so62iqFxXaTyY',
            ltc='M8NePw5tQgSGKm2jEHkvr8CmxHJfjkdoQ7',
            xlm='GCXONVKCJRTTA46N4ML35TAJYRMIV7NBA4TXNKM7CWLZJTSOQ3U5MGBB'
        )
    
    return render_template(
        safe_join("/help", pagename)+'.html',
        user=user
        )

@app.get("/assets/style/<stylefile>.css")
def light_css(stylefile):
	with open(safe_join("evidencelocker/assets/style/", stylefile)+'.scss') as stylesheet:
		return Response(
			sass.compile(string=stylesheet.read()),
			mimetype="text/css"
			)
