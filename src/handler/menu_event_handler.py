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


class MenuHandler:
    def handle_menu_event(event_key):

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
        send_message_response = '切换完成'
        if event_key == "b_starlightXLAnimated":
            response_text = "切换模型：b_starlightXLAnimated_v3"
            print(response_text)
            model = "b_starlightXLAnimated_v3"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)
            response_text = "切换模型：b_starlightXLAnimated_v3"
        elif event_key == "1_sdxlUnstableDiffusers":
            response_text = "切换模型：1_sdxlUnstableDiffusers_v8HeavensWrathVAE"
            print(response_text)
            model = "1_sdxlUnstableDiffusers_v8HeavensWrathVAE"
            sd_webui.set_model(model)
            sd_webui.set_options(options_none)
        elif event_key == "MR_3DQ _SDXL":
            response_text = "切换模型：MR_3DQ _SDXL_V0.2"
            print(response_text)
            model = "MR_3DQ _SDXL_V0.2"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)
        elif event_key == "a_moyou":
            response_text = "切换模型：a_moyou_v1060"
            print(response_text)
            model = "a_moyou_v1060"
            sd_webui.set_model(model)
            sd_webui.set_options(options)
        elif event_key == "1_xxmix9realisticsdxl":
            response_text = "切换模型：1_xxmix9realisticsdxl_v10"
            print(response_text)
            model = "1_xxmix9realisticsdxl_v10"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)
        elif event_key == "1_xxmix9realisticsdxl":
            response_text = "切换模型：1_xxmix9realisticsdxl_v10"
            print(response_text)
            model = "1_xxmix9realisticsdxl_v10"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)

        elif event_key == "future":
            response_text = "切换模型：dreamshaperXL_turboDpmppSDEKarras"
            print(response_text)
            model = "dreamshaperXL_turboDpmppSDEKarras"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl2)

            return send_message_response
