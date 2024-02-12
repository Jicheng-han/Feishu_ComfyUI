# review my code
import sys
import time
sys.path.append("D:\\Feishu-Stablediffusion-master\\src\\")
from typing import Dict
from handler.command_handler import CommandHandler
import json
from util.app_config import AppConfig
#from larksuiteoapi import Config
from feishu.message_sender import message_sender
from util.logger import app_logger
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent
from lark_oapi.api.application.v6.model.p2_application_bot_menu_v6 import P2ApplicationBotMenuV6
from larksuiteoapi.api.request import request
from larksuiteoapi.card import handle_card, set_card_callback
from feishu.feishu_conf import feishu_conf
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent
from lark_oapi.api.application.v6.model.p2_application_bot_menu_v6 import P2ApplicationBotMenuV6
from handler.command_handler import CommandHandler
from demo.demo_message import *
from service.stablediffusion import sd_webui 
 

class MenuHandler:
    processed_requests = set()

    @staticmethod
    def handle_menu_event(user_id, event_key, event_type,timestamp):
        # 如果已经处理过这个请求，直接返回
        if (event_key, timestamp) in MenuHandler.processed_requests:
            return
        # 获取当前时间戳
        current_timestamp = time.time()

        # 如果时间差在2分钟之内

        # 创建 MyReceiveEvent 对象
        options = {}
        options['sd_vae'] = 'vae-ft-mse-840000-ema-pruned.safetensors'
        options_xl = {}
        options_xl['sd_vae'] = 'sdxl_vae.safetensors'
        options_Y = {}
        options_Y['sd_vae'] = 'finalPruneVAE_v10.pt'
        options_xl2 = {}
        options_xl2['sd_vae'] = 'sdxl-vae-fp16-fix.safetensors'
        options_none = {}
        options_none['sd_vae'] = 'None'
        response_text = event_key + " 已就绪，请输入提示词， 出图时间<1分钟"
        # response_text = f'[当前模型:  {event_key}]\n' + "模型切换完成,点击" + "\u2328" + "输入提示词"
        event_key1 = "融合风格模型"
        event_key2 = "现实世界模型"
        event_key3 = "3D风格模型"
        event_key4 = "二次元模型"
        event_key5 = "中国风模型"
        event_key6 = "新技术探索"

        if event_key == event_key1:
            model = "sdxlUnstableDiffusers_v11Rundiffusion"
            sd_webui.set_model(model)
            sd_webui.set_options(options_none)

        elif event_key == event_key2:
            model = "现实世界_newrealityxl_21"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)

        elif event_key == event_key3:
            model = "3D风格_starlightXL_v3"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)

        elif event_key == event_key4:
            model = "sdxl-动漫二次元_1"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)

        elif event_key == event_key5:
            model = "xxmix9realistic_v40"
            sd_webui.set_model(model)
            sd_webui.set_options(options)

        elif event_key == event_key6:
            model = "newrealityxlAllInOne_21"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl2)
 
        if abs(current_timestamp - timestamp) <= 120:
            if event_type == "application.bot.menu_v6" and event_key in (event_key1,event_key2,event_key3,event_key4,event_key5,event_key6):
                menu_respon(user_id,response_text)

         # 将请求添加到已处理请求的集合中
        MenuHandler.processed_requests.add((event_key, timestamp))