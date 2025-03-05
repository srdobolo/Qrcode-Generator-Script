# First, install the required library by running: pip install qrcode pillow
# 'qrcode' generates the QR code, and 'pillow' (PIL) handles the image output

import qrcode

# Define the data you want to encode in the QR code
data = "https://www.recruityard.com"  # Replace this with your URL, text, or anything else

# Create a QR code instance with some basic settings
qr = qrcode.QRCode(
    version=1,              # Controls the size (1 is smallest, can go up to 40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level (L = ~7% correction)
    box_size=10,            # Size of each "box" (pixel size of the squares)
    border=4,               # Thickness of the border (in boxes)
)

# Add the data to the QR code
qr.add_data(data)
qr.make(fit=True)  # Automatically adjust the size to fit the data

# Generate the QR code as an image
qr_image = qr.make_image(fill_color="black", back_color="white")

# Save the image to a file
qr_image.save("my_qrcode.png")  # You can change the filename or path here

print("QR code generated and saved as 'my_qrcode.png'!")