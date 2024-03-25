from typing import List

from wcferry import Wcf


class WeChatContactsBase:
    def __init__(self, wcf: Wcf):
        self.wcf = wcf
        self._counts = self.wcf.query_sql("MicroMsg.db", "SELECT COUNT(*) FROM Contact;")[0]["COUNT(*)"]
        self._offset = 10
        self._all_contacts = self.__get_all_contacts()

    def __get_all_contacts(self):
        """
        If accounts are too many, will cause wcf out of memory, get them by offsets
        """

        page = int(self._counts / self._offset)
        remains = self._counts % self._offset
        contacts = list()
        for i in range(page):
            contact = self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM Contact "
                                                        f"LIMIT {self._offset} "
                                                        f"OFFSET {i * self._offset};")
            contacts.extend(contact)
        contacts.extend(self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM Contact "
                                                          f"LIMIT {remains} "
                                                          f"OFFSET {page * self._offset};"))
        return contacts


class WeChatRoom:
    def __init__(self, room_code: str, room_name: str):
        """
        :param room_code: unique code for every chat room, e.g. 111111@chatroom
        :param room_name: the real name of the chat room
        """
        self.room_code = room_code
        self.room_name = room_name


class WeChatRooms(WeChatContactsBase):
    def __init__(self, wcf: Wcf):
        """
        Get all ChatRooms information
        :param wcf:
        """
        super().__init__(wcf=wcf)
        self.__chat_rooms = self.__load_chat_rooms()
        self.__room_code2room_name = {room.room_code: room.room_name for room in self.__chat_rooms}

    def __load_chat_rooms(self) -> List[WeChatRoom]:
        """
        Load all chat rooms into self
        :return: All chat rooms
        """
        chat_rooms = list()
        contacts = self._all_contacts
        for contact in contacts:
            if contact["ChatRoomNotify"] != 1:
                continue
            room_code = contact["UserName"]
            room_name = contact["NickName"]
            chat_rooms.append(WeChatRoom(room_code=room_code, room_name=room_name))
        return chat_rooms

    def get_chat_rooms(self) -> List[WeChatRoom]:
        """
        return all chat rooms, directly get self.__chat_rooms
        :return:
        """
        return self.__chat_rooms

    def from_room_id_to_room_name(self, room_id: str):
        """
        get room name from room id
        :param room_id:
        :return:
        """
        try:
            name = self.__room_code2room_name[room_id]
            return name
        except Exception as e:
            err = f"no rood name for room id :{room_id}"
            raise Exception(err)

    def update_chat_rooms(self):
        """
        update/fresh the chat rooms list
        :return:
        """
        self.__chat_rooms = self.__load_chat_rooms()
        self.__room_code2room_name = {room.room_code: room.room_name for room in self.__chat_rooms}


class WeChatContact:
    def __init__(self, contact_code: str, alias: str, nick_name: str, type_number: int):
        """
        :param contact_code: unique contact code
        :param alias: alias of contact
        :param nick_name: the nickname of a contact
        :param type_number: used for check if it's a friends or comes from a room
        """
        self.contact_code = contact_code
        self.alias = alias
        self.nick_name = nick_name
        self.is_friend = True if type_number == 3 else False


class WeChatContacts(WeChatContactsBase):
    def __init__(self, wcf: Wcf):
        """
        Get all contacts information, groups friends included
        :param wcf:
        """
        super().__init__(wcf=wcf)
        self.__contacts = self.__load_contacts()
        self.__wxid2wxname = {contact.contact_code: contact.nick_name for contact in self.__contacts}

    def __load_contacts(self) -> List[WeChatContact]:
        """
        load contacts to self
        :return: 
        """
        contacts_result = list()

        contacts = self._all_contacts
        for contact in contacts:
            type_number = contact["Type"]
            if type_number != 3 and type_number != 4:
                # type 0 -> friends, type 1 internal account, type 2 group
                continue
            contact_code = contact["UserName"]
            alias = contact["Alias"]
            nick_name = contact["NickName"]
            contacts_result.append(WeChatContact(contact_code=contact_code,
                                                 alias=alias,
                                                 nick_name=nick_name,
                                                 type_number=type_number))
        return contacts_result

    def get_contacts(self) -> List[WeChatContact]:
        """
        get contacts
        :return:
        """
        return self.__contacts

    def wxid2wxname(self, wxid: str):
        return self.__wxid2wxname[wxid]

    def update_contacts(self):
        """
        update contacts information
        :return:
        """
        self.__contacts = self.__load_contacts()
        self.__wxid2wxname = {contact.contact_code: contact.nick_name for contact in self.__contacts}


class ContactInfo:
    def __init__(self, wcf: Wcf):
        self.wcf = wcf
        table_name = "ChatRoom"
        counts: int = self.wcf.query_sql("MicroMsg.db", f"SELECT COUNT(*) FROM {table_name};")[0]["COUNT(*)"]
        offset = 1
        page = int(counts / offset)
        remains = counts % offset
        contacts = list()
        for i in range(page):
            contact = self.wcf.query_sql("MicroMsg.db",
                                         f"SELECT * FROM {table_name} LIMIT {offset} OFFSET {i * offset};")
            contacts.extend(contact)
        contacts.extend(
            self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM {table_name} LIMIT {remains} OFFSET {page * offset};"))
        ...

        contacts = self.wcf.query_sql("MicroMsg.db", "SELECT * FROM Contact;")
        chatroom = self.wcf.query_sql("MicroMsg.db", "SELECT * FROM ChatRoom;")

        dbs = []
        tables = []
        for db in self.wcf.get_dbs():
            [tables.append(table) for table in self.wcf.get_tables(db)]
        infos = dict()
        for table in tables:
            table_name = table["name"]
            if table_name in [
                "BizInfo",
                "BizProfileV2",
            ]:
                continue
            infos[table_name] = (self.wcf.query_sql("MicroMsg.db", f"SELECT * FROM {table_name}"))

if __name__ == "__main__":
    wcf = Wcf(debug=True)
    ContactInfo(wcf=wcf)
    rooms = WeChatRooms(wcf=wcf).get_chat_rooms()
    contacts = WeChatContacts(wcf=wcf).get_contacts()
    ...
