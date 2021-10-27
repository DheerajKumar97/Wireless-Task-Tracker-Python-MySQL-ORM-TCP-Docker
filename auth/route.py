from flask import request, Response, Blueprint, jsonify
import sys
import hashlib
from . import model
from db import engine
import validator
from . import auth as auth
import os
import json
import logging
import base64
import traceback


AUTH_BP = Blueprint('auth_bp', __name__)


@AUTH_BP.route('/wtt/auth/user/create', methods=['POST'])
async def _create_user():

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

    try:

        json_dict = request.get_json()
        _create_user_response_json = await auth.create_user_(json_dict)
        _create_user_response = Response(json.dumps(_create_user_response_json))
        _create_user_response.mimetype = 'application/json'
        logging.info(_create_user_response_json)
        return _create_user_response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
        print("error_class",error_class)
        error_code = validator.__get_error_code__(error_class)
        print("error_code", error_code)
        response = {"response": {"status": "error", "message": error_class}}
        if error_code is not None:
            response["response"]['error_code'] = error_code
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


@AUTH_BP.route('/wtt/auth/user/logo-upload', methods=['POST'])
async def _user_logo_upload():

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


    try:

        if await auth.__token_required__() is True and await auth.__portal_dns__() is True:
            _user_logo_upload_value = await auth.upload_user_logo_()
            _user_logo_upload_response = Response(json.dumps(_user_logo_upload_value))
            _user_logo_upload_response.mimetype = 'application/json'
            logging.info(_user_logo_upload_value)
            return _user_logo_upload_response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
        print("error_class",error_class)
        error_code = validator.__get_error_code__(error_class)
        print("error_code", error_code)
        response = {"response": {"status": "error", "message": error_class}}
        if error_code is not None:
            response["response"]['error_code'] = error_code
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


@AUTH_BP.route('/wtt/auth/login', methods=['POST'])
async def _login_function():

    """

    Method Name  : login_function

    Parameters   : {"userName": Name,"password": password}

    This function takes input as json and allows user to
    login into the wireless Tracker build as Bearer Token
    based Login Authentication

    For every user separate user sessions will be created
    and those session will get expiry at particular interval
    of time

     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 3.0                ##
     ##   Revisions: 3                ##
     ###################################

    """


    try:

        json_dict = request.get_json()
        user_agent = request.headers.get('User-Agent')


        if 'userName' not in json_dict and 'password' not in json_dict:
            authorization = request.headers.get('Authorization')
            authorization = authorization.replace('Basic ','')
            authorization = base64.b64decode(authorization)
            authorization = str(authorization)[2:-1]
            authorization = authorization.split(":")
            json_dict['userName'] = authorization[0]
            json_dict['password'] = authorization[1]

        __log_in_json_value__ = await auth.login_function__(userName =json_dict['userName'],password=json_dict['password'],user_agent = user_agent)
        _log_in_response = Response(json.dumps(__log_in_json_value__))
        logging.info(__log_in_json_value__)
        _log_in_response.mimetype = 'application/json'
        return _log_in_response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
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


@AUTH_BP.route('/wtt/auth/logout', methods=['POST'])
async def _logout_function():

    """

    Method Name  : logout_function

    Parameters   : None

    This function does not take any parameters but
    as all the functions it requires token for
    logging out the sessions.

    For every logout only that particular user session
    will get logged out and Token generated by the
    particular user will get deleted in database.

     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 2.0                ##
     ##   Revisions: 2                ##
     ###################################

    """

    try:
        if await auth.__token_required__() is True:

            __current_user_token = request.headers.get('token')
            _logout_json_value = await auth.logout_func_(__current_user_token)
            _logout_json_response = Response(json.dumps(_logout_json_value))
            logging.info(_logout_json_value)
            _logout_json_response.mimetype = 'application/json'
            return _logout_json_response
    except:
        error_class = validator.__get_error_class__(sys.exc_info())
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


@AUTH_BP.route('/wtt/auth/login/verify', methods=['POST'])
async def _verify_user():

    try:

        if await auth.__token_required__() is True and await auth.__portal_dns__() is True:
            json_dict = request.get_json()
            _verify_user_json_value = await auth.__verify_otp__(json_dict)
            _verify_user_response = Response(json.dumps(_verify_user_json_value))
            _verify_user_response.mimetype = 'application/json'
            logging.info(_verify_user_json_value)
            return _verify_user_response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
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


@AUTH_BP.route('/wtt/auth/update', methods=['GET', 'POST'])
async def _login_update_function():

    """

    Method Name  : login_update_function

    Parameters   : {"userName":Name,"password": password}

    This function takes input as json contains of
    userName and Password , after the http request
    the user credentials of particular user will
    get updated
    For every update entire user login history of
    will get deleted along with Tokens, so that
    old token will be Invalid

     ###################################
     ##   Written By: Dheeraj Kumar K ##
     ##   Version: 2.0                ##
     ##   Revisions: 2                ##
     ###################################

    """


    try:
        if await auth.__token_required__() is True:

            json_dict = request.get_json()
            token = request.headers.get('token')
            userName = json_dict['userName']
            password = json_dict['password']
            config = {'userName': userName, 'password': password}

            password = hashlib.pbkdf2_hmac('sha512', bytes(password, 'utf-8'),
                                           bytes(os.environ.get("salt"), 'utf-8'),
                                           int(os.environ.get("iterations"))).hex()
            userName = str(userName)
            password = str(password)

            user_id = auth.get_userid_(token)
            stmt = model.WirelessToDoUser.user.update().where(
                model.WirelessToDoUser.user.c.userId == user_id).values(username=userName,
                                                                  password=password)
            conn = engine.connect()
            conn.execute(stmt, {'userId': user_id, 'userName': userName, 'password': password})



            userId = user_id
            await auth.update_reset_usersession_(userId)
            response = Response(json.dumps(
                {'status': 'success', 'message': 'username and password updated for user_id {}'.format(userId)}))
            response.mimetype = 'application/json'
            return response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
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