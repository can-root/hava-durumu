import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTabWidget, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer, QTime, Qt

class HavaDurumuUygulaması(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hava Durumu Uygulaması")
        self.setGeometry(100, 100, 400, 400)

        self.sekme = QTabWidget(self)
        self.layout = QVBoxLayout()

        self.mevcut_sekme = QWidget()
        self.arama_sekme = QWidget()

        self.sekme.addTab(self.mevcut_sekme, "Mevcut")
        self.sekme.addTab(self.arama_sekme, "Arama")

        self.layout.addWidget(self.sekme)
        self.setLayout(self.layout)

        self.mevcut_layout = QVBoxLayout()
        self.sonuc_etiket = QLabel("Hava durumu bilgisi alınıyor...", self)
        self.mevcut_layout.addWidget(self.sonuc_etiket)

        self.saat_etiket = QLabel("", self)
        self.saat_etiket.setAlignment(Qt.AlignCenter)
        self.saat_etiket.setStyleSheet("font-size: 45px;")
        self.mevcut_layout.addWidget(self.saat_etiket)

        self.konum_etiket = QLabel("", self)
        self.konum_etiket.setAlignment(Qt.AlignCenter)
        self.mevcut_layout.addWidget(self.konum_etiket)

        self.mevcut_sekme.setLayout(self.mevcut_layout)

        self.arama_layout = QVBoxLayout()
        self.sehir_girdisi = QLineEdit(self)
        self.sehir_girdisi.setPlaceholderText("Şehir adı girin...")
        self.arama_layout.addWidget(self.sehir_girdisi)

        self.arama_butonu = QPushButton("Ara", self)
        self.arama_butonu.clicked.connect(self.hava_durumu_ara)
        self.arama_layout.addWidget(self.arama_butonu)

        self.arama_sonuc_etiket = QLabel("", self)
        self.arama_layout.addWidget(self.arama_sonuc_etiket)

        self.arama_sekme.setLayout(self.arama_layout)

        self.setStyleSheet(open("style.css").read())

        self.konumu_al()

        self.zamanlayici = QTimer(self)
        self.zamanlayici.timeout.connect(self.konumu_al)
        self.zamanlayici.start(10000)

        self.saat_zamanlayici = QTimer(self)
        self.saat_zamanlayici.timeout.connect(self.saat_guncelle)
        self.saat_zamanlayici.start(1000)

    def konumu_al(self):
        ip_bilgisi = requests.get("https://ipinfo.io/json").json()
        self.sehir = ip_bilgisi.get("city", "Bilinmiyor")
        self.ulke = ip_bilgisi.get("country", "Bilinmiyor")
        self.enlem = ip_bilgisi.get("loc", "").split(',')[0]
        self.boylam = ip_bilgisi.get("loc", "").split(',')[1]
        self.hava_durumu_getir()
        self.konum_etiket_guncelle()

    def hava_durumu_getir(self):
        url = f"http://wttr.in/{self.sehir}?format=j1"
        cevap = requests.get(url)

        if cevap.status_code == 200:
            veri = cevap.json()
            mevcut_durum = veri['current_condition'][0]

            sicaklik = mevcut_durum['temp_C']
            nem = mevcut_durum['humidity']
            ruzgar_hizi = mevcut_durum['windspeedKmph']
            basinc = mevcut_durum['pressure']
            bulutluluk = mevcut_durum['cloudcover']
            hissedilen = mevcut_durum['FeelsLikeC']
            yagis_miktari = mevcut_durum['precipMM']
            hava_aciklamasi = mevcut_durum['weatherDesc'][0]['value']

            self.sonuc_etiket.setText(f"{self.sehir} için hava durumu:\n"
                                       f"Sıcaklık: {sicaklik} °C\n"
                                       f"Hissedilen: {hissedilen} °C\n"
                                       f"Nem: {nem}%\n"
                                       f"Rüzgar Hızı: {ruzgar_hizi} km/h\n"
                                       f"Hava Basıncı: {basinc} hPa\n"
                                       f"Bulutluluk: {bulutluluk}%\n"
                                       f"Yağış Miktarı: {yagis_miktari} mm\n"
                                       f"Hava Durumu: {hava_aciklamasi}")

        else:
            self.sonuc_etiket.setText("Hava durumu bilgisi alınamadı.")

    def hava_durumu_ara(self):
        sehir = self.sehir_girdisi.text()
        if sehir:
            url = f"http://wttr.in/{sehir}?format=j1"
            cevap = requests.get(url)

            if cevap.status_code == 200:
                veri = cevap.json()
                mevcut_durum = veri['current_condition'][0]

                sicaklik = mevcut_durum['temp_C']
                nem = mevcut_durum['humidity']
                ruzgar_hizi = mevcut_durum['windspeedKmph']
                basinc = mevcut_durum['pressure']
                bulutluluk = mevcut_durum['cloudcover']
                hissedilen = mevcut_durum['FeelsLikeC']
                yagis_miktari = mevcut_durum['precipMM']
                hava_aciklamasi = mevcut_durum['weatherDesc'][0]['value']

                self.arama_sonuc_etiket.setText(f"{sehir} için hava durumu:\n"
                                                  f"Sıcaklık: {sicaklik} °C\n"
                                                  f"Hissedilen: {hissedilen} °C\n"
                                                  f"Nem: {nem}%\n"
                                                  f"Rüzgar Hızı: {ruzgar_hizi} km/h\n"
                                                  f"Hava Basıncı: {basinc} hPa\n"
                                                  f"Bulutluluk: {bulutluluk}%\n"
                                                  f"Yağış Miktarı: {yagis_miktari} mm\n"
                                                  f"Hava Durumu: {hava_aciklamasi}")

            else:
                self.arama_sonuc_etiket.setText("Hava durumu bilgisi alınamadı.")
        else:
            self.arama_sonuc_etiket.setText("Lütfen bir şehir adı girin.")

    def konum_etiket_guncelle(self):
        self.konum_etiket.setText(f"Konum: {self.sehir}, {self.ulke}\n"
                                   f"Enlem: {self.enlem}, Boylam: {self.boylam}")

    def saat_guncelle(self):
        mevcut_zaman = QTime.currentTime()
        self.saat_etiket.setText(mevcut_zaman.toString("hh:mm:ss"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = HavaDurumuUygulaması()
    pencere.show()
    sys.exit(app.exec_())
