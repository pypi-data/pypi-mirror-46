from __future__ import print_function
import click
import glob
import os
from os.path import join

from mcutk.debugger import getdebugger
from mcutk.managers.conf_mgr import ConfMgr
from mcutk.managers.debug_helper import find_debuggers, list_devices, select_device


@click.command('gdbserver', short_help='start a standalone gdbserver')
@click.option('-t', '--type', default='jlink', help='debugger type, jlink/pyocd.')
@click.option('-u', '--usbid', help='unique usb id')
@click.option('-p', '--port', help='specific server port')
def cli(type, usbid, port):
    """ Start a gdb server."""

    cfger = ConfMgr.load()

    all_debuggers = find_debuggers()
    devices = list_devices(all_debuggers)
    selected_debugger, selected_device = select_device(all_debuggers, devices)
    if port:
        selected_device['port'] = port
    if selected_debugger and selected_device:
        selected_debugger.start_gdbserver(**selected_device)

