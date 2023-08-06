# built-in
from typing import List, Type

# app
from ._base import BaseShell
from ._manager import Shells
from ._utils import is_windows


def _register_shell(cls: Type[BaseShell]) -> Type[BaseShell]:
    if cls.name in Shells.shells:
        raise NameError('already registered: ' + cls.name)
    Shells.shells[cls.name] = cls
    return cls


@_register_shell
class CmdShell(BaseShell):
    name = 'cmd'
    activate = 'activate.bat'
    interactive = False

    @property
    def command(self):
        return [self.executable, '/k', self.entrypoint]


@_register_shell
class PowerShell(BaseShell):
    name = 'powershell'
    activate = 'activate.ps1'
    interactive = False

    @property
    def command(self):
        return [self.executable, '-executionpolicy', 'bypass', '-NoExit', '-NoLogo', '-File', self.activate]


@_register_shell
class BashShell(BaseShell):
    name = 'bash'
    activate = 'activate'
    interactive = True


@_register_shell
class FishShell(BaseShell):
    name = 'fish'
    activate = 'activate.fish'
    interactive = True


@_register_shell
class ZshShell(BaseShell):
    name = 'zsh'
    activate = 'activate'
    interactive = True


@_register_shell
class XonShell(BaseShell):
    name = 'xonsh'
    activate = 'activate'
    interactive = not is_windows()

    @property
    def command(self):
        path = str(self.bin_path.parent)
        if self.interactive:
            return '$PATH.insert(0, "{}")'.format(path)
        return [self.executable, '-i', '-D', 'VIRTUAL_ENV="{}"'.format(path)]

    @property
    def args(self) -> List[str]:
        return ['-i', '-D', 'VIRTUAL_ENV=' + str(self.bin_path.parent)]


@_register_shell
class TcShell(BaseShell):
    name = 'tcsh'
    activate = 'activate.csh'
    interactive = True


@_register_shell
class CShell(BaseShell):
    name = 'csh'
    activate = 'activate.csh'
    interactive = True
