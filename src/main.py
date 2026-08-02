#!/usr/bin/env python3
"""Main Script: Proxy HP Bridge - Laptop Controller
Jalankan: python src/main.py
"""

import json
import logging
import time
from pathlib import Path

from airplane_manager import AirplaneManager
from proxy_system import ProxySystem
from rotation_scheduler import RotationScheduler
from usb_tethering import USBTetheringManager

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
CONFIG_PATH = BASE_DIR / "src" / "config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "proxy_hp.log"), logging.StreamHandler()],
)


class ProxyHPBridge:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config()
        self.proxy_system = ProxySystem()
        self.usb_tethering = USBTetheringManager(self.config)
        self.airplane_manager = AirplaneManager(self.config)
        self.rotation_scheduler = RotationScheduler(self.airplane_manager, self.proxy_system, self.config)

    def load_config(self):
        if CONFIG_PATH.exists():
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return {"rotation_interval": 4}

    def start(self):
        self.logger.info("=== Starting Proxy HP Bridge ===")
        try:
            if not self.usb_tethering.is_ready():
                self.logger.error("HP tidak connected via USB!")
                return False

            if not self.usb_tethering.enable_tethering():
                self.logger.error("Gagal enable tethering!")
                return False

            ip = self.usb_tethering.get_current_ip()
            if ip and ip != "unknown":
                self.proxy_system.set_proxy(ip)

            self.rotation_scheduler.start()

            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping Proxy HP Bridge...")
            self.stop()
        except Exception as exc:
            self.logger.error("Error: %s", exc)
            self.stop()

    def stop(self):
        try:
            self.rotation_scheduler.stop() if hasattr(self.rotation_scheduler, "stop") else None
            self.usb_tethering.disable_tethering()
            self.proxy_system.disable_proxy()
            self.logger.info("Proxy HP Bridge stopped.")
        except Exception as exc:
            self.logger.error("Error stop: %s", exc)


if __name__ == "__main__":
    ProxyHPBridge().start()
