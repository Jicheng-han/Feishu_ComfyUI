import json
from util.app_config import AppConfig
#from larksuiteoapi import Config
from feishu.message_sender import message_sender
from util.logger import app_logger
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent
#from lark_oapi.api.application.v6.model.p2_application_bot_menu_v6 import P2ApplicationBotMenuV6



class CommandHandler:
    def __init__(self):
        pass

    def handle_command(self, myevent: MyReceiveEvent):
        command = myevent.get_command()
        print('command_handler')
        options = {}
        options['sd_vae'] = 'vae-ft-mse-840000-ema-pruned.safetensors'
        options_xl = {}
        options_xl['sd_vae'] = 'sdxl_vae.safetensors'
        options_Y = {}
        options_Y['sd_vae'] = 'finalPruneVAE_v10.pt'
        options_xl2 = {}
        options_xl2['sd_vae'] = 'xlVAEC_c9.safetensors'
        options_none = {}
        options_none['sd_vae'] = 'None'

        if command == 'help':
            # message_sender.send_text_message(myevent, sd_webui.help())
            message_sender.send_message_card(myevent,sd_webui.helpCard())
            app_logger.info(f"command /help")
        elif command == 'm':
            message_sender.send_text_message(myevent, sd_webui.list_models())
            app_logger.info(f"command /list_models")
        elif command == 'list_models':
#            message_sender.send_text_message_hanjicheng(myevent, '你好', 'SD')
            message_sender.send_message_card(myevent,sd_webui.list_models_card())
            app_logger.info(f"command /list_models")

        elif command == 'list_samplers':
            message_sender.send_text_message(myevent, sd_webui.list_samplers())
            app_logger.info(f"command /list_samplers")
        elif command == 'list_upscalers':
            message_sender.send_text_message(myevent, sd_webui.list_upscalers())
            app_logger.info(f"command /list_upscalers")
        elif command == 'list_controlnet_modules':
            message_sender.send_text_message(myevent, sd_webui.list_controlnet_modules())
            app_logger.info(f"command /list_controlnet_modules")
        elif command == 'list_controlnet_models':
            message_sender.send_text_message(myevent, sd_webui.list_controlnet_models())
            app_logger.info(f"command /list_controlnet_models")
        elif command == 'refresh_models':
            sd_webui.refresh_models()
            message_sender.send_text_message(myevent, '模型列表已刷新')
            app_logger.info(f"command /refresh_models")
        elif command == 'host_info':
            message_sender.send_text_message(myevent, sd_webui.host_info())
            app_logger.info(f"command /host_info")
        elif command == 'queue':
            message_sender.send_text_message(myevent, sd_webui.queue())
            app_logger.info(f"command /queue")
        elif command == 'model':
            model = myevent.get_command_args()
            if model is None:
                model = sd_webui.get_model()
                message_sender.send_text_message(myevent, f'当前模型为: [{model}]')
            else:
                print(model)
                print(myevent)
                sd_webui.set_model(model)
                message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == '0':
        #     model = "BDicon_SDXL_三维图标大模型_v1.0"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == '00':
        #     model = "counterfeitxl_v10"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')

        elif command == '1':
            model = "1_排名第一模型_Crystal"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '2':
            model = "2_realvisxlV20_v20Bakedvae"
            sd_webui.set_model(model)
            sd_webui.set_options(options_none)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '3':
            model = "3_juggernautXL_version5"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl2)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '4':
            model = "4_sdvn7Nijistylexl_v1"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl2)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '5':
            model = "5_beautifulRealistic_v7"
            sd_webui.set_model(model)
            sd_webui.set_options(options)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '6':
            model = "6_majicmixRealistic"
            sd_webui.set_model(model)
            sd_webui.set_options(options)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == '6':
        #     model = "6_BDicon_SDXL_三维图标大模型_v1.0"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == '7':
        #      model = "7_sdvn7Nijistylexl_v1"
        #      sd_webui.set_model(model)
        #      sd_webui.set_options(options_xl2)
        #      message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '8':
            model = "8_counterfeitxl_v10.5D"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl2)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == '9':
        #     model = "9_墨幽人造人_v1040精简"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'a':
            model = "a_墨幽人造人_v1060修复"
            sd_webui.set_model(model)
            sd_webui.set_options(options)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'b':
            model = "b_starlightXLAnimated_v3"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'c':
        #      model = "c_卡通二号_特化可爱风格"
        #      sd_webui.set_model(model)
        #      message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'd':
            model = "d_卡通3D_duchaitenAiartSDXL_v10"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl2)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'e':
        #     model = "e_deliberate_v2"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'f':
        #     model = "f_fantasyWorld_v10"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'g':
        #     model = "g_guofeng_国风3_v34"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'l':
            model = "lzSDXL_v10"
            sd_webui.set_model(model)
            sd_webui.set_options(options_none)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'i':
        #     model = "i_cetusMix_Whalefall2"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'j':
        #     model = "j_建筑dvarchMultiPrompt"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'jj':
        #     model = "jj_建筑architecturerealmix"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')

        # elif command == 'n':
        #     model = "5_2.5D_万象熔炉"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'o':
        #     model = "o_onlyrealistic_v30BakedVAE"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 's':
            model = "s_sdvn6Realxl_detailface"
            sd_webui.set_model(model)
            sd_webui.set_options(options_xl2)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 't':
        #     model = "t_tmndMixVI_2D"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'u':
        #     model = "u_unreal_meina_v41"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'y':
            model = "y_Yesmix_v30"
            sd_webui.set_model(model)
            sd_webui.set_options(options_Y)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'z':
        #     model = "z_建筑dvarchMultiPrompt"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        else:
            message_sender.send_text_message(myevent, "未知命令，请使用 /help 查看帮助")
            app_logger.info("unknown command")
            
        return True
