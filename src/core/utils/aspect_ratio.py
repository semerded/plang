from ...typedef import *
from ... import exceptions

def get_width_from_aspect_ratio(aspect_ratio: str, height: screen_unit) -> screen_unit:
    return height * convert_aspect_ratio(aspect_ratio)

def get_height_from_aspect_ratio(aspect_ratio: str, width: screen_unit) -> screen_unit:
    return width / convert_aspect_ratio(aspect_ratio)
    
def convert_aspect_ratio(aspect_ratio: str) -> float:
    if ":" not in aspect_ratio:
        raise exceptions.InvalidAspectRatioFormat("aspect ratio must contain a column (:) -> width:height")
    aspect_width, aspect_height = aspect_ratio.split(":")
    
    if not aspect_width.isdigit() or int(aspect_width) < 1:
        raise exceptions.Negativescreen_unitError("first value of aspect ratio must be a positive int ( > 0) -> width:height")
    
    if not aspect_height.isdigit() or int(aspect_height) < 1:
        raise exceptions.Negativescreen_unitError("second value of aspect ratio must be a positive int ( > 0) -> width:height")
    
    return int(aspect_width) / int(aspect_height)