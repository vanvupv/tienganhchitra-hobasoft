# Tài Liệu Chức Năng 11: Kết Nối API & Chrome Extension Gateway

## 📍 Vị Trí & Đường Dẫn
- **Menu Admin:** `Smart Importer` $\rightarrow$ `Kết Nối API`
- **URL Admin:** `admin.php?page=wpsai-api-settings`
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L1372-L1450)

---

## 🎯 Mục Đích Sử Dụng
Quản lý các khóa bảo mật (API Key / Nonce), cấu hình Gemini AI Key và kết nối Endpoint Bridge trực tiếp với Chrome Extension trên trình duyệt để cào 1-click ngay khi lướt web.

---

## 🔄 Luồng Hoạt Động

1. **Cấu Hình Gemini AI Key:**
   - Điền Google Gemini API Key để phục vụ tính năng sinh tự động bài viết và dịch thuật AI ở các tab khác.

2. **Cấu Hình Chrome Extension Bridge:**
   - Hệ thống cung cấp:
     - **Extension Token:** Khóa mã hóa bảo mật kết nối.
     - **Bridge Endpoint:** `http://localhost/11. BASE TEST CASE/wp-json/wpsai/v1/import` hoặc root `/api/ext/activate`.
   - Người dùng dán Token vào popup Chrome Extension. Khi duyệt bất kỳ trang báo/blog nào, chỉ cần bấm nút *"Auto-Post to WP"*, dữ liệu sẽ được đẩy trực tiếp về website.
