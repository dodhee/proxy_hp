import json
import logging
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
    handlers=[logging.FileHandler(LOG_DIR / 'rotation.log'), logging.StreamHandler()]
)
logger = logging.getLogger('rotation_scheduler')


class RotationScheduler:
    def __init__(self, airplane_manager=None, proxy_system=None, config: Optional[Dict] = None):
        self.config = config or self.load_config()
        self.airplane_manager = airplane_manager
        self.proxy_system = proxy_system
        self.airplane_path = 'src/airplane_manager.py'
        self.tethering_path = 'src/usb_tethering.py'
        self.proxy_path = 'src/proxy_system.py'
        self.rotation_interval = int(self.config.get('rotation_interval', 4))

    def load_config(self) -> Dict:
        if CONFIG_PATH.exists():
            return json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
        return {'rotation_interval': 4}

    def start_airplane_manager(self) -> bool:
        try:
            subprocess.Popen(['python', self.airplane_path], shell=True)
            logger.info('Airplane Manager started')
            return True
        except Exception as exc:
            logger.error('Failed to start Airplane Manager: %s', exc)
            return False

    def start_tethering_manager(self) -> bool:
        try:
            subprocess.Popen(['python', self.tethering_path], shell=True)
            logger.info('USB Tethering Manager started')
            return True
        except Exception as exc:
            logger.error('Failed to start Tethering Manager: %s', exc)
            return False

    def start_proxy_manager(self) -> bool:
        try:
            subprocess.Popen(['python', self.proxy_path], shell=True)
            logger.info('Proxy System Manager started')
            return True
        except Exception as exc:
            logger.error('Failed to start Proxy Manager: %s', exc)
            return False

    def start(self) -> None:
        logger.info('Rotation Scheduler started. Rotating every %s seconds', self.rotation_interval)
        self.start_airplane_manager()
        self.start_tethering_manager()
        self.start_proxy_manager()
        while True:
            try:
                if time.time() % self.rotation_interval < 1:
                    logger.info('Rotating IP (interval: %ss)', self.rotation_interval)
                    subprocess.run(['python', self.airplane_path, 'rotate'], shell=True)
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info('Rotation Scheduler stopped by user')
                break
            except Exception as exc:
                logger.error('Error in scheduler: %s', exc)
                time.sleep(5)


if __name__ == '__main__':
    scheduler = RotationScheduler()
    scheduler.start()
