# This file is part of "Jupyter Notebook Launcher" which is released
# under GPL. See file LICENCE.md or go to http://www.gnu.org/licenses/
# for full license details.
#
# Jupyter Notebook Launcher is a Jupyter Notebook Launcher and Indicator
# for Ubuntu.
#
# Copyright (c) 2017 Gabriele N. Tornetta <phoenix1987@gmail.com>.
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

from subprocess    import call

from .rsrc_mgr     import rsrc
from .thread       import JupyterNotebookThread
from .socket       import JupyterNotebookSocket, JNPSocketCmd

APPINDICATOR_ID = 'jupyter-notebook-launcher'

### Command Line Arguments #####################################################

from argparse      import ArgumentParser as ArgParse

def parse_args():
    p = ArgParse(description="Jupyter Notebook Launcher and Indicator for Ubuntu.")

    p.add_argument('notebook', type=str, nargs='?', help='Path to a notebook file', default="")

    return p.parse_args()

################################################################################

class JupyterNotebookIndicator(appindicator.Indicator):
    def __init__(self):
        self.is_running = False

        args = parse_args()
        print("*** " + args.notebook + " ***")

        self.socket = JupyterNotebookSocket(self.on_launch)
        if not self.socket.listen():
            self.socket.send_cmd("OPEN:" + args.notebook)
            self.is_running = True
            return

        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, rsrc('inactive.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.start_jupyter_notebook(args.notebook)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        return self.indicator.__dict__[name]

    def start_jupyter_notebook(self, notebook = None):
        if notebook: print("Launching notebook '{}'".format(notebook))
        self.thread = JupyterNotebookThread(self.on_load, self.on_quit, self.on_close, notebook)
        self.thread.start()

    def build_menu(self):
        menu = gtk.Menu()

        # Action
        self.item_action = gtk.MenuItem('Launching...')
        self.item_action.connect('activate', self.on_action)
        self.item_action.set_sensitive(False)

        menu.append(self.item_action)

        # Quit
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.on_quit)
        menu.append(item_quit)

        menu.show_all()

        return menu

    ### Callbacks ##############################################################

    def on_action(self, source, data = None):
        if self.item_action.get_sensitive():
            if hasattr(self, "url"):
                if self.url:
                    call(["gvfs-open", self.url])
                else:
                    self.item_action.set_label('Launching...')
                    self.item_action.set_sensitive(False)
                    self.start_jupyter_notebook(data)

    def on_quit(self, source):
        self.thread.stop()
        self.socket.close()
        gtk.main_quit()

    def on_load(self, url):
        self.url = url
        self.item_action.set_sensitive(True)
        self.item_action.set_label("Open in browser")
        self.indicator.set_icon(rsrc("active.svg"))

    def on_close(self):
        self.url = None
        self.item_action.set_label("Restart")
        self.item_action.set_sensitive(True)
        self.indicator.set_icon(rsrc("inactive.svg"))

    def on_launch(self, cmd, data = None):
        if cmd == JNPSocketCmd.OPEN:
            self.on_action(None, data)
