# coding=utf-8

from ..db import mongo as db
from tweb.error_exception import ErrException, ERROR
from webmother.utils.bson_util import bson_id, json_id
from webmother.service import ctrl_catalog


class Contract:

    def __init__(self, contract_id):
        ret = db.contract.find_one({'_id': bson_id(contract_id)})
        if ret is None:
            raise ErrException(ERROR.E40400, extra='eth contract not registered: %s' % contract_id)

        ret[f'contract_id'] = json_id(ret.pop('_id'))
        ret['catalog'] = ctrl_catalog.simple_read(ret['catalog'])
        self.json = ret
        self.symbol = ret['symbol']
        self.decimals = ret['decimals']
        self.precision = ret['precision']
