import openai
import config  # config.py 파일을 import

# OpenAI API 키 설정
openai.api_key = config.OPENAI_API_KEY

# 이미지 파일 경로
image_path = "./test.jpg"

# 이미지 파일을 OpenAI API에 업로드
with open(image_path, "rb") as image_file:
    response = openai.File.create(
        file=image_file,
        purpose='fine-tune'
    )

# 업로드된 파일의 ID 확인
file_id = response['id']
print(f"Uploaded file ID: {file_id}")

# 파일 ID를 사용하여 채팅 생성
response = openai.ChatCompletion.create(
  model="gpt-4o",
  messages=[
    {
      "role": "system",
      "content": "너는 이미지를 받으면 해당 이미지에 대해 OCR 분석 결과를 출력하는 기계다."
    },
    {
      "role": "user",
      "content": "해당 이미지에 대해 OCR 로 분석한 결과를 텍스트로 전체 얘기해주고 정리해서도 얘기해줘."
    },
    {
      "role": "user",
      "content": f"https://api.openai.com/v1/files/{file_id}/content"
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
response = response['choices'][0]['message']['content']
print(response)
