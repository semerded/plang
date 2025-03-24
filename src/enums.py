from enum import IntEnum, StrEnum

class RenderDriver(IntEnum):
    UNKNOWN = 0
    OPENGL = 1
    VULKAN = 2
    DIRECT3D = 3
    METAL = 4
    SOFTWARE = 5
    DUMMY = 6