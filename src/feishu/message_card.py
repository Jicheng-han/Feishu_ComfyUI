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
        elements.append({
            "tag": "action",

            "actions": [
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "试试手气 - AI润色 - 30秒"
                    },
                    "type": "primary",
                    "value": {
                        "type": "reload",
                        "prompt": prompt,
              #          "negative_prompt": negative_prompt,


                    }
                }
            ]
        })
 
        
        result = {"config": {"wide_screen_mode": True}, "elements": elements}
        # print(f'手气之后：{prompt}')

    return result


