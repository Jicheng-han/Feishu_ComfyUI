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
    del obj['infotexts']
    del obj['all_prompts']
    del obj['all_negative_prompts']
    del obj['all_seeds']
    del obj['all_subseeds']
    del obj['subseed']
    del obj['subseed_strength']
    del obj['seed_resize_from_w']
    del obj['seed_resize_from_h']
    del obj['job_timestamp']
    del obj['extra_generation_params']
    del obj['is_using_inpainting_conditioning']
    del obj['index_of_first_image']
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
        m1_a = '(close up:1.2), (portrait:1.2), '
        m1_b = '<lora:add-detail-xl:0.8>,'
        m1_c = 'masterpiece, best quality,  face front, smile, upper body, studio light, studio, side light, makeup portrait, face in center, '
        m1_d = 'mysterious, fantasy,'
        m1_e = 'masterpiece,best quality,realistic,1girl,'
        m1_f = 'Best quality, masterpiece, ultra high res, (photorealistic:1.4), 1girl, '
        m1_z = '(masterpiece,best quality, ultra realistic,32k,RAW photo,detail skin, 8k uhd, dslr,high quality, film grain:1.5),'
        m1_halfbody = '(close up:1.2), (half-body portrait:1.2),'
        m1_x = 'masterpiece, best quality, extremely delicate and beautiful, highres, original,'
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


        prompt_origin = prompt.replace(m1_a, '').replace(m1_b, '').replace(m1_c, '').replace(m1_d, '').replace(m1_f, '').replace(m1_z, '').replace(m1_halfbody, '').replace(m1_e, '').replace(m1_x, '').replace(',,,,,,half',"full",)
        negative_prompt = ""

        if image_info["model"] == "copaxTimelessxlSDXL1_v5":
            prompt_remix = prompt_origin
            negative_prompt = '(unaestheticXLv31:0.6), (worst quality, low quality, illustration, 3d, 2d), open mouth, tooth,ugly face, old face, long neck,'
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "1_排名第一模型_Crystal":
            prompt_remix = prompt_origin
            negative_prompt = 'FastNegative, '
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "a_墨幽人造人_v1060修复":
            prompt_remix = m1_halfbody + prompt_origin.replace("full", ',,,,,,half')
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "2_realvisxlV20_v20Bakedvae":
            prompt_remix = prompt_origin
            negative_prompt = 'FastNegative,wizards staff, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, oil painting, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,'
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "2_3D真人_女孩半身像":
            prompt_remix = prompt_origin
            negative_prompt = 'FastNegative,wizards staff, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, oil painting, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,'
            print(f'载入lora: {prompt_remix}')
        if image_info["model"] == "3_juggernautXL_version5":
            prompt_remix = prompt_origin
            negative_prompt = 'FastNegative,wizards staff, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, oil painting, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,'
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "5_beautifulRealistic_v7":
            prompt_remix = '(masterpiece, top quality, best quality, ' + prompt_origin
            negative_prompt = 'badhandv4, ng_deepnegative_v1_75t,(worst_quality:2.0) (MajicNegative_V2:0.8), BadNegAnatomyV1-neg, bradhands, cartoon, cgi, render, illustration, painting, drawing, sketches,  '
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "5_亚洲一号_AWPortrait":
            prompt_remix = '(masterpiece, top quality, best quality, ' + prompt_origin
            negative_prompt = 'ng_deepnegative_v1_75t, (badhandv4:1.2), (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, ((monochrome)), ((grayscale)) watermark, moles, large breast, big breast  '
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "4_sdvn7Nijistylexl_v1":
            prompt_remix = '' + prompt_origin
            negative_prompt = 'negativeXL_D, noise, grit, dull, washed out, low contrast, blurry, hazy, malformed, warped, deformed, text, watermark, worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch, bad anatomy, bad hands, multiple eyebrow, (cropped), extra limb, missing limbs, deformed hands, long neck, long body, (bad hands), signature, username, artist name, conjoined fingers, deformed fingers, ugly eyes, imperfect eyes, skewed eyes, unnatural face, unnatural body, error, painting by bad-artist",deformed hands, long neck, long body, (bad hands), conjoined fingers, deformed fingers,'
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "4_真人_麦橘写实V25":
            prompt_remix = 'Best quality, masterpiece, ultra high res, (photorealistic:1.4), 1girl, ' + prompt_origin
            negative_prompt = 'badhandv4, ng_deepnegative_v1_75t, BadNegAnatomyV1-neg, (worst quality:2),(low quality:2),(normal quality:2),lowres,watermark,'
            print(f'载入lora: {prompt_remix}')


        if image_info["model"] == "a_3D炫彩_LahMysterious_v40":
            prompt_remix = prompt_origin
            negative_prompt = 'FastNegative, '
            print(f'载入lora: {prompt_remix}')

        if image_info["model"] == "y_Yesmix_v30":
            prompt_remix = '' + prompt_origin
            negative_prompt = 'SimpleNegative_AnimeV1'

        if image_info["model"] == "s_sdvn6Realxl_detailface":
            prompt_remix = '' + prompt_origin
            negative_prompt = 'FastNegative,(worst quality, low quality, illustration, 3d, 2d, painting, cartoons, sketch), tooth, open mouth,'
            print(f'载入lora: {prompt_remix}')
        else:
            prompt_remix = prompt_origin
#            print(f'手气之前：{prompt_remix}')
        elements.append({
            "tag": "action",

            "actions": [
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "试试手气"
                    },
                    "type": "primary",
                    "value": {
                        "type": "reload",
                        "prompt": prompt_remix,
                        "negative_prompt": negative_prompt,

                    }
                }
            ]
        })
        
        result = {"config": {"wide_screen_mode": True}, "elements": elements}
        print(f'手气之后：{prompt_remix}')
    return result


