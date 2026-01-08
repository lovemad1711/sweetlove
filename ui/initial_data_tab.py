from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit, QHeaderView, QDoubleSpinBox,
    QSpinBox, QLineEdit
)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime


class InitialDataTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel('초기 데이터 설정')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        layout.addWidget(title)
        
        info_label = QLabel(
            '재고 관리를 시작하기 전에 현재 보유중인 재고의 초기값을 설정합니다.'
        )
        info_label.setStyleSheet('padding: 10px; background-color: #e3f2fd; border-radius: 5px;')
        layout.addWidget(info_label)
        
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel('기준 날짜:'))
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        date_layout.addWidget(self.date_edit)
        
        date_layout.addStretch()
        
        save_btn = QPushButton('초기 데이터 저장')
        save_btn.clicked.connect(self.save_initial_data)
        date_layout.addWidget(save_btn)
        
        load_btn = QPushButton('품목 불러오기')
        load_btn.setStyleSheet('background-color: #95a5a6;')
        load_btn.clicked.connect(self.load_products)
        date_layout.addWidget(load_btn)
        
        layout.addLayout(date_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            '품목명', '창고(박스)', '쇼케이스1', '쇼케이스2', '쇼케이스3',
            '쇼케이스4', '쇼케이스5', '비고', 'ID'
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 8):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        self.table.setColumnHidden(8, True)
        
        layout.addWidget(self.table)
        
        self.load_products()
    
    def load_products(self):
        products = self.main_window.db.get_products(active_only=True)
        
        self.table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product['name']))
            
            warehouse_spin = QDoubleSpinBox()
            warehouse_spin.setMinimum(0)
            warehouse_spin.setMaximum(10000)
            warehouse_spin.setSingleStep(0.5)
            self.table.setCellWidget(row, 1, warehouse_spin)
            
            for col in range(2, 7):
                showcase_spin = QSpinBox()
                showcase_spin.setMinimum(0)
                showcase_spin.setMaximum(10000)
                self.table.setCellWidget(row, col, showcase_spin)
            
            notes_edit = QLineEdit()
            self.table.setCellWidget(row, 7, notes_edit)
            
            self.table.setItem(row, 8, QTableWidgetItem(str(product['id'])))
        
        if len(products) == 0:
            self.table.setRowCount(1)
            no_data = QTableWidgetItem('먼저 품목을 등록해주세요')
            no_data.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, 0, no_data)
            self.table.setSpan(0, 0, 1, 8)
    
    def save_initial_data(self):
        date = self.date_edit.date().toString('yyyy-MM-dd')
        
        if self.table.rowCount() == 0:
            self.main_window.show_warning('저장할 데이터가 없습니다')
            return
        
        try:
            for row in range(self.table.rowCount()):
                product_id_item = self.table.item(row, 8)
                if not product_id_item:
                    continue
                
                product_id = int(product_id_item.text())
                
                warehouse_widget = self.table.cellWidget(row, 1)
                warehouse_boxes = warehouse_widget.value() if warehouse_widget else 0
                
                showcase_units = {}
                for i in range(1, 6):
                    widget = self.table.cellWidget(row, i + 1)
                    showcase_units[i] = widget.value() if widget else 0
                
                notes_widget = self.table.cellWidget(row, 7)
                notes = notes_widget.text() if notes_widget else ''
                
                self.main_window.db.set_initial_data(
                    date, product_id, warehouse_boxes, showcase_units, notes
                )
            
            self.main_window.show_success(f'{date} 날짜의 초기 데이터가 저장되었습니다')
            
        except Exception as e:
            self.main_window.show_error(f'저장 중 오류: {str(e)}')
