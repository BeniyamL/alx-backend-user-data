#!/usr/bin/env python3
"""
a main method to test the user authentication
"""
import requests

URL = 'http://localhost:5000'
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    a method to test the user registration
    """
    new_usr = {'email': email, 'password': password}
    rqst = requests.post("{}/users".format(URL), data=new_usr)
    out = {"email": email, "message": "user created"}

    assert rqst.status_code == 200
    assert rqst.json() == out


def log_in_wrong_password(email: str, password: str) -> None:
    """
    a method to test log in with wrong password
    """
    usr = {'email': email, 'password': password}
    rqst = requests.post("{}/sessions".format(URL), data=usr)

    assert rqst.status_code == 401


def profile_unlogged() -> None:
    """
    a method to test the loggout method
    """
    rqst = requests.delete("{}/sessions".format(URL))
    assert rqst.status_code == 403


def log_in(email: str, password: str) -> None:
    """
    a method to test the log in to the system
    """
    usr = {'email': email, 'password': password}
    rqst = requests.post("{}/sessions".format(URL), data=usr)
    out = {"email": email, "message": "logged in"}

    assert rqst.status_code == 200
    assert rqst.json() == out

    return rqst.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """
    a method to test a logged in profile
    """
    dta = {'session_id': session_id}
    rqst = requests.get("{}/profile".format(URL), cookies=dta)
    out = {"email": EMAIL}

    assert rqst.status_code == 200
    assert rqst.json() == out


def log_out(session_id: str) -> None:
    """
    a method to test log out from the sytem
    """
    dta = {'session_id': session_id}
    rqst = requests.delete("{}/sessions".format(URL), cookies=dta)
    assert rqst.status_code == 200


def reset_password_token(email: str) -> None:
    """
    a method to test the rest password token
    """
    usr = {'email': email}
    rqst = requests.post("{}/reset_password".format(URL), data=usr)
    tkn = rqst.json().get('reset_token')
    out = {"email": email, "reset_token": tkn}

    assert rqst.status_code == 200
    assert rqst.json() == out

    return tkn


def update_password(email: str, reset_token: str, new_pass: str) -> None:
    """
    a method to test the password update
    """
    usr = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_pass
        }

    rqst = requests.put("{}/reset_password".format(URL), data=usr)
    tkn = rqst.json().get('reset_token')
    out = {"email": email, "message": "Password updated"}

    assert rqst.status_code == 200
    assert rqst.json() == out


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
