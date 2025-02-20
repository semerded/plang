import pytest
from time import perf_counter
from src.core.handler.clock import Clock  

def test_clock_tick():
    # working with 60 FPS
    clock = Clock(60)
    start_tick = clock.tick
    sleep_time = 1 / 60

    perf_counter_start = perf_counter()
    while perf_counter() - perf_counter_start < sleep_time:
        pass  # Busy-wait just for test precision

    assert clock.tick > start_tick, "Tick should increment after one frame"

def test_clock_sleep():
    clock = Clock(60)
    start_time = perf_counter()
    clock.sleep()  
    elapsed_time = perf_counter() - start_time

    assert elapsed_time >= (1 / 60), "Sleep should wait at least one frame length"

def test_clock_dynamic_fps():
    clock = Clock(60)
    clock.sleep(30)  

    assert clock.fps == 30, "FPS should update dynamically"
    assert clock.frame_length == 1 / 30, "Frame length should adjust with FPS"
