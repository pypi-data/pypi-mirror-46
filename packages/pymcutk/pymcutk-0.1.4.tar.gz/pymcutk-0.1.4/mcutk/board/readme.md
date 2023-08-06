mcutk.board
-----------

## The relationship of board and debugger


- Swith debugger

    ```python
    # get debugger instance
    jlinkDebugger = JLINK.get_latest()
    board.debugger = jlinkDebugger

    # switch to pyocd
    pyocdDebugger = PYOCD.get_latest()
    board.debugger = pyocdDebugger
    ```

- Programming

    ```python
    board.programming('image')
    board.debugger.reset()
    ```

- Flash binary

    ```python
    board.debugger.flash('hello.bin')
    ```

- gdb programming steps

    - Default

    ```python
    board.debugger.gdb_program('hello.out')
    ```
    - Add extra options for gdb server commands

    Example:

    ```python
    '''
    debugger is jlink, we want to start jlink gdb server with a initialzation script.
    scirpt name: sdram_init.jlinkscript.
    '''
    gdbserver_cmd = board.debugger.get_gdbserver()
    gdbserver_cmd += ' --jlinkscript sdram_init.jlinkscript'

    board.debugger.gdb_program('hello.out', gdbserver_cmdline=gdbserver_cmd)
    ```

    - Custom gdb init commands

    Example:

    ```python
    gdb_init = '''
    target remote localhost: %s
    monitor reset
    load
    continue
    '''%board.gdbport
    board.debugger.gdb_program('hello.out', gdbserver_cmdline=gdbserver_cmd, gdbinit_commands=gdb_init)
    ```




# How to add a new board?

`mcutk.baseboard.Board` could be used for most platforms and most debuggers.For some reasons, we have to custom the programming method. If you want to custom the board, you can rewrite the functions by inheriting the base board.

- Add a new board module in `./mcutk/board` directory
    1. Create a new folder and rename it with the board name
    1. Create new file "__init__.py": tell python that current folder is a module.

- Add a new file(`<new_board>.py`) to include the new board class.

    - You can custom the programming method in `board.programming()`

For exmaple:

```python
class Board(board.Board):

    def _binloader(self, filepath):
        """Use binloader to download program to flash"""
        pass

    def _jlink(self, filepath):
        """Use jlink to download program to flash"""
        pass

    def programming(self, filepath, target):
        # when debugger is jlink
        if self.debugger_type == 'jlink':
            # custom the target
            if target == 'debug':
                self._binloader(filepath)
            else:
                self._jlink(filepath)
        else:
            self.debugger.gdb_program(filepath)
```

- Don't forget to expose the Board class in `__init__.py`

Example:

```python
from .mimxrt1020 import Board

__all__ = ["Board"]
```

