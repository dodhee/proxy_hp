import json
import logging
import os
import subprocess
import winreg
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxySystem:
    def __init__(self):
        self.config = self.load_config()
        self.logger = logging.getLogger(__name__)

    def load_config(self):
        config_path = Path("src/config.json")
        if not config_path.exists():
            self.logger.error("config.json tidak ditemukan!")
            raise FileNotFoundError("config.json tidak ditemukan")
        
        with open(config_path, 'r') as f:
            return json.load(f)

    def set_proxy(self, ip, port=8080):
        """Set system proxy ke IP dari HP"""
        try:
            # Windows Registry: HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            
            with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
                with winreg.OpenKey(hkey, reg_path, 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, f"127.0.0.1:{port}")
                    winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "*")

            self.logger.info(f"Proxy di-set ke {ip}:{port} (socks5)")
            return True
        except Exception as e:
            self.logger.error(f"Gagal set proxy: {e}")
            return False

    def disable_proxy(self):
        """Nonaktifkan proxy system"""
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
            
            with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
                with winreg.OpenKey(hkey, reg_path, 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)

            self.logger.info("Proxy dinonaktifkan")
            return True
        except Exception as e:
            self.logger.error(f"Gagal nonaktifkan proxy: {e}")
            return False

    def get_current_ip(self):
        """Dapatkan IP current (opsional, untuk debug)"""
        try:
            result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True, timeout=5)
            for line in result.stdout.splitlines():
                if "IPv4 Address" in line:
                    return line.split(":")[1].strip()
            return "unknown"
        except:
            return "unknown"