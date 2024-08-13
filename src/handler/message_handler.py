
import webuiapi
import json
import random

#from larksuiteoapi import Config
from urllib import request, parse

from feishu.message_sender import message_sender
from feishu.data_transfer import upload_image
from service.generate_config import TextToImageConfig
from feishu.message_card import handle_image_card
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent

api = webuiapi.WebUIApi()

ads = webuiapi.ADetailer(ad_model="face_yolov8n.pt")
class MessageHandler:
    def __init__(self):
        pass

    def handle_update_message_card(self, token, openId, prompt):
        messageCard = self.handle_prompt(prompt)
        if messageCard is None:
            print("handle_prompt returned None")
            return None
        messageCard["open_ids"] = [openId]
        print(f'模    块: message_handler - handle_update_message_card')
#        print(f'当前VAE: {sd_webui.get_sd_vae}')
        return message_sender.update_message_card(token, messageCard)

    def queue_prompt(self,comfy_prompt):
        p = {"prompt": comfy_prompt}
        data = json.dumps(p).encode('utf-8')
        # print(f"oooooxxxxxxxxxxxxxx:{data}")
        req =  request.Request("http://10.131.5.50:8188/prompt", data=data)
        s = request.urlopen(req) 
        print(f"request:{s}")
        request.urlopen(req)


    # 根据指令生成不同的消息卡片
    def handle_prompt(self, prompts):
        gen_cfg = TextToImageConfig()
        gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts)) #处理prompt串
        prompt = gen_cfg.prompt
        print (f'PPPPPPPPrompt: {prompt}')
        
        comfy_json = """
        {
        "3": {
            "inputs": {
            "seed": 230911048911329,
            "steps": 10,
            "cfg": 1.5,
            "sampler_name": "dpmpp_2m",
            "scheduler": "karras",
            "denoise": 0.8,
            "model": [
                "11",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "latent_image": [
                "5",
                0
            ]
            },
            "class_type": "KSampler",
            "_meta": {
            "title": "K采样器"
            }
        },
        "4": {
            "inputs": {
            "ckpt_name": "playground-v2.5-1024px-aesthetic.fp16.safetensors"
            },
            "class_type": "CheckpointLoaderSimple",
            "_meta": {
            "title": "Checkpoint加载器(简易)"
            }
        },
        "5": {
            "inputs": {
            "width": 832,
            "height": 1216,
            "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
            "title": "空Latent"
            }
        },
        "6": {
            "inputs": {
            "text": "",
            "clip": [
                "4",
                1
            ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
            "title": "CLIP文本编码器"
            }
        },
        "7": {
            "inputs": {
            "text": "worst quality, low quality",
            "clip": [
                "4",
                1
            ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
            "title": "CLIP文本编码器"
            }
        },
        "8": {
            "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
            },
            "class_type": "VAEDecode",
            "_meta": {
            "title": "VAE解码"
            }
        },
        "11": {
            "inputs": {
            "sampling": "edm_playground_v2.5",
            "sigma_max": 120,
            "sigma_min": 0.002,
            "model": [
                "4",
                0
            ]
            },
            "class_type": "ModelSamplingContinuousEDM",
            "_meta": {
            "title": "模型连续采样算法EDM"
            }
        },
        "12": {
            "inputs": {
            "images": [
                "8",
                0
            ]
            },
            "class_type": "PreviewImage",
            "_meta": {
            "title": "预览图像"
            }
        },
        "57": {
            "inputs": {
            "image": "20240215-115530.jpg",
            "upload": "image"
            },
            "class_type": "LoadImage",
            "_meta": {
            "title": "加载图像"
            }
        },
        "58": {
            "inputs": {
            "image": "pasted/image (1).png",
            "upload": "image"
            },
            "class_type": "LoadImage",
            "_meta": {
            "title": "加载图像"
            }
        }
        }
        """
 
       
         
        comfy_prompt = json.loads(comfy_json)
        #set the text prompt for our positive CLIPTextEncode

        comfy_prompt["6"]["inputs"]["text"] = prompt
        print (f'CCCCCCCCCCComfy_prompt:{comfy_prompt}')

        #set the seed for our KSampler node
        comfy_prompt["3"]["inputs"]["seed"] = random.randint(0, 1000000000000000)        
 


        result = self.queue_prompt(comfy_prompt)
        # result = sd_webui.txt2img(gen_cfg)
        if result is not None:
            if 'images' in result and result['images'] is not None:
                for img_data in result['images']:
                    images_key.append(upload_image(img_data))
            else:
                print("Error: 'images' key not found in result or its value is None")

            if 'info' in result and result['info'] is not None:
                return handle_image_card(result['info'], images_key, prompts)
            else:
                print("Error: 'info' key not found in result or its value is None")
        else:
            print("Error: result is None")

        images_key = []
        if 'images' in result:
            for img_data in result['images']:
                images_key.append(upload_image(img_data))
        else:
            print("Error: 'images' key not found in result")
        if 'info' in result:
            return handle_image_card(result['info'], images_key, prompts)
        else:
            print("Error: 'info' key not found in result")
        # print(f"XXXXXXXXXX: {result['info'], images_key, prompts}")
        return handle_image_card(result['info'], images_key, prompts)

    def handle_message(self, myevent: MyReceiveEvent):
        message_sender.send_text_message(myevent,"ComfyUI正在处理您的请求，请稍等")

        print(f'模    块: messageCard:{self.handle_prompt(myevent.text)}') 
        messageCard = self.handle_prompt(myevent.text)



        return message_sender.send_message_card(myevent, messageCard)
