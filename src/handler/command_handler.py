import json
from util.app_config import AppConfig
from larksuiteoapi import Config
from feishu.message_sender import message_sender
from util.logger import app_logger
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent



class CommandHandler:
    def __init__(self):
        pass

    def handle_command(self, myevent: MyReceiveEvent):
        command = myevent.get_command()
        print('command_handler')


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
        elif command == '1':
            model = "1_3D真人_麦橘写实"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '2':
            model = "2_3D真人_现实主义"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '3':
            model = "3_亚洲一号_AWPortrait"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '4':
            model = "4_亚洲二号_MoyouArtificial"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '5':
            model = "5_万象熔炉_2.5D"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '6':
            model = "6_YesMix_2D"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == '7':
        #     model = "7_hellojplassie_real"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == '8':
            model = "8_CuriousMerge_2.5D"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == '9':
        #     model = "9_colorful_v31_2D"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'a':
            model = "a_awpainting_v11_2D"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
#        elif command == 'b':
#            model = "b_beautifulRealistic_v60"
#            sd_webui.set_model(model)
#            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
#         elif command == 'c':
#             model = "c_cetusMix_Whalefall2"
#             sd_webui.set_model(model)
#             message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'd':
            model = "d_dreamshaper_7"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'e':
            model = "e_deliberate_v2"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'f':
            model = "f_fantasyWorld_v10"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'g':
            model = "g_guofeng_国风3_v34"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'h':
            model = "h_hellojplassie_real"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'i':
        #     model = "i_cetusMix_Whalefall2"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'j':
            model = "j_建筑dvarchMultiPrompt"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'jj':
            model = "jj_建筑architecturerealmix"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'm':
            model = "m_meichidarkMIX38"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'n':
        #     model = "5_2.5D_万象熔炉"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'p':
        #     model = "p_photon_v1_3D"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 's':
            model = "s_shenhua_神话2"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 't':
            model = "t_tmndMixVI_2D"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'u':
            model = "u_unreal_meina_v41"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        elif command == 'y':
            model = "y_yuzu_v11"
            sd_webui.set_model(model)
            message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        # elif command == 'z':
        #     model = "z_建筑dvarchMultiPrompt"
        #     sd_webui.set_model(model)
        #     message_sender.send_text_message(myevent, f'切换模型为: [{model}]')
        else:
            message_sender.send_text_message(myevent, "未知命令，请使用 /help 查看帮助")
            app_logger.info("unknown command")
            
        return True
