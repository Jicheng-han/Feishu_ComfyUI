import json

def update_prompt(data, new_prompt):
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

# 您提供的 JSON 数据
json_data = {'5': {'inputs': {'width': 1024, 'height': 1024, 'batch_size': 1}, 'class_type': 'EmptyLatentImage', '_meta': {'title': 'Empty Latent Image'}}, '6': {'inputs': {'text': ['61', 0], 'speak_and_recognation': None, 'clip': ['11', 0]}, 'class_type': 'CLIPTextEncode', '_meta': {'title': 'CLIP Text Encode (Prompt)'}}, '8': {'inputs': {'samples': ['13', 0], 'vae': ['10', 0]}, 'class_type': 'VAEDecode', '_meta': {'title': 'VAE Decode'}}, '9': {'inputs': {'filename_prefix': 'MarkuryFLUX', 'images': ['8', 0]}, 'class_type': 'SaveImage', '_meta': {'title': 'Save Image'}}, '10': {'inputs': {'vae_name': 'ae.sft'}, 'class_type': 'VAELoader', '_meta': {'title': 'Load VAE'}}, '11': {'inputs': {'clip_name1': 't5xxl_fp16.safetensors', 'clip_name2': 'clip_l.safetensors', 'type': 'flux'}, 'class_type': 'DualCLIPLoader', '_meta': {'title': 'DualCLIPLoader'}}, '12': {'inputs': {'unet_name': 'flux1-dev.safetensors', 'weight_dtype': 'default'}, 'class_type': 'UNETLoader', '_meta': {'title': 'Load Diffusion Model'}}, '13': {'inputs': {'noise': ['25', 0], 'guider': ['22', 0], 'sampler': ['16', 0], 'sigmas': ['17', 0], 'latent_image': ['5', 0]}, 'class_type': 'SamplerCustomAdvanced', '_meta': {'title': 'SamplerCustomAdvanced'}}, '16': {'inputs': {'sampler_name': 'euler'}, 'class_type': 'KSamplerSelect', '_meta': {'title': 'KSamplerSelect'}}, '17': {'inputs': {'scheduler': 'simple', 'steps': 25, 'denoise': 1, 'model': ['12', 0]}, 'class_type': 'BasicScheduler', '_meta': {'title': 'BasicScheduler'}}, '22': {'inputs': {'model': ['12', 0], 'conditioning': ['6', 0]}, 'class_type': 'BasicGuider', '_meta': {'title': 'BasicGuider'}}, '25': {'inputs': {'noise_seed': 111230751805892}, 'class_type': 'RandomNoise', '_meta': {'title': 'RandomNoise'}}, '61': {'inputs': {'prompt': '用英文扩写下面的内容,包括细节描写,艺术风格,大师作品,高质量和细节，并精简成一段话,不超过100个单词:一个女孩', 'debug': 'enable', 'url': 'http://127.0.0.1:11434', 'model': 'llava:7b', 'keep_alive': 60}, 'class_type': 'OllamaGenerate', '_meta': {'title': 'Ollama Generate'}}}

if __name__ == '__main__':
    # 调用函数并打印结果
    pre_prompt = "Expand the following content in English, including detailed descriptions, artistic style, masterful works, high quality, and intricate details, and condense it into a single paragraph of no more than 100 words:" + "一个女孩"

    result = update_prompt(json_data, pre_prompt)
    print(result)
