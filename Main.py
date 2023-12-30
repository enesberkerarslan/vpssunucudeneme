import requests
import json
from datetime import datetime, timedelta
import time 

try:
  with open('vpssunucudeneme/proxy.json', 'r') as f:
    data = json.load(f)
    proxy = data['proxies'][0]
    link = data['link']
    proxies={"http": f"http://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}", 
            "https": f"https://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}",}
except FileNotFoundError:
  print("proxyjson yok")





class MobileBot:
    
    def __init__(self,eventId,otpId,sessionId,refreshtoken,deviceId):
      self.eventId = eventId
      self.otpId = otpId
      self.sessionId = sessionId
      self.refreshToken = refreshtoken
      self.deviceId = deviceId

      self.accessToken = None
      self.start_time = time.time() # refreshToken için
      

      self.sicilno = None
      self.kod = None
      self.fenercell = None
      self.categoryId = None
      self.variantId = None
      self.blockId = None
      self.biletLimiti = False
      self.mail = ""

      self.ticketLimit = True
      self.categories = {}
      self.category_variant_mapping = {}
      self.bot_token = "6166443323:AAGvbrCPmFPhhPrYKtoS42vUHU4_IiNEnVU"
      self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
      self.chat_id = 2111168285       
   
    def kategorileriGetir(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/getcategories?eventId="+self.eventId+"&serieId=null&ticketType=100&campaignId=undefined&validationintegrationid=undefined"
      now = datetime.now()
      three_hours_ago = now - timedelta(hours=3)
      rfc_1123_date = three_hours_ago.strftime('%a, %d %b %Y %H:%M:%S GMT')
      headers ={
      "Accept-Encoding": "gzip",
      "Authorization": "Bearer " + self.accessToken,
      "Connection": "Keep-Alive",
      "Content-Type": "application/json",
      "Host": "ticketingmobile.passo.com.tr",
      "If-Modified-Since": rfc_1123_date,
      "User-Agent": "okhttp/3.12.12",
      "x-device-id": self.deviceId,
      "x-mobileversion-id": "Android - 2.6.12",
      "x-otp-id": self.otpId,
      "x-session-id": self.sessionId
      }
      getCategoriesResponse = requests.get(url=url, headers=headers,proxies=proxies,timeout=15)
      getCategoriesResponse = json.loads(getCategoriesResponse.text)
      print(getCategoriesResponse)     
      if(getCategoriesResponse["isError"] == False):
        for item in getCategoriesResponse["valueList"]:
          self.categories[item["id"]] = item["name"]
        return self.categories
      else:
        return "Hata"
   
    def variantGetir(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/getvariants?serieId=null&eventId=" + self.eventId + "&seatcategoryid="+ self.categoryId +"&campaignId=undefined&validationintegrationid=undefined&tickettype=100"
      headers = {
      "Accept-Encoding": "gzip",
      "Authorization": "Bearer " + self.accessToken,
      "Connection": "Keep-Alive",
      "Content-Type": "application/json",
      "Host": "ticketingmobile.passo.com.tr",
      "User-Agent": "okhttp/3.12.12",
      "x-device-id": self.deviceId,
      "x-mobileversion-id": "Android - 2.6.12",
      "x-otp-id": self.otpId,
      "x-session-id": self.sessionId
      }
      getVariantResponse = requests.get(url=url, headers=headers,proxies=proxies)
      getVariantResponse = json.loads(getVariantResponse.text)
      if(getVariantResponse["isError"] == False): 
        self.variantId = getVariantResponse["value"]["variants"][0]["id"]
   
    def sepeteAt(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/addbestseatstobasket"
      if self.categoryId in self.category_variant_mapping:
        variant_id = self.category_variant_mapping[self.categoryId]
      headers = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer " + self.accessToken,
        "Connection": "Keep-Alive",
        "Content-Length": "170",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "ticketingmobile.passo.com.tr",
        "User-Agent": "okhttp/3.12.12",
        "x-device-id": self.deviceId,
        "x-mobileversion-id": "Android - 2.6.12",
        "x-otp-id": self.otpId,
        "x-session-id": self.sessionId
        }
      sepeteAtBody = {
          "BlockId": self.blockId,
          "SeatCategoryId": self.categoryId,
          "SeatCategoryTicketTypeId": 100,
          "SideBySide": True,
          "variantCount": [
            {
              "count": 1,
              "SeatCategoryVariantId": variant_id
            }
          ],
          "EventId": self.eventId
        }
      basketResponse = requests.post(url=url,json=sepeteAtBody, headers=headers,proxies=proxies)
      basketResponse = json.loads(basketResponse.text)
      print(basketResponse)

      if(basketResponse["isError"] == False):
        category_name = self.categories.get(int(self.categoryId))
        message_text = self.mail + " " + str(category_name) +  "  kategorisinden bilet aldı " 
        data = {
            "chat_id": self.chat_id,
            "text": message_text
        }
        requests.post(self.api_url, data=data)  
      elif(basketResponse["message"] == "Bu etkinlik için etkinlik limiti aşılmıştır."):
        self.ticketLimit = False
        
    
    def bloklarıTara(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/getavailableblocklist?seatCategoryId=" + self.categoryId + "&serieId=null&eventId=" + self.eventId
      headers = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer " + self.accessToken,
        "Connection": "Keep-Alive",
        "Content-Type": "application/json",
        "Host": "ticketingmobile.passo.com.tr",
        "User-Agent": "okhttp/3.12.12",
        "x-device-id": self.deviceId,
        "x-mobileversion-id": "Android - 2.6.12",
        "x-otp-id": self.otpId,
        "x-session-id": self.sessionId
      }
      
      try:
        getTicketInfo = requests.get(url=url, headers=headers,timeout=2,proxies=proxies)
        getTicketInfo.raise_for_status()
      except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                print("Status 401")
                return self.halfLogin()
      except Exception as e:
        print(f'Hata oluştu: {e}')
        time.sleep(0.5)
        return self.bloklarıTara()
      try:  
        getTicketInfo = json.loads(getTicketInfo.text)
        print(getTicketInfo)
      except json.JSONDecodeError:
          requests.get(link)
          print(getTicketInfo.text)
          time.sleep(5)
          return self.bloklarıTara()       
      if getTicketInfo.get('isError'):
        if getTicketInfo.get('message') == 'Invalid token !':
          return self.halfLogin()
        elif getTicketInfo.get('message') == 'HalfLoginRequired': 
          return self.halfLogin()
        

      if not getTicketInfo['valueList']: 
        self.blockId = None 
      else :
        sorted_value_list = sorted(getTicketInfo['valueList'], key=lambda x: x['categoriesCount'], reverse=True)
        for item in sorted_value_list:
          self.blockId = item['id'] 
          self.sepeteAt()

    def biletAl(self):
      endtime= time.time()
      start = time.time()
      if(endtime-self.start_time>120):
        self.start_time = time.time()
        self.refreshToken()

      if self.categoryId not in self.category_variant_mapping :
        self.variantGetir()
        if self.variantId is not None :
          self.category_variant_mapping[self.categoryId] = self.variantId
          print(f"Kategori ID {self.categoryId} için Variant ID: {self.variantId}")
        else:
          print(f"Kategori ID {self.categoryId} için Variant ID: {self.variantId}")
          time.sleep(1)
        
      
      if self.variantId is not None :
        self.bloklarıTara()
        end = time.time()
        print(end-start)
      
    def halfLogin(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/faceIDhalflogin"
      body = {
        "RefreshToken": self.refreshToken
      }
      headers = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Length": "55",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "ticketingmobile.passo.com.tr",
        "User-Agent": "okhttp/3.12.12",
        "x-device-id": self.deviceId,
        "x-mobileversion-id": "Android - 2.6.12",
        "x-otp-id": self.otpId,
        "x-session-id": self.sessionId
      }
      try:
        getAvailableCategory = requests.post(url=url,json=body, headers=headers,proxies=proxies,timeout=15)
        getAvailableCategory.raise_for_status()
      except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:               
                return getAvailableCategory.text
      except Exception as e:
        print(f'Hata oluştu in half loginin içi: {e}')
        return self.halfLogin()

      try:
        getAvailableCategory = json.loads(getAvailableCategory.text)
      except json.JSONDecodeError:
        requests.get(link)
        print(getAvailableCategory.text)
        time.sleep(5)
        return self.halfLogin()
      if getAvailableCategory['isError']:
        print("hata")
      else:
        self.accessToken = getAvailableCategory["value"]["access_token"]
        return "Login Succesfully"

    def tokenYenile(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/refreshtoken/" + self.refreshToken
      headers = {
      "Accept-Encoding": "gzip",
      "Connection": "Keep-Alive",
      "Content-Length": "2",
      "Content-Type": "application/json; charset=utf-8",
      "Host": "ticketingmobile.passo.com.tr",
      "User-Agent": "okhttp/3.12.12",
      "x-device-id": self.deviceId,
      "x-mobileversion-id": "Android - 2.6.12",
      "x-otp-id": self.otpId,
      "x-session-id": self.sessionId
      }
      body = {}
      response = requests.post(url=url,json=body, headers=headers,proxies=proxies)
      response = json.loads(response.text)
      print(response)

    def sepetiGetir(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/getuserbasketbooking"
      now = datetime.now()
      three_hours_ago = now - timedelta(hours=3)
      rfc_1123_date = three_hours_ago.strftime('%a, %d %b %Y %H:%M:%S GMT')
      headers = {
        "Accept-Encoding": "gzip",
        "authorization": "Bearer " + self.accessToken,
        "Connection": "Keep-Alive",
        "content-type": "application/json",
        "Host": "ticketingmobile.passo.com.tr",
        "If-Modified-Since": rfc_1123_date,
        "User-Agent": "okhttp/3.12.12",
        "x-device-id": self.deviceId,
        "x-mobileversion-id": "Android - 2.6.12",
        "x-otp-id": self.otpId,
        "x-session-id": self.sessionId
      }
      response = requests.get(url=url, headers=headers)
      response = json.loads(response.text)
      row_id = response['value']['basketBookingProducts'][0]['rowId']
      if 'basketBookingProducts' in response['value']:
        for booking_product in response['value']['basketBookingProducts']:
          kategori_adi = booking_product.get('seatCategory_Name', 'Bilinmiyor')
          tribun_adi =  booking_product.get('tribune_Name', 'Bilinmiyor')
          blok_adi = booking_product.get('block_Name', 'Bilinmiyor')
          basket_remaning_time = response['value']['basketRemaningTime'] 
          message_text = "Sepetinizde "+kategori_adi +"  "+ tribun_adi +"  "+  blok_adi+ " kategorisinden bilet aldı KALAN SÜRE " + str(basket_remaning_time)
      return row_id
    
    def sepetiBosalt(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/removeallseatfrombookingbasket"
      headers = {
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer ' + self.accessToken,
        'Connection': 'Keep-Alive',
        'Content-Length': '2',
        'Content-Type': 'application/json; charset=utf-8',
        'Host': 'ticketingmobile.passo.com.tr',
        'User-Agent': 'okhttp/3.12.12',
        'X-Device-Id': self.deviceId,
        'X-MobileVersion-Id': 'Android - 2.6.12',
        'X-Otp-Id': self.otpId,
        'X-Session-Id': self.sessionId
        }
      body = {}
      response = requests.post(url=url,json=body,headers=headers,proxies=proxies)
      response = json.loads(response.text)


    def galatasarayOncelik(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/PriorityValidationRule"
      body = {
        "ValidationIntegrationID": 1625,
        "param1": "33623236952",
        "param2": "",
        "SerieId": None,
        "EventId": self.eventId
      }
      headers = {
            "Accept-Encoding": "gzip",
            "Authorization": 'Bearer ' + self.accessToken,
            "Connection": "Keep-Alive",
            "Content-Length": "102",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "ticketingmobile.passo.com.tr",
            "User-Agent": "okhttp/3.12.12",
            "x-device-id": self.deviceId,
            "x-mobileversion-id": "Android - 2.6.12",
            "x-otp-id": self.otpId,
            "x-session-id": self.sessionId
          }
      response = requests.post(url=url,json=body,headers=headers,proxies=proxies)
      response = json.loads(response.text)
      print(response)

    def fenerbahceOncelik(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/PriorityValidationRule"
      headers = {
            "Accept-Encoding": "gzip",
            "Authorization": 'Bearer ' + self.accessToken,
            "Connection": "Keep-Alive",
            "Content-Length": "102",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "ticketingmobile.passo.com.tr",
            "User-Agent": "okhttp/3.12.12",
            "x-device-id": self.deviceId,
            "x-mobileversion-id": "Android - 2.6.12",
            "x-otp-id": self.otpId,
            "x-session-id": self.sessionId
          }
      body = {
        "ValidationIntegrationID": 25625,
        "param1": self.fenercell,
        "param2": "",
        "SerieId": None,
        "EventId": self.eventId
      }
      response = requests.post(url=url,json=body,headers=headers,proxies=proxies)
      response = json.loads(response.text)
      print(response)
    
    def fenerKongre(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/PriorityValidationRule"
      headers = {
            "Accept-Encoding": "gzip",
            "Authorization": 'Bearer ' + self.accessToken,
            "Connection": "Keep-Alive",
            "Content-Length": "106",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "ticketingmobile.passo.com.tr",
            "User-Agent": "okhttp/3.12.12",
            "x-device-id": self.deviceId,
            "x-mobileversion-id": "Android - 2.6.12",
            "x-otp-id": self.otpId,
            "x-session-id": self.sessionId
          }
      body = {
        "ValidationIntegrationID": 341645,
        "param1": self.sicilno,
        "param2": self.kod,
        "SerieId": None,
        "EventId": self.eventId
      }
      response = requests.post(url=url,json=body,headers=headers,proxies=proxies)
      response = json.loads(response.text)
      print(response)

                
    def profilBilgisi(self):
      url = "http://ticketingmobile.passo.com.tr/api/passomobile/getcontactForProfile"
      now = datetime.now()
      three_hours_ago = now - timedelta(hours=3)
      rfc_1123_date = three_hours_ago.strftime('%a, %d %b %Y %H:%M:%S GMT')
      headers = {
        "Accept-Encoding": "gzip",
        "Authorization": "Bearer " + self.accessToken,
        "Connection": "Keep-Alive",
        "Content-Type": "application/json",
        "Host": "ticketingmobile.passo.com.tr",
        "If-Modified-Since": rfc_1123_date,
        "User-Agent": "okhttp/3.12.12",
        "x-device-id": self.deviceId,
        "x-mobileversion-id": "Android - 2.6.12",
        "x-otp-id": self.otpId,
        "x-session-id": self.sessionId
      }
      response = requests.get(url=url,headers=headers,proxies=proxies)
      response = json.loads(response.text)
      
      self.mail = response['value']['userName']




