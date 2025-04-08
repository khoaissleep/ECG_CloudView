import requests
import time
import math
import random
from collections import deque

SERVER_URL = "http://127.0.0.1:5000/update_data"
SEND_INTERVAL_SECONDS = 0.05 # Gửi dữ liệu mỗi 50ms
POINTS_PER_SEND = 10       # Gửi 10 điểm mỗi lần

# Biến toàn cục để theo dõi vị trí trong chu kỳ sóng ECG mô phỏng
current_pos = 0
cycle_length = 100 # Độ dài 1 chu kỳ (100 mẫu @ 200 mẫu/giây => 2Hz/120BPM)
                   # (10 mẫu / 0.05s = 200 mẫu/giây)

def generate_ecg_like_points(num_points):
    """Tạo ra các điểm dữ liệu mô phỏng sóng ECG đơn giản."""
    global current_pos, cycle_length
    points = []
    for _ in range(num_points):
        # Đường nền quanh 512 (phù hợp ADC 10-bit trên dashboard)
        val = 512
        pos_in_cycle = current_pos % cycle_length

        # Mô phỏng phức bộ QRS (nhọn)
        if 10 <= pos_in_cycle < 15: # Nhánh lên của R
            val += (pos_in_cycle - 10) * 80
        elif 15 <= pos_in_cycle < 20: # Nhánh xuống của R + S
             val += (20 - pos_in_cycle) * 80
        # Mô phỏng sóng T (tròn hơn)
        elif 40 <= pos_in_cycle < 60:
            val += 100 * math.sin((pos_in_cycle - 40) / 20 * math.pi) # Biên độ 100

        # Thêm nhiễu ngẫu nhiên
        val += random.randint(-15, 15)

        # Giữ giá trị trong khoảng 0-1023
        points.append(max(0, min(1023, int(val))))
        current_pos += 1 # Di chuyển đến vị trí tiếp theo trong chu kỳ
    return points

print(f"Mock Sender started. Sending {POINTS_PER_SEND} points every {SEND_INTERVAL_SECONDS} seconds to {SERVER_URL}")

while True:
    try:
        ecg_sample = generate_ecg_like_points(POINTS_PER_SEND)
        response = requests.post(SERVER_URL, json={"data": ecg_sample})
        response.raise_for_status() # Báo lỗi nếu status code là 4xx hoặc 5xx
        # print(f"Sent: {ecg_sample}") # Bỏ comment để debug
    except requests.exceptions.RequestException as e:
        # Bắt lỗi kết nối hoặc lỗi HTTP
        print(f"Error sending data: {e}")
        # Đợi một chút trước khi thử lại để tránh spam lỗi quá nhanh
        time.sleep(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        time.sleep(1)

    # Đợi khoảng thời gian đã định trước khi gửi lần tiếp theo
    time.sleep(SEND_INTERVAL_SECONDS)