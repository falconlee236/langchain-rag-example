# langchain-rag-example

![image](https://github.com/user-attachments/assets/b35a2097-15a8-4ac7-a7ba-8ec32070b523)

https://developer.nvidia.com/ko-kr/blog/rag-101-demystifying-retrieval-augmented-generation-pipelines/


<img width="1491" alt="image" src="https://github.com/user-attachments/assets/c228db9c-7c8a-40df-8615-04386e4b0f22" />


# 디렉토리 구조
```bash
rag-project/
├── docker/
│   ├── Dockerfile.app          # Web App 서비스를 위한 Dockerfile
│   ├── Dockerfile.embedding    # Embedding 서비스를 위한 Dockerfile
│   ├── Dockerfile.vector-db    # Vector DB 서비스를 위한 Dockerfile
│   └── Dockerfile.llm          # LLM 서비스를 위한 Dockerfile
│
├── docker-compose.yml          # 전체 서비스 오케스트레이션
│
├── src/
│   ├── app/                    # Web App 관련 코드
│   │   ├── main.py            # FastAPI/Flask 메인 앱
│   │   ├── routes/            # API 라우트
│   │   └── templates/         # 웹 템플릿
│   │
│   ├── embedding/             # Embedding 서비스 관련 코드
│   │   ├── model.py           # Embedding 모델 관리
│   │   └── service.py         # Embedding 처리 로직
│   │
│   ├── vector_db/            # Vector DB 관련 코드
│   │   ├── client.py         # DB 클라이언트
│   │   └── operations.py     # DB 작업 관련 로직
│   │
│   ├── llm/                  # LLM 서비스 관련 코드
│   │   ├── model.py          # LLM 모델 관리
│   │   └── service.py        # 생성 로직
│   │
│   └── preprocessor/         # 문서 전처리 관련 코드
│       ├── parser.py         # 문서 파싱
│       └── cleaner.py        # 데이터 정제
│
├── config/
│   ├── app.yml              # 앱 설정
│   ├── model.yml           # 모델 설정
│   └── db.yml             # 데이터베이스 설정
│
├── tests/                  # 테스트 코드
│   ├── test_app/
│   ├── test_embedding/
│   ├── test_vector_db/
│   └── test_llm/
│
├── data/                   # 데이터 저장소
│   ├── raw/               # 원본 문서
│   ├── processed/         # 전처리된 문서
│   └── embeddings/        # 임베딩 결과
│
├── scripts/               # 유틸리티 스크립트
│   ├── setup.sh          # 초기 설정 스크립트
│   └── download_models.sh # 모델 다운로드 스크립트
│
├── requirements/          # Python 패키지 요구사항
│   ├── base.txt          # 공통 요구사항
│   ├── app.txt           # Web App 요구사항
│   ├── embedding.txt     # Embedding 서비스 요구사항
│   └── llm.txt          # LLM 서비스 요구사항
│
└── README.md             # 프로젝트 문서
```

## 특징
1. 마이크로서비스 아키텍처 지원
   - 각 핵심 컴포넌트(웹 앱, 임베딩, Vector DB, LLM)가 독립적인 서비스로 구성
   - 각각의 Dockerfile과 관련 코드가 분리되어 있어 독립적으로 확장 가능

2. 모듈화된 소스 코드 구조
   - `src` 디렉토리 아래에 각 서비스별 코드가 분리
   - 각 서비스는 자체적인 모델과 서비스 로직을 포함

3. 설정 관리
   - `config` 디렉토리에서 중앙집중식 설정 관리
   - 환경별로 설정을 쉽게 변경 가능

4. 데이터 파이프라인 지원
   - `data` 디렉토리에서 데이터 처리 단계별로 구분된 저장소
   - 원본 문서부터 임베딩까지의 데이터 흐름을 명확히 표현

5. 의존성 관리
   - 서비스별로 분리된 requirements 파일로 의존성 관리
   - 각 서비스의 특정 요구사항을 독립적으로 관리 가능

추가적인 구성이나 특정 서비스에 대한 상세한 구조가 필요하시다면 말씀해 주세요.