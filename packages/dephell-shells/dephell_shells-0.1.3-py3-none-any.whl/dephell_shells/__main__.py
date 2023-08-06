from pathlib import Path
from sys import argv

from . import Shells

if len(argv) == 1:
    print(Shells(bin_path=Path()).shell_path)
elif len(argv) == 2:
    Shells(bin_path=Path(argv[1])).run()
