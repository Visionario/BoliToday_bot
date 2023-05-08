import requests
from bs4 import BeautifulSoup


class BolisInfo:
    """
    Get information from https://bolis.info

    Some code by Francisco "Cisco" Griman, https://github.com/fcoagz
    """

    def __init__(self):
        _response = 'https://bolis.info/'
        _document = requests.get(_response)

        self.hash_rate = ''
        self.difficulty = ''

        self.last_block = ''
        self.last_block_update = ''

        self.active_masternodes = ''
        self.expired_masternodes = ''

        self.coins_issued = ''
        self.coins_to_issue = ''

        if _document.status_code == 200:
            html = BeautifulSoup(_document.content, 'html.parser')

            html_state_red = html.find_all('div', 'card-body')

            self.hash_rate = html_state_red[0].text.split(' ')[3] + ' ' + html_state_red[0].text.split(' ')[4]
            self.difficulty = html_state_red[0].text.split(' ')[6] + ' ' + html_state_red[0].text.split(' ')[7]

            self.last_block = html_state_red[1].text.split(' ')[3]
            self.last_block_update = html_state_red[1].text.split(' ')[5] + ' ' + html_state_red[1].text.split(' ')[6] + ' ' + \
                                     html_state_red[1].text.split(' ')[7]

            self.active_masternodes = html_state_red[2].text.split(' ')[2]
            self.expired_masternodes = html_state_red[2].text.split(' ')[4]

            self.coins_issued = html_state_red[3].text.split(' ')[2].replace(',', '.')
            self.coins_to_issue = html_state_red[3].text.split(' ')[5].replace(',', '.')
