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

from gi.repository import GLib

from subprocess import Popen, PIPE, call
from threading  import Thread
from time       import sleep

class JupyterNotebookThread(Thread):
    def __init__(self, on_load_callback, on_quit_callback, on_close_callback, notebook):
        super().__init__(name="JypyterNotebookThread", target = self.restart)
        self.on_load_callback  = on_load_callback
        self.on_quit_callback  = on_quit_callback
        self.on_close_callback = on_close_callback
        self.notebook = notebook

    def restart(self):
        if self.launch():
            GLib.idle_add(self.on_load_callback, self.url)
            while self.p.poll() is None:
                sleep(1)
            GLib.idle_add(self.on_close_callback)
        else:
            print("Unable to start jupyter-notebook")


    def stop(self):
        self.p.terminate()

    def launch(self):
        args = ["jupyter-notebook"]
        if self.notebook != None:
            args += [self.notebook]
        self.p = Popen(args, stdout = PIPE, stderr = PIPE)

        self.url = None

        line = self.p.stderr.readline().decode('ascii')
        while line != "":
            if "http://" in line:
                self.url = "http://" + line.split("http://")[1].strip('\n')
                return True
            line = self.p.stderr.readline().decode('ascii')

        return False
