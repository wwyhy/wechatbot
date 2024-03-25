import re
from datetime import datetime

from PluginClub.DataBase.club_activity import ClubActivityManager
from WeChatCore.wechat_bot import GLOBAL_CONTACTS, GLOBAL_ROOMS
from WeChatCore.wechat_message import WeChatMessage


class CommandRules:
    GROUP_MESSAGE_ALLOW = 0x01
    DIRECT_MESSAGE_ALLOW = 0x02
    EVERY_ONE_ALLOW = 0x04
    ADMIN_ALLOW = 0x08


class CommandBase:

    def __init__(self):
        self.command_head: str = ""
        self.command_rule: int = 0x00

    def parse_command(self, msg: WeChatMessage):
        raise NotImplementedError

    def is_command(self, msg: WeChatMessage):
        content = msg.content.lstrip()
        return content.startswith(self.command_head)

    @staticmethod
    def _parse_date_str(date_str: str):
        try:
            date_ = date_str.split("-")
            date_result = datetime(year=int(date_[0]), month=int(date_[1]), day=int(date_[2]))
            return date_result
        except Exception as e:
            raise Exception("Error in Date Parsing")

    @staticmethod
    def _extract_from_pattern(content: str, pattern: str) -> str:
        """
        should only have one group
        :param content:
        :param pattern:
        :return:
        """
        result = re.findall(pattern=pattern, string=content)
        if len(result) <= 0:
            error = f"Didn't matched pattern {pattern}"
            raise Exception(error)
        return result[0]


class ActivityCommandBase(CommandBase):
    TITLE_PATTERN = r"活动名称: \[(.*)\]"
    START_DATE_PATTERN = r"活动开始时间: \[(.*)\]"
    END_DATE_PATTERN = r"活动结束时间: \[(.*)\]"

    def __init__(self):
        super().__init__()

    def _parse_activity_title_pattern(self, string: str) -> str:
        title = self._extract_from_pattern(content=string, pattern=self.TITLE_PATTERN)
        return title

    def _parse_activity_start_datetime(self, string: str):
        start_date_str = self._extract_from_pattern(content=string, pattern=self.START_DATE_PATTERN)
        return self._parse_date_str(start_date_str)

    def _parse_activity_end_datetime(self, string: str):
        start_date_str = self._extract_from_pattern(content=string, pattern=self.END_DATE_PATTERN)
        end_date = self._parse_date_str(start_date_str)
        end_date = datetime(year=end_date.year, month=end_date.month, day=end_date.day,
                            hour=23, minute=59, second=59)
        return end_date


class NewActivityCommand(ActivityCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".发起活动"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | CommandRules.ADMIN_ALLOW

    def parse_command(self, msg: WeChatMessage):
        room_id = msg.roomid
        room_name = GLOBAL_ROOMS.from_room_id_to_room_name(room_id)
        title = self._parse_activity_title_pattern(msg.content)
        full_content = str(msg.content).replace(self.command_head, "").lstrip()
        organizer_id = msg.sender
        organizer_name = GLOBAL_CONTACTS.wxid2wxname(organizer_id)
        start_date = self._parse_activity_start_datetime(msg.content)
        end_date = self._parse_activity_end_datetime(msg.content)

        return ClubActivityManager.new_activity(room_id=room_id,
                                                room_name=room_name,
                                                title=title,
                                                full_content=full_content,
                                                organizer_id=organizer_id,
                                                organizer_name=organizer_name,
                                                start_date=start_date,
                                                end_date=end_date,
                                                )


class UpdateActivityCommand(ActivityCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".更新活动"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | CommandRules.ADMIN_ALLOW

    def parse_command(self, msg: WeChatMessage):
        room_id = msg.roomid
        room_name = GLOBAL_ROOMS.from_room_id_to_room_name(room_id)
        title = self._parse_activity_title_pattern(msg.content)
        full_content = str(msg.content).replace(self.command_head, "").lstrip()
        organizer_id = msg.sender
        organizer_name = GLOBAL_CONTACTS.wxid2wxname(organizer_id)
        start_date = self._parse_activity_start_datetime(msg.content)
        end_date = self._parse_activity_end_datetime(msg.content)

        return ClubActivityManager.update_activity(room_id=room_id,
                                                   room_name=room_name,
                                                   title=title,
                                                   full_content=full_content,
                                                   organizer_id=organizer_id,
                                                   organizer_name=organizer_name,
                                                   start_date=start_date,
                                                   end_date=end_date,
                                                   )


class CheckActivityCommand(ActivityCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".活动状态"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.ADMIN_ALLOW | \
                            CommandRules.DIRECT_MESSAGE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        title = self._parse_activity_title_pattern(msg.content)
        flag = 0x01 if msg.from_group() else 0x07  # in group show only name, direct show all
        return ClubActivityManager.show_activity_status(title=title, show_flag=flag)


class JoinActivityCommand(ActivityCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".打卡"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.EVERY_ONE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        title = self._parse_activity_title_pattern(msg.content)
        partici_id = msg.sender
        partici_name = GLOBAL_CONTACTS.wxid2wxname(partici_id)
        content = str(msg.content).replace(self.command_head, "").lstrip()
        return ClubActivityManager.new_participates(title=title,
                                                    partici_id=partici_id,
                                                    partici_name=partici_name,
                                                    content=content, )


if __name__ == "__main__":
    ...
#     import PluginClub.DataBase.club_db as db
#     import wcferry
#
#     db.table.create_tables()
#     wcf = wcferry.Wcf()
#     GLOBAL_ROOMS = WeChatRooms(wcf=wcf)
#     GLOBAL_CONTACTS = WeChatContacts(wcf=wcf)
#
#     msg = WeChatMessage(msg=wcferry.wcf_pb2.WxMsg())
#     msg.roomid = "44@chatroom"
#     msg.content="""
#     .发起活动
#     活动名称: [测试活动1]
#     活动开始时间: [2023-08-08]
#     活动结束时间: [2023-08-11]
#     任意内容
#     """
#     msg.sender = "wx"
#     print(NewActivityCommand().is_command(msg))
#     result = NewActivityCommand().parse_command(msg)
#
#     msg.content="""
#     .更新活动
#     活动名称: [测试活动1]
#     活动开始时间: [2023-08-08]
#     活动结束时间: [2023-08-13]
#     任意内容111
#     """
#     if UpdateActivityCommand().is_command(msg):
#         result = UpdateActivityCommand().parse_command(msg)
#     msg.content="""
#     .打卡
#     活动名称: [测试活动1]
#     活动开始时间: [2023-08-08]
#     活动结束时间: [2023-08-13]
#     任意内容111
#     """
#     if JoinActivityCommand().is_command(msg):
#         result = JoinActivityCommand().parse_command(msg)
#         ...
#     ...
#
