import requests
import json

class BolisInfo:
    """
    Get information from https://api.bolivarcoin.tech//help_docs

    Some code by Francisco "Cisco" Griman, https://github.com/fcoagz
    """

    def __init__(self):
        _content = self._get_content(requests.get('https://api.bolivarcoin.tech/'))
        suffix = 'K' if _content['blockchain']['difficulty'] < 999999 else 'M'
        self.difficulty = f"{round(_content['blockchain']['difficulty'] / 1000, 2):.2f} {suffix}"
        self.hash_rate = _content['networkinfo']['connections']
        self.active_masternodes = _content['masternodes']['enabled']

    def _get_content(self, response: requests.Response):
        if not response.status_code == requests.codes.ok:
            raise ValueError('Cannot connect to api.bolivarcoin.tech server')
        return json.loads(response.content.decode('utf-8'))