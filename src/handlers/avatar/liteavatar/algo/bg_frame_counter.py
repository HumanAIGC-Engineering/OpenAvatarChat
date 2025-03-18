from loguru import logger


class BgFrameCounter:

    def __init__(self, total_bg_count, step=1) -> None:
        logger.info("create bg frame counter with {} frames", total_bg_count)
        self._increase_bg_index = True
        self._step = step
        self._current_bg_index = 0
        self._total_bg_count = total_bg_count

    def get_and_update_bg_index(self):
        """
        get bg index in a front-end-front loop
        """
        if self._total_bg_count <= 1:
            return 0
        bg_index = self._current_bg_index
        for i in range(int(self._step)):
            if self._increase_bg_index:
                if self._current_bg_index == self._total_bg_count - 1:
                    self._increase_bg_index = False
            else:
                if self._current_bg_index == 0:
                    self._increase_bg_index = True
            self._current_bg_index = (1 if self._increase_bg_index else
                                      -1) + self._current_bg_index
        return bg_index
