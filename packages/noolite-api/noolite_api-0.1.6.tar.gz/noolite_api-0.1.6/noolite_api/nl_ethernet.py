import asyncio
from urllib.parse import urlencode
import aiohttp
from typing import Callable, Any
from .const import logger, api_commands
from .nl_base import NooliteBase
from .typing import EthernetSensor
import xmltodict


class NooliteEthernet(NooliteBase):
    """
    Управление noolite через Ethernet
    Обновляет инфу о сенсорах с периодичностью, заданной в update_interval и вызывает колбэк с распарсеным xml
    """
    def __init__(self
                 , host
                 , update_interval = None
                 , cb_sensors: Callable[[dict], Any] = None
                 ):
        """

        :param host:
        :param update_interval: периодичность обновления сенсоров в секундах
        :param cb_sensors: колбэк на обновлении сенсоров
        """
        self.host=host
        self.lck=asyncio.locks.Lock()
        self.update_interval = update_interval
        self.cb_sensors = cb_sensors

    async def _request(self, **kwargs):
        kwargs = {x:y for x, y in kwargs.items() if x is not None}
        async with self.lck:
            url = f'{self.host}/api.htm?{urlencode(kwargs)}'
            logger.info(url)
            async with aiohttp.request('get', url) as req:
                await req.read()

    def send_api(self, ch, br=0, cmd_name=None, **kwargs):
        asyncio.ensure_future(self._request(ch=ch, cmd=api_commands[cmd_name], br=br))

    async def update_sensors(self):
        await asyncio.wait(self.update_interval)

        def parse():
            async with aiohttp.request('get', f'{self.host}/sens.xml') as req:
                txt = await req.text()
            parsed = xmltodict.parse(txt)['response']
            for x in range(4):
                yield x, EthernetSensor(
                    temp=parsed[f'snst{x}']
                    , humidity=parsed[f'snsh{x}']
                    , status=parsed[f'snt{x}']
                )

        await self.cb_sensors(dict(parse()))
        asyncio.ensure_future(self.update_sensors())

    def start_listen(self):
        asyncio.ensure_future(self.update_sensors())