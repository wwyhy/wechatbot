#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import signal

from PluginClub.club_message_handler import ClubMessageHandler
from WeChatCore.wechat_bot import GLOBAL_WCF
from WeChatCore.wechat_bot import WechatBot
from WeChatCore.wechat_message_handler import WeChatMessageHandler


def main():
    def handler(sig, frame):
        GLOBAL_WCF.cleanup()  # cleanup before exit
        exit(0)

    signal.signal(signal.SIGINT, handler)

    # load plugin
    main_handler = WeChatMessageHandler()
    main_handler.register_direct_message_handler(ClubMessageHandler.on_direct_message)
    main_handler.register_normal_group_message_handler(ClubMessageHandler.on_group_message)

    bot = WechatBot(wcf=GLOBAL_WCF, handler=main_handler)
    bot.LOG.info("Bot Is Running")
    bot.wcf.send_text("Bot Is Running", "filehelper")

    # receive message
    bot.enableReceivingMsg()

    # time base tasks
    # bot.onEveryTime("07:00",bot.GLOBAL_WCF.send_text,msg="Test",receiver="xxxx")

    # keep robot running
    bot.keepRunningAndBlockProcess()


if __name__ == "__main__":
    main()
