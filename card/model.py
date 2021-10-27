from sqlalchemy import MetaData, Table, Column, Text, Enum, Boolean, BLOB, Integer, DateTime, func
# import os



class WirelessCardModel:

    Meta = MetaData()
    card = Table(
        'card', Meta,
        Column('cardId', nullable=False, primary_key=True),
        Column('cardUid', Text),
        Column('cardName', Text),
        Column('cardContent', Text),
        Column('controllerName', Text),
        Column('dt_stamp', DateTime(timezone=True), onupdate=func.now()),
    )


class WirelessCardStatus:

    CardStatusMeta = MetaData()
    card_status = Table(
        'card_status', CardStatusMeta,
        Column('cardId', Text),
        Column('cardUid', Text),
        Column('cardStatus', Text),
        Column('cardAssociated', Text),
        Column('dt_stamp', DateTime(timezone=True), onupdate=func.now()),
    )


class WirelessUserCardAssociation:

    CardStatusMeta = MetaData()
    user_card = Table(
        'user_card', CardStatusMeta,
        Column('cardId', Text),
        Column('userId', Text),
        Column('cardContent', Text),
        Column('dt_stamp', DateTime(timezone=True), onupdate=func.now()),
    )