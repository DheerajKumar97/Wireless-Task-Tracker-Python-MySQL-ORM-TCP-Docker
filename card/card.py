from db import engine
from . import model
from flask import request
from sqlalchemy import update, delete
from sqlalchemy.sql import select, func
from sqlalchemy.dialects.mysql.dml import Insert
import validator as validator
from auth import model as auth_model
import os
import mail
from dotenv import load_dotenv
from random import randint
import timeit


_ENV_PATH = './config.env'
load_dotenv(dotenv_path=_ENV_PATH)


async def create_card_(json_dict):

    """

    Method Name  : create_card
    Parameters   : {"cardName":Name ,"cardContent": Content}

    This function will create card in Task Tracker with
    Card Description and Card Content and in Backend with
    unique Card Uid

    By default Card Status will get updated as [Created] with
    Card Id , Card Uid and Card Content


     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 2.2                ##
     ##   Revisions: 2                ##
     ###################################

    """
    __start_timer__ = timeit.default_timer()
    _updated_card_details_ = {'cardUid': str(int(await __random_card_uid(8), 16))}

    if 'cardName' in json_dict:
        _updated_card_details_['cardName'] = str(json_dict['cardName'])
    if 'cardContent' in json_dict:
        _updated_card_details_['cardContent'] = str(json_dict['cardContent'])

    connection = engine.connect()
    _insert_card_details = Insert(model.WirelessCardModel.card).values(_updated_card_details_)
    connection.execute(_insert_card_details)

    _last_inserted_record_in_card = select([model.WirelessCardModel.card.c.cardId, model.WirelessCardModel.card.c.cardUid]).order_by(
        model.WirelessCardModel.card.c.cardId.desc()).limit(1)
    _select_query_result = connection.execute(_last_inserted_record_in_card)
    _selected_last_record = list(_select_query_result)
    _last_record = [item for sublist in _selected_last_record for item in sublist]
    if not _last_record == [] and _updated_card_details_['cardUid'] in _last_record:
        update_status = await update_card_status_(
            {"cardId": _last_record[0], "cardUid": _updated_card_details_['cardUid'], "cardStatus": "created",
             "cardAssociated": False})

        if update_status['status'] == "success":
            _updated_card_details_['cardId'] = _last_record[0]
            _successful_response = {"response": {"card": _updated_card_details_}, "status": "success",
                        "message": "card successfully created"}
            __stop_timer__ = timeit.default_timer()
            __time_taken__ = __stop_timer__ - __start_timer__
            _successful_response['request time'] = str(__time_taken__)
            return _successful_response
        else:
            await delete_card_({"cardId": _last_record[0]})
            _failure_response = {"status": "error",
                        "message": "card creation failed"}
            return _failure_response



async def update_card_status_(json_dict):

    """

    Method Name  : update_card_status
    Parameters   : {"cardId": Id, "cardUid": UniqueId, "cardStatus": Card Status,
             "cardAssociated": True or False}

    This function will update Card Status and called inside
    the method {create_card}

    By default Card Status will get updated as [Created] with
    Card Id , Card Uid and Card Content


     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 2.0                ##
     ##   Revisions: 2                ##
     ###################################

    """

    _updated_card_status_ = {}

    if 'cardId' in json_dict:
        _updated_card_status_['cardId'] = str(json_dict['cardId'])
    if 'cardUid' in json_dict:
        _updated_card_status_['cardUid'] = str(json_dict['cardUid'])
    if 'cardStatus' in json_dict:
        _updated_card_status_['cardStatus'] = str(json_dict['cardStatus'])
    if 'cardAssociated' in json_dict:
        _updated_card_status_['cardAssociated'] = bool(json_dict['cardAssociated'])

    connection = engine.connect()
    _insert_card_status = Insert(model.WirelessCardStatus.card_status).values(_updated_card_status_)
    connection.execute(_insert_card_status)
    _card_status_response = {"response": {"card_status": _updated_card_status_}, "status": "success", "message": "card_status updated"}
    return _card_status_response


async def delete_card_(json_dict):

    """

    Method Name  : delete_card
    Parameters   : {"cardId": Id}

    This function will called inside
    the method {create_card} and delete the Card

    By default Card Status will get updated as [Deleted] with
    Card Id , Card Uid and Card Content


     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 1.0                ##
     ##   Revisions: 1                ##
     ###################################

    """

    _updated_delete_values_ = {}

    if 'cardId' in json_dict:
        _updated_delete_values_['cardId'] = str(json_dict['cardId'])
    if 'cardName' in json_dict:
        _updated_delete_values_['cardName'] = str(json_dict['cardName'])


    if 'queueCommand' in json_dict:

        connection = engine.connect()
        if not 'cardName' in _updated_delete_values_:

            print("No cardName")
            _delete_card_details = delete(model.WirelessCardModel.card).where(
                model.WirelessCardModel.card.c.cardId == _updated_delete_values_['cardId']
            )
            connection.execute(_delete_card_details)
        elif 'cardName' in _updated_delete_values_:

            print("cardName is there")
            _delete_card_details_ = delete(model.WirelessCardModel.card).where(
                model.WirelessCardModel.card.c.cardId == _updated_delete_values_['cardId'],
                model.WirelessCardModel.card.c.cardName == _updated_delete_values_['cardName']
            )
            connection.execute(_delete_card_details_)

        _select__cardid_and__userid_ = select([model.WirelessUserCardAssociation.user_card.c.cardId,
                            model.WirelessUserCardAssociation.user_card.c.userId]).where(
            model.WirelessUserCardAssociation.user_card.c.cardId == _updated_delete_values_['cardId'])
        _select_query_result = connection.execute(_select__cardid_and__userid_)
        _select_query_data = list(_select_query_result)
        _cardid_userid_data_ = [list(item) for item in _select_query_data]

        __user_id = []
        for id in _cardid_userid_data_:
            __user_id.append(str(id[1]))
        _user_id_ = [int(id) for id in __user_id]

        __user_list = []
        for user_id in _user_id_:
            _sql_user_details = select([auth_model.WirelessToDoUser.user.c.userId, auth_model.WirelessToDoUser.user.c.firstName,
                                auth_model.WirelessToDoUser.user.c.emailId]).where(
                auth_model.WirelessToDoUser.user.c.userId == user_id)
            _user_details_result = connection.execute(_sql_user_details)
            _user_details_data = list(_user_details_result)
            _user_data = [item for sublist in _user_details_data for item in sublist]
            __user_list.append(_user_data)

        __mail_list = []
        for user_detail in __user_list:
            if not user_detail[2] is None:
                __mail_list.append(user_detail)

        for email in __mail_list:
            await mail.send_card_edit_mail(os.environ.get("email_id"), email[2],
                                           os.environ.get("email_password"), email[1], _updated_delete_values_['cardName'],"delete")
    elif not 'queueCommand' in json_dict:

        print("No queueCommand")
        connection = engine.connect()
        if not 'cardName' in _updated_delete_values_:

            print("No cardName")
            _delete_with_cardid = delete(model.WirelessCardModel.card).where(
                model.WirelessCardModel.card.c.cardId == _updated_delete_values_['cardId']
            )
            connection.execute(_delete_with_cardid)
        elif 'cardName' in _updated_delete_values_:

            print("cardName is there")
            _delete_with_card_id_and__name = delete(model.WirelessCardModel.card).where(
                model.WirelessCardModel.card.c.cardId == _updated_delete_values_['cardId'],
                model.WirelessCardModel.card.c.cardName == _updated_delete_values_['cardName']
            )
            connection.execute(_delete_with_card_id_and__name)

    _successful_deletion_response = {"response": {"cardId": _updated_delete_values_['cardId']}, "status": "success",
                "message": "cardId {} deleted successfully".format(_updated_delete_values_['cardId'])}
    return _successful_deletion_response


async def edit_card_(json_dict):

    """

    Method Name  : edit_card
    Parameters   : {"cardId": Id, "cardName": Name,"cardContent": Content}

    This function will edit the details of the card
    in Task Tracker like Card Description and Card Content

    By default Card Status will get updated as [Modified] with
    Card Id , Card Uid , Card Description and Card Content

    Modify notification mails were generated and send to the
    user with respect to the details of the modification


     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 2.0                ##
     ##   Revisions: 2                ##
     ###################################

    """


    _updated_edit_card_details = {}

    if 'cardId' in json_dict:
        _updated_edit_card_details['cardId'] = str(json_dict['cardId'])
    if 'cardName' in json_dict:
        _updated_edit_card_details['cardName'] = str(json_dict['cardName'])
    if 'cardContent' in json_dict:
        _updated_edit_card_details['cardContent'] = str(json_dict['cardContent'])

    connection = engine.connect()
    edit_card_query_ = update(model.WirelessCardModel.card).where(
        model.WirelessCardModel.card.c.cardId == _updated_edit_card_details['cardId']).values(_updated_edit_card_details)
    connection.execute(edit_card_query_)

    select__card_id_and__user_id_ = select([model.WirelessUserCardAssociation.user_card.c.cardId, model.WirelessUserCardAssociation.user_card.c.userId]).where(model.WirelessUserCardAssociation.user_card.c.cardId == updated_values['cardId'])
    _select_query_result = connection.execute(select__card_id_and__user_id_)
    _select_query_data = list(_select_query_result)
    _query_data_ = [list(item) for item in _select_query_data]

    __user_id = []
    for id in _query_data_:
        __user_id.append(str(id[1]))
    _user_id_ = [int(id) for id in __user_id]

    __user_list = []
    for user_id in _user_id_:
        select_user_details__ = select([auth_model.WirelessToDoUser.user.c.userId,auth_model.WirelessToDoUser.user.c.firstName,
                            auth_model.WirelessToDoUser.user.c.emailId]).where(
            auth_model.WirelessToDoUser.user.c.userId == user_id)
        _select_query_result_ = connection.execute(select_user_details__)
        _select_query_data_ = list(_select_query_result_)
        user__data = [item for sublist in _select_query_data_ for item in sublist]
        __user_list.append(user__data)

    __mail_list = []
    for user_detail in __user_list:
        if not user_detail[2] is None:
            __mail_list.append(user_detail)

    for email in __mail_list:
        await mail.send_card_edit_mail(os.environ.get("email_id"), email[2],
                                              os.environ.get("email_password"), email[1],_updated_edit_card_details['cardName'],"edit")
    response = {"response": {"cardId": _updated_edit_card_details['cardId']}, "status": "success",
                "message": "cardId {} edited successfully".format(_updated_edit_card_details['cardId'])}
    return response


async def user_card_Association_(json_dict):

    """

    Method Name  : user_card_Association
    Parameters   : {"cardId": Id, "userId": Id}

    This function will Associate or assign the card with
    the specific user to track the user task
    assigned to him.

    Once card associated with user, notification mails
    will be generated to appropriate user emailId which is
    already stored in database.


     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 3.0                ##
     ##   Revisions: 3                ##
     ###################################

    """

    if 'cardId' and 'userId' in json_dict and await __check_card_id__(json_dict['cardId']) is True and await __check_user_id__(
            json_dict['userId']) is True:

        __updated_association_values = {'cardId': str(json_dict['cardId']), 'userId': str(json_dict['userId'])}
        card_content = await __get_card_content_for_id__(__updated_association_values['cardId'])
        __updated_association_values['cardContent'] = str(card_content)

        connection = engine.connect()
        query = Insert(model.WirelessUserCardAssociation.user_card).values(__updated_association_values)
        result = connection.execute(query)
        response = {"response": {"cardId": __updated_association_values['cardId'], "userId": __updated_association_values['userId']},
                    "status": "success",
                    "message": "cardId {} Associated successfully".format(__updated_association_values['cardId'])}

        if response['status']== "success":

            token = request.headers.get('token')
            _current_user_ = await __get_user_id__(token)

            _get_user_details = select(
                [auth_model.WirelessToDoUser.user.c.emailId, auth_model.WirelessToDoUser.user.c.firstName]).where(
                auth_model.WirelessToDoUser.user.c.userId == json_dict['userId'])
            _select_query_result = connection.execute(_get_user_details)
            _select_query_data = list(_select_query_result)
            _query_data = [item for sublist in _select_query_data for item in sublist]
            cardName = await __get_card_name__(__updated_association_values['cardId'])
            print("Arguments",os.environ.get("email_id"), _query_data[0],_query_data[1], cardName,
                                                 __updated_association_values['cardContent'])
            await mail.aws_send_cardAssociation_mail(os.environ.get("email_id"), _query_data[0],_query_data[1], cardName,
                                                 __updated_association_values['cardContent'])
            return response
        else:
            response = {"response":{},"status":"error","message":"edit card is not successfull"}
            return response
    else:
        raise validator.userId_or_cardId_is_Null()


async def __get_card_content_for_id__(cardid):

    connection = engine.connect()
    get_query = select([model.WirelessCardModel.card.c.cardContent]).where(
        model.WirelessCardModel.card.c.cardId == cardid)
    sql_query_result = connection.execute(get_query)
    sql_query_data = list(sql_query_result)
    query_data = [item for sublist in sql_query_data for item in sublist]
    if not query_data == []:
        return query_data[0]


async def __check_card_id__(cardid):

    connection = engine.connect()
    get_query = select([model.WirelessCardModel.card.c.cardId])
    sql_query_result = connection.execute(get_query)
    sql_query_data = list(sql_query_result)
    query_data = [item for sublist in sql_query_data for item in sublist]
    if cardid in query_data:
        return True
    else:
        raise validator.InvalidCardId()


async def __check_user_id__(userid):

    connection = engine.connect()
    get_query = select([auth_model.WirelessToDoUser.user.c.userId])
    sql_query_result = connection.execute(get_query)
    sql_query_data = list(sql_query_result)
    query_data = [item for sublist in sql_query_data for item in sublist]
    if userid in query_data:
        return True
    else:
        raise validator.InvalidUserId()


async def __random_card_uid(n):

    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    dec_val = randint(range_start, range_end)
    if len(hex(dec_val)) > 8:
        return hex(dec_val)[2:8]


async def __get_user_id__(token):

    userId_query = select([auth_model.WirelessToDoUserSession.user_session]).where(
        auth_model.WirelessToDoUserSession.user_session.c.token == token)
    connection = engine.connect()
    sql_query_result = connection.execute(userId_query)
    sql_query_data = list(sql_query_result)
    query_data = [item for sublist in sql_query_data for item in sublist]
    if not query_data == []:
        return query_data[0]


async def __get_card_name__(cardid):

    connection = engine.connect()
    get_query = select([model.WirelessCardModel.card.c.cardName]).where(model.WirelessCardModel.card.c.cardId == cardid)
    sql_query_result = connection.execute(get_query)
    sql_query_data = list(sql_query_result)
    query_data = [item for sublist in sql_query_data for item in sublist]
    if not query_data == []:
        return query_data[0]
