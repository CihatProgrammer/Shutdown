import urllib.request
import json
import re
from datetime import datetime, timedelta

def main():
    # 1. Aladhan API'den Yatsı (Isha) vaktini çek (Konya, Turkey, Diyanet Methodu: 13)
    api_url = "https://api.aladhan.com/v1/timingsByCity?city=Konya&country=Turkey&method=13"
    
    try:
        response = urllib.request.urlopen(api_url)
        data = json.loads(response.read().decode('utf-8'))
        yatsi_str = data['data']['timings']['Isha']
        
        # 2. Üzerine 10 Dakika Ekle
        yatsi_time = datetime.strptime(yatsi_str, "%H:%M")
        kapanma_time = yatsi_time + timedelta(minutes=10)
        kapanma_str = kapanma_time.strftime("%H:%M")
        
        # 3. JSON dosyasını oku, saati güncelle ve kaydet
        with open('komuta_merkezi.json', 'r') as f:
            komuta_verisi = json.load(f)
            
        komuta_verisi['kapanma_saatleri'] = [kapanma_str]
        
        with open('komuta_merkezi.json', 'w') as f:
            json.dump(komuta_verisi, f, indent=2)
            
        print(f"Yatsı vaktine göre yeni kapanma saati ayarlandı: {kapanma_str}")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()
