# MEGA PROMPT: Aplikasi Proxy Residential HP Bridge (Pure Python)

## Konteks Proyek
Proyek ini adalah aplikasi proxy residential yang aman dan sulit terdeteksi. User menggunakan HP (Telkomsel atau Smartfren) sebagai jembatan IP. Laptop mengatur HP untuk mendapatkan IP residential baru dengan mengubah airplane mode on/off otomatis setiap 3-5 request. HP connect ke laptop via USB tethering, lalu laptop set system proxy ke IP dari HP.

Semua kode dijalankan dari laptop. Tidak ada perubahan di HP kecuali tethering.

## Spesifikasi Teknis
- **Provider**: Telkomsel / Smartfren (residential mobile data pool)
- **Trigger Rotation**: Airplane mode on/off setiap 3-5 request
- **USB Tethering**: Detect HP connected via ADB, enable tethering
- **Proxy Management**: Set system proxy ke IP dari HP (socks5 atau http)
- **Anti-Detection**:
  - TLS fingerprint spoofing (bisa via mitmproxy atau custom)
  - Random User-Agent + Accept-Language per request
  - Session rotation
  - No static headers
  - IP rotation via HP airplane mode
- **Flow**:
  1. Laptop trigger airplane mode di HP
  2. Connect HP ke laptop via USB tethering
  3. Laptop dapatkan IP baru dari HP
  4. Set system proxy ke IP tersebut
  5. Lanjutkan request dengan proxy aktif

## Konvensi Kode (WAJIB)
- Semua kode di `src/`
- Gunakan Python 3.11+
- Gunakan `adb` untuk komunikasi dengan HP
- Gunakan `mitmproxy` atau `requests` untuk proxy management
- Gunakan `python-adb` atau `adb` CLI untuk trigger airplane mode
- Konfigurasi di `config.json`
- Logging dengan `logging` module
- Error handling dengan try/except dan logging

## Struktur Folder (Sudah ada)
```
proxy_hp/
└── src/
    ├── main.py
    ├── usb_tethering.py
    ├── airplane_manager.py
    ├── proxy_system.py
    ├── rotation_scheduler.py
    ├── requirements.txt
    ├── config.json
    └── structure.md
```

## Acceptance Criteria
- Script bisa detect HP connected via ADB
- Bisa trigger airplane mode on/off otomatis
- Bisa set system proxy ke IP dari HP
- Bisa rotate IP setiap 3-5 request
- Bisa integrasi provider Telkomsel/Smartfren
- Kode bersih, terstruktur, dan mudah dibaca
- Test cases untuk setiap fungsi

## Fase-fase yang Akan Dibuat
Mega prompt ini akan dipecah menjadi beberapa fase kecil yang terukur. Setiap fase harus diverifikasi bebas error sebelum lanjut fase berikutnya.

Fase 4: Pembuatan Mega Prompt & Alur Kerja (ini sudah dibuat)
Fase 5: Setup proyek & folder structure (sudah ada)
Fase 6: Implementasi airplane_manager.py
Fase 7: Implementasi usb_tethering.py
Fase 8: Provider runtime integration
Fase 9: Wiring runtime sync
Fase 10: Test & Verification
Fase 11: Git commit & final review

## Mega Prompt untuk Fase 6-11 (nanti akan dipakai)
"Gunakan mega prompt ini untuk implementasi fase-fase berikutnya. Buat kode sesuai spesifikasi, gunakan konvensi penamaan yang sudah ditentukan, dan verifikasi sebelum lanjut fase berikutnya."