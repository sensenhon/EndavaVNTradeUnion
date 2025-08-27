import re
import pandas as pd

# Đường dẫn file Excel
excel_path = 'C:\\Users\\sshon\\OneDrive - ENDAVA\\1. Trade Union\\ImportTUMembershipList.xlsx'  # Đổi thành tên file của bạn
# Đường dẫn file log lỗi
log_path = 'C:\\Users\\sshon\\OneDrive - ENDAVA\\1. Trade Union\\import_error.txt'  # Đổi thành tên file log của bạn

# Đọc file Excel
df = pd.read_excel(excel_path)

# Đọc file log lỗi
with open(log_path, 'r', encoding='utf-8') as f:
    log = f.read()

# Tìm các dòng bị lỗi
row_errors = set()
for match in re.finditer(r'Row (\d+):', log):
    row_errors.add(int(match.group(1)))

# Lọc các dòng bị lỗi
error_rows = df.iloc[[r-2 for r in row_errors if r >= 2]]  # Trừ 2 vì pandas index bắt đầu từ 0, header là dòng 1

# Xuất ra file Excel mới
error_rows.to_excel('error_rows.xlsx', index=False)
print(f'Đã xuất {len(error_rows)} dòng lỗi ra file error_rows.xlsx')
