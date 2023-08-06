import json

from tweb import tools, rdpool
from tweb.error_exception import ErrException, ERROR

import config


async def gen_permit(indicator, timeout):
    """
    :param indicator: 用户标识
    :param timeout: 有效时间
    :return: {'indicator': indicator, 'permit': 'xxx'}
    """
    permit = tools.gen_id3()
    ret = {'indicator': indicator, 'permit': permit}
    rdpool.rds.set(_key(indicator, permit), json.dumps(ret), timeout)
    return ret


async def verify_permit(indicator, permit):
    key = _key(indicator, permit)
    data = rdpool.rds.get(key)
    if data is None:
        raise ErrException(ERROR.E40100)

    rdpool.rds.delete(key)
    record = json.loads(data)
    return record


def _key(indicator, permit):
    return '{}/user/permit/{}/{}'.format(config.PLATFORM, indicator, permit)

