# coding:utf-8

from .. import ctrl_wallet
from asyncio import get_event_loop


async def query_mine(*auth_args):
    args = auth_args
    return await get_event_loop().run_in_executor(None, ctrl_wallet.query_mine, *args)


async def create(contract_id, data, *auth_args):
    args = (contract_id, data, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_wallet.create, *args)


async def remove(contract_id, wallet_id, *auth_args):
    args = (contract_id, wallet_id, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_wallet.remove, *args)


async def balance(contract_id, address):
    args = contract_id, address
    return await get_event_loop().run_in_executor(None, ctrl_wallet.balance, *args)


async def transfer_miner_fei(contract_id, sender_address, data):
    args = contract_id, sender_address, data
    return await get_event_loop().run_in_executor(None, ctrl_wallet.transfer_miner_fei, *args)


async def transfer(contract_id, from_address, data):
    args = contract_id, from_address, data
    return await get_event_loop().run_in_executor(None, ctrl_wallet.transfer, *args)


async def get_tx_info(cid, tx_hash):
    args = cid, tx_hash
    return await get_event_loop().run_in_executor(None, ctrl_wallet.tx_info, *args)


async def get_tx_list(cid, address):
    args = cid, address
    return await get_event_loop().run_in_executor(None, ctrl_wallet.tx_list, *args)


async def view(contract_id, data):
    args = contract_id, data
    return await get_event_loop().run_in_executor(None, ctrl_wallet.view, *args)


async def transaction(contract_id, sender_address, data):
    args = contract_id, sender_address, data
    return await get_event_loop().run_in_executor(None, ctrl_wallet.tx_cast, *args)

