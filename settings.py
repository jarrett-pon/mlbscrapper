MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_HOST = ''

try:
   from dev_settings import *
except ImportError:
   pass
