import time
import random
import werkzeug.security
import pyotp
from flask import *

from evidencelocker.helpers.loaders import *
from evidencelocker.classes import *
from evidencelocker.__main__ import app

@app.post("/login_victim")
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
        return invalid_login_victim()

    #set cookie and continue to locker
    session["utype"]="v"
    session["uid"]=user.id

    return redirect("/locker")

@app.post("/login_police")
def login_police():

    #define the response for an invalid login attempt
    #Random sleep is to ensure timing analysis cannot be used to deduce which part of the login failed
    def invalid_login_police():
        time.sleep(max(0, random.gauss(1.5, 0.33)))
        return redirect("/login_police?invalid")

    user = get_police_by_email(request.form.get("email"), graceful=True)
    if not user:
        return invalid_login_police()

    if not werkzeug.security.check_password_hash(user.password_hash, request.form.get("password")):
        return invalid_login_police()

    totp=pyotp.TOTP(user.otp_secret)
    if not totp.verify(request.form.get("otp_code")):
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
def mfa_qr(secret,):
    x = pyotp.TOTP(secret)
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L
    )
    qr.add_data(x.provisioning_uri(issuer_name="TEL"))
    img = qr.make_image(fill_color="#2589bd", back_color="white")

    mem = io.BytesIO()

    img.save(mem, format="PNG")
    mem.seek(0, 0)
    return send_file(mem, mimetype="image/png", as_attachment=False)

#disabled for now to prevent usage on live staging while this function is incomplete
#@app.post("/signup_victim")
def signup_victim():
    
    username=request.form.get("username")
    existing_user=get_victim_by_username(username, graceful=True)
    if existing_user:
        return redirect("/signup_victim?error=Username%20already%20taken")
        
    if request.form.get("password") != request.form.get("password_confirm"):
        return redirect("/signup_victim?error=Passwords%20do%20not%20match")
    
    #verify 2fa
    otp_secret=request.form.get("otp_secret")
    totp=pyotp.TOTP(otp_secret)
    if not totp.verify(request.form.get("otp_code")):
        return redirect("/signup_victim?error=Incorrect%20two-factor%20code")
    
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
        return abort(400)
    
    #create new vic user
    user = VictimUser(
        username=username,
        pw_hash=werkzeug.security.generate_password_hash(request.form.get("password")),
        created_utc=g.time,
        name=request.form.get(real_name),
        otp_secret=otp_secret,
        creation_country=request.headers.get("cf-ipcountry")
    )
