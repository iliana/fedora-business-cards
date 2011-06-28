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
Command-line interface to business card generator. Takes no arguments; uses
optparser.OptionParser instead.
"""

from copy import copy
import decimal
from getpass import getpass
from optparse import OptionParser, OptionGroup, Option, OptionValueError
import sys

from fedora_business_cards import information
from fedora_business_cards import generate
from fedora_business_cards import export # hah


def check_decimal(option, opt, value):
    """
    Checks that value can be converted to a decimal.Decimal object.
    """
    try:
        return decimal.Decimal(value)
    except decimal.InvalidOperation:
        return OptionValueError("option %s: invalid decimal value: %s" %
                                (opt, value))

class NewOptionClass(Option):
    """
    Replacement Option class for OptionParser that includes decimal type.
    """
    TYPES = Option.TYPES + ("decimal",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["decimal"] = check_decimal

def cmdline_card_line(data):
    """
    Print a line of the business card for the cmdline frontend.
    """
    return "| %s%s |" % (data, ' '*(59-len(data)))

def main():
    """
    Call this to make things happen.
    """
    # Setup option parser
    parser = OptionParser(option_class=NewOptionClass)
    parser.usage = "%prog [options]"
    # Create decimal type
    # Base options
    parser.add_option("-u", "--username", dest="username", default="",
                      help="If set, use a different name than the one logged"+\
                      " in with to fill out business card information")
    # Size options
    size_group = OptionGroup(parser, "Size options")
    size_group.add_option("--height", dest="height",
                          default=decimal.Decimal("2"), type="decimal",
                          help="business card height (default: 2)")
    size_group.add_option("--width", dest="width",
                          default=decimal.Decimal("3.5"), type="decimal",
                          help="business card width (default: 3.5)")
    size_group.add_option("--bleed", dest="bleed", type="decimal", 
                          default=decimal.Decimal("0"), help="extra space "
                          "around card, often requested by printers "
                          "(default: 0)")
    size_group.add_option("--inch", dest="unit", default="in", const="in",
                          action="store_const",
                          help="units are specified in inches (default)")
    size_group.add_option("--mm", dest="unit", default="in", const="mm",
                          action="store_const",
                          help="units are specified in millimeters")
    # Output options
    out_group = OptionGroup(parser, "Output options")
    out_group.add_option("-d", "--dpi", dest="dpi", default=300, type="int",
                         help="DPI of exported file")
    out_group.add_option("--pdf", dest="output", default="png", const="pdf",
                         action="store_const", help="Export as PDF")
    out_group.add_option("--png", dest="output", default="png", const="png",
                         action="store_const", help="Export as PNG (default)")
    out_group.add_option("--svg", dest="output", default="png", const="svg",
                         action="store_const", help="Export as SVG")
    out_group.add_option("--eps", dest="output", default="png", const="eps",
                         action="store_const", help="Export as EPS")
    out_group.add_option("--cmyk-pdf", dest="output", default="png",
                         const="cmyk_pdf", action="store_const",
                         help="Export as PDF with CMYK color")
    # Finish setting up option parser
    parser.add_option_group(size_group)
    parser.add_option_group(out_group)
    options = parser.parse_args()[0]

    # ask for FAS login
    print "Login to FAS:"
    print "Username:",
    username = raw_input()
    password = getpass()
    if options.username == "":
        options.username = username
    infodict = information.get_information(username, password,
                                           options.username)
    # setup default content
    name = infodict['name']
    title = infodict['title']
    if infodict['gpgid'] == None:
        gpg = ''
    else:
        gpg = "GPG key ID: %s" % infodict['gpgid']
    if infodict['irc'] == None:
        lines = [infodict['email'],
                 infodict['url'],
                 '',
                 gpg,
                 '',
                 '']
    else:
        lines = [infodict['email'],
                 infodict['irc']+" on irc.freenode.net",
                 infodict['url'],
                 '',
                 "GPG key ID: "+infodict['gpgid'],
                 '']
    done_editing = False
    while not done_editing:
        print "Current business card layout:"
        print "   +"+"-"*61+"+"
        print " n "+cmdline_card_line(name)
        print " t "+cmdline_card_line(title)
        print "   "+cmdline_card_line('')
        for i in range(6):
            print (" %i " % i)+cmdline_card_line(lines[i])
        print "   "+cmdline_card_line('')
        print "   "+cmdline_card_line('')
        print "   "+cmdline_card_line('fedora'+' '*17+\
                                      'freedom | friends | features | first')
        print "   +"+"-"*61+"+"
        print "Enter a line number to edit, or [y] to accept:",
        lineno = raw_input()
        if lineno == "" or lineno == "y":
            done_editing = True
        else:
            print ("Enter new data for line %s:" % lineno),
            newdata = raw_input()
            if lineno == 'n':
                name = newdata
            elif lineno == 't':
                title = newdata
            elif lineno == '0' or lineno == '1' or lineno == '2' or \
                    lineno == '3' or lineno == '4' or lineno == '5':
                lines[int(lineno)] = newdata
    # generate front of business card
    print "Generating front...",
    sys.stdout.flush()
    name_utf8 = name.decode('utf-8')
    xml = generate.gen_front(name_utf8, title, lines, options.height,
                             options.width, options.bleed, options.unit)
    if options.output == "svg":
        export.svg_to_file(xml, options.username+'-front.'+options.output)
    elif options.output == "cmyk_pdf":
        export.svg_to_cmyk_pdf(xml, options.username+'-front.pdf',
                               options.height, options.width, options.bleed,
                               options.unit)
    else:
        export.svg_to_pdf_png(xml, options.username+'-front.'+options.output,
                              options.output, options.dpi)
    # generate back of business card
    print "Generating back...",
    sys.stdout.flush()
    xml = generate.gen_back(options.height, options.width, options.bleed,
                            options.unit)
    if options.output == "svg":
        export.svg_to_file(xml, options.username+'-back.'+options.output)
    elif options.output == "cmyk_pdf":
        export.svg_to_cmyk_pdf(xml, options.username+'-back.pdf',
                               options.height, options.width, options.bleed,
                               options.unit)
    else:
        export.svg_to_pdf_png(xml, options.username+'-back.'+options.output,
                              options.output, options.dpi)
    print "Done."
    sys.stdout.flush()
