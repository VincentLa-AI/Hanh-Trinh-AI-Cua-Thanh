import requests
from bs4 import BeautifulSoup

print("Bắt đầu khởi động Bot cào dữ liệu...")
print("-" * 30)

# 1. Truy cập vào trang web VnExpress
url = 'https://vnexpress.net/'
response = requests.get(url)

# 2. Kiểm tra xem có truy cập thành công không
if response.status_code == 200:
    # 3. Phân tích cấu trúc trang web
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 4. Tìm kiếm các thẻ chứa tiêu đề bài báo
    danh_sach_tieu_de = soup.find_all('h3', class_='title-news', limit=10)
    
    # 5. In kết quả ra màn hình
    print(f"Đã tìm thấy {len(danh_sach_tieu_de)} tiêu đề:\n")
    for index, tieu_de in enumerate(danh_sach_tieu_de, start=1):
        chu = tieu_de.find('a').text.strip()
        print(f"{index}. {chu}")
else:
    print(f"Không thể truy cập trang web. Lỗi: {response.status_code}")

print("-" * 30)
print("Kết thúc!")