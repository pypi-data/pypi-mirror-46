# coding=utf-8

import webmother
from .db import mongo
from qccwallet import routes
from .service.external import ethereum
from .extra_passport import append_extra


def init(app, load_routes=True):
    # 初始化webmother
    webmother.init(app, True)

    # 初始化本系统数据库
    mongo.init()

    # 增加本系统增加的权限需求
    append_extra()

    # 初始化外部区块链模块
    ethereum.init()

    # 加载路由模块
    if load_routes:
        app.load_routes(routes)
