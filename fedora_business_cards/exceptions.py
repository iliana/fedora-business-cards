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
Miscellaneous exceptions used specifically for this module.
"""


class NoGPGKeyError(StandardError):
    """
    Exception used when the GPG key for a specific ID isn't available on the
    system; usually used when we can't derive the fingerprint from the ID
    because we don't have the key.
    """

    def __init__(self, keyid):
        StandardError.__init__(self)
        self.keyid = keyid

    def __str__(self):
        return self.keyid
