import requests
import json
import time
# Gönderilecek JSON verisi
data = {
    "eventId": "5904321",
    "otpId": "+sa4SIHM57lF6Td5Sv3nT5Yecffi+ixejW6uDrG5enRnkU1yrQ7k/f0UeQ4EhmZ6dT1V8IJrsS76kyqUIVK08wxHDywheKNfx5HHv+orDWnKB425zY4rD6ZZuJBZB/yK",
    "sessionId": "8d079c94-5ff9-4b5e-87fe-67e4d509a241",
    "refreshtoken": "328d53b2-f8cb-46c6-a044-8df1d8501fb5",
    "deviceId": "fca199647967b92c"
}

url_start = "http://104.247.166.78:5000/start_try"
url_stop = "http://104.247.166.78:5000/stop_try"

headers = {"Content-Type": "application/json"}

# Start endpoint'i için bir istek gönder
response_start = requests.post(url_start, headers=headers, json=data)

# GUID'yi alma
guid = response_start.json().get('message').split("GUID: ")[1].replace(")", "")

print(response_start.text)

time.sleep(55)
# Stop endpoint'i için bir istek gönder ve GUID ile hangi işlemi durduracağını belirt

response_stop = requests.post(url_stop, headers=headers, json={"guid": guid})
#
## Yanıtı ekrana yazdır
print(response_stop.json())
