# built-in
import os
import shutil
from pathlib import Path
from typing import Dict, Tuple, Type

# external
import attr
from shellingham import ShellDetectionFailure, detect_shell

# app
from ._base import BaseShell
from ._utils import cached_property


@attr.s()
class Shells:
    bin_path = attr.ib(type=Path)
    shells = dict()  # type: Dict[str, Type[BaseShell]]

    @cached_property
    def _shell_info(self) -> Tuple[str, str]:
        # detect by shellingham
        try:
            name, path = detect_shell()
        except (ShellDetectionFailure, RuntimeError):
            pass
        else:
            return name, path

        # detect by env
        for env in ('SHELL', 'COMSPEC'):
            path = os.environ.get(env)
            if path:
                return Path(path).stem, path

        # try to find any known shell
        for name in sorted(self.shells):
            path = shutil.which(name)
            if path is not None:
                return name, path

        raise OSError('cannot detect shell')

    @property
    def shell_name(self) -> str:
        return self._shell_info[0]

    @property
    def shell_path(self) -> Path:
        path = Path(self._shell_info[-1])
        if path.exists():
            return path.resolve()
        resolved = shutil.which(str(path))
        if resolved:
            return Path(resolved)
        return path

    @property
    def current(self) -> 'BaseShell':
        shell_class = self.shells.get(self.shell_name)
        if shell_class is None:
            raise LookupError('unsupported shell: {}'.format(self.shell_name))
        return shell_class(
            bin_path=self.bin_path,
            shell_path=self.shell_path,
        )

    def run(self) -> int:
        return self.current.run()
