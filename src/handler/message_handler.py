import os
import json
import random
# import websocket #NOTE: websocket-client (GitHub - websocket-client/websocket-client: WebSocket client for Python)
import uuid
import json
import urllib.request
import urllib.parse
import asyncio
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
from enum import Enum

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

    async def handle_update_message_card(self, token, openId, prompt):
      prompt = prompt + "retry_update_prompt"
      messageCard = self.handle_prompt(prompt)
      if messageCard is None:
        print("handle_prompt returned None")
        return None
      messageCard["open_ids"] = [openId]
      print(f'模    块: message_handler - handle_update_message_card')
      await asyncio.sleep(0)  # Return 200 status code before continuing execution
      return message_sender.update_message_card(token, messageCard)
    def update_prompt(self, data, new_prompt):
      for key, value in data.items():
        if isinstance(value, dict) and 'inputs' in value:
          inputs = value['inputs']
          if 'prompt' in inputs:
            if isinstance(inputs['prompt'], list):
              # 如果 prompt 是一个列表，我们假设第一个元素是实际的 prompt
              inputs['prompt'][0] = new_prompt
            else:
              inputs['prompt'] = new_prompt
      return json.dumps(data, ensure_ascii=False, indent=2)

      return "未找到包含 'prompt' 的 'inputs' 字典"
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

    def get_queue(self):
        req = urllib.request.Request("http://{}/queue".format(server_address))
        return json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

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
        # print (f'PPPPPPPPrompt: {prompt_input}')
        comfy_json = """

        {
          "225": {
            "inputs": {
              "width": 832,
              "height": 1216,
              "batch_size": 1
            },
            "class_type": "EmptyLatentImage",
            "_meta": {
              "title": "Empty Latent Image"
            }
          },
          "226": {
            "inputs": {
              "text": [
                "250",
                0
              ],
              "speak_and_recognation": null,
              "clip": [
                "230",
                0
              ]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {
              "title": "CLIP Text Encode (Prompt)"
            }
          },
          "227": {
            "inputs": {
              "samples": [
                "232",
                0
              ],
              "vae": [
                "229",
                0
              ]
            },
            "class_type": "VAEDecode",
            "_meta": {
              "title": "VAE Decode"
            }
          },
          "229": {
            "inputs": {
              "vae_name": "ae.sft"
            },
            "class_type": "VAELoader",
            "_meta": {
              "title": "Load VAE"
            }
          },
          "230": {
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
          "231": {
            "inputs": {
              "unet_name": "flux1-dev.safetensors",
              "weight_dtype": "default"
            },
            "class_type": "UNETLoader",
            "_meta": {
              "title": "Load Diffusion Model"
            }
          },
          "232": {
            "inputs": {
              "noise": [
                "236",
                0
              ],
              "guider": [
                "235",
                0
              ],
              "sampler": [
                "233",
                0
              ],
              "sigmas": [
                "234",
                0
              ],
              "latent_image": [
                "225",
                0
              ]
            },
            "class_type": "SamplerCustomAdvanced",
            "_meta": {
              "title": "SamplerCustomAdvanced"
            }
          },
          "233": {
            "inputs": {
              "sampler_name": "euler"
            },
            "class_type": "KSamplerSelect",
            "_meta": {
              "title": "KSamplerSelect"
            }
          },
          "234": {
            "inputs": {
              "scheduler": "simple",
              "steps": 25,
              "denoise": 1,
              "model": [
                "231",
                0
              ]
            },
            "class_type": "BasicScheduler",
            "_meta": {
              "title": "BasicScheduler"
            }
          },
          "235": {
            "inputs": {
              "model": [
                "231",
                0
              ],
              "conditioning": [
                "226",
                0
              ]
            },
            "class_type": "BasicGuider",
            "_meta": {
              "title": "BasicGuider"
            }
          },
          "236": {
            "inputs": {
              "noise_seed": 80602891815753
            },
            "class_type": "RandomNoise",
            "_meta": {
              "title": "RandomNoise"
            }
          },
          "250": {
            "inputs": {
              "prompt": [
                "251",
                0
              ],
              "debug": true,
              "url": "http://127.0.0.1:11434",
              "model": "phi3:14b",
              "system": "",
              "seed": 231576411,
              "top_k": 40,
              "top_p": 0.9,
              "temperature": 0.8,
              "num_predict": -1,
              "tfs_z": 1,
              "keep_alive": 0,
              "keep_context": false,
              "speak_and_recognation": true
            },
            "class_type": "OllamaGenerateAdvance",
            "_meta": {
              "title": "Ollama Generate Advance"
            }
          },
          "251": {
            "inputs": {
              "text": "You prompt text here",
              "speak_and_recognation": null
            },
            "class_type": "TextInput_",
            "_meta": {
              "title": "提示词输入"
            }
          },
          "257": {
            "inputs": {
              "filename_prefix": "ComfyUI",
              "images": [
                "227",
                0
              ]
            },
            "class_type": "SaveImage",
            "_meta": {
              "title": "Save Image"
            }
          }
        }
        """
        comfy_prompt = json.loads(comfy_json, strict=False)
        if "retry_update_prompt" in prompt_input:
          pre_prompt = "You are a highly imaginative AI art assistant, skilled in describing various scenes to be used as prompts for stable diffusion. I will provide you  a description, and I'd like you to pay special attention to the style of the image I describe. You need to describe the image according to the style I provide, keeping the main content of the scene as close to my description as possible. For secondary elements like backgrounds, you can use your imagination to enrich the overall scene. It's crucial to use very detailed language, building upon the original meaning with intricate artistic techniques to describe the image. Focus on expressing emotions, rendering artistic atmosphere, describing artistic scenes, constructing artistic details, creating artistic themes, describing colors and using professional color applications, choosing perspectives worthy of high-end commercial shots, varying viewpoints freely, and incorporating composition changes inspired by fashion magazine covers. The text must be written in complete paragraphs without titles, section breaks, or numbering. Finally, please output the prompt in professional English:" + prompt_input.replace("retry_update_prompt","")
        else:
          pre_prompt = "Directly translate into English, output the translated content directly, without the translation process:" + prompt_input
        comfy_prompt["251"]["inputs"]["text"] = pre_prompt
        # comfy_prompt = self.update_prompt(comfy_prompt, pre_prompt)
        # print (f'CCCCCCCCCCComfy_prompt:{comfy_prompt}')
        # set the seed for our KSampler node
        comfy_prompt["236"]["inputs"]["noise_seed"] = random.randint(0, 1000000000000000)            
        comfy_prompt["250"]["inputs"]["seed"] = random.randint(0, 2147483647)      
        result = self.queue_prompt(comfy_prompt)
        # print(f"Resultzzzzzzzzzzzzzzzzzzzzzzzzzzzzz: {result}")
        prompt_id = result['prompt_id']
        # print(f"Prompt ID: {prompt_id}")
        # 先倒头就睡0.5秒，确保任务提交到队列
        time.sleep(0.5)

        while True:
            queue = self.get_queue()
            prompt_finish_flag = True
            if len(queue["queue_running"]) == 0:
                break

            for item in queue["queue_running"]:
                if len(item) > 0 and item[1] == prompt_id:
                    prompt_finish_flag = False
                    continue

            for item in queue["queue_pending"]:
                if len(item) > 0 and item[1] == prompt_id:
                    prompt_finish_flag = False
                    continue

            if not prompt_finish_flag:
                # print("Prompt not finished yet. Sleeping for 2 seconds.")
                time.sleep(2)
            else:
                break

        info = self.get_history(prompt_id)
        history = info[prompt_id]
        output_images = {}
        image_data = None
        # print(f"Info: {info}")
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


        images_key = []
        if output_images is not None:
            for img_data in output_images['257']:
                images_key.append(upload_image(img_data))
        else:
            print("Error: 'images' key not found in result")

        return handle_image_card({'model': 'abcd','infotexts': []}, images_key, prompts)

    def handle_message(self, myevent: MyReceiveEvent):
        message_sender.send_text_message(myevent,"ComfyUI正在处理您的请求，请稍等")

        # print(f'模    块: messageCard:{self.handle_prompt(myevent.text)}') 
        messageCard = self.handle_prompt(myevent.text)

        return message_sender.send_message_card(myevent, messageCard)