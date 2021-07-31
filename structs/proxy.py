from aiohttp_socks import ProxyConnector
from structs.global_vars import GlobalVariables


class ProxyConnectorWrapper:

    def __init__(self):
        global_variables = GlobalVariables()
        if global_variables.config['connection']['proxy'] is None:
            self.connector = None
        else:
            self.connector = ProxyConnector.from_url(global_variables.config['connection']['proxy'],
                                                     rdns=global_variables.config['connection']['rdns'])