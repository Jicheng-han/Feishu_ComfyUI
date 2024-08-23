2024.8.23 2.0版本：高阶文生图功能，通过ai写小作文的方式，丰富提示词，生成更富有细节的图片
2024.8.21 1.0版本：飞书机器人 接入 comfyui ，基本文生图功能

目标：
1. 飞书机器人 配合 comfyui工作流，完成基本文生图功能  
2. 高阶版本文生图功能，配合卡片内置按钮功能
3. 图生图功能
4. 工作流切换功能，配合飞书后台配置的menu
   
目前问题：
1. 排队问题：飞书排队用户，无法第一时间收到飞书响应，需要等待服务端空闲后，才会返回 正在开始出图，客户体验差
2. 异步问题：异步处理不太好，因为飞书3秒超时报错问题，导致用户在排队期间 点击重新生成按钮，会报错，虽然不影响使用，但是导致客户重复点击，增加服务器压力
3. 交互问题：按钮不能置灰、按钮不能变更文案，交互体验较差
   
飞书讨论群， https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=dbel773a-47ed-43f7-a8be-0ab4e691eb4c 
效果展示：![screenshot-20240823-095849](https://github.com/user-attachments/assets/9fd0eabe-2b34-414c-bb75-8d95e9b39fec)
![screenshot-20240823-095907](https://github.com/user-attachments/assets/0a9bf644-c185-4ca0-b965-e75a9ba5a9fb)
![20240823-095927](https://github.com/user-attachments/assets/46b60191-2671-462a-aa2a-530c608f0faf)
![20240823-095959](https://github.com/user-attachments/assets/d945fc9d-55a6-4453-88b1-546eb5641c55)
![20240823-100101](https://github.com/user-attachments/assets/46dd60dd-e1f8-43ca-b470-d6da74ec0197)
![20240823-100042](https://github.com/user-attachments/assets/382f2a87-5ca7-4aab-a5ff-6ea9e02b5666)
