import logging
import time
from queue import Empty
from threading import Thread

from wcferry import Wcf

# from wechat_contact_info import WeChatContact, WeChatContacts, WeChatRoom, WeChatRooms
from WeChatCore.wechat_contact_info import WeChatContacts, WeChatRooms
from WeChatCore.wechat_job_mgmt import Job
from WeChatCore.wechat_message_handler import WeChatMessageHandler

GLOBAL_WCF = Wcf(debug=True)
GLOBAL_ROOMS = WeChatRooms(GLOBAL_WCF)
GLOBAL_CONTACTS = WeChatContacts(GLOBAL_WCF)


class WechatBot(Job):

    def __init__(self, wcf: Wcf, handler: WeChatMessageHandler) -> None:
        self.wcf = wcf
        self.LOG = logging.getLogger("Robot")
        self.wxid = self.wcf.get_self_wxid()
        self.msg_handler = handler
        self.rooms = WeChatRooms(wcf=wcf)
        self.contacts = WeChatContacts(wcf=wcf)

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    self.LOG.info(msg)
                    self.msg_handler.on_message(wcf, msg)
                except Empty:
                    continue  # Empty message
                except Exception as e:
                    self.LOG.error(f"Receiving message error: {e}")

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()

    def keepRunningAndBlockProcess(self) -> None:
        """
        Keep Robot running
        """
        while True:
            self.runPendingJobs()
            time.sleep(1)


if __name__ == "__main__":
    wcf = Wcf()
    contacts = WeChatContacts(wcf)
    wcf.send_text(msg=f"@{contacts.wxid2wxname('wxid_')} \n\n123",
                  receiver="445@chatroom",
                  aters="wxid_d")
    wcf.send_text(msg="wxid_d75", receiver="wxid_d75")
    wcf.send_text(msg="a", receiver="445@chatroom")
    xml_template = """ <xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>12345678</CreateTime>
 <MsgType><![CDATA[news]]></MsgType>
 <ArticleCount>2</ArticleCount>
 <Articles>
 <item>
 <Title><![CDATA[title1]]></Title> 
 <Description><![CDATA[description1]]></Description>
 <PicUrl><![CDATA[picurl]]></PicUrl>
 <Url><![CDATA[url]]></Url>
 </item>
 <item>
 <Title><![CDATA[title]]></Title>
 <Description><![CDATA[description]]></Description>
 <PicUrl><![CDATA[picurl]]></PicUrl>
 <Url><![CDATA[url]]></Url>
 </item>
 </Articles>
 </xml> """
    wcf.send_xml(receiver="wxid_d7", xml=xml_template, type=0x12)
