# Noolite API integration
Интеграция устройств noolite в python, полностью асинхронная работа

## MTRF-64
Поддерживается отправка и прием команд на адаптер MTRF-64 `https://www.noo.com.by/mtrf-64.html` через serial-порт. Команды от 
адаптера перенаправляются в колбэк пользователя. Колбэки регистрируются на канал, на каждом канале может быть 
зарегистрирован только один колбэк, колбэк должен на вход принимать один аргумент - это объект описывающий поступившую 
команду

Библиотека разрабатывалась для работы с  Нome-assistant, но никто не мешает использовать ее и за пределами HA

Пример:
```python
from noolite_api import NooliteSerial, dispatch_command, typing
import asyncio


async def test_callback(t: typing.NooliteRemote):
    print(f'Callback {t}')

nl = NooliteSerial(tty_name='test')
nl.reg_callback(1, test_callback)

async def main():
    nl.start_listen()
    nl.send_api('on', 1)

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

```
## Ethernet hub
Так же поддерживается работа с Ethernet-шлюзом PR1132 `https://www.noo.com.by/Ethernet_PR1132.html`
```python
from noolite_api import NooliteEthernet, dispatch_command
import asyncio


async def test_callback(t):
    print(f'Recieve sensors: {t}')


nl = NooliteEthernet(host='192.168.0.1', update_interval=30, cb_sensors=test_callback)


async def main():
    nl.start_listen()
    nl.send_api('on', 1)

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()

```