#!/usr/bin/env python3
"""
This module provides a function to obfuscate specified fields in a log message.
"""

import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the specified fields in the log message.

    :param fields: List of fields to obfuscate.
    :param redaction: The string to replace the field values with.
    :param message: The log message containing the fields.
    :param separator: The character separating fields in the log message.
    :return: The obfuscated log message.
    """
    return re.sub(
        f'({"|".join(fields)})=.*?(?={separator}|$)',
        lambda m: f'{m.group(1)}={redaction}',
        message
    )
