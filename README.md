# EndavaVNTradeUnion

## Developer:
Sen.Hon@endava.com

## Hướng dẫn chạy dự án

### 1. Clone repository

```bash
git clone https://github.com/sensenhon/EndavaVNTradeUnion.git
cd EndavaVNTradeUnion
```

### 2. Tạo và kích hoạt virtual environment (Windows PowerShell)

```powershell
py -m venv tuenv
.\tuenv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script, chạy:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Chạy migrations (nếu cần)

```bash
python manage.py migrate
```

### 5. Khởi động server

```bash
python manage.py runserver
```

Sau đó mở trình duyệt tại:

```text
http://127.0.0.1:8000/
```

## Ghi chú
- Nếu bạn dùng terminal khác như Git Bash hoặc CMD, thay lệnh activate bằng:
  - Git Bash: `source tuenv/Scripts/activate`
  - CMD: `tuenv\Scripts\activate.bat`
- Nếu gặp lỗi về module chưa cài, hãy kiểm tra lại file `requirements.txt` và chạy lại `pip install -r requirements.txt`.
