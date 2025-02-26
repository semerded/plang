import os
import platform
from ...messenger import Messenger

class Font:
    def __init__(self, path: str, size: int):
        self.path: str = path
        if size < 0:
            Messenger.criticalError(ValueError("a font size must be a positive number"))
        self.size: int = size

    @staticmethod
    def cache_os_fonts():
        # Determine the module directory
        module_dir = os.path.dirname(os.path.abspath(__file__))
        cache_dir = os.path.join(module_dir, 'cache')
        cache_file = os.path.join(cache_dir, 'font_cache.py')

        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Check if cache file exists and is not empty
        if not os.path.isfile(cache_file) or os.path.getsize(cache_file) == 0:
            fonts = Font._fetch_os_fonts()
            Font._write_cache_file(cache_file, fonts)
            Messenger.info(f"OS fonts cached successfully")

    @staticmethod
    def _fetch_os_fonts():
        system = platform.system()
        font_paths = {}
        if system == "Windows":
            font_dirs = [os.path.join(os.environ['WINDIR'], 'Fonts')]
        elif system == "Darwin":  # macOS
            font_dirs = ['/Library/Fonts', '/System/Library/Fonts']
        elif system == "Linux":
            font_dirs = ['/usr/share/fonts', '/usr/local/share/fonts']
        else:
            raise Messenger.fatalError(OSError(f"Unsupported OS: {system}"))

        for font_dir in font_dirs:
            if not os.path.exists(font_dir):
                continue
            for root, _, files in os.walk(font_dir):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf', '.ttc', '.otc')):
                        font_name = os.path.splitext(file)[0]
                        font_path = os.path.join(root, file)
                        font_name = font_name.replace(' ', '_').replace('-', '_')
                        font_name = ''.join(char for char in font_name if char.isalnum() or char == '_')
                        font_name = font_name.upper()
                        font_paths[font_name] = font_path

        return font_paths

    @staticmethod
    def _write_cache_file(cache_file, fonts):
        with open(cache_file, 'w', encoding='utf-8') as cf:
            cf.write("# Auto-generated font cache\n")
            cf.write("from enum import Enum\n")
            cf.write("class fonts(Enum):\n")
            for font_name in sorted(fonts.keys()):
                font_path = fonts[font_name]
                cf.write(f"    {font_name} = r'{font_path}',\n")


    # @staticmethod
    # def get_font(font_name):
    #     return Font._fonts.get(font_name.upper())

    # @staticmethod
    # def available_fonts():
    #     return list(.keys())