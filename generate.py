###
# generate.py - for rendering Fedora contributor business cards
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
Use this script to render yourself business cards in popular shapes, sizes, and
formats. Only run it from within the git repository, since it has some
templates that this script requires.

You'll need mgopen-fonts, python-fedora, and pygpgme from yum.
"""

from fedora.accounts.fas2 import AccountSystem
from optparse import OptionParser
import gpgme
import re
import subprocess
from getpass import getpass
from xml.dom import minidom

VALID_INFO = ['email', 'phone', 'irc', 'url', 'gpgid', 'gpgfingerprint',
              'blank']


class BusinessCardError(ValueError):
    """
    Possible problems:
        info>6
        notinfo (1 arg)
        pgpfp (1 arg)
        noirc (1 arg)
        nogpg (1 arg)
    """

    def __init__(self, problem, args=[]):
        ValueError.__init__(self)
        self.problem = problem
        self.args = args

    def __str__(self):
        if self.problem == "info>6":
            return "--info count can't be greater than 6"
        if self.problem == "notinfo":
            return "%s not valid for --info" % self.args[0]
        if self.problem == "pgpfp":
            return "Couldn't get PGP fingerprint for key %s" % self.args[0]
        if self.problem == "noirc":
            return "No IRC nick for %s, use override" % self.args[0]
        if self.problem == "nogpg":
            return "No GPG key ID for %s, use override" % self.args[0]


def get_gpg_fingerprint(keyid):
    """
    Gets the GPG fingerprint from the key ID.
    """
    ctx = gpgme.Context()
    try:
        key = ctx.get_key(keyid)
    except gpgme.GpgmeError:
        # fetch keys from subkeys.pgp.net
        subprocess.Popen('gpg --keyserver subkeys.pgp.net --recv-key %s' %
                         keyid, shell=True)
        try:
            key = ctx.get_key(keyid)
        except gpgme.GpgmeError:
            raise BusinessCardError('pgpfp', keyid)
    fpr = key.subkeys[0].fpr
    return ' '.join([i for i in re.split('([A-Z0-9]{4})', fpr) if i])


def find_node(doc_node, tag_name, attribute_name, attribute_value):
    """
    Finds a node based on tag name, attribute name, and attribute value.

    Thanks, mizmo!
    """
    # thanks, mizmo
    elements = doc_node.getElementsByTagName(tag_name)
    for element in elements:
        if element.hasAttribute(attribute_name):
            if element.getAttribute(attribute_name) == attribute_value:
                return element


def gen_front(name, title, lines, outfile):
    """
    Generates the front side of the business card based off of the given
    name, title, and 6 lines in a list. Also requires an outfile variable.
    """
    dom = minidom.parse('front-template.svg')
    namenode = find_node(dom, 'text', 'id', 'fullname')
    namenode.appendChild(dom.createTextNode(name))
    titlenode = find_node(dom, 'text', 'id', 'title')
    titlenode.appendChild(dom.createTextNode(title))
    for i in range(6):
        node = find_node(dom, 'tspan', 'id', 'line%d' % (i+1))
        node.appendChild(dom.createTextNode(lines[i]))
    out = file(outfile, "w")
    out.write(dom.toxml())
    out.close()


def main():
    # set up parser
    parser = OptionParser()
    parser.add_option("-i", "--info", dest="info",
                      default="email,phone,irc,url,blank,gpgid", help="Order"+\
                      " of information on card. Valid options are email, "+\
                      "phone, irc, url, gpgid, gpgfingerprint, and blank.")
    overrides = ['username', 'name', 'title'] + VALID_INFO
    for i in overrides:
        if i != "blank":
            parser.add_option("--override-%s" % i, dest="override%s" % i,
                              default="", help="Override for %s" % i)
    # parse
    options = parser.parse_args()[0]
    # check --info
    info = options.info.split(',')
    if len(info) > 6:
        raise BusinessCardError('info>6')
    for i in info:
        if i not in VALID_INFO:
            raise BusinessCardError('notinfo', [i])
    # FAS login
    print "Login to FAS"
    print "Username:",
    username = raw_input()
    password = getpass()
    fas = AccountSystem(username=username, password=password)
    # and go!
    if options.overrideusername != "":
        username = options.overrideusername
    overrides = {'email': options.overrideemail,
                 'phone': options.overridephone,
                 'blank': '',
                 'name': options.overridename,
                 'title': options.overridetitle,
                 'irc': options.overrideirc,
                 'url': options.overrideurl,
                 'gpgid': options.overridegpgid,
                 'gpgfingerprint': options.overridegpgfingerprint}
    userinfo = fas.person_by_username(username)
    infodict = {}
    infodict['name'] = userinfo["human_name"]
    infodict['title'] = "Fedora Project Contributor"
    infodict['email'] = "%s@fedoraproject.org" % username
    infodict['phone'] = "(919) 424-0063 x 5%s" % userinfo['id']
    infodict['url'] = 'fedoraproject.org'
    infodict['blank'] = ''
    if not options.overrideirc:
        if 'irc' in options.info:
            if userinfo['ircnick'] == "":
                raise BusinessCardError('noirc', username)
            else:
                infodict['irc'] = '%s on irc.freenode.net' % \
                        userinfo['ircnick']
    if not options.overridegpgid:
        if 'gpg' in options.info:
            if userinfo['gpg_keyid'] == "":
                raise BusinessCardError('nogpg', username)
            else:
                infodict['gpgid'] = 'GPG key ID: %s' % userinfo['gpg_keyid']
                infodict['gpgfingerprint'] = get_gpg_fingerprint(
                    userinfo['gpg_keyid'])
    else:
        if not options.overridegpgfingerprint:
            infodict['gpgfingerprint'] = get_gpg_fingerprint(
                options.overridegpgid)
    lines = []
    for i in info:
        lines.append(overrides[i] or infodict[i])
    gen_front(overrides['name'] or infodict['name'], overrides['title'] or
              infodict['title'], lines, 'out.svg')

if __name__ == "__main__":
    main()
