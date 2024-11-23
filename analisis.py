import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai  
import time

# Datos del proyecto
project_number = ''
project_name = ''
api_key = ''


genai.configure(api_key=api_key)
# Inicializa el modelo de Gemini
model = genai.GenerativeModel("gemini-1.5-flash")

# Ruta al archivo preprocesado de logs
preprocessed_log_path = ""


# Función de envío de correos electrónicos
def send_email_alert(log_entry, analysis):
    sender_email = ""
    receiver_email = ""
    password = ""
    
    subject = "Alerta de seguridad: Comportamiento sospechoso detectado"
    body = f"Se detectó un comportamiento sospechoso en el siguiente registro:\n\nLog: {log_entry}\nAnálisis: {analysis}"
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Alerta enviada: {log_entry}")
    except Exception as e:
        print(f"Error al enviar alerta: {e}")

def load_preprocessed_logs(log_path):
    """Carga los logs preprocesados desde un archivo JSON"""
    with open(log_path, 'r') as log_file:
        return json.load(log_file)

def analyze_log(log_entry):
    """Analiza un registro individual de log usando la API de Gemini"""
    try:
        response = model.generate_content(f"Analiza el siguiente registro de log y detecta comportamientos sospechosos: {log_entry}")
        # Acceder al contenido de la respuesta
        analysis_text = response.text  
        return analysis_text
    except Exception as e:
        print(f"Error al analizar el log: {log_entry}")
        print(f"Detalles: {e}")
        return None

def process_and_analyze_logs():
    preprocessed_logs = load_preprocessed_logs(preprocessed_log_path)
    analysis_results = []

    for log_entry in preprocessed_logs:
        analysis = analyze_log(log_entry)
        if analysis:
            analysis_results.append({"log": log_entry, "analysis": analysis})


        # Pausa entre las solicitudes
        time.sleep(1)  # Ajusta el tiempo según sea necesario

    # Guardar los resultados del análisis
    output_analysis_path = ""
    with open(output_analysis_path, 'w') as output_file:
        json.dump(analysis_results, output_file, indent=4)
    print(f"Análisis completado. Los resultados se guardaron en: {output_analysis_path}")

if __name__ == "__main__":
    process_and_analyze_logs()