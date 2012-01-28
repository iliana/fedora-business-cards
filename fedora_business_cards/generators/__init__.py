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
Various business card generators can be placed here (i.e., a Fedora business
card layout, a Beefy Miracle business card layout).
"""

from fedora_business_cards import common


class BaseGenerator(object):
    fields = {}
    options = None
    height = None
    width = None
    bleed = None
    unit = None
    rgb_to_cmyk = None

    def __init__(self, options):
        self.options = options
        self.height = options.height
        self.width = options.width
        self.bleed = options.bleed
        if options.unit not in common.UNITS:
            raise KeyError(options.unit)
        self.unit = options.unit

    @staticmethod
    def extra_options(parser):
        return None

    def collect_information(self):
        pass

    def generate_front(self):
        raise NotImplementedError()

    def generate_back(self):
        raise NotImplementedError()


__all__ = ('fedora',)
