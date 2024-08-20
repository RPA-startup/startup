import boto3
import sys
import os
import config

# S3 클라이언트 생성 (환경 변수에서 자격 증명을 읽습니다)
s3 = boto3.client(
    's3',
    aws_access_key_id=config.s3_Info["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=config.s3_Info["AWS_SECRET_ACCESS_KEY"],
    region_name=config.s3_Info["region_name"]
)

# S3에 파일을 업로드하는 함수 (한개씩)
def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print(f"파일이 성공적으로 {bucket_name}/{s3_file_path}에 업로드되었습니다.")
    except FileNotFoundError:
        print("파일이 로컬 시스템에 존재하지 않습니다.")
    except Exception as e:
        print(f"파일 업로드 중 오류가 발생했습니다: {e}")

# 지정된 디렉토리의 모든 파일을 S3 버킷의 루트에 업로드하는 함수
def upload_directory_to_s3(directory_path, bucket_name):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            # S3의 루트에 업로드하기 위해 파일명만 사용
            s3_file_path = file_name
            upload_to_s3(local_file_path, bucket_name, s3_file_path)

if __name__ == "__main__":
    # 명령줄 인자로 디렉토리 경로를 받음
    if len(sys.argv) != 2:
        print("사용법: python s3_upload.py <로컬 디렉토리 경로>")
        sys.exit(1)

    local_directory_path = sys.argv[1]  # 첫 번째 명령줄 인자: 로컬 디렉토리 경로
    bucket_name = config.s3_Info["bucket_name"]

    # S3에 디렉토리 내 모든 파일 업로드
    upload_directory_to_s3(local_directory_path, bucket_name)
