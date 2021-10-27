from flask import Flask, request, Response
from db import engine
from sqlalchemy.dialects.mysql.dml import Insert
from sqlalchemy.sql import select
from sqlalchemy import delete,update
from flask_httpauth import HTTPTokenAuth
from dotenv import load_dotenv
from . import model
import validator
import hashlib
import sys
import traceback
import string
import random
import json
import time
import logging
import os
import mail
import timeit
import base64


_ENV_PATH = './config.env'
load_dotenv(dotenv_path=_ENV_PATH)

_ENV_PATH_ = './mfaCode.env'
load_dotenv(dotenv_path=_ENV_PATH_)


_portal_dns = os.environ.get("portalDNS")


app = Flask(__name__)
token_auth = HTTPTokenAuth(scheme='Bearer', header='token')


@token_auth.verify_token
def _verify_Bearer_token(token):

    query = select([model.WirelessToDoUserSession.user_session]).where(
        model.WirelessToDoUserSession.user_session.c.token == token)
    result = engine.execute(query)
    if result.rowcount > 0:
        return result.first()
    else:
        return False


@token_auth.error_handler
def _auth_error():
    try:
        raise validator.InvalidAuthentication()
    except:
        error_class = validator.get_ErrorClass(sys.exc_info())
        error_code = validator.__get_error_code__(error_class)
        response = {"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.info(response)
            response = Response(json.dumps(response))
            response.mimetype = 'application/json'
            return response
        else:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            response = {'response': {"message": error_class + str(" has been occurred"),
                                     "error": json.loads(json.dumps(str(sys.exc_info()[0:2]))) + " error line = " + str(
                                         exc_tb.tb_lineno),
                                     'error_code': 'ER_UNK025'}, "status": "error"}
            logging.exception(str(traceback.TracebackException(exc_type, exc_obj, exc_tb)))
            logging.info(response)
            response = Response(json.dumps(response))
            response.mimetype = 'application/json'
            return response


async def create_user_(json_dict):

    """

    Method Name  : create_user

    Parameters   : {"userName": Name,"password": password,"firstName":Name,"lastName":Name,"emailId": Mail}

    This function will create the details of the user
    in access the software by logging in. The details of the
    user will be stored in database.
    Separate function has been implemented for adding
    the user logo to the user as image and it will
    convert to base64 image format and store it in database

     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 2.0                ##
     ##   Revisions: 2                ##
     ###################################

    """

    start = timeit.default_timer()
    update_values = {}

    if 'userName' in json_dict:
        update_values['userName'] = str(json_dict['userName'])

    hashed_json_password = hashlib.pbkdf2_hmac('sha512', bytes(json_dict['password'], 'utf-8'),
                                               bytes(os.environ.get("salt"), 'utf-8'),
                                               int(os.environ.get("iterations"))).hex()
    if 'password' in json_dict:
        update_values['password'] = str(hashed_json_password)
    if 'firstName' in json_dict:
        update_values['firstName'] = str(json_dict['firstName'])
    if 'lastName' in json_dict:
        update_values['lastName'] = str(json_dict['lastName'])
    if 'emailId' in json_dict:
        update_values['emailId'] = str(json_dict['emailId'])

    if 'mobileNo' in json_dict:
        update_values['mobileNo'] = str(json_dict['mobileNo'])

    connection_object = engine.connect()
    _insert_user_query_ = Insert(model.WirelessToDoUser.user).values(update_values)
    connection_object.execute(_insert_user_query_)

    _select_last_added_user_record = select([model.WirelessToDoUser.user.c.userId, model.WirelessToDoUser.user.c.userName,
                        model.WirelessToDoUser.user.c.emailId]).order_by(
        model.WirelessToDoUser.user.c.userId.desc()).limit(1)
    _last_user_record_result = connection_object.execute(_select_last_added_user_record)
    _last_user_record_data = list(_last_user_record_result)
    _last_user_record_ = [item for sublist in _last_user_record_data for item in sublist]

    if update_values['userName'] and update_values['emailId'] in _last_user_record_:
        response = {"response": {"message": 'user signed in successfully with user_Id {}'.format(_last_user_record_[0])},
                    "status": "success"}

        await mail.aws_send_email_with_attachment(os.environ.get("email_id"), update_values['emailId'],
                                         update_values['firstName'],
                                        update_values['userName'], json_dict['password'])
        stop = timeit.default_timer()
        time_taken = stop - start
        response['request_time (seconds)'] = str(time_taken)

        return response
    else:
        raise validator.UserSignInError()


async def upload_user_logo_():

    """

    Method Name  : upload_user_logo

    Parameters   : Image in postman

    This function will upload the user logo for the user
    to the database.
    Once the logo uploaded, email notification will be
    sent to particular user with the base64 image

     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 5.0                ##
     ##   Revisions: 5                ##
     ###################################

    """


    _image_read = request.files.get('Image').read()
    image_encoded_ = base64.b64encode(_image_read)

    updated_values = {'userLogo': image_encoded_}

    _token_in_headers = request.headers.get('token')
    _current_user = await get_userid_(_token_in_headers)

    _query_to_upload_user_logo = update(model.WirelessToDoUser.user).where(
        model.WirelessToDoUser.user.c.userId == _current_user).values(updated_values)
    connection = engine.connect()
    connection.execute(_query_to_upload_user_logo)

    _user_logo_response = {"response": {"message": 'userId {} Logo has been uploaded'.format(_current_user)},
                "status": "success"}

    _get_email_and_name_of_user = select(
        [model.WirelessToDoUser.user.c.emailId, model.WirelessToDoUser.user.c.firstName]).where(
        model.WirelessToDoUser.user.c.userId == _current_user)
    _get_result = connection.execute(_get_email_and_name_of_user)
    _get_data = list(_get_result)
    _data_ = [item for sublist in _get_data for item in sublist]
    print("query_data",_data_)
    if not _data_ ==[]:
        _email_id_ = _data_[0]
        _first_name_ = _data_[1]
        decode_img = base64.b64decode(image_encoded_)
        await mail.send_user_logo_upload_mail(os.environ.get("email_id"), _email_id_,
                                                 os.environ.get("email_password"), _first_name_,decode_img)
        return _user_logo_response


async def __insert_user_agent_record__(userid, token_pass, user_agent):


    _insert__user_id__token__token_agent = Insert(model.WirelessToDoUserSession.user_session).values(userId=userid, token=token_pass,
                                                                    user_Agent=user_agent)
    connection = engine.connect()
    connection.execute(_insert__user_id__token__token_agent, {'userId': userid, 'token': token_pass, 'user_Agent': user_agent})


async def login_function__(userName, password, user_agent):

    _hashed_password = hashlib.pbkdf2_hmac('sha512', bytes(password, 'utf-8'), bytes(os.environ.get("salt"), 'utf-8'),
                                          int(os.environ.get("iterations"))).hex()

    _query__to__select__user_name__password = select([model.WirelessToDoUser.user]).where(model.WirelessToDoUser.user.c.userName == userName,
                                                        model.WirelessToDoUser.user.c.password == _hashed_password)
    _select_query_result = engine.execute(_query__to__select__user_name__password)
    _select_query_data = list(_select_query_result)

    if len(_select_query_data) > 0:

        _user_id_ = _select_query_data[0][0]
        print('result', _select_query_data)
        _token_ = "Bearer " + await _random_token()
        await __insert_user_agent_record__(_user_id_, _token_, user_agent)
        _mobile_no = await _get_mobile_no(_user_id_)
        print("mobile_No",_mobile_no)
        await mail.__mfa_authenticator__(await _get_mobile_no(_user_id_))
        time.sleep(30)
        _mfa_file = open("mfaCode.env", "w")
        _mfa_file.write("\nmfaCode={}".format("None"))
        _mfa_file.close()
        return {'response': {'token': _token_, 'user id': _user_id_}, 'status': 'success'}

    else:
        return {"status": "failed", "message": "validator.InvalidAuthentication",
                    'error_code': validator.__get_error_code__('validator.InvalidAuthentication')}


async def __verify_otp__(json_dict):

    global _mfa_code_sent
    _update_json_dict = {}

    if 'mfaCode' in json_dict:
        _update_json_dict['mfaCode'] = str(json_dict['mfaCode'])

    f = open("mfaCode.env", "r")
    for line in f:
        mfaCode = line.split("=")
        _mfa_code_sent = list(mfaCode)

    if _mfa_code_sent[1] == _update_json_dict['mfaCode']:
        response = {'status': 'success','message':'otp Verified'}
        return response
    else:
        response = {'status': 'error', 'message': 'otp not Verified'}
        return response


async def _random_token(size=int(os.environ.get("token_size")),
                       chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


async def logout_func_(token_arg):

    _header_token = request.headers.get('token')
    connection = engine.connect()
    _user_id = await get_userid_(_header_token)
    _remove_user = delete(model.WirelessToDoUserSession.user_session).where(
        model.WirelessToDoUserSession.user_session.c.token == token_arg)
    connection.execute(_remove_user)
    print("token", token_arg)
    return {"status": "successful",
                "message": "userId: {} current session deleted in user_session table".format(_user_id)}


async def update_reset_usersession_(user_id):

    _header_token = request.headers.get('token')
    _user_id_ = await get_userid_(_header_token)
    remove_user = delete(model.WirelessToDoUserSession.user_session).where(
        model.WirelessToDoUserSession.user_session.c.userId == user_id)
    engine.execute(remove_user)
    response = {"status": "successful",
                "message": "userId: {} login details deleted in user_session table".format(user_id)}
    logging.info(response)
    return response


async def get_userid_(token):

    _user_id_query = select([model.WirelessToDoUserSession.user_session]).where(
        model.WirelessToDoUserSession.user_session.c.token == token)
    connection_object = engine.connect()
    _user_id_query_result = connection_object.execute(_user_id_query)
    _user_id_query_data = list(_user_id_query_result)
    _query_data = [item for sublist in _user_id_query_data for item in sublist]
    if not _query_data == []:
        return _query_data[0]


async def _get_mobile_no(userId):

    _mobile_no_query = select([model.WirelessToDoUser.user.c.mobileNo]).where(
        model.WirelessToDoUser.user.c.userId == userId)
    connection = engine.connect()
    _mobile_no_query_result = connection.execute(_mobile_no_query)
    _mobile_no_query_data = list(_mobile_no_query_result)
    _mobile_no_data = [item for sublist in _mobile_no_query_data for item in sublist]
    if not _mobile_no_data == []:
        return _mobile_no_data[0]


async def __token_required__():

    _headers_token = request.headers.get('token')
    _token_query = select([model.WirelessToDoUserSession.user_session]).where(
        model.WirelessToDoUserSession.user_session.c.token == _headers_token)
    _token_result = engine.execute(_token_query)
    _token_data = list(_token_result)
    if _token_data:
        if _token_data[0][1] == _headers_token:
            return True
        else:
            raise validator.InvalidAuthentication()
    else:
        raise validator.InvalidAuthentication()


async def __portal_dns__():

    _header_portal_dns_ = request.headers.get('portalDNS')
    if not _header_portal_dns_ is None:
        if _header_portal_dns_ == _portal_dns:
            return True
        else:
            raise validator.InvalidPortalDNS()
    else:
        raise validator.InvalidPortalDNS()