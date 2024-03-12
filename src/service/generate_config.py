import webuiapi
from webuiapi import HiResUpscaler, ControlNetUnit
from typing import List, Dict, Any
from feishu.message_card import LIST_INFO_CARD, handle_list_info_card
from service.aliyun_translator import aliyun_translator
import string

class GenerateConfig:
    def get_as_json(self) -> dict:
        return self.__dict__

    def update_from_json(self, json: dict):
        for key in json:
            if hasattr(self, key):
                setattr(self, key, json[key])
            else:
                print(f'Unknown key {key} in json')

    def translate_to_english(self, translator='alibaba'):
        def contains_chinese(text):
            return any('\u4e00' <= char <= '\u9fff' for char in text)

        # def translate(text):
        #     return html.unescape(ts.translate_text(query_text=text, translator=translator, from_language='auto', to_language='en'))
        print(f'\n模    块: generate_config : 原始输入')
#        print(f'原始输入: {self.prompt}')
        if len(self.prompt) > 0:
            self.prompt = self.prompt.replace('@_user_1','').replace('@_user_2','').replace('@_user_3','').replace('@_user_4','').replace('@_user_5','').replace('@_user_6','').replace('pussy', 'sheer').replace('裸', 'sheer').replace('naked', 'sheer').replace('nude','revealing').replace('bare','sheer').replace('undressed','sheer').replace('exposed','sheer').replace('Stripped','sheer').replace('Unclothed','sheer').replace('Au naturel','sheer').replace('In the buff','sheer').replace('porn','sheer').replace('j8','sheer')
            if contains_chinese(self.prompt):
                self.prompt = aliyun_translator.translate(self.prompt)
                print(f'翻译输出: {self.prompt}\n')
        if len(self.negative_prompt) > 0 and contains_chinese(self.negative_prompt):
            self.negative_prompt = aliyun_translator.translate(self.negative_prompt)

api = webuiapi.WebUIApi()

ads = webuiapi.ADetailer(ad_model="face_yolov8n.pt")

class TextToImageConfig(GenerateConfig):
    def __init__(
            self,
            enable_hr=False,
            denoising_strength=0.1,
            firstphase_width=0,
            firstphase_height=0,
            hr_scale=1,
            hr_upscaler="R-ESRGAN 4x+",
            hr_second_pass_steps=15,
            hr_resize_x=0,
            hr_resize_y=0,
            prompt="",
            styles=[],
            seed=-1,
            subseed=-1,
            subseed_strength=0.0,
            seed_resize_from_h=0,
            seed_resize_from_w=0,
            sampler_name="DPM++ 3M SDE Karras",  # use this instead of sampler_index   DPM++ 2M Karras
            batch_size=1,
            n_iter=1,
            # adetailer=[ads],
            steps=40,
            cfg_scale=7.0,
            width=832,
            height=1216,
            restore_faces=False,
            tiling=False,
            do_not_save_samples=False,
            do_not_save_grid=False,
            negative_prompt="FastNegative,blur,blurred background,disproportionate face,deformed eyes,poorly detailed eyes,(disfigured:1.2),(deformed:1.2),bad anatomy,brand,(logo:1.3),bad perspective,bad proportions,jpg artifacts,jpeg artifacts,extra leg,extra arm,missing arm,missing leg,extra finger,manga,drawing,painting,3D render,render,manga face,",
            #negative_prompt="FastNegative, blur, blurred background, disproportionate face, deformed eyes, poorly detailed eyes, (disfigured:1.2), (deformed:1.2), bad anatomy, brand, (logo:1.3), bad perspective, bad proportions, jpg artifacts, jpeg artifacts, extra leg, extra arm, missing arm, missing leg, extra finger, missing finger, broken finger, bad hands, deformed hand, bad finger, broken hand, broken finger, colored schlera, (four fingers:1.3), (six fingers:1.3), (3 fingers:1.3), (4 fingers:1.3), (6 fingers:1.3), (7 fingers:1.3), (seven fingers:1.3), (cloned finger:1.3), (cloned hand:1.3), cloned arm, (malformed:1.3), (three fingers:1.3), manga, drawing, painting, 3D render, render, manga face,",
            # "negativeXL_D, deformed hands, long neck, long body, (bad hands), conjoined fingers, deformed fingers,badhandv4, EasyNegative,NG_DeepNegative_V1_75T, worst quality, low quality, normal quality, naked, nsfw, nipples, nude, lowres, bad anatomy, bad eyes, negative_hand-neg:11",
            # (unaestheticXLv31:0.6),
            eta=1.0,
            s_churn=0,
            s_tmax=0,
            s_tmin=0,
            s_noise=1,
            override_settings={},
            override_settings_restore_afterwards=True,
            script_args=None,  # List of arguments for the script "script_name"
            script_name=None,
            send_images=True,
            save_images=False,
            alwayson_scripts={},
            controlnet_units: List[ControlNetUnit] = [],
            sampler_index=None,  # deprecated: use sampler_name
            use_deprecated_controlnet=False,
            # use_async=True,

    ):
        self.enable_hr = enable_hr
        self.denoising_strength = denoising_strength
        self.firstphase_width = firstphase_width
        self.firstphase_height = firstphase_height
        self.hr_scale = hr_scale
        self.hr_upscaler = hr_upscaler
        self.hr_second_pass_steps = hr_second_pass_steps
        self.hr_resize_x = hr_resize_x
        self.hr_resize_y = hr_resize_y
        self.prompt = prompt
        self.styles = styles
        self.seed = seed
        self.subseed = subseed
        self.subseed_strength = subseed_strength
        self.seed_resize_from_h = seed_resize_from_h
        self.seed_resize_from_w = seed_resize_from_w
        self.sampler_name = sampler_name
        self.batch_size = batch_size
        self.n_iter = n_iter
        self.steps = steps
        self.cfg_scale = cfg_scale
        self.width = width
        self.height = height
        self.restore_faces = restore_faces
        self.tiling = tiling
        self.do_not_save_samples = do_not_save_samples
        self.do_not_save_grid = do_not_save_grid
        self.negative_prompt = negative_prompt
        self.eta = eta
        self.s_churn = s_churn
        self.s_tmax = s_tmax
        self.s_tmin = s_tmin
        self.s_noise = s_noise
        self.override_settings = override_settings
        self.override_settings_restore_afterwards = override_settings_restore_afterwards
        self.script_args = script_args
        self.script_name = script_name
        self.send_images = send_images
        self.save_images = save_images
        self.alwayson_scripts = alwayson_scripts
        self.controlnet_units = controlnet_units
        self.sampler_index = sampler_index
        self.use_deprecated_controlnet = use_deprecated_controlnet
        # self.use_async = use_async


class ImageToImageConfig(GenerateConfig):
    def __init__(
            self,
            images=[],  # list of PIL Image
            resize_mode=2, #3"Just resize (latent upscale)"
            denoising_strength=0.75,
            image_cfg_scale=1.5,
            mask_image=None,  # PIL Image mask
            mask_blur=4,
            inpainting_fill=0,
            inpaint_full_res=True,
            inpaint_full_res_padding=0,
            inpainting_mask_invert=0,
            initial_noise_multiplier=1,
            prompt="",
            styles=[],
            seed=-1,
            subseed=-1,
            subseed_strength=0,
            seed_resize_from_h=0,
            seed_resize_from_w=0,
            sampler_name="DPM++ 3M SDE Exponential",  # use this instead of sampler_index
            batch_size=1,
            n_iter=1,
            steps=32,
            cfg_scale=3.5,
            width=832,
            height=1216,
            restore_faces=False,
            tiling=False,
            do_not_save_samples=False,
            do_not_save_grid=False,
            negative_prompt="FastNegative,blur,blurred background,disproportionate face,deformed eyes,poorly detailed eyes,(disfigured:1.2),(deformed:1.2),bad anatomy,brand,(logo:1.3),bad perspective,bad proportions,jpg artifacts,jpeg artifacts,extra leg,extra arm,missing arm,missing leg,extra finger,manga,drawing,painting,3D render,render,manga face,",
        
            eta=1.0,
            s_churn=0,
            s_tmax=0,
            s_tmin=0,
            s_noise=1,
            override_settings={},
            override_settings_restore_afterwards=True,
            script_args=None,  # List of arguments for the script "script_name"
            sampler_index=None,  # deprecated: use sampler_name
            include_init_images=False,
            script_name=None,
            send_images=True,
            save_images=False,
            alwayson_scripts={},
            controlnet_units: List[ControlNetUnit] = [],
            use_deprecated_controlnet=False,
    ):
        self.images = images
        self.resize_mode = resize_mode
        self.denoising_strength = denoising_strength
        self.image_cfg_scale = image_cfg_scale
        self.mask_image = mask_image
        self.mask_blur = mask_blur
        self.inpainting_fill = inpainting_fill
        self.inpaint_full_res = inpaint_full_res
        self.inpaint_full_res_padding = inpaint_full_res_padding
        self.inpainting_mask_invert = inpainting_mask_invert
        self.initial_noise_multiplier = initial_noise_multiplier
        self.prompt = prompt
        self.styles = styles
        self.seed = seed
        self.subseed = subseed
        self.subseed_strength = subseed_strength
        self.seed_resize_from_h = seed_resize_from_h
        self.seed_resize_from_w = seed_resize_from_w
        self.sampler_name = sampler_name
        self.batch_size = batch_size
        self.n_iter = n_iter
        self.steps = steps
        self.cfg_scale = cfg_scale
        self.width = width
        self.height = height
        self.restore_faces = restore_faces
        self.tiling = tiling
        self.do_not_save_samples = do_not_save_samples
        self.do_not_save_grid = do_not_save_grid
        self.negative_prompt = negative_prompt
        self.eta = eta
        self.s_churn = s_churn
        self.s_tmax = s_tmax
        self.s_tmin = s_tmin
        self.s_noise = s_noise
        self.override_settings = override_settings
        self.override_settings_restore_afterwards = override_settings_restore_afterwards
        self.script_args = script_args
        self.sampler_index = sampler_index
        self.include_init_images = include_init_images
        self.script_name = script_name
        self.send_images = send_images
        self.save_images = save_images
        self.alwayson_scripts = alwayson_scripts
        self.controlnet_units = controlnet_units
        self.use_deprecated_controlnet = use_deprecated_controlnet
