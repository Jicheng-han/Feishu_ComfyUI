import json

from larksuiteoapi import Config

from feishu.message_sender import message_sender
from feishu.data_transfer import upload_image
from service.generate_config import TextToImageConfig
from feishu.message_card import handle_image_card
from feishu.message_card import handle_infotexts
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent

class MessageHandler:
    def __init__(self):
        pass

    def handle_update_message_card(self, token, openId, prompt):
        messageCard = self.handle_prompt(prompt)
        messageCard["open_ids"] = [openId]
        print(f'模    块: message_handler - handle_update_message_card')
#        print(f'当前VAE: {sd_webui.get_sd_vae}')
        return message_sender.update_message_card(token, messageCard)

    # 根据指令生成不同的消息卡片
    def handle_prompt(self, prompts):
        gen_cfg = TextToImageConfig()
        gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts))
        model = sd_webui.get_model()[0:sd_webui.get_model().index(".")]
        models = ["5_beautifulRealistic_v7xxx","6_majicmixRealistic_v7","4_真人_麦橘写实V25","moomoofusion_v40Female","极氪写实MAX-白白酱_V6剪树枝版"]
        if model in models:
            gen_cfg.width = 512
            gen_cfg.height = 768
            gen_cfg.enable_hr = True
            gen_cfg.denoising_strength = 0.05  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
            gen_cfg.cfg_scale = 7
            gen_cfg.hr_upscaler= "4x-UltraSharp"
            gen_cfg.restore_faces= True
            gen_cfg.hr_scale = 1.5
            gen_cfg.steps = 30
            gen_cfg.hr_second_pass_steps = 15
       #     gen_cfg.sampler_name="Euler a"
            gen_cfg.negative_prompt = 'ng_deepnegative_v1_75t, (badhandv4:1.2), (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, ((monochrome)), ((grayscale)) watermark, moles, large breast, big breast  '

        elif(model == "a_墨幽人造人_v1060修复"):
            gen_cfg.width = 512
            gen_cfg.height = 768
            gen_cfg.enable_hr = True
            gen_cfg.denoising_strength = 0.05  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
            gen_cfg.cfg_scale = 7
            gen_cfg.hr_upscaler= "4x-UltraSharp"
            gen_cfg.restore_faces= True
            gen_cfg.hr_scale = 1.5
            gen_cfg.steps = 30
            gen_cfg.hr_second_pass_steps = 15
            gen_cfg.sampler_name="Restart"
            gen_cfg.negative_prompt = 'ng_deepnegative_v1_75t, (badhandv4:1.2), (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, ((monochrome)), ((grayscale)) watermark, moles, '

        elif(model == "y_Yesmix_v30"):
            gen_cfg.width = 544
            gen_cfg.height = 816
            gen_cfg.enable_hr = True
         #   gen_cfg.restore_faces= True
            gen_cfg.hr_scale = 1.5
            gen_cfg.steps = 30
            gen_cfg.hr_second_pass_steps = 15
            gen_cfg.hr_upscaler="R-ESRGAN 4x+ Anime6B"
            gen_cfg.cfg_scale = 8

        elif(model == "s_sdvn6Realxl_detailfacexxx"):
            gen_cfg.width = 768
            gen_cfg.height = 1162
            gen_cfg.steps = 60
            gen_cfg.enable_hr=False

        elif(model == "b_starlightXLAnimated_v3"):
            gen_cfg.width = 832
            gen_cfg.height = 1248
            gen_cfg.sampler_name="DPM++ 3M SDE Karras"
            gen_cfg.cfg_scale = 3.6
            negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"

        elif(model == "3_juggernautXL_version5"):
            gen_cfg.width = 832
            gen_cfg.height = 1216
        # elif(model == "2_realvisxlV20_v20Bakedvae"):
        #     gen_cfg.enable_hr = True
        #     gen_cfg.denoising_strength = 0.1  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
        #     gen_cfg.cfg_scale = 7
        #     gen_cfg.hr_upscaler= "4x-UltraSharp"
        #     gen_cfg.hr_scale = 1.1
        #     gen_cfg.steps = 30
        #     gen_cfg.hr_second_pass_steps = 15
        # elif(model == "2_3D真人_女孩半身像"):
        #     gen_cfg.sampler_name="Restart"
        #     gen_cfg.steps = 40

        print(f'模    块: message_handler - handle_prompt')

        result = sd_webui.txt2img(gen_cfg)

        images_key = []
        for img_data in result['images']:
            images_key.append(upload_image(img_data))
        return handle_image_card(result['info'], images_key, prompts)

    def handle_message(self, myevent: MyReceiveEvent):
        message_sender.send_text_message(myevent, f"{sd_webui.queue()}")
        messageCard = self.handle_prompt(myevent.text)
        print(f'模    块: message_handler - handle_message')
        print('------------------------------------------------------')

        return message_sender.send_message_card(myevent, messageCard)
