import subprocess
import time
import logging
import json
from typing import Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/rotation.log'), logging.StreamHandler()]
)
logger = logging.getLogger('rotation_scheduler')

class RotationScheduler:
    def __init__(self, config: Dict):
        self.config = config
        self.airplane_path = 'src/airplane_manager.py'
        self.tethering_path = 'src/usb_tethering.py'
        self.proxy_path = 'src/proxy_system.py'
        self.rotation_interval = 4  # seconds - rotate setiap 4 detik (3-5 request)

    def start_airplane_manager(self) -> bool:
        """Start airplane mode manager"""
        try:
            subprocess.Popen(['python', self.airplane_path], shell=True)
            logger.info('Airplane Manager started')
            return True
        except Exception as e:
            logger.error(f'Failed to start Airplane Manager: {e}')
            return False

    def start_tethering_manager(self) -> bool:
        """Start USB tethering manager"""
        try:
            subprocess.Popen(['python', self.tethering_path], shell=True)
            logger.info('USB Tethering Manager started')
            return True
        except Exception as e:
            logger.error(f'Failed to start Tethering Manager: {e}')
            return False

    def start_proxy_manager(self) -> bool:
        """Start proxy system manager"""
        try:
            subprocess.Popen(['python', self.proxy_path], shell=True)
            logger.info('Proxy System Manager started')
            return True
        except Exception as e:
            logger.error(f'Failed to start Proxy Manager: {e}')
            return False

    def start(self):
        """Start all managers"""
        logger.info(f'Rotation Scheduler started. Rotating every {self.rotation_interval} seconds')
        
        # Start all managers
        self.start_airplane_manager()
        self.start_tethering_manager()
        self.start_proxy_manager()
        
        # Main rotation loop
        while True:
            try:
                # Rotate IP setiap rotation_interval detik
                if time.time() % self.rotation_interval < 1:
                    logger.info(f'Rotating IP (interval: {self.rotation_interval}s)')
                    # Trigger airplane mode rotation
                    subprocess.run(['python', self.airplane_path, 'rotate'], shell=True)
                
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info('Rotation Scheduler stopped by user')
                break
            except Exception as e:
                logger.error(f'Error in scheduler: {e}')
                time.sleep(5)

if __name__ == "__main__":
    # Load config
    try:
        with open('src/config.json', 'r') as f:
            config = json.load(f)
    except:
        config = {"rotation_interval": 4}
    
    scheduler = RotationScheduler(config)
    scheduler.start()