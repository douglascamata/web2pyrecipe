Supported options
=================

appdir
    The directory where the compressed web2py application should be ...

default
    The default app of the web2py server ...

password
    The password for web2py adminsitrative app ...

Testing now::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test1
    ...
    ... [test1]
    ... recipe = web2pyrecipe
    ... password = 123
    ... pidfile = pid.txt
    ... appdir = %(dir)s
    ... default = web2py.app.chat
    ... option2 = %(bar)s
    ... """ % { 'dir' : 'web2pyapps', 'bar' : 'value2'})

    >>> mkdir('web2pyapps')
    ...

Downloading example app::

    >>> system('wget http://www.web2py.com/appliances/default/download/app.source.aa6d3615911c89b6.7765623270792e6170702e636861742e773270.w2p -O web2pyapps/web2py.app.chat.w2p -q')
    ''

Running the buildout gives us::

    >>> print 'start', system(buildout)
    start...
    Installing test1.
    Unused options for test1: 'option2'.
    <BLANKLINE>
    ...
    <BLANKLINE>

Checking the root directory structure::

    >>> ls('.')
     -  .installed.cfg
     d  bin
     -  buildout.cfg
     d  develop-eggs
     d  eggs
     d  parts
     d  web2py
     d  web2pyapps

Checking the test app for w2p::

    >>> ls('web2pyapps')
     - web2py.app.chat.w2p

Checking if web2py is extracted correctly::

    >>> ls('web2py')
    -  ABOUT
    -  LICENSE
    -  Makefile
    -  NEWINSTALL
    -  README
    -  VERSION
    -  __init__.py
    -  anyserver.py
    -  app.yaml
    -  appengine_config.py
    d  applications
    -  cgihandler.py
    -  epydoc.conf
    -  epydoc.css
    -  fcgihandler.py
    -  gaehandler.py
    d  gluon
    -  logging.example.conf
    -  modpythonhandler.py
    -  options_std.py
    -  queue.yaml
    -  router.example.py
    -  routes.example.py
    -  routes.py
    -  scgihandler.py
    d  scripts
    -  setup_app.py
    -  setup_exe.py
    -  splashlogo.gif
    -  web2py.py
    -  wsgihandler.py

Checking if the test app is correctly extracted at web2py's application directory::

    >>> ls(join('web2py','applications'))
    -  __init__.py
    d  admin
    d  examples
    d  web2py_app_chat
    d  welcome

    >>> cat(join('web2py','routes.py'))
    default_application = 'web2py_app_chat'
    default_controller = 'default'
    default_function = 'index'

Checking if the script for running the web2py server is created on 'bin' directory::

    >>> ls('bin')
    - buildout
    - web2py

So, let's check the content of 'web2py' script::

    >>> cat(join('bin','web2py'))
    #!/bin/bash
    PYTHON=python
    <BLANKLINE>
    start() {
        ${PYTHON} web2py/web2py.py -a 123 -d pid.txt &
    }
    <BLANKLINE>
    stop() {
        kill `cat web2py/pid.txt`
    }
    <BLANKLINE>
    case "$1" in
      start)
        start;;
      stop)
        stop;;
      restart)
        start
        stop;;
      *)
      echo "Usage: web2py {start|stop|restart}"
      exit 1;;
    esac
    exit

