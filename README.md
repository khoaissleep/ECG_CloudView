# ECG CloudView

## Overview
ECG CloudView is a web-based real-time electrocardiogram (ECG) monitoring system that allows for visualization and analysis of ECG signals. The system consists of a Flask backend server, a responsive web interface, and a data simulator for demonstration purposes.

## Features
- Real-time ECG waveform visualization
- Heart rate (BPM) calculation
- R-R interval measurement
- Signal quality assessment
- Automatic anomaly detection (bradycardia, tachycardia)
- Responsive web interface

## Requirements
- Python 3.6+
- Flask
- Flask-CORS
- Requests
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ECG_CloudView.git
cd ECG_CloudView
```

2. Install required Python packages:
```bash
pip install flask flask-cors requests
```

3. Ensure the correct directory structure:
```
ECG_CloudView/
  ├── API.py           # Backend server
  ├── mock_sender.py   # Data simulator
  └── static/          # Frontend files
      └── index.html   # Web dashboard
```

## Usage

### Start the server
```bash
python API.py
```
The server will start on http://localhost:5000

### Generate demo data
```bash
python mock_sender.py
```
This will simulate ECG data and send it to the server.

### View the dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

## Components

### API.py (Backend)
- REST API server built with Flask
- Endpoints:
  - `POST /update_data` - Receives ECG data points
  - `GET /ecg` - Provides the latest 500 data points
  - `GET /` - Serves the web interface

### mock_sender.py
- Generates simulated ECG waveforms
- Configurable parameters:
  - `SEND_INTERVAL_SECONDS` - Data transmission frequency
  - `POINTS_PER_SEND` - Number of data points per transmission
  - `cycle_length` - Controls heart rate (smaller = faster)

### index.html (Frontend)
- Responsive dashboard using Chart.js
- Real-time signal processing:
  - R-peak detection algorithm
  - Heart rate calculation
  - Signal quality estimation
- Configurable display parameters

## Customization

### Adjusting ECG simulation parameters
Edit `mock_sender.py` to change:
```python
SEND_INTERVAL_SECONDS = 0.05  # Update frequency (seconds)
POINTS_PER_SEND = 10          # Points per update
cycle_length = 100            # ECG cycle length (100 samples @ 200Hz = 120 BPM)
```

### Modifying the dashboard
Edit `static/index.html` to customize:
```javascript
const SAMPLE_RATE = 250;         // Hz - Sampling frequency
const CHART_POINTS = 500;        // Number of points to display
const FETCH_INTERVAL = 500;      // Milliseconds between API calls
const ANALYSIS_WINDOW_SECONDS = 4; // Analysis window size
```

## Troubleshooting

### No data appearing on dashboard
- Ensure both API.py and mock_sender.py are running
- Check browser console (F12) for errors
- Verify mock_sender.py is using the correct server URL
- Check if port 5000 is already in use by another application

### Connection issues
- Ensure the server host is set correctly in API.py
- If running on a network, make sure your firewall allows the connection
- Try using localhost (127.0.0.1) instead of 0.0.0.0

## Disclaimer
This system is designed for educational and demonstration purposes only and is not intended for clinical use or diagnosis.