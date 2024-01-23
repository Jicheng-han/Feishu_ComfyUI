import sys
sys.path.append("D:\\Feishu-Stablediffusion-master\\src\\")


from util.app_config import app_config
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
import uuid


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def menu_respon(user_id,response_text):
    # 创建client
    client = lark.Client.builder() \
        .app_id(app_config.APP_ID) \
        .app_secret(app_config.APP_SECRET) \
        .log_level(lark.LogLevel.ERROR) \
        .build()

    # 构造请求对象
    request: CreateMessageRequest = CreateMessageRequest.builder() \
        .receive_id_type("user_id") \
        .request_body(CreateMessageRequestBody.builder()
            .receive_id(user_id)
            .msg_type("text")
            .content("{\"text\":\""+ response_text +"\"}")
            .uuid(str(uuid.uuid4()))
            .build()) \
        .build()

    # 发起请求
    response: CreateMessageResponse = client.im.v1.message.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    # lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    menu_respon()

 