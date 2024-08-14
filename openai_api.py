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
        "role": "system",
        "content": "당신은 사진의 내용을 텍스트화하는 한글 최적화 OCR 전문가이다."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "모든 답변 한글로 설정. 백화점 행사 사진에 대해 텍스트 추출. 이미지의 높이가 5000픽셀 이상일 경우 이미지를 확대해서 정확한 내용으로 처리. 불가능 할경우 '내용 처리불가' 으로 답변.MariaDB 에 컬럼 속성이 text 인 row 하나에 입력할 수 있는 형태로 답변. "}
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
