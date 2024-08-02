# 프로젝트 작업 규칙

## 1. 브랜치 규칙
- **Main branch**: 항상 배포 가능한 상태를 유지합니다. 이 브랜치에 직접 푸시하지 않습니다.
- **Develop branch**: 새로운 기능 개발과 버그 수정을 위한 브랜치입니다.
- **Feature branches**: 각 기능이나 버그 수정은 독립적인 브랜치에서 작업합니다. `feature/기능명` 형태로 네이밍합니다.
- **Hotfix branches**: 긴급한 버그 수정을 위한 브랜치입니다. `hotfix/버그명` 형태로 네이밍합니다.

## 2. 커밋 메시지 규칙
- **일관된 스타일**: 커밋 메시지는 짧고 명확하게 작성합니다. 예: `[타입] 간단한 설명`
  - `feat`: 새로운 기능 추가
  - `fix`: 버그 수정
  - `docs`: 문서 수정
  - `style`: 코드 포맷팅, 세미콜론 누락 등 기능의 변경이 없는 수정
  - `refactor`: 코드 리팩토링
  - `test`: 테스트 추가 또는 수정
  - `chore`: 빌드 업무 수정, 패키지 매니저 설정 등

## 3. 코드 리뷰
- **Pull Request (PR)**: 모든 변경 사항은 PR을 통해서만 메인 브랜치에 병합합니다.
- **리뷰어 지정**: tigre911 지정, PR을 검토합니다.
- **승인 후 병합**: 모든 리뷰어의 승인을 받은 후 병합합니다.

## 4. 이슈 관리
- **이슈 템플릿**: 버그, 기능 요청 등의 이슈를 명확히 설명
- **라벨링**: 이슈의 종류와 우선순위에 따라 라벨을 붙입니다.

## 5. CI/CD
- **자동화된 테스트**: PR 생성 시 자동으로 테스트를 실행합니다.
- **빌드 및 배포**: CI/CD 파이프라인을 통해 자동화합니다.

## 6. 커뮤니케이션
- **정기 회의**: 미정

## 7. 기타 규칙
- **데이터 보호**: 민감한 정보는 저장소에 포함하지 않습니다.
- **컨벤션 준수**: 팀의 네이밍 컨벤션 및 기타 규칙을 준수.

## 8. DB Table구조
0. **EventID** `INT AUTO_INCREMENT PRIMARY KEY`
1. **DepartmentStore** `VARCHAR(100) NOT NULL` - 백화점 [ ex. 롯데, 신세계 ]
2. **StoreLocation** `VARCHAR(100) NOT NULL` - 점포 [ ex. 강남점, 월드타워점, 신사점 , ... ]
3. **Category** `VARCHAR(50)` - 행사 분류 [ ex. 테마, 쇼핑뉴스, 이벤트, 사은행사, ... ]
4. **Title** `VARCHAR(255)` NOT NULL` - 행사 제목 [ ex. 생로랑 팝업 스토어, 신세계 제휴카드 최대 12개월 무이자 할부 혜택  ] - 제목이 길 수 있음
5. **Content** `TEXT` - 행사 내용 [ ex. 생로랑 팝업 이벤트로 10% 할인, 신세계 카드 사용시 2-6개월 무이자 할부 ] - 내용이 클 수 있음
6. **StartDate** `DATE` - 행사 시작 날짜 [ ex. 20240729, 20240801 ]
7. **EndDate** `DATE` - 행사 종료 날짜 [ ex. 20240729, 20240801 ]
8. **Keywords** `VARCHAR(255)` - 키워드 [ ex. 팝업, 행사, 쿠폰, ... ] - 여러개 입력 가능함
9. **ImageURL** `VARCHAR(255)` - 이미지주소 - cnd 서버 주소
10. **CreatedDate** `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` - 등록 날짜 - 해당 db에 입력되는 날짜
11. **UpdatedDate** `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` - 수정 날짜 - 해당 db에 수정되는 날짜
