import sdl2
import sdl2.ext
import sdl2.sdlttf as sdlttf
from typing import TYPE_CHECKING
from ..core.utils.font import Font
from ..color import Color
from ..typedef import screen_unit

if TYPE_CHECKING:
    from ..core.window.window import Window

class Text:
    def __init__(self, window: 'Window', text: str, font: Font, color: Color = Color.BLACK):
        self.window: 'Window' = window
        self.text = str(text)
        self.font_path = font.path
        self.font_size = font.size
        self.color = sdl2.SDL_Color(*color)  # RGB tuple
        self.font = self._open_font(font.path, font.size)
        
        # Internal variables
        self.texture_cache = {}
        self.position = (0, 0)
        self.target_position = (0, 0)
        self.speed = 0
        self.rect = None

        # Create initial texture
        self._create_texture()
        self.width, self.height = self.get_size()
        
    def _open_font(self, path, size):
        if not isinstance(path, str):
            path = path.value[0]
            
        return sdlttf.TTF_OpenFont(path.encode('utf-8'), size)

    def _create_texture(self):
        if self.text in self.texture_cache:
            self.texture = self.texture_cache[self.text]
        else:
            surface = sdlttf.TTF_RenderUTF8_Blended(self.font, self.text.encode('utf-8'), self.color)
            self.texture = sdl2.SDL_CreateTextureFromSurface(self.window._renderer.sdlrenderer, surface)
            sdl2.SDL_FreeSurface(surface)
            self.texture_cache[self.text] = self.texture

    def change_text(self, new_text):
        if new_text != self.text:
            self.text = str(new_text)
            self._create_texture()
            self.width, self.height = self.get_size()

    def get_size(self):
        w = sdl2.Sint32()
        h = sdl2.Sint32()
        sdlttf.TTF_SizeUTF8(self.font, self.text.encode('utf-8'), w, h)
        return w.value, h.value
    
    def set_position(self, x: screen_unit, y: screen_unit):
        self.position = (x, y)

    def draw(self):
        dest_rect = sdl2.SDL_Rect(int(self.position[0]), int(self.position[1]), self.width, self.height)
        sdl2.SDL_RenderCopy(self.window._renderer.sdlrenderer, self.texture, None, dest_rect)

    def draw_in_rect(self, rect):
        # Check for overflow and add ellipsis if needed
        max_width = rect.w
        text = self.text
        while True:
            w = sdl2.Sint32()
            h = sdl2.Sint32()
            sdlttf.TTF_SizeUTF8(self.font, text.encode('utf-8'), w, h)
            if w.value <= max_width or len(text) == 0:
                break
            text = text[:-1]
        if text != self.text:
            text = text[:-3] + "..."  # Add ellipsis
        surface = sdlttf.TTF_RenderUTF8_Blended(self.font, text.encode('utf-8'), self.color)
        texture = sdl2.SDL_CreateTextureFromSurface(self.window._renderer, surface)
        sdl2.SDL_FreeSurface(surface)
        sdl2.SDL_RenderCopy(self.window._renderer, texture, None, rect)
        sdl2.SDL_DestroyTexture(texture)

    def hover(self, target_position, speed):
        self.target_position = target_position
        self.speed = speed

    def update(self, delta_time):
        # Move towards target_position at speed
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
