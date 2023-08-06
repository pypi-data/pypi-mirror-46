# coding:utf-8

from hexbytes import HexBytes
from eth_abi import decode_abi
from tornado import httpclient
import logging
import json
import re
from tweb.error_exception import ErrException, ERROR
from tweb import time
from webmother.utils.bson_util import bson_id, json_id
from webmother.service import ctrl_catalog
from . import ctrl_contract
from .internal import ethereum as in_ethereum
from .external import ethereum as ex_ethereum
from ..db import mongo as db
from ..utils import secret
from ..utils.coinnum import CoinNum


def query_mine(*auth_args):
    uid = auth_args[0]

    cursor = db.wallet.find({'uid': bson_id(uid), 'status': {'$gte': 0}}, {'uid': 0, 'catalog': 0})

    array = list()
    for item in cursor:
        item['wallet_id'] = json_id(item.pop('_id'))
        item['contract'] = ctrl_contract.simple_read(json_id(item.pop('contract_id')))
        array.append(item)

    return array


def create(contract_id, data, *auth_args):
    password = secret.verify_msg(data)
    uid = auth_args[0]

    now = time.millisecond()
    w = {
        "uid": bson_id(uid),
        "contract_id": bson_id(contract_id),
        "status": 10,
        "created": now,
        "updated": now
    }

    if 'alias' in data:
        w['alias'] = data['alias']
    if 'mark' in data:
        w['mark'] = data['mark']

    contract = ctrl_contract.simple_read(contract_id)
    cid = contract['catalog']['cid']
    w['catalog'] = bson_id(cid)

    t = contract['type']
    w['type'] = t

    if t == 'main':
        # 保证只有一个主币账户
        existed = db.wallet.find_one({'uid': bson_id(uid), 'catalog': bson_id(cid), 'status': {'$gte': 0}},
                                     {'uid': 0, 'catalog': 0})
        if existed is not None:
            existed['wallet_id'] = json_id(existed.pop('_id'))
            existed['contract'] = ctrl_contract.simple_read(json_id(existed.pop('contract_id')))
            return existed

        if not re.match(r'^.{6,20}$', password):
            raise ErrException(ERROR.E40000, extra='password should be 6-20 characters')

        chain_name = contract['catalog']['name']
        if chain_name == 'eth':
            w['address'] = in_ethereum.new_account(password)
        else:
            raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)
    else:
        existed = db.wallet.find_one(
            {'uid': bson_id(uid), 'contract_id': bson_id(contract_id), 'status': {'$gte': 0}},
            {'uid': 0, 'catalog': 0})
        if existed is not None:
            existed['wallet_id'] = json_id(existed.pop('_id'))
            existed['contract'] = ctrl_contract.simple_read(json_id(existed.pop('contract_id')))
            return existed

        # 保证已经存在主币账户
        tmp = db.wallet.find_one({'uid': bson_id(uid), 'catalog': bson_id(cid), 'status': {'$gte': 0}},
                                 {'address': 1})
        if tmp is None:
            raise ErrException(ERROR.E40000, extra='please create main account first')

        w['address'] = tmp['address']

        # 校验主币钱包密码
        verify_password(w['address'], password)

    result = db.wallet.insert_one(w)
    ret = db.wallet.find_one(result.inserted_id, {'uid': 0, 'catalog': 0})
    ret['wallet_id'] = json_id(ret.pop('_id'))
    ret['contract'] = ctrl_contract.simple_read(json_id(ret.pop('contract_id')))

    return ret


def remove(contract_id, wallet_id, *auth_args):
    uid = auth_args[0]

    contract = ctrl_contract.simple_read(contract_id)

    t = contract['type']
    if t == 'main':
        # 主币钱包涉及私钥等重要信息，故只做逻辑删除。同时将关联的合约账户全部删除

        existed = db.wallet.find_one({'_id': bson_id(wallet_id),
                                      'uid': bson_id(uid),
                                      'contract_id': bson_id(contract_id),
                                      'status': {'$gte': 0}
                                      })
        if existed is None:
            raise ErrException(ERROR.E40400)

        address = existed['address']

        db.wallet.update_one({'_id': bson_id(wallet_id),
                              'uid': bson_id(uid),
                              'contract_id': bson_id(contract_id)
                              },
                             {'$set': {'status': -10}})

        cursor = db.wallet.find({'address': address.lower(), 'uid': bson_id(uid), 'status': {'$gte': 0}})
        for item in cursor:
            db.wallet.delete_one({'_id': item['_id']})
    else:
        # 合约账户实际是一种方便查看管理的绑定关系，故直接删除

        db.wallet.delete_one({'_id': bson_id(wallet_id), 'uid': bson_id(uid), 'contract_id': bson_id(contract_id)})

    return {}


def balance(contract_id, address):
    contract = ctrl_contract.simple_read(contract_id)

    decimals = contract['decimals']
    precision = contract.get('precision', decimals)

    chain_name = contract['catalog']['name']
    t = contract['type']
    if chain_name == 'eth':
        if t == 'main':
            amount = ex_ethereum.wallet_balance(address)
        elif t == 'ERC20':
            amount = ex_ethereum.contract_call(contract, 'balanceOf', [address])
        else:
            raise ErrException(ERROR.E40000, extra='invalid contract type: %s' % t)
    else:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)

    return {
        'balance': CoinNum(amount).set(decimals, precision).group()
    }


def view(contract_id, data):
    """
    合约查看（不用签名，不用矿工费，不会写入数据）
    """
    contract = ctrl_contract.simple_read(contract_id)

    method = data['method']
    if 'params' in data:
        params = data['params']
    else:
        params = list()

    chain_name = contract['catalog']['name']
    if chain_name == 'eth':
        result = ex_ethereum.contract_call(contract, method, params)
        return {
            'result': result
        }
    else:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)


def tx_estimate(contract_id, sender_address, data):
    # secret.verify_msg(data)

    tx, contract = tx_create(contract_id, sender_address, data)

    main_contract = ctrl_contract.get_main_of_chain(contract['catalog']['cid'])

    decimals = main_contract['decimals']
    precision = main_contract.get('precision', decimals)

    amount = tx['gas'] * tx['gasPrice']
    return {
        'amount': CoinNum(amount).set(decimals, precision),
        'symbol': main_contract['symbol'].upper()
    }


def transfer_miner_fei(contract_id, sender_address, data):
    # secret.verify_msg(data)

    data['method'] = 'transfer'
    data['params'] = [data['to'], int(data['value'])]

    mf = tx_estimate(contract_id, sender_address, {
        'method': 'transfer',
        'params': [data['to'], int(data['value'])]
    })
    mf['amount'] = mf['amount'].group()
    return mf


def transfer(contract_id, sender_address, data):
    """
    转账交易广播（属交易的一种，是tx_cast方法的特例）
    """
    password = secret.verify_msg(data)

    data['method'] = 'transfer'
    data['params'] = [data['to'], int(data['value'])]

    tx, contract = tx_create(contract_id, sender_address, data)
    # 广播交易
    signed = in_ethereum.sign_tx(sender_address, tx, password)
    tx_hash = ex_ethereum.send_raw_tx(signed['rawTransaction'])
    # 返回交易详情
    cid = contract['catalog']['cid']
    return tx_info(cid, tx_hash)


def tx_cast(contract_id, sender_address, data):
    """
    通用交易广播
    """
    password = secret.verify_msg(data)

    tx, contract = tx_create(contract_id, sender_address, data)
    # 广播交易
    signed = in_ethereum.sign_tx(sender_address, tx, password)
    tx_hash = ex_ethereum.send_raw_tx(signed['rawTransaction'])
    # 返回交易详情
    cid = contract['catalog']['cid']
    return tx_info(cid, tx_hash)


def tx_create(contract_id, sender_address, data):
    contract = ctrl_contract.simple_read(contract_id)

    contract_type = contract['type']
    chain_name = contract['catalog']['name']
    if chain_name not in ['eth']:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)

    params = data.get('params')
    if 'params' is None:
        raise ErrException(ERROR.E40000, extra='not params field')

    # 如果参数中有地址，则进行转换
    for i, v in enumerate(params):
        if in_ethereum.is_address(v):
            params[i] = in_ethereum.to_crc_address(v)

    if contract_type == 'main':
        tx = ex_ethereum.create_tx(sender_address, params[0], params[1])
    elif contract_type == 'ERC20':
        method = data.get('method')
        if 'method' is None:
            raise ErrException(ERROR.E40000, extra='not method field')

        nonce = ex_ethereum.get_tx_count(sender_address)
        gas_price = ex_ethereum.get_gas_price()
        tx = ex_ethereum.contract_create_tx(contract, method, params, {
            'from': in_ethereum.to_crc_address(sender_address),
            'gasPrice': gas_price,
            'nonce': nonce
        })
    else:
        raise ErrException(ERROR.E40000, extra='invalid contract type: %s' % contract_type)

    return tx, contract


def tx_list(cid, address):
    address = address.lower()

    c = ctrl_catalog.simple_read(cid)
    chain_type = c['name']

    cond = {'chain_type': chain_type,
            'chain_name': ex_ethereum.chain,
            '$or': [
                {'from': address},
                {'to': address}
            ]}
    if chain_type == 'eth':
        the_last = db.transaction.find_one(cond, {'_id': 0, 'blockNumber': 1, 'synced_block_number': 1, 'synced': 1})
        if the_last is None:
            synced_block_number = 0
            synced = 0
        else:
            synced = the_last.get('synced', 0)
            if 'synced_block_number' not in the_last:
                synced_block_number = the_last['blockNumber']
            else:
                synced_block_number = the_last['synced_block_number']
        block_number = ex_ethereum.block_number()

        now = time.millisecond()
        if ex_ethereum.chain == 'main' and block_number > synced_block_number and now - synced > 30000:
            start = synced_block_number + 1
            http_client = httpclient.HTTPClient()
            try:
                url = 'http://api.etherscan.io/api?module=account&action=txlist&address={}&startblock={}&' \
                      'sort=desc&apikey=AHCCB5IKCR1RM49ZC5R2TD453DUHVC747V'
                url = url.format(address, start)
                response = http_client.fetch(url)
                response = json.loads(response.body)

                if response['status'] == '1':
                    items = response['result']
                    for item in items:
                        item['chain_type'] = chain_type
                        item['chain_name'] = ex_ethereum.chain
                        if 'from' in item:
                            item['from'] = item['from'].lower()
                        if 'to' in item:
                            item['to'] = item['to'].lower()
                        if 'blockNumber' in item:
                            item['blockNumber'] = int(item['blockNumber'])
                        if 'transactionIndex' in item:
                            item['transactionIndex'] = int(item['transactionIndex'])
                        if 'timeStamp' in item:
                            item['timeStamp'] = int(item['timeStamp'])
                        if 'confirmations' in item:
                            item.pop('confirmations')

                        try:
                            db.transaction.insert_one(item)
                        except Exception:
                            pass
                elif response['status'] == '0' and response['message'] == 'No transactions found':
                    if the_last is not None:
                        temp = {
                            # 减10目的是为了防止etherscan服务同步链上数据时间误差
                            'synced_block_number': max(block_number - 10, synced_block_number),
                            'synced': now
                        }
                        db.transaction.update_one(cond, {'$set': temp})
                else:
                    raise ErrException(ERROR.E50000, extra='error from etherscan: %s' % response['message'])

            except httpclient.HTTPError as e:
                logging.exception(e)
                raise ErrException(ERROR.E50000, extra=e)
            except Exception as e:
                raise ErrException(ERROR.E50000, extra=e)
            finally:
                http_client.close()

        cursor = db.transaction.find(cond, {
            '_id': 0, 'chain_type': 0, 'chain_name': 0, 'synced_block_number': 0, 'synced': 0
        })
        return list(cursor)
    else:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_type)


def tx_info(cid, tx_hash):
    c = ctrl_catalog.simple_read(cid)
    chain_name = c['name']

    if chain_name == 'eth':
        tx = ex_ethereum.get_tx(tx_hash)

        sender = tx.pop('from')
        ret = {
            'hash': tx.pop('hash'),
            'blockHash': tx.pop('blockHash'),
            'blockNumber': tx.pop('blockNumber'),
            'gas': tx.pop('gas'),
            'gasPrice': tx.pop('gasPrice'),
            'nonce': tx.pop('nonce'),
            'sender': sender,
            'from': sender
        }

        if tx['input'] == '0x':
            ret['to'] = tx.pop('to')
            ret['value'] = tx.pop('value')

            cnt = db.contract.find_one({'catalog': bson_id(cid), 'type': 'main'})
            ret['symbol'] = cnt['symbol']
            ret['type'] = cnt['type']
            ret['contract_id'] = json_id(cnt['_id'])
        else:
            # 此交易是合约交易
            contract_address = tx.pop('to')

            cnt = db.contract.find_one({'spec.address': contract_address.lower()})
            if cnt is None:
                raise ErrException(ERROR.E50000, extra='unknown contract address: %s' % contract_address)
            contract = in_ethereum.get_contract(contract_address, cnt['spec']['data'])
            abi_result = decode_abi_result(contract, tx['input'])

            contract_type = cnt['type']
            if contract_type == 'ERC20':
                method = abi_result['method']
                params = abi_result['params']
                if method == 'transfer' and len(params) >= 2:
                    ret['to'] = params[0]
                    ret['value'] = params[1]
                elif method == 'transferFrom' and len(params) >= 3:
                    ret['from'] = params[0]
                    ret['to'] = params[1]
                    ret['value'] = params[2]
                elif method == 'loan' and len(params) >= 3:
                    ret['to'] = params[0]
                    ret['value'] = params[1]
                    ret['charge'] = params[2]
                elif method == 'repay' and len(params) >= 2:
                    ret['to'] = contract_address
                    ret['value'] = params[0]
                    ret['charge'] = params[1]

            ret['symbol'] = cnt['symbol']
            ret['type'] = contract_type
            ret['contract_id'] = json_id(cnt['_id'])
            ret['contract_address'] = contract_address

            tx['abi_result'] = abi_result

        ret['extra'] = tx
        return ret
    else:
        raise ErrException(ERROR.E40000, extra='invalid block-chain: %s' % chain_name)


def decode_abi_result(contract, data):
    data = HexBytes(data)
    selector, params = data[:4], data[4:]
    func = contract.get_function_by_selector(selector)
    types = [x['type'] for x in func.abi['inputs']]
    decoded = decode_abi(types, params)
    return {
        'method': func.fn_name,
        'params': list(decoded)
    }


def verify_password(address, password):
    in_ethereum.sign_msg(address, '', password)
