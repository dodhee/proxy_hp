# Struktur Folder Proyek (Pure Python)

```
proxy_hp/
├── src/                     # Semua kode utama (pure Python)
│   ├── main.py                 # Script utama (detect HP, trigger airplane mode, set proxy)
│   ├── usb_tethering.py        # Manage USB tethering ke HP
│   ├── airplane_manager.py     # Trigger airplane mode on/off otomatis
│   ├── proxy_system.py         # Set system proxy ke IP dari HP
│   ├── rotation_scheduler.py   # Scheduler rotate IP setiap 3-5 request
│   ├── requirements.txt        # Dependencies
│   ├── config.json             # Konfigurasi provider Telkomsel/Smartfren
│   └── structure.md            # Dokumentasi struktur folder
│
├── providers/                  # Konfigurasi provider
│   └── providers.json          # Semua provider support
│
├── docs/                       # Dokumentasi
│   └── tests/                  # Test dokumentasi
│
├── logs/                       # Log files
│   ├── airplane.log
│   ├── proxy_hp.log
│   ├── rotation.log
│   └── usb_tethering.log
│
├── tests/                      # Test cases
│   ├── integration/
│   └── usb_tethering/
│
├── README
├── LICENSE
└── agent.md
```

## Penjelasan Singkat
- **src/**: Semua kode dijalankan dari laptop (pure Python).
- **providers/**: Konfigurasi untuk Telkomsel dan Smartfren.
- **airplane_manager.py**: Trigger airplane mode on/off setiap 3-5 request.
- **usb_tethering.py**: Detect HP connected via ADB dan trigger tethering.
- **proxy_system.py**: Set system proxy ke IP dari HP.

Mega prompt akan mencakup konvensi penamaan, folder structure, dan acceptance criteria untuk setiap file.