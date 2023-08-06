# coding:utf-8

from config import MongoServer
import pymongo
from pymongo import ASCENDING, DESCENDING

MongoCfg = {
    'authSource': 'proddb',
    'username': 'app',
    'password': 'Prod2app',
    'connecttimeoutms': 60 * 1000
}

# product DB
mongo_client = None
mongo_db = None

product = None


def init():
    if not MongoServer['active']:
        return

    global mongo_client
    global mongo_db

    global product

    if mongo_client is not None:
        return

    server = MongoServer['mongodb'].split(':')
    host = server[0]
    port = int(server[1]) if len(server) > 1 else 27017

    mongo_client = pymongo.MongoClient(host=host, port=port, **MongoCfg)
    mongo_db = mongo_client[MongoCfg['authSource']]

    # my collections
    product = mongo_db.product
    # END

    # 创建索引
    _product_index()

    # 初始化系统数据
    _init_data()


def start_session():
    return mongo_client.start_session()


def _product_index():
    """
    {
        "_id": ObjectId('5c729df2e155ac16da86a1d0'),
        "name": "live-pledge",                           # 产品标示名，英文、数字、"-"
        "catalog": ObjectId('5c710622e155ac0c39c8b66d'), # 所属分类节点ID
        "status": 30,                                    # 状态：-10:已删除；0:编辑中；10:待审；20:休眠中；30:已激活；
        "display": {
            "zh": "活期质押",
            "en": "Live Pledge"
        },
        "desc": {
            "zh": "灵活的质押和支取",
            "en": "Pledge and draw flexibly"
        },
        "icon": "http://your.com/icon/pledge.png",
        "the_pledged": {...},   # 被质押的东西
        "the_loaned": {...},    # 被贷出的东西
        "normal_rate": 1.5,   # 正常质押率，质押率：质押资产市值/贷款货币市值
        "warn_rate": 1.1,     # 禁戒质押率
        "bomb_rate": 1.05,    # 爆仓质押率
        "interest_rate": 0.0001 # 贷款利率（日利率）
        "time_limit": 2592000000, # 期限，单位：ms，0表示无限制
        "fei_ex_rate": 1,       # 手续费率，因为平台发起交易时需要矿工费，定义是否以手续费的形式从用户收取
        "flow_fei": {
            "loan": "0x+0",     # f(x)=ax+b的函数形式计算费率，x为流水进出数量，单位为流水操作的货币数量
            "redeem": "0x+5"    # 同上
        },
        "created": 1551015331186,
        "updated": 1551015331186
    }
    """
    product.create_index('name')
    product.create_index([('catalog', ASCENDING), ("created", DESCENDING)])


def _init_data():
    pass
