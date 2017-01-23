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

from . import data
from pkg_resources import ResourceManager, get_provider

manager  = ResourceManager()
provider = get_provider("jupyter_notebook_launcher.data")

def rsrc(name):
    global manager
    global provider

    return provider.get_resource_filename(manager, name)
