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
import math
import os

RGB_TO_CMYK = (
    # Inkscape .46 output
    ("0 0 0 setrgbcolor", "0 0 0 1"),
    ("1 1 1 setrgbcolor", "0 0 0 0"),
    ("0.23529412 0.43137255 0.70588237 setrgbcolor", "1 0.46 0 0"),
    ("0.16078432 0.25490198 0.44705883 setrgbcolor", "1 0.57 0 0.38"),
    # Inkscape .47 output
    ("0 g", "0 0 0 1"),
    ("1 g", "0 0 0 0"),
    ("0.235294 0.431373 0.705882 rg", "1 0.46 0 0"),
    ("0.160784 0.254902 0.447059 rg", "1 0.57 0 0.38"),
)


def svg_to_file(xmlstring, filename):
    """
    Write an SVG to a file.
    """
    handle = file(filename, 'w')
    handle.write(xmlstring.encode('utf-8'))
    handle.close()
    return True


def svg_to_pdf_png(xmlstring, filename, format='png', dpi=300):
    """
    Export an SVG to either a PDF or PNG.
      xmlstring = the SVG XML to export
      filename = name of file to save as
      format = either 'png', 'pdf', or 'eps'
      dpi = DPI to export PNG with (default: 300)
    """
    svgfilename = "/tmp/fedora-business-cards-buffer.svg"
    filename = os.path.join(os.getenv("PWD"), filename)
    svg_to_file(xmlstring, svgfilename)
    command = ['inkscape', '-C -z -d', str(dpi), '-e', filename, svgfilename]
    if format == 'png':
        proc = subprocess.Popen(' '.join(command), shell=True,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.communicate()
    elif format == 'pdf':
        command[1] = '-C -z -T -d'
        command[3] = '-A'
        proc = subprocess.Popen(' '.join(command), shell=True,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.communicate()
    elif format == 'eps':
        command[1] = '-C -z -T -d'
        command[3] = '-E'
        proc = subprocess.Popen(' '.join(command), shell=True,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.communicate()
    else:
        raise Exception("Invalid file format requested")
    return True


def svg_to_cmyk_pdf(xmlstring, filename, dpi=300, converter=RGB_TO_CMYK):
    """
    Export an SVG to a PDF while converting to CMYK.
      xmlstring = the SVG XML to export
      filename = name of file to save as
      dpi = DPI to export PDF with (default: 300)
      converter = a tuple of tuples to convert from RGB to CMYK colors. see
                  RGB_TO_CMYK for an example
    """
    svgfilename = "/tmp/fedora-business-cards-buffer.svg"
    filename = os.path.join(os.getenv("PWD"), filename)
    svg_to_file(xmlstring, svgfilename)
    command = "inkscape -C -z -T -E /dev/stdout %s" % svgfilename
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    eps = proc.communicate()[0]
    for that in converter:
        eps = eps.replace("\n%s" % that[0],
                          "\n%s setcmykcolor" % that[1])
    command = "inkscape -z -W %s" % svgfilename
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    width = str(int(math.ceil(float(proc.communicate()[0])*dpi/90)))
    command = "inkscape -z -H %s" % svgfilename
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    height = str(int(math.ceil(float(proc.communicate()[0])*dpi/90)))
    command = "gs -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -r%s -g%sx%s -sOutputFile='%s' - -c quit" % (str(dpi), width, height, filename)
    proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(eps)
    return True
