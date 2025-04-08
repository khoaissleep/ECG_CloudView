from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Biến toàn cục để lưu dữ liệu ECG
ecg_data = []

@app.route('/')
def index():
    return render_template('index.html', ecg_data=ecg_data)

# Endpoint nhận dữ liệu từ mock_sender (hoặc ESP32)
@app.route('/update_data', methods=['POST'])
def update_data():
    global ecg_data
    data = request.json
    ecg_data = data.get("data", [])
    return jsonify({"status": "success"}), 200

# Endpoint trả về dữ liệu ECG cho web
@app.route('/get_data')
def get_data():
    global ecg_data
    return jsonify({"data": ecg_data})

if __name__ == '__main__':
    app.run(debug=True)
