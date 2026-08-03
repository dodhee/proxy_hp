# Proxy HP Bridge

Aplikasi proxy residential pure Python yang menggunakan HP (Telkomsel/Smartfren) sebagai bridge IP. Laptop mengatur HP via ADB untuk rotate airplane mode dan USB tethering, lalu set system proxy ke IP dari HP.

---

## 📋 Persyaratan Sebelum Mulai

### 1. Hardware
- **Laptop/PC** dengan Windows 10/11
- **Smartphone Android** (Telkomsel atau Smartfren) dengan kartu SIM aktif dan paket data
- **Kabel USB** untuk menghubungkan HP ke laptop

### 2. Software yang Harus Diinstall
- **Python 3.11+** — [Download di python.org](https://www.python.org/downloads/) ✅ *Pilih "Add Python to PATH" saat install*
- **ADB (Android Debug Bridge)** — [Download platform-tools](https://developer.android.com/tools/releases/platform-tools) ✅ *Extract ke folder, misal `C:\adb`, lalu tambahkan ke PATH Windows*
- **Git** (opsional) — [Download di git-scm.com](https://git-scm.com/)

### 3. Pengaturan di HP Android
1. **Aktifkan Developer Options:**
   - Buka **Pengaturan** → **Tentang Ponsel** → **Informasi Perangkat Lunak**
   - Ketuk **Nomor Build** 7 kali sampai muncul "Mode pengembang已启用"
2. **Aktifkan USB Debugging:**
   - Buka **Pengaturan** → **Sistem** → **Opsi Pengembang**
   - Aktifkan **Debug USB**
3. **Izin USB Tethering:**
   - Buka **Pengaturan** → **Jaringan & Internet** → **Hotspot & Tethering**
   - Aktifkan **Tethering USB** (akan aktif otomatis nanti via aplikasi)

---

## 🚀 Langkah-Langkah Instalasi

### Langkah 1: Buka Terminal (Command Prompt / PowerShell)
- Tekan tombol `Windows + R`, ketik `cmd`, tekan Enter
- Atau klik kanan Start → **Terminal (Admin)** / **PowerShell (Admin)**

### Langkah 2: Clone / Download Proyek
**Opsi A: Pakai Git (disarankan)**
```cmd
cd D:\
git clone https://github.com/username/proxy_hp.git
cd proxy_hp
```

**Opsi B: Download Manual**
1. Download ZIP dari GitHub → Extract ke `D:\proxy_hp`
2. Buka terminal → `cd D:\proxy_hp`

### Langkah 3: Install Dependencies Python
```cmd
pip install -r src/requirements.txt
```
*Tunggu sampai selesai. Jika error "pip not found", restart terminal atau reinstall Python dengan centang "Add to PATH".*

### Langkah 4: Verifikasi ADB Terinstall
```cmd
adb version
```
Harus keluar versi ADB (contoh: `Android Debug Bridge version 1.0.41`).
Jika error `'adb' is not recognized`, tambahkan folder `platform-tools` ke **Environment Variables → Path**.

### Langkah 5: Hubungkan HP ke Laptop
1. Sambungkan HP via kabel USB
2. Di HP akan muncul popup **"Izinkan debug USB?"** → Centang **"Selalu izinkan dari komputer ini"** → **Izinkan**
3. Di terminal, cek koneksi:
```cmd
adb devices
```
Harus muncul serial number HP Anda (contoh: `R58R12345678    device`).
Jika `unauthorized` → ulangi langkah 2 di HP.
Jika kosong → coba ganti kabel/port USB, restart ADB: `adb kill-server && adb start-server`.

---

## ▶️ Menjalankan Aplikasi

### Jalankan Program Utama
```cmd
python -m src.main
```

### Yang Akan Terjadi Otomatis:
1. **Deteksi HP** — Aplikasi cari device via ADB
2. **Enable USB Tethering** — HP jadi modem USB, laptop dapat IP baru
3. **Set System Proxy** — Windows proxy diarahkan ke IP HP (default port 8080)
4. **Rotasi IP** — Setiap 3-5 request, airplane mode di-toggle on/off → dapat IP baru

### Hentikan Program
Tekan `Ctrl + C` di terminal.

---

## 🧪 Menjalankan Test (Opsional)
```cmd
python -m unittest discover -s tests -v
```
Harus keluar `OK` dengan 9 test passed.

---

## ⚙️ Konfigurasi (Opsional)

### File: `src/config.json`
```json
{
  "rotation_interval_requests": 4,
  "default_provider": "telkomsel",
  "proxy_port": 8080,
  "adb_path": "adb"
}
```
- `rotation_interval_requests`: Rotasi setiap berapa request (3-5)
- `default_provider`: `telkomsel` atau `smartfren`
- `proxy_port`: Port proxy lokal (default 8080)
- `adb_path`: Path ke binary ADB (kosongkan kalau sudah di PATH)

### File: `providers/providers.json`
Konfigurasi APN dan detail provider. **Jangan diubah** kecuali tau apa yang dilakukan.

---

## 🌐 Verifikasi Proxy Berfungsi

### Cara 1: Cek IP Publik
1. Buka browser → kunjungi [whatismyipaddress.com](https://whatismyipaddress.com) atau [ipinfo.io](https://ipinfo.io)
2. IP yang muncul harus **IP mobile Telkomsel/Smartfren**, bukan IP WiFi/ISP rumah Anda

### Cara 2: Cek via Terminal
```cmd
curl ipinfo.io/ip
```

### Cara 3: Cek Proxy Windows
- Buka **Settings** → **Network & Internet** → **Proxy**
- "Use a proxy server" harus **On**, Address: `127.0.0.1`, Port: `8080`

---

## ❗ Troubleshooting Umum

| Masalah | Solusi |
|---------|--------|
| `adb devices` kosong | Ganti kabel USB, aktifkan USB Debugging, restart ADB |
| `unauthorized` di adb devices | Hapus debug authorization di HP (Opsi Pengembang → Hapus otorisasi debug USB), reconnect |
| Error "Permission denied" proxy | Jalankan terminal sebagai **Administrator** |
| IP tidak berubah setelah rotasi | Tunggu 10-15 detik setelah airplane mode off, cek `adb shell dumpsys connectivity` |
| USB Tethering tidak aktif otomatis | Aktifkan manual sekali di HP, lalu coba lagi |
| `ModuleNotFoundError` | Jalankan `pip install -r src/requirements.txt` ulang |
| Proxy tidak ter-set di Windows | Butuh akses Admin. Jalankan terminal sebagai Administrator |

---

## 📁 Struktur Folder Penting
```
proxy_hp/
├── src/                    # Kode utama
│   ├── main.py             # Entry point
│   ├── airplane_manager.py # Toggle airplane mode
│   ├── usb_tethering.py    # Handle USB tethering & ambil IP
│   ├── proxy_system.py     # Set Windows proxy via Registry
│   ├── rotation_scheduler.py # Jadwal rotasi IP
│   ├── config.json         # Konfigurasi aplikasi
│   └── requirements.txt    # Dependencies Python
├── providers/
│   └── providers.json      # Config provider (Telkomsel/Smartfren)
├── tests/
│   └── test_unit.py        # Unit tests
├── logs/                   # Log otomatis
├── README.md               # File ini
└── agent.md                # Status proyek (internal)
```

---

## ⚠️ Catatan Penting

1. **Provider API masih statis** — Konfigurasi Telkomsel/Smartfren di `providers/providers.json` belum pakai endpoint API nyata. Untuk production, butuh integrasi API provider.
2. **Butuh akses Administrator** — Set system proxy via Windows Registry butuh hak admin.
3. **Field test belum dilakukan** — Belum diuji di mesin nyata dengan HP fisik. Gunakan dengan risiko sendiri.
4. **Hanya Windows** — `proxy_system.py` pakai Windows Registry. Linux/Mac butuh implementasi lain.
5. **Rotasi IP butuh waktu** — Airplane mode on/off butuh ~10-15 detik sebelum IP baru siap.

---

## 📞 Butuh Bantuan?

- Cek log di folder `logs/` (otomatis dibuat saat jalan)
- Jalankan test: `python -m unittest discover -s tests -v`
- Pastikan semua persyaratan di atas terpenuhi

---

**Branch:** `main`  
**Status:** 9/9 unit tests pass, siap field test