# Noolite API integration
Интеграция устройств noolite в python

# MTRF-64
Поддерживается отправка и прием команд на адаптер MTRF-64 через serial-порт. Команды от 
адаптера перенаправляются в колбэк пользователя. Команду можно передать как есть, а так же если оформить
колбэк специальным декоратором, то передается готовый распарсеный объект нужного типа: (датчик температуры, датчик 
движения или обычные кнопки) 

Библиотека разрабатывалась для работы с  Нome-assistant, но никто не мешает использовать ее и за пределами HA

Пример:
```python
from noolite_serial import NooliteSerial
import asyncio


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