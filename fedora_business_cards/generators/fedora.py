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
Generator for the Fedora business card layout.

https://fedoraproject.org/wiki/Business_cards
"""

from decimal import Decimal
from getpass import getpass
from optparse import OptionGroup
from xml.dom import minidom

from fedora_business_cards import __version__
from fedora_business_cards import common
from fedora_business_cards.generators import BaseGenerator

AccountSystem = \
        common.recursive_import('fedora.client.fas2', True).AccountSystem

FEDORA_LOGO_VIEWBOX = '100 100 707.776 215.080'


class FedoraGenerator(BaseGenerator):
    rgb_to_cmyk = {
            (60, 110, 180): (1, .46, 0, 0),
            (41, 65, 114): (1, .57, 0, .38),
            (0, 0, 0): (0, 0, 0, 1),
            (255, 255, 255): (0, 0, 0, 0),
    }

    @staticmethod
    def extra_options(parser):
        option_group = OptionGroup(parser, "Options for fedora")
        option_group.add_option('-u', '--username', dest='username',
                                default='', help='If set, use a different name'
                                ' than the one logged in with to fill out'
                                ' business card information')
        return option_group

    def collect_information(self):
        # ask for FAS login
        print "Login to FAS:"
        print "Username:",
        username = raw_input()
        password = getpass()

        # get information from FAS
        fas = AccountSystem(username=username, password=password,
                            useragent='fedora-business-cards/%s' % __version__)
        if self.options.username:
            username = self.options.username
        userinfo = fas.person_by_username(username)

        # set business card fields
        self.fields['name'] = userinfo["human_name"]
        self.fields['title'] = "Fedora Project Contributor"
        if userinfo['gpg_keyid'] == None:
            gpg = ''
        else:
            gpg = "GPG key ID: %s" % userinfo['gpg_keyid']
        self.fields['lines'] = [''] * 6
        self.fields['lines'][0] = '%s@fedoraproject.org' % username
        self.fields['lines'][1] = 'fedoraproject.org'
        next_line = 2
        if userinfo['ircnick']:
            self.fields['lines'][next_line] = '%s on irc.freenode.net' % \
                    userinfo['ircnick']
            next_line += 1
        next_line += 1  # blank line
        self.fields['lines'][next_line] = gpg

        # ask user to edit information
        def cmdline_card_line(data):
            return "| %s%s |" % (data, ' ' * (59 - len(data)))

        done_editing = False
        while not done_editing:
            print "Current business card layout:"
            print "   +" + "-" * 61 + "+"
            print " n " + cmdline_card_line(self.fields['name'])
            print " t " + cmdline_card_line(self.fields['title'])
            print "   " + cmdline_card_line('')
            for i in range(6):
                print (" %i " % i) + cmdline_card_line(self.fields['lines'][i])
            print "   " + cmdline_card_line('')
            print "   " + cmdline_card_line('')
            print "   " + cmdline_card_line('fedora' + ' ' * 17 + \
                                            'freedom | friends | '
                                            'features | first')
            print "   +" + "-" * 61 + "+"
            print "Enter a line number to edit, or [y] to accept:",
            lineno = raw_input()
            if lineno == "" or lineno == "y":
                done_editing = True
            elif lineno in ['n', 't', '0', '1', '2', '3', '4', '5']:
                print ("Enter new data for line %s:" % lineno),
                newdata = raw_input()
                if lineno == 'n':
                    self.fields['name'] = newdata
                elif lineno == 't':
                    self.fields['title'] = newdata
                elif lineno in ['0', '1', '2', '3', '4', '5']:
                    self.fields['lines'][int(lineno)] = newdata

    def generate_front(self):
        # Create DOM objects
        biz_card = common.create_blank_svg(self.height, self.width, self.bleed,
                                           self.unit)
        svg_element = biz_card.documentElement
        fedora_logo = minidom.parse('/usr/share/fedora-logos/fedora_logo.svg')
        # Basic constants
        total_height = self.height + (2 * self.bleed)
        total_width = self.width + (2 * self.bleed)
        zeropointtwo = common.convert(Decimal('0.2'), 'in', self.unit)
        # White background
        white_back = biz_card.createElement('rect')
        white_back.setAttribute('height', '%s%s' % (total_height, self.unit))
        white_back.setAttribute('width', '%s%s' % (total_width, self.unit))
        white_back.setAttribute('x', '0')
        white_back.setAttribute('y', '0')
        white_back.setAttribute('fill', '#ffffff')
        svg_element.appendChild(white_back)
        # Blue stripe on right
        blue_stripe = biz_card.createElement('rect')
        blue_stripe.setAttribute('height', '%s%s' % (total_height, self.unit))
        blue_stripe.setAttribute('width', '%s%s' % (zeropointtwo + self.bleed,
                                                    self.unit))
        blue_stripe.setAttribute('x', '%s%s' % (self.width + self.bleed -
                                                zeropointtwo, self.unit))
        blue_stripe.setAttribute('y', '0')
        blue_stripe.setAttribute('fill', '#3c6eb4')
        svg_element.appendChild(blue_stripe)
        # Business card text
        usertext = biz_card.createElement('text')
        usertext.setAttribute('font-family', 'Cantarell')
        usertext.setAttribute('font-size', '10px')
        usertext.setAttribute('fill', '#000000')
        usertext.setAttribute('y', '%s%s' % (zeropointtwo + self.bleed,
                                             self.unit))
        # Name
        name = biz_card.createElement('tspan')
        name.setAttribute('font-weight', 'bold')
        name.setAttribute('font-size', '13px')
        name.setAttribute('x', '%s%s' % (zeropointtwo + self.bleed, self.unit))
        name.setAttribute('dy', '10px')
        name_text = biz_card.createTextNode(self.fields['name'])
        name.appendChild(name_text)
        usertext.appendChild(name)
        # Title
        title = biz_card.createElement('tspan')
        title.setAttribute('font-size', '11px')
        title.setAttribute('x', '%s%s' % (zeropointtwo + self.bleed,
                                          self.unit))
        title.setAttribute('dy', '13px')
        title_text = biz_card.createTextNode(self.fields['title'])
        title.appendChild(title_text)
        usertext.appendChild(title)
        # Custom rows
        self.fields['lines'] = [''] + self.fields['lines']
        y_offset = '10px'
        for data_line in self.fields['lines']:
            line = biz_card.createElement('tspan')
            line.setAttribute('x', '%s%s' % (zeropointtwo + self.bleed,
                                             self.unit))
            if data_line == '':
                y_offset = '20px'
                continue
            line.setAttribute('dy', y_offset)
            y_offset = '10px'
            line_text = biz_card.createTextNode(data_line)
            line.appendChild(line_text)
            usertext.appendChild(line)
        svg_element.appendChild(usertext)
        # Fedora logo
        logo_svg = biz_card.importNode(fedora_logo.documentElement, 9001)
        logo_svg.setAttribute('height', '.25in')
        logo_svg.removeAttribute('width')
        logo_svg.setAttribute('x', '%s%s' % \
                              (self.bleed +
                               common.convert(Decimal('0.175'), 'in',
                                              self.unit), self.unit))
        logo_svg.setAttribute('y', '%s%s' % \
                              (self.height + self.bleed - zeropointtwo -
                               common.convert(Decimal('0.25'), 'in',
                                              self.unit), self.unit))
        logo_svg.setAttribute('viewBox', FEDORA_LOGO_VIEWBOX)
        logo_svg.setAttribute('preserveAspectRatio', 'xMinYMin meet')
        svg_element.appendChild(logo_svg)
        # Four foundations set in Comfortaa
        foundations = biz_card.createElement('text')
        foundations.setAttribute('font-family', 'Comfortaa')
        foundations.setAttribute('font-size', '9px')
        foundations.setAttribute('text-anchor', 'end')
        foundations.setAttribute('x', '%s%s' % \
                                 (self.width + self.bleed - (2 * zeropointtwo),
                                                self.unit))
        foundations.setAttribute('y', '%s%s' % (self.height + self.bleed -
                                                zeropointtwo, self.unit))
        foundations_text = biz_card.createTextNode('FREEDOM. FRIENDS. '
                                                   'FEATURES. FIRST.')
        foundations.appendChild(foundations_text)
        svg_element.appendChild(foundations)
        return biz_card.toprettyxml()

    def generate_back(self):
        # Create DOM objects
        biz_card = common.create_blank_svg(self.height, self.width, self.bleed,
                                           self.unit)
        svg_element = biz_card.documentElement
        fedora_logo = minidom.parse('/usr/share/fedora-logos/'
                                    'fedora_logo_darkbackground.svg')
        # Basic constants
        total_height = self.height + (2 * self.bleed)
        total_width = self.width + (2 * self.bleed)
        # Blue background
        blue_back = biz_card.createElement('rect')
        blue_back.setAttribute('height', '%s%s' % (total_height, self.unit))
        blue_back.setAttribute('width', '%s%s' % (total_width, self.unit))
        blue_back.setAttribute('x', '0')
        blue_back.setAttribute('y', '0')
        blue_back.setAttribute('fill', '#3c6eb4')
        svg_element.appendChild(blue_back)
        # Fedora logo
        # This requires a whole bunch of calculations:
        # - The ratio between the length from the leftmost 'f' (not including
        #   the left terminal) to the right of the 'f' in the infinity logo
        #   (including the right terminal) and the width of the card is the
        #   golden ratio.
        # - The length above (the first part of the ratio) is centered in the
        #   card. This consists of 91.4408% of the width of the Fedora logo
        #   (the left terminal is 3.0853%).
        # - The aspect ratio of the Fedora logo is 3.290757.
        # - The "fedora" logotype is centered vertically on the card. This
        #   logotype consists of the bottom 69.7434% of the full logo.
        # Calculate length above
        middle_length = self.width / common.GOLDEN_RATIO
        horz_padding = (self.width - middle_length) / 2
        # Calculate width of logo
        logo_width = middle_length / Decimal('.914408')
        # Calculate horizontal position of logo
        horz_pos = horz_padding - (logo_width * Decimal('.030853')) + self.bleed
        # Calculate height of logotype
        logo_height = logo_width / Decimal('3.290757')
        logotype_height = logo_height * Decimal('.697434')
        # Calculate vertical position of logo
        vert_padding = (self.height - logotype_height) / 2
        vert_pos = self.height - (vert_padding + logo_height) + self.bleed
        # Apply everything to the logo SVG
        logo_svg = biz_card.importNode(fedora_logo.documentElement, 9001)
        logo_svg.setAttribute('width', '%s%s' % (logo_width, self.unit))
        logo_svg.setAttribute('viewBox', FEDORA_LOGO_VIEWBOX)
        logo_svg.setAttribute('preserveAspectRatio', 'xMinYMin meet')
        logo_svg.setAttribute('x', '%s%s' % (horz_pos, self.unit))
        logo_svg.setAttribute('y', '%s%s' % (vert_pos, self.unit))
        svg_element.appendChild(logo_svg)
        return biz_card.toprettyxml()

generator = FedoraGenerator
