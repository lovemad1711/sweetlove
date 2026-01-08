from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QDialog, QLabel, QLineEdit, QTextEdit,
    QFormLayout, QDoubleSpinBox, QSpinBox, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush
from .ui_helpers import create_table_item, get_standard_font, set_row_heights


class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.product = product
        self.init_ui()
        
        if product:
            self.load_product()
    
    def init_ui(self):
        self.setWindowTitle('품목 추가' if not self.product else '품목 수정')
        self.setMinimumWidth(500)
        self.setMinimumHeight(350)
        
        layout = QFormLayout()
        self.setLayout(layout)
        
        # 폰트 설정
        font = QFont()
        font.setPointSize(10)
        
        self.name_edit = QLineEdit()
        self.name_edit.setFont(font)
        self.name_edit.setMinimumHeight(30)
        layout.addRow('품목명 *:', self.name_edit)
        
        self.units_per_box_spin = QSpinBox()
        self.units_per_box_spin.setFont(font)
        self.units_per_box_spin.setMinimumHeight(30)
        self.units_per_box_spin.setMinimum(1)
        self.units_per_box_spin.setMaximum(1000)
        self.units_per_box_spin.setValue(20)
        layout.addRow('박스당 수량 *:', self.units_per_box_spin)
        
        self.unit_price_spin = QDoubleSpinBox()
        self.unit_price_spin.setFont(font)
        self.unit_price_spin.setMinimumHeight(30)
        self.unit_price_spin.setMinimum(0)
        self.unit_price_spin.setMaximum(1000000)
        self.unit_price_spin.setValue(1000)
        self.unit_price_spin.setSuffix(' 원')
        layout.addRow('개별 판매 단가 *:', self.unit_price_spin)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setFont(font)
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setMinimumHeight(80)
        layout.addRow('비고:', self.notes_edit)
        
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton('저장' if not self.product else '수정')
        save_btn.setFont(font)
        save_btn.setMinimumHeight(35)
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton('취소')
        cancel_btn.setFont(font)
        cancel_btn.setMinimumHeight(35)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet('background-color: #95a5a6;')
        button_layout.addWidget(cancel_btn)
        
        layout.addRow(button_layout)
    
    def load_product(self):
        self.name_edit.setText(self.product['name'])
        self.units_per_box_spin.setValue(self.product['units_per_box'])
        self.unit_price_spin.setValue(self.product['unit_price'])
        self.notes_edit.setPlainText(self.product.get('notes', ''))
    
    def get_data(self):
        return {
            'name': self.name_edit.text().strip(),
            'units_per_box': self.units_per_box_spin.value(),
            'unit_price': self.unit_price_spin.value(),
            'notes': self.notes_edit.toPlainText().strip()
        }


class ProductsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        self.load_products()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        header_layout = QHBoxLayout()
        
        title = QLabel('품목 관리')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_btn = QPushButton('품목 추가')
        add_btn.clicked.connect(self.add_product)
        header_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton('새로고침')
        refresh_btn.clicked.connect(self.load_products)
        refresh_btn.setStyleSheet('background-color: #95a5a6;')
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            '품목명', '박스당 수량', '단가', '비고', '수정', '삭제'
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.table)
    
    def load_products(self):
        products = self.main_window.db.get_products(active_only=True)
        
        self.table.setRowCount(len(products))
        font = get_standard_font(10)
        
        for row, product in enumerate(products):
            # 품목명
            self.table.setItem(row, 0, create_table_item(product['name']))
            
            # 박스당 수량
            self.table.setItem(row, 1, create_table_item(f"{product['units_per_box']}개"))
            
            # 단가
            self.table.setItem(row, 2, create_table_item(f"{product['unit_price']:,.0f}원"))
            
            # 비고
            self.table.setItem(row, 3, create_table_item(product.get('notes', '')))
            
            # 수정 버튼
            edit_btn = QPushButton('수정')
            edit_btn.setFont(font)
            edit_btn.setMinimumHeight(35)
            edit_btn.setMinimumWidth(70)
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
            self.table.setCellWidget(row, 4, edit_btn)
            
            # 삭제 버튼
            delete_btn = QPushButton('삭제')
            delete_btn.setFont(font)
            delete_btn.setMinimumHeight(35)
            delete_btn.setMinimumWidth(70)
            delete_btn.setStyleSheet('background-color: #e74c3c; color: white; font-weight: bold; font-size: 10pt;')
            delete_btn.clicked.connect(lambda checked, p=product: self.delete_product(p))
            self.table.setCellWidget(row, 5, delete_btn)
        
        # 행 높이 설정
        set_row_heights(self.table, 45)
        
        if len(products) == 0:
            self.table.setRowCount(1)
            no_data_item = create_table_item('등록된 품목이 없습니다', font_size=11, align_center=True)
            no_data_item.setForeground(QBrush(QColor(120, 120, 120)))
            self.table.setItem(0, 0, no_data_item)
            self.table.setSpan(0, 0, 1, 6)
            self.table.setRowHeight(0, 60)
    
    def add_product(self):
        dialog = ProductDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            if not data['name']:
                self.main_window.show_error('품목명을 입력하세요')
                return
            
            try:
                self.main_window.db.add_product(
                    data['name'],
                    data['units_per_box'],
                    data['unit_price'],
                    data['notes']
                )
                self.main_window.show_success(f'품목 "{data["name"]}"이 추가되었습니다')
                self.load_products()
            except ValueError as e:
                self.main_window.show_error(str(e))
    
    def edit_product(self, product):
        dialog = ProductDialog(self, product)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            
            if not data['name']:
                self.main_window.show_error('품목명을 입력하세요')
                return
            
            try:
                self.main_window.db.update_product(
                    product['id'],
                    data['name'],
                    data['units_per_box'],
                    data['unit_price'],
                    data['notes']
                )
                self.main_window.show_success(f'품목 "{data["name"]}"이 수정되었습니다')
                self.load_products()
            except Exception as e:
                self.main_window.show_error(f'수정 중 오류: {str(e)}')
    
    def delete_product(self, product):
        if self.main_window.confirm(f'품목 "{product["name"]}"을 삭제하시겠습니까?'):
            try:
                self.main_window.db.delete_product(product['id'])
                self.main_window.show_success(f'품목 "{product["name"]}"이 삭제되었습니다')
                self.load_products()
            except Exception as e:
                self.main_window.show_error(f'삭제 중 오류: {str(e)}')
