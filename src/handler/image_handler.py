from util.logger import app_logger
from feishu.data_transfer import upload_image, get_message_resource
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent
from feishu.message_card import handle_image_card
from service.generate_config import ImageToImageConfig
from feishu.message_sender import message_sender
from PIL import Image
from io import BytesIO
import webuiapi

api = webuiapi.WebUIApi()


class ImageHandler:
    def __init__(self) -> None:
        pass

    def img2txt(self, img) -> str:
        result = sd_webui.interrogate(img)
        print(f'模    块: image_handler - img2txt', result['info'])  # Added closing parenthesis
        return result['info']

    # 根据指令生成不同的消息卡片
    def img2img(self, img, prompts):
        imginfo = sd_webui.interrogate(img)
        print(f'模    块: image_handler - img2img', imginfo['info'])  # Added closing parenthesis
        # unit1 = webuiapi.ControlNetUnit(input_image=img, module='instant_id_face_embedding', model='ip-adapter_instant_id_sdxl',control_mode=2,lowvram=True)
        # unit2 = webuiapi.ControlNetUnit(input_image=img, module='instant_id_face_keypoints', model='control_instant_id_sdxl',lowvram=True, weight=0.5)
        # # unit1 = webuiapi.ControlNetUnit(input_image=img, module='canny', model='diffusers_xl_canny_mid',lowvram=True)
        # unit2 = webuiapi.ControlNetUnit(input_image=img, module='depth', model='diffusers_xl_depth_mid',lowvram=True, weight=0.5)


        # unit1 = webuiapi.ControlNetUnit(input_image = Image.open(r'D:\\Feishu-Stablediffusion-master\\src\\demo.jpg'), module='ip-adapter_clip_sdxl', model='ip-adapter_xl',lowvram=True)
        # unit2 = webuiapi.ControlNetUnit(input_image=img, module='canny', model='diffusers_xl_canny_mid',lowvram=True)
        # print(unit1)
        # print(unit2)
        gen_cfg = ImageToImageConfig(images=[img])
        gen_cfg.resize_mode = 2
        # gen_cfg.controlnet_units = [unit1, unit2]
        gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts))
        # print(sd_webui.img2img(gen_cfg))
        result = sd_webui.img2img(gen_cfg)
        images_key = []
        for img_data in result['images']:
            images_key.append(upload_image(img_data))
        return handle_image_card(result['info'], images_key, prompts)


    def handle_image(self, myevent: MyReceiveEvent):
        if myevent.image_key is None:
            return False

        img = get_message_resource(myevent.get_message_id(), myevent.image_key)
        img = Image.open(BytesIO(img))
        imginfo = sd_webui.interrogate(img)
        clip_prompt = imginfo['info']

        # img2img with multiple ControlNets (used 1.0 but also supports 1.1)
 

        # if myevent.text is None:
        #     message_sender.send_text_message(myevent, f"正在以图生文，{sd_webui.queue()}")
        #     clip_info_en = self.img2txt(img)
        #     clip_info_cn = ts.translate_text(clip_info_en, translator='alibaba', from_language='en', to_language='zh-cn')
        #     # interrogate_result = api.interrogate(image=img, model="deepdanbooru")
        # interrogate_result = api.interrogate(image=img, model="clip")
        # prompt = interrogate_result.info
        # print(prompt)
        #     return message_sender.send_text_message(myevent, f'英文：{clip_info_en}\n中文：{clip_info_cn}')
        # else:
        plus_prompt = "Illustration, highres, original, extremely detailed wallpaper, perfect lighting,"
        if not myevent.text:
            # Handle the case where myevent.text is empty
            # For example, you might want to set a default value
            myevent.text = ""
        message_sender.send_text_message(myevent, f"正在以图生图，{sd_webui.queue()}")
        # messageCard = self.img2img(img,myevent.text+imginfo['info'])
        messageCard = self.img2img(img,myevent.text+","+clip_prompt )
        # messageCard = self.img2img(img,"Illustration,(masterpiece:1,2), best quality, masterpiece, highres, original, extremely detailed wallpaper, perfect lighting,(extremely detailed CG:1.2), drawing,")
        # interrogate_result = api.interrogate(image=img, model="deepdanbooru")
        # # also you can use clip. clip is set by default
        # #interrogate_result = api.interrogate(image=img, model="clip")
        # #interrogate_result = api.interrogate(image=img)

        # prompt = interrogate_result.info
        # prompt

        # # OR    
        # print(prompt)
        # print(messageCard)
        # print(messageCard)
        return message_sender.send_message_card(myevent, messageCard)
