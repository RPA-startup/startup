# 가상환경 생성 (venv은 가상환경 이름)
# python3 -m venv venv
# 가상환경 활성화 (윈도우)
# venv\Scripts\activate

import openai
import requests
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import base64
import io
import config

# api_key = config.OPENAI_API_KEY
client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

# 이미지를 base64로 인코딩하고 PIL 이미지 객체를 반환하는 함수
def load_and_encode_images(image_sources):
    encoded_images = []
    pil_images = []
    for source in image_sources:
        if source.startswith('http'):  # URL인 경우
            response = requests.get(source)
            image_data = response.content
        else:  # 파일 경로인 경우
            with open(source, "rb") as image_file:
                image_data = image_file.read()
 
        pil_images.append(Image.open(io.BytesIO(image_data)))
        encoded_images.append(base64.b64encode(image_data).decode('utf-8'))
    return encoded_images, pil_images
  
# 응답결과와 이미지를 출력하기 위한 함수
def display_response(pil_images, response_text):
    # 이미지 로딩 및 서브플롯 생성
    fig, axes = plt.subplots(nrows=1, ncols=len(pil_images), figsize=(5 * len(pil_images), 5))
    if len(pil_images) == 1:  # 하나의 이미지인 경우
        axes = [axes]
 
    # 이미지들 표시
    for i, img in enumerate(pil_images):
        axes[i].imshow(img)
        axes[i].axis('off')  # 축 정보 숨기기
        axes[i].set_title(f'Image #{i+1}')
 
    # 전체 플롯 표시
    plt.show()
 
    print(response_text)
    
    # 이미지 경로 또는 URL과 프롬프트를 처리하는 함수
def process_and_display_images(image_sources, prompt):
    # 이미지 로드, base64 인코딩 및 PIL 이미지 객체 생성
    base64_images, pil_images = load_and_encode_images(image_sources)
 
    # OpenAI에 요청 보내기
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt}
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}} for base64_image in base64_images]
        }
    ]
 
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=4000
    )
 
    response_text = response.choices[0].message.content
 
    # 응답과 이미지 표시
    display_response(pil_images, response.choices[0].message.content)
 
    return response_text
  
image_sources = ["res/img/test.jpg"]
prompt = "행사 사진이야 이 사진에서 텍스트 추출해서 OCR 수행해줘 행사내용 정리해줘"
response_text = process_and_display_images(image_sources, prompt)

#출력 결과
'''
다음은 "COOL VACANCE FAIR" 백화점 행사 사진에서 추출한 브랜드명, 행사내용, 행사품목입니다:

1. **브랜드명:** 배럴 (BARREL)
   - **행사내용:**
     - 바캉스 래쉬가드, 비치웨어 할인
     - 배럴 해변용 매트 선착순 증정 (10만원 이상 품목 구매 시)
   - **행사품목:**
     - 배럴 챔피언 숏 슬리브, ₩69,000원
     - 투인원 바지, ₩84,000원

2. **브랜드명:** 스윔 (SWIM)
   - **행사내용:**
     - 스윔웨어 30-50% 할인
   - **행사품목:**
     - 바디 핏 레깅스, ₩44,000원
     - 글래디에이터 스타일, ₩68,000원

3. **브랜드명:** 크록스 (CROCS)
   - **행사내용:**
     - 여름 샌들 및 신발 30% 할인
     - 이벤트 참여 시 랜덤 소장템 증정
   - **행사품목:**
     - 올 시즌 샌들, ₩54,000원
     - 인기 크록스 라인업, ₩60,000원

4. **브랜드명:** 그레비 (GREVI)
   - **행사내용:**
     - 모자 및 여름용 액세서리 할인
     - 특별한 구매 증정이벤트 진행 중
   - **행사품목:**
     - 베스트 리본 햇, ₩45,000원
     - 스타일리시 서머햇, ₩60,000원

5. **브랜드명:** 플로페스 (FLOWPES)
   - **행사내용:**
     - 썸머 슈즈 컬렉션 할인
     - 구매 시 추가 사은품 증정
   - **행사품목:**
     - 편안한 슬립온, ₩62,000원
     - 데일리 캐주얼 슬리퍼, ₩34,000원

6. **브랜드명:** 아레나 (ARENA)
   - **행사내용:**
     - 여름 시즌 남성복 할인
     - 추가 할인 및 증정 이벤트 진행
   - **행사품목:**
     - 서핑 스타일 래쉬가드, ₩74,000원
     - 비치 팬츠, ₩39,800원

7. **브랜드명:** 젝시믹스 (XEXYMIX)
   - **행사내용:**
     - 30-50% 스페셜 할인
     - 여름 오픈기념 추가 할인 진행 중
   - **행사품목:**
     - 베이직 워터 레깅스, ₩45,000원
     - 스타일리시 래쉬가드, ₩39,800원

8. **브랜드명:** 리맹고 (LEMANGO)
   - **행사내용:**
     - 프리미엄 쿨링 수트 할인
   - **행사품목:**
     - 프리미엄 쿨링 수트, ₩58,000원
     - 여름 필수 아이템, ₩32,800원

9. **브랜드명:** 블랙야크 (BLACKYAK)
   - **행사내용:**
     - 등산 및 아웃도어 장비 할인
     - 추가 대형 사은품 증정
   - **행사품목:**
     - 베스트 등산 장비, ₩98,000원
     - 기타 등산용품, ₩45,000원

추가 정보가 필요하거나 다른 도움이 필요하시면 언제든지 말씀해 주세요!'''