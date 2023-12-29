import requests
import json
import time
# Gönderilecek JSON verisi
data = {
    "eventId": "5860325",
    "otpId": "V1+JRsjRdZL2PDfly9EnDQxB8itxIOLpA7508kT94hHdBovT5BAqJ+pT+7xc+yMnMl3WaFdL6w9XsUV6jDR5b14UOGhzRQSzeuuE6Gp/wzfhZhSO+OoxDXBm5I2TV0zj",
    "sessionId": "4aa56104-5895-4dec-a51e-e0981af29a7a",
    "refreshtoken": "04523c86-2e5f-492d-a4b4-48cfcca7d2bf",
    "deviceId": "bee8bd17fa220847"
}

url_start = "http://localhost:5000//start_try"
url_stop = "http://127.0.0.1:5000/stop_try"

headers = {"Content-Type": "application/json"}

# Start endpoint'i için bir istek gönder
response_start = requests.post(url_start, headers=headers, json=data)

# GUID'yi alma
guid = response_start.json().get('message').split("GUID: ")[1].replace(")", "")

print(f"Başlatılan işlem GUID: {guid}")

time.sleep(5)
# Stop endpoint'i için bir istek gönder ve GUID ile hangi işlemi durduracağını belirt

#response_stop = requests.post(url_stop, headers=headers, json={"guid": guid})
#
## Yanıtı ekrana yazdır
#print(response_stop.json())
