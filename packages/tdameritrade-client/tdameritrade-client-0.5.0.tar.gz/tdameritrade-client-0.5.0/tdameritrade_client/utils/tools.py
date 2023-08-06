import functools
from datetime import datetime, timezone
from typing import Callable, Dict


def check_auth(func: Callable) -> Callable:
    """
    Decorator that ensures auth has been run before calling func
    Args:
        func: The decorated function
    """
    @functools.wraps(func)
    def wrapper_check_auth(*args, **kwargs):
        if args[0].token is None:
            raise AssertionError('Cannot run {} before performing auth flow'.format(func.__name__))
        value = func(*args, **kwargs)
        return value
    return wrapper_check_auth


def validate_price_history_args(symbol: str, frequency_type: str = None, frequency: int = None,
                                period_type: str = 'day', period: int = None, start_date: datetime = None,
                                end_date: datetime = None, need_extended_hours_data: bool = True) -> Dict:
    """Ensures all variables passed to a self.get_price_history() call are valid with respect to one another.

    See the following API definition for a source on all of the following rules:
    https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory

    Args:
        symbol: Ticker symbol to search for.
        frequency_type: The type of frequency with which a new candle is formed. Must be
            either 'minute', 'daily', 'weekly', or 'monthly'.
        frequency: Frequency with which to return candles.
        period_type: The type of period-data to return. Must be either 'day', 'month',
            'year', or 'ytd'. Default: 'day'.
        period: The length of periodType over which to receive price history.
        start_date: Start date for price history period. Given with endDate as an alternative to period.
        end_date: End date for price history period. Given with endDate as an alternative to period.
        need_extended_hours_data: False to only return regular market hours data. Default: True.

    Returns:
        Dict of params to pass to self._get_url for a proper API call.

    Raises:
        ValueError: If passed arguments are invalid.

    """
    # Check frequencies are valid
    if frequency_type is not None and frequency is not None:
        if frequency_type == 'minute' and frequency not in [1, 5, 10, 15, 30]:
            raise ValueError(f'Invalid frequency ({frequency}) for frequency_type {frequency_type}. Must be in '
                             f'[1, 5, 10, 15, 30].')
        elif frequency_type in ['daily', 'weekly', 'monthly'] and frequency != 1:
            raise ValueError(f'Invalid frequency ({frequency}) for frequency_type {frequency_type}. Must be in '
                             f'[1].')
        elif frequency_type not in ['minute', 'daily', 'weekly', 'monthly']:
            raise ValueError(f'Invalid frequency_type {frequency_type}. Must be in ["minute", "daily", "weekly", "monthly"]')

    if period is not None:
        # Check period/period_type is valid
        if start_date is not None or end_date is not None:
            raise ValueError('Provide either start/endDate or period, but not both.')

        if period_type not in ['day', 'month', 'year', 'ytd']:
            raise ValueError(f'Invalid periodType: {period_type}. Must be either day, month, year, or ytd.')

        if period_type == 'day':
            if period not in [1, 2, 3, 4, 5, 10]:
                raise ValueError(f'Invalid period ({period}) for periodType {period_type}. '
                                 f'Must be one of [1, 2, 3, 4, 5, 10].')
            if frequency_type not in ['minute']:
                raise ValueError(f'Invalid frequency_type ({frequency_type}) for periodType {period_type}. '
                                 f'Must be one of ["minute"].')
        elif period_type == 'month':
            if period not in [1, 2, 3, 6]:
                raise ValueError(f'Invalid period ({period}) for periodType {period_type}. '
                                 f'Must be one of [1, 2, 3, 6].')
            if frequency_type not in ['daily', 'weekly']:
                raise ValueError(f'Invalid frequency_type ({frequency_type}) for periodType {period_type}. '
                                 f'Must be one of ["daily", "weekly"].')
        elif period_type == 'year':
            if period not in [1, 2, 3, 5, 10, 15, 20]:
                raise ValueError(f'Invalid period ({period}) for periodType {period_type}. '
                                 f'Must be one of [1, 2, 3, 5, 10, 15, 20].')
            if frequency_type not in ['daily', 'weekly', 'monthly']:
                raise ValueError(f'Invalid frequency_type ({frequency_type}) for periodType {period_type}. '
                                 f'Must be one of ["daily", "weekly", "monthly"].')
        elif period_type == 'ytd':
            if period != 1:
                raise ValueError(f'Invalid period ({period}) for periodType {period_type}. '
                                 f'Must be one of [1].')
            if frequency_type not in ['daily', 'weekly']:
                raise ValueError(f'Invalid frequency_type ({frequency_type}) for periodType {period_type}. '
                                 f'Must be one of ["daily", "weekly"].')
        params = {
            'format': 'period',
            'symbol': symbol.upper(),
            'frequencyType': frequency_type,
            'frequency': frequency,
            'periodType': period_type,
            'period': period,
            'needExtendedHoursData': need_extended_hours_data
        }
    else:
        if end_date is None or start_date is None:
            raise ValueError('Must provide both end_date and start_date with get_dated_price_history, or provide '
                             'neither using get_period_price_history along with a valid period/period_type.')
        if end_date <= start_date:
            raise ValueError(f'end_date {end_date} is earlier than start_date {start_date}.')
        params = {
            'format': 'date',
            'symbol': symbol.upper(),
            'frequencyType': 'minute',
            'frequency': 1,
            'startDate': int(start_date.replace(tzinfo=timezone.utc).timestamp() * 1000),
            'endDate': int(end_date.replace(tzinfo=timezone.utc).timestamp() * 1000),
            'needExtendedHoursData': need_extended_hours_data
        }
    return params


def process_price_history(candles_response: Dict, start_date: datetime = None) -> Dict:
    """Turn timestamps into datetimes and remove entries before start_date.

    Performs post processing on a response from a price history call. Converts timestamps to UTC human readable dates
    and removes dates that are before start_date

    Args:
        candles_response: A response from a call to the price history endpoint
        start_date: An optional datetime used if calling get_dated_price_history to filter results

    Returns:
        Candles with human readable dates only after start_date

    Raises:
        ValueError: If the response was an error

    """
    if 'error' not in candles_response.keys():
        processed_candles = []
        for candle in candles_response['candles']:
            processed_candle = candle
            candle_datetime = datetime.utcfromtimestamp(candle['datetime'] / 1000)
            processed_candle['datetime'] = candle_datetime.strftime('%Y-%m-%d_%H-%M-%S')

            if start_date is not None:
                if candle_datetime < start_date:
                    continue
            processed_candles.append(processed_candle)

        candles_response['candles'] = processed_candles
        return candles_response

    else:
        raise ValueError('Invalid response returned from TDAmeritrade. Try setting end time after 11am UTC.')

