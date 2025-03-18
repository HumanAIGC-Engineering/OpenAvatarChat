import base64
import os
from openai import OpenAI

#  base 64 编码格式


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


base64_image = encode_image('open-video-chat/assets/images/test.png')
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-vl-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'user', 'content': [
            # 如果有图片，则添加图片信息；否则只保留文本内容
            {"type": "text", "text": "图里有什么"},  # 纯文本部分
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}  # 图片 URL 部分（如果有图片）
        ]}],
    stream=True,
    stream_options={"include_usage": True}
)
for chunk in completion:
    if (chunk.choices is not None and len(chunk.choices) > 0):
        print(chunk.model_dump_json())
        print(chunk.choices[0].delta.content)
