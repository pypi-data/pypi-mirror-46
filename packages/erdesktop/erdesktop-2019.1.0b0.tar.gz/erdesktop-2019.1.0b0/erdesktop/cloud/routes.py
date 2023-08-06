_PORT = 8000
_IP = 'localhost'
_PROTOCOL = 'https'

# _HOST = '{}:{}'.format(_IP, _PORT)
_HOST = 'event-reminder-cloud.herokuapp.com'

_BASE = '{}://{}/api/v1'.format(_PROTOCOL, _HOST)


AUTH_LOGIN = '{}/login'.format(_BASE)
AUTH_LOGOUT = '{}/logout'.format(_BASE)


_ACCOUNTS = '{}/accounts'.format(_BASE)

ACCOUNT_EDIT = '{}/edit'.format(_ACCOUNTS)
ACCOUNT_DETAILS = '{}/user'.format(_ACCOUNTS)
ACCOUNT_CREATE = '{}/create'.format(_ACCOUNTS)
ACCOUNT_DELETE = '{}/delete'.format(_ACCOUNTS)
ACCOUNT_SEND_TOKEN = '{}/send/confirmation/code'.format(_ACCOUNTS)
ACCOUNT_PASSWORD_RESET = '{}/password/reset'.format(_ACCOUNTS)


BACKUPS = '{}/backups/'.format(_BASE)

BACKUP_CREATE = '{}create'.format(BACKUPS)
BACKUP_DELETE = '{}delete/'.format(BACKUPS)
BACKUP_DETAILS = '{}details/'.format(BACKUPS)
