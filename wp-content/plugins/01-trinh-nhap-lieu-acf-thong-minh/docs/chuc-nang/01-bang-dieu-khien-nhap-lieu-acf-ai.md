# Tài Liệu Chức Năng 01: Bảng Điều Khiển Nhập Liệu ACF & AI

## 📍 Vị Trí & Đường Dẫn
- **Menu Admin:** `Smart Importer` $\rightarrow$ `Nhập Liệu ACF & AI`
- **URL Admin:** `admin.php?page=wp-acf-smart-importer`
- **File Xử Lý Chính:** [class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/01-trinh-nhap-lieu-acf-thong-minh/includes/class-wp-acf-smart-importer-admin.php#L200-L430)

---

## 🎯 Mục Đích Sử Dụng
Tự động nhận diện cấu trúc trường dữ liệu bài viết (Core & ACF/Postmeta) của bất kỳ Post Type nào, cho phép chỉnh sửa giá trị trực tiếp, sinh dữ liệu mẫu bằng AI/Rule, hoặc nhập dữ liệu hàng loạt từ Excel/CSV/Google Sheet mà không bị lệch cột.

---

## 🔄 Luồng Hoạt Động Chi Tiết 4 Bước

### 1️⃣ Bước 1: Quét Cấu Trúc Trường
- Người dùng chọn `Post Type` và `Bài Viết Mẫu/Đích` (Hoặc nhấp nút **Tạo Bài Viết Rỗng Mới**).
- Bấm **"Quét Các Trường Bài Viết"** $\rightarrow$ Hệ thống tự động thu thập:
  - Tất cả các trường mặc định (`post_title`, `post_content`, `post_excerpt`, `post_status`, `featured_image`).
  - Tất cả các trường tùy chỉnh **ACF** và **Postmeta** liên quan.

### 2️⃣ Bước 2: Bảng Cấu Trúc Trường & Tải File Excel Mẫu
- **Bảng Cấu Trúc:** Hiển thị `Label`, `Key/Name`, `Loại trường` và `Giá trị hiện tại`. Cho phép sửa và bấm **"Lưu/Cập nhật trực tiếp bài viết"**.
- **Nút "Tải File Excel Mẫu":** Tự động tạo và tải xuống file `.xlsx` trong đó dòng Tiêu đề (Header) trùng khớp 100% tên các trường dữ liệu vừa quét được + 1 dòng dữ liệu mẫu chuẩn.

### 3️⃣ Bước 3: Chọn Cách Điền Dữ Liệu
Người dùng chọn 1 trong 2 nguồn:
- **Cách A - Tự sinh dữ liệu:** Sinh dữ liệu ngẫu nhiên theo thuật toán Rule-based hoặc Gemini AI cho $N$ dòng bài viết.
- **Cách B - Tải từ File:** Kéo thả file Excel (`.xlsx`, `.csv`), Google Sheet URL, JSON, hoặc Notepad.
- **Thanh Preview Navigator:** Bấm nút `< Dòng trước` | `Dòng sau >` để kiểm tra trước giá trị sẽ được map vào bài viết.

### 4️⃣ Bước 4: Thực Thi Lưu / Import
- **Chế độ 1:** Chỉ cập nhật dòng dữ liệu đang xem trước vào đúng bài viết mẫu ở Bước 1.
- **Chế độ 2:** Nhập hàng loạt thành $N$ bài viết mới hoàn chỉnh trên WordPress với trạng thái bài viết (`Publish`, `Pending`, `Draft`).
- **Log & Progress:** Hiển thị thanh tiến trình % và nhật ký thực thi thời gian thực.
