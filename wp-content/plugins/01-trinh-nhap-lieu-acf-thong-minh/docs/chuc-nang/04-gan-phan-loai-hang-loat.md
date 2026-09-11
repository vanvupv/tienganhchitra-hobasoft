# Tài Liệu Chức Năng 04: Gán Phân Loại Hàng Loạt (Bulk Taxonomy Assigner)

## 📍 Vị Trí & Đường Dẫn
- **Tab Dashboard:** `Gán Phân Loại Hàng Loạt` (`#bulk-taxonomy`)
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L732-L820)

---

## 🎯 Mục Đích Sử Dụng
Cho phép gán Chuyên mục (Category), Thẻ (Tag) hoặc bất kỳ Custom Taxonomy nào cho hàng loạt bài viết cùng một lúc, hỗ trợ cú pháp phân cấp cha-con (`Cha > Con`).

---

## 🔄 Luồng Hoạt Động

1. **Chọn Post Type & Taxonomy:** Chọn Post Type bài viết đích và chọn Taxonomy cần gán (vd: `category`, `post_tag`, `product_cat`).
2. **Chọn Bài Viết:** Chọn danh sách bài viết nhận phân loại.
3. **Điền Giá Trị Term Hỗ Trợ Phân Cấp:**
   - Cú pháp: `Tin tức > Thế giới, Technology`
   - Bấm **"Gán Phân Loại Ngay"** $\rightarrow$ Hệ thống tự động tạo Term nếu chưa có và gọi `wp_set_post_terms()`.
