from flask import Flask


app = Flask(__name__)


class ErrorTable:
    Data = {'jsonschema.exceptions.ValidationError': 'ER_AUT001',
            'validator.UserSignInError': 'ER_AUT002',
            'validator.InvalidAuthentication':'ER_AUT003',
            'validator.InvalidPortalDNS':'ER_AUT004',
            'validator.userId_or_cardId_is_Null':'ER_CRD005',
            'validator.InvalidCardId':'ER_CRD006',
            'validator.InvalidUserId': 'ER_CRD007'
            }


def __verify_error_reason__(ErrorReason):
    for Reason, ErrorCode in ErrorTable.Data.items():
        if Reason == ErrorReason:
            return ErrorCode


def __get_error_code__(ErrorReason):
    print("ErrorReason",ErrorReason)
    if ErrorReason in ErrorTable.Data:
        return ErrorTable.Data[ErrorReason]
    else:
        None

def __get_error_class__(sys_exec):
    error_class = str(sys_exec[0])
    error_class = error_class[8:-2]
    return error_class


class UserSignInError(Exception):
    pass

class InvalidAuthentication(Exception):
    pass

class InvalidPortalDNS(Exception):
    pass

class userId_or_cardId_is_Null(Exception):
    pass

class InvalidCardId(Exception):
    pass

class InvalidUserId(Exception):
    pass
