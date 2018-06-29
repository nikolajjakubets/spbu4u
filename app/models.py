# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app import db, new_functions as f
import spbu
from datetime import timedelta
from app.constants import week_off_answer, weekend_answer, emoji


users_groups = db.Table(
    "users_groups",
    db.Column("group_id", db.Integer, db.ForeignKey("groups.id"),
              primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"),
              primary_key=True)
)


users_added_lesson = db.Table(
    "users_added_lesson",
    db.Column("lesson", db.Integer, db.ForeignKey("lessons.id"),
              primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"),
              primary_key=True)
)


users_hidden_lessons = db.Table(
    "users_hidden_lessons",
    db.Column("lesson", db.Integer, db.ForeignKey("lessons.id"),
              primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"),
              primary_key=True)
)


users_chosen_educators = db.Table(
    "users_chosen_educators",
    db.Column("lesson", db.Integer, db.ForeignKey("lessons.id"),
              primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"),
              primary_key=True)
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    is_educator = db.Column(db.Boolean, default=False, nullable=False)
    is_full_place = db.Column(db.Boolean, default=True, nullable=False)
    is_subscribed = db.Column(db.Boolean, default=False, nullable=False)
    home_station_code = db.Column(db.String(10), default="c2", nullable=False)
    univer_station_code = db.Column(db.String(10), default="s9603770",
                                    nullable=False)
    current_group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    educator_id = db.Column(db.Integer, nullable=True)
    groups = db.relationship("Group", secondary=users_groups,
                             back_populates="members", lazy="dynamic")
    added_lessons = db.relationship("Lesson", secondary=users_added_lesson,
                                    lazy="dynamic")
    hidden_lessons = db.relationship("Lesson", secondary=users_hidden_lessons,
                                     lazy="dynamic")
    chosen_educators = db.relationship("Lesson",
                                       secondary=users_chosen_educators,
                                       lazy="dynamic")
    __current_group = db.relationship("Group")

    def __parse_event(self, event):
        # TODO delete hidden lessons
        return f.create_schedule_answer(event, self.is_full_place)

    def __parse_day_events(self, events):
        """
        This method parses the events data from SPBU API
        :param events: an element of `DayStudyEvents`
        :type events: dict
        :return: html safe string
        :rtype: str
        """
        answer = "{0} {1}\n\n".format(
            emoji["calendar"], events["DayString"].capitalize()
        )

        events = f.delete_cancelled_events(events["DayStudyEvents"])
        for event in events:
            answer += self.__parse_event(event)
        return answer

    def create_answer_for_date(self, date):
        """
        This method gets the schedule for date and parses it
        :param date: date for schedule
        :type date: datetime.date
        :return: html safe string
        :rtype: str
        """
        if self.is_educator:
            """
            In future:
            json_day_events = spbu.get_educator_events(self.current_group_id
                from_date=date, to_date=date + timedelta(days=1)  
            )["Days"]
            """
            json_day_events = []
        else:
            json_day_events = self.__current_group.get_events(
                from_date=date, to_date=date + timedelta(days=1)
            )["Days"]

        if len(json_day_events):
            answer = self.__parse_day_events(json_day_events[0])
        else:
            answer = weekend_answer

        return answer

    def create_answers_for_interval(self, from_date, to_date):
        """
        Method to create answers for interval
        :param from_date: the datetime the events start from
        :type from_date: datetime.date
        :param to_date: the datetime the events ends
        :type to_date: datetime.date
        :return: list of schedule answers
        :rtype: list of str
        """
        answers = []

        if self.is_educator:
            """
            In future:
            json_day_events = spbu.get_educator_events(self.current_group_id
                from_date=from_date, to_date=to_date  
            )["Days"]
            """
            json_day_events = []
        else:
            json_day_events = self.__current_group.get_events(
                from_date=from_date, to_date=to_date
            )["Days"]

        if len(json_day_events):
            for event in json_day_events:
                answers.append(self.__parse_day_events(event))
        else:
            answers.append(week_off_answer)

        return answers


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    members = db.relationship("User", secondary=users_groups,
                              back_populates="groups", lazy="dynamic")

    def get_events(self, from_date=None, to_date=None, lessons_type=None):
        return spbu.get_group_events(self.id, from_date, to_date, lessons_type)


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    types = db.Column(db.JSON)
    days = db.Column(db.JSON)
    times = db.Column(db.JSON)
    educators = db.Column(db.JSON)
    places = db.Column(db.JSON)

    @staticmethod
    def add_or_get(name, types, days, times, educators, places):
        """
        Так как из полей типа JSON сделать уникальный индекс нельзя, то
        приходится проверять наличие элемента в базе перед добавлением.
        Будет возвращен либо новый объект, либо уже существующий.
        """
        lesson = Lesson.query.filter_by(name=name, types=types, days=days,
                                        times=times, educators=educators,
                                        places=places).one_or_none()
        if not lesson:
            lesson = Lesson(name=name, types=types, days=days, times=times,
                            educators=educators, places=places)
        return lesson
