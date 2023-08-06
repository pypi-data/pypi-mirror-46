# coding=utf-8

from tweb import base_handler, myweb
from tornado import gen
import json
from ..service.async_wrap import ctrl_wallet


class MyWalletsHandler(base_handler.BaseHandler):

    @myweb.authenticated
    @gen.coroutine
    def get(self):
        user_id = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_wallet.query_mine(user_id, access_token)
        return self.write({'list': ret})


class WalletHandler(base_handler.BaseHandler):
    """
    钱包账户操作
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, contract_id, wallet_id, **kwargs):
        user_id = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_wallet.create(contract_id, data, user_id, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, contract_id, wallet_id, **kwargs):
        user_id = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_wallet.remove(contract_id, wallet_id, user_id, access_token)
        return self.write(ret)


class BalanceHandler(base_handler.BaseHandler):
    """
    钱包余额
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, contract_id, address, **kwargs):
        ret = yield ctrl_wallet.balance(contract_id, address)
        return self.write(ret)


class TransferHandler(base_handler.BaseHandler):
    """
    交易转账（含合约交易）
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, contract_id, from_address, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_wallet.transfer(contract_id, from_address, data)
        return self.write(ret)


class TransferEstimateHandler(base_handler.BaseHandler):
    """
    交易矿工费预估
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, contract_id, from_address, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_wallet.transfer_miner_fei(contract_id, from_address, data)
        return self.write(ret)


class TxInfoHandler(base_handler.BaseHandler):
    """
    获取交易详情（含合约交易）
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid, tx_hash, **kwargs):
        ret = yield ctrl_wallet.get_tx_info(cid, tx_hash)
        return self.write(ret)


class TxListHandler(base_handler.BaseHandler):
    """
    获取交易详情（含合约交易）
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, cid, address, **kwargs):
        ret = yield ctrl_wallet.get_tx_list(cid, address)
        return self.write({'list': ret})


class ViewHandler(base_handler.BaseHandler):
    """
    合约查看（不用签名，不用矿工费，不会写入数据）
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, contract_id, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_wallet.view(contract_id, data)
        return self.write(ret)


class TransactionHandler(base_handler.BaseHandler):
    """
    # 合约交易调用（需签名，会扣矿工费，会写入/改变数据）
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, contract_id, from_address, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        ret = yield ctrl_wallet.transaction(contract_id, sender_address, data)
        return self.write(ret)
