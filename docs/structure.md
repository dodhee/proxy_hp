# Struktur Folder Proyek (Pure Python)

```
proxy_hp/
├── docs/                  # Dokumentasi
│   ├── structure.md
│   └── mega_prompt.md
├── logs/                   # Log files
├── providers/              # Provider config
│   └── providers.json
├── src/                    # Kode utama
│   ├── __init__.py
│   ├── airplane_manager.py
│   ├── config.json
│   ├── main.py
│   ├── proxy_system.py
│   ├── rotation_scheduler.py
│   ├── requirements.txt
│   └── usb_tethering.py
├── tests/                  # Unit tests
│   └── test_unit.py
├── README.md
├── LICENSE
├── agent.md
└── .gitignore
```

## Penjelasan Singkat
- **src/**: Semua kode dijalankan dari laptop (pure Python).
- **providers/**: Konfigurasi untuk Telkomsel dan Smartfren.
- **airplane_manager.py**: Trigger airplane mode on/off setiap 3-5 request.
- **usb_tethering.py**: Detect HP connected via ADB dan trigger tethering.
- **proxy_system.py**: Set system proxy ke IP dari HP.

Mega prompt akan mencakup konvensi penamaan, folder structure, dan acceptance criteria untuk setiap file.