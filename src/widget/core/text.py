import sdl2
import sdl2.sdlttf as sdlttf
from typing import TYPE_CHECKING, Union
from ...core.utils.font import Font
from ...color import Color
from ...typedef import screen_unit
from ...core.window.rect import Rect

if TYPE_CHECKING:
    from ...core.window.window import Window


class Text:
    def __init__(self, window: 'Window', text: str, font: Font, color: Color = Color.BLACK):
        self.window: 'Window' = window
        self.text = str(text)
        self.font_path = font.path
        self.font_size = font.size
        self.color = sdl2.SDL_Color(*color)  # Convert to SDL_Color
        self.font = self._open_font(self.font_path, self.font_size)

        # Optional variables for extra decorations that you might use
        self.leading = ""
        self.trailing = ""
        
        self._newline_char = '\n'

        # Internal variables
        self.position = (0, 0)
        self.target_position = (0, 0)
        self.speed = 0

        # Caching mechanisms
        self.texture_cache = {}
        self.size_cache = {}

        # Initialize texture and size
        self.texture, self.width, self.height = self._get_cached_texture(self.text)

    def _open_font(self, path, size):
        if not isinstance(path, str):
            path = path.value[0]  # Adjust based on how Font.path is structured
        font = sdlttf.TTF_OpenFont(path.encode('utf-8'), size)
        if not font:
            raise RuntimeError(f"Failed to load font from path: {path}")
        return font

    def _get_cached_texture(self, text: str) -> Union[tuple[sdl2.SDL_Texture, int, int], None]:
        """
        Retrieve the texture and size from the cache if available,
        otherwise render and cache them.
        This method now supports newline (\n) characters.
        """
        # Create a cache key that is unique for the text, font size, and color
        cache_key = (text, self.font_size, self.color.r, self.color.g, self.color.b, self.color.a)
        if cache_key in self.texture_cache:
            return self.texture_cache[cache_key]

        if not text:
            return None, 0, 0

        # Check if the text contains newlines
        if self._newline_char in text:
            texture, total_width, total_height = self._render_multiline_text(text)
        else:
            # Simple single-line render
            surface = sdlttf.TTF_RenderUTF8_Blended(
                self.font, text.encode('utf-8'), self.color)
            if not surface:
                raise RuntimeError("Failed to render text surface")
            texture = sdl2.SDL_CreateTextureFromSurface(
                self.window._renderer.sdlrenderer, surface)
            if not texture:
                sdl2.SDL_FreeSurface(surface)
                raise RuntimeError("Failed to create texture from surface")
            total_width = surface.contents.w
            total_height = surface.contents.h
            sdl2.SDL_FreeSurface(surface)

        # Cache and return the texture along with its dimensions
        self.texture_cache[cache_key] = (texture, total_width, total_height)
        return texture, total_width, total_height

    def _render_multiline_text(self, text: str) -> tuple[sdl2.SDL_Texture, int, int]:
        """
        Render multi-line text (lines separated by "\n") into a single texture.
        """
        # Split the incoming text into lines
        lines = text.split(self._newline_char)
        line_surfaces = []
        total_height = 0
        max_width = 0

        # Render each line
        for line in lines:
            # For empty lines, render a space to preserve vertical spacing
            if line == "":
                line = " "
            line_surface = sdlttf.TTF_RenderUTF8_Blended(
                self.font, line.encode('utf-8'), self.color)
            if not line_surface:
                raise RuntimeError(f"Failed to render text surface for line: '{line}'")
            w, h = line_surface.contents.w, line_surface.contents.h
            max_width = max(max_width, w)
            total_height += h
            line_surfaces.append(line_surface)

        # Create a new surface that will hold all lines
        # The masks below are typical for a 32-bit surface; adjust if needed
        new_surface = sdl2.SDL_CreateRGBSurface(0, max_width, total_height, 32,
                                                0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
        if not new_surface:
            for surf in line_surfaces:
                sdl2.SDL_FreeSurface(surf)
            raise RuntimeError("Failed to create a destination surface for multi-line text")

        # Blit each line onto the new surface
        current_y = 0
        for surf in line_surfaces:
            # Define a destination rectangle for this line
            dst_rect = sdl2.SDL_Rect(0, current_y, surf.contents.w, surf.contents.h)
            sdl2.SDL_BlitSurface(surf, None, new_surface, dst_rect)
            current_y += surf.contents.h
            sdl2.SDL_FreeSurface(surf)  # Free the individual line surface

        # Create a texture from the combined surface
        texture = sdl2.SDL_CreateTextureFromSurface(self.window._renderer.sdlrenderer, new_surface)
        if not texture:
            sdl2.SDL_FreeSurface(new_surface)
            raise RuntimeError("Failed to create texture from multi-line surface")
        width = new_surface.contents.w
        height = new_surface.contents.h
        sdl2.SDL_FreeSurface(new_surface)
        return texture, width, height
    
    def set_newline_char(self, newline_char: str):
        """
        Set the newline character where a line will be broken and a new line will be rendered\n
        Try to use something uncommon to avoid confusion\n
        Default is '\\n'
        """
        self._newline_char = newline_char

    def set_text(self, new_text):
        if new_text != self.text:
            self.text = str(new_text)
            self.texture, self.width, self.height = self._get_cached_texture(self.text)
            
    def set_leading(self, new_leading):
        if new_leading != self.leading:
            self.leading = str(new_leading)
            self.texture, self.width, self.height = self._get_cached_texture(
                self.leading + self.text + self.trailing)
            
    def set_trailing(self, new_trailing):
        if new_trailing != self.trailing:
            self.trailing = str(new_trailing)
            self.texture, self.width, self.height = self._get_cached_texture(
                self.leading + self.text + self.trailing)

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

    def draw(self):  # TODO fix this
        # Create a destination rect using your custom Rect class
        dest_rect = Rect(int(self.position[0]), int(self.position[1]), self.width, self.height)
        # Create an SDL_Rect from the custom Rect when calling SDL functions
        sdl_dest_rect = sdl2.SDL_Rect(dest_rect.x, dest_rect.y, dest_rect.w, dest_rect.h)

        sdl2.SDL_RenderCopy(self.window._renderer.sdlrenderer,
                            self.texture, None, sdl_dest_rect)

    def draw_in_rect(self, rect: Rect, align_percent_x=50, align_percent_y=50):
        """
        Draw the text within a given rectangle, aligning it based on percentage values.
        """
        max_width = rect.w
        max_height = rect.h
        # Concatenate leading and trailing decorations, if any
        text = self.leading + self.text + self.trailing  # TODO: only recalc when changed
        
        if text:
            # Create a cache key based on text content, font size, etc.
            cache_key = (text, self.font_size, max_width, max_height, align_percent_x,
                        align_percent_y, self.color.r, self.color.g, self.color.b, self.color.a)

            if cache_key in self.texture_cache:
                texture, text_width, text_height = self.texture_cache[cache_key]
            else:
                # Render and measure similarly, handling newlines as well
                texture, text_width, text_height = self._get_cached_texture(text)
                self.texture_cache[cache_key] = (texture, text_width, text_height)

            # Clamp alignment percentages
            align_percent_x = max(0, min(align_percent_x, 100))
            align_percent_y = max(0, min(align_percent_y, 100))

            # Calculate position based on alignment percentages
            pos_x = rect.x + (rect.w - text_width) * (align_percent_x / 100)
            pos_y = rect.y + (rect.h - text_height) * (align_percent_y / 100)

            dest_rect = Rect(int(pos_x), int(pos_y), text_width, text_height)
            sdl_dest_rect = sdl2.SDL_Rect(dest_rect.x, dest_rect.y, dest_rect.w, dest_rect.h)

            sdl2.SDL_RenderCopy(self.window._renderer.sdlrenderer,
                                texture, None, sdl_dest_rect)

    def hover(self, target_position, speed):
        self.target_position = target_position
        self.speed = speed

    def update(self, delta_time):
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

            if abs(move_x) > abs(dx):
                move_x = dx
            if abs(move_y) > abs(dy):
                move_y = dy

            self.position = (x + move_x, y + move_y)
