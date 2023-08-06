# coding:utf-8

from .. import ctrl_product
from asyncio import get_event_loop


async def create(cid, prod_meta, *auth_args):
    args = (cid, prod_meta, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_product.create, *args)


async def read(cid, pid, *auth_args):
    args = cid, pid, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_product.read, *args)


async def update(cid, pid, prod_meta, *auth_args):
    args = cid, pid, prod_meta, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_product.update, *args)


async def change_status(cid, pid, action, *auth_args):
    args = cid, pid, action, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_product.change_status, *args)


async def move(cid, pid, cid_to, *auth_args):
    args = cid, pid, cid_to, *auth_args
    return await get_event_loop().run_in_executor(None, ctrl_product.move, *args)


async def query_products(cid, page_no, page_size, *auth_args):
    args = (cid, page_no, page_size, *auth_args)
    return await get_event_loop().run_in_executor(None, ctrl_product.query_products, *args)
