from tronpy import Tron
from tronpy.providers import HTTPProvider
from app.tron.env_tron_api_key import api_key


client = Tron(
    provider=HTTPProvider(
        endpoint_uri="https://api.trongrid.io",
        api_key=api_key
    )
)


async def get_tron_info(address):
    '''Функция получения данных о пользователе'''
    balance = client.get_account_balance(address)
    resources = client.get_account_resource(address)
    return balance, resources