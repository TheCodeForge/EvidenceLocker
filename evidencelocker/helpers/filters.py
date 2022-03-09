import qrcode
import io
import base64
from evidencelocker.__main__ import app

@app.template_filter('qrcode_img_data')
def qrcode_filter(x):
  
    mem=io.BytesIO()
    img=qrcode.make(
        x,
        fill_color="#2589bd",
        back_color="white",
        image_factory=qrcode.image.svg.SvgImage
    )
    img.save(
        mem, 
        format="SVG"
    )
    mem.seek(0)
    
    data=base64.b64encode(mem.read()).decode('ascii')
    return f"data:image/svg;base64,{data}"
