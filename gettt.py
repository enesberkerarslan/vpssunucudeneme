import requests
import json
import time
url_stop = "http://127.0.0.1:5000/status"

headers = {"Content-Type": "application/json"}

# Start endpoint'i için bir istek gönder
response_start = requests.get(url_stop, headers=headers)
print(response_start.text)