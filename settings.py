"""My sql settings and config."""
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_HOST = ''

try:
    from dev_settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST
except ImportError:
    pass
