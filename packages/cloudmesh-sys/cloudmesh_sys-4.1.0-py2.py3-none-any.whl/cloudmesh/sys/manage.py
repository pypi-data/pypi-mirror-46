"""
Managing the cmd5 system installation and package distribution
"""
from __future__ import print_function

import os
import shutil
from distutils.dir_util import copy_tree
from pprint import pprint

from cloudmesh.common.util import banner
from cloudmesh.common.util import writefile
from cloudmesh.common.console import Console


class Command(object):
    """
    Class to generate cmd5 command templates
    """

    @classmethod
    def generate(cls, name):
        """
        Generate a command template with the given name
        :param name: the name of the command
        :return: 
        """

        data = {
            "command": name,
            "package": "cloudmesh-{}".format(name),
            "Command": name.capitalize()
        }

        pprint(data)

        # os.system("rm -rf  cloudmesh-gregor")
        # noinspection PyUnusedLocal,PyBroadException
        try:
            os.system("git clone https://github.com/cloudmesh/cloudmesh-bar")
        except Exception as e:
            pass

        os.system("cd cloudmesh-bar; make clean")
        copy_tree("cloudmesh-bar", "{package}".format(**data))
        shutil.rmtree("{package}/.git".format(**data))
        os.system('sed -ie "s/bar/{command}/g" {package}/setup.py'.format(**data))
        os.rename("{package}/cloudmesh/bar/command/bar.py".format(**data),
                  "{package}/cloudmesh/bar/command/{command}.py".format(**data))
        os.rename("{package}/cloudmesh/bar".format(**data),
                  "{package}/cloudmesh/{command}".format(**data))
        shutil.rmtree('{package}/cloudmesh/foo'.format(**data))
        os.system('sed -ie "s/bar/{command}/g" {package}/cloudmesh/{command}/command/{command}.py'.format(**data))
        os.system('sed -ie "s/Bar/{Command}/g" {package}/cloudmesh/{command}/command/{command}.py'.format(**data))
        os.system('sed -ie "s/bar/{command}/g" {package}/Makefile'.format(**data))        
        os.system("rm -rf {package}/Makefilee")
        os.system("rm -rf {package}/setup.pye")

class Git(object):
    """
    Git management for the preparation to upload the code to pypi
    """

    pypis = ["cloudmesh-common",
             "cloudmesh-cmd5",
             "cloudmesh-sys",
             "cloudmesh-comet",
             "cloudmesh-openapi"]
    commits = pypis + ["cloudmesh-bar"]
    # , "cloudmesh-rest"]
    # "cloudmesh-robot"]

    @classmethod
    def upload(cls):
        """
        upload the code to pypi
        :return: 
        """

        banner("CREATE DIST")
        for p in cls.pypis:
            try:
                os.system("cd {}; make dist".format(p))
            except Exception as e:
                Console.error("can not create dist" + p)
                print(e)

        banner("UPLOAD TO PYPI")
        for p in cls.pypis:
            try:
                os.system("cd {}; make upload".format(p))
            except Exception as e:
                Console.error("can upload" + p)
                print(e)

    @classmethod
    def commit(cls, msg):
        """
        commit the current code to git
        :param msg: 
        :return: 
        """

        banner("COMMIT " + msg)
        for p in cls.commits:
            banner("repo " + p)
            os.system('cd {}; git commit -a -m "{}"'.format(p, msg))
            os.system('cd {}; git push'.format(p))


class Version(object):
    """
    set the version number of all base packages
    """

    @classmethod
    def set(cls, version):
        """
        set the version number
        :param version: the version as text string
        :return: 
        """
        for repo in Git.commits:
            print(repo, "->", version)
            writefile(os.path.join(repo, "VERSION"), version)
