import qrcode
import io
import base64
from evidencelocker.__main__ import app

@app.template_filter('qrcode_img_data')
def qrcode_filter(x):
  
    qr = qrcode.QRCode()
    qr.add_data(x)
  
    mem=io.BytesIO()
    img=qr.make_image(,
        fill_color="#2589bd",
        back_color="white"
    )
    img.save(
        mem, 
        format="PNG"
    )
    mem.seek(0)
    
    data=base64.b64encode(mem.read()).decode('ascii')
    return f"data:image/png;base64,{data}"
