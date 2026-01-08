# 술음료 재고관리 시스템 설치 가이드

## 목차
1. [시스템 요구사항](#시스템-요구사항)
2. [Windows 설치](#windows-설치)
3. [macOS 설치](#macos-설치)
4. [Linux 설치](#linux-설치)
5. [문제 해결](#문제-해결)

---

## 시스템 요구사항

### 최소 사양
- **운영체제**: Windows 7/10/11, macOS 10.12+, Ubuntu 18.04+
- **프로세서**: 1GHz 이상
- **RAM**: 512MB 이상
- **디스크**: 100MB 여유 공간
- **Python**: 3.8 이상

### 권장 사양
- **RAM**: 2GB 이상
- **디스크**: 500MB 여유 공간 (데이터 증가 고려)
- **Python**: 3.10 이상

---

## Windows 설치

### 1단계: Python 설치

1. [Python 공식 웹사이트](https://www.python.org/downloads/) 방문
2. 최신 Python 3.x 버전 다운로드
3. 설치 시 **"Add Python to PATH"** 체크 ✅
4. "Install Now" 클릭

**설치 확인:**
```cmd
python --version
```
출력: `Python 3.x.x`

### 2단계: 프로그램 다운로드

**방법 1: ZIP 다운로드**
1. 프로젝트 ZIP 파일 다운로드
2. 원하는 위치에 압축 해제 (예: `C:\Programs\InventorySystem\`)

**방법 2: Git 사용**
```cmd
git clone <repository-url>
cd inventory-system
```

### 3단계: 패키지 설치

```cmd
cd C:\Programs\InventorySystem
pip install -r requirements.txt
```

### 4단계: 프로그램 실행

**방법 1: 배치 파일 사용 (추천)**
```cmd
run.bat
```
또는 `run.bat` 파일을 더블클릭

**방법 2: 직접 실행**
```cmd
python main.py
```

### 5단계: 바로가기 만들기

1. `run.bat` 파일 우클릭
2. "바로 가기 만들기" 선택
3. 바로가기를 바탕화면으로 이동
4. (선택) 바로가기 아이콘 변경

---

## macOS 설치

### 1단계: Homebrew 설치 (선택사항)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2단계: Python 설치

**방법 1: Homebrew 사용**
```bash
brew install python@3.11
```

**방법 2: 공식 설치 파일**
1. [Python 공식 웹사이트](https://www.python.org/downloads/macos/) 방문
2. macOS용 설치 파일 다운로드 및 실행

**설치 확인:**
```bash
python3 --version
```

### 3단계: 프로그램 다운로드

```bash
cd ~/Documents
git clone <repository-url>
cd inventory-system
```

또는 ZIP 파일을 다운로드하여 압축 해제

### 4단계: 패키지 설치

```bash
pip3 install -r requirements.txt
```

### 5단계: 프로그램 실행

**방법 1: 쉘 스크립트 사용**
```bash
./run.sh
```

**방법 2: 직접 실행**
```bash
python3 main.py
```

### 6단계: Dock에 추가 (선택사항)

실행 중인 앱 아이콘을 Dock에서 우클릭 → "옵션" → "Dock에 유지"

---

## Linux 설치

### 1단계: Python 설치

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

**설치 확인:**
```bash
python3 --version
```

### 2단계: 시스템 라이브러리 설치 (PyQt5용)

**Ubuntu/Debian:**
```bash
sudo apt install python3-pyqt5 libgl1-mesa-glx
```

**Fedora:**
```bash
sudo dnf install python3-qt5
```

**Arch Linux:**
```bash
sudo pacman -S python-pyqt5
```

### 3단계: 프로그램 다운로드

```bash
cd ~/Documents
git clone <repository-url>
cd inventory-system
```

### 4단계: 가상환경 생성 (권장)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5단계: 패키지 설치

```bash
pip install -r requirements.txt
```

### 6단계: 프로그램 실행

**방법 1: 쉘 스크립트 사용**
```bash
./run.sh
```

**방법 2: 직접 실행**
```bash
python3 main.py
```

### 7단계: 데스크톱 바로가기 생성 (선택사항)

`inventory-system.desktop` 파일 생성:
```bash
nano ~/.local/share/applications/inventory-system.desktop
```

내용:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=술음료 재고관리
Exec=/home/USERNAME/Documents/inventory-system/run.sh
Icon=applications-office
Terminal=false
Categories=Office;
```

`USERNAME`을 실제 사용자명으로 변경

---

## 가상환경 사용 (모든 OS, 권장)

가상환경을 사용하면 시스템 Python과 독립적으로 패키지를 관리할 수 있습니다.

### 생성
```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

### 활성화
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 비활성화
```bash
deactivate
```

---

## 문제 해결

### Python을 찾을 수 없다는 오류

**Windows:**
- 환경 변수 PATH에 Python 추가
- 제어판 → 시스템 → 고급 시스템 설정 → 환경 변수
- Path에 `C:\Python3x` 추가

**macOS/Linux:**
- `python3` 명령어 사용
- 또는 `~/.bashrc`나 `~/.zshrc`에 alias 추가:
  ```bash
  alias python=python3
  ```

### PyQt5 설치 오류

**Windows에서 Visual C++ 오류:**
1. [Visual C++ Redistributable](https://support.microsoft.com/ko-kr/help/2977003/the-latest-supported-visual-c-downloads) 다운로드 및 설치
2. PyQt5 재설치:
   ```cmd
   pip install PyQt5 --force-reinstall
   ```

**Linux에서 Qt 플랫폼 플러그인 오류:**
```bash
sudo apt install libxcb-xinerama0
```

### 한글이 깨져 보일 때

**Windows:** 일반적으로 문제 없음

**macOS:** 일반적으로 문제 없음

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install fonts-nanum

# Fedora
sudo dnf install google-noto-sans-cjk-ttc-fonts

# Arch Linux
sudo pacman -S noto-fonts-cjk
```

### 데이터베이스 파일 권한 오류

**모든 OS:**
```bash
# 프로젝트 디렉토리에서
chmod -R 755 data/
chmod -R 755 backups/
```

### 프로그램이 느릴 때

1. 오래된 데이터 백업 후 초기화
2. 더 나은 하드웨어 사용 고려
3. SSD 사용 권장

---

## 업데이트 방법

### 1. 데이터 백업
프로그램 내에서 백업 생성 또는:
```bash
cp -r data/ data_backup/
cp -r backups/ backups_backup/
```

### 2. 프로그램 업데이트
```bash
git pull
# 또는 새 ZIP 다운로드 및 압축 해제
```

### 3. 패키지 업데이트
```bash
pip install -r requirements.txt --upgrade
```

### 4. 데이터 복원 (필요시)
```bash
cp -r data_backup/ data/
```

---

## 완전 삭제 방법

### 1. 데이터 백업 (중요!)
```bash
cp -r data/ ~/Documents/inventory_backup/
cp -r backups/ ~/Documents/inventory_backup/
```

### 2. 프로그램 삭제
- 프로젝트 폴더 전체 삭제

### 3. Python 패키지 삭제 (선택사항)
```bash
pip uninstall PyQt5 matplotlib pandas python-dateutil
```

---

## 추가 도움말

### 공식 문서
- `README_PYQT5.md` - 사용 설명서
- `QUICKSTART.md` - 빠른 시작 가이드
- `EXAMPLES.md` - 사용 예제

### 문의
시스템 관리자에게 문의하세요.

---

**설치가 완료되었습니다! 🎉**

`run.bat` (Windows) 또는 `run.sh` (macOS/Linux)를 실행하여 프로그램을 시작하세요.
