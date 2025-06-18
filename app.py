import qrcode
from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Folder to store generated QR codes
QR_CODE_DIR = os.path.join(app.static_folder, "qr_codes")
os.makedirs(QR_CODE_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_image = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            filename = f"qr_{hash(url) % 10000}.png"
            filepath = os.path.join(QR_CODE_DIR, filename)
            qr_img.save(filepath)

            qr_image = f"qr_codes/{filename}"

    return render_template("index.html", qr_image=qr_image)

if __name__ == "__main__":
    app.run(debug=True)