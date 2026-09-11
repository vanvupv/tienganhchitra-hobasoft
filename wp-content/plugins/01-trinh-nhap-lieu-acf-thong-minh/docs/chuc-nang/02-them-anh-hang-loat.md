# Tài Liệu Chức Năng 02: Thêm Ảnh Hàng Loạt (Bulk Image Uploader)

## 📍 Vị Trí & Đường Dẫn
- **Tab Dashboard:** `Thêm Ảnh Hàng Loạt` (`#bulk-images`)
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L433-L580)

---

## 🎯 Mục Đích Sử Dụng
Cho phép quản trị viên tải lên nhiều ảnh từ máy tính hoặc dán danh sách URL ảnh từ xa, tự động gắn làm **Ảnh Đại Diện (Featured Image)** cho hàng loạt bài viết/sản phẩm mà không cần mở từng bài để sửa thủ công.

---

## 🔄 Luồng Hoạt Động

1. **Bước 1: Chọn Post Type & Các Bài Viết Nhận Ảnh:**
   - Chọn Post Type (ví dụ: `post`, `product`, `du-an`).
   - Lọc danh sách các bài viết chưa có ảnh đại diện hoặc tích chọn các bài viết cụ thể.

2. **Bước 2: Nguồn Ảnh (Upload / URL List):**
   - **Tải tệp ảnh từ máy:** Kéo thả hàng loạt ảnh `.jpg`, `.png`, `.webp` vào khu vực Dropzone.
   - **Nhập URL từ xa:** Dán danh sách đường dẫn URL ảnh, hệ thống dùng `media_sideload_image` để tự động tải về thư mục Media WordPress.

3. **Bước 3: Thực Thi Gán Ảnh Hàng Loạt:**
   - Hệ thống tự động ghép thứ tự ảnh với danh sách bài viết đã chọn và gọi AJAX gán `_thumbnail_id` cho từng bài viết.
