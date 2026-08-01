import subprocess
import time
import logging
import json
import os
from typing import Dict, Optional

log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = 'laptop/usb_tethering.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)
logger = logging.getLogger('usb_tethering')

class USBTetheringManager:
    def __init__(self, config: Dict):
        self.config = config
        self.adb_path = self._find_adb()
        self.device_id = self._find_device()

    def _find_adb(self) -> str:
        """Cari adb executable"""
        adb_paths = [
            r"C:\Users\dody\AppData\Local\Android\Sdk\platform-tools\adb.exe",
            r"C:\Program Files\Android\platform-tools\adb.exe",
            "adb"
        ]
        for path in adb_paths:
            try:
                subprocess.run([path, "devices"], capture_output=True, timeout=2)
                return path
            except:
                continue
        raise FileNotFoundError("ADB not found. Install Android SDK platform-tools.")

    def _find_device(self) -> Optional[str]:
        """Cari device ID HP yang connected"""
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:
                if 'device' in line and 'emulator' not in line:
                    return line.split('\t')[0]
            return None
        except Exception as e:
            logger.error(f"Failed to find device: {e}")
            return None

    def enable_tethering(self) -> bool:
        """Enable USB Tethering"""
        if not self.device_id:
            logger.error("No device connected")
            return False

        try:
            command = [self.adb_path, "shell", "svc", "usb", "tether"]
            subprocess.run(command, check=True, timeout=10)
            time.sleep(3)
            logger.info("USB Tethering enabled")
            return True
        except Exception as e:
            logger.error(f"Failed to enable tethering: {e}")
            return False

    def disable_tethering(self) -> bool:
        """Disable USB Tethering"""
        if not self.device_id:
            logger.error("No device connected")
            return False

        try:
            command = [self.adb_path, "shell", "svc", "usb", "tether"]
            subprocess.run(command, check=True, timeout=10)
            logger.info("USB Tethering disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable tethering: {e}")
            return False

    def toggle_tethering(self) -> bool:
        """Toggle USB Tethering"""
        if not self.device_id:
            logger.error("No device connected")
            return False

        try:
            self.disable_tethering()
            time.sleep(1)
            success = self.enable_tethering()
            if success:
                logger.info("USB Tethering toggled")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to toggle tethering: {e}")
            return False

    def run(self):
        """Main tethering management"""
        logger.info(f"USB Tethering Manager started")
        
        while True:
            try:
                if not self.device_id:
                    logger.info("Waiting for HP to connect via USB...")
                    time.sleep(5)
                    self.device_id = self._find_device()
                    continue
                
                if time.time() % 30 < 1:
                    self.toggle_tethering()
                
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("USB Tethering Manager stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in tethering loop: {e}")
                time.sleep(5)
if __name__ == "__main__":
    # Load config
    config_path = os.path.join(log_dir, 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except:
        config = {}
    
    manager = USBTetheringManager(config)
    manager.run()
