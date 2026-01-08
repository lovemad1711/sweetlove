#!/usr/bin/env python3
"""
테스트 스크립트 - 시스템 기능 검증
"""

from database import InventoryDatabase
from inventory_manager import InventoryManager
from backup_manager import BackupManager
from datetime import datetime

def test_system():
    print("=" * 60)
    print("술음료 재고관리 시스템 테스트")
    print("=" * 60)
    
    db = InventoryDatabase()
    manager = InventoryManager()
    backup_mgr = BackupManager()
    
    print("\n1. 품목 추가 테스트")
    print("-" * 60)
    try:
        products_data = [
            ("소주", 20, 1500, "대중적인 소주"),
            ("맥주", 24, 2000, "생맥주"),
            ("와인", 12, 15000, "레드 와인"),
            ("막걸리", 30, 3000, "생막걸리"),
            ("사이다", 20, 1200, "탄산음료"),
        ]
        
        for name, units, price, notes in products_data:
            try:
                product_id = db.add_product(name, units, price, notes)
                print(f"✓ {name} 추가 완료 (ID: {product_id})")
            except ValueError:
                print(f"  {name}은 이미 존재합니다.")
    except Exception as e:
        print(f"✗ 오류: {e}")
    
    print("\n2. 쇼케이스 설정 테스트")
    print("-" * 60)
    products = db.get_products()
    for product in products:
        for showcase_num in range(1, 6):
            max_capacity = 50 if showcase_num == 1 else 30
            db.update_showcase_config(showcase_num, product['id'], max_capacity, 1)
        print(f"✓ {product['name']} 쇼케이스 설정 완료")
    
    print("\n3. 초기 데이터 설정 테스트")
    print("-" * 60)
    today = datetime.now().strftime('%Y-%m-%d')
    for product in products:
        showcase_units = {1: 30, 2: 0, 3: 0, 4: 0, 5: 0}
        db.set_initial_data(today, product['id'], 5.0, showcase_units, "초기 재고")
        print(f"✓ {product['name']} 초기 데이터 설정 (창고: 5박스, 쇼케이스1: 30개)")
    
    print("\n4. 입고/출고 테스트")
    print("-" * 60)
    product = products[0]
    db.add_warehouse_entry(today, product['id'], 3.0, "입고 테스트")
    print(f"✓ {product['name']} 3박스 입고")
    
    db.add_outbound_entry(today, product['id'], 2.0, "출고 테스트")
    print(f"✓ {product['name']} 2박스 출고")
    
    manager.distribute_outbound_to_showcases(today, product['id'], 2.0)
    print(f"✓ {product['name']} 쇼케이스에 자동 배분")
    
    print("\n5. 판매 데이터 입력 테스트")
    print("-" * 60)
    db.add_sales_entry(today, product['id'], 25, "일일 판매")
    print(f"✓ {product['name']} 25개 판매 기록")
    
    print("\n6. 재고 현황 조회 테스트")
    print("-" * 60)
    summary = manager.get_inventory_summary(today)
    for item in summary:
        print(f"{item['product_name']}:")
        print(f"  - 창고: {item['warehouse_boxes']:.1f}박스 ({item['warehouse_units']:.0f}개)")
        print(f"  - 쇼케이스 1: {item['showcase_1']}개")
        print(f"  - 쇼케이스 합계: {item['total_showcase_units']}개")
    
    print("\n7. 주간 보고서 테스트")
    print("-" * 60)
    report = manager.get_weekly_report(today)
    print(f"기간: {report['start_date']} ~ {report['end_date']}")
    print(f"예측 판매: {report['total_predicted_sales']}개")
    print(f"실제 판매: {report['total_actual_sales']}개")
    print(f"차이: {report['total_discrepancy_units']}개")
    
    print("\n8. 백업 테스트")
    print("-" * 60)
    try:
        backup_path = backup_mgr.create_backup("테스트 백업")
        print(f"✓ 백업 생성 완료: {backup_path}")
        
        backups = backup_mgr.list_backups()
        print(f"✓ 총 {len(backups)}개의 백업 파일 존재")
    except Exception as e:
        print(f"✗ 백업 오류: {e}")
    
    print("\n" + "=" * 60)
    print("모든 테스트 완료!")
    print("=" * 60)
    print("\n웹 애플리케이션을 실행하려면:")
    print("  python app.py")
    print("\n그 다음 브라우저에서 http://localhost:5000 을 열어주세요.")

if __name__ == '__main__':
    test_system()
