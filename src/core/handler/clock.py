from time import perf_counter, sleep
from src import data  # Ensure you have the appropriate debugging flag

class Clock:
    """
    A clock set to a specific FPS with frame delay detection.
    """

    def __init__(self, fps: int = 60, frame_delay_threshold_ms: float = 0.02):
        self.fps: int = fps
        self.frame_length: float = 1 / fps  # Duration of one frame in seconds
        self._start = perf_counter()
        self._last_tick = 0
        self._delay_threshold = frame_delay_threshold_ms  # Delay threshold in seconds
        self._frame_time = self._start  # Keep track of frame time
    
    @property
    def tick(self) -> int:
        """Calculate the current tick based on elapsed time and FPS"""
        return int((perf_counter() - self._start) / self.frame_length)

    def sleep(self, fps=None) -> None:
        """Sleep until the next frame. Optionally, adjust FPS dynamically."""
        if fps and fps != self.fps:
            self.fps = fps
            self.frame_length = 1 / fps

        # Calculate target time for the next frame
        target_time = self._frame_time + self.frame_length
        sleep_time = target_time - perf_counter()

        # Only sleep if we have time before the next frame
        if sleep_time > 0:
            sleep(sleep_time)

        # Measure the actual frame delay
        if self._last_tick != 0 and target_time - self._last_tick > self._delay_threshold and data.debugging:
            self._frame_delay(target_time - self._last_tick)

        # Update the last tick and the frame time
        self._last_tick = self._frame_time
        self._frame_time = perf_counter()  # Reset frame time for next iteration

    def _frame_delay(self, delay_time):
        """Triggered when the frame is delayed beyond the specified threshold"""
        print(f"Frame delayed by {delay_time:.5f} seconds")

