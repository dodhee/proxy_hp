import json
import logging
import winreg
from pathlib import Path
from typing import Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
CONFIG_PATH = BASE_DIR / "src" / "config.json"
PROVIDERS_PATH = BASE_DIR / "providers" / "providers.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ProxySystem:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config()
        self.providers = self.load_providers()
        self.default_provider = self.config.get("default_provider", "telkomsel")
        self.proxy_port = int(self.config.get("proxy_port", 8080))

    def load_config(self) -> Dict:
        if CONFIG_PATH.exists():
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return {"default_provider": "telkomsel", "proxy_port": 8080}

    def load_providers(self) -> Dict:
        if PROVIDERS_PATH.exists():
            data = json.loads(PROVIDERS_PATH.read_text(encoding="utf-8"))
            return data.get("providers", {})
        return {}

    def get_provider(self, name: Optional[str] = None) -> Dict:
        provider_name = name or self.default_provider
        provider = self.providers.get(provider_name)
        if not provider:
            raise KeyError(f"provider tidak ditemukan: {provider_name}")
        return provider

    def set_proxy(self, ip: str, port: Optional[int] = None) -> bool:
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            proxy_port = int(port or self.proxy_port)
            with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
                with winreg.OpenKey(hkey, reg_path, 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, f"{ip}:{proxy_port}")
                    winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "*")
            self.logger.info("Proxy di-set ke %s:%s", ip, proxy_port)
            return True
        except Exception as exc:
            self.logger.error("Gagal set proxy: %s", exc)
            return False

    def disable_proxy(self) -> bool:
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
                with winreg.OpenKey(hkey, reg_path, 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            self.logger.info("Proxy dinonaktifkan")
            return True
        except Exception as exc:
            self.logger.error("Gagal nonaktifkan proxy: %s", exc)
            return False
