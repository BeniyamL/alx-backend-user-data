#!/usr/bin/env python3
"""DB module
"""
from tkinter.messagebox import NO
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        add_user - function to add a user
        Arguments:
            email: the given email
            hashed_password: the given hashed password
        Returns:
            the created user
        """
        new_usr = User(email=email, hashed_password=hashed_password)
        self._session.add(new_usr)
        self._session.commit()
        return new_usr

    def find_user_by(self, **kwargs) -> User:
        """
        find_user_by - a method to find a user
        Arguments:
            kwargs: key word based argument
        Return:
            the first row found in the users
        """
        if kwargs is None:
            raise InvalidRequestError
        key_cols = User.__table__.columns.keys()
        for k in kwargs.keys():
            if k not in key_cols:
                raise InvalidRequestError
        rqrd_usr = self._session.query(User).filter_by(**kwargs).first()
        if rqrd_usr is None:
            raise NoResultFound
        return rqrd_usr

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update_user - method to update the user
        Arguments:
            user_id - the given user id
        Returns:
            Nothing
        """
        if kwargs is None:
            return None
        rqrd_usr = self.find_user_by(id=user_id)
        key_cols = User.__table__.columns.keys()
        for k in kwargs:
            if k not in key_cols:
                raise ValueError

        for k, v in kwargs.items():
            setattr(rqrd_usr, k, v)

        self._session.commit()
