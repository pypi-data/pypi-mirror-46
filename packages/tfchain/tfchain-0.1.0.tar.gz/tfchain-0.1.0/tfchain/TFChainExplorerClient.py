"""
Tfchain Client
"""
import tfchain
from tfchain.internal.jsutils import json_dumps, json_loads
from tfchain.internal.HttpClient import HTTPError, HttpClient
import random

http = HttpClient()

class TFChainExplorerClient:
    """
    Client to get data from a tfchain explorer.
    """

    def __init__(self, addresses):
        if not isinstance(addresses, list) or len(addresses) == 0:
            raise TypeError("addresses expected to be a non-empty list of string-formatted explorer addresses, not {}".format(type(addresses)))
        self._addresses = addresses

    @property
    def addresses(self):
        """
        Addresses of the explorers to use
        """
        return self._addresses

    def get(self, endpoint):
        """
        get data from an explorer at the endpoint from any explorer that is available
        on one of the given urls. The list of urls is traversed in random order until
        an explorer returns with a 200 OK status.

        @param endpoint: the endpoint to get the data from
        """
        indices = list(range(len(self._addresses)))
        random.shuffle(indices)
        for idx in indices:
            try:
                address = self._addresses[idx]
                if not isinstance(address, str):
                    raise TypeError("explorer address expected to be a string, not {}".format(type(address)))
                # this is required in order to be able to talk directly a daemon
                headers = {'User-Agent': 'Rivine-Agent'}
                # do the request and check the response
                resp = http.get(url=address+endpoint, headers=headers)
                if resp.getcode() == 200:
                    return resp.readline()
                if resp.getcode() == 204:
                    raise tfchain.errors.ExplorerNoContent("GET: no content available (code: 204)", endpoint)
                raise tfchain.errors.ExplorerServerError("error (code: {})".format(resp.getcode()), endpoint)
            except HTTPError as e:
                if e.status_code == 400:
                    msg = e.msg
                    if isinstance(msg, (bytes, bytearray)):
                        msg = msg.decode('utf-8')
                    if isinstance(msg, str) and (('unrecognized hash' in msg) or ('not found' in msg)):
                        raise tfchain.errors.ExplorerNoContent("GET: no content available for specified hash (code: 400)", endpoint)
                if e.status_code:
                    raise tfchain.errors.ExplorerServerError("GET: error (code: {}): {}".format(e.status_code, e.msg), endpoint)
                print("tfchain explorer get exception at endpoint {} on {}: {}".format(endpoint, address, e))
        raise tfchain.errors.ExplorerNotAvailable("no explorer was available", endpoint=endpoint, addresses=self._addresses)

    def post(self, endpoint, data):
        """
        put data to an explorer at the endpoint from any explorer that is available
        on one of the given urls. The list of urls is traversed in random order until
        an explorer returns with a 200 OK status.

        @param endpoint: the endpoint to post the data to
        """
        indices = list(range(len(self._addresses)))
        random.shuffle(indices)
        for idx in indices:
            try:
                address = self._addresses[idx]
                if not isinstance(address, str):
                    raise TypeError("explorer address expected to be a string, not {}".format(type(address)))
                # this is required in order to be able to talk directly a daemon,
                # and to specify the data format correctly
                headers = {
                    'User-Agent': 'Rivine-Agent',
                    'content-type': 'application/json',
                }
                # ensure the data is already JSON encoded and bytes
                if isinstance(data, dict):
                    data = json_dumps(data)
                if isinstance(data, str):
                    data = data.encode('utf-8')
                if not isinstance(data, bytes):
                    raise TypeError("expected post data to be bytes, not {}".format(type(data)))
                # do the request and check the response
                resp = http.post(url=address+endpoint, data=data, headers=headers)
                if resp.getcode() == 200:
                    return resp.readline()
                raise tfchain.errors.ExplorerServerPostError("POST: unexpected error (code: {})".format(resp.getcode()), endpoint, data=data)
            except HTTPError as e:
                if e.status_code:
                    raise tfchain.errors.ExplorerServerPostError("POST: error (code: {}): {}".format(e.status_code, e.msg), endpoint, data=data)
                print("tfchain explorer get exception at endpoint {} on {}: {}".format(endpoint, address, e))
                pass
        raise tfchain.errors.ExplorerNotAvailable("no explorer was available", endpoint=endpoint, addresses=self._addresses)
