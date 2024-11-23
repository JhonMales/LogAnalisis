import json
import os
import re
import requests


# Rutas de los archivos de log
access_log_path = ""
error_log_path = ""
output_json_path = ""

# Expresión regular para parsear los logs de acceso
log_pattern = re.compile(
    r'(?P<ip>\S+) - (?P<user>\S+) \[(?P<time>.+?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status>\d+) (?P<bytes>\d+) "(?P<referer>[^"]*)" "(?P<agent>[^"]*)"'
)

def parse_access_log(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    return None

def read_logs(log_path):
    if not os.path.exists(log_path):
        print(f"El archivo {log_path} no existe.")
        return []
    with open(log_path, 'r') as log_file:
        return log_file.readlines()

def filter_relevant_logs(logs):
    filtered_logs = []
    for log in logs:
        if log['type'] == 'access' and int(log['data']['status']) >= 400:
            filtered_logs.append(log)
        elif log['type'] == 'error':
            filtered_logs.append(log)
    return filtered_logs

def preprocess_logs(logs):
    preprocessed_logs = []
    seen_logs = set()  # Para rastrear entradas ya procesadas
    
    for log in logs:
        if log['type'] == 'access':
            entry = f"IP {log['data']['ip']} intentó acceder a {log['data']['url']} y obtuvo el código de estado {log['data']['status']}."
            if entry not in seen_logs:
                preprocessed_logs.append(entry)
                seen_logs.add(entry)
        elif log['type'] == 'error':
            entry = f"Error registrado: {log['data']}"
            if entry not in seen_logs:
                preprocessed_logs.append(entry)
                seen_logs.add(entry)
    
    return preprocessed_logs


def save_preprocessed_logs(preprocessed_logs, output_path):
    with open(output_path, 'w') as output_file:
        json.dump(preprocessed_logs, output_file, indent=4)

def process_logs():
    logs = []
    
    access_logs = read_logs(access_log_path)
    for line in access_logs:
        log_data = parse_access_log(line)
        if log_data:
            logs.append({"type": "access", "data": log_data})
        else:
            print(f"Línea de acceso no válida: {line.strip()}")

    error_logs = read_logs(error_log_path)
    for line in error_logs:
        logs.append({"type": "error", "data": line.strip()})

    relevant_logs = filter_relevant_logs(logs)

    preprocessed_logs = preprocess_logs(relevant_logs)

    save_preprocessed_logs(preprocessed_logs, output_json_path)
    print(f"Logs preprocesados y guardados en: {output_json_path}")

if __name__ == "__main__":
    process_logs()
