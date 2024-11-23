import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_alerta_vulnerabilidad(sender_email, password, receiver_email, ip_address):
    # Configuración del mensaje
    asunto = "Alerta de Seguridad: Posible Vulnerabilidad de Acceso"
    cuerpo = f"""
    ¡Alerta!

    Se ha detectado una posible vulnerabilidad de acceso desde la IP: {ip_address}.
    Esto puede ser indicativo de un ataque de fuerza bruta u otra actividad sospechosa.

    Por favor, toma las medidas necesarias para investigar este incidente.

    Atentamente,
    Tu Sistema de Monitoreo
    """

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = sender_email
    mensaje['To'] = receiver_email
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Enviar el correo
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()  # Seguridad
            servidor.login(sender_email, password)
            servidor.send_message(mensaje)
            print("Alerta enviada correctamente.")
    except Exception as e:
        print(f"Error al enviar la alerta: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Configura las credenciales
    sender_email = ""
    password = ""  # Usa una contraseña de aplicación con 2FA habilitado
    receiver_email = ""  # Cambia a la dirección de correo del destinatario

    enviar_alerta_vulnerabilidad(sender_email, password, receiver_email, ip_address)
