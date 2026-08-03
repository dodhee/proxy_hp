# Proxy HP Bridge

Aplikasi proxy residential pure Python yang menggunakan HP (Telkomsel/Smartfren) sebagai bridge IP. Laptop mengatur HP via ADB untuk rotate airplane mode dan USB tethering, lalu set system proxy ke IP dari HP.

## Struktur Proyek

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

## Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r src/requirements.txt
```

### 2. Jalankan Aplikasi
```bash
python -m src.main
```

### 3. Jalankan Test
```bash
python -m unittest discover -s tests -v
```

## Modul Utama

| File | Deskripsi |
|------|-----------|
| `src/main.py` | Entry point, mengoordinasikan semua komponen |
| `src/airplane_manager.py` | Toggle airplane mode via ADB, rotate IP |
| `src/usb_tethering.py` | Detect HP via ADB, enable USB tethering, baca IP aktual |
| `src/proxy_system.py` | Set system proxy Windows via Registry, load provider config |
| `src/rotation_scheduler.py` | Scheduler rotate IP pakai injected airplane_manager |

## Konfigurasi

- `src/config.json` - rotation_interval, default_provider, proxy_port
- `providers/providers.json` - konfigurasi provider Telkomsel & Smartfren

## Test Results

- ✅ 9/9 unit tests pass
- Config load, providers load
- ProxySystem.set_proxy(ip:port) format benar
- USBTetheringManager.get_current_ip() parse IP aktual
- AirplaneManager._find_adb() fallback shutil.which
- RotationScheduler pakai injected objects (no subprocess spawn)

## Branch

`main`

## Catatan

- Provider Telkomsel/Smartfren masih statis (perlu endpoint API nyata untuk production)
- Belum ada field test di mesin nyata dengan HP + ADB
- README.md ini baru dibuat untuk dokumentasi awal