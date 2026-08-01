# Struktur Folder Proyek (Pure Python - Laptop Only)

```
proxy_hp/
├── laptop/                     # Semua kode utama di laptop (pure Python)
│   ├── main.py                 # Script utama (detect HP, trigger airplane mode, set proxy)
│   ├── usb_tethering.py        # Manage USB tethering ke HP
│   ├── airplane_manager.py     # Trigger airplane mode on/off otomatis
│   ├── proxy_system.py         # Set system proxy ke IP dari HP
│   ├── rotation_scheduler.py   # Scheduler rotate IP setiap 3-5 request
│   ├── requirements.txt        # Dependencies
│   └── config.json             # Konfigurasi provider Telkomsel/Smartfren
│
├── providers/                  # Konfigurasi provider
│   ├── telkomsel.json
│   ├── smartfren.json
│   └── providers.json          # Semua provider support
│
├── docs/                       # Dokumentasi
│   ├── architecture.md
│   ├── developer.md
│   └── api.md
│
├── tests/                      # Test cases
│   ├── laptop/
│   ├── integration/
│   └── usb_tethering/
│
├── README.md
├── LICENSE
└── agent.md
```

## Penjelasan Singkat
- **laptop/**: Semua kode dijalankan dari laptop (pure Python).
- **providers/**: Konfigurasi untuk Telkomsel dan Smartfren.
- **airplane_manager.py**: Trigger airplane mode on/off setiap 3-5 request.
- **usb_tethering.py**: Detect HP connected via USB dan trigger tethering.
- **proxy_system.py**: Set system proxy ke IP dari HP.

Mega prompt akan mencakup konvensi penamaan, folder structure, dan acceptance criteria untuk setiap file.