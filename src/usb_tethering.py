import json
import logging
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
CONFIG_PATH = BASE_DIR / "src" / "config.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_DIR / 'usb_tethering.log'), logging.StreamHandler()]
)
logger = logging.getLogger('usb_tethering')


class USBTetheringManager:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self.load_config()
        self.adb_path = self._find_adb()
        self.device_id = self._find_device()

    def load_config(self) -> Dict:
        if CONFIG_PATH.exists():
            return json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
        return {}

    def _find_adb(self) -> str:
        # Use shutil.which to find adb in PATH, fallback to common locations
        adb_path = shutil.which('adb')
        if adb_path:
            return adb_path
        
        adb_paths = [
            r"C:\Users\dody\AppData\Local\Android\Sdk\platform-tools\adb.exe",
            r"C:\Program Files\Android\platform-tools\adb.exe",
        ]
        for path in adb_paths:
            try:
                subprocess.run([path, 'devices'], capture_output=True, timeout=2)
                return path
            except Exception:
                continue
        raise FileNotFoundError('ADB not found. Install Android SDK platform-tools.')

    def _find_device(self) -> Optional[str]:
        try:
            result = subprocess.run([self.adb_path, 'devices'], capture_output=True, text=True, timeout=5)
            for line in result.stdout.strip().splitlines()[1:]:
                if '\tdevice' in line and 'emulator' not in line:
                    return line.split('\t', 1)[0].strip()
            return None
        except Exception as exc:
            logger.error('Failed to find device: %s', exc)
            return None

    def is_ready(self) -> bool:
        return bool(self.device_id)

    def enable_tethering(self) -> bool:
        if not self.device_id:
            logger.error('No device connected')
            return False
        try:
            subprocess.run([self.adb_path, 'shell', 'svc', 'usb', 'tether'], check=True, timeout=10)
            time.sleep(3)
            logger.info('USB Tethering enabled')
            return True
        except Exception as exc:
            logger.error('Failed to enable tethering: %s', exc)
            return False

    def disable_tethering(self) -> bool:
        if not self.device_id:
            logger.error('No device connected')
            return False
        try:
            subprocess.run([self.adb_path, 'shell', 'svc', 'usb', 'tether'], check=True, timeout=10)
            logger.info('USB Tethering disabled')
            return True
        except Exception as exc:
            logger.error('Failed to disable tethering: %s', exc)
            return False

    def toggle_tethering(self) -> bool:
        if not self.device_id:
            logger.error('No device connected')
            return False
        try:
            self.disable_tethering()
            time.sleep(1)
            return self.enable_tethering()
        except Exception as exc:
            logger.error('Failed to toggle tethering: %s', exc)
            return False

    def get_current_ip(self) -> str:
        try:
            result = subprocess.run(["ipconfig"], capture_output=True, text=True, timeout=5)
            for line in result.stdout.splitlines():
                line = line.strip()
                if "IPv4 Address" in line or "IPv4" in line:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        ip = parts[-1].strip()
                        if ip and not ip.startswith("169.254") and not ip.startswith("127."):
                            return ip
            # fallback to netsh
            result = subprocess.run(["netsh", "interface", "ip", "show", "addresses"], capture_output=True, text=True, timeout=5)
            for line in result.stdout.splitlines():
                if "IP Address" in line and "Preferred" in line:
                    ip = line.split()[-1]
                    if ip and not ip.startswith("169.254") and not ip.startswith("127."):
                        return ip
            return "unknown"
        except Exception:
            return "unknown"

    def run(self) -> None:
        logger.info('USB Tethering Manager started')
        while True:
            try:
                if not self.device_id:
                    logger.info('Waiting for HP to connect via USB...')
                    time.sleep(5)
                    self.device_id = self._find_device()
                    continue
                if time.time() % 30 < 1:
                    self.toggle_tethering()
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info('USB Tethering Manager stopped by user')
                break
            except Exception as exc:
                logger.error('Error in tethering loop: %s', exc)
                time.sleep(5)


if __name__ == '__main__':
    manager = USBTetheringManager()
    manager.run()
