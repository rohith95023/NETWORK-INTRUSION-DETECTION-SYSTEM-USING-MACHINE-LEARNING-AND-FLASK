import os
import logging
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import joblib

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load model and encoders
model = joblib.load('models/network_intrusion_model.pkl')
protocol_type_encoder = joblib.load('models/protocol_type_encoder.pkl')
service_encoder = joblib.load('models/service_encoder.pkl')
flag_encoder = joblib.load('models/flag_encoder.pkl')
label_encoder = joblib.load('models/label_encoder.pkl')

# Safe encoding function
def safe_encode(label, encoder):
    try:
        return encoder.transform([label])[0]
    except ValueError:
        return encoder.transform([encoder.classes_[0]])[0]

# Default route
@app.route('/')
def default():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            error = 'Please fill out all fields.'
            return render_template('login.html', error=error)
        elif '@' not in email:
            error = 'Invalid email address. Please include "@" in the email.'
            return render_template('login.html', error=error)
        else:
            return redirect(url_for('index'))
    return render_template('login.html')

# Home route
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

# Predict route for form input
@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_data = request.form
        required_fields = [
            'duration', 'protocol_type', 'service', 'flag', 
            'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 
            'urgent', 'hot', 'num_failed_logins', 'root_shell'
        ]

        # Validate fields
        for field in required_fields:
            if field not in form_data or not form_data[field].strip():
                return render_template('prediction.html', error=f"Field '{field}' is missing or invalid!")

        # Prepare features
        features = [
            float(form_data['duration']),
            safe_encode(form_data['protocol_type'], protocol_type_encoder),
            safe_encode(form_data['service'], service_encoder),
            safe_encode(form_data['flag'], flag_encoder),
            float(form_data['src_bytes']),
            float(form_data['dst_bytes']),
            int(form_data['land']),
            float(form_data['wrong_fragment']),
            float(form_data['urgent']),
            float(form_data['hot']),
            float(form_data['num_failed_logins']),
            int(form_data['root_shell'])
        ]

        # Predict and decode output
        prediction = model.predict([features])
        output = label_encoder.inverse_transform(prediction)[0]
        return render_template('prediction.html', output=f"Attack Class: {output}")
    except Exception as e:
        logging.error("Error during prediction: %s", str(e))
        return render_template('prediction.html', error=f"Error: {str(e)}")

# Bulk upload route for CSV
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'csvfile' not in request.files:
            return render_template('upload.html', error="No file uploaded!")

        file = request.files['csvfile']
        try:
            # Read CSV
            df = pd.read_csv(file)
            required_columns = [
                'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
                'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'root_shell'
            ]

            # Validate columns
            if not all(column in df.columns for column in required_columns):
                missing_columns = [col for col in required_columns if col not in df.columns]
                return render_template('upload.html', error=f"Missing columns: {', '.join(missing_columns)}")

            # Encode and predict
            df['protocol_type'] = df['protocol_type'].apply(lambda x: safe_encode(x, protocol_type_encoder))
            df['service'] = df['service'].apply(lambda x: safe_encode(x, service_encoder))
            df['flag'] = df['flag'].apply(lambda x: safe_encode(x, flag_encoder))
            features = df[required_columns].values
            predictions = model.predict(features)
            df['Prediction'] = label_encoder.inverse_transform(predictions)

            # Save results
            results_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
            df.to_csv(results_filepath, index=False)
            results_html = df.to_html(classes='table table-striped', index=False)
            return f"""
            <!DOCTYPE html>
            <html>
              <head>
                <title>Results</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" />
              </head>
              <body class="container mt-5">
                <h2 class="text-center">Prediction Results</h2>
                {results_html}
                <div class="text-center mt-3">
                  <a href="/download/results.csv" class="btn btn-success">Download CSV</a>
                </div>
                <div class="text-center mt-3">
                  <a href="/index" class="btn btn-primary">Home</a>
                </div>
              </body>
            </html>
            """
        except Exception as e:
            logging.error("Error processing file: %s", str(e))
            return render_template('upload.html', error=f"Error: {str(e)}")
    return render_template('upload.html')

# Download results
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# API for JSON input
@app.route('/results', methods=['POST'])
def results():
    try:
        data = request.get_json(force=True)
        required_fields = [
            'duration', 'protocol_type', 'service', 'flag', 
            'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 
            'urgent', 'hot', 'num_failed_logins', 'root_shell'
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        features = [
            float(data['duration']),
            safe_encode(data['protocol_type'], protocol_type_encoder),
            safe_encode(data['service'], service_encoder),
            safe_encode(data['flag'], flag_encoder),
            float(data['src_bytes']),
            float(data['dst_bytes']),
            int(data['land']),
            float(data['wrong_fragment']),
            float(data['urgent']),
            float(data['hot']),
            float(data['num_failed_logins']),
            int(data['root_shell'])
        ]

        prediction = model.predict([features])
        output = label_encoder.inverse_transform(prediction)[0]
        return jsonify({"Prediction": output})
    except Exception as e:
        logging.error("Error during prediction: %s", str(e))
        return jsonify({"error": f"Error: {str(e)}"}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
