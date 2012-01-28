###
# fedora-business-cards - for rendering Fedora contributor business cards
# Copyright (C) 2012  Red Hat, Inc. and others.
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
from optparse import OptionParser, OptionGroup, Option, OptionValueError
import sys

from fedora_business_cards import common
from fedora_business_cards import export  # hah
from fedora_business_cards import generators


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


def main():
    """
    Call this to make things happen.
    """
    # Setup option parser
    parser = OptionParser(option_class=NewOptionClass)
    parser.usage = "%prog [options] GENERATOR"
    # General options
    parser.add_option("--list-generators", dest="showgen", default=False,
                      action="store_true", help="display list of generators")
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
                         help="Export as PDF with CMYK color (if the generator"
                         " supports it)")

    # Finish setting up option parser
    parser.add_option_group(size_group)
    parser.add_option_group(out_group)
    # Check for generator-specific option groups
    for module_name in generators.__all__:
        try:
            module = common.recursive_import(
                'fedora_business_cards.generators.%s' % module_name)
            generator = module.generator
            option_group = generator.extra_options(parser)
            if option_group:
                parser.add_option_group(option_group)
        except ImportError:
            pass

    # Parse arguments
    (options, args) = parser.parse_args()

    if options.showgen:
        print "Generators: %s" % ', '.join(generators.__all__)
        sys.exit()

    if len(args) != 1:
        parser.error("Exactly one argument (the generator) is required")

    # Import the generator we care abuot
    try:
        module = common.recursive_import('fedora_business_cards.generators.%s'
                                         % args[0])
    except ImportError:
        parser.error("Generator '%s' does not exist or is broken" % args[0])
    gen = generator(options)

    # collect information from user if necessary
    gen.collect_information()

    # generate front of business card
    print "Generating front...",
    sys.stdout.flush()
    xml = gen.generate_front()
    if options.output == "svg":
        export.svg_to_file(xml, 'front.' + options.output)
    elif options.output == "cmyk_pdf":
        export.svg_to_cmyk_pdf(xml, 'front.pdf', options.height, options.width,
                               options.bleed, options.unit, gen.rgb_to_cmyk)
    else:
        export.svg_to_pdf_png(xml, 'front.' + options.output, options.output,
                              options.dpi)
    # generate back of business card
    print "Generating back...",
    sys.stdout.flush()
    xml = gen.generate_back()
    if options.output == "svg":
        export.svg_to_file(xml, 'back.' + options.output)
    elif options.output == "cmyk_pdf":
        export.svg_to_cmyk_pdf(xml, 'back.pdf', options.height, options.width,
                               options.bleed, options.unit, gen.rgb_to_cmyk)
    else:
        export.svg_to_pdf_png(xml, 'back.' + options.output, options.output,
                              options.dpi)
    print "Done."
    sys.stdout.flush()
