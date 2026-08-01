import subprocess
import time
import logging
import json
from typing import Dict, Optional
from pathlib import Path

LOG_DIR = Path(__file__).parent
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('laptop/airplane.log'), logging.StreamHandler()]
)
logger = logging.getLogger('airplane_manager')

class AirplaneManager:
    def __init__(self, config: Dict):
        self.config = config
        self.adb_path = self._find_adb()
        self.device_id = self._find_device()
        self.rotation_interval = 4  # seconds - rotate setiap 4 detik (3-5 request)

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

    def toggle_airplane_mode(self, enable: bool) -> bool:
        """Toggle airplane mode"""
        if not self.device_id:
            logger.error("No device connected")
            return False

        try:
            command = [self.adb_path, "shell", "settings", "put", "global", "airplane_mode_on", str(int(enable))]
            subprocess.run(command, check=True, timeout=10)
            
            # Wait for airplane mode to apply
            time.sleep(2)
            
            # Send broadcast
            broadcast = [self.adb_path, "shell", "am", "broadcast", "-a", "android.intent.action.AIRPLANE_MODE"]
            subprocess.run(broadcast, check=True, timeout=5)
            
            logger.info(f"Airplane mode {'ON' if enable else 'OFF'} toggled")
            return True
        except Exception as e:
            logger.error(f"Failed to toggle airplane mode: {e}")
            return False

    def rotate_ip(self) -> bool:
        """Rotate IP by toggling airplane mode"""
        logger.info(f"Rotating IP - turning airplane mode ON for 15 seconds...")
        if self.toggle_airplane_mode(True):
            time.sleep(15)  # Wait 15 seconds for new IP
            logger.info(f"Turning airplane mode OFF...")
            return self.toggle_airplane_mode(False)
        return False

    def run(self):
        """Main rotation loop"""
        logger.info(f"Airplane Manager started. Rotating every {self.rotation_interval} seconds")
        
        while True:
            try:
                self.rotate_ip()
                time.sleep(self.rotation_interval)
            except KeyboardInterrupt:
                logger.info("Airplane Manager stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in rotation loop: {e}")
                time.sleep(5)

if __name__ == "__main__":
    # Load config
    try:
        with open(LOG_DIR / 'config.json', 'r') as f:
            config = json.load(f)
    except:
        config = {"rotation_interval": 4}
    
    manager = AirplaneManager(config)
    manager.run()