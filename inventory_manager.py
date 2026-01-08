from database import InventoryDatabase
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class InventoryManager:
    def __init__(self, db_path='data/inventory.db'):
        self.db = InventoryDatabase(db_path)
    
    def calculate_current_warehouse_inventory(self, product_id: int, end_date: str = None) -> float:
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        initial_data = self.db.get_initial_data()
        initial_boxes = 0
        initial_date = None
        
        for entry in initial_data:
            if entry['product_id'] == product_id:
                initial_boxes = entry['warehouse_boxes']
                initial_date = entry['date']
                break
        
        start_date = initial_date if initial_date else '1900-01-01'
        
        inbound = self.db.get_warehouse_inventory(start_date, end_date)
        outbound = self.db.get_outbound(start_date, end_date)
        
        total_inbound = sum(entry['boxes'] for entry in inbound if entry['product_id'] == product_id)
        total_outbound = sum(entry['boxes'] for entry in outbound if entry['product_id'] == product_id)
        
        current_inventory = initial_boxes + total_inbound - total_outbound
        return current_inventory
    
    def calculate_current_showcase_inventory(self, showcase_num: int, product_id: int, end_date: str = None) -> int:
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        initial_data = self.db.get_initial_data()
        initial_units = 0
        initial_date = None
        
        for entry in initial_data:
            if entry['product_id'] == product_id:
                initial_units = entry[f'showcase_{showcase_num}_units']
                initial_date = entry['date']
                break
        
        start_date = initial_date if initial_date else '1900-01-01'
        
        showcase_data = self.db.get_showcase_data(showcase_num, start_date, end_date)
        
        total_units = sum(entry['units'] for entry in showcase_data if entry['product_id'] == product_id)
        
        current_inventory = initial_units + total_units
        return current_inventory
    
    def calculate_predicted_sales(self, product_id: int, start_date: str, end_date: str) -> int:
        product = self.db.get_product_by_id(product_id)
        if not product:
            return 0
        
        units_per_box = product['units_per_box']
        
        outbound = self.db.get_outbound(start_date, end_date)
        total_outbound_boxes = sum(entry['boxes'] for entry in outbound if entry['product_id'] == product_id)
        
        predicted_units = total_outbound_boxes * units_per_box
        
        initial_data = self.db.get_initial_data()
        start_showcase_units = 0
        
        for entry in initial_data:
            if entry['product_id'] == product_id and entry['date'] < start_date:
                for i in range(1, 6):
                    start_showcase_units += entry[f'showcase_{i}_units']
        
        end_showcase_units = 0
        for i in range(1, 6):
            end_showcase_units += self.calculate_current_showcase_inventory(i, product_id, end_date)
        
        predicted_sales = start_showcase_units + predicted_units - end_showcase_units
        
        return predicted_sales
    
    def calculate_actual_sales(self, product_id: int, start_date: str, end_date: str) -> int:
        sales = self.db.get_sales(start_date, end_date)
        total_sales = sum(entry['units'] for entry in sales if entry['product_id'] == product_id)
        return total_sales
    
    def calculate_discrepancy(self, product_id: int, start_date: str, end_date: str) -> Dict:
        predicted = self.calculate_predicted_sales(product_id, start_date, end_date)
        actual = self.calculate_actual_sales(product_id, start_date, end_date)
        discrepancy = predicted - actual
        
        product = self.db.get_product_by_id(product_id)
        discrepancy_value = discrepancy * product['unit_price'] if product else 0
        
        return {
            'product_id': product_id,
            'product_name': product['name'] if product else 'Unknown',
            'predicted_sales': predicted,
            'actual_sales': actual,
            'discrepancy_units': discrepancy,
            'discrepancy_value': discrepancy_value
        }
    
    def calculate_all_discrepancies(self, start_date: str, end_date: str) -> List[Dict]:
        products = self.db.get_products(active_only=True)
        discrepancies = []
        
        for product in products:
            discrepancy = self.calculate_discrepancy(product['id'], start_date, end_date)
            discrepancies.append(discrepancy)
        
        return discrepancies
    
    def distribute_outbound_to_showcases(self, date: str, product_id: int, boxes: float):
        product = self.db.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        total_units = boxes * product['units_per_box']
        
        configs = self.db.get_all_showcase_configs()
        
        remaining_units = total_units
        
        for showcase_num in range(1, 6):
            if remaining_units <= 0:
                break
            
            if showcase_num not in configs or product_id not in configs[showcase_num]:
                continue
            
            config = configs[showcase_num][product_id]
            
            if config['field_active'] != 1:
                continue
            
            max_capacity = config['max_capacity']
            current_inventory = self.calculate_current_showcase_inventory(showcase_num, product_id, date)
            
            available_space = max_capacity - current_inventory
            
            if available_space > 0:
                units_to_add = min(remaining_units, available_space)
                self.db.add_showcase_entry(showcase_num, date, product_id, units_to_add)
                remaining_units -= units_to_add
        
        if remaining_units > 0:
            print(f"Warning: {remaining_units} units could not be distributed to showcases")
    
    def move_showcase_inventory(self, date: str, from_showcase: int, to_showcase: int, 
                                product_id: int, units: int):
        current_from = self.calculate_current_showcase_inventory(from_showcase, product_id, date)
        
        if current_from < units:
            raise ValueError(f"Insufficient inventory in showcase {from_showcase}")
        
        self.db.add_showcase_entry(from_showcase, date, product_id, -units)
        self.db.add_showcase_entry(to_showcase, date, product_id, units)
    
    def get_inventory_summary(self, date: str = None) -> Dict:
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        products = self.db.get_products(active_only=True)
        summary = []
        
        for product in products:
            warehouse = self.calculate_current_warehouse_inventory(product['id'], date)
            showcases = {}
            total_showcase_units = 0
            
            for i in range(1, 6):
                units = self.calculate_current_showcase_inventory(i, product['id'], date)
                showcases[f'showcase_{i}'] = units
                total_showcase_units += units
            
            summary.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'warehouse_boxes': warehouse,
                'warehouse_units': warehouse * product['units_per_box'],
                **showcases,
                'total_showcase_units': total_showcase_units
            })
        
        return summary
    
    def get_weekly_report(self, start_date: str) -> Dict:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = start + timedelta(days=6)
        end_date = end.strftime('%Y-%m-%d')
        
        discrepancies = self.calculate_all_discrepancies(start_date, end_date)
        
        total_predicted = sum(d['predicted_sales'] for d in discrepancies)
        total_actual = sum(d['actual_sales'] for d in discrepancies)
        total_discrepancy_units = sum(d['discrepancy_units'] for d in discrepancies)
        total_discrepancy_value = sum(d['discrepancy_value'] for d in discrepancies)
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'total_predicted_sales': total_predicted,
            'total_actual_sales': total_actual,
            'total_discrepancy_units': total_discrepancy_units,
            'total_discrepancy_value': total_discrepancy_value,
            'products': discrepancies
        }
    
    def get_monthly_report(self, year: int, month: int) -> Dict:
        start = datetime(year, month, 1)
        
        if month == 12:
            end = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end = datetime(year, month + 1, 1) - timedelta(days=1)
        
        start_date = start.strftime('%Y-%m-%d')
        end_date = end.strftime('%Y-%m-%d')
        
        weekly_reports = []
        current = start
        week_num = 1
        
        while current <= end:
            week_start = current
            week_end = min(current + timedelta(days=6), end)
            
            week_report = self.get_weekly_report(week_start.strftime('%Y-%m-%d'))
            week_report['week_number'] = week_num
            weekly_reports.append(week_report)
            
            current = week_end + timedelta(days=1)
            week_num += 1
        
        total_predicted = sum(w['total_predicted_sales'] for w in weekly_reports)
        total_actual = sum(w['total_actual_sales'] for w in weekly_reports)
        total_discrepancy_units = sum(w['total_discrepancy_units'] for w in weekly_reports)
        total_discrepancy_value = sum(w['total_discrepancy_value'] for w in weekly_reports)
        
        return {
            'year': year,
            'month': month,
            'start_date': start_date,
            'end_date': end_date,
            'total_predicted_sales': total_predicted,
            'total_actual_sales': total_actual,
            'total_discrepancy_units': total_discrepancy_units,
            'total_discrepancy_value': total_discrepancy_value,
            'weeks': weekly_reports
        }
