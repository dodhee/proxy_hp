#!/usr/bin/env python3
"""
Main Script: Proxy HP Bridge - Laptop Controller
Jalankan: python laptop/main.py
"""

import logging
import os
import subprocess
import time
import json
from pathlib import Path

from proxy_system import ProxySystem
from usb_tethering import USBTetheringManager as USBTethering
from airplane_manager import AirplaneManager
from rotation_scheduler import RotationScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("laptop/proxy_hp.log"),
        logging.StreamHandler()
    ]
)

class ProxyHPBridge:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = self.load_config()
        self.proxy_system = ProxySystem()
        self.usb_tethering = USBTethering()
        self.airplane_manager = AirplaneManager()
        self.rotation_scheduler = RotationScheduler(self.airplane_manager, self.proxy_system)

    def load_config(self):
        config_path = Path("laptop/config.json")
        with open(config_path, 'r') as f:
            return json.load(f)

    def start(self):
        """Jalankan aplikasi proxy HP bridge"""
        self.logger.info("=== Starting Proxy HP Bridge ===")
        
        try:
            # 1. Cek HP connected via USB
            if not self.usb_tethering.is_hp_connected():
                self.logger.error("HP tidak connected via USB!")
                return False
            
            # 2. Enable tethering
            if not self.usb_tethering.enable_tethering():
                self.logger.error("Gagal enable tethering!")
                return False
            
            # 3. Set proxy awal
            ip = self.usb_tethering.get_current_ip()
            if ip:
                self.proxy_system.set_proxy(ip)
            
            # 4. Start rotation scheduler
            self.rotation_scheduler.start()
            
            self.logger.info("Proxy HP Bridge berjalan. Press Ctrl+C untuk stop.")
            
            # Keep running
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("Stopping Proxy HP Bridge...")
            self.stop()
        except Exception as e:
            self.logger.error(f"Error: {e}")
            self.stop()

    def stop(self):
        """Stop aplikasi"""
        try:
            self.rotation_scheduler.stop()
            self.usb_tethering.disable_tethering()
            self.proxy_system.disable_proxy()
            self.logger.info("Proxy HP Bridge stopped.")
        except Exception as e:
            self.logger.error(f"Error stop: {e}")

if __name__ == "__main__":
    app = ProxyHPBridge()
    app.start()