import requests, json


class CoingateAPIClient:
    _url = 'https://api.coingate.com/v2'

    def __init__(self, token):
        self._token = token

    @staticmethod
    def get_url():
        return _url

    @property
    def url(self):
        return self._url

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self.token}',
        }

    def create_order(self, price_amount, price_currency, title, description):
        orders_url = f'{self.url}/orders'

        data = {
            'price_amount': price_amount,
            'price_currency': price_currency,
            'title': title,
            'description': description
        }

        response_json_string = requests.post(
            url=orders_url,
            headers=self.headers(),
            data=json.dumps(data)
        ).text
        return json.loads(response_json_string)

    def get_order(self, order_id):
        orders_url = f'{self.url}/orders'
        get_order_url = f'{orders_url}/{order_id}'

        response_json_string = requests.get(
            url=get_order_url,
            headers=self.headers(),
        ).text
        return json.loads(response_json_string)

    def get_orders(self):
        orders_url = f'{self.url}/orders'

        response_json_string = requests.get(
            url=orders_url,
            headers=self.headers(),
        ).text
        return json.loads(response_json_string)

