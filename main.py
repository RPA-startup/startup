from database_api import connect_db, get_empty_keywords_rows, update_content, disconnect_db
from s3_api import get_file_content_as_base64
from openai_api import process_images_and_get_response
import config

# Main execution
if __name__ == "__main__":
    print("*** 프로그램 시작 ***")

    # 데이터베이스 연결
    conn, cur = connect_db()

    # Keywords가 비어 있는 행들 가져오기
    rows = get_empty_keywords_rows(cur)
    
    if rows:
        for row in rows:
            event_id = row[0]
            image_url = row[1]

            print(f"현재 처리 중인 행 EventID: {event_id}, 이미지 URL: {image_url}")

            # S3에서 이미지 가져와서 Base64로 인코딩
            s3_file_path = image_url  # 여기서 image_url이 S3의 파일 경로임을 가정합니다.
            bucket_name = config.s3_Info["bucket_name"]
            base64_image = get_file_content_as_base64(bucket_name, s3_file_path)
            
            if base64_image:
                # OpenAI API를 사용하여 이미지 처리 및 Content 업데이트
                response_text = process_images_and_get_response([base64_image])
                update_content(cur, conn, event_id, response_text)
    
    # 데이터베이스 연결 종료
    disconnect_db(conn, cur)

    print("*** 프로그램 종료 ***")
