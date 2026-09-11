# Tài Liệu Chức Năng 08: Tạo Nội Dung AI (Gemini AI Content Generator)

## 📍 Vị Trí & Đường Dẫn
- **Tab Dashboard:** `Tạo Nội Dung AI` (`#ai-generator`)
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L1052-L1133)

---

## 🎯 Mục Đích Sử Dụng
Sử dụng AI (Google Gemini Model) để tự động sinh ra Tiêu đề chuẩn SEO, Nội dung bài viết chi tiết, Tóm tắt và điền tự động giá trị cho các trường ACF tùy chỉnh dựa theo chủ đề hoặc từ khóa đầu vào.

---

## 🔄 Luồng Hoạt Động

1. **Nhập Từ Khóa & Cấu Hình Prompt:**
   - Điền chủ đề / từ khóa (ví dụ: `Đánh giá iPhone 15 Pro Max`).
   - Chọn tông giọng văn (`Chuyên nghiệp`, `Sáng tạo`, `Thân thiện`).
2. **Chọn Các Trường Cần Sinh AI:**
   - Tích chọn sinh Tiêu đề, Nội dung HTML, và các trường ACF cụ thể (Giá, Ưu điểm, Nhược điểm).
3. **Thực Thi & Đăng Bài:** Bấm **"Sinh Nội Dung AI & Tạo Bài Viết"** $\rightarrow$ AI tạo nội dung chuẩn và tạo bài viết mới tự động.
