import openai
import config

# OpenAI API 클라이언트 초기화
client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

# Base64 이미지 데이터를 사용하여 OpenAI API에 요청을 보내고 응답을 처리
def process_images_and_get_response(base64_images):
    print("이미지 처리 및 OpenAI API 요청 시작...")

    # Base64 인코딩된 이미지 데이터를 사용하여 메시지 구성
    messages = [
        {
            "role": "system",
            "content": "당신은 사진의 내용을 텍스트화하는 한글 최적화 OCR 전문가이다."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "모든 답변 한글로 설정. 백화점 행사 사진에 대해 텍스트 추출. 이미지의 높이가 5000픽셀 이상일 경우 이미지를 확대해서 정확한 내용으로 처리. 불가능 할경우 '내용 처리불가' 으로 답변.MariaDB 에 컬럼 속성이 text 인 row 하나에 입력할 수 있는 형태로 답변. "}
            ] + [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}} for base64_image in base64_images]
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

# 주어진 정보로 키워드를 생성하는 함수
def generate_keywords(department_store, store_location, title, content, start_date, end_date, site_url):
    print("키워드 생성 요청을 OpenAI API에 보냅니다...")

    prompt = (
        f"백화점 행사에 대해 정보를 키워드로 저장하고 있어 이 행사에 대해 대표적인 키워드를 5~10가지 정도 뽑아줘 키워드는 , 로 구분해야해.\n"
        f"백화점: {department_store} {store_location}\n"
        f"행사 제목: {title}\n"
        f"행사 내용: {content}\n"
        f"행사 시작일자: {start_date}\n"
        f"행사 마감일자: {end_date}\n"
        f"사이트 주소: {site_url}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    keywords = response.choices[0].message.content.strip()
    print("생성된 키워드: ", keywords)
    return keywords
