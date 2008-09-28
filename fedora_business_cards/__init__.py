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
The Fedora business cards generator will generate business cards for Fedora
contributors. It connects to FAS to retrieve user information and lays it out on
a SVG, then exports that to a PDF and PNG. Different templates are/will be
available for different business card sizes, or different requirements by
different companies.
"""

__all__ = ('config', 'exceptions', 'export', 'frontend', 'generate',
           'information')
