#!/usr/bin/env python3
"""
a python module to user data
"""
from typing import List, Tuple
import re
import logging
import mysql.connector
import os

from mysql.connector.dbapi import ROWID

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List):
        """init method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format - function to filter the incoming log record
        Arguments:
            fields - the given fields
        Returns:
            the formated log information
        """
        msg = super(RedactingFormatter, self).format(record)
        msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return msg


def filter_datum(fields: List, redaction: str, message: str, separator: str):
    """
    filter_dataum - funtion to that returns log messaged obfuscated
    Arguments:
        fields: the fields to be obfuscated
        redaction: the value to be replaced
        message: the given message
        separator: the character used to separate
    Returns:
        the obfuscated string
    """
    msg = message
    for fld in fields:
        ptrn = "{}=.*?{}".format(fld, separator)
        rplc = "{}={}{}".format(fld, redaction, separator)
        msg = re.sub(ptrn, rplc, msg)
    return msg


def get_logger() -> logging.Logger:
    """
    a get logger method to return a user_data logger
    """
    lg: logging.Logger = logging.getLogger('user_data')
    lg.propagate = False

    strm_hdlr: logging.StreamHandler = logging.StreamHandler()
    strm_hdlr.setLevel(logging.INFO)

    frmt = logging.Formatter((RedactingFormatter(fields=PII_FIELDS)))
    strm_hdlr.formatter(frmt)
    strm_hdlr.setFormatter(frmt)

    lg.addHandler(strm_hdlr)
    return lg


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get db function to create a mysql connection
    """
    usr_name = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passwrd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host_name = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db_conn = mysql.connector.connect(
        host=host_name,
        username=usr_name,
        password=passwrd,
        database=db_name
    )
    return db_conn


def main():
    """
    an entry point for the execution of the program
    """
    conn: mysql.connector.connection.MySQLConnection = get_db()
    lg: logging.Logger = get_logger()
    crs = conn.cursor()
    hdrs: List = []
    qry: str = 'SELECT name, email, phone, ssn, password, ip, \
                last_login, user_agent FROM users'

    crs.execute(qry)
    for head in crs.description:
        hdrs.append(head[0])

    for rw in crs:
        ech_rw: List = []
        for hdr, val in zip(hdrs, rw):
            ech_rw.append(''.join("{}={}".format(hdr, str(val))))
        rslt: str = ';'.join(ech_rw)
        log_rcd = logging.LogRecord("user_data", logging.INFO, None, None,
                                    rslt, None, None)
        formatter = RedactingFormatter(fields=PII_FIELDS)
        print(formatter.format(log_rcd))

    crs.close()
    conn.close()


if __name__ == "__main__":
    main()
