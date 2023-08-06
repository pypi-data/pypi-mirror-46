from pathlib import Path
from dephell_shells import Shells


def test_command():
    shells = Shells(bin_path=None)
    for cls in shells.shells.values():
        shell = cls(bin_path=Path(), shell_path=None)
        assert isinstance(shell.command, (list, str))


def test_args():
    shells = Shells(bin_path=None)
    for cls in shells.shells.values():
        shell = cls(bin_path=Path(), shell_path=None)
        assert isinstance(shell.args, list)
