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
    """
    Command-line interface to business card generator. Takes no arguments; uses
    optparser.OptionParser instead.
    """
    parser = OptionParser()
    parser.usage = "%prog [options] [outfile]"
    parser.add_option("-d", "--dpi", dest="dpi", default=300, type="int",
                      help="DPI of exported file")
    parser.add_option("-t", "--template", dest="template",
                      default="northamerica", help="Name of template to use, "+\
                      "run with --list-templates to see a list")
    parser.add_option("--list-templates", dest="template", action="store_true",
                      dest="listtemplates", default=False,
                      help="List available templates")
    parser.add_option("-u", "--username", dest="username", default="",
                      help="If set, use a different name than the one logged"+\
                      " in with to fill out business card information")
    parser.add_option("--pdf", dest="output", default="png", const="pdf",
                      action="store_const", help="Export as PDF")
    parser.add_option("--png", dest="output", default="png", const="png",
                      action="store_const", help="Export as PNG (default)")
    options = parser.parse_args()[0]
