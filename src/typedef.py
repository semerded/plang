from typing_extensions import TypeAlias, Literal, Union
from typing import Annotated
from types import FunctionType
from uuid import UUID


# ranged int types are not regulated

uint8: TypeAlias = int  # 0 | 255
int8: TypeAlias = int # - 128 | 127

RGBvalue: TypeAlias = Annotated[tuple[uint8], 3]
RGBAvalue: TypeAlias = Annotated[tuple[uint8], 4]
screen_unit: TypeAlias = float
coordinate: TypeAlias = tuple[screen_unit, screen_unit]
percent: TypeAlias = float
annotated_var: TypeAlias = None


path: TypeAlias = str
# globalFont: TypeAlias = pygame.font.Font
g_id: TypeAlias = UUID