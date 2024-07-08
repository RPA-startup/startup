import pytesseract
from PIL import Image

# 이미지를 업로드하여 OCR을 수행하는 함수
def upload_image_and_ocr(image_path):
    # OCR을 위해 Tesseract 사용
    image = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(image)
    return ocr_text

# 이미지 경로 설정 (절대 경로 또는 올바른 상대 경로 사용)
image_path = './test.jpg'

# OCR 수행
ocr_result = upload_image_and_ocr(image_path)

# OCR 결과 출력
print(ocr_result)
