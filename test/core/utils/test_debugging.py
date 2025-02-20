import pytest
from src.core.utils.debugging import enable_debugging, DebugTimer
from src import data
import time

def test_enable_debug():
    enable_debugging()
    assert data.debugging == True
    
def test_set_time_point():
    timer = DebugTimer()
    timer.set_time_point()
    assert len(timer.time_points) == 1, "Time point should be added"

def test_remove_previous_time_point():
    timer = DebugTimer()
    timer.set_time_point()
    timer.remove_previous_time_point()
    assert len(timer.time_points) == 0, "Time point should be removed"

def test_get_last_time_point():
    timer = DebugTimer()
    timer.set_time_point()
    last_time = timer.get_last_time_point()
    assert last_time is not None, "Should return a valid time point"
    assert isinstance(last_time, float), "Last time point should be a float"

def test_get_last_time_point_empty():
    timer = DebugTimer()
    assert timer.get_last_time_point() is None, "Should return None if no time points exist"

def test_result():
    timer = DebugTimer()
    timer.set_time_point()
    timer.set_time_point()
    results = timer.result(print_results=False)
    assert len(results) == 2, "Result should return all stored time points"
    assert timer.time_points == [], "Time points list should be cleared after calling result()"

def test_result_printing(capfd):
    timer = DebugTimer()
    timer.set_time_point()
    timer.set_time_point()
    
    timer.result(print_results=True)
    
    captured = capfd.readouterr()
    
    assert "0. " in captured.out, "First time point should be printed"
    assert "1. " in captured.out, "Second time point should be printed"
    assert captured.out.count("\n") == 2, "Should print one line per time point"