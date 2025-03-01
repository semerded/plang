import sdl2
import sdl2.ext
import math
import numpy as np
from ctypes import c_int, POINTER, byref

class Draw:
    def __init__(self, window: sdl2.ext.Window, renderer: sdl2.ext.Renderer):
        self._renderer = renderer
        # Initialize caches for rounded rectangles, circles, and polygons
        self.rounded_rect_cache = {}
        self.circle_cache = {}
        self.polygon_cache = {}
        # Initialize angle lookup table
        self.angle_lookup = {}
        self.min_angle_step = 5
        self.max_angle_step = 30
        self.angle_steps = [i for i in range(self.min_angle_step, self.max_angle_step + 1, 5)]
        self._precalculate_angles()
        # Initialize buffers to minimize allocations
        self.vertex_buffer_size = 10000  # Adjust as needed
        self.index_buffer_size = 20000   # Adjust as needed
        self.vertex_buffer = np.zeros((self.vertex_buffer_size, 2), dtype=np.float32)
        self.index_buffer = np.zeros(self.index_buffer_size, dtype=np.int32)
        # Store the viewport dimensions for frustum culling
        self.viewport_w, self.viewport_h = window.size

    def _precalculate_angles(self):
        """Precompute sine and cosine values for angles."""
        for angle_step in self.angle_steps:
            angles = np.arange(0, 360 + angle_step, angle_step, dtype=np.float32)
            cos_vals = np.cos(np.radians(angles))
            sin_vals = np.sin(np.radians(angles))
            self.angle_lookup[angle_step] = dict(zip(angles.astype(int), zip(cos_vals, sin_vals)))

    def rectangle(self, x: float, y: float, w: float, h: float,
                  color=(128, 128, 128, 255), radii=(0, 0, 0, 0)):
        """Draws a rectangle using SDL_RenderGeometry."""
        if not self._is_visible(x, y, w, h):
            return  # Frustum culling: Skip rendering if not visible

        if radii == (0, 0, 0, 0) or radii == 0:
            vertices, indices = self._generate_rectangle_vertices(x, y, w, h)
            # Batch rendering: Collect shapes to render together
            self._render_geometry(vertices, indices, color)
        else:
            # Determine angle_step based on size (LOD)
            angle_step = self._determine_angle_step(w, h)
            radii = self._handle_radius(radii, w, h)

            # Create a cache key based on size, radii, and angle_step
            key = (w, h, radii, angle_step)
            if key in self.rounded_rect_cache:
                # Use cached vertices and indices
                cached_vertices, indices = self.rounded_rect_cache[key]
                # Adjust vertices based on x and y using NumPy
                vertices = cached_vertices + np.array([x, y], dtype=np.float32)
            else:
                vertices, indices = self._generate_rounded_rectangle_vertices(0, 0, w, h, radii, angle_step)
                # Cache the vertices and indices
                self.rounded_rect_cache[key] = (vertices.copy(), indices.copy())
                # Adjust vertices based on x and y using NumPy
                vertices = vertices + np.array([x, y], dtype=np.float32)

            self._render_geometry(vertices, indices, color)

    def circle(self, cx, cy, radius, color, segments=30):
        """Draws a circle using SDL_RenderGeometry."""
        if not self._is_visible(cx - radius, cy - radius, radius * 2, radius * 2):
            return  # Frustum culling: Skip rendering if not visible

        # Determine angle_step based on radius (LOD)
        angle_step = self._determine_angle_step(radius * 2, radius * 2)
        segments = max(int(360 / angle_step), 3)  # At least a triangle

        # Create a cache key based on radius and segments
        key = (radius, segments)
        if key in self.circle_cache:
            cached_vertices, indices = self.circle_cache[key]
            # Adjust vertices based on cx and cy using NumPy
            vertices = cached_vertices + np.array([cx, cy], dtype=np.float32)
        else:
            vertices, indices = self._generate_circle_vertices(0, 0, radius, segments)
            # Cache the vertices and indices
            self.circle_cache[key] = (vertices.copy(), indices.copy())
            # Adjust vertices based on cx and cy using NumPy
            vertices = vertices + np.array([cx, cy], dtype=np.float32)

        self._render_geometry(vertices, indices, color)

    def polygon(self, points, color):
        """Draws a polygon given a list of (x, y) points."""
        # Convert points to NumPy array
        points_array = np.array(points, dtype=np.float32)
        x_min, y_min = points_array.min(axis=0)
        x_max, y_max = points_array.max(axis=0)
        if not self._is_visible(x_min, y_min, x_max - x_min, y_max - y_min):
            return  # Frustum culling: Skip rendering if not visible

        # Create a cache key based on the points
        key = tuple(map(tuple, points_array))
        if key in self.polygon_cache:
            vertices, indices = self.polygon_cache[key]
        else:
            vertices, indices = self._generate_polygon_vertices(points_array)
            self.polygon_cache[key] = (vertices.copy(), indices.copy())

        self._render_geometry(vertices, indices, color)

    def line(self, x1, y1, x2, y2, color):
        """Draws a line using SDL_RenderDrawLineF."""
        if not self._is_line_visible(x1, y1, x2, y2):
            return  # Frustum culling: Skip rendering if not visible

        sdl2.SDL_SetRenderDrawColor(self._renderer.sdlrenderer, *color)
        sdl2.SDL_RenderDrawLineF(self._renderer.sdlrenderer, x1, y1, x2, y2)

    def _render_geometry(self, vertices, indices, color):
        """Helper function to send vertex data to SDL_RenderGeometry."""
        r, g, b, a = color
        num_vertices = len(vertices)

        # Ensure buffers are large enough
        if num_vertices > self.vertex_buffer_size:
            self.vertex_buffer_size = num_vertices * 2
            self.vertex_buffer = np.zeros((self.vertex_buffer_size, 2), dtype=np.float32)
        if len(indices) > self.index_buffer_size:
            self.index_buffer_size = len(indices) * 2
            self.index_buffer = np.zeros(self.index_buffer_size, dtype=np.int32)

        # Copy vertices into the buffer
        self.vertex_buffer[:num_vertices] = vertices[:]
        # Copy indices into the buffer
        self.index_buffer[:len(indices)] = indices[:]

        # Prepare SDL_Vertex array
        vertex_array = (sdl2.SDL_Vertex * num_vertices)()
        for i in range(num_vertices):
            vx, vy = self.vertex_buffer[i]
            vertex_array[i] = sdl2.SDL_Vertex(
                sdl2.SDL_FPoint(vx, vy),
                sdl2.SDL_Color(r, g, b, a),
                sdl2.SDL_FPoint(0, 0)
            )

        # Convert indices to c_int array
        index_array = (c_int * len(indices)).from_buffer_copy(self.index_buffer[:len(indices)].tobytes())

        # Render geometry
        sdl2.SDL_RenderGeometry(
            self._renderer.sdlrenderer, None,
            vertex_array, num_vertices,
            index_array, len(indices)
        )

    def _generate_rectangle_vertices(self, x, y, w, h):
        """Generates vertices and indices for a simple rectangle."""
        vertices = np.array([
            [x, y],               # Top-left
            [x + w, y],           # Top-right
            [x + w, y + h],       # Bottom-right
            [x, y + h]            # Bottom-left
        ], dtype=np.float32)

        indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype=np.int32)

        return vertices, indices

    def _generate_rounded_rectangle_vertices(self, x, y, w, h, radii, angle_step=5):
        """Generates vertices and indices for a rounded rectangle with different radii for each corner."""
        vertices = []
        indices = []

        # Unpack radii
        r_tl, r_tr, r_br, r_bl = radii  # Order: top-left, top-right, bottom-right, bottom-left

        # Use angle lookup table
        angles_dict = self.angle_lookup.get(angle_step)
        if not angles_dict:
            # If angle_step not in lookup, precalculate
            angles = np.arange(0, 360 + angle_step, angle_step, dtype=np.float32)
            cos_vals = np.cos(np.radians(angles))
            sin_vals = np.sin(np.radians(angles))
            angles_dict = dict(zip(angles.astype(int), zip(cos_vals, sin_vals)))
            self.angle_lookup[angle_step] = angles_dict

        # Begin constructing the outline of the rounded rectangle
        full_vertices = []

        # Helper function to generate corner arcs
        def generate_corner_arc(cx, cy, start_angle, end_angle, radius):
            if start_angle > end_angle:
                angles = np.arange(start_angle, end_angle + 360 + angle_step, angle_step, dtype=np.float32) % 360
            else:
                angles = np.arange(start_angle, end_angle + angle_step, angle_step, dtype=np.float32)
            cos_vals = np.cos(np.radians(angles))
            sin_vals = np.sin(np.radians(angles))
            arc_vertices = np.column_stack((cx + radius * cos_vals, cy + radius * sin_vals))
            return arc_vertices

        # Top-left corner
        if r_tl > 0:
            full_vertices.append([x + r_tl, y])
        else:
            full_vertices.append([x, y])

        # Top-right corner
        if r_tr > 0:
            full_vertices.append([x + w - r_tr, y])
            arc = generate_corner_arc(x + w - r_tr, y + r_tr, 270, 360, r_tr)
            full_vertices.extend(arc)
        else:
            full_vertices.append([x + w, y])

        # Bottom-right corner
        if r_br > 0:
            full_vertices.append([x + w, y + h - r_br])
            arc = generate_corner_arc(x + w - r_br, y + h - r_br, 0, 90, r_br)
            full_vertices.extend(arc)
        else:
            full_vertices.append([x + w, y + h])

        # Bottom-left corner
        if r_bl > 0:
            full_vertices.append([x + r_bl, y + h])
            arc = generate_corner_arc(x + r_bl, y + h - r_bl, 90, 180, r_bl)
            full_vertices.extend(arc)
        else:
            full_vertices.append([x, y + h])

        # Left edge and top-left corner
        if r_tl > 0:
            full_vertices.append([x, y + r_tl])
            arc = generate_corner_arc(x + r_tl, y + r_tl, 180, 270, r_tl)
            full_vertices.extend(arc)
        else:
            full_vertices.append([x, y])

        # Remove duplicate point at the end if necessary
        if np.allclose(full_vertices[0], full_vertices[-1]):
            full_vertices.pop()

        # Convert full_vertices to NumPy array
        full_vertices = np.array(full_vertices, dtype=np.float32)

        # Prepare indices for triangle fan
        center_x = x + w / 2
        center_y = y + h / 2
        center_vertex = np.array([[center_x, center_y]], dtype=np.float32)
        vertices = np.vstack((center_vertex, full_vertices))
        num_vertices = len(full_vertices)

        # Generate indices
        indices = np.empty((num_vertices, 3), dtype=np.int32)
        indices[:, 0] = 0  # Center index
        indices[:, 1] = np.arange(1, num_vertices + 1)
        indices[:, 2] = np.arange(2, num_vertices + 2)
        indices[-1, 2] = 1  # Wrap around
        indices = indices.flatten()

        return vertices, indices

    def _generate_circle_vertices(self, cx, cy, radius, segments):
        """Generates vertices and indices for a circle."""
        angle_step = 360 / segments
        angle_step = int(angle_step)
        angles = np.arange(0, 360, angle_step, dtype=np.float32)
        cos_vals = np.cos(np.radians(angles))
        sin_vals = np.sin(np.radians(angles))
        perimeter_vertices = np.column_stack((radius * cos_vals, radius * sin_vals))

        # Center point at (0,0)
        center_vertex = np.array([[0, 0]], dtype=np.float32)
        vertices = np.vstack((center_vertex, perimeter_vertices))

        # Generate indices
        num_vertices = len(vertices)
        indices = np.empty((num_vertices - 2, 3), dtype=np.int32)
        indices[:, 0] = 0  # Center index
        indices[:, 1] = np.arange(1, num_vertices - 1)
        indices[:, 2] = np.arange(2, num_vertices)
        indices = indices.flatten()

        return vertices, indices

    def _generate_polygon_vertices(self, points_array):
        """Generates vertices and indices for a polygon."""
        num_points = len(points_array)
        if num_points < 3:
            return points_array, np.array([], dtype=np.int32)  # Not enough vertices to form a polygon

        # Compute center point
        center = points_array.mean(axis=0, dtype=np.float32)
        vertices = np.vstack((center, points_array))

        # Generate indices using triangle fan
        num_vertices = len(vertices)
        indices = np.empty((num_vertices - 2, 3), dtype=np.int32)
        indices[:, 0] = 0  # Center index
        indices[:, 1] = np.arange(1, num_vertices - 1)
        indices[:, 2] = np.arange(2, num_vertices)
        indices = indices.flatten()

        return vertices, indices

    @staticmethod
    def _handle_radius(radii, w, h):
        """Adjusts radii so they fit within the rectangle dimensions."""
        if isinstance(radii, (int, float)):
            radii = [float(radii)] * 4
        else:
            if len(radii) != 4:
                raise ValueError("Radii must be a number or a tuple/list of four numbers.")
            radii = [float(r) for r in radii]

        radii = [max(0.0, r) for r in radii]

        # Adjust radii for each side
        def adjust_pair(r1, r2, side_length):
            sum_r = r1 + r2
            if sum_r > side_length and sum_r != 0:
                if r1 == 0 or r2 == 0:
                    r1 = min(r1, side_length)
                    r2 = min(r2, side_length)
                else:
                    scale = side_length / sum_r
                    r1 *= scale
                    r2 *= scale
            return r1, r2

        radii[0], radii[1] = adjust_pair(radii[0], radii[1], w)  # Top edge
        radii[3], radii[2] = adjust_pair(radii[3], radii[2], w)  # Bottom edge
        radii[0], radii[3] = adjust_pair(radii[0], radii[3], h)  # Left edge
        radii[1], radii[2] = adjust_pair(radii[1], radii[2], h)  # Right edge

        return tuple(radii)

    def _determine_angle_step(self, w, h):
        """Determines angle_step based on size for LOD."""
        size = max(w, h)
        if size < 100:
            return self.max_angle_step  # Less detail
        elif size < 300:
            return 15  # Medium detail
        else:
            return self.min_angle_step  # High detail

    def _is_visible(self, x, y, w, h):
        """Checks if a rectangle is within the viewport (frustum culling)."""
        return not (x + w < 0 or x > self.viewport_w or y + h < 0 or y > self.viewport_h)

    def _is_line_visible(self, x1, y1, x2, y2):
        """Checks if a line is within the viewport (frustum culling)."""
        x_min = min(x1, x2)
        x_max = max(x1, x2)
        y_min = min(y1, y2)
        y_max = max(y1, y2)
        return not (x_max < 0 or x_min > self.viewport_w or y_max < 0 or y_min > self.viewport_h)
