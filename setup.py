#!/usr/bin/env python
#
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

from setuptools import setup, find_packages

setup(
    name         = 'jupyter-notebook-launcher',
    version      = '0.1',
    description  = 'Launcher for jupyter notebook engine with Unity indicator support',
    author       = 'Gabriele N. Tornetta',
    author_email = 'phoenix1987@gmail.com',
    url          = 'https://launchpad.net/jupyter-notebook-launcher',
    packages     = ["jupyter_notebook_launcher"],
    requires     = [],
    entry_points = { 'gui_scripts' : [ 'jupyter-notebook-launcher=jupyter_notebook_launcher:main' ] },
    package_data = { 'jupyter_notebook_launcher' : ['data/*.*'] },
    data_files   = [ ('share/icons/hicolor/scalable/apps', ['jupyter.svg']),
                     ('share/applications', ['jupyter-notebook-launcher.desktop'])
                   ],
    zip_safe     = False
)
