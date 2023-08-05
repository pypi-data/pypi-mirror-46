import os
import sys
import click
import glob
import logging
from os.path import join

from mcutk.apps import appfactory
from mcutk.board import Board
from mcutk.managers.conf_mgr import ConfMgr
from mcutk.managers.debug_helper import find_debuggers, list_devices, select_device





@click.command('flash', short_help='flash debug file to board')
@click.argument('path', required=True, type=click.Path(exists=True))
@click.option('-a', '--base-address', default=0, help='base address to load.')
@click.option('-c', '--config', help='load configuration from file.')
def cli(path, base_address, config):
    gdb = None

    # get gdb
    armgcc = appfactory('armgcc').get_latest()
    if armgcc and armgcc.is_ready:
        gdb = os.path.join(armgcc.path, 'bin/arm-none-eabi-gdb')

    all_debuggers = find_debuggers()
    devices = list_devices(all_debuggers)
    selected_debugger, selected_device = select_device(all_debuggers, devices)

    selected_debugger.gdbpath = gdb
    devicename = selected_device.get('devicename')
    board = Board(devicename, **selected_device)
    board.name = selected_device.get('name', 'unknown')
    board.debugger_type = selected_debugger.name
    board.debugger = selected_debugger
    board.start_address = base_address
    board.programming(path)

