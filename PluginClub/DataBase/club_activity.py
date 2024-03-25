from datetime import datetime, timedelta

import PluginClub.DataBase.club_db as db


class ClubActivityManager:

    @staticmethod
    def new_activity(room_id, room_name, title, full_content,
                     organizer_id, organizer_name,
                     start_date, end_date):
        """
        :param room_id: room id
        :param room_name: the name of room
        :param title: activity title
        :param full_content: full activity content
        :param organizer_id: the wxid of organizer
        :param organizer_name: the nickname of organizer
        :param start_date: type is datetime, the first day of activity
        :param end_date: type is datetime, the last day of activity
        :return:
        """
        try:
            # if activity already existed
            query = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == title)
            if len(query.all()) > 0:
                raise Exception("Error in update activity")
            # if didn't exist
            activity = db.ClubActivity(
                club_room_id=room_id,
                club_room_name=room_name,
                activity_title=title,
                activity_full_content=full_content,
                activity_organizer_id=organizer_id,
                activity_organizer_name=organizer_name,
                activity_create_date=datetime.now(),
                activity_start_date=start_date,
                activity_end_date=end_date,
            )
            db.table.session.add(activity)
            db.table.session.commit()
            result_content = f"Activity {title} Added"
            return result_content
        except Exception as e:
            raise Exception("Error in update activity")

    @staticmethod
    def update_activity(room_id, room_name, title, full_content,
                        organizer_id, organizer_name,
                        start_date, end_date):
        """
        :param room_id: room id
        :param room_name: the name of room
        :param full_content: full activity content
        :param title: activity title
        :param organizer_id: the wxid of organizer
        :param organizer_name: the nickname of organizer
        :param start_date: type is datetime, the first day of activity
        :param end_date: type is datetime, the last day of activity
        :return:
        """
        try:
            # if activity already existed,update it
            query = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == title)
            if len(query.all()) <= 0:
                error_message = f"Error in update activity, No such title {title}"
                raise Exception(error_message)
            query.update({
                db.ClubActivity.club_room_id: room_id,
                db.ClubActivity.club_room_name: room_name,
                db.ClubActivity.activity_full_content: full_content,
                db.ClubActivity.activity_organizer_id: organizer_id,
                db.ClubActivity.activity_organizer_name: organizer_name,
                db.ClubActivity.activity_create_date: datetime.now(),
                db.ClubActivity.activity_start_date: start_date,
                db.ClubActivity.activity_end_date: end_date,
            })
            db.table.session.commit()
            result_content = f"Activity {title} updated"
            return result_content
        except Exception as e:
            raise Exception("Error in update activity")

    @staticmethod
    def new_participates(title, partici_id, partici_name, content):
        """
        :param title: activity title
        :param partici_id: the participated wxid
        :param partici_name: the participated  nickname
        :param content: the activity participation content
        :return:
        """
        try:
            # check title correct
            existed = db.table.session.query(db.ClubActivity, ). \
                filter(db.ClubActivity.activity_title == title).all()
            if not existed:
                raise Exception("Error in new participates")
            # get activity id from title
            activity_id = existed[0].activity_id
            # get end datetime from title
            activity_end_date = existed[0].activity_end_date
            if datetime.now() > activity_end_date:
                raise Exception("Error in new participates")
            participates = db.ClubActivityFlow(
                activity_flow_content=content,
                activity_id=activity_id,
                activity_participates_id=partici_id,
                activity_participates_name=partici_name,
                activity_flow_creat_date=datetime.now(),
            )
            db.table.session.add(participates)
            db.table.session.commit()
            result_content = f"Activity {title} Joined"
            return result_content
        except Exception as e:
            raise Exception("Error in new participates")

    @staticmethod
    def show_activity_status(title, show_flag: int = 1):
        """
        :param title:
        :param show_flag, 1-> name, 2-> date, 4-> content, 8(TODO)-> name,date,content,points change
        :return:
        """
        try:
            existed = db.table.session.query(db.ClubActivity, ). \
                filter(db.ClubActivity.activity_title == title).first()
            activity_id = existed.activity_id
            if not existed:
                raise Exception("Error in show activity status")
            existed = db.table.session.query(db.ClubActivityFlow). \
                filter(db.ClubActivityFlow.activity_id == activity_id).all()
            if not existed:
                raise Exception("Error in show activity status")
            result = f"\nActivity Title:{title}"
            for flow in existed:
                result += "\n"
                if show_flag & 1:  # name
                    result += f"nickname:{flow.activity_participates_name}"
                if show_flag & 2:  # date
                    result += f"\ndate:{flow.activity_flow_creat_date}"
                if show_flag & 4:  # content
                    result += f"\ncontent:\n[{flow.activity_flow_content}]"
            return result
        except Exception as e:
            raise Exception("Error in show activity status")


if __name__ == "__main__":
    db.table.create_tables()
    room_id = "123@chatroom"
    room_name = "test room"
    title = "Activity01"
    organizer_id = "wxid001"
    organizer_name = "001"
    full_content = "aa" * 100
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=3)

    # test new activity
    result = ClubActivityManager.new_activity(room_id=room_id,
                                              room_name=room_name,
                                              title=title,
                                              full_content=full_content,
                                              organizer_id=organizer_id,
                                              organizer_name=organizer_name,
                                              start_date=start_date,
                                              end_date=end_date)
    print(result)
    end_date = datetime.now() + timedelta(days=4)

    # test update activity
    result = ClubActivityManager.update_activity(room_id=room_id,
                                                 room_name=room_name,
                                                 title=title,
                                                 full_content=full_content,
                                                 organizer_id=organizer_id,
                                                 organizer_name=organizer_name,
                                                 start_date=start_date,
                                                 end_date=end_date)
    print(result)

    # test update wrong activity
    try:
        result = ClubActivityManager.update_activity(room_id=room_id,
                                                     room_name=room_name,
                                                     title=title + "1",
                                                     full_content=full_content,
                                                     organizer_id=organizer_id,
                                                     organizer_name=organizer_name,
                                                     start_date=start_date,
                                                     end_date=end_date)
        print(result)
    except Exception as e:
        print(e)

    # test join activity
    for i in range(10):
        partici_id = f"wxid00{i}"
        partici_name = f"00{i}"
        content = "test Content \n" * (i + 1)

        result = ClubActivityManager.new_participates(title=title,
                                                      partici_id=partici_id,
                                                      partici_name=partici_name,
                                                      content=content
                                                      )
        print(result)
        ...
    # test join wrong activity

    try:
        i = 99
        partici_id = f"wxid00{i}"
        partici_name = f"00{i}"
        content = "test Content \n"

        result = ClubActivityManager.new_participates(title=title + "0",
                                                      partici_id=partici_id,
                                                      partici_name=partici_name,
                                                      content=content
                                                      )
        print(result)
    except Exception as e:
        print(e)

    result = ClubActivityManager.show_activity_status(title=title, show_flag=1)
    result = ClubActivityManager.show_activity_status(title=title, show_flag=1)
    print(result)
    result = ClubActivityManager.show_activity_status(title=title, show_flag=3)
    print(result)
    result = ClubActivityManager.show_activity_status(title=title, show_flag=7)
    print(result)
