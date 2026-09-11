# 🛠️ Quy Chuẩn Kỹ Thuật (Technical Specification) — Quick Stack Installer

## 1. REST API Endpoints (`/wp-json/wdm-qi/v1`)

| Endpoint | Method | Chức năng |
| :--- | :---: | :--- |
| `/wdm-qi/v1/search-wp` | `GET` | Tìm kiếm plugin trực tiếp từ WordPress.org API (`plugins_api`) |
| `/wdm-qi/v1/install` | `POST` | Tải xuống, giải nén (`Plugin_Upgrader`) và kích hoạt plugin theo slug |
| `/wdm-qi/v1/installed` | `GET` | Lấy danh sách toàn bộ plugin hiện có trên host kèm trạng thái |

---

## 2. Các Hàm Core WordPress Được Sử Dụng

- **`plugins_api()`**: Nằm trong `wp-admin/includes/plugin-install.php`. Giúp truy vấn metadata và link tải `.zip` từ WordPress.org.
- **`Plugin_Upgrader`**: Lớp trong `wp-admin/includes/class-wp-upgrader.php` đảm nhiệm giải nén và chuyển thư mục vào `wp-content/plugins/`.
- **`activate_plugin()`**: Kích hoạt plugin vừa cài đặt.

---

## 3. Cấu Trúc File Plugin

```text
trinh-cai-dat-bo-plugin-nhanh/
├── trinh-cai-dat-bo-plugin-nhanh.php # File kích hoạt chính
├── docs/                             # Thư mục tài liệu
├── includes/
│   ├── class-wdm-qi-api.php          # REST API Endpoints
│   ├── class-wdm-qi-installer.php    # Core Logic Installer
│   └── class-wdm-qi-db.php           # Quản lý cấu hình Stack
├── assets/
│   ├── css/admin-style.css
│   └── js/installer-queue.js         # JavaScript Hàng đợi Queue AJAX
└── templates/main-page.php           # Giao diện Grid 3 Cột
```
