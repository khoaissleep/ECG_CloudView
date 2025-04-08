from flask import Flask, request, jsonify
from flask_cors import CORS # Thư viện để xử lý CORS
from collections import deque # Dùng deque để lưu trữ dữ liệu hiệu quả
import threading # Dùng lock để đảm bảo an toàn khi nhiều request truy cập dữ liệu

app = Flask(__name__)
# Kích hoạt CORS cho endpoint /ecg, cho phép tất cả các nguồn gốc (*)
# Trong môi trường production, bạn nên giới hạn origins cụ thể
CORS(app, resources={r"/ecg": {"origins": "*"}})

# Giới hạn số lượng điểm dữ liệu lưu trữ để tránh dùng quá nhiều bộ nhớ
# Dashboard hiển thị 500 điểm. Sender gửi 10 điểm/50ms => 200 điểm/giây.
# Lưu trữ khoảng 5 giây = 1000 điểm là hợp lý.
MAX_DATA_POINTS = 1000
# deque sẽ tự động loại bỏ các phần tử cũ khi đạt đến maxlen
ecg_data_store = deque(maxlen=MAX_DATA_POINTS)
data_lock = threading.Lock() # Khóa để tránh xung đột khi đọc/ghi dữ liệu

@app.route('/update_data', methods=['POST'])
def update_data():
    """Endpoint nhận dữ liệu từ mock_sender.py"""
    try:
        data = request.get_json()
        # Kiểm tra xem dữ liệu gửi lên có đúng định dạng không
        if not data or 'data' not in data or not isinstance(data['data'], list):
            return jsonify({"error": "Invalid data format. Expected {'data': [list_of_numbers]}"}), 400

        new_points = data['data']
        # print(f"Received: {len(new_points)} points") # Bỏ comment để debug

        # Dùng lock để đảm bảo an toàn khi thêm dữ liệu
        with data_lock:
            ecg_data_store.extend(new_points) # Thêm dữ liệu mới vào deque

        return jsonify({"message": "Data received successfully"}), 200
    except Exception as e:
        print(f"Error in /update_data: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/ecg', methods=['GET'])
def get_ecg_data():
    """Endpoint cung cấp dữ liệu cho dashboard JavaScript"""
    try:
        # Dùng lock để đảm bảo an toàn khi đọc dữ liệu
        with data_lock:
            # Lấy tối đa 500 điểm dữ liệu gần nhất từ deque
            # Dashboard chỉ hiển thị 500 điểm
            latest_data = list(ecg_data_store)[-500:]

        # JavaScript mong đợi đối tượng JSON có key là "ecgData"
        response_data = {"ecgData": latest_data}
        # print(f"Sending to dashboard: {len(latest_data)} points") # Bỏ comment để debug
        return jsonify(response_data)
    except Exception as e:
        print(f"Error in /ecg: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("Starting Flask server on http://127.0.0.1:5000")
    print("Endpoints:")
    print("  POST /update_data - Receives data from mock_sender.py")
    print("  GET  /ecg        - Provides latest data to the dashboard")
    # Chạy server, debug=False để ổn định hơn
    app.run(host='127.0.0.1', port=5000, debug=False)