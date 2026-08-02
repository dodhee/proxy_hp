import logging
import time
from typing import Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('rotation_scheduler')


class RotationScheduler:
    def __init__(self, airplane_manager=None, proxy_system=None, config: Optional[Dict] = None):
        self.config = config or {'rotation_interval': 4}
        self.airplane_manager = airplane_manager
        self.proxy_system = proxy_system
        self.rotation_interval = int(self.config.get('rotation_interval', 4))

    def start(self) -> None:
        logger.info('Rotation Scheduler started. Rotating every %s seconds', self.rotation_interval)
        while True:
            try:
                if time.time() % self.rotation_interval < 1:
                    logger.info('Rotating IP (interval: %ss)', self.rotation_interval)
                    if self.airplane_manager:
                        self.airplane_manager.rotate_ip()
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
