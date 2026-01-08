#!/usr/bin/env python3
"""
모든 UI 탭에 폰트 개선 자동 적용 스크립트
"""

import os
import re

# UI 탭 파일 목록
ui_files = [
    'ui/outbound_tab.py',
    'ui/sales_tab.py',
    'ui/showcase_tab.py',
    'ui/inventory_summary_tab.py',
    'ui/reports_tab.py',
    'ui/backups_tab.py',
    'ui/initial_data_tab.py',
    'ui/showcase_config_tab.py'
]

def add_imports(content):
    """필요한 import 추가"""
    if 'from .ui_helpers import' in content:
        return content
    
    # QFont import 추가
    if 'from PyQt5.QtGui import' not in content:
        content = re.sub(
            r'(from PyQt5\.QtCore import.*)',
            r'\1\nfrom PyQt5.QtGui import QFont',
            content
        )
    
    # ui_helpers import 추가
    content = re.sub(
        r'(from PyQt5\.QtGui import.*)',
        r'\1\nfrom .ui_helpers import create_table_item, get_standard_font, set_row_heights',
        content
    )
    
    return content

def fix_table_items(content):
    """QTableWidgetItem을 create_table_item으로 변경"""
    # 간단한 QTableWidgetItem(...) 패턴 교체
    content = re.sub(
        r'QTableWidgetItem\(([^)]+)\)',
        r'create_table_item(\1)',
        content
    )
    
    return content

def add_row_heights(content):
    """set_row_heights 호출 추가"""
    # load_history, load_products 등의 함수 마지막에 추가
    # 이미 있으면 건너뜀
    if 'set_row_heights' in content:
        return content
    
    # for row... 패턴 찾아서 그 다음에 추가
    content = re.sub(
        r'(for row.*?self\.table\.setItem.*?\n)(        \n        if len)',
        r'\1        set_row_heights(self.table, 40)\n\2',
        content,
        flags=re.DOTALL
    )
    
    return content

def process_file(filepath):
    """파일 처리"""
    print(f"Processing {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # 개선 적용
        content = add_imports(content)
        content = fix_table_items(content)
        content = add_row_heights(content)
        
        # 변경사항이 있으면 저장
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Updated {filepath}")
        else:
            print(f"  - No changes needed for {filepath}")
    
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")

def main():
    print("=" * 60)
    print("UI 탭 폰트 개선 자동 적용")
    print("=" * 60)
    print()
    
    for ui_file in ui_files:
        if os.path.exists(ui_file):
            process_file(ui_file)
        else:
            print(f"  ! File not found: {ui_file}")
    
    print()
    print("=" * 60)
    print("완료!")
    print("=" * 60)
    print()
    print("프로그램을 다시 실행하세요:")
    print("  python main.py")

if __name__ == '__main__':
    main()
