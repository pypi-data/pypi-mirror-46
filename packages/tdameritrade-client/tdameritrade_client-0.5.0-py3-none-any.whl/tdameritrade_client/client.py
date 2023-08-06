import os
from datetime import datetime
from typing import Dict, Type, TypeVar

import requests

from tdameritrade_client.auth import TDAuthenticator
from tdameritrade_client.utils import urls
from tdameritrade_client.utils.tools import check_auth, validate_price_history_args, process_price_history

# For typehint of the classmethod
T = TypeVar('T', bound='TrivialClass')


class TDClient(object):
    """
    Python client for the TDAmeritrade API.

    """
    def __init__(self, acct_number: int, oauth_user_id: str, redirect_uri: str, token_path: str = None):
        """
        Constructor for the TDClient object.

        Args:
            acct_number: The account number to authenticate against.
            oauth_user_id: The oauth user ID of the TD developer app this client is authenticating against.
            redirect_uri: The redirect URI where TDAmeritrade will send an auth token.
            token_path: Path where the auth-token.json should be written. Defaults to
                $HOME/.tda_certs/ACCT_NUMBER/auth-token.json.

        """
        self._acct_number = acct_number
        self._redirect_uri = redirect_uri
        self._oauth_user_id = oauth_user_id.upper()
        self._token_path = os.path.join(urls.DEFAULT_TOKEN_DIR,
                                        str(acct_number),
                                        'auth-token.json') if token_path is None else token_path
        self.token = None

        ip = redirect_uri.split('/')[-1]
        host, port = ip.split(':')

        self._authenticator = TDAuthenticator(host, int(port), self._oauth_user_id, self._token_path)

    @classmethod
    def from_dict(cls: Type[T], acct_info: Dict) -> T:
        """
        Create an instance of this class from a dictionary.

        Args:
            acct_info: A dictionary of init parameters

        Returns:
            An instance of this class

        """
        return cls(**acct_info)

    def run_auth(self) -> None:
        """
        Runs the authentication flow. See the TDAuthenticator class for details.
        """
        self.token = self._authenticator.authenticate()

    @check_auth
    def get_period_price_history(self, symbol: str, frequency_type: str, frequency: int, period_type: str = 'day',
                                 period: int = None, need_extended_hours_data: bool = True) -> Dict:
        """Get price history for a symbol by period

        Provide a ticker symbol, a frequency/frequencyType and a period/periodType to receive price history
        candles given at the requested frequency and within the requested period/date range.
        Responses are a dict with a "candles" key whose value is a list of objects each containing
        "open", "close", "low", "high", "volume", and "datetime" key-value pairs.

        Args:
            symbol: Ticker symbol to search for.
            frequency_type: The type of frequency with which a new candle is formed. Must be
                either 'minute', 'daily', 'weekly', or 'monthly'.
            frequency: Frequency with which to return candles.
            period_type: The type of period-data to return. Must be either 'day', 'month',
                'year', or 'ytd'. Default: 'day'.
            period: The length of periodType over which to receive price history.
            need_extended_hours_data: False to only return regular market hours data. Default: True.

        Returns:
            Price history for the ticker symbol as set of candles.

        Raises:
            ValueError: If passed arguments are invalid.

        """
        params = validate_price_history_args(symbol=symbol, frequency_type=frequency_type, frequency=frequency,
                                             period_type=period_type, period=period,
                                             need_extended_hours_data=need_extended_hours_data)
        reply = requests.get(self._get_url('get_price_history', params=params),
                             headers=self._build_header())
        return process_price_history(reply.json())

    @check_auth
    def get_dated_price_history(self, symbol: str, start_date: datetime, end_date: datetime,
                                need_extended_hours_data: bool = True) -> Dict:
        """Get price history for a symbol by date

        Provide a ticker symbol and a start/endDate to receive price history candles given at the
        the frequency of one candle per minute. Responses are a dict with a "candles" key
        whose value is a list of objects each containing "open", "close", "low", "high", "volume",
        and "datetime" key-value pairs.

        Args:
            symbol: Ticker symbol to search for.
            start_date: Start date for price history period in UTC.
            end_date: End date for price history period in UTC.
            need_extended_hours_data: False to only return regular market hours data. Default: True.

        Returns:
            Price history for the ticker symbol as set of candles.

        Raises:
            ValueError: If passed arguments are invalid, or if start_date/end_date range contains no data.

        """
        params = validate_price_history_args(symbol=symbol, start_date=start_date, end_date=end_date,
                                             need_extended_hours_data=need_extended_hours_data)
        reply = requests.get(self._get_url('get_price_history', params=params),
                             headers=self._build_header())
        return process_price_history(reply.json(), start_date)

    @check_auth
    def get_instrument(self, symbol: str, projection: str = 'symbol-search'):
        """
        Return fundamental information for an instrument by ticker, CUSIP, or description.

        Args:
            symbol: The search string. Can be a ticker or a regex.
            projection: Type of search to perform.
                Supports:\n
                symbol-search: Search by exact ticker or CUSIP.\n
                symbol-regex: Return all instruments that match a regex.\n
                desc-regex: Return all instruments whose descriptions contain a regex.

        Returns:
            A dict of results where keys are tickers and values are objects containing
            fundamental information.

        """
        if projection not in ['symbol-search', 'symbol-regex', 'desc-regex']:
            raise NotImplementedError('Can only search by symbol, symbol regex, or desc regex.')

        reply = requests.get(self._get_url('get_instrument',
                                           {'symbol': symbol,
                                            'projection': projection}),
                             headers=self._build_header())
        return reply.json()

    @check_auth
    def get_quote(self, symbol: str):
        """
        Return quote for a given symbol.

        Args:
            symbol: The ticker symbol for a quote.

        Returns:
            A dict of results where keys are tickers and values are objects containing
            a quote.

        """
        reply = requests.get(self._get_url('get_quote',
                                           {'symbol': symbol}),
                             headers=self._build_header())
        return reply.json()

    @check_auth
    def get_positions(self) -> Dict:
        """
        Requests the positions information of self._acct_number

        Returns:
            A json object containing the account positions information.

        """
        reply = requests.get(self._get_url('positions'),
                             headers=self._build_header())
        return reply.json()

    @check_auth
    def get_movers(self, index: str, direction: str, change: str) -> Dict:
        """
        Return top 10 movers (up or down) by percent or value of one of the DOW, NASDAQ, or S&P500 indices.

        Args:
            index: The index symbol from which to get movers. Must be one of ['$COMPX', '$DJIA', '$SPX.X']
            direction: Return stocks that are moving 'up' or 'down'
            change: Return movers as 'percent' change or 'value' change

        Returns:
            A dict of list of movers with keys ['change', 'description', 'direction', 'last', 'symbol', 'totalVolume']

        """
        assert index in ['$COMPX', '$DJI', '$SPX.X'], 'Index must be one of ["$COMPX", "$DJIA", "$SPX.X"]'
        assert direction in ['up', 'down'], 'Direction must be one of ["up", "down"]'
        assert change in ['percent', 'value'], 'Change must be one of ["percent", "value"]'
        reply = requests.get(self._get_url('get_movers', {'index': index,
                                                          'direction': direction,
                                                          'change': change}),
                             headers=self._build_header())
        return reply.json()

    @check_auth
    def get_hours(self, markets: str, date: datetime) -> Dict:
        """
        Return market hours for a given market.

        Args:
            markets: Which market to get hours for
            date: Which date to retrieve market hours for. Must be in the future.

        Returns:
            A dict containing market hours for the passed asset class.

        """
        assert markets in ['EQUITY', 'OPTION', 'FUTURE', 'BOND', 'FOREX'], \
            'markets must be one of ["EQUITY", "OPTION", "FUTURE", "BOND", "FOREX"]'
        assert date >= datetime.today(), 'Can only get hours for future dates'
        reply = requests.get(self._get_url('get_hours', {'markets': markets,
                                                         'date': date.strftime('%Y-%m-%d')}),
                             headers=self._build_header()).json()
        if 'error' in reply.keys():
            raise ValueError(reply['error'])
        return reply

    def _get_url(self, url_type: str, params: Dict = None) -> str:
        """
        Build the correct url to perform an API action.

        Args:
            url_type: What type of url to build. Supports:
                positions: Return account positions.
                get_instrument: Return fundamental data for a ticker or CUSIP
                    Must include params['symbol'] and params['projection']
                get_quote: Return quote for a symbol.
                    Must include params['symbol']
                get_price_history: Return price history for a symbol.
                    Must include params['symbol', 'periodType', 'period', 'frequencyType', 'frequency', 'startDate',
                    'endDate', and 'needExtendedHoursData'.
                get_movers: Return top 10 movers by value or percent for a particular market.
                    Must include params['index', 'direction', 'change']
                get_hours: Return hours for a given market.
                    Must include params['markets', 'date']
            params: Dict of keyword arguments

        Returns:
            The requested url.

        Raises:
            NotImplementedError

        """
        url = urls.BASE_URL
        if url_type == 'positions':
            url += f'{urls.ACCOUNT_URL}{str(self._acct_number)}?fields={url_type}'
        elif url_type == 'get_instrument':
            url += f'{urls.INSTRUMENTS_URL}{urls.APIKEY_PARAM}{self._oauth_user_id}' \
                   f'&symbol={params["symbol"]}&projection={params["projection"]}'
        elif url_type == 'get_quote':
            url += f'{urls.QUOTES_URL}{urls.APIKEY_PARAM}{self._oauth_user_id}&symbol={params["symbol"]}'
        elif url_type == 'get_price_history':
            if params['format'] == 'period':
                passed_args = f'&periodType={params["periodType"]}&period={params["period"]}' \
                    f'&frequencyType={params["frequencyType"]}&frequency={params["frequency"]}' \
                    f'&needExtendedHoursData={params["needExtendedHoursData"]}'
            elif params['format'] == 'date':
                passed_args = f'frequencyType={params["frequencyType"]}&frequency={params["frequency"]}' \
                    f'&endDate={params["endDate"]}&startDate={params["startDate"]}' \
                    f'&needExtendedHoursData={params["needExtendedHoursData"]}'
            else:
                raise NotImplementedError(f'url format {params["format"]} is not supported for get_price_history.')
            url += f'{urls.PRICE_HISTORY_URL}{params["symbol"]}/pricehistory?{passed_args}'
        elif url_type == 'get_movers':
            url += f'{urls.MOVERS_URL}{params["index"]}/movers?direction={params["direction"]}' \
                   f'&change={params["change"]}'
        elif url_type == 'get_hours':
            url += f'{urls.HOURS_URL}?markets={params["markets"]}&date={params["date"]}'
        else:
            raise NotImplementedError('URL type {} not supported.'.format(url_type))
        return url

    @check_auth
    def _build_header(self) -> Dict:
        """
        Builds auth header to include with all requests.

        Returns:
            The header object to use with requests

        """
        return {'Authorization': 'Bearer ' + self.token}
