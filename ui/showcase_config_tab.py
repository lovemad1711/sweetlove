from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QSpinBox, QCheckBox, QGroupBox
)
from PyQt5.QtCore import Qt


class ShowcaseConfigTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        header_layout = QHBoxLayout()
        
        title = QLabel('쇼케이스 설정')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        save_btn = QPushButton('설정 저장')
        save_btn.clicked.connect(self.save_config)
        header_layout.addWidget(save_btn)
        
        load_btn = QPushButton('설정 불러오기')
        load_btn.setStyleSheet('background-color: #95a5a6;')
        load_btn.clicked.connect(self.load_config)
        header_layout.addWidget(load_btn)
        
        layout.addLayout(header_layout)
        
        info_label = QLabel(
            '각 쇼케이스의 품목별 최대 용량과 사용 여부를 설정합니다.'
        )
        info_label.setStyleSheet('padding: 10px; background-color: #e3f2fd; border-radius: 5px;')
        layout.addWidget(info_label)
        
        self.tables = {}
        
        for showcase_num in range(1, 6):
            group = QGroupBox(f'쇼케이스 {showcase_num}')
            group_layout = QVBoxLayout()
            group.setLayout(group_layout)
            
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(['품목명', '최대 용량 (개)', '사용', 'ID'])
            
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            
            table.setColumnHidden(3, True)
            table.setMaximumHeight(200)
            
            group_layout.addWidget(table)
            layout.addWidget(group)
            
            self.tables[showcase_num] = table
        
        self.load_config()
    
    def load_config(self):
        products = self.main_window.db.get_products(active_only=True)
        configs = self.main_window.db.get_all_showcase_configs()
        
        for showcase_num, table in self.tables.items():
            table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                table.setItem(row, 0, QTableWidgetItem(product['name']))
                
                capacity_spin = QSpinBox()
                capacity_spin.setMinimum(0)
                capacity_spin.setMaximum(10000)
                
                checkbox = QCheckBox()
                checkbox.setStyleSheet('margin-left: 20px;')
                
                if showcase_num in configs and product['id'] in configs[showcase_num]:
                    config = configs[showcase_num][product['id']]
                    capacity_spin.setValue(config['max_capacity'])
                    checkbox.setChecked(config['field_active'] == 1)
                else:
                    capacity_spin.setValue(50 if showcase_num == 1 else 30)
                    checkbox.setChecked(True)
                
                table.setCellWidget(row, 1, capacity_spin)
                table.setCellWidget(row, 2, checkbox)
                table.setItem(row, 3, QTableWidgetItem(str(product['id'])))
    
    def save_config(self):
        try:
            for showcase_num, table in self.tables.items():
                for row in range(table.rowCount()):
                    product_id_item = table.item(row, 3)
                    if not product_id_item:
                        continue
                    
                    product_id = int(product_id_item.text())
                    
                    capacity_widget = table.cellWidget(row, 1)
                    max_capacity = capacity_widget.value() if capacity_widget else 0
                    
                    checkbox_widget = table.cellWidget(row, 2)
                    field_active = 1 if (checkbox_widget and checkbox_widget.isChecked()) else 0
                    
                    self.main_window.db.update_showcase_config(
                        showcase_num, product_id, max_capacity, field_active
                    )
            
            self.main_window.show_success('쇼케이스 설정이 저장되었습니다')
            
        except Exception as e:
            self.main_window.show_error(f'저장 중 오류: {str(e)}')
