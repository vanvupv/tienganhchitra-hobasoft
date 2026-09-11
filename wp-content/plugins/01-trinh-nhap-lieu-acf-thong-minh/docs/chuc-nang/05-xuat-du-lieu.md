# Tài Liệu Chức Năng 05: Xuất Dữ Liệu (Data Exporter)

## 📍 Vị Trí & Đường Dẫn
- **Tab Dashboard:** `Xuất Dữ Liệu` (`#export`)
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L822-L900)

---

## 🎯 Mục Đích Sử Dụng
Cho phép trích xuất toàn bộ bài viết, các trường mặc định và toàn bộ trường dữ liệu ACF/Postmeta ra định dạng Excel (`.xlsx`), CSV hoặc JSON để sao lưu hoặc chuyển giao sang website khác.

---

## 🔄 Luồng Hoạt Động

1. **Chọn Post Type & Bộ Lọc:** Chọn Post Type cần xuất, lọc theo trạng thái (`publish`, `draft`) hoặc khoảng ID.
2. **Chọn Các Trường Cần Xuất:** Tích chọn các trường core (`title`, `content`, `excerpt`, `date`, `status`) và các trường meta ACF.
3. **Thực Thi Xuất:** Chọn định dạng tệp (`Excel`, `CSV`, `JSON`) và nhấp nút **"Xuất Dữ Liệu Ngay"** để tải file về máy.
