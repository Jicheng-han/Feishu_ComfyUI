from time import sleep
import sys
sys.path.append("D:\\Feishu-Stablediffusion-master\\src\\")
from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.model import OapiHeader, OapiRequest
from flask import Flask, jsonify, request
from flask.helpers import make_response
from larksuiteoapi.service.im.v1.event import MessageReceiveEventHandler
from larksuiteoapi.model.oapi_response import OapiResponse
from message_router import route_im_message
from message_action import action_im_message, delayedUpdateMessageCard
from feishu.feishu_conf import feishu_conf
from util.app_config import app_config
from threading import Thread
import asyncio
from aiohttp import web
import json
from handler.menu_event_handler import MenuHandler
from feishu.message_sender import MessageSender
import queue
import threading

MessageReceiveEventHandler.set_callback(feishu_conf, route_im_message)
set_card_callback(feishu_conf, action_im_message)
app = Flask("feishu_sd_bot")

# 参考 https://github.com/larksuite/oapi-sdk-python/blob/main/README.zh.md
@app.route("/", methods=["GET", "POST"])

async def ping(request):
    return web.Response(text="pong", status=200)

async def webhook_card(request):
    return await handle_webhook_card(request)

async def handle_webhook_card(request):
    print('模    块: main.py - webhook_card: 试试手气')
    data = await request.read()
    oapi_request = OapiRequest(
        uri=request.path, body=data, header=OapiHeader(request.headers)
    )
    oapi_resp = handle_card(feishu_conf, oapi_request)
    data_dict = json.loads(oapi_request.body)
    print(f"handle_webhook_card_oapi_request.body: {oapi_request.body}")
    print(f"handle_webhook_card_data_dict: {data_dict}")
    return web.Response(headers={'Content-Type': 'application/json'}, text="", status=200)

async def webhook_event(request):
    event_data = await request.json()
    print("Received event data:", event_data)
    
    # 处理事件数据的业务逻辑
    # 例如，可以根据 event_data 中的 event_id 或 uuid 做幂等处理

    oapi_resp = handle_event(feishu_conf, OapiRequest)
    print("Event handled, sending response")
    return web.Response(headers={'Content-Type': 'application/json'}, text="", status=200)

async def handle_webhook_event(request):
    print('模    块: main.py - webhook_event: 直接输入')
    data = await request.read()
    oapi_request = OapiRequest(
        uri=request.path, body=data, header=OapiHeader(request.headers)
    )
    event_data = await request.json()
    # 打印接收到的事件数据
    print("Received event data:", event_data)
    
    # 处理事件数据的业务逻辑
    # 例如，可以根据 event_data 中的 event_id 或 uuid 做幂等处理

    oapi_resp = handle_event(feishu_conf, oapi_request)
    return web.Response(headers={'Content-Type': 'application/json'}, text="", status=200)

def app_main():
    app = web.Application()
    app.add_routes([web.get('/', ping),
                    web.route('*','/webhook/card', webhook_card),
                    web.route('*', '/webhook/event', webhook_event)])
    web.run_app(app, host="0.0.0.0", port=app_config.HTTP_PORT)
    print('模    块: main.py - app_main')

if __name__ == "__main__":
    app_main()