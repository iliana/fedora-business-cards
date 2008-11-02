from glob import glob
import iniparse
import os
import paver.path

options(
    setup=Bunch(
        name="fedora-business-cards",
        version="0.2.1",
        description="A generator for Fedora contributor business cards",
        packages=["fedora_business_cards"],
        author="Ian Weller",
        author_email="ianweller@gmail.com",
        license="GPLv2+",
        url="https://fedoraproject.org/wiki/Business_cards"
    ),
    install_data=Bunch(
        templates=glob("templates/*"),
        ui=glob("ui/*"),
        data_dir="/usr/share/fedora-business-cards"
    ),
    install_executable=Bunch(
        bin_dir="/usr/bin"
    )
)


@task
@cmdopts([('root=', None, 'install everything relative to this alternative root'
           ' directory')])
def install_data():
    """install necessary data for generator"""
    options.order("install_data", add_rest=True)
    try:
        root_dir = options.root
    except AttributeError:
        root_dir = ''
    parser = iniparse.ConfigParser()
    parser.read("config.ini")
    templates_dir = options.data_dir + "/templates"
    parser.set("location", "templates", templates_dir)
    ui_dir = options.data_dir + "/ui"
    parser.set("location", "ui", ui_dir)
    data_dir = paver.path.path(root_dir + options.data_dir)
    if not os.path.exists(data_dir):
        data_dir.makedirs(0755)
    parser.write(file(root_dir + options.data_dir + "/config.ini", "w"))
    for template_file in options.templates:
        templates_dir = paver.path.path(root_dir + options.data_dir +
                                        "/templates")
        if not os.path.exists(templates_dir):
            templates_dir.makedirs(0755)
        command = "install -cpm 644 %s %s" % (template_file, templates_dir)
        dry(command, paver.runtime.sh, [command])
    for ui_file in options.ui:
        ui_dir = paver.path.path(root_dir + options.data_dir + "/ui")
        if not os.path.exists(ui_dir):
            templates_dir.makedirs(0755)
        command = "install -cpm 644 %s %s" % (ui_file, ui_dir)
        dry(command, paver.runtime.sh, [command])


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
    dry(command, paver.runtime.sh, [command])
