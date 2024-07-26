import openai
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import config

# OpenAI API 키 설정
openai.api_key = config.OPENAI_API_KEY

# 이미지 URL
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"

# 이미지 다운로드 및 표시
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
plt.imshow(img)
plt.axis('off')  # 축 표시를 끔
plt.show()

# OpenAI API 호출
response = openai.ChatCompletion.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": "이 그림에 대해 설명해줘."
        },
        {
            "role": "user",
            "content": image_url
        }
    ],
    max_tokens=1000
)

# 응답 출력
print(response['choices'][0]['message']['content'])
