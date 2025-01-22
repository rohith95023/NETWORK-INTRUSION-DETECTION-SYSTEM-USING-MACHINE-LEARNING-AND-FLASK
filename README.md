# NETWORK-INTRUSION-DETECTION-SYSTEM-USING-MACHINE-LEARNING-AND-FLASK




Network Intrusion Detection System (NIDS)
Overview
The Network Intrusion Detection System (NIDS) is a machine learning-based project designed to identify and classify network intrusions. It employs a web-based interface for real-time predictions and bulk predictions via CSV uploads. This system uses a Random Forest model to detect various types of attacks, including Denial of Service (DoS), Probe, Remote-to-Local (R2L), and User-to-Root (U2R).

Features
Manual Input for Predictions: Users can manually input network attributes to predict potential attacks.
Batch Predictions via CSV: Upload CSV files with network data for bulk predictions.
Real-Time Malware Detection: Provides immediate insights into network activity.
Interactive Visualization: View attack classifications and associated details.
Secure and User-Friendly Interface: Login and account creation functionalities ensure ease of use.



Project Structure

├── app.py                  # Flask backend implementation
├── models/                 # Trained model and encoders
│   ├── network_intrusion_model.pkl
│   ├── protocol_type_encoder.pkl
│   ├── service_encoder.pkl
│   ├── flag_encoder.pkl
│   └── label_encoder.pkl
├── static/                 # Static files for styling
│   ├── css/
│   ├── js/
│   └── uploads/            # Directory for uploaded CSV files
├── templates/              # HTML templates for web pages
│   ├── login.html
│   ├── index.html
│   ├── prediction.html
│   ├── upload.html
│   └── ...
├── dataset/                # Sample datasets for testing
├── requirements.txt        # Python dependencies
└── README.md               # Documentation



Installation
Clone the repository(CMD):
git clone https://github.com/yourusername/nids.git
cd nids


Create a virtual environment(CMD):
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`


Install dependencies:

pip install -r requirements.txt
Ensure the models directory exists with the required .pkl files.

Usage:
Start the Flask server:
python app.py
Open your browser and navigate to http://127.0.0.1:5000.

Use the following features:

Login/Register: Authenticate to access the application.
Predict: Enter network parameters manually for predictions.
Upload CSV: Predict attacks in bulk by uploading CSV files.
Dataset
The dataset used for training is a network intrusion dataset with features like:

duration, protocol_type, service, flag, etc.
Target classes include:
0: Normal
1: Denial of Service (DoS)
2: Probe
3: Remote-to-Local (R2L)
4: User-to-Root (U2R)
For testing, download the sample dataset from the application.

Model Training
The system employs a Random Forest Classifier. Key steps include:

Data preprocessing and label encoding.
Model training and evaluation using sklearn.
Saving the trained model and encoders for deployment.
Refer to the model_training_code.py for detailed implementation.

Screenshots
Login Page

Prediction Page

Upload Page

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch.
Commit your changes and push the branch.
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Author
G. ROHITH
