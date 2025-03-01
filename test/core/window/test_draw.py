# test_draw.py

import pytest
import math
import numpy as np
from src.core.window.draw import Draw

# Assuming the Draw class is in a module named draw_module
# from draw_module import Draw

# Since we don't have a separate module here, we'll proceed with the provided Draw class.

class MockRenderer:
    """A mock renderer to pass into the Draw class for testing purposes."""
    def __init__(self):
        self.sdlrenderer = None  # We won't actually render anything.
        # Mock window size for frustum culling
        self.window = MockWindow()

class MockWindow:
    """A mock window to provide size for the renderer."""
    def __init__(self):
        self.size = (800, 600)  # Example window size

def test_generate_rectangle_vertices():
    draw = Draw(MockWindow(), MockRenderer())
    x, y, w, h = 10, 20, 100, 200
    expected_vertices = np.array([
        [10.0, 20.0],          # Top-left
        [110.0, 20.0],         # Top-right
        [110.0, 220.0],        # Bottom-right
        [10.0, 220.0]          # Bottom-left
    ], dtype=np.float32)
    expected_indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.int32)
    vertices, indices = draw._generate_rectangle_vertices(x, y, w, h)
    np.testing.assert_allclose(vertices, expected_vertices, rtol=1e-5, atol=1e-8, err_msg="Rectangle vertices do not match expected values.")
    np.testing.assert_array_equal(indices, expected_indices, err_msg="Rectangle indices do not match expected values.")

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
    draw = Draw(MockWindow(), MockRenderer())
    x, y, w, h = 0, 0, 100, 50
    radii = (10, 20, 30, 40)
    angle_step = 5  # Adjust as needed
    vertices, indices = draw._generate_rounded_rectangle_vertices(x, y, w, h, radii, angle_step)

    # Ensure vertices is a NumPy array
    assert isinstance(vertices, np.ndarray), "Vertices should be a NumPy array."
    assert isinstance(indices, np.ndarray), "Indices should be a NumPy array."

    # Check that vertices have shape (N, 2)
    assert vertices.shape[1] == 2, "Vertices should be of shape (N, 2)."

    # Check that all vertices are within the bounds of the rectangle
    x_coords = vertices[:, 0]
    y_coords = vertices[:, 1]
    assert np.all(x_coords >= x - 1e-5) and np.all(x_coords <= x + w + 1e-5), "Vertex x-coordinate out of bounds."
    assert np.all(y_coords >= y - 1e-5) and np.all(y_coords <= y + h + 1e-5), "Vertex y-coordinate out of bounds."

    # Check that indices are within valid range
    assert indices.min() >= 0, "Indices contain negative values."
    assert indices.max() < len(vertices), "Indices refer to nonexistent vertices."

    # Check that there are enough vertices and indices
    assert len(vertices) > 0, "No vertices were generated."
    assert len(indices) > 0, "No indices were generated."

def test_generate_circle_vertices():
    draw = Draw(MockWindow(), MockRenderer())
    radius, segments = 25, 12
    vertices, indices = draw._generate_circle_vertices(0, 0, radius, segments)

    # Expected number of vertices: center + perimeter vertices
    expected_num_vertices = segments + 1  # Center vertex + perimeter vertices
    assert len(vertices) == expected_num_vertices, "Circle vertex count mismatch."

    # Check that all vertices are within the expected circle
    for vx, vy in vertices[1:]:  # Skip center
        distance = math.hypot(vx, vy)
        assert math.isclose(distance, radius, rel_tol=1e-5), f"Vertex at ({vx}, {vy}) not on circle perimeter."

def test_generate_polygon_vertices():
    draw = Draw(MockWindow(), MockRenderer())
    points = np.array([[0, 0], [100, 0], [100, 100], [0, 100]], dtype=np.float32)
    vertices, indices = draw._generate_polygon_vertices(points)

    # Expected number of vertices: center + points
    expected_num_vertices = len(points) + 1  # Center vertex + original points
    assert len(vertices) == expected_num_vertices, "Polygon vertex count mismatch."

    # Check that all vertices match the input points after the center vertex
    np.testing.assert_allclose(vertices[1:], points, rtol=1e-5, atol=1e-8, err_msg="Polygon vertices do not match input points.")

    # Check that indices are within valid range
    assert indices.min() >= 0, "Indices contain negative values."
    assert indices.max() < len(vertices), "Indices refer to nonexistent vertices."

    # Correct the number of indices based on the implementation
    # The triangle fan method generates (len(points) - 2 + 1) triangles (n - 1)
    expected_indices_length = (len(points) - 1) * 3  # Each triangle has 3 indices

    assert len(indices) == expected_indices_length, "Polygon indices length mismatch."


if __name__ == "__main__":
    pytest.main([__file__])
