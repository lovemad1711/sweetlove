@echo off
REM Windows용 실행 스크립트

echo 술음료 재고관리 시스템을 시작합니다...
echo.

REM 가상환경이 있으면 활성화
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM 프로그램 실행
python main.py

REM 오류 발생 시 일시정지
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 오류가 발생했습니다.
    pause
)
