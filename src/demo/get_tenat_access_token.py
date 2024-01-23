from time import sleep

from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.model import OapiHeader, OapiRequest
from flask import Flask, request
from flask.helpers import make_response
from larksuiteoapi.service.im.v1.event import MessageReceiveEventHandler
from larksuiteoapi.model.oapi_response import OapiResponse
from message_router import route_im_message
from message_action import action_im_message, delayedUpdateMessageCard
from feishu.feishu_conf import feishu_conf
from util.app_config import app_config
from threading import Thread
import asyncio
# from aiohttp import web
import json
from handler.menu_event_handler import MenuHandler
from feishu.message_sender import MessageSender
import logging

# Create a custom logger
# logger = logging.getLogger(__name__)

# Create handlers
# c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler('file.log')
# c_handler.setLevel(logging.WARNING)
# f_handler.setLevel(logging.ERROR)
# Create formatters and add it to handlers
# c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# c_handler.setFormatter(c_format)
# f_handler.setFormatter(f_format)
# Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)
MessageReceiveEventHandler.set_callback(feishu_conf, route_im_message)
set_card_callback(feishu_conf, action_im_message)
app = Flask("feishu_sd_bot")

# 参考 https://github.com/larksuite/oapi-sdk-python/blob/main/README.zh.md
@app.route("/", methods=["GET", "POST"])
def ping():
    resp = make_response()
    resp.data = "pong"
    resp.status_code = 200
    return resp

@app.route("/webhook/card", methods=["POST"])
def webhook_card():
    oapi_request = OapiRequest(
        uri=request.path, body=request.data, header=OapiHeader(request.headers)
    )
    resp = make_response()
    oapi_resp = handle_card(feishu_conf, oapi_request)
    resp.headers["Content-Type"] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp

@app.route("/webhook/event", methods=["GET", "POST"])
def webhook_event():
    oapi_request = OapiRequest(
        uri=request.path, body=request.get_data(), header=OapiHeader(dict(request.headers))
    )
    resp = make_response()
    oapi_resp = handle_event(feishu_conf, oapi_request)

    # Parse the request body as a JSON object
    data_dict = json.loads(oapi_request.body)
    # print(f"oapi_request.body: {oapi_request.body}")

    # Extract the event_type and event_key values
    event_type = data_dict.get("header", {}).get("event_type")
    event = data_dict.get("event", {})
    operator = event.get("operator") if event else None
    operator_id = operator.get("operator_id") if operator else None
    user_id = operator_id.get("user_id") if operator_id else None
    
    event_type = data_dict.get("header", {}).get("event_type")
    event_key = data_dict.get("event", {}).get("event_key")
    #
    print(f"event_type: {event_type}")
    print(f"event_key: {event_key}")

    # menu_response =  MenuHandler.handle_menu_event(uuid = data_dict.get("event", {}).get("union_id"),user_id = data_dict.get("event", {}).get("user_id"),event_key = data_dict.get("event", {}).get("event_key"))
    # logger.info('webhook_event function called')
    # ... rest of your code ...
    menu_response =  MenuHandler.handle_menu_event(user_id,event_key,event_type)
    # logger.info('MenuHandler.handle_menu_event function finished')
    # print (user_id)
    # print (event_key)
    resp.headers["Content-Type"] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp

def app_main():
    app.run(host="0.0.0.0", port=app_config.HTTP_PORT)

if __name__ == "__main__":
    app_main()

# async def webhook_event(request):
#     print('模    块: main.py - webhook_event: 直接输入')
#     data = await request.read()
#     oapi_request = OapiRequest(
#         uri=request.path, body=data, header=OapiHeader(request.headers)
#     )
#     oapi_resp = handle_event(feishu_conf, oapi_request)

#     # Parse the request body as a JSON object
#     data_dict = json.loads(oapi_request.body)
#     print(f"oapi_request.body: {oapi_request.body}")
#     # Extract the event_type and event_key values
#     event_type = data_dict.get("header", {}).get("event_type")
 
 
#     event = data_dict.get("event", {})
#     operator = event.get("operator") if event else None
#     operator_id = operator.get("operator_id") if operator else None
#     user_id = operator_id.get("user_id") if operator_id else None
    
#     event_type = data_dict.get("header", {}).get("event_type")
#     event_key = data_dict.get("event", {}).get("event_key")
#     #
#     print(f"event_type: {event_type}")
#     print(f"event_key: {event_key}")
 

#     # menu_response =  MenuHandler.handle_menu_event(uuid = data_dict.get("event", {}).get("union_id"),user_id = data_dict.get("event", {}).get("user_id"),event_key = data_dict.get("event", {}).get("event_key"))
#     menu_response =  MenuHandler.handle_menu_event(user_id,event_key,event_type)
 

#     print (user_id)
#     print (event_key)
#     return menu_response

#     #
#     # return web.Response(headers={'Content-Type': oapi_resp.content_type}, text="", status=oapi_resp.status_code)


# def app_main():
#     app = web.Application()
#     app.add_routes([web.get('/', ping),
#                     web.route('*','/webhook/card', handle_webhook_card),
#                     web.route('*', '/webhook/event', webhook_event)])
#     web.run_app(app, host="0.0.0.0", port=app_config.HTTP_PORT)
#     print('模    块: main.py - app_main')



# if __name__ == "__main__":
#     app_main()
