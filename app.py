from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Cargar el archivo log_analysis_results.json y parsear los datos
def load_log_data():
    with open('log_analysis_results.json', 'r') as f:
        data = json.load(f)
    return data

@app.route('/')
def index():
    log_data = load_log_data()
    return render_template('index.html', log_data=log_data)

if __name__ == '__main__':
    app.run(debug=True)
