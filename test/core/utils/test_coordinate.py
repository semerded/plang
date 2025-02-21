import pytest
from unittest.mock import patch
from src.exceptions import OutOfWindowBoundsError, ExpectedLengthError
from src.core.window.window import Window
from src.messenger import Messenger
from src.core.utils.coordinate import Coordinate

@pytest.mark.parametrize("input_coord, strict_positive, strict_in_window_bounds, window, expected_error", [
    ((10, 20), False, False, None, None),  # Valid case
    ((-5, 10), True, False, None, ValueError),  # Negative x with strict_positive
    ((10, -5), True, False, None, ValueError),  # Negative y with strict_positive
    ((500, 10), False, True, Window(400, 300), OutOfWindowBoundsError),  # x out of bounds
    ((10, 500), False, True, Window(400, 300), OutOfWindowBoundsError),  # y out of bounds
    ((10,), False, False, None, ExpectedLengthError),  # Too few coordinates
    ((10, 20, 30), False, False, None, ExpectedLengthError),  # Too many coordinates
])
def test_check_input(input_coord, strict_positive, strict_in_window_bounds, window, expected_error):
    with patch.object(Messenger, "error") as mock_error, \
         patch.object(Messenger, "fatalError") as mock_fatal_error, \
         patch.object(Messenger, "warning") as mock_warning:

        Coordinate.check_input(input_coord, strict_positive, strict_in_window_bounds, window)

        if expected_error:
            if expected_error in [ValueError, OutOfWindowBoundsError]:
                mock_error.assert_called_once()
            else:
                mock_fatal_error.assert_called_once()
        else:
            mock_error.assert_not_called()
            mock_fatal_error.assert_not_called()
            mock_warning.assert_not_called()
