import boto3
import base64
import config
import os

# S3 클라이언트 생성 (환경 변수에서 자격 증명을 읽습니다)
s3 = boto3.client(
    's3',
    aws_access_key_id=config.s3_Info["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=config.s3_Info["AWS_SECRET_ACCESS_KEY"],
    region_name=config.s3_Info["region_name"]
)

def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    """
    S3에 파일을 업로드하는 함수

    :param local_file_path: 업로드할 로컬 파일의 경로
    :param bucket_name: S3 버킷 이름
    :param s3_file_path: S3에서 사용할 파일 경로
    """
    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print(f"파일이 성공적으로 {bucket_name}/{s3_file_path}에 업로드되었습니다.")
    except FileNotFoundError:
        print("파일이 로컬 시스템에 존재하지 않습니다.")
    except Exception as e:
        print(f"파일 업로드 중 오류가 발생했습니다: {e}")

def download_from_s3(bucket_name, s3_file_path, local_file_path):
    """
    S3에서 파일을 다운로드하는 함수

    :param bucket_name: S3 버킷 이름
    :param s3_file_path: S3에서 다운로드할 파일의 경로
    :param local_file_path: 로컬에 저장할 파일 경로
    """
    try:
        s3.download_file(bucket_name, s3_file_path, local_file_path)
        print(f"파일이 성공적으로 {local_file_path}에 다운로드되었습니다.")
    except Exception as e:
        print(f"파일 다운로드 중 오류가 발생했습니다: {e}")

def get_file_content_as_base64(bucket_name, s3_file_path):
    """
    S3에서 파일을 가져와서 base64로 인코딩하는 함수

    :param bucket_name: S3 버킷 이름
    :param s3_file_path: S3에서 가져올 파일의 경로
    :return: base64로 인코딩된 파일 콘텐츠
    """
    try:
        # S3 객체를 메모리로 다운로드
        obj = s3.get_object(Bucket=bucket_name, Key=s3_file_path)
        
        # 파일 콘텐츠를 읽어오기
        file_content = obj['Body'].read()
        
        # 파일 콘텐츠를 base64로 인코딩
        base64_content = base64.b64encode(file_content).decode('utf-8')
        
        return base64_content
    
    except Exception as e:
        print(f"파일 콘텐츠를 가져오는 중 오류가 발생했습니다: {e}")
        return None

# 사용 예시 (직접 함수 호출)
if __name__ == "__main__":
    # 업로드 예시
    local_file_path = "C:/path/to/your/file.txt"
    s3_file_path = "2024.08.19_테마_본점_그로서리6.jpg"
    bucket_name = config.s3_Info["bucket_name"]
    # download_path = r"C:\Users\Administrator\Documents\김진우_업무\startup-1\정육1.jpg"
    # upload_to_s3(local_file_path, bucket_name, s3_file_path)

    # 다운로드 예시
    # download_from_s3(bucket_name, s3_file_path, download_path)

    # Base64 인코딩 예시
    base64_content = get_file_content_as_base64(bucket_name, s3_file_path)
    if base64_content:
        print("파일 콘텐츠를 base64로 인코딩한 결과:")
        print(base64_content)
