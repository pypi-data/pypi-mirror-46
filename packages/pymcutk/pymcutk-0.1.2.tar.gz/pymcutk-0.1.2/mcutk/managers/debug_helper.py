from __future__ import print_function
import click
import glob
import os
from os.path import join

from mcutk.debugger import getdebugger
from mcutk.managers.conf_mgr import ConfMgr


DEBUGGERS = ['jlink', 'pyocd']


def find_debuggers():
    """Find installed debuggers from system."""

    all_debuggers = list()
    for name in DEBUGGERS:
        debugger = getdebugger(name).get_latest()
        if debugger and debugger.is_ready:
            all_debuggers.append(debugger)
        else:
            click.echo('Error, debugger %s is unavailiable to use!'%name)
    return all_debuggers


def list_devices(debuggers):
    """List connected devices."""

    devices = list()
    for deb in debuggers:
        for item in deb.list_connected_devices():
            devices.append(item)
    return devices


def select_device(debuggers, devices):
    """Promt user to select device."""

    selected_device = None
    selected_debugger = None

    if len(devices) == 0:
        print('no devices found.')
        return None, None

    elif len(devices) == 1:
        selected_device = devices[0]
    else:
        for index, item in enumerate(devices):
            print('{:2} - {:10} - {} - {}'.format(index, item['type'], item.get('name'), item['usbid']))

        while True:
            try:
                index = raw_input('Please input the index to select device > ')
                index = int(index)
                selected_device = devices[index]
                break
            except Exception:
                pass

    if selected_device['debugger'] == 'jlink':
        selected_device['devicename'] = raw_input('Please input device name > ')

    debugger_type = selected_device['debugger']
    for deb in debuggers:
        if deb.name == debugger_type:
            selected_debugger = deb
            break
    else:
        print("Error: unknown debugger type: %s"%debugger_type)

    return selected_debugger, selected_device
