from time import perf_counter, sleep

class Clock:
    """
    An efficient clock to maintain a target FPS with precise frame delay detection.
    """

    def __init__(self, fps: int = 60, frame_delay_threshold_multiplier: float = 1.44):
        self.fps = fps
        self.frame_length = 1.0 / fps  # Duration of one frame in seconds
        self._start_time = perf_counter()
        self._next_frame_time = self._start_time + self.frame_length
        self.frame_delay_threshold_multiplier = frame_delay_threshold_multiplier
        self._frame_delay_threshold = self.frame_length * self.frame_delay_threshold_multiplier

    def sleep(self, fps=None) -> None:
        """Sleep until the next frame. Optionally adjust FPS dynamically."""
        if fps and fps != self.fps:
            # Update FPS and related calculations
            self.fps = fps
            self.frame_length = 1.0 / fps
            self._frame_delay_threshold = self.frame_length * self.frame_delay_threshold_multiplier
            # Reset the frame schedule to prevent drift
            current_time = perf_counter()
            self._next_frame_time = current_time + self.frame_length

        current_time = perf_counter()
        sleep_time = self._next_frame_time - current_time

        if sleep_time > 0:
            sleep(sleep_time)
            current_time = self._next_frame_time
        else:
            # We're behind schedule; adjust the next frame time
            current_time = perf_counter()

        # Check for frame delays
        delay = current_time - self._next_frame_time
        if delay > self._frame_delay_threshold:
            self._frame_delay(delay)

        # Schedule the next frame
        self._next_frame_time = current_time + self.frame_length

    def _frame_delay(self, delay_time):
        """Handle significant frame delays."""
        print(f"Frame delayed by {delay_time:.5f} seconds")

