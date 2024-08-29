#!/usr/bin/env python3
"""filtered_logger Module"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """filter_datum function"""
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message
