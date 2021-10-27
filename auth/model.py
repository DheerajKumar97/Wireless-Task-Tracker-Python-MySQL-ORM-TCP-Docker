from sqlalchemy import MetaData, Table, Column, Integer, String
import datetime
# import os

class WirelessToDoUser:

    Meta = MetaData()
    user = Table(
        'user', Meta,
        Column('userId', Integer, primary_key=True),
        Column('userLogo', String),
        Column('userName', String),
        Column('password', String),
        Column('firstName', String),
        Column('lastName', String),
        Column('emailId', String),
        Column('mobileNo', String),
        Column('policy', String),
    )


class WirelessToDoUserSession:

    Meta = MetaData()
    user_session = Table(
        'user_session', Meta,
        Column('userId', Integer, primary_key=True),
        Column('token', String),
        Column('mfaCode', String),
        Column('user_Agent', String),
    )