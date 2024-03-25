import logging.config
import os
import shutil
from typing import List

import yaml


class ConfigGroup:
    def __init__(self, room_id: str, managers: List[str]):
        """
        Config Groups
        :param room_id:
        :param managers:
        """
        self.room_id = room_id
        self.managers = managers

    def is_manager(self, account: str) -> bool:
        """
        judge if an account is a manager of this group
        :return:
        """
        if account in self.managers:
            return True
        return False


class ClubPluginConfig(object):
    def __init__(self) -> None:
        self.update_config()

    def _load_config(self) -> dict:
        pwd = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(f"{pwd}/config.yaml", "rb") as fp:
                yconfig = yaml.safe_load(fp)
                return yconfig
        except FileNotFoundError:
            shutil.copyfile(f"{pwd}/config.yaml.template", f"{pwd}/config.yaml")
            with open(f"{pwd}/config.yaml", "rb") as fp:
                yconfig = yaml.safe_load(fp)
                return config

    def is_group_activated(self, room_id: str):
        for room in self.groups:
            if room_id == room.room_id:
                return True
        return False

    def is_account_manager(self, room_id: str, wxid: str):
        for room in self.groups:
            if room_id != room.room_id:
                continue
            if wxid in room.managers:
                return True
            else:
                return False
        return False

    def is_one_of_managers(self, wxid: str):
        for room in self.groups:
            if wxid in room.managers:
                return True
            else:
                return False
        return False

    def update_config(self):
        yconfig = self._load_config()
        logging.config.dictConfig(yconfig["logging"])

        self.groups = [ConfigGroup(room_id=room_id, managers=yconfig["club_activate_groups"][room_id])
                       for room_id in yconfig["club_activate_groups"]]


club_config = ClubPluginConfig()

if __name__ == "__main__":
    config = ClubPluginConfig()
    print(config.is_group_activated(room_id="Abbbbb@chatroom"))  # True
    print(config.is_group_activated(room_id="Bbbbbb@chatroom"))  # False
    print(config.is_account_manager(room_id="Abbbbb@chatroom", wxid="bbbb"))  # True
    print(config.is_account_manager(room_id="Abbbbb@chatroom", wxid="eeee"))  # False
    print(config.is_account_manager(room_id="Abbbbb@chatroom", wxid="ffff"))  # False
