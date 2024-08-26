import sys
from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.model import OapiHeader, OapiRequest
from aiohttp import web
import asyncio
import json
from message_router import route_im_message
from message_action import action_im_message
from feishu.feishu_conf import feishu_conf
from util.app_config import app_config
from larksuiteoapi.service.im.v1.event import MessageReceiveEventHandler
import asyncio
import logging
from aiohttp import web
import asyncio
from aiohttp import web
 

# 注册事件处理器
MessageReceiveEventHandler.set_callback(feishu_conf, route_im_message)
set_card_callback(feishu_conf, action_im_message)

async def ping(request):
    return web.Response(text="pong", status=200)

async def webhook_card(request):
    # 在返回响应之前读取请求数据
    try:
        data = await request.read()
        # 创建一个异步任务来处理请求数据
        asyncio.create_task(handle_webhook_card(request.path, request.headers, data))
    except Exception:
        pass

    # 立即返回 200 状态码
    return web.Response(headers={'Content-Type': 'application/json'}, text="", status=200)

async def handle_webhook_card(path, headers, data):
    try:
        oapi_request = OapiRequest(
            uri=path, body=data, header=OapiHeader(headers)
        )
        # 使用 asyncio.to_thread 来处理同步函数
        await asyncio.to_thread(handle_card, feishu_conf, oapi_request)
    except Exception:
        pass

async def webhook_event(request):
    # print('模    块: main.py - webhook_event: 直接输入')
    data = await request.read()
    oapi_request = OapiRequest(
        uri=request.path, body=data, header=OapiHeader(request.headers)
    )
    event_data = await request.json()
    # 打印接收到的事件数据
    # print("Received event data:", event_data)

    oapi_resp = handle_event(feishu_conf, oapi_request)
    # print(f"handle_webhook_event_oapi_request.body: {oapi_resp}")
    return web.json_response({"message": "OK"})

def app_main():
    app = web.Application()
    app.add_routes([web.get('/', ping),
                    web.route('*', '/webhook/card', webhook_card),
                    web.route('*', '/webhook/event', webhook_event)])
    web.run_app(app, host="0.0.0.0", port=app_config.HTTP_PORT)

if __name__ == "__main__":
    app_main()