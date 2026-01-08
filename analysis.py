import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime, timedelta
from typing import Dict, List
import os

class InventoryAnalyzer:
    def __init__(self, inventory_manager):
        self.manager = inventory_manager
        
        font_path = None
        for font in fm.findSystemFonts():
            if 'NanumGothic' in font or 'NotoSans' in font or 'Malgun' in font:
                font_path = font
                break
        
        if font_path:
            plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
        
        plt.rcParams['axes.unicode_minus'] = False
    
    def generate_weekly_comparison_chart(self, start_date: str, output_path: str = 'static/charts'):
        os.makedirs(output_path, exist_ok=True)
        
        report = self.manager.get_weekly_report(start_date)
        products = report['products']
        
        product_names = [p['product_name'] for p in products]
        predicted = [p['predicted_sales'] for p in products]
        actual = [p['actual_sales'] for p in products]
        
        x = range(len(product_names))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars1 = ax.bar([i - width/2 for i in x], predicted, width, label='예측 판매')
        bars2 = ax.bar([i + width/2 for i in x], actual, width, label='실제 판매')
        
        ax.set_xlabel('품목')
        ax.set_ylabel('판매량 (개)')
        ax.set_title(f'주간 판매 비교 ({report["start_date"]} ~ {report["end_date"]})')
        ax.set_xticks(x)
        ax.set_xticklabels(product_names, rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        
        filename = f'weekly_comparison_{start_date}.png'
        filepath = os.path.join(output_path, filename)
        plt.savefig(filepath)
        plt.close()
        
        return filename
    
    def generate_discrepancy_chart(self, start_date: str, end_date: str, output_path: str = 'static/charts'):
        os.makedirs(output_path, exist_ok=True)
        
        discrepancies = self.manager.calculate_all_discrepancies(start_date, end_date)
        
        product_names = [d['product_name'] for d in discrepancies]
        discrepancy_units = [d['discrepancy_units'] for d in discrepancies]
        
        colors = ['red' if d > 0 else 'green' if d < 0 else 'gray' for d in discrepancy_units]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(product_names, discrepancy_units, color=colors)
        
        ax.set_xlabel('품목')
        ax.set_ylabel('차이 (개)')
        ax.set_title(f'판매 차이 분석 ({start_date} ~ {end_date})')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        filename = f'discrepancy_{start_date}_{end_date}.png'
        filepath = os.path.join(output_path, filename)
        plt.savefig(filepath)
        plt.close()
        
        return filename
    
    def generate_monthly_trend_chart(self, product_id: int, months: int = 6, output_path: str = 'static/charts'):
        os.makedirs(output_path, exist_ok=True)
        
        product = self.manager.db.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months)
        
        monthly_sales = []
        month_labels = []
        
        current = start_date
        while current <= end_date:
            month_start = current.replace(day=1)
            
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)
            
            month_end = min(month_end, end_date)
            
            sales = self.manager.calculate_actual_sales(
                product_id,
                month_start.strftime('%Y-%m-%d'),
                month_end.strftime('%Y-%m-%d')
            )
            
            monthly_sales.append(sales)
            month_labels.append(month_start.strftime('%Y-%m'))
            
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1, day=1)
            else:
                current = current.replace(month=current.month + 1, day=1)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(month_labels, monthly_sales, marker='o', linewidth=2)
        
        ax.set_xlabel('월')
        ax.set_ylabel('판매량 (개)')
        ax.set_title(f'{product["name"]} - 월별 판매 추이')
        plt.xticks(rotation=45, ha='right')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = f'monthly_trend_{product_id}.png'
        filepath = os.path.join(output_path, filename)
        plt.savefig(filepath)
        plt.close()
        
        return filename
    
    def generate_product_comparison_chart(self, start_date: str, end_date: str, output_path: str = 'static/charts'):
        os.makedirs(output_path, exist_ok=True)
        
        products = self.manager.db.get_products(active_only=True)
        
        product_names = []
        sales_data = []
        
        for product in products:
            sales = self.manager.calculate_actual_sales(product['id'], start_date, end_date)
            product_names.append(product['name'])
            sales_data.append(sales)
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        colors = plt.cm.Set3(range(len(product_names)))
        wedges, texts, autotexts = ax.pie(sales_data, labels=product_names, autopct='%1.1f%%',
                                           colors=colors, startangle=90)
        
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(10)
        
        ax.set_title(f'품목별 판매 비중 ({start_date} ~ {end_date})')
        
        plt.tight_layout()
        
        filename = f'product_comparison_{start_date}_{end_date}.png'
        filepath = os.path.join(output_path, filename)
        plt.savefig(filepath)
        plt.close()
        
        return filename
    
    def generate_yearly_report(self, year: int) -> Dict:
        start_date = f'{year}-01-01'
        end_date = f'{year}-12-31'
        
        monthly_reports = []
        for month in range(1, 13):
            report = self.manager.get_monthly_report(year, month)
            monthly_reports.append(report)
        
        total_predicted = sum(r['total_predicted_sales'] for r in monthly_reports)
        total_actual = sum(r['total_actual_sales'] for r in monthly_reports)
        total_discrepancy_units = sum(r['total_discrepancy_units'] for r in monthly_reports)
        total_discrepancy_value = sum(r['total_discrepancy_value'] for r in monthly_reports)
        
        return {
            'year': year,
            'total_predicted_sales': total_predicted,
            'total_actual_sales': total_actual,
            'total_discrepancy_units': total_discrepancy_units,
            'total_discrepancy_value': total_discrepancy_value,
            'months': monthly_reports
        }
    
    def generate_yearly_comparison_chart(self, year: int, output_path: str = 'static/charts'):
        os.makedirs(output_path, exist_ok=True)
        
        yearly_report = self.generate_yearly_report(year)
        months = yearly_report['months']
        
        month_labels = [f'{m["month"]}월' for m in months]
        predicted = [m['total_predicted_sales'] for m in months]
        actual = [m['total_actual_sales'] for m in months]
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        x = range(len(month_labels))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], predicted, width, label='예측 판매')
        bars2 = ax.bar([i + width/2 for i in x], actual, width, label='실제 판매')
        
        ax.set_xlabel('월')
        ax.set_ylabel('판매량 (개)')
        ax.set_title(f'{year}년 월별 판매 비교')
        ax.set_xticks(x)
        ax.set_xticklabels(month_labels)
        ax.legend()
        
        plt.tight_layout()
        
        filename = f'yearly_comparison_{year}.png'
        filepath = os.path.join(output_path, filename)
        plt.savefig(filepath)
        plt.close()
        
        return filename
