
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
import time
from service.aliyun_translator import aliyun_translator

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

    def queue_prompt(self,comfy_prompt):
        p = {"prompt": comfy_prompt, "client_id": client_id}
        data = json.dumps(p).encode('utf-8')
        req =  urllib.request.Request("http://{}/prompt?token={}".format(server_address, TOKEN), data=data)
        return json.loads(urllib.request.urlopen(req).read())
    
    def get_image(self,filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/?{}&token={}".format(server_address, url_values, TOKEN)) as response:
            print(f'reponse========:{response.read().decode("utf-8")}')
            return response.read().decode("utf-8")

    def get_history(self,prompt_id):
        with urllib.request.urlopen("http://{}/history/{}?token={}".format(server_address, prompt_id, TOKEN)) as response:
            return json.loads(response.read())
         
    def get_images(self,ws, prompt):
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        output_images = {}
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
            else:
                continue #previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for o in history['outputs']:
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
        gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts)) #处理prompt串
        prompt_input = gen_cfg.prompt
        print (f'PPPPPPPPrompt: {prompt_input}')
        
        comfy_json = """


{
  "5": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "6": {
    "inputs": {
      "text": [
        "62",
        0
      ],
      "speak_and_recognation": null,
      "clip": [
        "11",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "13",
        0
      ],
      "vae": [
        "10",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": "MarkuryFLUX",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "10": {
    "inputs": {
      "vae_name": "ae.sft"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "Load VAE"
    }
  },
  "11": {
    "inputs": {
      "clip_name1": "t5xxl_fp16.safetensors",
      "clip_name2": "clip_l.safetensors",
      "type": "flux"
    },
    "class_type": "DualCLIPLoader",
    "_meta": {
      "title": "DualCLIPLoader"
    }
  },
  "12": {
    "inputs": {
      "unet_name": "flux1-dev.safetensors",
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "Load Diffusion Model"
    }
  },
  "13": {
    "inputs": {
      "noise": [
        "25",
        0
      ],
      "guider": [
        "22",
        0
      ],
      "sampler": [
        "16",
        0
      ],
      "sigmas": [
        "17",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "SamplerCustomAdvanced",
    "_meta": {
      "title": "SamplerCustomAdvanced"
    }
  },
  "16": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "KSamplerSelect"
    }
  },
  "17": {
    "inputs": {
      "scheduler": "simple",
      "steps": 25,
      "denoise": 1,
      "model": [
        "12",
        0
      ]
    },
    "class_type": "BasicScheduler",
    "_meta": {
      "title": "BasicScheduler"
    }
  },
  "22": {
    "inputs": {
      "model": [
        "12",
        0
      ],
      "conditioning": [
        "6",
        0
      ]
    },
    "class_type": "BasicGuider",
    "_meta": {
      "title": "BasicGuider"
    }
  },
  "25": {
    "inputs": {
      "noise_seed": 187180102399976
    },
    "class_type": "RandomNoise",
    "_meta": {
      "title": "RandomNoise"
    }
  },
  "60": {
    "inputs": {
      "image": "pasted/image (716).png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Flux 效果展示"
    }
  },
  "61": {
    "inputs": {
      "text": [
        "62",
        0
      ],
      "text2": " This is a photograph of three pandas eating steamed buns. The style of the artwork appears to be realistic with fine details, capturing the essence of the animals and their environment. The high-quality image showcases the exquisite craftsmanship of the artist, who has skillfully rendered the textures and colors in a lifelike manner. "
    },
    "class_type": "ShowText|pysssss",
    "_meta": {
      "title": "Show Text"
    }
  },
  "62": {
    "inputs": {
      "prompt": "用英文扩写下面的内容,包括细节描写,艺术风格,大师作品,高质量和细节,\n并精简成一段话,不超过50个单词:\n\n一张三只熊猫在吃烧烤的照片",
      "debug": "enable",
      "url": "http://127.0.0.1:11434",
      "model": "llava:7b",
      "keep_alive": 60,
      "speak_and_recognation": null
    },
    "class_type": "OllamaGenerate",
    "_meta": {
      "title": "Ollama Generate"
    }
  }
}
        """

        comfy_prompt = json.loads(comfy_json, strict=False)
        #set the text prompt for our positive CLIPTextEncode

        comfy_prompt["62"]["inputs"]["prompt"] = "用英文扩写下面的内容,包括细节描写,艺术风格,大师作品,高质量和细节,并精简成一段话,不超过50个单词:" + prompt_input
        print (f'CCCCCCCCCCComfy_prompt:{comfy_prompt}')

        #set the seed for our KSampler node
        comfy_prompt["25"]["inputs"]["noise_seed"] = random.randint(0, 1000000000000000)            

        result = self.queue_prompt(comfy_prompt)
        print(f"Resultzzzzzzzzzzzzzzzzzzzzzzzzzzzzz: {result}")
        prompt_id = result['prompt_id']
        print(f"Prompt ID: {prompt_id}")
        time.sleep(30)
        info = self.get_history(prompt_id)
        history = info[prompt_id]
        output_images = {}
        image_data = None
        print(f"Info: {info}")
        for o in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                if 'images' in node_output:
                    images_output = []
                    for image in node_output['images']:
                        print(f"Imagename: {image['filename']}")
                        with open('/opt/ComfyUI/output/' + image['filename'], 'rb') as f:
                            image_data = f.read()
                        # image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                        images_output.append(image_data)
                output_images[node_id] = images_output
        # if result is not None:
        #     if 'images' in result and result['images'] is not None:
        #         for img_data in result['images']:
        #             images_key.append(upload_image(img_data))
        #     else:
        #         print("Error: 'images' key not found in result or its value is None")

        #     if 'info' in result and result['info'] is not None:
        #         return handle_image_card(result['info'], images_key, prompts)
        #     else:
        #         print("Error: 'info' key not found in result or its value is None")
        # else:
        #     print("Error: result is None")
        # print(f"image_data: {image_data}")
        images_key = []
        if output_images is not None:
            for img_data in output_images['9']:
                images_key.append(upload_image(img_data))
        else:
            print("Error: 'images' key not found in result")
        
        return handle_image_card({'model': 'abcd','infotexts': []}, images_key, prompts)

        # print(f"XXXX_images_key_XXXXXX: {result['info'], images_key, prompts}")
        # return handle_image_card(result['info'], images_key, prompts)

    def handle_message(self, myevent: MyReceiveEvent):
        message_sender.send_text_message(myevent,"ComfyUI正在处理您的请求，请稍等")

        print(f'模    块: messageCard:{self.handle_prompt(myevent.text)}') 
        messageCard = self.handle_prompt(myevent.text)

        return message_sender.send_message_card(myevent, messageCard)
