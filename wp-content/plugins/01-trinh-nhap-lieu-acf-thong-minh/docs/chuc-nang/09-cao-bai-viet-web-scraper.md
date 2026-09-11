# Tài Liệu Chức Năng 09: Cào Bài Viết & Web Scraper (Online URL Scraper)

## 📍 Vị Trí & Đường Dẫn
- **Menu Admin:** `Smart Importer` $\rightarrow$ `Cào Bài Viết & Scraper`
- **URL Admin:** `admin.php?page=wpsai-smart-scraper`
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L1135-L1278)

---

## 🎯 Mục Đích Sử Dụng
Cho phép cào bóc tách nội dung chi tiết của bất kỳ bài viết/sản phẩm nào từ trang web ngoài chỉ bằng cách cung cấp đường dẫn URL và các bộ chọn (CSS Selectors / XPath) linh hoạt.

---

## 🔄 Luồng Hoạt Động

1. **Bước 1: Nhập URL Trang Nguồn:**
   - Người dùng điền đường dẫn URL cần cào (Ví dụ: `https://vnexpress.net/bai-viet-abc.html`).

2. **Bước 2: Cấu Hình Selectors (CSS / XPath):**
   - **Bộ chọn Tiêu đề (Title):** `h1`, `.title`, `//h1`
   - **Bộ chọn Nội dung (Content):** `.entry-content`, `#content`, `//div[@class='content']`
   - **Bộ chọn Ảnh đại diện:** `meta[property='og:image']`, `.post-thumbnail img`
   - **Phần tử loại bỏ:** `.ads-wrapper`, `.related-posts`, `script`

3. **Xem Trước Kết Quả Cào (Preview Box):**
   - Bấm nút **"Xem Trước Nội Dung Cào Được"** $\rightarrow$ Hệ thống gửi request cào thử nghiệm và hiển thị trực quan Tiêu đề, Ảnh đại diện và HTML nội dung đã bóc tách.

4. **Bước 3 & 4: Đăng Bài & Gán Phân Loại:**
   - Chọn Post Type đích (`post`, `product`), Trạng thái (`publish`, `draft`) và Gán Chuyên mục/Thẻ tự động.
   - Bấm **"Cào & Đăng Bài Viết Ngay"** $\rightarrow$ Tạo bài viết mới và hiển thị link xem trực tiếp.
