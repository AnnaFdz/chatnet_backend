from flask import Blueprint, jsonify
from ..models.exceptions import SourceNotFound, InvalidDataError, DuplicateUsernameError

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(SourceNotFound)
def handle_source_not_found(error):
    return error.get_response()

@errors.app_errorhandler(InvalidDataError)
def handle_validate_data(error):
    return error.get_response()
@errors.app_errorhandler(DuplicateUsernameError)
def handle_duplicate_username(error):
    return error.get_response()

@errors.app_errorhandler(SourceNotFound)
def handle_source_not_found(error):
    response = error.get_response()
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5500")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

@errors.app_errorhandler(InvalidDataError)
def handle_validate_data(error):
    response = error.get_response()
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5500")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

@errors.app_errorhandler(DuplicateUsernameError)
def handle_duplicate_username(error):
    response = error.get_response()
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5500")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response