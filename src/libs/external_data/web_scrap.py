import requests
from bs4 import BeautifulSoup


class BolisInfo:
    """
    Get information from https://bolis.info

    Some code by Francisco "Cisco" Griman, https://github.com/fcoagz
    """

    def __init__(self):
        _response = 'https://bolis.info/'
        content = self._response_in_return_content(requests.get(_response))
        soup = BeautifulSoup(content, features="lxml")

        self.hash_rate = f'{self._get_value_bolis_info(soup)[0][3]} {self._get_value_bolis_info(soup)[0][4]}'
        self.difficulty = f'{self._get_value_bolis_info(soup)[0][6]} {self._get_value_bolis_info(soup)[0][7]}'

        self.last_block = f'{self._get_value_bolis_info(soup)[1][3]}'
        self.last_block_update = f'{self._get_value_bolis_info(soup)[1][5]} {self._get_value_bolis_info(soup)[1][6]} {self._get_value_bolis_info(soup)[1][7]}'

        self.active_masternodes = f'{self._get_value_bolis_info(soup)[2][2]}'
        self.expired_masternodes = f'{self._get_value_bolis_info(soup)[2][4]}'

        # optional replace , by .
        self.coins_issued = f'{self._get_value_bolis_info(soup)[3][2]}'.replace(',', '.')
        self.coins_to_issue = f'{self._get_value_bolis_info(soup)[3][5]}'.replace(',', '.')

    def _response_in_return_content(self, response: requests.Response) -> bytes:
        if not response.status_code == requests.codes.ok:
            raise ValueError('Cannot connect to bolis.info server')
        return response.content

    def _get_value_bolis_info(self, soup: BeautifulSoup) -> list:
        values = soup.find_all('div', 'card-body')
        list_value = []
        for value in values:
            list_value.append(value.text.split(' '))
        return list_value
