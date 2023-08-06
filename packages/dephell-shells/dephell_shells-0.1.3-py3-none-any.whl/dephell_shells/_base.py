# built-in
import shutil
import signal
import subprocess
from pathlib import Path
from typing import Tuple, List, Optional

# external
import attr
import pexpect

# app
from ._utils import is_windows


@attr.s()
class BaseShell:
    bin_path = attr.ib(type=Path)
    shell_path = attr.ib(type=Optional[Path])

    name = NotImplemented
    activate = NotImplemented
    interactive = NotImplemented

    @property
    def executable(self) -> str:
        if self.shell_path is not None:
            return str(self.shell_path)
        return self.name

    @property
    def entrypoint(self) -> str:
        return str(self.bin_path / self.activate)

    @property
    def dimensions(self) -> Tuple[int, int]:
        columns, lines = shutil.get_terminal_size()
        return lines, columns

    @property
    def command(self) -> str:
        return 'source "{}"'.format(str(self.entrypoint))

    @property
    def args(self) -> List[str]:
        return ['-i']

    # https://github.com/ofek/hatch/blob/master/hatch/shells.py
    def run(self) -> int:
        if not self.interactive:
            result = subprocess.run(self.command, shell=is_windows())
            return result.returncode

        terminal = pexpect.spawn(
            self.executable,
            args=self.args,
            dimensions=self.dimensions,
        )

        def sigwinch_passthrough(sig, data):
            terminal.setwinsize(*self.dimensions)

        signal.signal(signal.SIGWINCH, sigwinch_passthrough)
        terminal.sendline(self.command)
        terminal.interact(escape_character=None)
        terminal.close()
        return terminal.exitstatus
