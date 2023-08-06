from __future__ import print_function
import click
import glob
import os
import logging
from os.path import join

from mcutk.debugger import getdebugger
from mcutk.managers.conf_mgr import ConfMgr




class Debughelper(object):

    supported_debuggers = ['jlink', 'pyocd']

    @staticmethod
    def find_debuggers():
        """Find installed debuggers from system."""

        debs = list()
        for name in Debughelper.supported_debuggers:
            debugger = getdebugger(name).get_latest()
            if debugger and debugger.is_ready:
                debs.append(debugger)
            else:
                click.echo('Error, debugger %s is unavailiable to use!'%name)

        return debs


    @staticmethod
    def list_devices(debuggers):
        """List connected devices."""

        devices = list()
        for deb in debuggers:
            for item in deb.list_connected_devices():
                devices.append(item)
        return devices


    @staticmethod
    def choose_device(device):
        """Promt user to select device."""

        debuggers = Debughelper.find_debuggers()

        if device == None:
            device = dict()

        debugger = None
        devices = None

        debugger_type = device.get('debugger_type')
        usbid = device.get('usbid')

        if usbid and debugger_type:
            pass
        else:
            selected_device = None
            # use usb id to find debugger type
            devices = Debughelper.list_devices(debuggers)
            if len(devices) == 0:
                click.secho('no devices found!', fg='red')
                return None, None

            if usbid and not debugger_type:
                for d in devices:
                    if d['usbid'] == str(usbid):
                        selected_device = d
                        break
                else:
                    logging.warning('not found usbid in system, is it right?', fg='red')
                    return None, None

            else:
                # prompt user to select
                if devices and len(devices) == 1:
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
                        except (ValueError, IndexError) as e:
                            pass
                device['usbid'] = selected_device['usbid']
                device['debugger_type'] = selected_device['type']

        if device.get('debugger_type') == 'jlink':
            if not device.get('devicename'):
                device['devicename'] = raw_input('Please input device name > ')
            if not device.get('interface'):
                interface = raw_input('SWD or JTAG > ')
                device['interface'] = "SWD" if not interface else interface

        debugger_type = device.get('debugger_type')
        usbid = device.get('usbid')

        # usbid and debugger
        if usbid and debugger_type:
            for deb in debuggers:
                if deb.name == debugger_type:
                    debugger = deb
                    break

        return debugger, device


