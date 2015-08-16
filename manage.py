__author__ = 'arshad'

import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask.ext.script import Manager, Server
from core_components.webapp import app


manager = Manager(app)

manager.add_command("runserver", Server(use_debugger = True, use_reloader = True, host = '0.0.0.0', port=9900))

if __name__ == '__main__':
    manager.run()

