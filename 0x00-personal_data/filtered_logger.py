#!/usr/bin/env python3
"""filtered_logger Module"""
import re
from typing import List


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
