import os
import shutil
from datetime import datetime
from database import InventoryDatabase

class BackupManager:
    def __init__(self, db_path='data/inventory.db', backup_dir='backups'):
        self.db_path = db_path
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, notes: str = '') -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'inventory_backup_{timestamp}.db'
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        
        shutil.copy2(self.db_path, backup_path)
        
        metadata_file = os.path.join(self.backup_dir, f'backup_metadata_{timestamp}.txt')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(f"Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Original Database: {self.db_path}\n")
            f.write(f"Backup File: {backup_filename}\n")
            f.write(f"Notes: {notes}\n")
        
        return backup_path
    
    def list_backups(self):
        if not os.path.exists(self.backup_dir):
            return []
        
        backups = []
        for filename in os.listdir(self.backup_dir):
            if filename.startswith('inventory_backup_') and filename.endswith('.db'):
                filepath = os.path.join(self.backup_dir, filename)
                stat = os.stat(filepath)
                
                timestamp_str = filename.replace('inventory_backup_', '').replace('.db', '')
                backup_date = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                
                metadata_file = os.path.join(self.backup_dir, f'backup_metadata_{timestamp_str}.txt')
                notes = ''
                if os.path.exists(metadata_file):
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'Notes:' in content:
                            notes = content.split('Notes:')[1].strip()
                
                backups.append({
                    'filename': filename,
                    'filepath': filepath,
                    'date': backup_date,
                    'size': stat.st_size,
                    'notes': notes
                })
        
        backups.sort(key=lambda x: x['date'], reverse=True)
        return backups
    
    def restore_backup(self, backup_filename: str):
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        if os.path.exists(self.db_path):
            temp_backup = f"{self.db_path}.temp_backup"
            shutil.copy2(self.db_path, temp_backup)
        
        try:
            shutil.copy2(backup_path, self.db_path)
        except Exception as e:
            if os.path.exists(temp_backup):
                shutil.copy2(temp_backup, self.db_path)
            raise e
        finally:
            if os.path.exists(temp_backup):
                os.remove(temp_backup)
    
    def delete_old_backups(self, days_to_keep: int = 1825):
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        deleted_count = 0
        for backup in self.list_backups():
            if backup['date'].timestamp() < cutoff_date:
                os.remove(backup['filepath'])
                
                timestamp_str = backup['filename'].replace('inventory_backup_', '').replace('.db', '')
                metadata_file = os.path.join(self.backup_dir, f'backup_metadata_{timestamp_str}.txt')
                if os.path.exists(metadata_file):
                    os.remove(metadata_file)
                
                deleted_count += 1
        
        return deleted_count
    
    def archive_backup(self, backup_filename: str, archive_dir: str = 'archives'):
        os.makedirs(archive_dir, exist_ok=True)
        
        backup_path = os.path.join(self.backup_dir, backup_filename)
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        archive_path = os.path.join(archive_dir, backup_filename)
        shutil.move(backup_path, archive_path)
        
        timestamp_str = backup_filename.replace('inventory_backup_', '').replace('.db', '')
        metadata_file = os.path.join(self.backup_dir, f'backup_metadata_{timestamp_str}.txt')
        if os.path.exists(metadata_file):
            archive_metadata = os.path.join(archive_dir, f'backup_metadata_{timestamp_str}.txt')
            shutil.move(metadata_file, archive_metadata)
        
        return archive_path
