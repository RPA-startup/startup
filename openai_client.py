import openai
import requests
from PIL import Image
import matplotlib.pyplot as plt
import config

# OpenAI API 클라이언트 초기화
client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

# 이미지 URL을 사용하여 OpenAI API에 요청을 보내고 응답을 처리
def process_images_and_get_response(image_sources):
    print("이미지 처리 및 OpenAI API 요청 시작...")

    # 이미지 URL을 직접 사용하여 메시지 구성
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "한글로 설정. 백화점 행사 사진이야 이 사진에서 텍스트 추출해서 OCR 수행해줘 이미지가 길은 경우 자세히 확대해서 정확한 내용으로 처리해야해"}
            ] + [{"type": "image_url", "image_url": {"url": image_url}} for image_url in image_sources]
        }
    ]
 
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=4000
    )
 
    response_text = response.choices[0].message.content

    print("OpenAI 응답: ", response_text)
    print("OpenAI API 요청 완료.")
 
    return response_text
