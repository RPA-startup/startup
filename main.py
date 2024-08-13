# 가상환경 생성 (venv은 가상환경 이름)
# python3 -m venv venv
# 가상환경 활성화 (윈도우)
# venv\Scripts\activate

from database import connect_db, get_empty_content_rows, update_content, disconnect_db
from openai_client import process_images_and_get_response

# Main execution
if __name__ == "__main__":
    print("***프로그램 시작***")

    # 데이터베이스 연결
    conn, cur = connect_db()

    # Content가 비어 있는 행들 가져오기
    rows = get_empty_content_rows(cur)
    
    print(rows)
    
    if rows:
        for row in rows:
            event_id = row[0]
            image_url = row[1]

            print(f"현재 처리 중인 행 EventID: {event_id}, 이미지 URL: {image_url}")

            # OpenAI API를 사용하여 이미지 처리 및 Content 업데이트
            response_text = process_images_and_get_response([image_url])
            update_content(cur, conn, event_id, response_text)
    
    # 데이터베이스 연결 종료
    disconnect_db(conn, cur)

    print("프로그램 종료.")
