#!/usr/bin/env python3
"""
This module provides a function to obfuscate specified fields in a log message.
"""

import re
import logging
from typing import List, Tuple

# Define PII_FIELDS with fields considered as PII
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "credit_card")


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record, obfuscating specified fields.

        :param record: The log record to format.
        :return: The formatted log record as a string.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super().format(record)


get_logger() -> logging.Logger:
    """
    Creates and configures a logger named "user_data".

    :return: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
