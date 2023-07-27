from time import sleep

from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.model import OapiHeader, OapiRequest
from flask import Flask, request
from flask.helpers import make_response
from larksuiteoapi.service.im.v1.event import MessageReceiveEventHandler

from message_router import route_im_message
from message_action import action_im_message, delayedUpdateMessageCard
from feishu.feishu_conf import feishu_conf
from util.app_config import app_config
from threading import Thread
import asyncio
from aiohttp import web

MessageReceiveEventHandler.set_callback(feishu_conf, route_im_message)
set_card_callback(feishu_conf, action_im_message)
app = Flask("feishu_sd_bot")

# 参考 https://github.com/larksuite/oapi-sdk-python/blob/main/README.zh.md
@app.route("/", methods=["GET", "POST"])

async def ping(request):
    return web.Response(text="pong", status=200)

async def handle_webhook_card(request):
    print('模    块: main.py - webhook_card: 试试手气')
    data = await request.read()
    oapi_request = OapiRequest(
        uri=request.path, body=data, header=OapiHeader(request.headers)
    )
    oapi_resp = handle_card(feishu_conf, oapi_request)
    print(f'webhook_card.content_type: {oapi_resp.content_type}')
    print(f'webhook_card.status_code: {oapi_resp.status_code}')

async def webhook_card(request):
    asyncio.create_task(handle_webhook_card(request))
    return web.Response(headers={'Content-Type': 'application/json'}, text="", status=200)
# async def webhook_card(request):
#     print('模    块: main.py - webhook_card: 试试手气')
#     data = await request.read()
#     oapi_request = OapiRequest(
#         uri=request.path, body=data, header=OapiHeader(request.headers)
#     )
#
#     oapi_resp = handle_card(feishu_conf, oapi_request)
#     print(f'webhook_card.content_type: {oapi_resp.content_type}')
#     print(f'webhook_card.status_code: {oapi_resp.status_code}')
#     return web.Response(headers={'Content-Type': oapi_resp.content_type}, text="", status=oapi_resp.status_code)


async def webhook_event(request):
    print('模    块: main.py - webhook_event: 直接输入')
    data = await request.read()
    oapi_request = OapiRequest(
        uri=request.path, body=data, header=OapiHeader(request.headers)
    )
    oapi_resp = handle_event(feishu_conf, oapi_request)
    print(f'webhook_event.content_type: {oapi_resp.content_type}')
    print(f'webhook_event.status_code: {oapi_resp.status_code}')
    return web.Response(headers={'Content-Type': oapi_resp.content_type}, text="", status=oapi_resp.status_code)

def app_main():
    app = web.Application()
    app.add_routes([web.get('/', ping),
                    web.route('*','/webhook/card', webhook_card),
                    web.route('*', '/webhook/event', webhook_event)])
    web.run_app(app, host="0.0.0.0", port=app_config.HTTP_PORT)
    print('模    块: main.py - app_main')



if __name__ == "__main__":
    app_main()
