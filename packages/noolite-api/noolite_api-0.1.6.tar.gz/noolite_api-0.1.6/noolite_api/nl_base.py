from .typing import NooliteCommand
from .const import api_commands
import asyncio
from typing import Dict, Callable


class NooliteBase(object):

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj.callbacks: Dict[int, Callable] = {}
        return obj

    def reg_callback(self, channel: int, foo: Callable):
        """
        Регистрирует колбэк
        :param channel:
        :param foo:
        :return:
        """
        assert asyncio.iscoroutinefunction(foo), f'{foo} must be cotoutinefunction'
        self.callbacks[channel] = foo

    async def send_command(self, command: NooliteCommand):
        raise NotImplementedError

    def send_api(self, ch, br=0, cmd_name=None, **kwargs):
        """
        Отправляет команду из справочника команд
        :param cmd_name: название команды (как в справочнике)
        :param ch: номер канала
        :param br: яркость
        :param kwargs: дополнительные параметры, которые будут переданы в конструктор команды
        :return:
        """
        if br:
            kwargs['fmt'] = 1
            kwargs['d1'] = br
        if cmd_name is not None:
            kwargs.update(cmd=api_commands[cmd_name])
        asyncio.ensure_future(self.send_command(NooliteCommand(ch=ch, **kwargs)))

