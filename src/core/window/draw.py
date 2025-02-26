from ...typedef import *
from ...color import Color
import sdl2
import sdl2.ext
import math
from typing import Annotated
from ctypes import c_int as _c_int


class Draw:
    def __init__(self, renderer: sdl2.ext.renderer):
        self._renderer = renderer
    
    def rectangle(self, x: screen_unit, y: screen_unit, w: screen_unit, h: screen_unit, color: Color = Color.GRAY, radii: (Annotated[screen_unit, 4] | screen_unit) = (0, 0, 0, 0)):
        """ Draws a rectangle using SDL_RenderGeometry. """
        # Check if we are drawing a simple rectangle or a rounded rectangle
        if radii == (0, 0, 0, 0) or radii == 0:
            vertices, indices = self._generate_rectangle_vertices(x, y, w, h)
        else:
            vertices, indices = self._generate_rounded_rectangle_vertices(x, y, w, h, Draw._handle_radius(radii, w, h), angle_step=5)

        self._render_geometry(vertices, indices, color)
    
    def circle(self, cx, cy, radius, color, segments=30):
        segments = min(segments, 360)
        """ Draws a circle using SDL_RenderGeometry. """
        vertices, indices = self._generate_circle_vertices(cx, cy, radius, segments)
        self._render_geometry(vertices, indices, color)
    
    def polygon(self, points, color):
        """ Draws a polygon given a list of (x, y) points. """
        vertices, indices = self._generate_polygon_vertices(points)
        self._render_geometry(vertices, indices, color)
    
    def line(self, x1, y1, x2, y2, color):
        """ Draws a line using SDL_RenderDrawLineF. """
        sdl2.SDL_SetRenderDrawColor(self._renderer.sdlrenderer, *color)
        sdl2.SDL_RenderDrawLineF(self._renderer.sdlrenderer, x1, y1, x2, y2)
    
    def _render_geometry(self, vertices, indices, color, line_mode=False):
        """ Helper function to send vertex data to SDL_RenderGeometry. """
        r, g, b, a = color
        num_vertices = len(vertices)

        # Flatten the vertices list: [(x1, y1), (x2, y2), ...] -> [x1, y1, x2, y2, ...]
        flat_vertices = []
        
        for point in vertices:
            if isinstance(point, tuple):  # If the point is a tuple, it's (x, y)
                flat_vertices.extend(point)
            else:
                # Handle case where a point is a float, assuming it's an x-coordinate
                flat_vertices.append(point)  # Add the x value
                flat_vertices.append(0.0)     # Default y value (0) if only x is provided

        # Create SDL_Vertex objects from the flattened vertices list
        vertex_array = (sdl2.SDL_Vertex * (num_vertices))( 
            *[sdl2.SDL_Vertex(
                sdl2.SDL_FPoint(flat_vertices[i * 2], flat_vertices[i * 2 + 1]),  # Unpack x and y
                sdl2.SDL_Color(r, g, b, a),
                sdl2.SDL_FPoint(0, 0)) 
            for i in range(num_vertices)]
        )

        index_array = (_c_int * len(indices))(*indices)  # Convert to correct type

        sdl2.SDL_SetRenderDrawColor(self._renderer.sdlrenderer, r, g, b, a)

        if line_mode:
            for i in range(0, len(flat_vertices) - 2, 2):
                sdl2.SDL_RenderDrawLineF(self._renderer.sdlrenderer, flat_vertices[i], flat_vertices[i + 1], flat_vertices[i + 2], flat_vertices[i + 3])
        else:
            sdl2.SDL_RenderGeometry(self._renderer.sdlrenderer, None, vertex_array, num_vertices, index_array, len(indices))
            

    def _generate_rectangle_vertices(self, x, y, w, h):
        """Generates vertices and indices for a simple rectangle."""
        vertices = [
            (x, y),          # Top-left
            (x + w, y),      # Top-right
            (x + w, y + h),  # Bottom-right
            (x, y + h)       # Bottom-left
        ]

        indices = [
            0, 1, 2,
            2, 3, 0
        ]

        return vertices, indices
    
    def _generate_rounded_rectangle_vertices(self, x, y, w, h, radii, angle_step=5):
        """
        Generates vertices and indices for a rounded rectangle with different radii for each corner.
        
        Parameters:
        - x, y: Top-left coordinates of the rectangle.
        - w, h: Width and height of the rectangle.
        - radii: Tuple of four radii (r_tl, r_tr, r_br, r_bl).
        - angle_step: Angle step in degrees for generating corner arcs.
        """
        vertices = []
        indices = []
        
        # Unpack radii
        r_tl, r_tr, r_br, r_bl = radii  # Order: top-left, top-right, bottom-right, bottom-left
        
        # Remove the individual radius limitation
        # Previously, radii were limited to half of min(w, h), which we now remove

        # Begin constructing the outline of the rounded rectangle
        # Start from the top-left corner and move clockwise
        full_vertices = []

        # Move to the top-left corner
        # First point after the top-left corner arc
        if r_tl > 0:
            full_vertices.append((x + r_tl, y))
        else:
            full_vertices.append((x, y))

        # Top edge and top-right corner
        if r_tr > 0:
            full_vertices.append((x + w - r_tr, y))
            # Generate top-right corner arc
            angles = [angle for angle in range(270, 360 + angle_step, angle_step)]
            if angles[-1] != 360:
                angles.append(360)
            for angle in angles:
                rad = math.radians(angle)
                full_vertices.append((
                    x + w - r_tr + r_tr * math.cos(rad),
                    y + r_tr + r_tr * math.sin(rad)
                ))
        else:
            full_vertices.append((x + w, y))

        # Right edge and bottom-right corner
        if r_br > 0:
            full_vertices.append((x + w, y + h - r_br))
            # Generate bottom-right corner arc
            angles = [angle for angle in range(0, 90 + angle_step, angle_step)]
            if angles[-1] != 90:
                angles.append(90)
            for angle in angles:
                rad = math.radians(angle)
                full_vertices.append((
                    x + w - r_br + r_br * math.cos(rad),
                    y + h - r_br + r_br * math.sin(rad)
                ))
        else:
            full_vertices.append((x + w, y + h))

        # Bottom edge and bottom-left corner
        if r_bl > 0:
            full_vertices.append((x + r_bl, y + h))
            # Generate bottom-left corner arc
            angles = [angle for angle in range(90, 180 + angle_step, angle_step)]
            if angles[-1] != 180:
                angles.append(180)
            for angle in angles:
                rad = math.radians(angle)
                full_vertices.append((
                    x + r_bl + r_bl * math.cos(rad),
                    y + h - r_bl + r_bl * math.sin(rad)
                ))
        else:
            full_vertices.append((x, y + h))

        # Left edge and back to top-left corner
        if r_tl > 0:
            full_vertices.append((x, y + r_tl))
            # Generate top-left corner arc
            angles = [angle for angle in range(180, 270 + angle_step, angle_step)]
            if angles[-1] != 270:
                angles.append(270)
            for angle in angles:
                rad = math.radians(angle)
                full_vertices.append((
                    x + r_tl + r_tl * math.cos(rad),
                    y + r_tl + r_tl * math.sin(rad)
                ))
        else:
            full_vertices.append((x, y))

        # Prepare indices for rendering the filled polygon
        # Since the polygon is convex and vertices are in order, we can use a triangle fan

        # Add the center point of the rectangle
        center_x = x + w / 2
        center_y = y + h / 2
        vertices.append((center_x, center_y))
        center_index = 0  # The center point will be the first vertex

        # Add the full_vertices to the vertices list
        vertices.extend(full_vertices)
        
        # Generate indices
        indices = []
        num_vertices = len(full_vertices)
        for i in range(1, num_vertices + 1):
            indices.extend([
                center_index,
                i,
                i % num_vertices + 1
            ])
        
        return vertices, indices













    
    def _generate_circle_vertices(self, cx, cy, radius, segments):
        """ Generates vertices and indices for a circle. """
        vertices = [(cx, cy)]
        indices = []
        center_index = 0
        
        for i in range(segments):
            angle = math.radians(i * (360 / segments))
            vertices.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
        
        for i in range(1, len(vertices) - 1):
            indices.extend([center_index, i, i + 1])
        indices.extend([center_index, len(vertices) - 1, 1])
        
        return vertices, indices
    
    def _generate_polygon_vertices(self, points):
        """ Generates vertices and indices for a polygon. """
        vertices = points[:]
        indices = []
        
        for i in range(1, len(vertices) - 1):
            indices.extend([0, i, i + 1])
        indices.extend([0, len(vertices) - 1, 1])
        
        return vertices, indices
 

    @staticmethod
    def _handle_radius(radii, w, h):
        """
        Adjusts the radii so that the sum of adjacent radii along each side
        does not exceed the rectangle's width or height. Allows individual radii
        to be larger than half the width or height if the adjacent radius is zero.
        """
        # Convert radii to a list of four floats
        if isinstance(radii, (int, float)):
            # If radii is a single number, create a list with the same radius for all corners
            radii = [float(radii)] * 4
        else:
            # Ensure radii is a tuple or list with four elements
            if len(radii) != 4:
                raise ValueError("Radii must be a singular number (1 value for all sides) or a tuple with a length of 4 (each value for one corner).")
            radii = [float(r) for r in radii]

        # Ensure radii are non-negative
        radii = [max(0.0, r) for r in radii]
            
        sum_top = radii[0] + radii[1]
        if sum_top > w and sum_top != 0:
            if radii[0] == 0 or radii[1] == 0:
                # Allow the non-zero radius to be up to the full width
                radii[0] = min(radii[0], w)
                radii[1] = min(radii[1], w)
            else:
                # Scale both radii proportionally
                scale = w / sum_top
                radii[0] *= scale
                radii[1] *= scale

        # Adjust radii for bottom edge (radii[3], radii[2])
        sum_bottom = radii[3] + radii[2]
        if sum_bottom > w and sum_bottom != 0:
            if radii[3] == 0 or radii[2] == 0:
                radii[3] = min(radii[3], w)
                radii[2] = min(radii[2], w)
            else:
                scale = w / sum_bottom
                radii[3] *= scale
                radii[2] *= scale

        # Adjust radii for left edge (radii[0], radii[3])
        sum_left = radii[0] + radii[3]
        if sum_left > h and sum_left != 0:
            if radii[0] == 0 or radii[3] == 0:
                radii[0] = min(radii[0], h)
                radii[3] = min(radii[3], h)
            else:
                scale = h / sum_left
                radii[0] *= scale
                radii[3] *= scale

        # Adjust radii for right edge (radii[1], radii[2])
        sum_right = radii[1] + radii[2]
        if sum_right > h and sum_right != 0:
            if radii[1] == 0 or radii[2] == 0:
                radii[1] = min(radii[1], h)
                radii[2] = min(radii[2], h)
            else:
                scale = h / sum_right
                radii[1] *= scale
                radii[2] *= scale

        return tuple(radii)
