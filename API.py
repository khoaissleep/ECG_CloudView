from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import deque
import threading

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

MAX_DATA_POINTS = 1000  # Lưu tối đa 1000 điểm ECG
ecg_data_store = deque(maxlen=MAX_DATA_POINTS)
data_lock = threading.Lock()

@app.route('/update_data', methods=['POST'])
def update_data():
    try:
        data = request.get_json()
        if not data or 'data' not in data or not isinstance(data['data'], list):
            return jsonify({"error": "Invalid data format. Expected {'data': [list_of_numbers]}"}), 400

        new_points = data['data']
        print(f"[ECG] Received: {len(new_points)} points")

        with data_lock:
            ecg_data_store.extend(new_points)

        return jsonify({"message": "Data received"}), 200
    except Exception as e:
        print(f"Error in /update_data: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/ecg', methods=['GET'])
def get_ecg_data():
    try:
        with data_lock:
            latest_data = list(ecg_data_store)[-500:]  # Lấy 500 điểm mới nhất (nếu có)
        return jsonify({"ecgData": latest_data})
    except Exception as e:
        print(f"Error in /ecg: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Route để phục vụ giao diện web (index.html)
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    print("Flask server running at http://localhost:5000")
    # Bạn có thể bật debug=True để kiểm tra lỗi khi phát triển
    app.run(host='0.0.0.0', port=5000, debug=True)
