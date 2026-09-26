from playwright.sync_api import sync_playwright
import time

# Tổng số bài tập cần lấy
TONG_SO_BAI = 159 

print("🚀 KHỞI ĐỘNG CỖ MÁY VÉT SẠCH 159 BÀI TẬP (BẢN TỐI ƯU) 🚀")
print("-" * 50)

# Hàm chuyên dụng để lọc rác Menu
def loc_rac(van_ban_tho):
    # Danh sách các chữ rác cần loại bỏ
    tu_khoa_rac = ["Skip to main content", "Courses", "Assignments", "eBooks", "Tests", "Gradebook", "Messages"]
    van_ban_sach = []
    
    # Cắt văn bản thành từng dòng, nếu dòng nào là rác thì bỏ qua
    for dong in van_ban_tho.split('\n'):
        dong_chu = dong.strip()
        if dong_chu != "" and dong_chu not in tu_khoa_rac:
            van_ban_sach.append(dong_chu)
            
    return '\n'.join(van_ban_sach)

# Khởi tạo file trắng ban đầu
with open("bai_tap_tieng_anh.txt", "w", encoding="utf-8") as file:
    file.write("=== TÀI LIỆU ÔN TẬP TIẾNG ANH - 159 BÀI ===\n\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    
    print("1. Đang mở cửa đăng nhập...")
    page.goto("https://learn.eltngl.com/")
    page.get_by_text("Got it").click()
    page.get_by_text("Sign in").first.click()
    page.fill('input[name="identifier"]', 'sieunhancho')
    page.get_by_placeholder("Password").fill('14252007_lvT')
    page.keyboard.press("Enter")
    time.sleep(5) 
    
    print("2. Đang tiến vào danh sách khóa học...")
    page.get_by_text("ENG3 - GROUP 8").last.click(force=True)
    time.sleep(3) 
        
    print("3. Bấm mở bài tập đầu tiên...")
    page.get_by_text("1a | Grammar 1 | 1").first.click(force=True)
    time.sleep(6) 

    print("\n" + "="*50)
    print("⚙️ BẮT ĐẦU VÒNG LẶP HÚT CHỮ VÀ LẬT TRANG ⚙️")
    
    for bai_so in range(1, TONG_SO_BAI + 1):
        print(f"\n[Bài {bai_so}/{TONG_SO_BAI}] Đang xử lý...")
        
        noi_dung_bai = f"--- BÀI TẬP SỐ {bai_so} ---\n"
        
        # BƯỚC 1: HÚT CHỮ (Đã tích hợp Bộ Lọc Rác)
        try:
            # Hút trang chính và lọc rác ngay lập tức
            text_trang_chinh = page.inner_text("body")
            noi_dung_bai += loc_rac(text_trang_chinh)
            
            # Hút các khung con và lọc rác
            for frame in page.frames:
                text_trong_frame = frame.inner_text("body")
                text_sach = loc_rac(text_trong_frame)
                if len(text_sach) > 10: 
                    noi_dung_bai += "\n\n" + text_sach
        except Exception as e:
            noi_dung_bai += f"\n(Lỗi khi hút chữ bài này: {e})"

        # BƯỚC 2: LƯU VÀO SỔ
        with open("bai_tap_tieng_anh.txt", "a", encoding="utf-8") as file:
            file.write(noi_dung_bai + "\n\n" + "="*40 + "\n\n")
        print(f"✅ Đã lưu xong Bài {bai_so}.")

        # BƯỚC 3: BẤM NÚT NEXT BẰNG JAVASCRIPT
        if bai_so < TONG_SO_BAI:
            print(f"👉 Đang tìm nút Next để sang Bài {bai_so + 1}...")
            nut_next_duoc_bam = False
            time.sleep(1)

            cac_kieu_tim = [
                'button[data-event="forward_lo"]',
                'button.learningObject__controls-button.active_button',
                'button:has-text("Next")',
                'button[title="Next"]'
            ]

            for idx, frame in enumerate(page.frames):
                for kieu in cac_kieu_tim:
                    try:
                        nut = frame.locator(kieu)
                        if nut.count() > 0:
                            print(f"   => Đã khóa mục tiêu nút Next ở khung số {idx + 1}!")
                            
                            # TUYỆT CHIÊU MỚI: Dùng JS để click xuyên màng bảo vệ
                            try:
                                nut.first.evaluate("node => node.click()")
                            except:
                                nut.first.click(force=True)
                                
                            nut_next_duoc_bam = True
                            break
                    except Exception:
                        continue
                if nut_next_duoc_bam:
                    break
            
            if not nut_next_duoc_bam:
                print("⚠️ LỖI: Không thể chuyển bài!")
                break
                
            print(f"⏳ Đang chờ Bài {bai_so + 1} tải...")
            time.sleep(6) 
                
    print("\n" + "="*50)
    print("🎉 HOÀN TẤT THU THẬP! TẤT CẢ ĐÃ NẰM TRONG FILE bai_tap_tieng_anh.txt 🎉")
    time.sleep(5)
    browser.close()

print("-" * 30)
print("Robot đã nghỉ ngơi.")