# 시스템 아키텍처

## 전체 구조

```
┌─────────────────────────────────────────────────────────┐
│                     웹 브라우저                          │
│              (사용자 인터페이스)                         │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP 요청/응답
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Flask 웹 애플리케이션                   │
│                     (app.py)                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │          라우트 및 뷰 함수                        │  │
│  │  - 품목 관리                                      │  │
│  │  - 재고 관리 (입고, 출고, 쇼케이스, 판매)        │  │
│  │  - 보고서 생성                                    │  │
│  │  - 백업 관리                                      │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
┌──────────┐  ┌──────────────┐  ┌─────────┐
│          │  │              │  │         │
│ Inventory│  │   Backup     │  │Analysis │
│ Manager  │  │   Manager    │  │ Module  │
│          │  │              │  │         │
└────┬─────┘  └──────┬───────┘  └────┬────┘
     │               │               │
     └───────────────┼───────────────┘
                     ▼
           ┌──────────────────┐
           │                  │
           │  Database Module │
           │   (database.py)  │
           │                  │
           └────────┬─────────┘
                    ▼
           ┌──────────────────┐
           │                  │
           │    SQLite3 DB    │
           │ (inventory.db)   │
           │                  │
           └──────────────────┘
```

## 계층 구조

### 1. 프레젠테이션 계층 (Presentation Layer)
- **위치**: `templates/`, `static/css/`
- **역할**: 사용자 인터페이스 제공
- **기술**: HTML5, CSS3, Jinja2 템플릿

#### 주요 템플릿
- `base.html`: 기본 레이아웃
- `index.html`: 메인 대시보드
- 품목 관리: `products.html`, `add_product.html`, `edit_product.html`
- 데이터 입력: `warehouse.html`, `outbound.html`, `showcase.html`, `sales.html`
- 보고서: `weekly_report.html`, `monthly_report.html`, `yearly_report.html`

### 2. 애플리케이션 계층 (Application Layer)
- **위치**: `app.py`
- **역할**: HTTP 요청 처리 및 라우팅
- **기술**: Flask 3.0

#### 주요 라우트
```python
# 품목 관리
GET  /products              # 품목 목록
GET  /products/add          # 품목 추가 폼
POST /products/add          # 품목 추가 처리
GET  /products/edit/<id>    # 품목 수정 폼
POST /products/edit/<id>    # 품목 수정 처리
POST /products/delete/<id>  # 품목 삭제

# 데이터 입력
GET/POST /warehouse         # 입고 관리
GET/POST /outbound          # 출고 관리
GET/POST /showcases/<num>   # 쇼케이스 관리
GET/POST /sales             # 판매 관리

# 보고서
GET /reports/weekly         # 주간 보고서
GET /reports/monthly        # 월간 보고서
GET /reports/yearly         # 연간 보고서

# 기타
GET/POST /initial-data      # 초기 데이터
GET/POST /showcase-config   # 쇼케이스 설정
GET /inventory-summary      # 재고 현황
GET/POST /backups           # 백업 관리
```

### 3. 비즈니스 로직 계층 (Business Logic Layer)

#### 3.1 재고 관리 (`inventory_manager.py`)
```python
class InventoryManager:
    - calculate_current_warehouse_inventory()  # 현재 창고 재고 계산
    - calculate_current_showcase_inventory()   # 현재 쇼케이스 재고 계산
    - calculate_predicted_sales()              # 예측 판매 계산
    - calculate_actual_sales()                 # 실제 판매 계산
    - calculate_discrepancy()                  # 차이 분석
    - distribute_outbound_to_showcases()       # 자동 배분
    - move_showcase_inventory()                # 쇼케이스 간 이동
    - get_inventory_summary()                  # 재고 요약
    - get_weekly_report()                      # 주간 보고서
    - get_monthly_report()                     # 월간 보고서
```

#### 3.2 백업 관리 (`backup_manager.py`)
```python
class BackupManager:
    - create_backup()          # 백업 생성
    - list_backups()           # 백업 목록
    - restore_backup()         # 백업 복원
    - delete_old_backups()     # 오래된 백업 삭제
    - archive_backup()         # 영구 보관
```

#### 3.3 분석 모듈 (`analysis.py`)
```python
class InventoryAnalyzer:
    - generate_weekly_comparison_chart()     # 주간 비교 차트
    - generate_discrepancy_chart()           # 차이 분석 차트
    - generate_monthly_trend_chart()         # 월별 추이 차트
    - generate_product_comparison_chart()    # 품목 비교 차트
    - generate_yearly_report()               # 연간 보고서
    - generate_yearly_comparison_chart()     # 연간 비교 차트
```

### 4. 데이터 접근 계층 (Data Access Layer)
- **위치**: `database.py`
- **역할**: 데이터베이스 CRUD 작업
- **기술**: SQLite3

#### 주요 메서드
```python
class InventoryDatabase:
    # 품목 관리
    - add_product()
    - get_products()
    - get_product_by_id()
    - update_product()
    - delete_product()
    
    # 데이터 입력
    - add_warehouse_entry()
    - add_outbound_entry()
    - add_showcase_entry()
    - add_sales_entry()
    - set_initial_data()
    
    # 조회
    - get_warehouse_inventory()
    - get_outbound()
    - get_sales()
    - get_showcase_data()
    - get_initial_data()
    
    # 설정
    - update_showcase_config()
    - get_showcase_config()
    - get_all_showcase_configs()
```

### 5. 데이터베이스 계층 (Database Layer)
- **위치**: `data/inventory.db`
- **기술**: SQLite3

## 데이터 흐름

### 입고 프로세스
```
1. 사용자가 입고 폼 작성
   ↓
2. POST /warehouse 요청
   ↓
3. app.py의 warehouse() 함수 처리
   ↓
4. database.add_warehouse_entry() 호출
   ↓
5. SQLite3 INSERT 실행
   ↓
6. 성공 메시지 표시
```

### 출고 및 자동 배분 프로세스
```
1. 사용자가 출고 폼 작성 (자동 배분 체크)
   ↓
2. POST /outbound 요청
   ↓
3. app.py의 outbound() 함수 처리
   ↓
4. database.add_outbound_entry() 호출
   ↓
5. inventory_manager.distribute_outbound_to_showcases() 호출
   ↓
6. 쇼케이스 설정 조회
   ↓
7. 쇼케이스 1부터 순차적으로 재고 추가
   ↓
8. 용량 초과 시 다음 쇼케이스로 이동
   ↓
9. 각 쇼케이스에 database.add_showcase_entry() 호출
   ↓
10. 성공 메시지 표시
```

### 보고서 생성 프로세스
```
1. 사용자가 주간 보고서 요청
   ↓
2. GET /reports/weekly?start_date=...
   ↓
3. app.py의 weekly_report() 함수 처리
   ↓
4. inventory_manager.get_weekly_report() 호출
   ↓
5. 각 품목별로:
   - calculate_predicted_sales()
   - calculate_actual_sales()
   - calculate_discrepancy()
   ↓
6. analyzer.generate_weekly_comparison_chart() 호출
   ↓
7. Matplotlib으로 차트 생성
   ↓
8. 차트 이미지 저장 (static/charts/)
   ↓
9. 템플릿에 데이터와 차트 경로 전달
   ↓
10. HTML 렌더링 및 응답
```

## 주요 알고리즘

### 1. 현재 재고 계산
```python
def calculate_current_warehouse_inventory(product_id, end_date):
    # 초기 재고 조회
    initial = get_initial_data(product_id)
    
    # 입고 합계
    total_inbound = sum(get_warehouse_inventory(product_id, start_date, end_date))
    
    # 출고 합계
    total_outbound = sum(get_outbound(product_id, start_date, end_date))
    
    # 현재 재고 = 초기 + 입고 - 출고
    current = initial + total_inbound - total_outbound
    
    return current
```

### 2. 자동 배분 알고리즘
```python
def distribute_outbound_to_showcases(date, product_id, boxes):
    # 박스를 개수로 환산
    total_units = boxes * units_per_box
    remaining_units = total_units
    
    # 쇼케이스 1부터 5까지 순회
    for showcase_num in [1, 2, 3, 4, 5]:
        if remaining_units <= 0:
            break
        
        # 쇼케이스 설정 확인
        config = get_showcase_config(showcase_num, product_id)
        
        # 사용 여부 확인
        if not config.field_active:
            continue
        
        # 현재 재고와 최대 용량 확인
        current = calculate_current_showcase_inventory(showcase_num, product_id)
        max_capacity = config.max_capacity
        available_space = max_capacity - current
        
        # 추가 가능한 만큼 추가
        if available_space > 0:
            units_to_add = min(remaining_units, available_space)
            add_showcase_entry(showcase_num, date, product_id, units_to_add)
            remaining_units -= units_to_add
```

### 3. 예측 판매 vs 실제 판매 차이
```python
def calculate_discrepancy(product_id, start_date, end_date):
    # 예측 판매 = 출고량(개수 환산) - 쇼케이스 재고 증가
    outbound_boxes = sum(get_outbound(product_id, start_date, end_date))
    predicted = outbound_boxes * units_per_box
    
    # 실제 판매
    actual = sum(get_sales(product_id, start_date, end_date))
    
    # 차이
    discrepancy = predicted - actual
    
    return {
        'predicted': predicted,
        'actual': actual,
        'discrepancy': discrepancy,
        'discrepancy_value': discrepancy * unit_price
    }
```

## 설계 원칙

### 1. 단일 책임 원칙 (Single Responsibility Principle)
- 각 모듈은 하나의 명확한 책임을 가짐
- `database.py`: 데이터베이스 접근
- `inventory_manager.py`: 재고 비즈니스 로직
- `backup_manager.py`: 백업 관리
- `analysis.py`: 분석 및 차트 생성

### 2. 관심사의 분리 (Separation of Concerns)
- 프레젠테이션, 비즈니스 로직, 데이터 접근 계층 분리
- HTML/CSS와 Python 코드 분리

### 3. DRY (Don't Repeat Yourself)
- 공통 로직은 함수로 추출
- 템플릿 상속 활용 (base.html)

### 4. 명확한 네이밍
- 함수명: 동사로 시작 (`calculate_`, `get_`, `add_`)
- 변수명: 명확한 의미 전달 (`warehouse_boxes`, `showcase_units`)

## 확장성 고려사항

### 1. 수평 확장
- 다중 지점 지원을 위한 `branch_id` 추가 가능
- 각 지점별 독립적인 데이터베이스

### 2. 수직 확장
- PostgreSQL/MySQL로 데이터베이스 마이그레이션
- Redis 캐싱 추가
- 비동기 작업 처리 (Celery)

### 3. 기능 확장
- RESTful API 추가 (Flask-RESTful)
- 사용자 인증 (Flask-Login)
- 실시간 알림 (WebSocket)
- 모바일 앱 지원

## 보안 고려사항

### 현재 구현
- SQLite 인젝션 방지 (파라미터화된 쿼리)
- 입력 검증 (Flask 폼 검증)

### 향후 추가 가능
- 사용자 인증 및 세션 관리
- CSRF 토큰
- HTTPS 지원
- 데이터베이스 암호화
- 접근 로그 기록

## 성능 최적화

### 데이터베이스
- 인덱스 활용 (`product_id`, `date`)
- 쿼리 최적화 (필요한 컬럼만 조회)
- 연결 풀링

### 애플리케이션
- 차트 캐싱 (자주 조회되는 보고서)
- 페이지네이션 (대량 데이터 조회 시)
- 비동기 작업 (백업, 차트 생성)

### 프론트엔드
- CSS 최소화
- 이미지 최적화
- 브라우저 캐싱

## 테스트 전략

### 단위 테스트
- 각 모듈의 개별 함수 테스트
- `pytest` 활용

### 통합 테스트
- 전체 워크플로우 테스트
- `test_system.py` 활용

### 사용자 테스트
- 실제 사용 시나리오 테스트
- 피드백 수집 및 개선

## 모니터링 및 로깅

### 로깅
- Flask 로깅 설정
- 오류 추적
- 사용자 활동 로그

### 모니터링
- 데이터베이스 크기 모니터링
- 응답 시간 측정
- 백업 상태 확인

## 결론
이 시스템은 명확한 계층 구조와 모듈화된 설계를 통해 유지보수가 용이하고 확장 가능한 구조를 가지고 있습니다.
