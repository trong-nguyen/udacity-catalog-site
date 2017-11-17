#!/usr/bin/python
activate_this = '/home/catalog/catalog-app/init/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/catalog")

from views import app as application
application.secret_key = '03uklsjadf09'