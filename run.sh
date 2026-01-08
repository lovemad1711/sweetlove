#!/bin/bash
# Linux/macOS용 실행 스크립트

echo "술음료 재고관리 시스템을 시작합니다..."
echo

# 가상환경이 있으면 활성화
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi

# 프로그램 실행
python3 main.py

# 오류 발생 시 메시지 표시
if [ $? -ne 0 ]; then
    echo
    echo "오류가 발생했습니다."
    read -p "Enter 키를 눌러 종료하세요..."
fi
