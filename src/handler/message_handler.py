
import json
import webuiapi

#from larksuiteoapi import Config

from feishu.message_sender import message_sender
from feishu.data_transfer import upload_image
from service.generate_config import TextToImageConfig
from feishu.message_card import handle_image_card
from feishu.message_card import handle_infotexts
from service.stablediffusion import sd_webui
from util.event_helper import MyReceiveEvent

api = webuiapi.WebUIApi()

ads = webuiapi.ADetailer(ad_model="face_yolov8n_v2.pt")
# ads = webuiapi.ADetailer(ad_model=["face_yolov8n.pt", "hand_yolov8n.pt"])
class MessageHandler:
    def __init__(self):
        pass

    def handle_update_message_card(self, token, openId, prompt):
        messageCard = self.handle_prompt(prompt)
        messageCard["open_ids"] = [openId]
        print(f'模    块: message_handler - handle_update_message_card')
#        print(f'当前VAE: {sd_webui.get_sd_vae}')
        return message_sender.update_message_card(token, messageCard)

    # 根据指令生成不同的消息卡片
    def handle_prompt(self, prompts):
        gen_cfg = TextToImageConfig()
        gen_cfg.update_from_json(sd_webui.parse_prompts_args(prompts))
        model = sd_webui.get_model()[0:sd_webui.get_model().index(".")]

        # models = ["sdxlTURBOPLUSREDTEAMMODEL_","turbovisionxlSuperFastXLBasedOnNew_tvxlV20Bakedvae"]
        #
        # if model in models:
        #     gen_cfg.width = 768
        #     gen_cfg.height = 1024
        #     gen_cfg.cfg_scale = 1.5
        #     gen_cfg.steps = 8
        #     gen_cfg.sampler_name="Euler a"
        #     negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"

        if(model == "融合风格_sdxlUnstableDiffusers_v8"): #已定版版
            gen_cfg.width = 832
            gen_cfg.height = 1216
            # gen_cfg.cfg_scale = 1.5
            # gen_cfg.steps = 5
            # gen_cfg.sampler_name="LCM"
            gen_cfg.steps = 40
            gen_cfg.cfg_scale = 7
            gen_cfg.sampler_name = "DPM++ 3M SDE Karras"
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"

        if(model == "sdxlUnstableDiffusers_v11Rundiffusion"): #已定版版
            gen_cfg.width = 832
            gen_cfg.height = 1216
            # gen_cfg.cfg_scale = 1.5
            # gen_cfg.steps = 5
            # gen_cfg.sampler_name="LCM"
            gen_cfg.steps = 40
            gen_cfg.cfg_scale = 7
            gen_cfg.sampler_name = "DPM++ 3M SDE Karras"
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"



        elif(model == "现实世界_newrealityxl_20"): # 
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name="DPM++ 3M SDE Exponential"
            gen_cfg.cfg_scale = 5
            gen_cfg.steps = 40
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"

        elif(model == "3D风格_starlightXL_v3"): #已定版
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name="DPM++ 3M SDE Karras"
            gen_cfg.cfg_scale = 3.6
            # gen_cfg.cfg_scale = 1.5
            # gen_cfg.steps = 5
            # gen_cfg.sampler_name="LCM"
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"
        
        elif(model == "二次元_AnimeBulldozer_v20"): #已定版版
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name="DPM++ 3M SDE Karras"
            gen_cfg.steps = 28
            gen_cfg.cfg_scale = 6
            gen_cfg.denoising_strength = 0.75
            gen_cfg.negative_prompt="negativeXL_D,unaestheticXL_hk1,bad anatomy,blurry,disembodied limb,Two navel eyes,worst quality,low quality,More than five fingers in one hand,More than 5 toes on one foot,hand with more than 5 fingers,hand with less than 4 fingers,ad anatomy,bad hands,mutated hands and fingers,extra legs,extra arms,interlocked fingers,duplicate,cropped,text,jpeg,artifacts,signature,watermark,username,blurry,artist name,trademark,title,muscular,sd character,multiple view,Reference sheet,long body,malformed limbs,multiple breasts,cloned face,malformed,mutated,bad anatomy,disfigured,bad proportions,duplicate,bad feet,artist name,extra limbs,ugly,fused anus,text font ui,missing limb,"


        elif(model == "sdxl-动漫二次元_1"): # 
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name = "DPM++ 2M Karras"
            gen_cfg.steps = 30
            gen_cfg.cfg_scale = 7
            gen_cfg.denoising_strength = 0.75
            gen_cfg.negative_prompt = "negativeXL_D,unaestheticXL_hk1,bad anatomy,blurry,disembodied limb,Two navel eyes,worst quality,low quality,More than five fingers in one hand,More than 5 toes on one foot,hand with more than 5 fingers,hand with less than 4 fingers,ad anatomy,bad hands,mutated hands and fingers,extra legs,extra arms,interlocked fingers,duplicate,cropped,text,jpeg,artifacts,signature,watermark,username,blurry,artist name,trademark,title,muscular,sd character,multiple view,Reference sheet,long body,malformed limbs,multiple breasts,cloned face,malformed,mutated,bad anatomy,disfigured,bad proportions,duplicate,bad feet,artist name,extra limbs,ugly,fused anus,text font ui,missing limb,"

        # elif(model == "中国风模型_LEOSAM_HelloWorld_v5"): #16-fix.safetensorssdxl-vae-fp
        #     gen_cfg.width = 832
        #     gen_cfg.height = 1248
        #     gen_cfg.restore_faces= True
        #     gen_cfg.cfg_scale = 2.5
        #     gen_cfg.steps = 8
        #     gen_cfg.sampler_name="Euler a"
        #     gen_cfg.negative_prompt="(unaestheticXL_hk1:0.8),FastNegative,bad X,distorted,twisted,FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"

        elif(model == "中国风模型_LEOSAM_HelloWorld_v5"): #16-fix.safetensorssdxl-vae-fp
            gen_cfg.width = 832
            gen_cfg.height = 1248
            gen_cfg.cfg_scale = 7
            gen_cfg.steps = 21
            gen_cfg.sampler_name="Restart"
            gen_cfg.negative_prompt="(unaestheticXL_hk1:0.8),FastNegative,bad X,distorted,twisted,FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"


        elif(model == "ultraspiceXLTURBO_v10"): #16-fix.safetensorssdxl-vae-fp
            gen_cfg.width = 900
            gen_cfg.height = 1200
            gen_cfg.cfg_scale = 2.2
            gen_cfg.steps = 5
            gen_cfg.sampler_name="DPM++ SDE Karras"
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"

        elif(model == "新技术探索_dreamshaperXL"): #16-fix.safetensorssdxl-vae-fp
            gen_cfg.width = 900
            gen_cfg.height = 1200
            gen_cfg.cfg_scale = 2
            gen_cfg.steps = 8
            gen_cfg.sampler_name="DPM++ SDE Karras"
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"


        elif(model == "wildcardxXLLIGHTNING_wildcardxXL"): # 
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name="DPM++ SDE Karras"
            gen_cfg.cfg_scale = 1.5
            gen_cfg.steps = 6
            gen_cfg.negative_prompt="(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2),"
        
        elif(model == "leosamsHelloworldXL_hw50EulerALightning"): # 
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name="Euler a"
            gen_cfg.cfg_scale = 1
            gen_cfg.steps = 8
            gen_cfg.denoising_strength = 0.3
            gen_cfg.negative_prompt="(worst quality,low resolution,bad hands),distorted,twisted,watermark,open mouth,"

        elif(model == "sdxlUnstableDiffusers_v11"): # 
            gen_cfg.width = 832
            gen_cfg.height = 1216
            # gen_cfg.cfg_scale = 1.5
            # gen_cfg.steps = 5
            # gen_cfg.sampler_name="LCM"
            gen_cfg.steps = 40
            gen_cfg.cfg_scale = 7
            gen_cfg.sampler_name = "DPM++ 3M SDE Karras"
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"


        elif(model == "animagineXLV30"): #已定版版
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name="Euler a"
            gen_cfg.steps = 32
            gen_cfg.cfg_scale = 6
            gen_cfg.denoising_strength = 0.75
            gen_cfg.negative_prompt="nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name,"


        elif(model == "copaxTimelessxlSDXL1_v8"): #定版 80分
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.steps = 45
            gen_cfg.negative_prompt = '(unaestheticXLv31:0.6), (worst quality, low quality, illustration, 3d, 2d), open mouth, tooth,ugly face, old face, long neck,'

        elif(model == "2_XXMix_9realisticSDXL_test_v2"): #已定版 test2比1.0效果更好
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name = "DPM++ 3M SDE Karras"
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,",


        elif(model == "现实世界_newrealityxl_21"): #已定版
            gen_cfg.width = 832
            gen_cfg.height = 1216
            gen_cfg.sampler_name="DPM++ 3M SDE Exponential"
            gen_cfg.cfg_scale = 5
            gen_cfg.steps = 30
            gen_cfg.negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"


        elif(model == "a_moyou_v1060"): #已定版
            gen_cfg.width = 512
            gen_cfg.height = 768
            gen_cfg.enable_hr = True
            gen_cfg.denoising_strength = 0.05  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
            gen_cfg.cfg_scale = 7
            gen_cfg.hr_upscaler= "4x-UltraSharp"
            gen_cfg.restore_faces= True
            gen_cfg.hr_scale = 1.5
            gen_cfg.steps = 30
            gen_cfg.hr_second_pass_steps = 15
            gen_cfg.sampler_name="Restart"
            gen_cfg.negative_prompt = 'ng_deepnegative_v1_75t, (badhandv4:1.2), (worst quality:2), (low quality:2), (normal quality:2), lowres, bad anatomy, bad hands, ((monochrome)), ((grayscale)) watermark, moles, '

        elif(model == "xxmix9realistic_v40"): #已定版
            gen_cfg.width = 512
            gen_cfg.height = 768
            gen_cfg.enable_hr = True
            gen_cfg.denoising_strength = 0.4  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
            gen_cfg.cfg_scale = 7
            gen_cfg.hr_upscaler= "1x_NMKDDetoon_97500_G"
            gen_cfg.restore_faces= False
            gen_cfg.hr_scale = 1.5
            gen_cfg.adetailer=[ads]
            gen_cfg.steps = 20
            gen_cfg.hr_second_pass_steps = 10
            gen_cfg.sampler_name="Restart"
            gen_cfg.negative_prompt="easynegative,ng_deepnegative_v1_75t,(worst quality:2),(low quality:2),(normal quality:2),lowres,bad anatomy,bad hands,normal quality,((monochrome)),((grayscale)),((watermark)),"

        elif(model == "majicMIX realistic 麦橘写实_v7"): #已定版
            gen_cfg.width = 512
            gen_cfg.height = 768
            gen_cfg.enable_hr = True
            gen_cfg.denoising_strength = 0.4  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
            gen_cfg.cfg_scale = 7
            gen_cfg.hr_upscaler= "8x_NMKD-Superscale_150000_G"
            gen_cfg.restore_faces= False
            gen_cfg.hr_scale = 1.5
            gen_cfg.adetailer=[ads]
            gen_cfg.steps = 20
            gen_cfg.hr_second_pass_steps = 15
            gen_cfg.sampler_name= "Euler a"
            gen_cfg.negative_prompt="nsfw, easynegative,ng_deepnegative_v1_75t,(worst quality:2),(low quality:2),(normal quality:2),lowres,bad anatomy,bad hands,normal quality,((monochrome)),((grayscale)),((watermark)),"

        elif(model == "t3_Ver121"): #已定版
            gen_cfg.width = 512
            gen_cfg.height = 768
            gen_cfg.enable_hr = True
            gen_cfg.denoising_strength = 0.4  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
            gen_cfg.cfg_scale = 11
            gen_cfg.hr_upscaler= "8x_NMKD-Superscale_150000_G"
            gen_cfg.restore_faces= False
            gen_cfg.hr_scale = 1.5
            gen_cfg.adetailer=[ads]
            gen_cfg.steps = 20
            gen_cfg.hr_second_pass_steps = 15
            gen_cfg.sampler_name= "Restart"
            gen_cfg.negative_prompt="nsfw, easynegative,ng_deepnegative_v1_75t,(worst quality:2),(low quality:2),(normal quality:2),lowres,bad anatomy,bad hands,normal quality,((monochrome)),((grayscale)),((watermark)),"


        elif(model == "manmaruMix_v30图生图"): #已定版
            gen_cfg.width = 512
            gen_cfg.height = 768
            gen_cfg.enable_hr = True
            gen_cfg.denoising_strength = 0.4  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
            gen_cfg.cfg_scale = 7
            gen_cfg.hr_upscaler= "4x-UltraSharp"
            gen_cfg.restore_faces= False
            gen_cfg.hr_scale = 1.5
            # gen_cfg.adetailer=[ads]
            gen_cfg.steps = 20
            gen_cfg.hr_second_pass_steps = 15
            gen_cfg.sampler_name="Euler"
            gen_cfg.negative_prompt="nsfw, ng_deepnegative_v1_75t, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,"






    # elif(model == "2_realvisxlV20_v20Bakedvae"):
        #     gen_cfg.enable_hr = True
        #     gen_cfg.denoising_strength = 0.1  #高清修复的重绘幅度,降低该值有效避免高清修复时画面变形
        #     gen_cfg.cfg_scale = 7
        #     gen_cfg.hr_upscaler= "4x-UltraSharp"
        #     gen_cfg.hr_scale = 1.1
        #     gen_cfg.steps = 30
        #     gen_cfg.hr_second_pass_steps = 15
        # elif(model == "2_3D真人_女孩半身像"):
        #     gen_cfg.sampler_name="Restart"
        #     gen_cfg.steps = 40

        print(f'模    块: message_handler - handle_prompt')

        result = sd_webui.txt2img(gen_cfg)

        images_key = []
        for img_data in result['images']:
            images_key.append(upload_image(img_data))
        # print(f"XXXXXXXXXX: {result['info'], images_key, prompts}")
        return handle_image_card(result['info'], images_key, prompts)

    def handle_message(self, myevent: MyReceiveEvent):
        message_sender.send_text_message(myevent, f"{sd_webui.queue()}")
        messageCard = self.handle_prompt(myevent.text)
        # print(f'模    块: message_handler - handle_message')


        return message_sender.send_message_card(myevent, messageCard)
