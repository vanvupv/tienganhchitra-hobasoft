# Tài Liệu Chức Năng 06: Lấy Tiêu Đề Bài Viết (Bulk Title Extractor)

## 📍 Vị Trí & Đường Dẫn
- **Tab Dashboard:** `Lấy Tiêu Đề Bài Viết` (`#get-titles`)
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L902-L970)

---

## 🎯 Mục Đích Sử Dụng
Trích xuất nhanh danh sách Tiêu đề, Slug và Đường dẫn URL của toàn bộ bài viết theo Post Type để phục vụ việc kiểm tra SEO, nghiên cứu từ khóa hoặc đưa sang mô-đun Dịch Thuật AI.

---

## 🔄 Luồng Hoạt Động

1. **Chọn Post Type:** Chọn loại nội dung cần trích xuất.
2. **Thực Thi Trích Xuất:** Hệ thống truy vấn danh sách bài viết và hiển thị bảng Tiêu đề + Slug.
3. **Thao Tác Nhanh:** Copy danh sách tiêu đề vào bộ nhớ tạm hoặc xuất ra file `.txt` / `.csv`.
