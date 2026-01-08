from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit, QHeaderView
)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime


class InventorySummaryTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        header_layout = QHBoxLayout()
        
        title = QLabel('재고 현황')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        header_layout.addWidget(QLabel('기준일:'))
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        header_layout.addWidget(self.date_edit)
        
        refresh_btn = QPushButton('조회')
        refresh_btn.clicked.connect(self.load_summary)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        info_label = QLabel(
            '현재 창고와 쇼케이스의 재고 상태를 확인합니다.\n'
            '창고는 박스 단위, 쇼케이스는 개수 단위로 표시됩니다.'
        )
        info_label.setStyleSheet('padding: 10px; background-color: #e3f2fd; border-radius: 5px;')
        layout.addWidget(info_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            '품목명', '창고(박스)', '창고(개)', '쇼케1', '쇼케2',
            '쇼케3', '쇼케4', '쇼케5', '쇼케합계', '총재고'
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 10):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        self.load_summary()
    
    def load_summary(self):
        date = self.date_edit.date().toString('yyyy-MM-dd')
        
        try:
            summary = self.main_window.manager.get_inventory_summary(date)
            
            self.table.setRowCount(len(summary))
            
            for row, item in enumerate(summary):
                self.table.setItem(row, 0, QTableWidgetItem(item['product_name']))
                self.table.setItem(row, 1, QTableWidgetItem(f"{item['warehouse_boxes']:.1f}"))
                self.table.setItem(row, 2, QTableWidgetItem(f"{item['warehouse_units']:.0f}"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{item['showcase_1']}"))
                self.table.setItem(row, 4, QTableWidgetItem(f"{item['showcase_2']}"))
                self.table.setItem(row, 5, QTableWidgetItem(f"{item['showcase_3']}"))
                self.table.setItem(row, 6, QTableWidgetItem(f"{item['showcase_4']}"))
                self.table.setItem(row, 7, QTableWidgetItem(f"{item['showcase_5']}"))
                self.table.setItem(row, 8, QTableWidgetItem(f"{item['total_showcase_units']}"))
                
                total = item['warehouse_units'] + item['total_showcase_units']
                self.table.setItem(row, 9, QTableWidgetItem(f"{total:.0f}"))
            
            if len(summary) == 0:
                self.table.setRowCount(1)
                no_data = QTableWidgetItem('재고 데이터가 없습니다')
                no_data.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(0, 0, no_data)
                self.table.setSpan(0, 0, 1, 10)
        
        except Exception as e:
            self.main_window.show_error(f'조회 중 오류: {str(e)}')
