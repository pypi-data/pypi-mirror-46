import base64
from asyncio import get_running_loop

from aiohttp import ClientSession
from mixpanel import MixpanelException


class AIOConsumer(object):
    def __init__(self, client: ClientSession, events_url=None, people_url=None, import_url=None):
        self._endpoints = {
            'events': events_url or 'https://api.mixpanel.com/track',
            'people': people_url or 'https://api.mixpanel.com/engage',
            'imports': import_url or 'https://api.mixpanel.com/import',
        }
        self._client = client

    def send(self, endpoint: str, json_message: str, api_key: str = None):
        """Immediately record an event or a profile update.
        :param endpoint: the Mixpanel API endpoint appropriate for the message
        :type endpoint: "events" | "people" | "imports"
        :param str json_message: a JSON message formatted for the endpoint
        :param str api_key: your Mixpanel project's API key
        :raises MixpanelException: if the endpoint doesn't exist, the server is
            unreachable, or the message cannot be processed
        """
        if endpoint in self._endpoints:
            loop = get_running_loop()
            loop.create_task(self._write_request(self._endpoints[endpoint], json_message, api_key))
        else:
            raise MixpanelException('No such endpoint "{0}". Valid endpoints are one of {1}'
                                    .format(endpoint, self._endpoints.keys()))

    async def _write_request(self, url: str, json_message: str, api_key: str):
        data = {
            'data': base64.b64encode(json_message.encode('utf8')).decode("utf8"),
            'verbose': 1,
            'ip': 0,
        }

        if api_key:
            data.update(dict(api_key=api_key))

        try:
            response = await self._client.get(url, params=data, raise_for_status=True)
            json = await response.json()
        except Exception as e:
            raise MixpanelException(e)

        if json['status'] != 1:
            raise MixpanelException('Mixpanel error: {0}'.format(json['error']))

        return True
