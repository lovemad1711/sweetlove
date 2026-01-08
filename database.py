import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

class InventoryDatabase:
    def __init__(self, db_path='data/inventory.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                units_per_box INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                notes TEXT,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warehouse_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                boxes REAL DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outbound (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                boxes REAL DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        for i in range(1, 6):
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS showcase_{i} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    product_id INTEGER NOT NULL,
                    units INTEGER DEFAULT 0,
                    max_capacity INTEGER DEFAULT 0,
                    field_active INTEGER DEFAULT 1,
                    notes TEXT,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                units INTEGER DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS initial_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                warehouse_boxes REAL DEFAULT 0,
                showcase_1_units INTEGER DEFAULT 0,
                showcase_2_units INTEGER DEFAULT 0,
                showcase_3_units INTEGER DEFAULT 0,
                showcase_4_units INTEGER DEFAULT 0,
                showcase_5_units INTEGER DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS showcase_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                showcase_number INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                max_capacity INTEGER DEFAULT 0,
                field_active INTEGER DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES products(id),
                UNIQUE(showcase_number, product_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_product(self, name: str, units_per_box: int, unit_price: float, notes: str = '') -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO products (name, units_per_box, unit_price, notes)
                VALUES (?, ?, ?, ?)
            ''', (name, units_per_box, unit_price, notes))
            
            product_id = cursor.lastrowid
            
            for i in range(1, 6):
                cursor.execute(f'''
                    INSERT INTO showcase_config (showcase_number, product_id, max_capacity, field_active)
                    VALUES (?, ?, 0, 1)
                ''', (i, product_id))
            
            conn.commit()
            return product_id
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError(f"Product '{name}' already exists")
        finally:
            conn.close()
    
    def delete_product(self, product_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE products SET active = 0 WHERE id = ?', (product_id,))
        
        conn.commit()
        conn.close()
    
    def get_products(self, active_only: bool = True) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute('SELECT * FROM products WHERE active = 1 ORDER BY name')
        else:
            cursor.execute('SELECT * FROM products ORDER BY name')
        
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return products
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    def update_product(self, product_id: int, name: str, units_per_box: int, unit_price: float, notes: str = ''):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products 
            SET name = ?, units_per_box = ?, unit_price = ?, notes = ?
            WHERE id = ?
        ''', (name, units_per_box, unit_price, notes, product_id))
        
        conn.commit()
        conn.close()
    
    def add_warehouse_entry(self, date: str, product_id: int, boxes: float, notes: str = ''):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO warehouse_inventory (date, product_id, boxes, notes)
            VALUES (?, ?, ?, ?)
        ''', (date, product_id, boxes, notes))
        
        conn.commit()
        conn.close()
    
    def add_outbound_entry(self, date: str, product_id: int, boxes: float, notes: str = ''):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO outbound (date, product_id, boxes, notes)
            VALUES (?, ?, ?, ?)
        ''', (date, product_id, boxes, notes))
        
        conn.commit()
        conn.close()
    
    def add_showcase_entry(self, showcase_num: int, date: str, product_id: int, units: int, notes: str = ''):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            INSERT INTO showcase_{showcase_num} (date, product_id, units, notes)
            VALUES (?, ?, ?, ?)
        ''', (date, product_id, units, notes))
        
        conn.commit()
        conn.close()
    
    def add_sales_entry(self, date: str, product_id: int, units: int, notes: str = ''):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sales (date, product_id, units, notes)
            VALUES (?, ?, ?, ?)
        ''', (date, product_id, units, notes))
        
        conn.commit()
        conn.close()
    
    def set_initial_data(self, date: str, product_id: int, warehouse_boxes: float,
                        showcase_units: Dict[int, int], notes: str = ''):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO initial_data (date, product_id, warehouse_boxes,
                                     showcase_1_units, showcase_2_units, showcase_3_units,
                                     showcase_4_units, showcase_5_units, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, product_id, warehouse_boxes,
              showcase_units.get(1, 0), showcase_units.get(2, 0), showcase_units.get(3, 0),
              showcase_units.get(4, 0), showcase_units.get(5, 0), notes))
        
        conn.commit()
        conn.close()
    
    def get_showcase_config(self, showcase_num: int, product_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM showcase_config 
            WHERE showcase_number = ? AND product_id = ?
        ''', (showcase_num, product_id))
        
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_showcase_config(self, showcase_num: int, product_id: int, max_capacity: int, field_active: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE showcase_config 
            SET max_capacity = ?, field_active = ?
            WHERE showcase_number = ? AND product_id = ?
        ''', (max_capacity, field_active, showcase_num, product_id))
        
        if cursor.rowcount == 0:
            cursor.execute('''
                INSERT INTO showcase_config (showcase_number, product_id, max_capacity, field_active)
                VALUES (?, ?, ?, ?)
            ''', (showcase_num, product_id, max_capacity, field_active))
        
        conn.commit()
        conn.close()
    
    def get_all_showcase_configs(self) -> Dict[int, Dict[int, Dict]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM showcase_config ORDER BY showcase_number, product_id')
        rows = cursor.fetchall()
        
        configs = {}
        for row in rows:
            showcase_num = row['showcase_number']
            product_id = row['product_id']
            
            if showcase_num not in configs:
                configs[showcase_num] = {}
            
            configs[showcase_num][product_id] = dict(row)
        
        conn.close()
        return configs
    
    def get_warehouse_inventory(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT w.*, p.name as product_name, p.units_per_box
            FROM warehouse_inventory w
            JOIN products p ON w.product_id = p.id
            WHERE 1=1
        '''
        params = []
        
        if start_date:
            query += ' AND w.date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND w.date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY w.date, p.name'
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_outbound(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT o.*, p.name as product_name, p.units_per_box
            FROM outbound o
            JOIN products p ON o.product_id = p.id
            WHERE 1=1
        '''
        params = []
        
        if start_date:
            query += ' AND o.date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND o.date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY o.date, p.name'
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_sales(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT s.*, p.name as product_name, p.unit_price
            FROM sales s
            JOIN products p ON s.product_id = p.id
            WHERE 1=1
        '''
        params = []
        
        if start_date:
            query += ' AND s.date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND s.date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY s.date, p.name'
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_showcase_data(self, showcase_num: int, start_date: str = None, end_date: str = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = f'''
            SELECT s.*, p.name as product_name
            FROM showcase_{showcase_num} s
            JOIN products p ON s.product_id = p.id
            WHERE 1=1
        '''
        params = []
        
        if start_date:
            query += ' AND s.date >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND s.date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY s.date, p.name'
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_initial_data(self, date: str = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if date:
            cursor.execute('''
                SELECT i.*, p.name as product_name
                FROM initial_data i
                JOIN products p ON i.product_id = p.id
                WHERE i.date = ?
                ORDER BY p.name
            ''', (date,))
        else:
            cursor.execute('''
                SELECT i.*, p.name as product_name
                FROM initial_data i
                JOIN products p ON i.product_id = p.id
                ORDER BY i.date DESC, p.name
            ''')
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
