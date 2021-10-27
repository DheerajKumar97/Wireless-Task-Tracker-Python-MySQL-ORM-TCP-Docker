from flask import request, Response, Blueprint
from . import card
import json
from auth import auth
import validator as validator
import traceback
import logging
import sys


CARD_BP = Blueprint('card_bp', __name__)


@CARD_BP.route('/wtt/card/create', methods=['POST'])
async def _create_card():

    try:

        if await auth.__token_required__() is True and await auth.__portal_dns__() is True:
            json_dict = request.get_json()
            _create_card_value = await card.create_card_(json_dict)
            _create_card_response = Response(json.dumps(_create_card_value))
            _create_card_response.mimetype = 'application/json'
            logging.info(_create_card_value)
            return _create_card_response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
        error_code = validator.__get_error_code__(error_class)
        response = {"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.error(response)
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
            logging.error(response)
            response = Response(json.dumps(response))
            response.mimetype = 'application/json'
            return response


# {"cardId": 1, "cardStatus": "created", "cardAssociated": False}
@CARD_BP.route('/wtt/card/update_status', methods=['POST'])
async def _update_card_status():

    try:

        if await auth.__token_required__() is True and await auth.__portal_dns__() is True:
            json_dict = request.get_json()
            _create_status_value = await card.update_card_status_(json_dict)
            _create_status_response = Response(json.dumps(_create_status_value))
            _create_status_response.mimetype = 'application/json'
            logging.info(_create_status_value)
            return _create_status_response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
        error_code = validator.__get_error_code__(error_class)
        response = {"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.error(response)
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
            logging.error(response)
            response = Response(json.dumps(response))
            response.mimetype = 'application/json'
            return response


# {"cardId": 1}
@CARD_BP.route('/wtt/card/delete', methods=['POST'])
async def _delete_card():

    try:

        if await auth.__token_required__() is True and await auth.__portal_dns__() is True:
            json_dict = request.get_json()
            if not 'queueCommand' in json_dict.keys() or 'queueCommand' in json_dict.keys():
                json_dict['queueCommand'] = 1
            _delete_card_value = await card.delete_card_(json_dict)
            _delete_card_response = Response(json.dumps(_delete_card_value))
            _delete_card_response.mimetype = 'application/json'
            logging.info(_delete_card_value)
            return _delete_card_response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
        error_code = validator.__get_error_code__(error_class)
        response = {"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.error(response)
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
            logging.error(response)
            response = Response(json.dumps(response))
            response.mimetype = 'application/json'
            return response


# {"cardId": 1, "cardName":"New Card","cardName":"edit your content"}
@CARD_BP.route('/wtt/card/edit', methods=['POST'])
async def _edit_card():

    try:

        if await auth.__token_required__() is True and await auth.__portal_dns__() is True:
            json_dict = request.get_json()
            _edit_card_value_ = await card.edit_card_(json_dict)
            _edit_card_response_ = Response(json.dumps(_edit_card_value_))
            _edit_card_response_.mimetype = 'application/json'
            logging.info(_edit_card_value_)
            return _edit_card_response_

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
        error_code = validator.__get_error_code__(error_class)
        response = {"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.error(response)
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
            logging.error(response)
            response = Response(json.dumps(response))
            response.mimetype = 'application/json'
            return response


@CARD_BP.route('/wtt/card/associate_user', methods=['POST'])
async def _associate_user_and_card():

    try:

        if await auth.__token_required__() is True and await auth.__portal_dns__() is True:
            json_dict = request.get_json()
            response_value = await card.user_card_Association_(json_dict)
            response = Response(json.dumps(response_value))
            response.mimetype = 'application/json'
            logging.info(response_value)
            return response

    except:
        error_class = validator.__get_error_class__(sys.exc_info())
        error_code = validator.__get_error_code__(error_class)
        response = {"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.error(response)
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
            logging.error(response)
            response = Response(json.dumps(response))
            response.mimetype = 'application/json'
            return response