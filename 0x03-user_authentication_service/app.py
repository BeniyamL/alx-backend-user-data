#!/usr/bin/env python3
"""
a flask app module
"""
from flask import Flask, jsonify, redirect, request, abort
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def index() -> str:
    """
    method to handle the / from the url
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def register_user() -> str:
    """
    an end point to register a given user
    """
    try:
        eml = request.form.get('email')
        psswrd = request.form.get('password')
    except KeyError:
        abort(400)

    try:
        new_usr = AUTH.register_user(eml, psswrd)
        messeage = {"email": new_usr.email, "message": "user created"}
        return jsonify(messeage)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def log_in() -> str:
    """
    an end point for log in to the system
    """
    try:
        eml = request.form.get('email')
        psswrd = request.form.get('password')
        if AUTH.valid_login(eml, psswrd):
            sesn_id = AUTH.create_session(eml)
            if sesn_id:
                out = jsonify({"email": eml, "message": "logged in"})
                out.set_cookie("session_id", sesn_id)
                return out
            else:
                abort(401)
        else:
            abort(401)
    except NoResultFound:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    """
    end point to log out from the system
    """
    try:
        sesn_id = request.cookies.get('session_id')
        usr = AUTH.get_user_from_session_id(sesn_id)
        if usr:
            AUTH.destroy_session(usr.id)
            return redirect('/', code=302)
        else:
            abort(403)
    except KeyError:
        abort(403)


@app.route('/profile', methods=['GET'])
def get_profile() -> str:
    """
    a method to get the user profile
    """
    try:
        sesn_id = request.cookies.get('session_id')
        if sesn_id is None:
            abort(403)
        usr = AUTH.get_user_from_session_id(sesn_id)
        if usr:
            msg = {"email": usr.email}
            return jsonify(msg), 200
        else:
            abort(403)
    except KeyError:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password() -> str:
    """
    an end point to to get the resseted password
    """
    try:
        eml = request.form.get('email')
        tkn: str = AUTH.get_reset_password_token(eml)
        msg = {"email": eml, "reset_token": tkn}
        return jsonify(msg), 200
    except (KeyError, ValueError):
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """
    an end point to update the password
    """
    try:
        eml = request.form.get('email')
        tokn = request.form.get('reset_token')
        psswrd = request.form.get('new_password')
        AUTH.update_password(tokn, psswrd)
        msg = {"email": eml, "message": "Password updated"}
        return jsonify(msg), 200
    except (KeyError, ValueError):
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
