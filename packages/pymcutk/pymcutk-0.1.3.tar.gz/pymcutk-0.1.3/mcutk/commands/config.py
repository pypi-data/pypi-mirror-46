from __future__ import print_function
import click
import glob
import os
from os.path import join
from mcutk.apps import appfactory
from mcutk.exceptions import ProjectNotFound
from mcutk.managers.conf_mgr import ConfMgr

from . import TOOLCHAINS




@click.command('config', short_help='configuration(\"~/.mcutk\") management')
@click.option('--show', is_flag=True, help='show configuration from \"~/.mcutk\"')
@click.option('--auto', is_flag=True, help='auto scan your system, then configure into \"~/.mcutk\"')
def cli(show, auto):
    """Configuration Management Command"""
    cfger = ConfMgr.load()

    if show:
        if cfger.is_empty:
            print("Need to initialize the mcutk")
            return
        print(cfger)

    if auto:
        print("scaning toolchains on your system ...\n")
        for toolname in TOOLCHAINS:
            tool = appfactory(toolname)
            app = tool.get_latest()
            if app and app.is_ready:
                print(' ----------------------------------------------------- ')
                print(' [x] {:10s} version={}, path={}'.format(app.name, app.version, app.path))
                cfger.set_app(app)
            else:
                print('Warning: failed to set %s'%toolname)
        cfger.save()

        print("\n\"{}\" have been updated successfully!".format(cfger.CONFIG_FILE))

