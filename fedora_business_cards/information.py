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
Assembles information about a person from FAS and their GPG key.
"""

from fedora.client.fas2 import AccountSystem
import gpgme
import re

# local imports
import exceptions


def get_gpg_fingerprint(keyid):
    """
    Gets the GPG fingerprint from the key ID.
    """
    ctx = gpgme.Context()
    try:
        key = ctx.get_key(keyid)
    except:
        raise exceptions.NoGPGKeyError(keyid)
    fpr = key.subkeys[0].fpr
    return ' '.join([i for i in re.split('([A-Z0-9]{4})', fpr) if i])


def get_information(loginname, password, username=None):
    """
    Fetches information about a certain contributor from FAS.
      loginname: username to *login with* on FAS
      password: password to loginname
      username: username to get information on (default: same as loginname)
    """
    if username == None:
        username = loginname
    fas = AccountSystem(username=loginname, password=password)
    userinfo = fas.person_by_username(username)
    infodict = {}
    infodict['name'] = userinfo["human_name"]
    infodict['title'] = "Fedora Project Contributor"
    infodict['email'] = "%s@fedoraproject.org" % username
    infodict['phone'] = "(919) 424-0063 x 5%s" % userinfo['id']
    infodict['url'] = 'fedoraproject.org'
    infodict['gpgid'] = userinfo['gpg_keyid']
    return infodict
