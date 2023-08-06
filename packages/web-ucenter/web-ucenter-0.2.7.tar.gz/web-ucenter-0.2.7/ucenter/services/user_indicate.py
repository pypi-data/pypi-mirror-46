import re
from bson.objectid import ObjectId


def is_user_id(indicator):
    return ObjectId.is_valid(indicator)


def is_email(indicator):
    return re.match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$', indicator)


def is_mobile(indicator):
    return re.match(r'[0-9]+-[0-9]+$', indicator)


def is_username(indicator):
    return re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', indicator)
