import os
import qrcode
from flask import Flask, request, render_template

app = Flask(__name__)

QR_CODE_DIR = 'static/qr_codes'

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                if not os.path.exists(QR_CODE_DIR):
                    os.makedirs(QR_CODE_DIR)

                filename = f"qr_{hash(url) % 10000}.png"
                filepath = os.path.join(QR_CODE_DIR, filename)

                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(url)
                qr.make(fit=True)
                qr_image_obj = qr.make_image(fill_color="black", back_color="white")
                qr_image_obj.save(filepath)

                qr_image = f"qr_codes/{filename}"
                print(f"Generated QR image: {qr_image}")
            except Exception as e:
                print(f"Error: {e}")

    return render_template("index.html", qr_image=qr_image)

if __name__ == '__main__':
    app.run(debug=True)