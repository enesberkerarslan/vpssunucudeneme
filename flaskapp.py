from flask import Flask, request ,  jsonify
import threading
from Main import MobileBot
import time
import uuid
import os


stop_flags = {}
bots = {}  # Her bir GUID için MobileBot'u saklamak için bir sözlük
is_active = {}  # Her bir GUID için işlemin aktif olup olmadığını saklamak için bir sözlük
app = Flask(__name__)
total_started_accounts = 0

def ticket_try(guid,data):
    global total_started_accounts
    eventId = data.get('eventId')
    otpId = data.get('otpId')
    sessionId = data.get('sessionId')
    refreshtoken = data.get('refreshtoken')
    deviceId = data.get('deviceId')

    mobile_bot = MobileBot(eventId,otpId,sessionId,refreshtoken,deviceId)
    response = mobile_bot.halfLogin()
    if response != "Login Succesfully":
        print(response)
        return response
    mobile_bot.categoryId = "7010426"

    bots[guid] = mobile_bot
    is_active[guid] = True
    total_started_accounts = total_started_accounts +1
    start = time.time()
    while is_active[guid]:
        try:
            mobile_bot.biletAl()
        except Exception as e:
            print(f"Bilinmeyen bir hata oluştu: Flask-App İçinde {e}")
            time.sleep(3)
        if time.time() - start> 900:
            print("Belirli bir süre boyunca işlem gerçekleşmedi. Yeniden başlatılıyor...")
            return ticket_try(guid, data)

    print("Durduruldu")
    total_started_accounts = total_started_accounts -1
    del bots[guid]
    del is_active[guid]

@app.route('/check_information', methods=['POST'])
def check_information():
    data = request.get_json()  # Gelen veriyi alın

    # Her istekle birlikte yeni bir işlem oluşturun
    eventId = data.get('eventId')
    otpId = data.get('otpId')
    sessionId = data.get('sessionId')
    refreshtoken = data.get('refreshtoken')
    deviceId = data.get('deviceId')

    mobile_bot = MobileBot(eventId,otpId,sessionId,refreshtoken,deviceId)
    response = mobile_bot.halfLogin()

    return {'status': 'success', 'message': response}

@app.route('/get_categories', methods=['POST'])
def get_categories():
    data = request.get_json()  # Gelen veriyi alın

    # Her istekle birlikte yeni bir işlem oluşturun
    eventId = data.get('eventId')
    otpId = data.get('otpId')
    sessionId = data.get('sessionId')
    refreshtoken = data.get('refreshtoken')
    deviceId = data.get('deviceId')
    eventId = data.get('eventId')

    mobile_bot = MobileBot(eventId,otpId,sessionId,refreshtoken,deviceId)
    mobile_bot.halfLogin()
    response = mobile_bot.kategorileriGetir()

    # Örnek bir yanıt gönderin
    return {'status': 'success', 'message': response}

@app.route('/start_try', methods=['POST'])
def start_try():
    data = request.get_json()  # Gelen veriyi alın

    
    guid = str(uuid.uuid4())

    is_active[guid] = True
    # Her bir GUID için ayrı bir thread oluştur
    t = threading.Thread(target=ticket_try, args=(guid, data))
    t.start()

    # Örnek bir yanıt gönderin
    return jsonify({'status': 'success', 'message': f'try_ticket başlatıldı (GUID: {guid})'})

@app.route('/stop_try', methods=['POST'])
def stop_try():
    data = request.get_json()
    guid = data.get('guid')  # Hangi işlemi durduracağını belirten GUID
    print(guid)
    if is_active.get(guid):
        is_active[guid] = False  # İşlemi durdur
        return jsonify({'status': 'success', 'message': f'try_ticket durduruldu (GUID: {guid})'})
    else:
        return jsonify({'status': 'error', 'message': 'try_ticket bulunamadı'})

@app.route('/status', methods=['GET'])
def status():
    global total_started_accounts

    return jsonify({
        'total_started_accounts': total_started_accounts
    })





@app.route('/')
def index():
   return "Merhaba Dünya!"
if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))



