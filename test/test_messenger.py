import pytest

from src.messenger import Messenger

def test_info(capsys):
    Messenger.info("This is useful info!")
    read = capsys.readouterr()
    
    assert read.out == "This is useful info!\n"