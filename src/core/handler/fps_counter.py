import time

class FPSCounter:
    def __init__(self):
        self.last_time = time.perf_counter()
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = self.last_time
        self.update_interval = 0.5  # Update FPS value every 0.5 seconds

    def tick(self):
        current_time = time.perf_counter()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        self.frame_count += 1

        # Update the FPS value every 'update_interval' seconds
        if current_time - self.last_fps_time >= self.update_interval:
            self.fps = self.frame_count / (current_time - self.last_fps_time)
            self.frame_count = 0
            self.last_fps_time = current_time

        return delta_time

    def get_fps(self):
        return self.fps