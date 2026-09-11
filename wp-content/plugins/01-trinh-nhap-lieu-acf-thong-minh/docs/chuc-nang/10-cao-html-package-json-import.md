# Tài Liệu Chức Năng 10: Package JSON Import & Offline HTML Scraper

## 📍 Vị Trí & Đường Dẫn
- **Menu Admin:** `Smart Importer` $\rightarrow$ `Package JSON Import`
- **URL Admin:** `admin.php?page=wpsai-package-import`
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L1280-L1370)

---

## 🎯 Mục Đích Sử Dụng
Cho phép nạp dữ liệu offline từ các tệp tin HTML đã lưu bằng SingleFile hoặc nạp các gói dữ liệu Package `.json` đã được bóc tách sẵn từ xa để khôi phục và nhập hàng loạt vào website.

---

## 🔄 Luồng Hoạt Động

1. **Nạp File SingleFile HTML:**
   - Kéo thả file `.html` hoặc `.zip` được lưu từ trình duyệt.
   - Nhập hoặc chọn khối mẫu đại diện (Product snippet item) để hệ thống tự phân tích cấu trúc DOM.

2. **Cấu Hình Item Wrapper & Field Mapping:**
   - Điền bộ chọn khung bọc ngoài (`.product-item`, `.post-card`).
   - Ánh xạ tên trường (như `post_title`, `post_content`, `acf_price`) tương ứng với CSS Selectors tương đối.

3. **Nạp Gói Package JSON:**
   - Chọn tệp `.json` chứa danh sách bài viết + media.
   - Bấm **"Thực Thi Import Package"** $\rightarrow$ Hệ thống tự động tải media sideloading và tạo các bài viết tương ứng.
