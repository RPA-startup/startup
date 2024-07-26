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
        max_tokens=1000
    )
 
    response_text = response.choices[0].message.content
 
    # 응답과 이미지 표시
    display_response(pil_images, response.choices[0].message.content)
 
    return response_text
  
image_sources = ["test.jpg"]
prompt = "이 사진에서 텍스트 추출해서 OCR 수행해줘"
response_text = process_and_display_images(image_sources, prompt)

#출력 결과
'''다음은 이미지에서 추출한 텍스트입니다:

```
COOL VACANCE FAIR
"조깅하자, 가볍게! 피싱하자 시원하게!"
기간한정특가
6.432~7.12
삼성생명카드 구매시 1095 청구할인+ 무품증
*1. 상품 미부합시 맬려 배송비 추가

BARREL
배럴
SPECIAL EVENT
-여성레시가드 구매 시 이너 비끼or여성래시가드 증정
- 여성래시가드 1095 청구할인(삼성생명카드)
*모든세일상품 무료배송

BEST ITEM
- 여성래시가드 최혜은가 80,000원
- 남성래시가드 백에서 60,004원

SWIM
ELLIPSES
시키비

SPECIAL EVENT
-기공 시 50% 이상 상품 구매시 30점 포인트 적립
-생각리업 착룬 팔베게 풍선교환

BEST ITEM
-남자 썬바이저 골프통 60,000원
-여성레시가드 화미일카족 티 120,000원
-레시가드 백에서 80,000원


crocs
크록스
SPECIAL EVENT
-레바 스키스 각 티젠스 평가 허용
-티켓플 계약시 크로스 제품 20% 가격.

BEST ITEM
-우마이닝 이느 비끼 80,000원
-여성 레시포드 하디 85,000원

GREVI
그레비티
SPECIAL EVENT
-기공시 20% 세일/베스트 레이불59,0000구입 구매한정

BEST ITEM
- 여성 드레시가 70,000원
- 시크한 패션원 티 9040원

FLOWER
플브워
SPECIAL EVENT
-다종 선디 10% 할인

BEST ITEM
-여성 하이햄 티백 80,000원
-신발 드레스 와 신발 케이스 종합의걸
 120,000원

arena
아르으나
SPECIAL EVENT
-여성 전상품 10~20%OFF/여전상품 한정기간 할인
아재미한 고별/신발 크로 LOCAL KR 페임

BEST ITEM
여성래쉬가드 80,000원/남여모든상품구매 시배송비관

나무지
- BAT
-신상 트레모디 판매중
WIMLAG0

LEMANGO
레망고
SPECIAL EVENT
-도매 채널 구출가 구에터 체납시 삼일무료죄쿠폰(사정상품 최종형 테스트)
- 여인의 의류 95시장

BEST ITEM
-여성 래시가드 80,000원
-언더더스 80,000원

BLACKYAK
블랙야크
SPECIAL EVENT
- 여성래시가드 109%정품
-남여모든상품 최종할인
 사코각 화페금 받기 기

BEST ITEM
--레인코트/우의 80,000원
-수영모자 기능성 30,000원 가방보다
```'''