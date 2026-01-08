# 술음료 재고관리 시스템 (PyQt5 버전)

## 개요
술과 음료의 재고를 효율적으로 관리하기 위한 **데스크톱 애플리케이션**입니다. 
PyQt5 GUI 프레임워크를 사용하여 Windows, macOS, Linux에서 모두 실행 가능합니다.

## 주요 특징
- ✅ **완전한 로컬 애플리케이션**: 인터넷 연결 불필요
- ✅ **직관적인 GUI**: 탭 기반 인터페이스로 쉬운 사용
- ✅ **실시간 데이터**: 즉시 업데이트되는 재고 현황
- ✅ **자동 배분**: 쇼케이스 자동 배분 알고리즘
- ✅ **상세 분석**: 주간/월간/연간 보고서
- ✅ **안전한 백업**: 5년 보관 정책

## 시스템 요구사항
- Python 3.8 이상
- 최소 512MB RAM
- 100MB 여유 디스크 공간

## 설치 방법

### 1. Python 설치
먼저 Python이 설치되어 있는지 확인합니다:
```bash
python --version
```

Python이 없다면 [python.org](https://www.python.org/downloads/)에서 다운로드하세요.

### 2. 프로젝트 다운로드
```bash
# Git이 설치되어 있다면
git clone <repository-url>
cd <project-directory>

# 또는 ZIP 파일을 다운로드하고 압축 해제
```

### 3. 가상환경 생성 (권장)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 실행 방법

### 일반 실행
```bash
python main.py
```

### Windows에서 더블클릭 실행
`main.py` 파일을 더블클릭하면 자동으로 실행됩니다.

### 바로가기 생성 (Windows)
1. `main.py` 파일 우클릭
2. "바로 가기 만들기" 선택
3. 바로가기를 바탕화면으로 이동

## 사용 가이드

### 첫 실행 시 설정 순서
1. **품목 관리** 탭
   - "품목 추가" 버튼 클릭
   - 제품 정보 입력 (품목명, 박스당 수량, 단가)
   - 판매하는 모든 제품을 등록

2. **쇼케이스 설정** 탭
   - 각 쇼케이스의 최대 용량 설정
   - 사용할 품목 체크
   - "설정 저장" 버튼 클릭

3. **초기 데이터** 탭
   - 기준 날짜 선택
   - 현재 보유중인 재고 입력
   - 창고: 박스 단위
   - 쇼케이스 1~5: 개수 단위
   - "초기 데이터 저장" 버튼 클릭

### 일일 운영

#### 아침 업무
1. **입고 관리** 탭
   - 새로 들어온 제품 등록
   - 날짜, 품목, 박스 수량 입력

2. **출고 관리** 탭
   - 쇼케이스로 출고할 제품 등록
   - "쇼케이스에 자동 배분" 체크 (권장)
   - 자동으로 쇼케이스 1부터 배분됨

#### 저녁 업무
1. **판매 관리** 탭
   - 하루 실제 판매량 입력
   - 날짜, 품목, 판매 수량 입력

2. **재고 현황** 탭
   - 현재 재고 상태 확인
   - 창고와 쇼케이스별 재고 확인

### 주간/월간 분석
1. **분석 보고서** 탭
   - 보고서 유형 선택 (주간/월간/연간)
   - 기준 날짜 선택
   - "보고서 생성" 버튼 클릭
   - 예측 vs 실제 판매 비교
   - 차이 분석 및 원인 파악

### 데이터 백업
1. **백업 관리** 탭
   - 백업 메모 입력 (선택사항)
   - "백업 생성" 버튼 클릭
   - 정기적으로 백업 권장 (주 1회 이상)

## UI 구성

### 탭 구조
```
홈
├─ 품목관리          # 제품 CRUD
├─ 초기데이터        # 재고 시작점 설정
├─ 쇼케이스설정      # 용량 및 사용 설정
├─ 입고관리          # 창고 입고 등록
├─ 출고관리          # 창고→쇼케이스 출고
├─ 쇼케이스          # 쇼케이스 현황 조회
├─ 판매관리          # 실제 판매 등록
├─ 재고현황          # 전체 재고 현황
├─ 분석보고서        # 주간/월간/연간 분석
└─ 백업관리          # 백업 및 복원
```

### 단축키
- `Ctrl+1~0`: 탭 전환
- `Enter`: 폼 제출
- `Esc`: 다이얼로그 닫기

## 데이터 파일 위치
```
project/
├── data/
│   └── inventory.db      # 메인 데이터베이스
├── backups/
│   ├── inventory_backup_*.db    # 백업 파일
│   └── backup_metadata_*.txt    # 백업 메타데이터
└── archives/
    └── inventory_backup_*.db    # 영구 보관 파일
```

## 문제 해결

### 프로그램이 실행되지 않을 때
1. Python 버전 확인
   ```bash
   python --version
   ```
   Python 3.8 이상이어야 합니다.

2. 패키지 재설치
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. 가상환경 재생성
   ```bash
   # 기존 가상환경 삭제
   rm -rf venv  # Linux/Mac
   rmdir /s venv  # Windows
   
   # 새로 생성
   python -m venv venv
   source venv/bin/activate  # 또는 venv\Scripts\activate
   pip install -r requirements.txt
   ```

### PyQt5 설치 오류
Windows에서 PyQt5 설치 시 오류가 발생하면:
```bash
pip install PyQt5 --user
```

### 데이터베이스 오류
1. `data/` 폴더가 존재하는지 확인
2. 권한 문제 확인
3. 백업에서 복원 시도

### 한글 표시 문제
- 시스템에 한글 폰트가 설치되어 있어야 합니다
- Windows: 기본 제공
- macOS: 기본 제공
- Linux: 
  ```bash
  sudo apt-get install fonts-nanum
  ```

## 성능 최적화

### 대용량 데이터 처리
- 6개월마다 백업 후 초기 데이터 재설정 권장
- 백업 파일은 별도 보관

### 메모리 사용량 줄이기
- 불필요한 탭 닫기 (프로그램 재시작)
- 오래된 데이터 정리

## 개발자 정보

### 프로젝트 구조
```
project/
├── main.py              # 메인 애플리케이션
├── database.py          # 데이터베이스 관리
├── inventory_manager.py # 재고 비즈니스 로직
├── backup_manager.py    # 백업 관리
├── analysis.py          # 분석 및 차트
├── ui/                  # UI 모듈
│   ├── __init__.py
│   ├── products_tab.py
│   ├── initial_data_tab.py
│   ├── showcase_config_tab.py
│   ├── warehouse_tab.py
│   ├── outbound_tab.py
│   ├── showcase_tab.py
│   ├── sales_tab.py
│   ├── inventory_summary_tab.py
│   ├── reports_tab.py
│   └── backups_tab.py
└── requirements.txt
```

### 기술 스택
- **GUI**: PyQt5 5.15
- **Database**: SQLite3
- **Charts**: Matplotlib 3.8
- **Data**: Pandas 2.1

### 커스터마이징
스타일을 변경하려면 `main.py`의 `apply_styles()` 메서드를 수정하세요.

## 라이선스
단일 회사 전용 시스템

## 지원
문제가 발생하면 시스템 관리자에게 문의하세요.

---

## 자주 묻는 질문 (FAQ)

**Q: 여러 컴퓨터에서 사용할 수 있나요?**
A: 네, `data/` 폴더를 복사하면 됩니다. 단, 동시 접근은 불가능합니다.

**Q: 데이터를 Excel로 내보낼 수 있나요?**
A: SQLite 뷰어를 사용하거나 별도 기능 추가가 필요합니다.

**Q: 자동 백업 기능이 있나요?**
A: 현재는 수동 백업만 지원합니다. 자동 백업은 추후 추가 예정입니다.

**Q: 네트워크로 다른 컴퓨터와 공유할 수 있나요?**
A: 현재는 로컬 전용입니다. 네트워크 기능은 별도 개발이 필요합니다.

**Q: 프로그램을 업데이트하면 데이터가 유지되나요?**
A: 네, `data/` 폴더만 그대로 두면 됩니다.
