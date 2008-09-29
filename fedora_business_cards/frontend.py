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
Frontend to the business card generator. Theoretically expandable to GUI and
whatnot, but for now just has a command-line interface.
"""

from optparse import OptionParser

def cmdline():
    parser = OptionParser()
    parser.add_option("-d", "--dpi", dest="dpi", default=300,
                      help="DPI of exported PNG")
    options = parser.parse_args()[0]
