# -*- coding: utf-8 -*-
#
# This file is part of django-xmpp-account (https://account.jabber.at/doc).
#
# django-xmpp-account is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# django-xmpp-account is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See
# the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with django-xmpp-account.
# If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import logging
import os
import sys
logging.basicConfig(level=logging.DEBUG)

from six.moves import configparser

from fabric.api import local
from fabric.colors import red
from fabric.tasks import Task

from fabric_webbuilders import BuildBootstrapTask
from fabric_webbuilders import BuildJqueryTask
from fabric_webbuilders import MinifyCSSTask
from fabric_webbuilders import MinifyJSTask

node_path = os.path.abspath('node_modules')
if os.path.exists(node_path):
    if node_path not in os.environ['PATH']:
        os.environ['PATH'] = '%s/.bin:%s' % (node_path, os.environ['PATH'])

build_jquery = BuildJqueryTask(
    excludes='-deprecated,-dimensions',
    dest_dir='core/static/lib/jquery/'
)
build_bootstrap = BuildBootstrapTask(
    config='core/static/bootstrap-config.json',
    dest_dir='core/static/lib/bootstrap/'
)
minify_css = MinifyCSSTask(files=[
    'core/static/lib/bootstrap/css/bootstrap.min.css',
    'core/static/lib/font-awesome/css/font-awesome.min.css',
    'core/static/lib/shariff/shariff.min.css',
    'core/static/css/base.css',
], dest='core/static/account.min.css')
minify_js = MinifyJSTask(files=[
    'core/static/lib/jquery/jquery.min.js',
    'core/static/js/base.js',
], dest='core/static/account.min.js')


config = configparser.ConfigParser({
    'remote': 'origin',
    'branch': 'master',
})
config.read('fab.conf')


class BuildTask(Task):
    def run(self):
        minify_js.run()
        minify_css.run()


class DeployTask(Task):
    def run(self, section='DEFAULT', group='xmpp-account'):
        # get options that have a default:
        remote = config.get(section, 'remote')
        branch = config.get(section, 'branch')

        # these options are required for deployment
        try:
            path = config.get(section, 'path')
        except configparser.NoOptionError:
            print(red('Please configure option "%s" in section "%s" in fab.conf' % ('path', section)))
            sys.exit(1)

        try:
            host = config.get('DEFAULT', 'host')
        except configparser.NoOptionError:
            print(red('Please configure option "%s" in section "%s" in fab.conf' % ('host', section)))
            sys.exit(1)

        local('git push %s %s' % (remote, branch))
        ssh = lambda cmd: local('ssh %s sudo sg %s -c \'"cd %s && %s"\'' % (host, group, path, cmd))
        local('ssh %s sudo chgrp -R %s %s' % (host, group, path))
        ssh("git fetch %s" % remote)
        ssh("git pull %s %s" % (remote, branch))
        ssh("../bin/pip install -r requirements.txt")
        ssh("../bin/python manage.py update")
        ssh("touch /etc/uwsgi-emperor/vassals/xmpp-account.ini")


deploy = DeployTask()
build = BuildTask()
