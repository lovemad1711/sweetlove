from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit, QComboBox, QDoubleSpinBox,
    QLineEdit, QHeaderView, QGroupBox, QFormLayout, QCheckBox
)
from PyQt5.QtCore import Qt, QDate


class OutboundTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel('출고 관리')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        layout.addWidget(title)
        
        input_group = QGroupBox('출고 데이터 입력')
        input_layout = QFormLayout()
        input_group.setLayout(input_layout)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        input_layout.addRow('날짜:', self.date_edit)
        
        self.product_combo = QComboBox()
        self.load_products()
        input_layout.addRow('품목:', self.product_combo)
        
        self.boxes_spin = QDoubleSpinBox()
        self.boxes_spin.setMinimum(0)
        self.boxes_spin.setMaximum(10000)
        self.boxes_spin.setSingleStep(0.5)
        self.boxes_spin.setSuffix(' 박스')
        input_layout.addRow('박스 수량:', self.boxes_spin)
        
        self.auto_distribute_check = QCheckBox('쇼케이스에 자동 배분')
        self.auto_distribute_check.setChecked(True)
        input_layout.addRow('', self.auto_distribute_check)
        
        self.notes_edit = QLineEdit()
        input_layout.addRow('비고:', self.notes_edit)
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton('출고 등록')
        add_btn.clicked.connect(self.add_entry)
        button_layout.addWidget(add_btn)
        
        clear_btn = QPushButton('초기화')
        clear_btn.setStyleSheet('background-color: #95a5a6;')
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_btn)
        
        input_layout.addRow(button_layout)
        
        layout.addWidget(input_group)
        
        history_layout = QHBoxLayout()
        
        history_label = QLabel('출고 내역')
        history_label.setStyleSheet('font-size: 14pt; font-weight: bold;')
        history_layout.addWidget(history_label)
        
        history_layout.addStretch()
        
        refresh_btn = QPushButton('새로고침')
        refresh_btn.clicked.connect(self.load_history)
        history_layout.addWidget(refresh_btn)
        
        layout.addLayout(history_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            '날짜', '품목명', '박스 수량', '개수 (환산)', '비고'
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        self.load_history()
    
    def load_products(self):
        self.product_combo.clear()
        products = self.main_window.db.get_products(active_only=True)
        
        for product in products:
            self.product_combo.addItem(
                f"{product['name']} ({product['units_per_box']}개/박스)",
                product['id']
            )
    
    def clear_form(self):
        self.date_edit.setDate(QDate.currentDate())
        self.product_combo.setCurrentIndex(0)
        self.boxes_spin.setValue(0)
        self.auto_distribute_check.setChecked(True)
        self.notes_edit.clear()
    
    def add_entry(self):
        if self.product_combo.count() == 0:
            self.main_window.show_warning('먼저 품목을 등록하세요')
            return
        
        date = self.date_edit.date().toString('yyyy-MM-dd')
        product_id = self.product_combo.currentData()
        boxes = self.boxes_spin.value()
        notes = self.notes_edit.text().strip()
        auto_distribute = self.auto_distribute_check.isChecked()
        
        if boxes <= 0:
            self.main_window.show_warning('박스 수량을 입력하세요')
            return
        
        try:
            self.main_window.db.add_outbound_entry(date, product_id, boxes, notes)
            
            if auto_distribute:
                try:
                    self.main_window.manager.distribute_outbound_to_showcases(
                        date, product_id, boxes
                    )
                    self.main_window.show_success(
                        '출고 데이터가 추가되고 쇼케이스에 자동 배분되었습니다'
                    )
                except Exception as e:
                    self.main_window.show_warning(
                        f'출고 데이터가 추가되었으나 자동 배분 중 오류가 발생했습니다:\n{str(e)}'
                    )
            else:
                self.main_window.show_success('출고 데이터가 추가되었습니다')
            
            self.clear_form()
            self.load_history()
            
        except Exception as e:
            self.main_window.show_error(f'등록 중 오류: {str(e)}')
    
    def load_history(self):
        outbound = self.main_window.db.get_outbound()
        
        self.table.setRowCount(len(outbound))
        
        for row, item in enumerate(reversed(outbound[-100:])):
            self.table.setItem(row, 0, QTableWidgetItem(item['date']))
            self.table.setItem(row, 1, QTableWidgetItem(item['product_name']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item['boxes']:.1f}"))
            
            total_units = item['boxes'] * item['units_per_box']
            self.table.setItem(row, 3, QTableWidgetItem(f"{total_units:.0f}개"))
            self.table.setItem(row, 4, QTableWidgetItem(item.get('notes', '')))
        
        if len(outbound) == 0:
            self.table.setRowCount(1)
            no_data = QTableWidgetItem('출고 내역이 없습니다')
            no_data.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, 0, no_data)
            self.table.setSpan(0, 0, 1, 5)
