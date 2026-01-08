from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import InventoryDatabase
from inventory_manager import InventoryManager
from backup_manager import BackupManager
from analysis import InventoryAnalyzer
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

db = InventoryDatabase()
manager = InventoryManager()
backup_manager = BackupManager()
analyzer = InventoryAnalyzer(manager)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    products_list = db.get_products()
    return render_template('products.html', products=products_list)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        units_per_box = int(request.form.get('units_per_box'))
        unit_price = float(request.form.get('unit_price'))
        notes = request.form.get('notes', '')
        
        try:
            db.add_product(name, units_per_box, unit_price, notes)
            flash(f'품목 "{name}"이 추가되었습니다.', 'success')
            return redirect(url_for('products'))
        except ValueError as e:
            flash(str(e), 'error')
    
    return render_template('add_product.html')

@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = db.get_product_by_id(product_id)
    
    if not product:
        flash('품목을 찾을 수 없습니다.', 'error')
        return redirect(url_for('products'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        units_per_box = int(request.form.get('units_per_box'))
        unit_price = float(request.form.get('unit_price'))
        notes = request.form.get('notes', '')
        
        db.update_product(product_id, name, units_per_box, unit_price, notes)
        flash(f'품목 "{name}"이 수정되었습니다.', 'success')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = db.get_product_by_id(product_id)
    
    if product:
        db.delete_product(product_id)
        flash(f'품목 "{product["name"]}"이 삭제되었습니다.', 'success')
    else:
        flash('품목을 찾을 수 없습니다.', 'error')
    
    return redirect(url_for('products'))

@app.route('/initial-data', methods=['GET', 'POST'])
def initial_data():
    if request.method == 'POST':
        date = request.form.get('date')
        products_list = db.get_products()
        
        for product in products_list:
            warehouse_boxes = float(request.form.get(f'warehouse_{product["id"]}', 0))
            
            showcase_units = {}
            for i in range(1, 6):
                showcase_units[i] = int(request.form.get(f'showcase_{i}_{product["id"]}', 0))
            
            notes = request.form.get(f'notes_{product["id"]}', '')
            
            db.set_initial_data(date, product['id'], warehouse_boxes, showcase_units, notes)
        
        flash(f'{date} 날짜의 초기 데이터가 설정되었습니다.', 'success')
        return redirect(url_for('initial_data'))
    
    products_list = db.get_products()
    initial_data_list = db.get_initial_data()
    
    return render_template('initial_data.html', products=products_list, initial_data=initial_data_list)

@app.route('/showcase-config', methods=['GET', 'POST'])
def showcase_config():
    if request.method == 'POST':
        products_list = db.get_products()
        
        for showcase_num in range(1, 6):
            for product in products_list:
                max_capacity = int(request.form.get(f'max_{showcase_num}_{product["id"]}', 0))
                field_active = 1 if request.form.get(f'active_{showcase_num}_{product["id"]}') else 0
                
                db.update_showcase_config(showcase_num, product['id'], max_capacity, field_active)
        
        flash('쇼케이스 설정이 저장되었습니다.', 'success')
        return redirect(url_for('showcase_config'))
    
    products_list = db.get_products()
    configs = db.get_all_showcase_configs()
    
    return render_template('showcase_config.html', products=products_list, configs=configs)

@app.route('/warehouse', methods=['GET', 'POST'])
def warehouse():
    if request.method == 'POST':
        date = request.form.get('date')
        product_id = int(request.form.get('product_id'))
        boxes = float(request.form.get('boxes'))
        notes = request.form.get('notes', '')
        
        db.add_warehouse_entry(date, product_id, boxes, notes)
        flash('입고 데이터가 추가되었습니다.', 'success')
        return redirect(url_for('warehouse'))
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    inventory = db.get_warehouse_inventory(start_date, end_date)
    products_list = db.get_products()
    
    return render_template('warehouse.html', inventory=inventory, products=products_list)

@app.route('/outbound', methods=['GET', 'POST'])
def outbound():
    if request.method == 'POST':
        date = request.form.get('date')
        product_id = int(request.form.get('product_id'))
        boxes = float(request.form.get('boxes'))
        notes = request.form.get('notes', '')
        auto_distribute = request.form.get('auto_distribute')
        
        db.add_outbound_entry(date, product_id, boxes, notes)
        
        if auto_distribute:
            try:
                manager.distribute_outbound_to_showcases(date, product_id, boxes)
                flash('출고 데이터가 추가되고 쇼케이스에 자동 배분되었습니다.', 'success')
            except Exception as e:
                flash(f'출고 데이터가 추가되었으나 자동 배분 중 오류가 발생했습니다: {str(e)}', 'warning')
        else:
            flash('출고 데이터가 추가되었습니다.', 'success')
        
        return redirect(url_for('outbound'))
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    outbound_data = db.get_outbound(start_date, end_date)
    products_list = db.get_products()
    
    return render_template('outbound.html', outbound=outbound_data, products=products_list)

@app.route('/showcases/<int:showcase_num>', methods=['GET', 'POST'])
def showcase(showcase_num):
    if showcase_num < 1 or showcase_num > 5:
        flash('유효하지 않은 쇼케이스 번호입니다.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        date = request.form.get('date')
        product_id = int(request.form.get('product_id'))
        units = int(request.form.get('units'))
        notes = request.form.get('notes', '')
        
        db.add_showcase_entry(showcase_num, date, product_id, units, notes)
        flash(f'쇼케이스 {showcase_num} 데이터가 추가되었습니다.', 'success')
        return redirect(url_for('showcase', showcase_num=showcase_num))
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    showcase_data = db.get_showcase_data(showcase_num, start_date, end_date)
    products_list = db.get_products()
    
    return render_template('showcase.html', showcase_num=showcase_num, 
                          showcase_data=showcase_data, products=products_list)

@app.route('/showcase-move', methods=['GET', 'POST'])
def showcase_move():
    if request.method == 'POST':
        date = request.form.get('date')
        from_showcase = int(request.form.get('from_showcase'))
        to_showcase = int(request.form.get('to_showcase'))
        product_id = int(request.form.get('product_id'))
        units = int(request.form.get('units'))
        
        try:
            manager.move_showcase_inventory(date, from_showcase, to_showcase, product_id, units)
            flash(f'쇼케이스 {from_showcase}에서 쇼케이스 {to_showcase}로 {units}개가 이동되었습니다.', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        
        return redirect(url_for('showcase_move'))
    
    products_list = db.get_products()
    return render_template('showcase_move.html', products=products_list)

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        date = request.form.get('date')
        product_id = int(request.form.get('product_id'))
        units = int(request.form.get('units'))
        notes = request.form.get('notes', '')
        
        db.add_sales_entry(date, product_id, units, notes)
        flash('판매 데이터가 추가되었습니다.', 'success')
        return redirect(url_for('sales'))
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    sales_data = db.get_sales(start_date, end_date)
    products_list = db.get_products()
    
    return render_template('sales.html', sales=sales_data, products=products_list)

@app.route('/inventory-summary')
def inventory_summary():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    summary = manager.get_inventory_summary(date)
    
    return render_template('inventory_summary.html', summary=summary, date=date)

@app.route('/reports/weekly')
def weekly_report():
    start_date = request.args.get('start_date')
    
    if not start_date:
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        start_date = monday.strftime('%Y-%m-%d')
    
    report = manager.get_weekly_report(start_date)
    
    try:
        chart_filename = analyzer.generate_weekly_comparison_chart(start_date)
        discrepancy_chart = analyzer.generate_discrepancy_chart(
            report['start_date'], 
            report['end_date']
        )
    except Exception as e:
        chart_filename = None
        discrepancy_chart = None
        flash(f'차트 생성 중 오류가 발생했습니다: {str(e)}', 'warning')
    
    return render_template('weekly_report.html', report=report, 
                          chart_filename=chart_filename,
                          discrepancy_chart=discrepancy_chart)

@app.route('/reports/monthly')
def monthly_report():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    if not year or not month:
        today = datetime.now()
        year = today.year
        month = today.month
    
    report = manager.get_monthly_report(year, month)
    
    return render_template('monthly_report.html', report=report)

@app.route('/reports/yearly')
def yearly_report():
    year = request.args.get('year', type=int, default=datetime.now().year)
    
    report = analyzer.generate_yearly_report(year)
    
    try:
        chart_filename = analyzer.generate_yearly_comparison_chart(year)
    except Exception as e:
        chart_filename = None
        flash(f'차트 생성 중 오류가 발생했습니다: {str(e)}', 'warning')
    
    return render_template('yearly_report.html', report=report, chart_filename=chart_filename)

@app.route('/reports/product-trend/<int:product_id>')
def product_trend(product_id):
    months = request.args.get('months', type=int, default=6)
    
    product = db.get_product_by_id(product_id)
    
    if not product:
        flash('품목을 찾을 수 없습니다.', 'error')
        return redirect(url_for('products'))
    
    try:
        chart_filename = analyzer.generate_monthly_trend_chart(product_id, months)
    except Exception as e:
        chart_filename = None
        flash(f'차트 생성 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return render_template('product_trend.html', product=product, 
                          chart_filename=chart_filename, months=months)

@app.route('/backups')
def backups():
    backups_list = backup_manager.list_backups()
    return render_template('backups.html', backups=backups_list)

@app.route('/backups/create', methods=['POST'])
def create_backup():
    notes = request.form.get('notes', '')
    
    try:
        backup_path = backup_manager.create_backup(notes)
        flash(f'백업이 생성되었습니다: {os.path.basename(backup_path)}', 'success')
    except Exception as e:
        flash(f'백업 생성 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('backups'))

@app.route('/backups/restore/<filename>', methods=['POST'])
def restore_backup(filename):
    try:
        backup_manager.restore_backup(filename)
        flash(f'백업이 복원되었습니다: {filename}', 'success')
    except Exception as e:
        flash(f'백업 복원 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('backups'))

@app.route('/backups/archive/<filename>', methods=['POST'])
def archive_backup(filename):
    try:
        archive_path = backup_manager.archive_backup(filename)
        flash(f'백업이 영구 보관되었습니다: {os.path.basename(archive_path)}', 'success')
    except Exception as e:
        flash(f'백업 보관 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('backups'))

if __name__ == '__main__':
    os.makedirs('static/charts', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
