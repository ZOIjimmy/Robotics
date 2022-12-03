#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

#ifndef STASSID
#define STASSID "AP SSID"  //無線分享器的名稱
#define STAPSK  "xxxxx"    //密碼
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(80);

void handleRoot() {  //訪客進入主網頁時顯示的內容
  server.send(200, "text/plain", "Hello From ESP8266 !");
}

void handleNotFound() {  //找不到網頁時顯示的內容
  server.send(404, "text/plain", "File Not Found");
}

void setup(void) {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // 等待WiFi連線
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  //在監控視窗顯示取得的IP

  if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);  //綁定主網頁會觸發的副程式

  server.onNotFound(handleNotFound);  //綁定找不到網頁時會觸發的副程式

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  MDNS.update();
}