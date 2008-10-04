###
# fedora-business-cards - for rendering Fedora contributor business cards
# Copyright (C) 2008  Ian Weller <ianweller@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###

"""
Controls the locations of configuration files, and imports configurations from
all those files in a specific order.
"""

import iniparse
import os

# locations, in reverse-order of priority
LOCATIONS = ['/'.join(__file__.split('/')[:-1]+['config.ini']),
             'config.ini', # in current working directory
             '/usr/share/fedora-business-cards/config.ini',
             '/etc/fedora-business-cards.ini',
             os.getenv('HOME')+'/.fedora-business-cards.ini']

parser = iniparse.ConfigParser()

# import the configs
for i in LOCATIONS:
    parser.read(i)

__all__ = ('parser')
