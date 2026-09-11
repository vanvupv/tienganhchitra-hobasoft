# Tài Liệu Chức Năng 03: Nhập Excel Hàng Loạt (Bulk Excel Importer)

## 📍 Vị Trí & Đường Dẫn
- **Tab Dashboard:** `Nhập Excel Hàng Loạt` (`#bulk-excel`)
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L582-L730)

---

## 🎯 Mục Đích Sử Dụng
Hỗ trợ đọc và phân tích file dữ liệu `.xlsx`, `.xls`, `.csv` có dung lượng lớn tại phía Client bằng thư viện SheetJS, tự động nhận diện ánh xạ các cột dữ liệu với trường bài viết & ACF và tiến hành import hàng loạt bài viết nhanh chóng.

---

## 🔄 Luồng Hoạt Động

1. **Nạp File Excel:** Người dùng kéo thả file `.xlsx` hoặc `.csv`. SheetJS đọc file tại phía trình duyệt và hiển thị danh sách các Sheet.
2. **Ánh Xạ Cột (Column Mapping):**
   - Hệ thống tự động so khớp tên cột Excel với các trường `post_title`, `post_content`, `post_excerpt`, `_thumbnail_id` và các meta key ACF.
   - Người dùng có thể tùy chỉnh ánh xạ từng cột thủ công nếu tên cột không khớp hoàn toàn.
3. **Thực Thi Batch Import:**
   - Hệ thống chia dữ liệu thành từng gói nhỏ (Batch Size = 50-100 bài) gửi về `admin-ajax.php` để xử lý không gây treo Server.
