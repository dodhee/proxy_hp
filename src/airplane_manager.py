import json
import logging
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
CONFIG_PATH = BASE_DIR / "src" / "config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "airplane.log"), logging.StreamHandler()],
)
logger = logging.getLogger("airplane_manager")


class AirplaneManager:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self.load_config()
        self.adb_path = self._find_adb()
        self.device_id = self._find_device()
        self.rotation_interval = int(self.config.get("rotation_interval", 4))

    def load_config(self) -> Dict:
        if CONFIG_PATH.exists():
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return {"rotation_interval": 4}

    def _find_adb(self) -> str:
        # Use shutil.which to find adb in PATH, fallback to common locations
        adb_path = shutil.which('adb')
        if adb_path:
            return adb_path
        
        # Common platform-tools locations (cross-platform)
        adb_paths = [
            r"C:\Program Files\Android\platform-tools\adb.exe",
            r"C:\Program Files (x86)\Android\platform-tools\adb.exe",
            "/opt/android-sdk/platform-tools/adb",
            "/usr/local/android-sdk/platform-tools/adb",
            str(Path.home() / "Android" / "Sdk" / "platform-tools" / "adb"),
            str(Path.home() / "Library" / "Android" / "sdk" / "platform-tools" / "adb"),
        ]
        for path in adb_paths:
            try:
                subprocess.run([path, "devices"], capture_output=True, timeout=2)
                return path
            except Exception:
                continue
        raise FileNotFoundError("ADB not found. Install Android SDK platform-tools.")

    def _find_device(self) -> Optional[str]:
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            for line in result.stdout.strip().splitlines()[1:]:
                if "\tdevice" in line and "emulator" not in line:
                    return line.split("\t", 1)[0].strip()
            return None
        except Exception as exc:
            logger.error("Failed to find device: %s", exc)
            return None

    def is_ready(self) -> bool:
        return bool(self.device_id)

    def toggle_airplane_mode(self, enable: bool) -> bool:
        if not self.device_id:
            logger.error("No device connected")
            return False

        try:
            subprocess.run(
                [self.adb_path, "shell", "settings", "put", "global", "airplane_mode_on", str(int(enable))],
                check=True,
                timeout=10,
            )
            time.sleep(2)
            subprocess.run(
                [self.adb_path, "shell", "am", "broadcast", "-a", "android.intent.action.AIRPLANE_MODE"],
                check=True,
                timeout=5,
            )
            logger.info("Airplane mode %s toggled", "ON" if enable else "OFF")
            return True
        except Exception as exc:
            logger.error("Failed to toggle airplane mode: %s", exc)
            return False

    def rotate_ip(self) -> bool:
        logger.info("Rotating IP: airplane mode ON 15s then OFF")
        if not self.toggle_airplane_mode(True):
            return False
        time.sleep(15)
        return self.toggle_airplane_mode(False)

    def run(self, mode: str = "loop") -> None:
        if mode == "rotate":
            self.rotate_ip()
            return

        logger.info("Airplane Manager started. Rotating every %s seconds", self.rotation_interval)
        while True:
            try:
                self.rotate_ip()
                time.sleep(self.rotation_interval)
            except KeyboardInterrupt:
                logger.info("Airplane Manager stopped by user")
                break
            except Exception as exc:
                logger.error("Error in rotation loop: %s", exc)
                time.sleep(5)


if __name__ == "__main__":
    mode = "rotate" if len(sys.argv) > 1 and sys.argv[1] == "rotate" else "loop"
    manager = AirplaneManager()
    manager.run(mode=mode)
