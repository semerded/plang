from enum import Enum
from sdl2 import (
    SDLK_UNKNOWN, SDLK_RETURN, SDLK_ESCAPE, SDLK_BACKSPACE, SDLK_TAB, SDLK_SPACE,
    SDLK_EXCLAIM, SDLK_QUOTEDBL, SDLK_HASH, SDLK_PERCENT, SDLK_DOLLAR, SDLK_AMPERSAND,
    SDLK_QUOTE, SDLK_LEFTPAREN, SDLK_RIGHTPAREN, SDLK_ASTERISK, SDLK_PLUS, SDLK_COMMA,
    SDLK_MINUS, SDLK_PERIOD, SDLK_SLASH, SDLK_0, SDLK_1, SDLK_2, SDLK_3, SDLK_4, SDLK_5,
    SDLK_6, SDLK_7, SDLK_8, SDLK_9, SDLK_COLON, SDLK_SEMICOLON, SDLK_LESS, SDLK_EQUALS,
    SDLK_GREATER, SDLK_QUESTION, SDLK_AT, SDLK_a, SDLK_b, SDLK_c, SDLK_d, SDLK_e, SDLK_f,
    SDLK_g, SDLK_h, SDLK_i, SDLK_j, SDLK_k, SDLK_l, SDLK_m, SDLK_n, SDLK_o, SDLK_p,
    SDLK_q, SDLK_r, SDLK_s, SDLK_t, SDLK_u, SDLK_v, SDLK_w, SDLK_x, SDLK_y, SDLK_z,
    SDLK_LCTRL, SDLK_LSHIFT, SDLK_LALT, SDLK_LGUI, SDLK_RCTRL, SDLK_RSHIFT, SDLK_RALT,
    SDLK_RGUI, SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT, SDLK_INSERT, SDLK_DELETE,
    SDLK_HOME, SDLK_END, SDLK_PAGEUP, SDLK_PAGEDOWN, SDLK_F1, SDLK_F2, SDLK_F3, SDLK_F4,
    SDLK_F5, SDLK_F6, SDLK_F7, SDLK_F8, SDLK_F9, SDLK_F10, SDLK_F11, SDLK_F12
)

class mouse_button(Enum):
    left = 1
    middle = 2
    right = 3
    scroll_up = 4
    scroll_down = 5
    bottom_side = 6
    top_side = 7
    

class key(Enum):
    UNKNOWN = SDLK_UNKNOWN
    RETURN = SDLK_RETURN
    ESCAPE = SDLK_ESCAPE
    BACKSPACE = SDLK_BACKSPACE
    TAB = SDLK_TAB
    SPACE = SDLK_SPACE
    EXCLAIM = SDLK_EXCLAIM
    QUOTEDBL = SDLK_QUOTEDBL
    HASH = SDLK_HASH
    PERCENT = SDLK_PERCENT
    DOLLAR = SDLK_DOLLAR
    AMPERSAND = SDLK_AMPERSAND
    QUOTE = SDLK_QUOTE
    LEFTPAREN = SDLK_LEFTPAREN
    RIGHTPAREN = SDLK_RIGHTPAREN
    ASTERISK = SDLK_ASTERISK
    PLUS = SDLK_PLUS
    COMMA = SDLK_COMMA
    MINUS = SDLK_MINUS
    PERIOD = SDLK_PERIOD
    SLASH = SDLK_SLASH
    
    NUM_0 = SDLK_0
    NUM_1 = SDLK_1
    NUM_2 = SDLK_2
    NUM_3 = SDLK_3
    NUM_4 = SDLK_4
    NUM_5 = SDLK_5
    NUM_6 = SDLK_6
    NUM_7 = SDLK_7
    NUM_8 = SDLK_8
    NUM_9 = SDLK_9
    
    COLON = SDLK_COLON
    SEMICOLON = SDLK_SEMICOLON
    LESS = SDLK_LESS
    EQUALS = SDLK_EQUALS
    GREATER = SDLK_GREATER
    QUESTION = SDLK_QUESTION
    AT = SDLK_AT
    
    A = SDLK_a
    B = SDLK_b
    C = SDLK_c
    D = SDLK_d
    E = SDLK_e
    F = SDLK_f
    G = SDLK_g
    H = SDLK_h
    I = SDLK_i
    J = SDLK_j
    K = SDLK_k
    L = SDLK_l
    M = SDLK_m
    N = SDLK_n
    O = SDLK_o
    P = SDLK_p
    Q = SDLK_q
    R = SDLK_r
    S = SDLK_s
    T = SDLK_t
    U = SDLK_u
    V = SDLK_v
    W = SDLK_w
    X = SDLK_x
    Y = SDLK_y
    Z = SDLK_z
    
    LCTRL = SDLK_LCTRL
    LSHIFT = SDLK_LSHIFT
    LALT = SDLK_LALT
    LGUI = SDLK_LGUI
    RCTRL = SDLK_RCTRL
    RSHIFT = SDLK_RSHIFT
    RALT = SDLK_RALT
    RGUI = SDLK_RGUI
    
    UP = SDLK_UP
    DOWN = SDLK_DOWN
    LEFT = SDLK_LEFT
    RIGHT = SDLK_RIGHT
    
    INSERT = SDLK_INSERT
    DELETE = SDLK_DELETE
    HOME = SDLK_HOME
    END = SDLK_END
    PAGEUP = SDLK_PAGEUP
    PAGEDOWN = SDLK_PAGEDOWN
    
    F1 = SDLK_F1
    F2 = SDLK_F2
    F3 = SDLK_F3
    F4 = SDLK_F4
    F5 = SDLK_F5
    F6 = SDLK_F6
    F7 = SDLK_F7
    F8 = SDLK_F8
    F9 = SDLK_F9
    F10 = SDLK_F10
    F11 = SDLK_F11
    F12 = SDLK_F12

class xPos(Enum):
    left = 0
    center = 50
    right = 100
    
class yPos(Enum):
    top = 0
    center = 50
    bottom = 100
    
class corner(Enum):
    top_left = 0
    top_right = 1
    bottom_left = 2
    bottom_right = 3