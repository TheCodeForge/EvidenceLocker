import io
import pyotp
import qrcode
import random
import time
import werkzeug.security
import requests

from flask import *

from evidencelocker.helpers.hashes import *
from evidencelocker.decorators.auth import *
from evidencelocker.classes import *
from evidencelocker.helpers.loaders import *

from evidencelocker.__main__ import app

@app.post("/login")
def login_victim():

    #define the response for an invalid login attempt
    #Random sleep is to ensure timing analysis cannot be used to deduce which part of the login failed
    def invalid_login_victim():
        time.sleep(max(0, random.gauss(1.5, 0.33)))
        return redirect("/login_victim?invalid")

    user = get_victim_by_username(request.form.get("username"), graceful=True)
    if not user:
        return invalid_login_victim()

    if not werkzeug.security.check_password_hash(user.pw_hash, request.form.get("password")):
        return invalid_login_victim()

    totp=pyotp.TOTP(user.otp_secret)
    if not totp.verify(request.form.get("otp_code")):

        if request.form.get("otp_code")==user.otp_secret_reset_code:
            user.otp_secret==None
            g.db.add(user)
            g.db.commit()
            session['utype']='v'
            session['uid']=user.id
            return redirect('/set_otp')

        return invalid_login_victim()

    #set cookie and continue to locker
    session["utype"]="v"
    session["uid"]=user.id

    return redirect("/")

@app.post("/login_police")
def login_police():

    #define the response for an invalid login attempt
    #Random sleep is to ensure timing analysis cannot be used to deduce which part of the login failed
    def invalid_login_police():
        time.sleep(max(0, random.gauss(1.5, 0.33)))
        return redirect("/login_police?invalid=1")

    user = get_police_by_email(request.form.get("email"), graceful=True)
    if not user:
        return invalid_login_police()

    if not werkzeug.security.check_password_hash(user.password_hash, request.form.get("password")):
        return invalid_login_police()

    totp=pyotp.TOTP(user.otp_secret)
    if not totp.verify(request.form.get("otp_code")):

        if request.form.get("otp_code")==user.otp_secret_reset_code:
            user.otp_secret==None
            g.db.add(user)
            g.db.commit()
            session['utype']='v'
            session['uid']=user.id
            return redirect('/set_otp')

        return invalid_login_police()

    #set cookie and continue to lockers
    session["utype"]="p"
    session["uid"]=user.id

    return redirect("/lockers")

@app.post("/logout")
def logout():

    session.pop("utype")
    session.pop("uid")

    return redirect ("/")


@app.get("/otp_secret_qr/<secret>.png")
@logged_in_any
def mfa_qr(user, secret):
    x = pyotp.TOTP(secret)
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )
    issuer_name = request.args.get("issuer","TEL")
    qr.add_data(x.provisioning_uri(user.username, issuer_name=issuer_name))
    img = qr.make_image(fill_color="#2589bd", back_color="white")

    mem = io.BytesIO()

    img.save(mem, format="PNG")
    mem.seek(0, 0)
    return send_file(mem, mimetype="image/png", as_attachment=False)

@app.get("/login")
def get_login_victim():

    return render_template(
        "login_victim.html",
        token=logged_out_csrf_token()
        )

@app.get("/signup")
def get_signup_victim():
    
    return render_template(
        "signup_victim.html",
        token=logged_out_csrf_token(),
        hcaptcha = app.config["HCAPTCHA_SITEKEY"]
        )

@app.get("/set_otp")
@logged_in_any
def get_set_otp(user):

    otp_secret=pyotp.random_base32()
    recovery = compute_otp_recovery_code(user, otp_secret)
    recovery=" ".join([recovery[i:i+5] for i in range(0,len(recovery),5)])

    return render_template(
        "set_otp.html",
        otp_secret = otp_secret,
        recovery = recovery,
        user=user
        )

@app.post("/set_otp")
@logged_in_any
def post_set_otp(user):
    otp_secret = request.form.get(otp_secret)
    code = request.form.get(otp_code)

    totp = pyotp.TOTP(otp_secret)

    if not totp.verify(code):
        return redirect('/set_otp?error=Incorrect%20code')



    user.otp_secret=otp_secret
    g.db.add(user)
    g.db.commit()

    return redirect("/")



@app.post("/signup")
def post_signup_victim():
    
    username=request.form.get("username")
    existing_user=get_victim_by_username(username, graceful=True)
    if existing_user:
        return redirect("/signup?error=Username%20already%20taken")
        
    if request.form.get("password") != request.form.get("password_confirm"):
        return redirect("/signup?error=Passwords%20do%20not%20match")

    if request.form.get("terms_agree") != "true":
        return redirect("/signup?error=You%20must%20agree%20to%20the%terms")

    
    #verify hcaptcha
    token = request.form.get("h-captcha-response")
    if not token:
        abort(400)

    data = {"secret": app.config["HCAPTCHA_SECRET"],
            "response": token,
            "sitekey": app.config["HCAPTCHA_SITEKEY"]}
    url = "https://hcaptcha.com/siteverify"

    x = requests.post(url, data=data)

    if not x.json()["success"]:
        return redirect("/signup?error=hCaptcha%20failed")
    
    #create new vic user
    user = VictimUser(
        username=username,
        pw_hash=werkzeug.security.generate_password_hash(request.form.get("password")),
        created_utc=g.time,
        created_country=request.headers.get("cf-ipcountry")
    )

    g.db.add(user)
    g.db.commit()

    session["utype"]='v'
    session["uid"]=user.id

    return redirect("/set_otp")
