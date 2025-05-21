import os
import qrcode
from flask import Flask, request, render_template

app = Flask(__name__)

# Defina o diretório onde os códigos QR serão armazenados
QR_CODE_DIR = 'static/qr_codes'  # Certifique-se de que esta pasta existe e tem permissões de escrita

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    if request.method == "POST":
        # Obter o URL do formulário
        url = request.form.get("url")
        if url:
            # Gerar código QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Guardar o código QR com um nome de ficheiro único
            filename = f"qr_{hash(url) % 10000}.png"
            # Verifique se o diretório existe
            if not os.path.exists(QR_CODE_DIR):
                os.makedirs(QR_CODE_DIR)

            filepath = os.path.join(QR_CODE_DIR, filename)
            qr_image.save(filepath)

            # Calcular o caminho relativo a partir do diretório base da aplicação
            qr_image = os.path.relpath(filepath, start='static')

    return render_template("index_copy.html", qr_image=qr_image)

if __name__ == '__main__':
    app.run(debug=True)