import pytest
from time import perf_counter, sleep
from src.core.handler.clock import Clock  # Update the import path as needed
from src import data
data.debugging = True

def test_clock_sleep():
    clock = Clock(fps=60)
    start_time = perf_counter()
    clock.sleep()
    elapsed_time = perf_counter() - start_time

    assert elapsed_time >= clock.frame_length, "Sleep should wait at least one frame length"

def test_clock_dynamic_fps():
    clock = Clock(fps=60)
    clock.sleep(fps=30)  # Change FPS to 30

    assert clock.fps == 30, "FPS should update dynamically"
    assert clock.frame_length == 1 / 30, "Frame length should adjust with FPS"
    expected_delay_threshold = clock.frame_length * 0.5  # Assuming default multiplier is 0.5
    assert clock._frame_delay_threshold == expected_delay_threshold, "Frame delay threshold should adjust with FPS"

def test_frame_delay_triggered(capsys):
    clock = Clock(fps=60, frame_delay_threshold_multiplier=0.5)
    clock.sleep()  # First frame

    # Simulate a delay longer than the threshold (e.g., sleep for 110% of frame length)
    sleep(clock.frame_length * 1.1)
    clock.sleep()  # Second frame

    # Capture the printed output
    captured = capsys.readouterr()
    assert "Frame delayed by" in captured.out, "Expected 'Frame delayed by' message"

def test_no_frame_delay_triggered(capsys):
    clock = Clock(fps=60, frame_delay_threshold_multiplier=0.5)
    clock.sleep()  # First frame

    # Simulate a delay shorter than the threshold (e.g., sleep for 40% of frame length)
    # sleep(clock.frame_length * 0.4)
    clock.sleep()  # Second frame

    # Capture the printed output
    captured = capsys.readouterr()
    assert "Frame delayed by" not in captured.out, "Frame delay should not be triggered"

def test_delay_threshold_adjustment(capsys):
    # Test with a stricter threshold (e.g., 10% of frame length)
    strict_clock = Clock(fps=60, frame_delay_threshold_multiplier=0.1)
    strict_clock.sleep()
    sleep(strict_clock.frame_length * 0.2)  # Exceeds 10% threshold
    strict_clock.sleep()
    captured_strict = capsys.readouterr()
    assert "Frame delayed by" in captured_strict.out, "Expected 'Frame delayed by' message with strict threshold"

    # Test with a lenient threshold (e.g., 100% of frame length)
    lenient_clock = Clock(fps=60, frame_delay_threshold_multiplier=1.0)
    lenient_clock.sleep()
    sleep(lenient_clock.frame_length * 0.9)  # Below 100% threshold
    lenient_clock.sleep()
    captured_lenient = capsys.readouterr()
    assert "Frame delayed by" not in captured_lenient.out, "No 'Frame delayed by' message expected with lenient threshold"
