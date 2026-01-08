from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit, QComboBox, QSpinBox,
    QLineEdit, QHeaderView, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, QDate


class SalesTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel('판매 관리')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        layout.addWidget(title)
        
        input_group = QGroupBox('판매 데이터 입력')
        input_layout = QFormLayout()
        input_group.setLayout(input_layout)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        input_layout.addRow('날짜:', self.date_edit)
        
        self.product_combo = QComboBox()
        self.load_products()
        input_layout.addRow('품목:', self.product_combo)
        
        self.units_spin = QSpinBox()
        self.units_spin.setMinimum(0)
        self.units_spin.setMaximum(100000)
        self.units_spin.setSuffix(' 개')
        input_layout.addRow('판매 수량:', self.units_spin)
        
        self.notes_edit = QLineEdit()
        input_layout.addRow('비고:', self.notes_edit)
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton('판매 등록')
        add_btn.clicked.connect(self.add_entry)
        button_layout.addWidget(add_btn)
        
        clear_btn = QPushButton('초기화')
        clear_btn.setStyleSheet('background-color: #95a5a6;')
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_btn)
        
        input_layout.addRow(button_layout)
        
        layout.addWidget(input_group)
        
        history_layout = QHBoxLayout()
        
        history_label = QLabel('판매 내역')
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
            '날짜', '품목명', '판매 수량', '판매 금액', '비고'
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
                f"{product['name']} ({product['unit_price']:,.0f}원)",
                product['id']
            )
    
    def clear_form(self):
        self.date_edit.setDate(QDate.currentDate())
        self.product_combo.setCurrentIndex(0)
        self.units_spin.setValue(0)
        self.notes_edit.clear()
    
    def add_entry(self):
        if self.product_combo.count() == 0:
            self.main_window.show_warning('먼저 품목을 등록하세요')
            return
        
        date = self.date_edit.date().toString('yyyy-MM-dd')
        product_id = self.product_combo.currentData()
        units = self.units_spin.value()
        notes = self.notes_edit.text().strip()
        
        if units <= 0:
            self.main_window.show_warning('판매 수량을 입력하세요')
            return
        
        try:
            self.main_window.db.add_sales_entry(date, product_id, units, notes)
            self.main_window.show_success('판매 데이터가 추가되었습니다')
            self.clear_form()
            self.load_history()
        except Exception as e:
            self.main_window.show_error(f'등록 중 오류: {str(e)}')
    
    def load_history(self):
        sales = self.main_window.db.get_sales()
        
        self.table.setRowCount(len(sales))
        
        for row, item in enumerate(reversed(sales[-100:])):
            self.table.setItem(row, 0, QTableWidgetItem(item['date']))
            self.table.setItem(row, 1, QTableWidgetItem(item['product_name']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item['units']}개"))
            
            amount = item['units'] * item['unit_price']
            self.table.setItem(row, 3, QTableWidgetItem(f"{amount:,.0f}원"))
            self.table.setItem(row, 4, QTableWidgetItem(item.get('notes', '')))
        
        if len(sales) == 0:
            self.table.setRowCount(1)
            no_data = QTableWidgetItem('판매 내역이 없습니다')
            no_data.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, 0, no_data)
            self.table.setSpan(0, 0, 1, 5)
