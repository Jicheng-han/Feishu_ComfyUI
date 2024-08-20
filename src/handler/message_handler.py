import os
import json
import random
import uuid
import aiohttp
import asyncio
from feishu.message_sender import message_sender
from feishu.data_transfer import upload_image
from service.generate_config import TextToImageConfig
from feishu.message_card import handle_image_card
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent
from service.aliyun_translator import aliyun_translator
from enum import Enum
import aiofiles

import urllib.request
import urllib.parse


server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())
 
class MessageHandler:
  def __init__(self):
    pass

  async def update_prompt(self, data, new_prompt):
    for key, value in data.items():
      if isinstance(value, dict) and 'inputs' in value:
        inputs = value['inputs']
        if 'prompt' in inputs:
          if isinstance(inputs['prompt'], list):
            inputs['prompt'][0] = new_prompt
          else:
            inputs['prompt'] = new_prompt
    return json.dumps(data, ensure_ascii=False, indent=2)

  async def queue_prompt(self, comfy_prompt):
    p = {"prompt": comfy_prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    async with aiohttp.ClientSession() as session:
      async with session.post(f"http://{server_address}/prompt?token={TOKEN}", data=data) as response:
        return await response.json()

  async def get_image(self, filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    async with aiohttp.ClientSession() as session:
      async with session.get(f"http://{server_address}/?{url_values}&token={TOKEN}") as response:
        return await response.text()

  async def get_history(self, prompt_id):
    async with aiohttp.ClientSession() as session:
      async with session.get(f"http://{server_address}/history/{prompt_id}?token={TOKEN}") as response:
        return await response.json()

  async def get_queue(self):
    async with aiohttp.ClientSession() as session:
      async with session.get(f"http://{server_address}/queue") as response:
        return await response.json()

  async def get_images(self, ws, prompt):
    prompt_id = await self.queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
      out = await ws.recv()
      if isinstance(out, str):
        message = json.loads(out)
        if message['type'] == 'executing':
          data = message['data']
          if data['node'] is None and data['prompt_id'] == prompt_id:
            break
      else:
        continue

    history = await self.get_history(prompt_id)
    for o in history['outputs']:
      for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'images' in node_output:
          images_output = []
          for image in node_output['images']:
            image_data = await self.get_image(image['filename'], image['subfolder'], image['type'])
            images_output.append(image_data)
          output_images[node_id] = images_output

    return output_images

  async def handle_prompt(self, prompts):
    gen_cfg = TextToImageConfig()
    gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts))
    prompt_input = gen_cfg.prompt

    comfy_json = """

          {
            "5": {
              "inputs": {
                "width": 768,
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
                  "61",
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
                "noise_seed": 111230751805892
              },
              "class_type": "RandomNoise",
              "_meta": {
                "title": "RandomNoise"
              }
            },
            "61": {
              "inputs": {
                "prompt": "用英文扩写下面的内容,包括细节描写,艺术风格,大师作品,高质量和细节，并精简成一段话,不超过100个单词:一个女孩",
                "debug": "enable",
                "url": "http://127.0.0.1:11434",
                "model": "phi3:14b",
                "keep_alive": 60
              },
              "class_type": "OllamaGenerate",
              "_meta": {
                "title": "Ollama Generate"
              }
            }
          }
    """

    comfy_prompt = json.loads(comfy_json, strict=False)
    pre_prompt = "Directly translate into English, output the translated content directly, without the translation process:" + prompt_input + ""
    comfy_prompt["61"]["inputs"]["prompt"] = pre_prompt

    comfy_prompt["25"]["inputs"]["noise_seed"] = random.randint(0, 1000000000000000)

    result = await self.queue_prompt(comfy_prompt)
    prompt_id = result['prompt_id']

    await asyncio.sleep(0.5)

    while True:
      queue = await self.get_queue()
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
        print("Prompt not finished yet. Sleeping for 2 seconds.")
        await asyncio.sleep(2)
      else:
        break

    info = await self.get_history(prompt_id)
    history = info[prompt_id]
    output_images = {}
    image_data = None

    for o in history['outputs']:
      for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'images' in node_output:
          images_output = []
          for image in node_output['images']:
            async with aiofiles.open('/opt/ComfyUI/output/' + image['filename'], 'rb') as f:
              image_data = await f.read()
            images_output.append(image_data)
          output_images[node_id] = images_output

    images_key = []
    if output_images is not None:
      for img_data in output_images['9']:
        images_key.append(upload_image(img_data))
    else:
      print("Error: 'images' key not found in result")

    return handle_image_card({'model': 'abcd', 'infotexts': []}, images_key, prompts)

  async def handle_message(self, myevent: MyReceiveEvent):
    message_sender.send_text_message(myevent, "ComfyUI正在处理您的请求，请稍等")

    print(f'模    块: messageCard:{await self.handle_prompt(myevent.text)}')
    messageCard = await self.handle_prompt(myevent.text)

    return message_sender.send_message_card(myevent, messageCard)
