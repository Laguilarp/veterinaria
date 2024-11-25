import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Configuración del servidor SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'infomedipets@gmail.com'
EMAIL_PASSWORD = 'fdrj pkrk gtkf uawl'  # Usar contraseña de aplicación si es Gmail


def enviar_correo(destinatario, asunto, mensaje, archivo=None):
    try:
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = destinatario
        msg['Subject'] = asunto

        # Cuerpo del mensaje
        msg.attach(MIMEText(mensaje, 'html'))

        # Adjuntar archivo (si se proporciona)
        if archivo:
            with open(archivo, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={archivo.split("/")[-1]}'
            )
            msg.attach(part)

        # Conexión al servidor SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"Correo enviado a {destinatario}")

    except Exception as e:
        print(f"Error al enviar el correo: {e}")