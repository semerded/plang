# Typedef
/src/typedef.py

In the typedef files, custom types (for informative reasons) are defined
They use the python TypeAlias class to point to a built-in python type

## types

### ranged int types
<span style="color: red;">not regulated!</span>
unit8: int -> 0 | 255
int8: int -> -128 | 127

### general plang types
RGBvalue: Annotated[tuple[uint8], 3]
screenUnit: int | float
