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

from gi.repository import Gio
from gi.repository import GLib

JNL_PORT = 50005
CMD_BUF_SIZE = 256

class JNPSocketCmd:
    OPEN = 0

class JupyterNotebookSocket:
    def __init__(self, socket_callback):
        self.socket = Gio.Socket.new(Gio.SocketFamily.IPV4, Gio.SocketType.STREAM, Gio.SocketProtocol.DEFAULT)
        self.address = Gio.InetSocketAddress.new(Gio.InetAddress.new_from_string("127.0.0.1"), JNL_PORT)
        self.callback = socket_callback

    def listen(self):
        try:
            self.socket.bind(self.address, False)
            self.socket.listen()
        except GLib.Error:
            return False

        GLib.io_add_watch(GLib.IOChannel.unix_new(self.socket.get_fd()), GLib.PRIORITY_DEFAULT, GLib.IOCondition.IN, self.receive_cmd)

        return True

    def receive_cmd(self, channel, condition):
        ret = False

        buf = bytes(CMD_BUF_SIZE)
        socket = self.socket.accept()
        n = socket.receive(buf)
        if n > 0:
            cmd, args = buf.decode("utf-8")[:n].split(':', 1)
            GLib.idle_add(self.callback, getattr(JNPSocketCmd, cmd), args)
            ret = True
        socket.close()
        return ret

    def send_cmd(self, cmd):
        self.socket.connect(self.address)
        self.socket.send(cmd.encode("utf-8"))
        self.socket.close()

    def close(self):
        self.socket.close()
