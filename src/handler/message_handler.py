
import webuiapi
import json
import random
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse

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

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())
# TOKEN is stored in the file `./PASSWORD`, or you can obtain it from the command line window when ComfyUI starts.
# It will appear like this:
# For direct API calls, token=$2b$12$qUfJfV942nrMiX77QRVgIuDk1.oyXBP7FYrXVEBqouTk.uP/hiqAK
TOKEN = "$2b$12$FoR7ezNDPAPYaG2kit0aLuV9YsmSefGZyTx6rV3QcE1K6qUH5qeAm"
# If you get errors like: HTTP Error 400: Bad Request, please check the server's console for more detailed error message.
# Sometimes it's related to the model file's filename.

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

    # def queue_prompt(self,comfy_prompt):
    #     p = {"prompt": comfy_prompt}
    #     data = json.dumps(p).encode('utf-8')
    #     # print(f"oooooxxxxxxxxxxxxxx:{data}")
    #     req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    #     s = request.urlopen(req) 
    #     print(f"request:{s}")
    #     request.urlopen(req)
    def queue_prompt(self,comfy_prompt):
        p = {"prompt": comfy_prompt, "client_id": client_id}
        data = json.dumps(p).encode('utf-8')
        req =  urllib.request.Request("http://{}/prompt?token={}".format(server_address, TOKEN), data=data)
        return json.loads(urllib.request.urlopen(req).read())
    
    def get_image(self,filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}&token={}".format(server_address, url_values, TOKEN)) as response:
            return response.read()

    def get_history(self,prompt_id):
        with urllib.request.urlopen("http://{}/history/{}?token={}".format(server_address, prompt_id, TOKEN)) as response:
            return json.loads(response.read())


    def get_images(self, prompt_id):
        history = self.get_history(prompt_id)[prompt_id]
        output_images = {}
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output
        return output_images

  
    # 根据指令生成不同的消息卡片

    def handle_prompt(self, prompts):
        gen_cfg = TextToImageConfig()
        gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts))
        prompt_input = gen_cfg.prompt
        print(f'Prompt: {prompt_input}')
        
        comfy_json = """
        {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "cfg": 8,
                    "denoise": 1,
                    "latent_image": [
                        "5",
                        0
                    ],
                    "model": [
                        "4",
                        0
                    ],
                    "negative": [
                        "7",
                        0
                    ],
                    "positive": [
                        "6",
                        0
                    ],
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "seed": 8566257,
                    "steps": 20
                }
            },
            "4": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "anything-v5-PrtRE.safetensors"
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "batch_size": 1,
                    "height": 512,
                    "width": 512
                }
            },
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": [
                        "4",
                        1
                    ],
                    "text": "masterpiece best quality girl"
                }
            },
            "7": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "clip": [
                        "4",
                        1
                    ],
                    "text": "bad hands"
                }
            },
            "8": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": [
                        "3",
                        0
                    ],
                    "vae": [
                        "4",
                        2
                    ]
                }
            },
            "9": {
                "class_type": "SaveImage",
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": [
                        "8",
                        0
                    ]
                }
            }
        }
        """

    
       
        comfy_prompt = json.loads(comfy_json)
        comfy_prompt["6"]["inputs"]["text"] = prompt_input
        print(f'Comfy_prompt: {comfy_prompt}')

        comfy_prompt["3"]["inputs"]["seed"] = random.randint(0, 1000000000000000)            

        result = self.queue_prompt(comfy_prompt)
        print(f"Result_queue_prompt: {result}")

        result_images = self.get_images(result['prompt_id'])
        print(f"result_images: {result_images}")

        result_history = self.get_history(result['prompt_id'])
        print(f"result_history: {result_history}")

        # 处理图像上传
        images_key = []
        for node_id, images in result_images.items():
            for img_data in images:
                images_key.append(upload_image(img_data))

        # 假设 handle_image_card 函数需要这些参数
        return handle_image_card(result_history, images_key, prompts)


    def handle_message(self, myevent: MyReceiveEvent):
        message_sender.send_text_message(myevent,"ComfyUI正在处理您的请求，请稍等")

        print(f'模    块: messageCard:{self.handle_prompt(myevent.text)}') 
        messageCard = self.handle_prompt(myevent.text)

        return message_sender.send_message_card(myevent, messageCard)
