from wcferry import Wcf

from PluginClub.club_command import CommandRules, \
    NewActivityCommand, UpdateActivityCommand, JoinActivityCommand, CheckActivityCommand
from PluginClub.club_plugin_config import club_config
from WeChatCore.wechat_bot import GLOBAL_WCF, GLOBAL_CONTACTS
from WeChatCore.wechat_message import WeChatMessage

command_list = [
    NewActivityCommand(),
    UpdateActivityCommand(),
    JoinActivityCommand(),
    CheckActivityCommand(),
]


class ClubMessageHandler:
    @staticmethod
    def on_group_message(wcf: Wcf, msg: WeChatMessage):
        room_id = msg.roomid
        sender_id = msg.sender
        # if is not activated group
        if not club_config.is_group_activated(room_id=room_id):
            return
        for command in command_list:
            # if is not a command
            if not command.is_command(msg):
                continue
            # if is not a group allowed command
            if not (command.command_rule & CommandRules.GROUP_MESSAGE_ALLOW):
                continue
            # if it's ad admin allowed command but sender is not an admin
            if command.command_rule & CommandRules.ADMIN_ALLOW and \
                    not club_config.is_account_manager(room_id=room_id, wxid=sender_id):
                continue
            try:
                new_message = command.parse_command(msg)
                GLOBAL_WCF.send_text(msg=f"@{GLOBAL_CONTACTS.wxid2wxname(sender_id)}\n{new_message}", receiver=room_id,
                                     aters=sender_id)
                return
            except Exception as e:
                new_message = str(e)
                GLOBAL_WCF.send_text(msg=f"@{GLOBAL_CONTACTS.wxid2wxname(sender_id)}\n{new_message}", receiver=room_id,
                                     aters=sender_id)
                return

    @staticmethod
    def on_direct_message(wcf: Wcf, msg: WeChatMessage):
        sender_id = msg.sender
        for command in command_list:
            # if is not a command
            if not command.is_command(msg):
                continue
            # if is not a direct allowed command
            if not (command.command_rule & CommandRules.DIRECT_MESSAGE_ALLOW):
                continue
            # if is admin allowed command but sender is not an admin
            if command.command_rule & CommandRules.ADMIN_ALLOW and \
                    not club_config.is_one_of_managers(wxid=sender_id):
                continue
            try:
                new_message = command.parse_command(msg)
                GLOBAL_WCF.send_text(msg=new_message, receiver=sender_id)
                return
            except Exception as e:
                new_message = str(e)
                GLOBAL_WCF.send_text(msg=new_message, receiver=sender_id)
