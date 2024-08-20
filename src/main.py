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
def ping():
    return "pong", 200

@app.route("/webhook/card", methods=["POST"])
def webhook_card():
    asyncio.create_task(handle_webhook_card(request))
    return jsonify({}), 200

async def handle_webhook_card(request):
    print('模    块: main.py - webhook_card: 试试手气')
    data = await request.get_data()
    oapi_request = OapiRequest(
        uri=request.path, body=data, header=OapiHeader(request.headers)
    )
    oapi_resp = handle_card(feishu_conf, oapi_request)
    data_dict = json.loads(oapi_request.body)
    print(f"handle_webhook_card_oapi_request.body: {oapi_request.body}")
    print(f"handle_webhook_card_data_dict: {data_dict}")

@app.route("/webhook/event", methods=["POST"])
def webhook_event():
    print('模    块: main.py - webhook_event: 直接输入')
    data = request.get_data()
    oapi_request = OapiRequest(
        uri=request.path, body=data, header=OapiHeader(request.headers)
    )
    event_data = request.json
    # 打印接收到的事件数据
    print("Received event data:", event_data)

    # 处理事件数据的业务逻辑
    # 例如，可以根据 event_data 中的 event_id 或 uuid 做幂等处理

    oapi_resp = handle_event(feishu_conf, oapi_request)
    return jsonify({"message": "OK"}), 200

def app_main():
    app.run(host="0.0.0.0", port=app_config.HTTP_PORT)
    print('模    块: main.py - app_main')

if __name__ == "__main__":
    with app.app_context():
        app_main()