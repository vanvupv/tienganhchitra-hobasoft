# Tài Liệu Chức Năng 07: Nhân Bản Hàng Loạt (Bulk Post Duplicator)

## 📍 Vị Trí & Đường Dẫn
- **Tab Dashboard:** `Nhân Bản Hàng Loạt` (`#duplicate`)
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L972-L1050)

---

## 🎯 Mục Đích Sử Dụng
Cho phép chọn 1 bài viết mẫu và tạo ra $N$ bản sao (Duplicates) giữ nguyên 100% tất cả các trường dữ liệu ACF, Taxonomy và Featured Image, đồng thời tự động thêm tiền tố/hậu tố tiêu đề để thử nghiệm dữ liệu lớn.

---

## 🔄 Luồng Hoạt Động

1. **Chọn Bài Viết Nguồn:** Chọn Post Type và chọn bài viết gốc cần nhân bản.
2. **Cấu Hình Nhân Bản:**
   - Số lượng bản sao cần tạo (ví dụ: 10, 50 bản sao).
   - Quy tắc đặt tên: Thêm số thứ tự tự động (vd: `[Tên gốc] - Bản sao #1`).
3. **Thực Thi Nhân Bản:** Bấm **"Bắt Đầu Nhân Bản"** $\rightarrow$ Hệ thống sao chép `post` + toàn bộ `postmeta` ACF tương ứng.
