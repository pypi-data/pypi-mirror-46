
Dephell Shells
==============

Run shell for virtual environment.

Installation
------------

Install from `PyPI <https://pypi.org/project/dephell-shells/>`_\ :

.. code-block:: bash

   python3 -m pip install --user dephell_shells

Usage
-----

.. code-block:: python

   from pathlib import Path
   from dephell_shells import Shells

   shells = Shells(bin_path=Path('/home/gram/.../dephell-nLn6/bin'))
   shells.current
   # ZshShell(bin_path=Path('/home/gram/.../dephell-nLn6'), shell_path=Path('/usr/bin/zsh'))
   shells.current.run()

CLI
---

Show current shell path:

.. code-block:: bash

   $ python3 -m dephell_shells
   /bin/zsh

Actiavate venv:

.. code-block:: bash

   $ python3.7 -m dephell_shells ./venv/bin
