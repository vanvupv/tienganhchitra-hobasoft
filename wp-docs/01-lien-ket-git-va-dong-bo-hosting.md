# HƯỚNG DẪN LIÊN KẾT VÀ ĐỒNG BỘ GIT VỚI CPANEL HOSTING

> **Dự án:** Tiếng Anh Chị Trà  
> **Repository:** [vanvupv/tienganhchitra-hobasoft](https://github.com/vanvupv/tienganhchitra-hobasoft.git)  
> **Nhánh mặc định (Default Branch):** `main`  
> **Domain / Thư mục Hosting:** `englishchitra.demoweb360.top`  
> **Ngày thiết lập:** 11/09/2026  

---

## 1. TỔNG QUAN HỆ THỐNG ĐỒNG BỘ

Quy trình đồng bộ mã nguồn được thiết lập theo mô hình tiêu chuẩn:

```
[Máy tính phát triển (Local)] 
          │
          │  git push origin main
          ▼
   [GitHub Repo] (Kho lưu trữ trung tâm)
          │
          │  cPanel Git™ Version Control (Update from Remote)
          ▼
[Hosting cPanel (Live Site)]
```

---

## 2. CHI TIẾT CÁC BƯỚC ĐÃ THỰC HIỆN

### Bước 1: Chuẩn hóa & Dọn sạch Hello Elementor Child Theme
* **Vị trí:** `wp-content/themes/hello-theme-child`
* **Xử lý:**
  - Loại bỏ ~1.800 dòng code thừa từ dự án bán hàng cũ (WooCommerce, ACF sản phẩm Cha & Mom, popup checkout).
  - Tối ưu `functions.php` chỉ giữ lại đoạn nạp CSS chuẩn của Hello Elementor và cơ chế chống dính cache tự động (`filemtime`).
  - Kiểm tra cú pháp PHP đạt chuẩn (`php -l`).

---

### Bước 2: Khởi tạo Git Local và đẩy lên GitHub
1. **Tạo file `.gitignore`:**
   Loại trừ các file tạm của hệ điều hành, logs, cache và file sao lưu:
   ```gitignore
   # OS files
   .DS_Store
   Thumbs.db
   desktop.ini

   # Logs and temp
   *.log
   *.tmp
   *.bak

   # Cache
   wp-content/cache/
   ```
2. **Khởi tạo và cấu hình remote:**
   ```bash
   git init -b main
   git remote add origin https://github.com/vanvupv/tienganhchitra-hobasoft.git
   ```
3. **Commit & Push toàn bộ mã nguồn:**
   ```bash
   git add .
   git commit -m "Initial commit: WordPress source and Hello Elementor child theme"
   git push -u origin main
   ```

---

### Bước 3: Cấu hình đồng bộ trong cPanel Hosting
1. **Chuẩn bị thư mục trên Hosting:**
   * Vào **cPanel $\rightarrow$ File Manager**.
   * Mở thư mục chứa website: `englishchitra.demoweb360.top`.
   * Xóa sạch các file mặc định/file rác bên trong để thư mục hoàn toàn trống (yêu cầu bắt buộc của Git khi clone).
2. **Tạo kết nối Git Version Control:**
   * Vào **cPanel $\rightarrow$ Git™ Version Control** $\rightarrow$ Bấm nút **Create**.
   * Bật **Clone a repository**: `ON`.
   * **Clone URL:** `https://github.com/vanvupv/tienganhchitra-hobasoft.git`
   * **Repository Path:** `englishchitra.demoweb360.top`
   * **Repository Name:** `tienganhchitra`
   * Bấm **Create** để cPanel kéo toàn bộ source code từ GitHub về hosting.

---

### Bước 4: Kiểm tra và xác nhận đồng bộ (Test Sync)
1. Tạo file kiểm tra `test-sync.txt` trên máy local.
2. Commit và đẩy lên GitHub:
   ```bash
   git add test-sync.txt
   git commit -m "Test: Thêm file test-sync.txt để kiểm tra đồng bộ Git"
   git push origin main
   ```
3. Trên cPanel: Vào **Git™ Version Control** $\rightarrow$ Bấm **Manage** (tại repo `tienganhchitra`) $\rightarrow$ Tab **Pull or Deploy** $\rightarrow$ Bấm **Update from Remote**.
4. **Kết quả:** File `test-sync.txt` đã xuất hiện trên hosting và truy cập được qua web thành công.

---

## 3. QUY TRÌNH LÀM VIỆC HÀNG NGÀY (DAILY WORKFLOW)

Từ bây giờ, mỗi khi bạn code hoặc sửa đổi giao diện, hãy thực hiện theo chu trình sau:

### 1. Tại máy Local (sau khi sửa xong code):
Chạy các lệnh trong terminal:
```bash
# 1. Kiểm tra các file đã sửa
git status

# 2. Thêm tất cả thay đổi
git add .

# 3. Tạo commit ghi chú nội dung sửa
git commit -m "Mo ta ngan gon noi dung thay doi"

# 4. Đẩy code lên GitHub
git push origin main
```

### 2. Tại cPanel (để cập nhật web trên host):
1. Đăng nhập vào cPanel Hosting.
2. Mở **Git™ Version Control**.
3. Bấm nút **Manage** tại repo `tienganhchitra`.
4. Chọn tab **Pull or Deploy** $\rightarrow$ Bấm nút **Update from Remote**.
5. Toàn bộ thay đổi sẽ được cập nhật ngay lập tức lên website.

---

## 4. LƯU Ý QUAN TRỌNG

1. **Về Cơ sở dữ liệu (Database):**
   * Git chỉ quản lý các tệp tin mã nguồn (PHP, CSS, JS, HTML, hình ảnh theme).
   * Dữ liệu bài viết, trang, cài đặt Elementor nằm trong database MySQL. Nếu có cập nhật cấu trúc database, cần import/export qua **phpMyAdmin**.
2. **File cấu hình `wp-config.php`:**
   * Thông tin kết nối database trên local và hosting có thể khác nhau (nếu chạy local môi trường riêng). Cần kiểm tra kỹ các hằng số `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
