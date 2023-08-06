import base64
import encodings.utf_8
from asyncio import get_running_loop, AbstractEventLoop

from aiohttp import ClientSession
from mixpanel import MixpanelException, Consumer

_encoding = encodings.utf_8.getregentry().name


class AIOConsumer(Consumer):
    """
    A aiohttp-based consumer that sends an HTTP request directly to the Mixpanel service, one
    per call to :meth:`~.send`.

    :param ClientSession client: a client session to use throughout the Consumer lifetime
    :param AbstractEventLoop loop: override current loop the relevant loop to create tasks with
    :param str events_url: override the default events API endpoint
    :param str people_url: override the default people API endpoint
    :param str import_url: override the default import API endpoint
    """

    def __init__(self, client: ClientSession, loop: AbstractEventLoop = None,
                 events_url: str = None, people_url: str = None, import_url: str = None):
        super().__init__(events_url, people_url, import_url)
        self._loop = loop or get_running_loop()
        self._client = client

    def send(self, endpoint: str, json_message: str, api_key: str = None):
        """
        Record an event or a profile update.

        :param endpoint: the Mixpanel API endpoint appropriate for the message
        :type endpoint: "events" | "people" | "imports"
        :param str json_message: a JSON message formatted for the endpoint
        :param str api_key: your Mixpanel project's API key
        :raises MixpanelException: if the endpoint doesn't exist, the server is
            unreachable, or the message cannot be processed
        """
        if endpoint in self._endpoints:
            self._loop.create_task(self._write_request(self._endpoints[endpoint], json_message, api_key))
        else:
            raise MixpanelException('No such endpoint "{0}". Valid endpoints are one of {1}'
                                    .format(endpoint, self._endpoints.keys()))

    async def _write_request(self, request_url: str, json_message: str, api_key: str = None):
        b64message = base64.b64encode(json_message.encode(_encoding)).decode(_encoding)

        data = {
            'data': b64message,
            'verbose': 1,
            'ip': 0,
        }

        if api_key:
            data.update(dict(api_key=api_key))

        try:
            response = await self._client.get(request_url, params=data, raise_for_status=True)
            json = await response.json()
        except Exception as e:
            raise MixpanelException(e)

        if json.get('status') != 1:
            raise MixpanelException('Mixpanel error: {0}'.format(json.get('error')))

        return True
