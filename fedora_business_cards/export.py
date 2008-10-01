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
Functions to export cards from SVGs.
"""

import subprocess


def svg_to_pdf_png(xmlstring, filename, format='png', dpi=300):
    """
    Export an SVG to either a PDF or PNG.
      xmlstring = the SVG XML to export
      filename = name of file to save as
      format = either 'png' or 'pdf'
      dpi = DPI to export PNG with (default: 300)
    """
    stdin = xmlstring.encode('iso-8859-1')
    command = ['inkscape', '-d', str(dpi), '-e', filename, '/dev/stdin']
    if format == 'png':
        sp = subprocess.Popen(' '.join(command), shell=True,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
        sp.communicate(stdin)
    elif format == 'pdf':
        command[3] = '-A'
        sp = subprocess.Popen(' '.join(command), shell=True,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
        sp.communicate(stdin)
    else:
        raise Exception("Invalid file format requested")
