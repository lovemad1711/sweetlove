from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit, QComboBox, QHeaderView,
    QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ReportsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel('분석 보고서')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        layout.addWidget(title)
        
        control_group = QGroupBox('보고서 설정')
        control_layout = QFormLayout()
        control_group.setLayout(control_layout)
        
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItem('주간 보고서', 'weekly')
        self.report_type_combo.addItem('월간 보고서', 'monthly')
        self.report_type_combo.addItem('연간 보고서', 'yearly')
        control_layout.addRow('보고서 유형:', self.report_type_combo)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        control_layout.addRow('기준 날짜:', self.date_edit)
        
        generate_btn = QPushButton('보고서 생성')
        generate_btn.clicked.connect(self.generate_report)
        control_layout.addRow(generate_btn)
        
        layout.addWidget(control_group)
        
        self.summary_label = QLabel()
        self.summary_label.setStyleSheet(
            'padding: 15px; background-color: #f8f9fa; '
            'border-radius: 5px; font-size: 11pt;'
        )
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            '품목명', '예측 판매', '실제 판매', '차이(개)', '차이(금액)', '차이율'
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 6):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
    
    def generate_report(self):
        report_type = self.report_type_combo.currentData()
        date = self.date_edit.date().toString('yyyy-MM-dd')
        
        try:
            if report_type == 'weekly':
                self.generate_weekly_report(date)
            elif report_type == 'monthly':
                self.generate_monthly_report(date)
            elif report_type == 'yearly':
                self.generate_yearly_report(date)
        except Exception as e:
            self.main_window.show_error(f'보고서 생성 중 오류: {str(e)}')
    
    def generate_weekly_report(self, start_date):
        report = self.main_window.manager.get_weekly_report(start_date)
        
        summary_text = f"""
        <b>주간 보고서</b><br>
        기간: {report['start_date']} ~ {report['end_date']}<br><br>
        <b>예측 판매:</b> {report['total_predicted_sales']}개<br>
        <b>실제 판매:</b> {report['total_actual_sales']}개<br>
        <b>차이:</b> {report['total_discrepancy_units']}개 
        ({report['total_discrepancy_value']:,.0f}원)<br>
        """
        
        self.summary_label.setText(summary_text)
        
        products = report['products']
        self.table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product['product_name']))
            self.table.setItem(row, 1, QTableWidgetItem(f"{product['predicted_sales']}개"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{product['actual_sales']}개"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{product['discrepancy_units']}개"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{product['discrepancy_value']:,.0f}원"))
            
            rate = 0
            if product['predicted_sales'] > 0:
                rate = (product['discrepancy_units'] / product['predicted_sales']) * 100
            
            rate_item = QTableWidgetItem(f"{rate:.1f}%")
            
            if product['discrepancy_units'] > 0:
                rate_item.setBackground(Qt.red)
            elif product['discrepancy_units'] < 0:
                rate_item.setBackground(Qt.green)
            
            self.table.setItem(row, 5, rate_item)
    
    def generate_monthly_report(self, date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        report = self.main_window.manager.get_monthly_report(date_obj.year, date_obj.month)
        
        summary_text = f"""
        <b>월간 보고서</b><br>
        기간: {report['year']}년 {report['month']}월<br><br>
        <b>예측 판매:</b> {report['total_predicted_sales']}개<br>
        <b>실제 판매:</b> {report['total_actual_sales']}개<br>
        <b>차이:</b> {report['total_discrepancy_units']}개 
        ({report['total_discrepancy_value']:,.0f}원)<br>
        <b>주차 수:</b> {len(report['weeks'])}주<br>
        """
        
        self.summary_label.setText(summary_text)
        
        products = self.main_window.db.get_products(active_only=True)
        self.table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            total_predicted = 0
            total_actual = 0
            total_discrepancy = 0
            total_value = 0
            
            for week in report['weeks']:
                for p in week['products']:
                    if p['product_name'] == product['name']:
                        total_predicted += p['predicted_sales']
                        total_actual += p['actual_sales']
                        total_discrepancy += p['discrepancy_units']
                        total_value += p['discrepancy_value']
            
            self.table.setItem(row, 0, QTableWidgetItem(product['name']))
            self.table.setItem(row, 1, QTableWidgetItem(f"{total_predicted}개"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{total_actual}개"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{total_discrepancy}개"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{total_value:,.0f}원"))
            
            rate = 0
            if total_predicted > 0:
                rate = (total_discrepancy / total_predicted) * 100
            
            rate_item = QTableWidgetItem(f"{rate:.1f}%")
            
            if total_discrepancy > 0:
                rate_item.setBackground(Qt.red)
            elif total_discrepancy < 0:
                rate_item.setBackground(Qt.green)
            
            self.table.setItem(row, 5, rate_item)
    
    def generate_yearly_report(self, date_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        from analysis import InventoryAnalyzer
        analyzer = InventoryAnalyzer(self.main_window.manager)
        report = analyzer.generate_yearly_report(date_obj.year)
        
        summary_text = f"""
        <b>연간 보고서</b><br>
        기간: {report['year']}년<br><br>
        <b>예측 판매:</b> {report['total_predicted_sales']:,}개<br>
        <b>실제 판매:</b> {report['total_actual_sales']:,}개<br>
        <b>차이:</b> {report['total_discrepancy_units']:,}개 
        ({report['total_discrepancy_value']:,.0f}원)<br>
        """
        
        self.summary_label.setText(summary_text)
        
        self.main_window.show_success('연간 보고서가 생성되었습니다')
