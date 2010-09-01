#!/usr/bin/python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) 2010 Mathieu Comandon <strycore@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import sys
import os
import gtk
import logging
import optparse

# This is inspired by gwibber because the quickly method was starting to be 
# annoying, there might be some issues left with running from source tree or
# packaged version (and running from source with the packaged version installed)
# See Gwibber source for more inspiration.
LAUNCH_PATH=os.path.abspath(sys.path[0])
DATA_PATH=os.path.join(LAUNCH_PATH, '..', 'data')
SOURCE_PATH=os.path.join(LAUNCH_PATH, '..')
sys.path.insert(0, SOURCE_PATH)

from lutris.installer import Installer
from lutris.gui.lutriswindow import LutrisWindow

def new_lutris_window():
    """ Returns an instantiated LutrisWindow object. """
    ui_filename = os.path.join(DATA_PATH, 'ui', 'LutrisWindow.ui')
    if not os.path.exists(ui_filename):
        raise IOError('File not found')
    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    window = builder.get_object("lutris_window")
    window.finish_initializing(builder,DATA_PATH)
    return window

# Support for command line options.
parser = optparse.OptionParser(version="%prog %ver")
parser.add_option("-v", "--verbose", action="store_true",
                  dest="verbose", help="Show debug messages")
(options, args) = parser.parse_args()

# Set the logging level to show debug messages.
if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('logging enabled')

# Run the application.
game = None
for arg in args:
    if arg.startswith('lutris://'):
        print 'Installing ' + arg[9:]
        game = arg[9:]
        break
if game:
    installer = Installer(game)
    success = installer.pre_install()
    if success is False:
        print "Unable to install game"
        print installer.installer_errors
    else:
        print "Ready! Launching installer."
        installer.install()
    exit()
else:
    lutris_window = new_lutris_window()
    lutris_window.show()
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
