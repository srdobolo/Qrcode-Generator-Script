import qrcode
from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Folder to store QR code images
QR_CODE_DIR = os.path.join("static", "qr_codes")
if not os.path.exists(QR_CODE_DIR):
    os.makedirs(QR_CODE_DIR)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_image = None
    if request.method == "POST":
        # Get URL from form
        url = request.form.get("url")
        if url:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Save QR code with a unique filename
            filename = f"qr_{hash(url) % 10000}.png"
            filepath = os.path.join(QR_CODE_DIR, filename)
            qr_image.save(filepath)

            # Pass relative path for frontend
            qr_image = f"qr_codes/{filename}"

    return render_template("index.html", qr_image=qr_image)

@app.route("/static/qr_codes/<filename>")
def serve_qr_code(filename):
    return send_from_directory(QR_CODE_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)