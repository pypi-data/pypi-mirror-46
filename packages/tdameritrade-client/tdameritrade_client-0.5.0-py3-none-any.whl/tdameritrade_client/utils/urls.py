import os
import platform
from environs import Env

env = Env()

# Package urls
PACKAGE_BASE = os.path.dirname(os.path.dirname(__file__))
if platform.system() == 'Windows':
    DEFAULT_TOKEN_DIR = os.path.join(env('HOMEDRIVE'), env('HOMEPATH'),
                                      '.tda_certs')
elif platform.system() == 'Linux' or platform.system() == 'Darwin':
    DEFAULT_TOKEN_DIR = os.path.join(env('HOME'), '.tda_certs')

else:
    raise NotImplementedError(f'Your OS ({platform.system()}) is not supported by this package.')

# TDAmeritrade base urls
AUTH_URL = 'https://auth.tdameritrade.com/auth'
BASE_URL = 'https://api.tdameritrade.com'

# Resource URLs
TOKEN_URL = '/v1/oauth2/token'
ACCOUNT_URL = '/v1/accounts/'
INSTRUMENTS_URL = '/v1/instruments/'
QUOTES_URL = '/v1/marketdata/quotes'
PRICE_HISTORY_URL = '/v1/marketdata/'
MOVERS_URL = '/v1/marketdata/'
HOURS_URL = f'{MOVERS_URL}hours'

# Params
AUTH_PARAMS = '?response_type=code&redirect_uri='
APIKEY_PARAM = '?apikey='
