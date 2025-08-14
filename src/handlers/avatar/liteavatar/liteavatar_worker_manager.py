import time
from loguru import logger

from handlers.avatar.liteavatar.liteavatar_worker import LiteAvatarWorker, \
    Tts2FaceConfigModel, Tts2FaceEvent, WorkerStatus


class LiteAvatarWorkerManager:
    
    def __init__(self, cocurrent_limit: int, handler_root: str, config: Tts2FaceConfigModel):
        self.cocurrent_limit = cocurrent_limit
        self.handler_root = handler_root
        self.config = config
        self.lite_avatar_workers = []
        for _ in range(cocurrent_limit):
            self.lite_avatar_workers.append(LiteAvatarWorker(handler_root, config))
            time.sleep(5)
    
    def start_worker(self):
        for worker in self.lite_avatar_workers:
            if worker.get_status() == WorkerStatus.IDLE:
                worker.recruit()
                worker.event_in_queue.put_nowait(Tts2FaceEvent.START)
                return worker
        return None
    
    def destroy(self):
        logger.info("destroy LiteAvatarWorkerManager")
        for worker in self.lite_avatar_workers:
            worker.destroy()
