from dataclasses import dataclass, astuple
import time
from .const import APPROVAL_TIMEOUT

MODE_SEND = 1
MODE_RECIEVE = 2


@dataclass()
class _NooliteCommand:
    """
    Контейнер для команды от адаптера или к адаптеру
    """
    st: int = 171
    mode: int = 0
    ctr: int = 0
    togl: int = 0
    ch: int = 0
    cmd: int = 0
    fmt: int = 0
    d0: int = 0
    d1: int = 0
    d2: int = 0
    d3: int = 0
    id0: int = 0
    id1: int = 0
    id2: int = 0
    id3: int = 0
    crc: int = 0
    sp: int = 172
    commit: bool = APPROVAL_TIMEOUT


@dataclass()
class EthernetSensor:

    temp: float
    status: str
    humidity: float = None

class NooliteCommand(_NooliteCommand):
    """
    Автоматический расчет crc если команда исходящая
    """
    # todo: валидация входящей команды по crc

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.sp == 171:
            self.crc = self.calc_crc()

    def calc_crc(self):
        crc = sum(astuple(self)[0:15])
        return crc if crc < 256 else divmod(crc, 256)[1]


class BaseNooliteRemote(object):

    """
    Базовый класс для описания пульта noolite
    """

    def __init__(self, command: NooliteCommand):
        self.command = command
        self.last_update = time.time()

    @property
    def channel(self):
        return self.command.ch

    @property
    def battery_status(self):
        return int('{:08b}'.format(self.command.d1)[0])


class TempHumSensor(BaseNooliteRemote):

    def __str__(self):
        return 'Ch: {}, battery: {}, temp: {}, hum: {}'.format(self.channel, self.battery_status, self.temp, self.hum)

    @property
    def sensor_type(self):
        """
        тип датчика
        :return:
        """
        # Тип датчика:
        #   000-зарезервировано
        #   001-датчик температуры (PT112)
        #   010-датчик температуры/влажности (PT111)
        return '{:08b}'.format(self.command.d1)[1:4]

    @property
    def temp(self):
        """
        температура
        :return:
        """
        temp_bits = '{:08b}'.format(self.command.d1)[4:] + '{:08b}'.format(self.command.d0)
        # Если первый бит 0 - температура считается выше нуля
        if temp_bits[0] == '0':
            return int(temp_bits, 2) / 10.
        # Если 1 - ниже нуля. В этом случае необходимо от 4096 отнять полученное значение
        elif temp_bits[0] == '1':
            return -((4096 - int(temp_bits, 2)) / 10.)

    @property
    def hum(self):
        """
        влажность
        :return:
        """
        # Если датчик PT111 (с влажностью), то получаем влажность из 3 байта данных
        if self.sensor_type == '010':
            return self.command.d2

    @property
    def analog_sens(self):
        # Значение, считываемое с аналогового входа датчика; 8 бит; (по умолчанию = 255)
        return self.command.d3


class MotionSensor(BaseNooliteRemote):

    def __str__(self):
        return 'Ch: {}, battery: {}, active_time: {}'.format(self.channel, self.battery_status, self.active_time)

    @property
    def active_time(self):
        """
        Время на которое включается устройство
        :return:
        """
        return self.command.d0 * 5

    @property
    def is_active(self):
        """
        Статус активности
        :return:
        """
        return self.last_update + self.active_time >= time.time()


class NooliteRemote(BaseNooliteRemote):

    @property
    def command(self):
        """
        Команда
        :return:
        """
        return self.command.cmd
