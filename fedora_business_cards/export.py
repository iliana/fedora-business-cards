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

# Thanks much to Jef Spaleta for this code.

import rsvg
import cairo
from StringIO import StringIO

if not cairo.HAS_PDF_SURFACE:
    raise SystemExit('cairo was not compiled with PDF support')
if not cairo.HAS_PNG_FUNCTIONS:
    raise SystemExit('cairo was not compiled with PNG support')


def svg_to_pdf_png(xmlstring, filename, format='png', dpi=300):
    """
    Export an SVG to either a PDF or PNG.
      xmlstring = the SVG XML to export
      filename = name of file to save as
      format = either 'png' or 'pdf'
      dpi = DPI to export PNG with (default: 300)
    """
    svg = rsvg.Handle(data=xmlstring)
    if format == "pdf":
        pdffile = file(filename, 'w')
    else:
        pdffile = StringIO()
    width = int(svg.props.width/90.*dpi)
    height = int(svg.props.height/90.*dpi)
    surface = cairo.PDFSurface(pdffile, width, height)
    ctx = cairo.Context(surface)
    ctx.scale(dpi/90., dpi/90.)
    svg.render_cairo(ctx)
    if format == "png":
        surface.write_to_png(filename)
    surface.finish()
    pdffile.close()
