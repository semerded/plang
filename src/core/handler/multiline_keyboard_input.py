from ...core.handler.keyboard_input import KeyboardInput
from ...enum import key


class MultilineKeyboardInput(KeyboardInput):
    def __init__(self, window, arrow_control=True, newline_char: str = '\n'):
        super().__init__(window, arrow_control)
        self.newline_char: str = newline_char
        self._line_pointer = 0
        self._input = [""]

    def get_input_string(self):
        self._get_input()
        if self._caret_status:
            return ''.join(self._input[:self._line_pointer] + [self._input[self._line_pointer][:self._caret_pointer] + '|' + self._input[self._line_pointer][self._caret_pointer:]] + self._input[self._line_pointer+1:])

        return ''.join(self._input)

    def _get_input(self):
        print(self._input)
        if self._caret_timer.is_ringing():
            self._caret_status = not self._caret_status
            self._caret_timer.reset()

        curr_input = ""
        for _key in self.window.keyboard.clicked_keys:
            if self._arrow_control:

                if _key == key.DELETE.value and self._caret_pointer < len(self._input):
                    self._input[self._line_pointer] = self._input[self._line_pointer][:self._caret_pointer] + \
                        self._input[self._line_pointer][self._caret_pointer+1:]
                    self._show_caret()
                    continue

                elif _key == key.LEFT.value:
                    if self._caret_pointer > 0:
                        self._caret_pointer -= 1
                        self._show_caret()
                        continue
                    elif self._caret_pointer == 0 and self._line_pointer > 0:
                        self._line_pointer -= 1
                        self._caret_pointer = len(
                            self._input[self._line_pointer]) - 1

                elif _key == key.RIGHT.value:
                    if self._caret_pointer < len(self._input[self._line_pointer]):
                        self._caret_pointer += 1
                        self._show_caret()
                        continue
                    elif self._caret_pointer == len(self._input[self._line_pointer]) and self._line_pointer < len(self._input) - 1:
                        self._line_pointer += 1
                        self._caret_pointer = 0

            if _key == key.BACKSPACE.value:
                if self._line_pointer > 0 and self._caret_pointer == 0:
                    if self._input[self._line_pointer] == "":
                        self._input.pop(self._line_pointer)
                        self._input[self._line_pointer -
                                    1] = self._input[self._line_pointer-1].rstrip(self.newline_char)
                    self._line_pointer -= 1
                    self._caret_pointer = len(
                        self._input[self._line_pointer]) 

                elif self._caret_pointer > 0:
                    self._input[self._line_pointer] = self._input[self._line_pointer][:self._caret_pointer -
                                                                                      1] + self._input[self._line_pointer][self._caret_pointer:]
                    self._caret_pointer -= 1
                self._show_caret()

            elif _key == key.RETURN.value:
                curr_input += self.newline_char
                self._input[self._line_pointer] = self._input[self._line_pointer][:self._caret_pointer] + \
                    self.newline_char + \
                    self._input[self._line_pointer][self._caret_pointer:]
                self._caret_pointer = 0
                self._line_pointer += 1
                self._input.append("")

            elif _key in self._UTF8_INPUT_KEYS:
                curr_input += chr(_key)
                self._input[self._line_pointer] = self._input[self._line_pointer][:self._caret_pointer] + \
                    chr(_key) + \
                    self._input[self._line_pointer][self._caret_pointer:]
                self._caret_pointer += 1
                self._show_caret()

        return curr_input

    def clear_input(self) -> str:
        self._line_pointer = 0
        return super().clear_input()
