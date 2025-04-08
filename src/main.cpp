#include <WiFi.h>
#include <HTTPClient.h>

// Thông tin kết nối WiFi
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

// Địa chỉ IP của Flask Server (localhost hoặc IP của máy chủ)
const String serverUrl = "http://192.168.1.100:5000";  // Đổi IP thành địa chỉ máy chạy Flask

void setup() {
  Serial.begin(115200);

  // Kết nối WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");

  // Dữ liệu giả lập ECG
  int ecgData[100];
  for (int i = 0; i < 100; i++) {
    ecgData[i] = random(0, 1023); // Tạo dữ liệu ngẫu nhiên
  }

  // Gửi dữ liệu ECG đến Flask server
  sendDataToServer(ecgData, 100);
}

void loop() {
  // Dữ liệu có thể được gửi theo chu kỳ hoặc khi cần thiết
}

void sendDataToServer(int* data, int size) {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);  // URL của Flask server

    http.addHeader("Content-Type", "application/json");

    // Tạo JSON từ dữ liệu ECG
    String jsonPayload = "{\"data\": [";
    for (int i = 0; i < size; i++) {
      jsonPayload += String(data[i]);
      if (i < size - 1) jsonPayload += ",";
    }
    jsonPayload += "]}";

    // Gửi POST request
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response Code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    // Đóng kết nối
    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }
}
