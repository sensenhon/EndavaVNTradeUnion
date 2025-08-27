import pandas as pd
import json
import django
import os
from employee.models import Employee, Children

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Đường dẫn file Excel
excel_path = 'C:\\Users\\sshon\\OneDrive - ENDAVA\\1. Trade Union\\ImportTUMembershipListChildrenFinal.xlsx'  # Đổi thành tên file của bạn

df = pd.read_excel(excel_path)

for idx, row in df.iterrows():
    username = str(row['username']).strip()
    children_json = row['children']
    try:
        employee = Employee.objects.get(user__username=username)
    except Employee.DoesNotExist:
        print(f'Không tìm thấy employee với username: {username}')
        continue
    # Xóa toàn bộ children cũ
    Children.objects.filter(employee=employee).delete()
    # Thêm lại children mới
    try:
        children_list = json.loads(children_json)
        for child in children_list:
            name = child.get('name')
            dob = child.get('dob')
            if name and dob:
                Children.objects.create(employee=employee, name=name, dob=dob)
            else:
                print(f'Children info thiếu name hoặc dob cho employee {username}: {child}')
    except Exception as e:
        print(f'Lỗi parse children cho employee {username}: {e}')
print('Đã cập nhật xong Children info cho các employee.')
