import json
import random

LIST_INFO_CARD = {
    "config": {"wide_screen_mode": True},
    "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": "根据的描述得到如下结果:"}}],
}

str_arr = [
    "variant",
    "scale",
    "Face restoration",
    "Size",
    "Model hash",
    "Model",
    "Seed resize from",
    "Denoising strength",
    "Clip skip",
    "Steps",
    "Sampler",
    "Seed",
    "Negative prompt",
    "prompt",
    "negative_prompt",
]
def handle_list_info_card(LIST_INFO_CARD, list):
    LIST_INFO_CARD["elements"] = []
    for item in list:
        element = {
            "tag": "div",
            "text": {"tag": "lark_md", "content": json.dumps(item)},
        }
        LIST_INFO_CARD["elements"].append(element)
    return LIST_INFO_CARD
print('模    块: message_card - format_input_str')
def handle_infotexts(obj):
    # 获取 Model 信息并将其作为一个新的字段添加到对象中
    model_info = ''
    for text in obj['infotexts']:
        if 'Model: ' in text:
            model_info = text.split('Model: ')[1].split(',')[0]
    # del obj['infotexts']
    # del obj['all_prompts']
    # del obj['all_negative_prompts']
    # del obj['all_seeds']
    # del obj['all_subseeds']
    # del obj['subseed']
    # del obj['subseed_strength']
    # del obj['seed_resize_from_w']
    # del obj['seed_resize_from_h']
    # del obj['job_timestamp']
    # del obj['extra_generation_params']
    # del obj['is_using_inpainting_conditioning']
    # del obj['index_of_first_image']
    obj['model'] = model_info
    def format_input_str(input_str, str_arr):
        for key in str_arr:
            input_str = input_str.replace(key + ':', '\n **【' + key + '】** ')
        return input_str
    # 格式化字符串
    formatted_str = format_input_str('', obj.keys())
    for key, value in obj.items():
        formatted_str += '\n **【' + key + '】** ' + str(value).replace('<', ' &lt ').replace('>', ' &gt ')
#        print('模    块: message_card - formatted_str')
#        print(formatted_str)
    return formatted_str
def handle_image_card(image_info, img_key_list, prompt):
#   elements = [
#       {"tag": "column_set", "flex_mode": "none", "background_style": "default", "columns": []},
#   ]
    elements = []

    for index, img_key in enumerate(img_key_list):
# 调整lora   options = ['', a, b, c]
        m1_a = '((close up portrait:1)),masterpiece, top quality, best quality,(upper body:1.2), 1girl,'
        m1_b = 'Best quality, masterpiece, ultra high res, (photorealistic:1.4),'
        m1_c = '(score_9,score_8_up,score_7_up),source_anime, '
        m1_d = '(score_9,score_8_up,score_7_up), '
        m1_e = '<lora:add_detail:1>,Best quality, masterpiece, ultra high res, (photorealistic:1.4),'
        m1_f = 'Best quality, masterpiece, ultra high res, (photorealistic:1.4), 1girl, '
        m1_z = '(masterpiece,best quality, ultra realistic,32k,RAW photo,detail skin, 8k uhd, dslr,high quality, film grain:1.5), (close-up:1.2), (upper body:1.2), 1girl,'
        m1_halfbody = '(close up:1.2),' # 已定版
        m1_x = 'anime artwork pixar,3d style,toon,,masterpiece,best quality,good shine,OC rendering,best quality,4K,super detail,'
        # m1_options = [m1_a, m1_b, m1_c, m1_d]
        # random.shuffle(m1_options)
        elements.append(
            {
                "tag": "img",
                "img_key": img_key,
                "alt": {
                    "tag": "plain_text",
                    "content": ""
                },
                "mode": "fit_horizontal",
                "preview": True
            })

        # m1_temple = m1_options.pop()
        # m1_options.insert(0, prompt)
        handle_infotexts(image_info)
        print('模    块: message_card')
        print(f'当前模型: {image_info["model"]}')

        print(f"prompt: {prompt}\n")

        prompt_origin = prompt.replace(m1_a, '').replace(m1_b, '').replace(m1_c, '').replace(m1_d, '').replace(m1_e, '').replace(m1_f, '').replace(m1_z, '').replace(m1_halfbody, '').replace(m1_e, '').replace(m1_x, '').replace(',,,,,,half',"full",)
        print(f"prompt_origin: {prompt_origin}\n")
        if image_info["model"] == "moyou_v1080-none":
            prompt_remix = m1_halfbody + prompt_origin.replace("full", ',,,,,,half')
            # print(f'载入lora: {prompt_remix}')

        elif image_info["model"] == "kimchiMix_v32":
            print ('FFFFFFFF')
            prompt_remix = m1_c + prompt_origin
 
# print(f'载入lora: {prompt_remix}')

        elif image_info["model"] == "PVCStyleModelMovable_pony151":
             prompt_remix = m1_c + prompt_origin 
             #print(f'载入lora: {prompt_remix}')
        
        elif image_info["model"] == "moxiePony_v11":
             prompt_remix = m1_d + prompt_origin 
             #print(f'载入lora: {prompt_remix}')

        elif image_info["model"] == "AWPortrait_v14":
             prompt_remix = m1_z + prompt_origin
             # print(f'载入lora: {prompt_remix}')

        elif image_info["model"] == "1_sdxlUnstableDiffusers_v8HeavensWrathVAE":
             prompt_remix = prompt_origin
             # print(f'载入lora: {prompt_remix}')

        elif image_info["model"] == "xxmix9realistic_v40":
             prompt_remix = m1_e + prompt_origin
             print(f'载入lora: {prompt_remix}')

        elif image_info["model"] == "majicMIX realistic 麦橘写实_v7":
             prompt_remix = m1_d + prompt_origin
             print(f'载入lora: {prompt_remix}')

        elif image_info["model"] == "亚洲一号_AWPortraitv13":
            prompt_remix = m1_d +  m1_a + prompt_origin
            # print(f'载入lora: {prompt_remix}')

        else:
               prompt_remix = prompt_origin
               # print(f'手气之前：{prompt_remix}')
        elements.append({
            "tag": "action",

            "actions": [
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "重新生成"
                    },
                    "type": "primary",
                    "value": {
                        "type": "reload",
                        "prompt": prompt_remix,
              #          "negative_prompt": negative_prompt,


                    }
                }
            ]
        })
        
        result = {"config": {"wide_screen_mode": True}, "elements": elements}
        # print(f'手气之后：{prompt}')

    return result


