from pathlib import Path
from dephell_shells import Shells


def test_name():
    shells = Shells(bin_path=None)
    name = shells.shell_name
    assert type(name) is str
    assert name in shells.shells


def test_path():
    shells = Shells(bin_path=None)
    path = shells.shell_path
    assert isinstance(path, Path)
    assert path.exists() is True
    assert path.stem == shells.shell_name
