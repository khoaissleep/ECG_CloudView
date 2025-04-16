#include <WiFi.h>
#include <HTTPClient.h>

// ==== CẤU HÌNH MẠNG ====
const char* ssid = "AICLUB_B8.2";
const char* password = "aiclub_uit";
const String serverUrl = "http://192.168.0.151:5000/update_data";

// ==== KHAI BÁO CHÂN ====
#define ECG_PIN 36
#define LO_PLUS_PIN 35
#define LO_MINUS_PIN 34

// Bộ đệm
const int BUFFER_SIZE = 100;
int ecgBuffer[BUFFER_SIZE];
int bufferIndex = 0;

unsigned long lastSendTime = 0;
const unsigned long SEND_INTERVAL = 500;

void sendDataToServer(int* data, int size) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{\"data\": [";
    for (int i = 0; i < size; i++) {
      jsonPayload += String(data[i]);
      if (i < size - 1) jsonPayload += ",";
    }
    jsonPayload += "]}";

    int httpResponseCode = http.POST(jsonPayload);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    http.end();
  } else {
    Serial.println("Error: WiFi not connected");
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(LO_PLUS_PIN, INPUT);
  pinMode(LO_MINUS_PIN, INPUT);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected.");
}

void loop() {
  int loPlus = digitalRead(LO_PLUS_PIN);
  int loMinus = digitalRead(LO_MINUS_PIN);

  if (loPlus == 1 || loMinus == 1) {
    Serial.println("0"); // mất điện cực
    delay(5);
    return;
  }

  int rawEcg = analogRead(ECG_PIN);   // Đọc giá trị raw
  ecgBuffer[bufferIndex++] = rawEcg;

  Serial.println(rawEcg);             // In raw ra serial plotter

  if (millis() - lastSendTime >= SEND_INTERVAL && bufferIndex == BUFFER_SIZE) {
    sendDataToServer(ecgBuffer, BUFFER_SIZE);
    bufferIndex = 0;
    lastSendTime = millis();
  }

  delay(5); // ~200Hz sampling rate
}
