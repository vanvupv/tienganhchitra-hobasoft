# HỆ THỐNG MẪU ELEMENTOR JSON - DỰ ÁN TIẾNG ANH CHỊ TRÀ

> **Thư mục:** `wp-json-elementor/.agent-wp-json-elementor/tienganh-chitra--11092026/`  
> **Cập nhật:** 21/09/2026  
> **Kiến trúc:** 100% Flexbox Container chuẩn Elementor Pro 3.x, Query động WordPress Post Types, thiết kế Responsive đầy đủ.

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

Toàn bộ các trang và module đã được tách thành từng thư mục con độc lập, khép kín (chứa đầy đủ file cấu hình `.json`, gói nén import `.zip`, script tái tạo `.py` và tài liệu kỹ thuật `.md`):

```
tienganh-chitra--11092026/
│
├── 📁 01-trang-chu/               # Toàn bộ 7 Sections Trang Chủ (Landing Page)
│   ├── trang-chu-elementor.json
│   ├── trang-chu-elementor.zip
│   ├── generate_trang_chu.py
│   ├── 2. Trang chu 7 section.md
│   └── (Ảnh nền & assets liên quan)
│
├── 📁 02-trang-gioi-thieu/        # Trang Giới Thiệu (Banner + Stats Cards + Bài viết)
│   ├── trang-gioi-thieu-elementor.json
│   ├── trang-gioi-thieu-elementor.zip
│   ├── generate_gioi_thieu.py
│   └── 5. Trang gioi thieu.md
│
├── 📁 03-trang-giang-vien/        # Trang Đội Ngũ Giảng Viên (Archive CPT giang_vien)
│   ├── trang-giang-vien-elementor.json
│   ├── trang-giang-vien-elementor.zip
│   ├── generate_giang_vien_page.py
│   └── 6. Trang giang vien.md
│
├── 📁 04-trang-co-so-vat-chat/    # Trang Cơ Sở Vật Chất (Lightbox Carousel & Z-pattern)
│   ├── trang-co-so-vat-chat-elementor.json
│   ├── trang-co-so-vat-chat-elementor.zip
│   ├── generate_co_so_vat_chat.py
│   └── 7. Trang co so vat chat.md
│
├── 📁 05-trang-thu-vien-anh/      # Trang Thư Viện Ảnh (Filterable Gallery 5 Tab)
│   ├── trang-thu-vien-anh-elementor.json
│   ├── trang-thu-vien-anh-elementor.zip
│   ├── generate_thu_vien_anh.py
│   └── 8. Trang thu vien anh.md
│
├── 📁 06-trang-tin-tuc/           # Trang Tin Tức & Sự Kiện (Dynamic Featured + Posts Grid)
│   ├── trang-tin-tuc-elementor.json
│   ├── trang-tin-tuc-elementor.zip
│   ├── generate_tin_tuc.py
│   └── 9. Trang tin tuc.md
│
├── 📁 07-danh-muc-bai-viet/      # Trang Danh Mục Bài Viết (Category / Archive 2 cột + Mobile List)
│   ├── danh-muc-bai-viet-elementor.json
│   ├── danh-muc-bai-viet-elementor.zip
│   ├── generate_danh_muc_bai_viet.py
│   └── 10. Trang danh muc bai viet.md
│
├── 📁 08-bang-vang-hoc-vien/       # Trang Bảng Vàng Học Viên (7 Section: Banner + Tabs + Lưới 8 Thẻ + Stats + CTA)
│   ├── bang-vang-hoc-vien-elementor.json
│   ├── bang-vang-hoc-vien-elementor.zip
│   ├── generate_bang_vang_hoc_vien.py
│   └── 11. Trang bang vang hoc vien.md
│
├── 📁 loop-items/                 # Các mẫu Loop Item động dùng trong Loop Grid / Carousel
│   ├── loop-item-giang-vien.json / .zip
│   ├── loop-item-khoa-hoc-3d.json / .zip
│   ├── loop-item-hoc-vien.json / .zip
│   └── loop-item-blog.json / .zip
│
└── 📄 TÀI LIỆU VÀ QUY CHUẨN CHUNG TẠI GỐC:
    ├── 1. Widget basic.md
    ├── 3. Theo doi do chinh xac.md
    ├── 4. Tong ket danh gia lan 1 - Quy chuan thiet lap theo Section.md
    └── master-config-quy-chuan-section.json
```

---

## 🚀 HƯỚNG DẪN TÁI TẠO BẰNG SCRIPT

Mỗi thư mục con đều chứa file script Python tương ứng (`generate_*.py`). Để tái tạo lại file JSON & ZIP của bất kỳ trang nào, bạn chỉ cần mở terminal tại thư mục của trang đó và chạy:

```bash
# Ví dụ tái tạo Trang Chủ:
cd 01-trang-chu
python generate_trang_chu.py

# Ví dụ tái tạo Trang Tin Tức:
cd 06-trang-tin-tuc
python generate_tin_tuc.py
```
File `.json` và `.zip` mới sẽ tự động được xuất ngay trong chính thư mục con đó.
