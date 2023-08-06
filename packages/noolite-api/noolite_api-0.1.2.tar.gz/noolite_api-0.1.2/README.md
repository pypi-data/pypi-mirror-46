# Noolite API integration
Интеграция устройств noolite в python, полностью асинхронная работа

## MTRF-64
Поддерживается отправка и прием команд на адаптер MTRF-64 `https://www.noo.com.by/mtrf-64.html` через serial-порт. Команды от 
адаптера перенаправляются в колбэк пользователя. Команду можно передать как есть, а так же если оформить
колбэк специальным декоратором, то передается готовый распарсеный объект нужного типа: (датчик температуры, датчик 
движения или обычные кнопки) 

Библиотека разрабатывалась для работы с  Нome-assistant, но никто не мешает использовать ее и за пределами HA

Пример:
```python
from noolite_api import NooliteSerial, dispatch_command
import asyncio


@dispatch_command
async def test_callback(t):
    print(t)


nl = NooliteSerial(tty_name='test', input_command_callback_method=test_callback)


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