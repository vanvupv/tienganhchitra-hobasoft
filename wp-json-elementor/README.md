# THƯ MỤC THƯ VIỆN ELEMENTOR JSON TEMPLATES (`wp-json-elementor`)

Thư mục này chứa toàn bộ các file Mẫu trang (Page Templates), file Nén Package (.zip), Script khởi tạo và Script nạp tự động vào WordPress Database dành cho dự án **Cha & Mom (GOONGBE VN)**.

---

## 📂 Danh Sách File trong Thư Mục `wp-json-elementor/`:

### 📄 1. Trang Chủ GOONGBE VN (Homepage):
- **File JSON**: `goongbe-homepage-elementor-template.json`
- **File ZIP Import**: `goongbe-homepage-elementor-template.zip`
- **Cấu trúc bao gồm**:
  - Section 1: Hero Banner (Goongbe Baby Collection).
  - Section 2: Danh Mục Sản Phẩm Nổi Bật (Layout Grid 2 Hàng x 2 Cột).
  - Section 3: Feature Promo Banner (Dưỡng Ẩm 48h - Công Thức Oji Relief).
  - Section 4: Best Sellers (Top sản phẩm bán chạy nhất).
  - Section 5: Mây - Nhân Vật Hoạt Hình Tại Thị Trường Việt Nam (Grid 2 cột).
  - Section 6: Đối Tác Chính Thức (Grid 6 cột logo hệ thống siêu thị & bán lẻ).
  - Section 7: GOONGBE's News (Tin tức & Truyền thông - Mockup Query Posts).
  - Section 8: Bottom Banner CTA (Bảo vệ làn da bé yêu).

### 🛠️ 2. Script Tự Động Nạp Database:
- **File PHP**: `import_elementor_template.php`
- **Cách dùng**: Truy cập `http://domain-cua-ban/wp-json-elementor/import_elementor_template.php` để nạp tự động vào bảng `wp_posts` & `wp_postmeta`.

---

## 🚀 Hướng Dẫn Thêm Trang Mới:
Khi thiết kế trang mới (ví dụ: Trang Giới Thiệu, Trang Liên Hệ, Trang Sản Phẩm):
1. Sinh file `.json` & `.zip` tương ứng lưu vào thư mục `wp-json-elementor/`.
2. Commit & Push toàn bộ thư mục `wp-json-elementor/` lên GitHub để lưu trữ và tự động sync lên Vietnix Hosting.
