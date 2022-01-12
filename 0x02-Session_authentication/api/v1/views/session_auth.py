#!/usr/bin/env python3
""" Module of session authorization view
"""
from os import getenv
from flask import jsonify, abort, request
from flask.helpers import make_response
from api.v1.views import app_views
from models.user import User
from typing import TypeVar, List


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    a method to log in to the system
    """
    usr_email = request.form.get('email')
    usr_passwrd = request.form.get('password')
    if usr_email is None or usr_email == '':
        return make_response(jsonify({"error": "email missing"}), 400)
    if usr_passwrd is None or usr_passwrd == '':
        return make_response(jsonify({"error": "password missing"}), 400)

    usr: List[TypeVar('User')]
    try:
        usr = User.search({'email': usr_email})
    except Exception:
        return make_response(
                            jsonify({"error": "no user found for this email"}),
                            404
                            )

    if len(usr) == 0 or usr is None:
        return make_response(
                            jsonify({"error": "no user found for this email"}),
                            404
                            )
    for u in usr:
        if u.is_valid_password(usr_passwrd):
            from api.v1.app import auth
            sen_id = auth.create_session(u.id)
            ses_name = getenv('SESSION_NAME')
            usr_dct = make_response(u.to_json())
            usr_dct.set_cookie(ses_name, sen_id)
            return usr_dct

    return make_response(jsonify({"error": "wrong password"}), 401)


@app_views.route(
                '/auth_session/logout',
                methods=['DELETE'], strict_slashes=False
                )
def logout():
    """
    a method to logout from the system
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(200)
