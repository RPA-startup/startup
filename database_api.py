import mariadb
import sys
import config
import pandas as pd

# MariaDB 플랫폼에 연결
def connect_db():
    try:
        conn = mariadb.connect(
            user=config.DB_Info["user"],
            password=config.DB_Info["password"],
            host=config.DB_Info["host"],
            port=config.DB_Info["port"],
            database=config.DB_Info["database"]
        )
        cur = conn.cursor()
        print("MariaDB에 성공적으로 연결되었습니다.")
    except mariadb.Error as e:
        print(f"MariaDB 플랫폼에 연결하는 중 오류 발생: {e}")
        sys.exit(1)
    return conn, cur

def get_data(cur, query):
    #retrieving information
    cur.execute(query) 
    column_names = [desc[0] for desc in cur.description]
    results = cur.fetchall()
    results_as_dicts = [dict(zip(column_names, row)) for row in results]
    return results_as_dicts

# Keywords가 비어 있는 행들을 가져옴
def get_empty_keywords_rows(cur):
    try:
        query = f"SELECT EventID, ImageURL, Content FROM {config.DB_Info['table']} WHERE Keywords IS NULL OR Keywords = ''"
        print(f"쿼리 실행 중: {query}")
        cur.execute(query)
        resultset = cur.fetchall()
        print(f"가져온 행의 수: {len(resultset)}")
    except mariadb.Error as e:
        print(f"쿼리 실행 중 오류 발생: {e}")
        return None
    return resultset

# 특정 행의 Content를 업데이트 (기존 내용에 추가)
def update_content(cur, conn, event_id, additional_content):
    try:
        print(f"EventID {event_id}에 대해 Content 업데이트 중...")

        # 기존 Content 가져오기
        cur.execute(f"SELECT Content FROM {config.DB_Info['table']} WHERE EventID = %s", (event_id,))
        existing_content = cur.fetchone()[0]

        # 새로운 Content로 업데이트
        new_content = (existing_content or '') + additional_content
        cur.execute(f"UPDATE {config.DB_Info['table']} SET Content = %s WHERE EventID = %s", (new_content, event_id))
        conn.commit()
        print(f"EventID {event_id}에 대해 Content 업데이트 완료.")
    except mariadb.Error as e:
        print(f"EventID {event_id} 업데이트 중 오류 발생: {e}")

# Keywords가 비어있고 Content가 채워진 행들을 가져옴
def get_filled_content_rows(cur):
    try:
        query = f"SELECT EventID, DepartmentStore, StoreLocation, Title, Content, StartDate, EndDate, ImageURL FROM {config.DB_Info['table']} WHERE Keywords IS NULL OR Keywords = '' AND Content IS NOT NULL"
        print(f"쿼리 실행 중: {query}")
        cur.execute(query)
        resultset = cur.fetchall()
        print(f"가져온 행의 수: {len(resultset)}")
    except mariadb.Error as e:
        print(f"쿼리 실행 중 오류 발생: {e}")
        return None
    return resultset

# 특정 행의 Keywords를 업데이트
def update_keywords(cur, conn, event_id, keywords):
    try:
        print(f"EventID {event_id}에 대해 Keywords 업데이트 중...")
        cur.execute(f"UPDATE {config.DB_Info['table']} SET Keywords = %s WHERE EventID = %s", (keywords, event_id))
        conn.commit()
        print(f"EventID {event_id}에 대해 Keywords 업데이트 완료.")
    except mariadb.Error as e:
        print(f"EventID {event_id} 업데이트 중 오류 발생: {e}")


# 데이터베이스에서 데이터를 엑셀 파일로 저장하는 함수
def export_to_excel(cur, query, file_name="output.xlsx"):
    try:
        # SQL 쿼리 실행 및 DataFrame으로 변환
        df = pd.read_sql(query, con=cur.connection)
        
        # DataFrame을 엑셀 파일로 저장
        df.to_excel(file_name, index=False)
        print(f"데이터가 {file_name} 파일로 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"엑셀 파일로 데이터를 내보내는 중 오류 발생: {e}")

# 데이터베이스 연결 종료
def disconnect_db(conn, cur):
    cur.close()
    conn.close()
    print("데이터베이스 연결이 종료되었습니다.")


if __name__ == "__main__":
    conn, cur = connect_db()

    # 예시 쿼리
    query = "SELECT eventid, keywords FROM event WHERE Keywords <> 'test';"

    # 엑셀로 내보내기
    export_to_excel(cur, query, file_name="event_data_keywords.xlsx")

    disconnect_db(conn, cur)
