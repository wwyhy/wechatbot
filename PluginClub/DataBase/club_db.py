from pathlib import Path

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session

Base = declarative_base()


class ClubActivity(Base):
    __tablename__ = "ClubActivity"
    activity_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    club_room_id = Column(String(50))
    club_room_name = Column(String(512))
    activity_title = Column(String(1024), unique=True)
    activity_full_content = Column(String(1024 * 100))
    activity_organizer_id = Column(String(100))
    activity_organizer_name = Column(String(100))
    activity_create_date = Column(DateTime)
    activity_regis_start_date = Column(DateTime)
    activity_regis_end_date = Column(DateTime)
    activity_start_date = Column(DateTime)
    activity_end_date = Column(DateTime)
    activity_place = Column(String(512))
    activity_planed_people = Column(Integer)
    activity_candidate = Column(Integer)
    activity_point_budget = Column(Integer)
    activity_consumed_budget = Column(Integer)


class ClubActivityFlow(Base):
    __tablename__ = "ClubActivityFlow"
    activity_flow_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    activity_flow_content = Column(String(1024 * 100))
    activity_id = Column(Integer, ForeignKey("ClubActivity.activity_id"))
    activity_participates_id = Column(String(1024))
    activity_participates_name = Column(String(1024))
    bonus_point_flow_id = Column(Integer)
    activity_flow_creat_date = Column(DateTime)

    activity = relationship("ClubActivity", backref="ClubActivityFlow")


class BonusPoint(Base):
    __tablename__ = "BonusPoint"
    bonus_point_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    club_room_id = Column(String(50))
    club_member_id = Column(String(50))
    bonus_points = Column(Integer)
    last_changed_flow_id = Column(Integer)


class BonusPointFlow(Base):
    __tablename__ = "BonusPointFlow"
    bonus_flow_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    club_room_id = Column(String(50))
    bonus_flow_type = Column(Integer)  # 0->increase , 1->decrease, 2-> force update
    operator_id = Column(String(50))
    activity_flow_id = Column(Integer)
    previous_point = Column(Integer)
    current_point = Column(Integer)
    bonus_flow_comments = Column(String(1024))


class TableManager:
    def __init__(self):
        self.db_path = Path("club.db")
        self.engine = create_engine('sqlite:///club.db', echo=True,
                                    max_overflow=0,
                                    pool_size=5,
                                    pool_timeout=10,
                                    pool_recycle=1)

        if not self.db_path.exists():
            self.create_tables()
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def create_tables(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)


table = TableManager()
