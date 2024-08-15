import os
import json
import random
# import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
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

    def handle_update_message_card(self, token, openId, prompt):
        messageCard = self.handle_prompt(prompt)
        if messageCard is None:
            print("handle_prompt returned None")
            return None
        messageCard["open_ids"] = [openId]
        print(f'模    块: message_handler - handle_update_message_card')
#        print(f'当前VAE: {sd_webui.get_sd_vae}')
        return message_sender.update_message_card(token, messageCard)
    def update_prompt(self,data, new_prompt):
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
        print (f'PPPPPPPPrompt: {prompt_input}')

        workflowResult = get_workflow_by_name("高级文生图")
        pre_prompt = "Expand the following content in English, including detailed descriptions, artistic style, masterful works, high quality, and intricate details, and condense it into a single paragraph of no more than 100 words:" + prompt_input

        print (f'wwwwwwwwwwwwwwworkflowResult: {workflowResult}')
        workflowJson = json.dumps(workflowResult.data)

        print (f'wwwwwwwwwwwwwwworkflowJson: {workflowJson}')
        comfy_prompt = self.update_prompt(json.loads(workflowJson), pre_prompt)

        print (f'CCCCCCCCCCComfy_prompt:{comfy_prompt}')

        # set the seed for our KSampler node
        comfy_prompt["25"]["inputs"]["noise_seed"] = random.randint(0, 1000000000000000)            

        result = self.queue_prompt(comfy_prompt)
        print(f"Resultzzzzzzzzzzzzzzzzzzzzzzzzzzzzz: {result}")
        prompt_id = result['prompt_id']
        print(f"Prompt ID: {prompt_id}")
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
                print("Prompt not finished yet. Sleeping for 2 seconds.")
                time.sleep(2)
            else:
                break

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

class WorkFlow:
    def __init__(self, display_name, file_path):
        self.display_name = display_name
        self.file_path = file_path
        self.data = self.load_json()

    def load_json(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

def create_workflow_enum(directory):
    workflows = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            name = os.path.splitext(filename)[0]
            file_path = os.path.join(directory, filename)
            workflows[name.upper()] = (name, file_path)

    class WorkFlows(Enum):
        def __new__(cls, display_name, file_path):
            obj = object.__new__(cls)
            obj._value_ = display_name
            obj.display_name = display_name
            obj.file_path = file_path
            obj.data = WorkFlow.load_json(obj)
            return obj

        @classmethod
        def load_json(cls, obj):
            with open(obj.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)

    return WorkFlows('WorkFlows', workflows)

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构造 workflow 目录的路径
workflow_dir = os.path.join(current_dir, 'workflow')

# 确保 workflow 目录存在
if not os.path.exists(workflow_dir):
    raise FileNotFoundError(f"Workflow directory not found: {workflow_dir}")

# 创建 WorkFlows 枚举
WorkFlows = create_workflow_enum(workflow_dir)

# 打印所有工作流
def print_all_workflows():
    for wf in WorkFlows:
        print(f"{wf.display_name}: {wf.file_path}")
        # 如果需要，你也可以打印 JSON 数据
        # print(f"Data: {wf.data}")

# 根据名称获取工作流
def get_workflow_by_name(name):
    for wf in WorkFlows:
        if wf.display_name == name:
            return wf
    return None
