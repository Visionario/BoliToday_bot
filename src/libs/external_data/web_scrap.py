import requests
from bs4 import BeautifulSoup

def _response_in_return_content(response: requests.Response) -> bytes:
    if not response.status_code == requests.codes.ok:
        raise ValueError('Cannot connect to bolis.info server')
    return response.content

def _get_value_bolis_info(soup: BeautifulSoup) -> list:
    values = soup.find_all('div', 'card-body')
    list_value = []
    for value in values:
        list_value.append(value.text.split(' '))
    return list_value

class BolisInfo:
    """
    Get information from https://bolis.info

    Some code by Francisco "Cisco" Griman, https://github.com/fcoagz
    """
    def __init__(self):
        _response = 'https://bolis.info/'
        content = _response_in_return_content(requests.get(_response))
        soup = BeautifulSoup(content, features="lxml")

        self.hash_rate = f'{_get_value_bolis_info(soup)[0][3]} {_get_value_bolis_info(soup)[0][4]}'
        self.difficulty = f'{_get_value_bolis_info(soup)[0][6]} {_get_value_bolis_info(soup)[0][7]}'

        self.last_block = f'{_get_value_bolis_info(soup)[1][3]}'
        self.last_block_update = f'{_get_value_bolis_info(soup)[1][5]} {_get_value_bolis_info(soup)[1][6]} {_get_value_bolis_info(soup)[1][7]}'

        self.active_masternodes = f'{_get_value_bolis_info(soup)[2][2]}'
        self.expired_masternodes = f'{_get_value_bolis_info(soup)[2][4]}'
        
        # optional replace , by .
        self.coins_issued = f'{_get_value_bolis_info(soup)[3][2]}'.replace(',', '.')
        self.coins_to_issue = f'{_get_value_bolis_info(soup)[3][5]}'.replace(',', '.')
