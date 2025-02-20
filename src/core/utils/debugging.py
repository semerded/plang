from ... import data
import time

def enable_debugging():
    print("Debugging enabled")
    data.debugging = True
    
class DebugTimer:
    def __init__(self) -> None:
        self.time_points: list[float] = []
        
    def set_time_point(self) -> None:
        self.time_points.append(time.perf_counter())
        
    def remove_previous_time_point(self) -> None:
        if len(self.time_points) > 0:
            self.time_points.pop()
            
    def get_last_time_point(self) -> (float | None):
        if len(self.time_points) > 0:
            return self.time_points[-1]
        return None
        
    def result(self, print_results: bool = True) -> list[float]:
        if print_results:
            for index, _time in enumerate(self.time_points):
                print(f"{index}. {_time}")
        _return = self.time_points
        self.time_points = []
        return _return