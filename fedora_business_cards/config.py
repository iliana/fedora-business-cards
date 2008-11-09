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
Controls the locations of configuration files, and imports configurations from
all those files in a specific order.
"""

from iniparse import ConfigParser
import os


def available_templates(config):
    """
    Takes the main ConfigParser as the argument.
    """
    templates_dir = config.get('location', 'templates')
    templates = ConfigParser()
    templates.read(templates_dir+"/templates.ini")
    filelist = os.listdir(templates_dir)
    for section in templates.sections():
        if templates.options(section) == ["humandesc", "front", "back",
                                          "type"]:
            if templates.get(section, "front") in filelist:
                if templates.get(section, "back") in filelist:
                    # only SVG templates are currently supported
                    if templates.get(section, "type") == "svg":
                        continue
        elif templates.options(section) == ["humandesc", "front", "type"]:
            if templates.get(section, "front") in filelist:
                # only SVG templates are currently supported
                if templates.get(section, "type") == "svg":
                    continue
        templates.remove_section(section)
    return templates


# locations, in reverse-order of priority
LOCATIONS = ['/'.join(__file__.split('/')[:-1]+['config.ini']),
             'config.ini', # in current working directory
             '/usr/share/fedora-business-cards/config.ini',
             '/etc/fedora-business-cards.ini',
             os.getenv('HOME')+'/.fedora-business-cards.ini']

parser = ConfigParser()
for i in LOCATIONS:
    parser.read(i)


__all__ = ('parser', 'available_templates')
