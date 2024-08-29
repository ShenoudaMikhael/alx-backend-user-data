#!/usr/bin/env python3
"""filtered_logger Module"""
import re


def filter_datum(fields, redaction, message, separator):
    """filter_datum function"""
    for field in fields:
        message = re.sub(
            "{}=.*?{}".format(field, separator),
            "{}={}{}".format(field, redaction, separator),
            message,
        )
    return message
