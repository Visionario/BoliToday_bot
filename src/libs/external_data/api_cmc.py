import json

from requests import Session

from libs.settings import AppSettings

# import pprint

# Settings
settings = AppSettings()


def get_cmc_data(convert_to='USD'):
    """
    Function to get the info from CMC

    https://coinmarketcap.com/api/documentation/v1/#operation/getV2CryptocurrencyQuotesLatest

        {'data': {'1053': {'circulating_supply': 18638951.87379985,
                           'cmc_rank': 2255,
                           'date_added': '2015-09-08T00:00:00.000Z',
                           'id': 1053,
                           'infinite_supply': False,
                           'is_active': 1,
                           'is_fiat': 0,
                           'last_updated': '2023-05-08T01:18:00.000Z',
                           'max_supply': 25000000,
                           'name': 'Bolivarcoin',
                           'num_market_pairs': 1,
                           'platform': None,
                           'quote': {'USD': {'fully_diluted_market_cap': 72884.09,
                                             'last_updated': '2023-05-08T01:18:00.000Z',
                                             'market_cap': 54339.3186333851,
                                             'market_cap_dominance': 0,
                                             'percent_change_1h': -0.03033565,
                                             'percent_change_24h': -0.14318585,
                                             'percent_change_30d': 3.3944432,
                                             'percent_change_60d': 32.77725717,
                                             'percent_change_7d': -2.40176449,
                                             'percent_change_90d': -6.11892234,
                                             'price': 0.0029153634282283896,
                                             'tvl': None,
                                             'volume_24h': 16.91648679,
                                             'volume_change_24h': -67.9387}},
                           'self_reported_circulating_supply': None,
                           'self_reported_market_cap': None,
                           'slug': 'bolivarcoin',
                           'symbol': 'BOLI',
                           'tags': ['mineable', 'pow', 'x11', 'masternodes'],
                           'total_supply': 18638951.87379985,
                           'tvl_ratio': None}},
         'status': {'credit_count': 1,
                    'elapsed': 86,
                    'error_code': 0,
                    'error_message': None,
                    'notice': None,
                    'timestamp': '2023-05-08T01:19:27.626Z'}}
    :return:
    """

    # CoinMarketCap API url
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    # API parameters to pass in for retrieving specific cryptocurrency data
    # parameters = {'slug': 'bolivarcoin', 'convert': 'USD'}
    parameters = {
            "id": '1053',
            'convert': convert_to,
            # 'convert': 'BTC',
            # 'convert_id': 1,
            # 'aux': "num_market_pairs,cmc_rank,circulating_supply"
            }

    # Replace 'YOUR_API_KEY' with the API key you have received in the previous step
    headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.CMC_PRO_API_KEY
            }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    info = json.loads(response.text)

    # pprint.pprint(info)
    return info
