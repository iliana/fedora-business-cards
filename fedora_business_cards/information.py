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
Assembles information about a person from FAS.
"""

from fedora.client.fas2 import AccountSystem

from fedora_business_cards import __version__


def get_information(loginname, password, username=None):
    """
    Fetches information about a certain contributor from FAS.
      loginname: username to *login with* on FAS
      password: password to loginname
      username: username to get information on (default: same as loginname)
    """
    if username == None:
        username = loginname
    fas = AccountSystem(username=loginname, password=password,
                        useragent='fedora-business-cards/%s' % __version__)
    userinfo = fas.person_by_username(username)
    infodict = {}
    infodict['name'] = userinfo["human_name"]
    infodict['title'] = "Fedora Project Contributor"
    infodict['email'] = "%s@fedoraproject.org" % username
    infodict['url'] = 'fedoraproject.org'
    infodict['gpgid'] = userinfo['gpg_keyid']
    infodict['irc'] = userinfo['ircnick']
    return infodict
