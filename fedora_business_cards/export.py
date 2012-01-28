###
# fedora-business-cards - for rendering Fedora contributor business cards
# Copyright (C) 2011  Red Hat, Inc.
# Primary maintainer: Ian Weller <iweller@redhat.com>
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

from fedora_business_cards.common import convert


def run_command(args, stdin=None):
    """
    Run a command with subprocess.
    """
    #print subprocess.list2cmdline(args)
    proc = subprocess.Popen(args, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if stdin:
        return proc.communicate(stdin)
    else:
        return proc.communicate()


def svg_to_file(xmlstring, filename):
    """
    Write an SVG to a file.
    """
    handle = file(filename, 'w')
    handle.write(xmlstring.encode('utf-8'))
    handle.close()
    return True


def svg_to_pdf_png(xmlstring, filename, output_format='png', dpi=300):
    """
    Export an SVG to either a PDF or PNG.
      xmlstring = the SVG XML to export
      filename = name of file to save as
      output_format = either 'png', 'pdf', or 'eps'
      dpi = DPI to export PNG with (default: 300)
    """
    svgfilename = "/tmp/fedora-business-cards-buffer.svg"
    filename = os.path.join(os.getenv("PWD"), filename)
    svg_to_file(xmlstring, svgfilename)
    if output_format == 'png':
        run_command(['inkscape', '-C', '-z', '-d', str(dpi), '-e', filename,
                     svgfilename])
    elif output_format == 'pdf':
        run_command(['inkscape', '-C', '-z', '-T', '-A', filename,
                     svgfilename])
    elif output_format == 'eps':
        run_command(['inkscape', '-C', '-z', '-T', '-E', filename,
                     svgfilename])
    else:
        raise Exception("Invalid file format requested")
    return True


def svg_to_cmyk_pdf(xmlstring, filename, user_height, user_width, user_bleed,
                    unit, dpi=300, converter=None):
    """
    Export an SVG to a PDF while converting to CMYK.
      xmlstring = the SVG XML to export
      filename = name of file to save as
      dpi = DPI to export PDF with (default: 300)
      converter = a tuple of tuples to convert from RGB to CMYK colors. see
                  generators.fedora.rgb_to_cmyk for an example
    """
    svgfilename = "/tmp/fedora-business-cards-buffer.svg"
    filename = os.path.join(os.getenv("PWD"), filename)
    svg_to_file(xmlstring, svgfilename)
    args = ['inkscape', '-C', '-z', '-T', '-E', '/dev/stdout', svgfilename]
    eps = run_command(args)[0]
    if converter:
        eps = eps_cmyk_convert(eps, converter)
    width = int(math.ceil(convert(user_width + (user_bleed * 2), unit, 'in') *
                          dpi))
    height = int(math.ceil(convert(user_height + (user_bleed * 2), unit, 'in')
                           * dpi))
    args = ['gs', '-q', '-sDEVICE=pdfwrite', '-dAutoRotatePages=/None',
            '-r%s' % dpi, '-g%sx%s' % (width, height),
            '-sOutputFile=%s' % filename, '-', '-c', 'quit']
    print run_command(args, eps)[0]
    return True


def eps_cmyk_convert(epsdata_in, converter):
    # first, normalize the output through eps2eps
    args = ['eps2eps', '/dev/stdin', '/dev/stdout']
    epsdata = run_command(args, epsdata_in)[0]
    epsdata_new = ''
    # go through each line and check for color commands
    for line in epsdata.split('\n'):
        # parse color commands
        # R G B rG
        if line[-2:] == 'rG':
            (red, green, blue) = line[:-2].split()
        # R GB r3
        elif line[-2:] == 'r3':
            (red, green) = line[:-2].split()
            blue = green
        # RB G r5
        elif line[-2:] == 'r5':
            (red, green) = line[:-2].split()
            blue = red
        # RG B r6
        elif line[-2:] == 'r6':
            (red, blue) = line[:-2].split()
            green = red
        # RGB G
        elif line[-2:] == ' G':
            red = line.split()[0]
            green = red
            blue = red
        # K
        elif line == 'K':
            red = 0
            green = 0
            blue = 0
        else:
            epsdata_new += line + '\n'
        # check converter
        rgb = [int(x) for x in (red, green, blue)]
        if rgb in converter:
            epsdata_new += '%.4f %.4f %.4f %.4f setcmykcolor' % converter[rgb]
