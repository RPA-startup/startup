from database_api import connect_db, get_empty_keywords_rows, update_content, get_filled_content_rows, update_keywords, disconnect_db
from s3_api import get_file_content_as_base64
from openai_api import process_images_and_get_response, generate_keywords
import config

# Main execution
if __name__ == "__main__":
    print("*** 프로그램 시작 ***")

    # 데이터베이스 연결
    conn, cur = connect_db()

    # Step 1: Keywords가 비어 있는 행들 가져오기
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

    # Step 2: Content가 채워지고 Keywords가 비어있는 행들 가져오기
    rows_with_content = get_filled_content_rows(cur)
    
    if rows_with_content:
        for row in rows_with_content:
            event_id = row[0]
            department_store = row[1]
            store_location = row[2]
            title = row[3]
            content = row[4]
            start_date = row[5]
            end_date = row[6]
            site_url = row[7]  # ImageURL을 SiteURL로 사용

            print(f"현재 처리 중인 행 EventID: {event_id}")

            # OpenAI API를 사용하여 키워드 생성
            keywords = generate_keywords(department_store, store_location, title, content, start_date, end_date, site_url)
            
            # Keywords 업데이트
            update_keywords(cur, conn, event_id, keywords)
    
    # 데이터베이스 연결 종료
    disconnect_db(conn, cur)

    print("*** 프로그램 종료 ***")
