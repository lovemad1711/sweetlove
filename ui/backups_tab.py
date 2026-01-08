from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QLineEdit, QHeaderView, QGroupBox,
    QFormLayout, QTextEdit
)
from PyQt5.QtCore import Qt


class BackupsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel('백업 관리')
        title.setStyleSheet('font-size: 16pt; font-weight: bold; color: #2c3e50;')
        layout.addWidget(title)
        
        info_label = QLabel(
            '데이터를 정기적으로 백업하여 안전하게 보관합니다. '
            '백업 파일은 5년간 보관되며, 이후 영구 보관함으로 이동됩니다.'
        )
        info_label.setStyleSheet('padding: 10px; background-color: #e3f2fd; border-radius: 5px;')
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        backup_group = QGroupBox('새 백업 생성')
        backup_layout = QFormLayout()
        backup_group.setLayout(backup_layout)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        self.notes_edit.setPlaceholderText('백업 사유나 특이사항을 입력하세요')
        backup_layout.addRow('백업 메모:', self.notes_edit)
        
        create_btn = QPushButton('백업 생성')
        create_btn.clicked.connect(self.create_backup)
        backup_layout.addRow(create_btn)
        
        layout.addWidget(backup_group)
        
        list_layout = QHBoxLayout()
        
        list_label = QLabel('백업 목록')
        list_label.setStyleSheet('font-size: 14pt; font-weight: bold;')
        list_layout.addWidget(list_label)
        
        list_layout.addStretch()
        
        refresh_btn = QPushButton('새로고침')
        refresh_btn.clicked.connect(self.load_backups)
        list_layout.addWidget(refresh_btn)
        
        layout.addLayout(list_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            '백업 파일명', '생성일시', '파일 크기', '메모', '관리'
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)
        
        self.load_backups()
    
    def create_backup(self):
        notes = self.notes_edit.toPlainText().strip()
        
        if self.main_window.confirm('백업을 생성하시겠습니까?'):
            try:
                backup_path = self.main_window.backup_manager.create_backup(notes)
                self.main_window.show_success(f'백업이 생성되었습니다:\n{backup_path}')
                self.notes_edit.clear()
                self.load_backups()
            except Exception as e:
                self.main_window.show_error(f'백업 생성 중 오류: {str(e)}')
    
    def load_backups(self):
        try:
            backups = self.main_window.backup_manager.list_backups()
            
            self.table.setRowCount(len(backups))
            
            for row, backup in enumerate(backups):
                self.table.setItem(row, 0, QTableWidgetItem(backup['filename']))
                self.table.setItem(row, 1, QTableWidgetItem(
                    backup['date'].strftime('%Y-%m-%d %H:%M:%S')
                ))
                self.table.setItem(row, 2, QTableWidgetItem(
                    f"{backup['size'] / 1024:.2f} KB"
                ))
                self.table.setItem(row, 3, QTableWidgetItem(backup.get('notes', '')))
                
                button_widget = QWidget()
                button_layout = QHBoxLayout()
                button_layout.setContentsMargins(2, 2, 2, 2)
                button_widget.setLayout(button_layout)
                
                restore_btn = QPushButton('복원')
                restore_btn.clicked.connect(
                    lambda checked, f=backup['filename']: self.restore_backup(f)
                )
                button_layout.addWidget(restore_btn)
                
                archive_btn = QPushButton('영구보관')
                archive_btn.setStyleSheet('background-color: #95a5a6;')
                archive_btn.clicked.connect(
                    lambda checked, f=backup['filename']: self.archive_backup(f)
                )
                button_layout.addWidget(archive_btn)
                
                self.table.setCellWidget(row, 4, button_widget)
            
            if len(backups) == 0:
                self.table.setRowCount(1)
                no_data = QTableWidgetItem('백업 파일이 없습니다')
                no_data.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(0, 0, no_data)
                self.table.setSpan(0, 0, 1, 5)
        
        except Exception as e:
            self.main_window.show_error(f'백업 목록 조회 중 오류: {str(e)}')
    
    def restore_backup(self, filename):
        if self.main_window.confirm(
            f'이 백업으로 복원하시겠습니까?\n{filename}\n\n'
            '현재 데이터는 덮어씌워집니다.'
        ):
            try:
                self.main_window.backup_manager.restore_backup(filename)
                self.main_window.show_success(f'백업이 복원되었습니다: {filename}')
            except Exception as e:
                self.main_window.show_error(f'백업 복원 중 오류: {str(e)}')
    
    def archive_backup(self, filename):
        if self.main_window.confirm(f'이 백업을 영구 보관함으로 이동하시겠습니까?\n{filename}'):
            try:
                archive_path = self.main_window.backup_manager.archive_backup(filename)
                self.main_window.show_success(f'백업이 영구 보관되었습니다:\n{archive_path}')
                self.load_backups()
            except Exception as e:
                self.main_window.show_error(f'백업 보관 중 오류: {str(e)}')
