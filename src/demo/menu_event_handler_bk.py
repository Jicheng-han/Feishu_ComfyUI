# # review my code

# from typing import Dict
# from handler.command_handler import CommandHandler
# import json
# from util.app_config import AppConfig
# #from larksuiteoapi import Config
# from feishu.message_sender import message_sender
# from util.logger import app_logger
# from service.stablediffusion import sd_webui
# from util.event_helper import MyReceiveEvent
# from lark_oapi.api.application.v6.model.p2_application_bot_menu_v6 import P2ApplicationBotMenuV6
# from larksuiteoapi.api.request import request
# from larksuiteoapi.card import handle_card, set_card_callback
# from feishu.feishu_conf import feishu_conf
# from util.logger import app_logger
# from service.stablediffusion import sd_webui
# from util.event_helper import MyReceiveEvent
# from lark_oapi.api.application.v6.model.p2_application_bot_menu_v6 import P2ApplicationBotMenuV6
# from handler.command_handler import CommandHandler
# from demo.demo_message import *

 
 


# class MenuHandler:
#    # def handle_menu_event(user_id,event_key,event_type):
#     def handle_menu_event( event_key):

#         # 创建 MyReceiveEvent 对象
#         options = {}
#         options['sd_vae'] = 'vae-ft-mse-840000-ema-pruned.safetensors'
#         options_xl = {}
#         options_xl['sd_vae'] = 'sdxl_vae.safetensors'
#         options_Y = {}
#         options_Y['sd_vae'] = 'finalPruneVAE_v10.pt'
#         options_xl2 = {}
#         options_xl2['sd_vae'] = 'sdxl-vae-fp16-fix.safetensors'
#         options_none = {}
#         options_none['sd_vae'] = 'None'
#         send_message_response = '切换完成'

#         if event_key == "b_starlightXLAnimated":
#             model = "b_starlightXLAnimated_v3"
#             sd_webui.set_model(model)
#             sd_webui.set_options(options_xl)
#             response_text = "3D风格模型 已就位，点击键盘输入提示词"
 
#         elif event_key == "1_sdxlUnstableDiffusers":
#             model = "1_sdxlUnstableDiffusers_v8HeavensWrathVAE"
#             sd_webui.set_model(model)
#             sd_webui.set_options(options_none)
#             response_text = "遥遥领先模型 已就位，点击键盘输入提示词"

 
#         elif event_key == "二次元风格模型":
#             response_text = "二次元风格模型 已就位，点击键盘输入提示词"
#             model = "SDXLAnimeBulldozer_v10"
#             sd_webui.set_model(model)
#             sd_webui.set_options(options_xl)
 
#         elif event_key == "1_xxmix9realisticsdxl":
#             response_text = "真人质感模型 已就位，点击键盘输入提示词"
#             model = "LEOSAM_HelloWorld_Turbo+LCM_3"
#             sd_webui.set_model(model)
#             sd_webui.set_options(options_xl2)
 
#         elif event_key == "future":
#             response_text = "探索未来 已就位，点击键盘输入提示词"
#             model = "dreamshaperXL_turboDpmppSDEKarras"
#             sd_webui.set_model(model)
#             sd_webui.set_options(options_xl2)
 

#         # if event_type == "application.bot.menu_v6" and event_key in ("b_starlightXLAnimated","1_sdxlUnstableDiffusers","二次元风格模型","1_xxmix9realisticsdxl","future",):
#             # menu_respon(user_id,response_text)

#             return send_message_response
