from .const import dispatchers, logger
from .typing import NooliteCommand, NooliteRemote, BaseNooliteRemote
from .nl_base import NooliteBase
from typing import Callable, Any, Optional
from functools import wraps
import time
import asyncio
from dataclasses import astuple
import serial

APPROVAL_TIMEOUT = 1


class NotApprovedError(Exception):
    pass


class NooliteSerial(NooliteBase):
    """
    Взаимодействие с noolite через serial-порт
    """
    def __init__(self
                 , tty_name: str
                 , loop: Optional[asyncio.AbstractEventLoop] = None):
        """
        :param tty_name: имя порта
        :param input_command_callback_method: колбэк на входящие сообщения
        :param loop: eventloop, по умолчанию текущий евентлуп
        """
        self.tty = self._get_tty(tty_name)
        self.responses = []
        self._loop = loop
        #работа с очередью исходящих сообщений
        self.send_lck = asyncio.Lock()
        self.wait_ftr: asyncio.Future = None
        self.wait_out: NooliteCommand = None

    @property
    def loop(self):
        return self._loop or asyncio.get_event_loop()

    def start_listen(self):
        """
        Начать прослушивание порта, можно запускать только при наличии работающего eventloop
        :return:
        """
        self.loop.add_reader(self.tty.fd, self.inf_reading)

    def cancel_waiting(self, msg: NooliteCommand):
        """
        Отменяет ожидание подвтерждения, возвращает истину если ожидание было, ложь, если нет
        :return:
        """
        if isinstance(self.wait_ftr, asyncio.Future) \
                and msg.ch == self.wait_out.ch \
                and msg.mode == self.wait_out.mode:
            self.wait_ftr.cancel()
            self.wait_ftr = None
            return True
        else:
            return False

    def inf_reading(self):
        """
        Хендлер входящих данных от адаптера
        :return:
        """
        while self.tty.in_waiting >= 17:
            in_bytes = self.tty.read(17)
            resp = NooliteCommand(*list(in_bytes))
            if not self.cancel_waiting(resp):
                logger.debug('Incoming command: {}'.format(resp))
                remote = (dispatchers.get(resp.cmd) or NooliteRemote)(resp)
                self.loop.create_task(self.callbacks[resp.ch](remote))

    async def send_command(self, command: NooliteCommand):
        """
        Отправляет команды, асинхронно, ждет подтверждения уже отправленной команды
        :param command:
        :return:
        """
        # отправляем только одну команду до получения подтверждения
        async with self.send_lck:
            logger.info('> {}'.format(command))
            before = time.time()
            self.tty.write(bytearray(astuple(command)))
            logger.info('Time to write: {}'.format(time.time() - before))

            async def waiter():
                await asyncio.sleep(APPROVAL_TIMEOUT)
                return True

            # отправляем команду и ждем секунду, если придет ответ, то ожидание будет отменено с ошибкой CancelledError
            # - значит от модуля пришел ответ о подтверждении команды, в противном случае поднимаем ошибку о том что
            # команда не подтверждена

            try:
                self.wait_ftr = asyncio.ensure_future(waiter())
                await self.wait_ftr
            except asyncio.CancelledError:
                return True
            raise NotApprovedError(command)

    @staticmethod
    def _get_tty(tty_name) -> serial.Serial:
        """
        Подключение к последовательному порту
        :param tty_name: имя порта
        :return:
        """
        serial_port = serial.Serial(tty_name, timeout=2)
        if not serial_port.is_open:
            serial_port.open()
        serial_port.flushInput()
        serial_port.flushOutput()
        return serial_port


def dispatch_command(foo: Callable[[BaseNooliteRemote], Any]):
    """
    Декоратор, который обрабатывает команду от адаптера и передает ее в функцию как BaseNooliteRemote - объект
    :param foo: функция для декорирования
    :return:
    """
    @wraps(foo)
    def wrapper(command: NooliteCommand):
        logger.info(f'Dispatch command with channel {command.ch}')
        sensor = (dispatchers.get(command.cmd) or NooliteRemote)(command)
        return foo(sensor)

    return wrapper
