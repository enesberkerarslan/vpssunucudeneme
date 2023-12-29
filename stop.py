import requests
import json

url_stop = "http://127.0.0.1:5000/stop_try"

headers = {"Content-Type": "application/json"}

# Start endpoint'i için bir istek gönder
# Stop endpoint'i için bir istek gönder ve GUID ile hangi işlemi durduracağını belirt
response_stop = requests.post(url_stop, headers=headers, json={"guid": "a4ae024e-24fe-41e0-a68f-e9518c6116d1"})

# Yanıtı ekrana yazdır
print(response_stop.json())

# GUID'yi alma

