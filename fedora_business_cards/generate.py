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
Generates both sides of the business card.
"""

from xml.dom import minidom


def find_node(doc_node, tag_name, attribute_name, attribute_value):
    """
    Gets a specific node from a DOM tree with a certain tag name, attribute
    name, and attribute value.
    """
    # thanks, mizmo
    elements = doc_node.getElementsByTagName(tag_name)
    for element in elements:
        if element.hasAttribute(attribute_name):
            if element.getAttribute(attribute_name) == attribute_value:
                return element


def gen_front(name, title, lines, template_loc):
    """
    Generates the front of the business card.
    """
    dom = minidom.parse(template_loc)
    namenode = find_node(dom, 'text', 'id', 'fullname')
    namenode.appendChild(dom.createTextNode(name))
    titlenode = find_node(dom, 'text', 'id', 'title')
    titlenode.appendChild(dom.createTextNode(title))
    for i in range(6):
        node = find_node(dom, 'tspan', 'id', 'line%d' % (i+1))
        node.appendChild(dom.createTextNode(lines[i]))
    return dom.toxml()


def gen_back(template_loc):
    """
    Generates the back of the business card.
    """
    dom = minidom.parse(template_loc)
    return dom.toxml()
