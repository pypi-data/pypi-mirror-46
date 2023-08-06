from ..db import mongo as db
from tweb.error_exception import ErrException, ERROR
from webmother.utils.bson_util import bson_id, json_id
from qccwallet.model.contract import Contract


class Product:

    def __init__(self, pid):
        ret = db.product.find_one({'_id': bson_id(pid)}, {'catalog': 0})
        if ret is None:
            raise ErrException(ERROR.E40400, extra=f'the product({pid}) not existed')

        if isinstance(ret['the_pledged'], ObjectId):
            ret['the_pledged'] = ctrl_contract.simple_read(ret['the_pledged'])
        if isinstance(ret['the_loaned'], ObjectId):
            ret['the_loaned'] = ctrl_contract.simple_read(ret['the_loaned'])
        ret['pid'] = json_id(ret.pop('_id'))

        self.json = ret
