import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(ticket):
    qr_data = f"{ticket.id}|{ticket.user.id}|{ticket.event.id}"
    qr_img = qrcode.make(qr_data)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    filename = f"ticket_{ticket.id}.png"
    ticket.qr_code_image.save(filename, File(buffer), save=True)
