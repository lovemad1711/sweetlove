from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QComboBox, QHeaderView
)
from PyQt5.QtCore import Qt


class ShowcaseTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        header_layout = QHBoxLayout()
        
        title = QLabel('쇼케이스 관리')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        header_layout.addWidget(QLabel('쇼케이스 선택:'))
        
        self.showcase_combo = QComboBox()
        for i in range(1, 6):
            self.showcase_combo.addItem(f'쇼케이스 {i}', i)
        self.showcase_combo.currentIndexChanged.connect(self.load_showcase_data)
        header_layout.addWidget(self.showcase_combo)
        
        layout.addLayout(header_layout)
        
        info_label = QLabel(
            '쇼케이스별 현재 재고 상태를 확인할 수 있습니다. '
            '수동 조정이 필요한 경우 출고 탭을 이용하세요.'
        )
        info_label.setStyleSheet('padding: 10px; background-color: #e3f2fd; border-radius: 5px;')
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            '품목명', '현재 재고', '최대 용량', '사용률'
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        self.load_showcase_data()
    
    def load_showcase_data(self):
        showcase_num = self.showcase_combo.currentData()
        if not showcase_num:
            return
        
        products = self.main_window.db.get_products(active_only=True)
        configs = self.main_window.db.get_all_showcase_configs()
        
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        self.table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product['name']))
            
            current = self.main_window.manager.calculate_current_showcase_inventory(
                showcase_num, product['id'], today
            )
            self.table.setItem(row, 1, QTableWidgetItem(f"{current}개"))
            
            max_capacity = 0
            if showcase_num in configs and product['id'] in configs[showcase_num]:
                max_capacity = configs[showcase_num][product['id']]['max_capacity']
            
            self.table.setItem(row, 2, QTableWidgetItem(f"{max_capacity}개"))
            
            usage = (current / max_capacity * 100) if max_capacity > 0 else 0
            usage_item = QTableWidgetItem(f"{usage:.1f}%")
            
            if usage >= 90:
                usage_item.setBackground(Qt.red)
            elif usage >= 70:
                usage_item.setBackground(Qt.yellow)
            else:
                usage_item.setBackground(Qt.green)
            
            self.table.setItem(row, 3, usage_item)
