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
Frontend to the business card generator. Theoretically expandable to GUI and
whatnot, but for now just has a command-line interface.
"""

from optparse import OptionParser
import os
import sys
from getpass import getpass

# local imports
import config
import information


def cmdline_card_line(data):
    return "| %s%s |" % (data, ' '*(59-len(data)))


def cmdline():
    """
    Command-line interface to business card generator. Takes no arguments; uses
    optparser.OptionParser instead.
    """
    # setup option parser
    parser = OptionParser()
    parser.usage = "%prog [options] [outfile]"
    parser.add_option("-d", "--dpi", dest="dpi", default=300, type="int",
                      help="DPI of exported file")
    parser.add_option("-t", "--template", dest="template",
                      default="northamerica", help="Name of template to use, "+\
                      "run with --list-templates to see a list")
    parser.add_option("--list-templates", action="store_true", default=False,
                      dest="listtemplates", help="List available templates")
    parser.add_option("-u", "--username", dest="username", default="",
                      help="If set, use a different name than the one logged"+\
                      " in with to fill out business card information")
    parser.add_option("--pdf", dest="output", default="png", const="pdf",
                      action="store_const", help="Export as PDF")
    parser.add_option("--png", dest="output", default="png", const="png",
                      action="store_const", help="Export as PNG (default)")
    options = parser.parse_args()[0]
    # check what templates are available
    templates_dir = config.parser.get('location', 'templates')
    contents = os.listdir(templates_dir)
    checked_once = []
    available_templates = []
    for i in contents:
        if i[-4:] == '.svg':
            if i[:6] == 'front-':
                name = i[6:-4]
            elif i[:5] == 'back-':
                name = i[5:-4]
            else:
                continue
            if name in checked_once:
                available_templates.append(name)
            else:
                checked_once.append(name)
    if options.listtemplates:
        print "Available templates:"
        for i in available_templates:
            print "  %s" % i
        sys.exit(0)
    if options.template not in available_templates:
        print "%s not an available template" % options.template
        sys.exit(1)
    # ask for FAS login
    print "Login to FAS:"
    print "Username:",
    username = raw_input()
    password = getpass()
    if options.username == "":
        options.username = username
    infodict = information.get_information(username, password, options.username)
    # setup default content
    name = infodict['name']
    title = infodict['title']
    if infodict['gpgid'] == None:
        gpg = ''
    else:
        gpg = "GPG key ID: %s" % infodict['gpgid']
    if infodict['irc'] == None:
        lines = [infodict['email'],
                 infodict['phone'],
                 infodict['url'],
                 '',
                 gpg,
                 '']
    else:
        lines = [infodict['email'],
                 infodict['phone'],
                 infodict['irc']+" on irc.freenode.net",
                 infodict['url'],
                 '',
                 "GPG key ID: "+infodict['gpgid']]
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
