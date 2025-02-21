import pytest
from time import perf_counter, sleep
from src.core.handler.clock import Clock  
from src.core.utils.debugging import enable_debugging
from src import data
data.debugging = True

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
    
def test_frame_delay_triggered(capsys):
    clock = Clock(60, frame_delay_threshold_ms=0.02)
    
    # Simulate the first frame and delay it by 30ms
    clock.sleep()  # This will be the first frame
    sleep(0.03)  # Simulate a 30ms delay (which exceeds the threshold)
    clock.sleep()  # This will be the second frame after the delay
    
    # Capture the printed output (frame delay message)
    captured = capsys.readouterr()
    
    # Ensure the frame delay message is printed
    assert "Frame delayed by" in captured.out, "Expected 'Frame delayed by' message"

def test_no_frame_delay_triggered():
    clock = Clock(60, frame_delay_threshold_ms=0.02)
    
    # Simulate two frames with no delay exceeding the threshold
    clock.sleep()  # This will be the first frame
    sleep(0.01)  # Simulate a 10ms sleep (below threshold)
    clock.sleep()  # This will be the second frame after the short delay
    
    # Ensure that the frame delay was not triggered
    assert clock._last_tick - clock._frame_time < 0.02, "Frame should not be delayed beyond the threshold"

def test_delay_threshold_adjustment(capsys):
    clock = Clock(60, frame_delay_threshold_ms=0.01)  # Set a stricter delay threshold
    
    # Simulate a delayed frame (larger than 0.01s)
    start_time = perf_counter()
    clock.sleep()  # Should trigger frame_delay if delay exceeds 0.01s
    sleep(0.02)
    clock.sleep()
    elapsed_time = perf_counter() - start_time
    captured = capsys.readouterr()
    
    
    # Check that the delay trigger message appears
    assert "Frame delayed by" in captured.out, "Expected 'Frame delayed by' message"
    assert elapsed_time > 0.01, "Frame delay should exceed 0.01s threshold"
    
    # Test a larger threshold, which should not trigger the frame delay
    clock = Clock(60, frame_delay_threshold_ms=0.05)  # Set a more lenient delay threshold
    sleep(0.02)
    start_time = perf_counter()
    clock.sleep()  # Should not trigger frame_delay if delay is less than 0.05s
    elapsed_time = perf_counter() - start_time
    captured = capsys.readouterr()
    
    # Ensure no message was printed when the delay is below the threshold
    assert "Frame delayed by" not in captured.out, "Expected no 'Frame delayed by' message"
    assert elapsed_time < 0.05, "Frame delay should be under 0.05s threshold"
