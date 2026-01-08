"""
UI 공통 헬퍼 함수
"""
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtCore import Qt


def create_table_item(text, font_size=10, align_center=False):
    """
    테이블 아이템 생성 (폰트와 색상 설정 포함)
    """
    item = QTableWidgetItem(str(text))
    
    font = QFont()
    font.setPointSize(font_size)
    item.setFont(font)
    
    item.setForeground(QBrush(QColor(0, 0, 0)))
    
    if align_center:
        item.setTextAlignment(Qt.AlignCenter)
    
    return item


def get_standard_font(size=10, bold=False):
    """
    표준 폰트 반환
    """
    font = QFont()
    font.setPointSize(size)
    if bold:
        font.setBold(True)
    return font


def set_row_heights(table, height=40):
    """
    테이블의 모든 행 높이 설정
    """
    for row in range(table.rowCount()):
        table.setRowHeight(row, height)
