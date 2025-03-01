import sdl2
import sdl2.sdlttf as sdlttf
from typing import TYPE_CHECKING
from ..core.utils.font import Font
from ..color import Color
from ..typedef import screen_unit
from ..core.window.rect import Rect

if TYPE_CHECKING:
    from ..core.window.window import Window


class Text:
    def __init__(self, window: 'Window', text: str, font: Font, color: Color = Color.BLACK):
        self.window: 'Window' = window
        self.text = str(text)
        self.font_path = font.path
        self.font_size = font.size
        self.color = sdl2.SDL_Color(*color)  # Convert to SDL_Color
        self.font = self._open_font(self.font_path, self.font_size)

        # Internal variables
        self.position = (0, 0)
        self.target_position = (0, 0)
        self.speed = 0

        # Caching mechanisms
        self.texture_cache = {}
        self.size_cache = {}

        # Initialize texture and size
        self.texture, self.width, self.height = self._get_cached_texture(
            self.text)

    def _open_font(self, path, size):
        if not isinstance(path, str):
            path = path.value[0]  # Adjust based on how Font.path is structured
        font = sdlttf.TTF_OpenFont(path.encode('utf-8'), size)
        if not font:
            raise RuntimeError(f"Failed to load font from path: {path}")
        return font

    def _get_cached_texture(self, text):
        """
        Retrieve the texture and size from the cache if available,
        otherwise render and cache them.
        """
        cache_key = (text, self.font_size, self.color.r, self.color.g, self.color.b, self.color.a)
        if cache_key in self.texture_cache:
            return self.texture_cache[cache_key]
        else:
            # Render the text to a surface
            surface = sdlttf.TTF_RenderUTF8_Blended(
                self.font, text.encode('utf-8'), self.color)
            if not surface:
                raise RuntimeError("Failed to render text surface")
            texture = sdl2.SDL_CreateTextureFromSurface(
                self.window._renderer.sdlrenderer, surface)
            if not texture:
                sdl2.SDL_FreeSurface(surface)
                raise RuntimeError("Failed to create texture from surface")
            w, h = surface.contents.w, surface.contents.h
            sdl2.SDL_FreeSurface(surface)

            # Cache the texture and size
            self.texture_cache[cache_key] = (texture, w, h)
            return texture, w, h

    def change_text(self, new_text):
        if new_text != self.text:
            self.text = str(new_text)
            self.texture, self.width, self.height = self._get_cached_texture(
                self.text)

    def get_size(self):
        cache_key = (self.text, self.font_size)
        if cache_key in self.size_cache:
            return self.size_cache[cache_key]
        else:
            w = sdl2.Sint32()
            h = sdl2.Sint32()
            result = sdlttf.TTF_SizeUTF8(
                self.font, self.text.encode('utf-8'), w, h)
            if result != 0:
                raise RuntimeError("Failed to get text size")
            size = (w.value, h.value)
            self.size_cache[cache_key] = size
            return size

    def set_position(self, x: screen_unit, y: screen_unit):
        self.position = (x, y)

    def draw(self):
        # Create a destination rect using your custom Rect class
        dest_rect = Rect(int(self.position[0]), int(
            self.position[1]), self.width, self.height)
        # Create an SDL_Rect from the custom Rect when calling SDL functions
        sdl_dest_rect = sdl2.SDL_Rect(
            dest_rect.x, dest_rect.y, dest_rect.w, dest_rect.h)

        sdl2.SDL_RenderCopy(self.window._renderer.sdlrenderer,
                            self.texture, None, sdl_dest_rect)

    def draw_in_rect(self, rect: Rect, align_percent_x=50, align_percent_y=50):
        """
        Draw the text within a given rectangle, aligning it based on percentage values.

        :param rect: Custom Rect defining the area to draw the text.
        :param align_percent_x: Horizontal alignment percentage (0 to 100).
        :param align_percent_y: Vertical alignment percentage (0 to 100).
        """
        max_width = rect.w
        max_height = rect.h
        text = self.text

        # Create a cache key based on text content, font size, max dimensions, and alignment
        cache_key = (text, self.font_size, max_width, max_height, align_percent_x,
                     align_percent_y, self.color.r, self.color.g, self.color.b, self.color.a)

        if cache_key in self.texture_cache:
            texture, text_width, text_height = self.texture_cache[cache_key]
        else:
            # Measure the text
            w = sdl2.Sint32()
            h = sdl2.Sint32()
            sdlttf.TTF_SizeUTF8(self.font, text.encode('utf-8'), w, h)
            text_width = w.value
            text_height = h.value

            # Handle horizontal overflow
            if text_width > max_width:
                # Truncate text and add ellipsis
                original_text = text
                while text_width > max_width and len(text) > 0:
                    text = text[:-1]
                    sdlttf.TTF_SizeUTF8(
                        self.font, (text + "...").encode('utf-8'), w, h)
                    text_width = w.value
                    text_height = h.value
                text += "..."
                if len(text) <= 3 and text != original_text:
                    text = "..."  # If truncated to nothing, show ellipsis only

            # Optionally handle vertical overflow here if needed

            # Render the text to a surface
            surface = sdlttf.TTF_RenderUTF8_Blended(
                self.font, text.encode('utf-8'), self.color)
            if not surface:
                raise RuntimeError("Failed to render text surface")
            texture = sdl2.SDL_CreateTextureFromSurface(
                self.window._renderer.sdlrenderer, surface)
            if not texture:
                sdl2.SDL_FreeSurface(surface)
                raise RuntimeError("Failed to create texture from surface")
            sdl2.SDL_FreeSurface(surface)

            # Cache the texture and dimensions
            self.texture_cache[cache_key] = (texture, text_width, text_height)

        # Clamp alignment percentages
        align_percent_x = max(0, min(align_percent_x, 100))
        align_percent_y = max(0, min(align_percent_y, 100))

        # Calculate position based on alignment percentages
        pos_x = rect.x + (rect.w - text_width) * (align_percent_x / 100)
        pos_y = rect.y + (rect.h - text_height) * (align_percent_y / 100)

        # Create a destination rect using your custom Rect class
        dest_rect = Rect(int(pos_x), int(pos_y), text_width, text_height)
        # Create an SDL_Rect from the custom Rect when calling SDL functions
        sdl_dest_rect = sdl2.SDL_Rect(
            dest_rect.x, dest_rect.y, dest_rect.w, dest_rect.h)

        # Render the texture
        sdl2.SDL_RenderCopy(self.window._renderer.sdlrenderer,
                            texture, None, sdl_dest_rect)

    def hover(self, target_position, speed):
        self.target_position = target_position
        self.speed = speed

    def update(self, delta_time):
        # Move towards target_position at the given speed
        x, y = self.position
        tx, ty = self.target_position
        dx = tx - x
        dy = ty - y
        distance = (dx**2 + dy**2)**0.5
        if distance != 0:
            nx = dx / distance
            ny = dy / distance
            move_x = nx * self.speed * delta_time
            move_y = ny * self.speed * delta_time

            # Ensure we don't overshoot the target
            if abs(move_x) > abs(dx):
                move_x = dx
            if abs(move_y) > abs(dy):
                move_y = dy

            self.position = (x + move_x, y + move_y)
