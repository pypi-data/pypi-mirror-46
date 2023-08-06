import uuid
import requests

from urllib.parse import urlparse 

from .hub.base_hub_connection import BaseHubConnection
from .hub.auth_hub_connection import AuthHubConnection
from .messages.invocation_message import InvocationMessage
from .protocol.json_hub_protocol import JsonHubProtocol
from .helpers import helpers

class HubConnectionError(ValueError):
    pass


class HubConnectionBuilder(object):
    """
    Hub connection class, manages handshake and messaging

    Args:
        hub_url: SignalR core url

    Raises:
        HubConnectionError: Raises an Exception if url is empty or None
    """
    def __init__(self):
        self.hub_url = None
        self._hub = None
        self.options = {
                "access_token_factory": None
            }
        self.token = None
        self.headers = None
        self.negotiate_headers = None
        self.has_auth_configured = None
        self.protocol = None        

    def with_url(
            self,
            hub_url,
            options=None):
        if hub_url is None or hub_url.strip() is "":
            raise HubConnectionError("hub_url must be a valid url.")

        if options is not None and type(options) != dict:
            raise HubConnectionError("options must be a dict {0}.".format(self.options))

        if options is not None \
                and "access_token_factory" in options.keys()\
                and not callable(options["access_token_factory"]):
            raise HubConnectionError("access_token_factory must be a function without params")

        if options is not None:

            self.has_auth_configured = "access_token_factory" in options.keys() \
                                       and callable(options["access_token_factory"])
        self.hub_url = hub_url
        self._hub = None
        self.options = self.options if options is None else options
        return self

    def build(self):
        """"
        self.token = token
        self.headers = headers
        self.negotiate_headers = negotiate_headers
        self.has_auth_configured = token is not None

        """
        self.protocol = JsonHubProtocol()
        self.headers = {}        

        if self.has_auth_configured:
            auth_function = self.options["access_token_factory"]
            self.token = auth_function()
            self.negotiate_headers = {"Authorization": "Bearer " + self.token}     

        self.negotiate() 

        self._hub = AuthHubConnection(self.hub_url, self.protocol, self.token, self.negotiate_headers)\
            if self.has_auth_configured else\
            BaseHubConnection(
                self.hub_url,
                self.protocol)
        return self

    def on(self, event, callback_function):
        """
        Register a callback on the specified event
        :param event: Event name
        :param callback_function: callback function, arguments will be binded
        :return:
        """
        self._hub.register_handler(event, callback_function)

    def stream(self, event, event_params):
        return self._hub.stream(event, event_params)
        
    def start(self):
        self._hub.start()

    def stop(self):
        self._hub.stop()

    def send(self, method, arguments):
        if not self._hub.connection_alive:
            raise HubConnectionError("Connection is closed, cant send a message")
        if type(arguments) is not list:
            raise HubConnectionError("Arguments of a message must be a list")
        self._hub.send(InvocationMessage(
            {},
            str(uuid.uuid4()),
            method,
            arguments))    

    def negotiate(self):
        response = requests.post(helpers.get_negotiate_url(self.hub_url), headers=self.negotiate_headers)
        data = response.json()

        if 'url' in data.keys() and 'accessToken' in data.keys():
            self.hub_url = data["url"]
            self.token = data["accessToken"]
            self.negotiate_headers = {"Authorization": "Bearer " + self.token}
            self.has_auth_configured = True