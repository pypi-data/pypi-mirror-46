from .typing import NooliteCommand
from .const import api_commands
import asyncio


class NooliteBase(object):

    async def send_command(self, command: NooliteCommand):
        raise NotImplementedError

    def send_api(self, cmd_name, ch, br=0, **kwargs):
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
        asyncio.ensure_future(self.send_command(NooliteCommand(cmd = api_commands[cmd_name], ch=ch, **kwargs)))

