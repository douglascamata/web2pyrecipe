# -*- coding: utf-8 -*-

from subprocess import call
from os import listdir, mkdir, chmod, walk, remove, rmdir, remove
from os.path import join, abspath, dirname, exists
from zipfile import ZipFile
from tarfile import TarFile
from urllib2 import urlopen

"""
A recipe for installing the lastest web2py framework version and all the apps in
the 'appdir' options. It defines the 'default' option as the default web2py's app.
"""

FOLDER = abspath(dirname(__file__))

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        """Installer"""
        apps_dir = self.options.get('appdir')
        default_app = self.options.get('default') or 'welcome'
        default_app = default_app.replace('.','_')
        password = self.options.get('password') or 'web2py'
        pid_file = self.options.get('pidfile') or 'pid.txt'

        if exists('web2py_src.zip'):
            remove('web2py_src.zip')

        self._download('http://www.web2py.com/examples/static/web2py_src.zip', 'web2py_src.zip')

        self._unzip('web2py_src.zip')

        remove('web2py_src.zip')

        self._install_apps(apps_dir)

        self._set_default_app(default_app)

        self._create_web2py_bin_script(pid_file, password)

        # XXX Implement recipe functionality here
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return ('webpy',)
    update = install

    def _download(self, url, destination):
        web_file = urlopen(url).read()
        local_file = open(destination, 'wb')
        local_file.write(web_file)
        local_file.close()

    def _unzip(self, archive):
        zip_file = ZipFile(archive, 'r')
        zip_file.extractall()

    def _install_apps(self, apps_dir):
        file_list = listdir(apps_dir)
        for file_ in file_list:
            filename = join(self.options.get('appdir'), file_)
            new_dir = file_[:-4].replace('.','_')
            if new_dir in listdir(join('web2py','applications')):
                rmdir(new_dir)
            mkdir(join('web2py','applications', new_dir))
            dest = join('web2py', 'applications', new_dir)
            self._untar(filename, dest)

    def _untar(self, archive, destination):
        tar = TarFile.open(archive)
        tar.extractall(path=destination)

    def _set_default_app(self, default_app):
        routes = open(join('web2py','routes.py'),'w+')
        routes.write("default_application = '%s'\n" % default_app + \
                     "default_controller = 'default'\n" + \
                     "default_function = 'index'\n"
                     )
        routes.close()

    def _create_web2py_bin_script(self, pid_file, password):
        self._web2py_script_template(pid_file, password)
        self._make_executable(join('bin','web2py'))

    def _web2py_script_template(self, pid_file, password):
        script = "#!/bin/bash\n" + \
                 "PYTHON=python\n" + \
                 "\n" + \
                 "start() {\n" + \
                 "  ${PYTHON} %s -a %s -d %s &\n" % (join('web2py','web2py.py'), \
                                         password, \
                                         pid_file) + \
                 "}\n" + \
                 "\n" + \
                 "stop() {\n" + \
                 "  kill `cat %s`\n" % join('web2py', pid_file) + \
                 "}\n" + \
                 "\n" + \
                 'case "$1" in\n' + \
                 "  start)\n" + \
                 "    start;;\n" + \
                 "  stop)\n" + \
                 "    stop;;\n" + \
                 "  restart)\n" + \
                 "    start\n" + \
                 "    stop;;\n" + \
                 "  *)\n" + \
                 '  echo "Usage: web2py {start|stop|restart}"\n' + \
                 "  exit 1;;\n" + \
                 "esac\n" + \
                 "exit"

        open(join('bin','web2py'),'w+').write(script)

    def _make_executable(self, file_):
        chmod(file_, 0777)

#    def update(self):
#        """Updater"""
#        pass

