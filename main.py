#!/usr/bin/env python3
"""
술음료 재고관리 시스템 - PyQt5 메인 애플리케이션
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QMessageBox, QStatusBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from ui.products_tab import ProductsTab
from ui.initial_data_tab import InitialDataTab
from ui.showcase_config_tab import ShowcaseConfigTab
from ui.warehouse_tab import WarehouseTab
from ui.outbound_tab import OutboundTab
from ui.showcase_tab import ShowcaseTab
from ui.sales_tab import SalesTab
from ui.inventory_summary_tab import InventorySummaryTab
from ui.reports_tab import ReportsTab
from ui.backups_tab import BackupsTab

from database import InventoryDatabase
from inventory_manager import InventoryManager
from backup_manager import BackupManager


class InventoryMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.db = InventoryDatabase()
        self.manager = InventoryManager()
        self.backup_manager = BackupManager()
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('술음료 재고관리 시스템')
        self.setGeometry(100, 100, 1400, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        title_label = QLabel('술음료 재고관리 시스템')
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('color: #2c3e50; padding: 10px;')
        layout.addWidget(title_label)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setMovable(False)
        
        self.tab_widget.addTab(self.create_home_tab(), '홈')
        self.tab_widget.addTab(ProductsTab(self), '품목관리')
        self.tab_widget.addTab(InitialDataTab(self), '초기데이터')
        self.tab_widget.addTab(ShowcaseConfigTab(self), '쇼케이스설정')
        self.tab_widget.addTab(WarehouseTab(self), '입고관리')
        self.tab_widget.addTab(OutboundTab(self), '출고관리')
        self.tab_widget.addTab(ShowcaseTab(self), '쇼케이스')
        self.tab_widget.addTab(SalesTab(self), '판매관리')
        self.tab_widget.addTab(InventorySummaryTab(self), '재고현황')
        self.tab_widget.addTab(ReportsTab(self), '분석보고서')
        self.tab_widget.addTab(BackupsTab(self), '백업관리')
        
        layout.addWidget(self.tab_widget)
        
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage('준비')
        
        self.apply_styles()
    
    def create_home_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        welcome_label = QLabel('술음료 재고관리 시스템에 오신 것을 환영합니다')
        welcome_font = QFont()
        welcome_font.setPointSize(14)
        welcome_label.setFont(welcome_font)
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        layout.addSpacing(20)
        
        info_label = QLabel(
            '이 시스템은 술과 음료의 재고를 효율적으로 관리합니다.\n\n'
            '주요 기능:\n'
            '• 품목 관리: 제품 정보 등록 및 관리\n'
            '• 재고 관리: 입고, 출고, 쇼케이스 관리\n'
            '• 판매 관리: 실제 판매 데이터 기록\n'
            '• 분석 보고서: 주간/월간/연간 분석\n'
            '• 백업: 데이터 안전 보관\n\n'
            '시작하기:\n'
            '1. 품목관리 탭에서 제품을 등록하세요\n'
            '2. 쇼케이스설정 탭에서 용량을 설정하세요\n'
            '3. 초기데이터 탭에서 현재 재고를 입력하세요\n'
            '4. 매일 입고, 출고, 판매 데이터를 입력하세요'
        )
        info_label.setAlignment(Qt.AlignLeft)
        info_label.setWordWrap(True)
        info_label.setStyleSheet('padding: 20px; background-color: #f8f9fa; border-radius: 5px;')
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        
        quick_buttons = [
            ('품목 추가', lambda: self.tab_widget.setCurrentIndex(1)),
            ('입고 등록', lambda: self.tab_widget.setCurrentIndex(4)),
            ('재고 확인', lambda: self.tab_widget.setCurrentIndex(8)),
            ('보고서 보기', lambda: self.tab_widget.setCurrentIndex(9)),
        ]
        
        for text, func in quick_buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(40)
            btn.clicked.connect(func)
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)
        
        return widget
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #333;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #5dade2;
                color: white;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #e0e0e0;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
                border: 2px solid #3498db;
            }
            QLabel {
                color: #2c3e50;
            }
        """)
    
    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
    
    def show_success(self, message):
        self.show_message('성공', message, QMessageBox.Information)
    
    def show_error(self, message):
        self.show_message('오류', message, QMessageBox.Critical)
    
    def show_warning(self, message):
        self.show_message('경고', message, QMessageBox.Warning)
    
    def confirm(self, message):
        reply = QMessageBox.question(
            self, '확인', message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes


def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    window = InventoryMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
