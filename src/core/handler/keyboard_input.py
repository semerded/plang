from typing import TYPE_CHECKING
from ...enum import key
from ...core.handler.timer import Timer

if TYPE_CHECKING:
    from ...core.window.window import Window


class KeyboardInput:
    def __init__(self, window: 'Window', arrow_control: bool = True) -> None:
        self.window = window
        self._activated = False
        self._input = ""
        self._arrow_control = arrow_control
        if arrow_control:
            self._caret_pointer = 0

        self._caret_timer = Timer(0.5)
        self._caret_status = True
        self._UTF8_INPUT_KEYS = [key.SPACE.value, key.EXCLAIM.value, key.QUOTEDBL.value, key.HASH.value, key.DOLLAR.value, key.AMPERSAND.value, key.QUOTE.value, key.LEFTPAREN.value, key.RIGHTPAREN.value, key.ASTERISK.value, key.PLUS.value, key.COMMA.value, key.MINUS.value, key.PERIOD.value, key.SLASH.value, key.NUM_0.value, key.NUM_1.value, key.NUM_2.value, key.NUM_3.value, key.NUM_4.value, key.NUM_5.value, key.NUM_6.value, key.NUM_7.value, key.NUM_8.value,
                                 key.NUM_9.value, key.COLON.value, key.SEMICOLON.value, key.LESS.value, key.EQUALS.value, key.GREATER.value, key.QUESTION.value, key.A.value, key.B.value, key.C.value, key.D.value, key.E.value, key.F.value, key.G.value, key.H.value, key.I.value, key.J.value, key.K.value, key.L.value, key.M.value, key.N.value, key.O.value, key.P.value, key.Q.value, key.R.value, key.S.value, key.T.value, key.U.value, key.V.value, key.W.value, key.X.value, key.Y.value, key.Z.value]

    def get_current_input(self) -> str:
        return self._get_input()

    def get_input_string(self) -> str:
        self._get_input()
        if self._caret_status:
            return self._input[:self._caret_pointer] + "|" + self._input[self._caret_pointer:]
        return self._input

    def _get_input(self) -> str:
        if self._caret_timer.is_ringing():
            self._caret_status = not self._caret_status
            self._caret_timer.reset()

        curr_input = ""
        for _key in self.window.keyboard.clicked_keys:
            if self._arrow_control:

                if _key == key.DELETE.value and self._caret_pointer < len(self._input):
                    self._input = self._input[:self._caret_pointer] + \
                        self._input[self._caret_pointer+1:]
                    self._show_caret()
                    continue

                elif _key == key.LEFT.value and self._caret_pointer > 0:
                    self._caret_pointer -= 1
                    self._show_caret()
                    continue

                elif _key == key.RIGHT.value and self._caret_pointer < len(self._input):
                    self._caret_pointer += 1
                    self._show_caret()
                    continue

            if _key == key.BACKSPACE.value and len(self._input) > 0:
                self._input = self._input[:-1]
                self._caret_pointer -= 1
                self._show_caret()

            elif _key in self._UTF8_INPUT_KEYS:
                curr_input += chr(_key)
                self._input += chr(_key)
                self._caret_pointer += 1
                self._show_caret()

        return curr_input

    def _show_caret(self) -> None:
        self._caret_timer.reset()
        self._caret_status = True

    def clear_input(self) -> str:
        input = self._input
        self._input = ""
        return input

    def activate(self) -> None:
        self._activated = True

    def deactivate(self) -> None:
        self._activated = False
