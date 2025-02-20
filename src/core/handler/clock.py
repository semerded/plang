from time import perf_counter, sleep

class Clock:
    def __init__(self, fps):
        self.fps = fps
        self.frame_length = 1 / fps
        self._start = perf_counter()
        self._last_tick = 0

    @property
    def tick(self):
        return int((perf_counter() - self._start) / self.frame_length)

    def sleep(self, fps=None):
        if fps and fps != self.fps:
            self.fps = fps
            self.frame_length = 1 / fps

        target_time = self._start + (self.tick + 1) * self.frame_length
        sleep_time = target_time - perf_counter()

        if sleep_time > 0:
            sleep(sleep_time)
