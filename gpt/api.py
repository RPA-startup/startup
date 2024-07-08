import openai
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import config  # config.py 파일을 import

# OpenAI API 키 설정
openai.api_key = config.OPENAI_API_KEY

# 이미지를 OpenAI API를 사용하여 업로드 및 OCR 요청을 보내는 함수
def upload_image_and_ocr(image_path):
    # 이미지 파일을 읽기
    with open(image_path, 'rb') as f:
        img_data = f.read()

    # OpenAI API로 이미지 업로드
    response = openai.Image.create(file=img_data, purpose='fine-tune')
    image_id = response['id']
    
    # OCR을 위해 Tesseract 사용
    image = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(image)
    
    return ocr_text

# 이미지 경로 설정
image_path = 'path_to_your_image.jpg'

# 이미지 업로드 및 OCR 수행
ocr_result = upload_image_and_ocr(image_path)

# OCR 결과 출력
print(ocr_result)
