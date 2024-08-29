#!/usr/bin/env python3
"""filtered_logger Module"""
from os import getenv
import re
from typing import List
import logging
import mysql.connector


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """filter_datum function"""
    for field in fields:
        message = re.sub(
            f"{field}=.*?{separator}",
            f"{field}={redaction}{separator}", message
        )
    return message


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """get_logger fucntion"""
    log_obj = logging.getLogger("user_data")
    log_obj.setLevel(logging.INFO)
    log_obj.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    log_obj.addHandler(stream_handler)

    return log_obj


def get_db() -> mysql.connector.connection.MySQLConnection:
    """get_db function"""
    return mysql.connector.connect(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME')
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format function"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def main() -> None:
    """main function"""
    db = get_db()
    db_cursor = db.cursor()
    db_cursor.execute("SELECT * FROM users;")
    headers = [field[0] for field in db_cursor.description]
    logger = get_logger()
    for row in db_cursor:
        info_answer = ''
        for r, h in zip(row, headers):
            info_answer += f'{h}={(r)}; '
        logger.info(info_answer)
    db_cursor.close()
    db.close()


if __name__ == '__main__':
    main()
