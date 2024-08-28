#!/usr/bin/env python3
"""filtered_logger Module"""
import re


def filter_datum(fields, redaction, message, separator):
    """filter_datum function"""
    z = message
    for field in fields:
        z = re.sub(
            "{}=.*?{}".format(field, separator),
            "{}={}{}".format(field, redaction, separator),
            z,
        )
    return z
