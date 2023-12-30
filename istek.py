import requests
import json
import time
# Gönderilecek JSON verisi
data = {
    "eventId": "5904321",
    "otpId": "iFrpsrOLRO4qtXkug1YT4GWqeJ71P+mImafdGZ4J8AXqkcWQNx2EnWrpNo+j/JCJE29uWZG/Lja912PSW8yQ1azvbEHW6AaCrKmGKgDHVQEfxk51L2DeNKIVeOLlJKbM",
    "sessionId": "e9ed7a2a-7e21-4a77-9d81-60f91e4ae530",
    "refreshtoken": "04523c86-2e5f-492d-a4b4-48cfcca7d2bf",
    "deviceId": "cd8df8dbb2dbee97"
}

url_start = "http://104.247.166.78:5000/start_try"
url_stop = "http://104.247.166.78:5000/stop_try"

headers = {"Content-Type": "application/json"}

# Start endpoint'i için bir istek gönder
response_start = requests.post(url_start, headers=headers, json=data)

# GUID'yi alma
guid = response_start.json().get('message').split("GUID: ")[1].replace(")", "")

print(f"Başlatılan işlem GUID: {guid}")

time.sleep(5)
# Stop endpoint'i için bir istek gönder ve GUID ile hangi işlemi durduracağını belirt

response_stop = requests.post(url_stop, headers=headers, json={"guid": guid})
#
## Yanıtı ekrana yazdır
print(response_stop.json())
