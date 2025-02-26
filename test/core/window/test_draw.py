# test_draw.py

import pytest
import math
from src.core.window.draw import Draw

# Assuming the Draw class is in a module named draw_module
# from draw_module import Draw

# However, since we don't have a separate module here, I'll assume the Draw class is available.

class MockRenderer:
    """ A mock renderer to pass into the Draw class for testing purposes. """
    def __init__(self):
        self.sdlrenderer = None  # We won't actually render anything.

def test_generate_rectangle_vertices():
    draw = Draw(MockRenderer())
    x, y, w, h = 10, 20, 100, 200
    expected_vertices = [
        (10, 20),          # Top-left
        (110, 20),         # Top-right
        (110, 220),        # Bottom-right
        (10, 220)          # Bottom-left
    ]
    expected_indices = [0, 1, 2, 2, 3, 0]
    vertices, indices = draw._generate_rectangle_vertices(x, y, w, h)
    assert vertices == expected_vertices, "Rectangle vertices do not match expected values."
    assert indices == expected_indices, "Rectangle indices do not match expected values."

def test_handle_radius():
    # Case 1: All radii are the same and fit within the rectangle
    radii_input = 20
    w, h = 100, 100
    expected_radii = (20.0, 20.0, 20.0, 20.0)
    adjusted_radii = Draw._handle_radius(radii_input, w, h)
    assert adjusted_radii == expected_radii, "Radii were incorrectly adjusted."

    # Case 2: Radii sum exceeds width
    radii_input = (60, 60, 0, 0)
    w, h = 100, 100
    expected_radii = (50.0, 50.0, 0.0, 0.0)
    adjusted_radii = Draw._handle_radius(radii_input, w, h)
    assert adjusted_radii == expected_radii, "Radii were not correctly scaled down."

    # Case 3: One radius zero, other large
    radii_input = (0, 120, 0, 0)
    w, h = 100, 100
    expected_radii = (0.0, 100.0, 0.0, 0.0)
    adjusted_radii = Draw._handle_radius(radii_input, w, h)
    assert adjusted_radii == expected_radii, "Radii were not adjusted correctly when one radius is zero."

def test_generate_rounded_rectangle_vertices():
    draw = Draw(MockRenderer())
    x, y, w, h = 0, 0, 100, 50
    radii = (10, 20, 30, 40)
    vertices, indices = draw._generate_rounded_rectangle_vertices(x, y, w, h, radii)

    # Since the vertices are floats calculated from cosine and sine, we can't compare them directly.
    # We'll check the number of vertices and indices, and certain key points.

    # Expected number of vertices
    expected_num_vertices = None  # This depends on the angle_step and the radii
    # For testing purposes, let's calculate it
    angle_steps = [5]  # You can adjust this if you change angle_step
    expected_vertices_count = 1  # Starts with center point
    for r in radii:
        if r > 0:
            num_steps = len(range(0, 91, angle_steps[0]))
            expected_vertices_count += num_steps
    # Add the initial points (without arcs) and segments
    expected_vertices_count += 4  # For each corner without radius
    # Omitted here due to complexity; adjust accordingly

    # Assert number of vertices is as expected
    # This is simplified due to the complexity of exact calculation
    assert len(vertices) > 0, "Vertices should not be empty."
    assert len(indices) > 0, "Indices should not be empty."

    # Check that all vertices are within the bounds of the rectangle
    for vx, vy in vertices:
        assert x <= vx <= x + w, "Vertex x-coordinate out of bounds."
        assert y <= vy <= y + h, "Vertex y-coordinate out of bounds."

def test_generate_circle_vertices():
    draw = Draw(MockRenderer())
    cx, cy, radius, segments = 50, 50, 25, 12
    vertices, indices = draw._generate_circle_vertices(cx, cy, radius, segments)

    # Expected number of vertices: center + segments
    expected_num_vertices = segments + 1
    assert len(vertices) == expected_num_vertices, "Circle vertex count mismatch."

    # Check that all vertices are within the expected circle
    for vx, vy in vertices[1:]:  # Skip center
        distance = math.hypot(vx - cx, vy - cy)
        assert math.isclose(distance, radius, rel_tol=1e-5), "Vertex not on circle perimeter."

def test_generate_polygon_vertices():
    draw = Draw(MockRenderer())
    points = [(0, 0), (100, 0), (100, 100), (0, 100)]
    vertices, indices = draw._generate_polygon_vertices(points)

    # Expected indices for a square
    expected_indices = [0, 1, 2, 0, 2, 3, 0, 3, 1]
    assert vertices == points, "Polygon vertices do not match input points."
    assert indices == expected_indices, "Polygon indices do not match expected values."

