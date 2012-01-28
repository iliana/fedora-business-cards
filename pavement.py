import os
import paver.path
from paver.easy import *
import paver.setuputils

paver.setuputils.install_distutils_tasks()

options(
    setup=Bunch(
        name="fedora-business-cards",
        version="0.3",
        description="A generator for Fedora contributor business cards",
        packages=["fedora_business_cards",
                  "fedora_business_cards.frontend",
                  "fedora_business_cards.generators"],
        author="Ian Weller",
        author_email="iweller@redhat.com",
        license="GPLv2+",
        url="https://fedoraproject.org/wiki/Business_cards"
    ),
    install_executable=Bunch(
        bin_dir="/usr/bin"
    )
)

@task
@cmdopts([('root=', None, 'install everything relative to this alternative root'
           ' directory')])
def install_executable():
    """install executable for generator"""
    options.order("install_executable", add_rest=True)
    try:
        root_dir = options.root
    except AttributeError:
        root_dir = ''
    bin_dir = paver.path.path(root_dir + options.bin_dir)
    if not os.path.exists(bin_dir):
        bin_dir.makedirs(0755)
    command = "install -cpm 755 %s %s" % ("fedora-business-cards", bin_dir)
    dry(command, sh, command)
