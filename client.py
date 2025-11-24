from dotenv import dotenv_values
from py_clob_client.constants import POLYGON
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY

config = dotenv_values('pmpe.env')

host = 'https://clob.polymarket.com'
chain_id = POLYGON # Polygon chain ID (137)
address = config["FUNDER_ADDRESS"] # the actual address that holds your funds on Polymarket
key = config["PRIVATE_KEY"] # Polymarket - Settings - Export Private Key
signature_type=1 # tells the system how to verify your signatures: 1 means Email/Magic wallet signatures

# Learn more about Signature Types: https://github.com/Polymarket/py-clob-client?tab=readme-ov-file#start-trading-proxy-wallet

def get_client():
    ''' 
        Learn more about CLOB Authentication: https://docs.polymarket.com/developers/CLOB/authentication

        L1: Private Key Authentication
        1. Sign the order
        2. Create or revoke API keys
    '''
    client = ClobClient(host=host, key=key, chain_id=chain_id, signature_type=signature_type, funder=address) # L1: Private Key Authentication

    ''' 
        L2: API Key Authentication - The next level of authentication consists of the API key, secret, and passphrase.
        These are used solely to authenticate API requests made to Polymarket’s CLOB, such as posting/canceling orders or retrieving an account’s orders and fills.
    '''
    credentials = client.create_or_derive_api_creds()
    client.set_api_creds(credentials) # L2 authentication: API Key Authentication 

    return client


if __name__ == '__main__':
    client = get_client()

    order_args = OrderArgs(
        price=0.01,
        size=10.0,
        side=BUY,
        token_id="" # <-- specify token
    )

    signed_order = client.create_order(order_args) # This endpoint requires the L1 authentication: Private Key Authentication

    response = client.post_order(signed_order, OrderType.GTC) # This endpoint requires the L2 authentication: API Key Authentication
    
    print(response)