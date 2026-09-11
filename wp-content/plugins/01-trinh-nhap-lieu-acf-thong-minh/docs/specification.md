# 🛠️ Quy Chuẩn Kỹ Thuật (Technical Specification) — ACF Smart Importer

## 1. Core Classes & Roles

- `WP_ACF_Smart_Importer_Admin`: Quản lý giao diện Admin Dashboard và render các tab chức năng.
- `WP_ACF_Smart_Importer_Ajax`: API Gateway kiểm tra bảo mật (Nonce & Capabilities) trước khi xử lý AJAX.
- `WP_ACF_Smart_Importer_Generator`: Phân tích cấu trúc trường ACF, gửi Prompt tới Gemini AI (`gemini-1.5-flash`) và tự tạo URL ảnh qua LoremFlickr.
- `WP_ACF_Smart_Importer_Engine`: Thực thi ghi bài viết `wp_insert_post()`, sideload media `media_handle_sideload()` và đệ quy tạo taxonomies.

---

## 2. External API Endpoints

- **Gemini AI API:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}`
- **LoremFlickr Image Mock Service:** `https://loremflickr.com/800/600/{keywords}?lock={rand_id}`
