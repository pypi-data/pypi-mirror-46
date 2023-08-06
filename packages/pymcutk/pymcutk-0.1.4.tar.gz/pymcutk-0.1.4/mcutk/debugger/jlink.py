
import os
import sys
import re
import platform
import subprocess
import logging
import threading
import time
import tempfile
from mcutk.debugger.base import DebuggerBase

PY = sys.version_info[0]


class JLINK(DebuggerBase):
    """J-Link debugger is a wrapper for SEGGER-JLink.
    """

    @staticmethod
    def get_latest():
        """Get latest installed instance from the system.
        """
        return _scan_installed_instance()



    def __init__(self, *args, **kwargs):
        """Create an instance of the JLink debugger class.
        """
        super(JLINK, self).__init__("jlink", *args, **kwargs)
        self._jlink_exe = os.path.join(self.path, "JLink.exe")



    @property
    def is_ready(self):
        return os.path.exists(self._jlink_exe)



    def _run_jlink_exe(self, jlink_exe_cmd, timeout_sec):
        """Run jlink.exe process.

        Arguments:
            jlink_exe_cmd {list or string} -- JLink.exe or JLinkExe command line
            timeout_sec {int} -- Max timeout in seconds

        Returns:
            Tuple -- (retcode, output)
        """
        def timeout_exceeded(p):
            p.kill()
            raise Exception('JLink process:%s exceeded timeout!', p.pid)

        kwargs = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.STDOUT,
        }
        if PY > 2:
            kwargs['encoding'] = 'utf8'

        process = subprocess.Popen(jlink_exe_cmd, **kwargs)
        if timeout_sec is not None:
            timeout = threading.Timer(timeout_sec, timeout_exceeded, [process])
            timeout.start()

        # Grab output of JLink.
        output, _ = process.communicate()
        if timeout_sec is not None:
            timeout.cancel()

        logging.debug('JLink response: {0}'.format(output))
        return process.returncode, output




    def run_script(self, filename, timeout_sec=60):
        """Run jlink script with JLink.exe with a timeout timer.

        Arguments:
            filename -- {string} path to jlink script
            timeout_sec -- {int} seconds for timeout value, default 60s.

        Returns:
            tuple -- (jlink_exit_code, console_output)
        """

        if self._board:
            jlink_exe_cmd = [
                self._jlink_exe,
                "-SelectEmuBySN",
                "{0}".format(self._board.usbid),
                "-Device",
                "{0}".format(self._board.devicename),
                "-IF",
                "{0}".format(self._board.interface),
                "-Speed",
                "auto",
                '-autoconnect',
                '1',
                "-ExitOnError",
                "-CommanderScript",
                filename
            ]
            # default jtag chain
            if self._board.interface.upper() == "JTAG":
                jlink_exe_cmd.append("-jtagconf")
                jlink_exe_cmd.append("-1,-1")

        else:
            jlink_exe_cmd = [
                self._jlink_exe,
                "-SelectEmuBySN",
                "6210000",
                "-CommanderScript",
                filename
            ]



        return self._run_jlink_exe(jlink_exe_cmd, timeout_sec)




    def run_commands(self, commands, timeout_sec=60):
        """Run a list of commands by JLink.exe.

        Arguments:
            commands -- {list} list of JLink.exe commands
            timeout_sec -- {int} seconds for timeout value
        """
        # Create temporary file to hold script.
        script_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        commands = '\n'.join(commands)
        script_file.write(commands)
        script_file.close()
        logging.debug('Using script file name: {0}'.format(script_file.name))
        logging.debug('Running JLink commands: {0}'.format(commands))

        return self.run_script(script_file.name, timeout_sec)


    def test_conn(self):
        """Test debugger connection."""

        p1 = re.compile("Connecting to J-Link via USB.{3}FAILED")
        p2 = re.compile("Found.*JTAG")
        p3 = re.compile("Found.*SW")
        p4 = re.compile("JTAG chain detection found 1 devices")

        commands = [
            'regs',
            'qc'
        ]
        # Run commands.
        _, output = self.run_commands(commands, timeout_sec=30)
        if p1.search(output) is not None:
            return "NotConnected"
        elif (p2.search(output) is not None) or (p3.search(output) is not None) \
            or (p4.search(output) is not None):
            return "NoError"
        else:
            return "Error"


    def erase(self):
        """Erase flash."""
        commands = [
            'r',      # Reset
            'erase',  # Erase
            'r',      # Reset
            'q'       # Quit
        ]
        self.run_commands(commands)


    def unlock(self):
        """Unlock kientis device."""

        commands = [
            'unlock Kinetis',
            'q'
        ]
        self.run_commands(commands)



    def reset(self):
        """Reset chip and not halt."""
        commands = [
            'rnh',      # Reset
            'q'         # Quit
        ]
        # Run commands.
        self.run_commands(commands, timeout_sec=30)




    def flash(self, filepath, addr=0):
        """Program binary to flash.
        The file could be ".bin" or ".hex". addr is the start address.
        """
        address = addr
        if self._board.start_address:
            address = self._board.start_address

        # Build list of commands to program hex files.
        commands = ['r']   # Reset

        # Program each hex file.
        if filepath.endswith(".hex"):
            commands.append('loadfile "{0}"'.format(filepath))

        elif filepath.endswith(".bin"):
            commands.append('loadbin "{0}" {1}'.format(filepath, address))

        commands.extend([
            'r',  # Reset
            'g',  # Run the MCU
            'q'   # Quit
        ])
        logging.info("flash start address: %s", address)
        # call registerd callback function
        self._call_registered_callback("before-load")
        # Run commands.
        return self.run_commands(commands)


    def list_connected_devices(self):
        """Return a list of connected id list."""

        devices = list()
        ret, raw_data = self.run_commands([ "ShowEmuList", "qc"], 10)
        if ret != 0:
            return devices

        reg1 = re.compile(r"number: -{0,1}\d{5,15}, ProductName:")
        reg2 = re.compile(r"-{0,1}\d{5,15}")

        for line in raw_data.split('\n'):
            if reg1.search(line)is not None:
                m = reg2.search(line)
                if m is not None:
                    usb_id = m.group(0)
                    if '-' in usb_id:
                        usb_id = str(0xFFFFFFFF + int(usb_id) + 1)
                    devices.append({'debugger': 'jlink', "type": 'jlink', 'usbid': usb_id})

        return devices



    def get_gdbserver(self, **kwargs):
        """Return gdbserver startup shell command.

        Example returns:
            JLinkGDBServerCL.exe -if <JTAG/SWD> -speed auto -device <device name> -port <port>
            --singlerun -strict -select usb=<usb serial number>
        """

        board = kwargs.get('board')
        speed = kwargs.get('speed', 'auto')
        interface = kwargs.get('interface', 'SWD')
        port = kwargs.get('port')
        usbid = kwargs.get('usbid')
        jlinkscript = kwargs.get('jlinkscript')
        devicename = kwargs.get('devicename')


        if board is None:
            board = self._board

        if board and board.gdbport:
            devicename = board.devicename
            interface = board.interface
            port = board.gdbport
            usbid = board.usbid

        if not devicename:
            logging.warning('jlink: not configure device name.')

        gdbserverExe = os.path.join(self.path, "JLinkGDBServerCL.exe")
        options = "-if {} -singlerun -strict".format(interface, devicename)

        if devicename:
            options += " -device %s"%devicename

        if usbid not in [None, ""]:
            options = "-select usb={} {}".format(usbid, options)

        if port:
            options += " -port %s"%port

        if speed:
            options += " -speed %s"%speed

        if jlinkscript:
            options += " -jlinkscriptfile " + jlinkscript

        return "\"%s\" %s"%(gdbserverExe, options)



    @staticmethod
    def gdb_init_template():
        """Defined default gdb commands for J-Link gdb-server."""

        commands = '''
set tcp connect-timeout 10
set remotetimeout 10
target remote localhost: {gdbport}
monitor speed auto
monitor reset 0
monitor halt
load
monitor reg sp = {sp}
monitor reg pc = {pc}
monitor go
q
'''
        return commands







def _scan_installed_instance():
    if os.name == "nt":
        try:
            import _winreg as winreg
        except ImportError:
            import winreg

        try:

            root_entry = "SOFTWARE\WOW6432Node\SEGGER\J-Link"
            jlink_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, root_entry, 0, winreg.KEY_READ)
            path = winreg.QueryValueEx(jlink_key, "InstallPath")[0]
            version = winreg.QueryValueEx(jlink_key, "CurrentVersion")[0]
            winreg.CloseKey(jlink_key)
            return JLINK(path, version=version)
        except WindowsError:
            return None
