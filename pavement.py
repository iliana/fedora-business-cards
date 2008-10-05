from glob import glob
import iniparse
import os
import paver.path

options(
    setup=Bunch(
        name="fedora-business-cards",
        version="0.2",
        description="A generator for Fedora contributor business cards",
        packages=["fedora_business_cards"],
        author="Ian Weller",
        author_email="ianweller@gmail.com",
        license="GPLv2+",
        url="https://fedoraproject.org/wiki/Business_cards"
    ),
    install_templates=Bunch(
        templates=glob("templates/*"),
        data_dir="/usr/share/fedora-business-cards"
    )
)


@task
@cmdopts([('root=', 'r', 'install everything relative to this alternative root'
           ' directory')])
def install_templates():
    """install necessary templates for generator"""
    options.order("install_templates", add_rest=True)
    try:
        root_dir = options.root
    except AttributeError:
        root_dir = ''
    parser = iniparse.ConfigParser()
    parser.read("config.ini")
    templates_dir = options.data_dir + "/templates"
    parser.set("location", "templates", templates_dir)
    data_dir = paver.path.path(root_dir + options.data_dir)
    if not os.path.exists(data_dir):
        data_dir.makedirs(0755)
    parser.write(file(root_dir + options.data_dir + "/config.ini", "w"))
    for template_file in options.templates:
        templates_dir = paver.path.path(root_dir + options.data_dir +
                                        "/templates")
        if not os.path.exists(templates_dir):
            templates_dir.makedirs(0755)
        command = "install -p %s %s" % (template_file, templates_dir)
        dry(command, paver.runtime.sh, [command])
