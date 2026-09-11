# WDM Quick Stack Installer — Luồng Nghiệp Vụ Chi Tiết (Flow Documentation)

> Plugin: `wdm-quick-installer`  
> Phiên bản: 1.0.0  
> Tác giả: WDM Portal Team

---

## Tổng Quan Hệ Thống

Plugin cho phép Admin cài đặt hàng loạt plugin từ WordPress.org thông qua 3 luồng chức năng chính, tất cả hoạt động trong một giao diện Admin duy nhất với thiết kế Glassmorphism Dark Mode.

---

## Luồng 1: Plugin Hay Dùng (Favorites)

```
[Admin mở trang Quick Installer]
        |
        v
[Backend PHP đọc `wdm_qi_favorites` từ wp_options]
        |
        v
[Render danh sách Favorites dạng Checkbox Pills]
        |
        v
[Admin tích chọn các plugin muốn cài]
        |
        v
[Click "+ Đưa vào hàng đợi"]
        |
        v
[JS: Kiểm tra slug trong danh sách Installed Plugins]
    - Nếu CHƯA CÀI: Thêm vào Queue với status "pending"
    - Nếu ĐÃ CÀI + CHƯA ACTIVE: Thêm vào Queue với action "activate"
    - Nếu ĐÃ CÀI + ĐÃ ACTIVE: Bỏ qua, hiện badge "Đã cài"
        |
        v
[Queue Console hiển thị danh sách chờ]
```

**API liên quan**: `GET /wdm-qi/v1/favorites`, `POST /wdm-qi/v1/favorites`

---

## Luồng 2: Bảng Plugin Đã Cài + Bộ Lọc

```
[Trang load → JS gọi GET /wdm-qi/v1/installed]
        |
        v
[PHP: get_plugins() + is_plugin_active() → trả JSON]
        |
        v
[Render bảng HTML 4 cột:
  Tên Plugin | Phiên bản | Trạng thái | Hành động]
        |
        v
[Live Filter: User gõ vào ô tìm kiếm]
        |
        v
[JS lọc DOM tức thì (không cần AJAX)]
        |
        v
[Highlight: Nếu slug plugin trùng với plugin đang trong Queue]
        |
        v
[Nút hành động nhanh:
  - Plugin ACTIVE → nút "Tắt nhanh" (màu đỏ)
  - Plugin INACTIVE → nút "Bật nhanh" (màu xanh lục)
  → Gọi POST /wdm-qi/v1/toggle]
```

**API liên quan**: `GET /wdm-qi/v1/installed`, `POST /wdm-qi/v1/toggle`

---

## Luồng 3: Tìm Kiếm Trực Tiếp WP.org

```
[User gõ từ khóa vào ô Search WP.org]
        |
        v
[JS: Debounce 500ms → Gọi GET /wdm-qi/v1/search?q={keyword}]
        |
        v
[PHP: Gọi plugins_api() với action='query_plugins']
        |
        v
[Trả về JSON: [{name, slug, author, rating, short_description, icons}]]
        |
        v
[JS: Render kết quả dưới dạng Card grid nhỏ gọn]
        |
        v
[Mỗi card có nút "+ Thêm nhanh"]
        |
        v
[JS: Thêm plugin đó vào Queue với status "pending"]
```

**API liên quan**: `GET /wdm-qi/v1/search?q={keyword}`

---

## Luồng Cài Đặt (Queue Processing)

```
[User click "🚀 Bắt Đầu Cài Đặt Hàng Loạt"]
        |
        v
[JS: Lấy plugin đầu tiên trong Queue có status "pending"]
        |
        v
[Cập nhật UI: Plugin đó chuyển sang status "installing"]
        |
        v
[JS gọi POST /wdm-qi/v1/install → { slug: "classic-editor" }]
        |
        v
[PHP xử lý (class-wdm-qi-installer.php):
  1. require_once wp-admin/includes (file, plugin-install, upgrader)
  2. WP_Filesystem()
  3. plugins_api() → lấy download_link
  4. Plugin_Upgrader::install(download_link)
  5. get_plugin_main_file(slug) → tìm đường dẫn file chính
  6. activate_plugin(plugin_path)]
        |
        v
[Trả về JSON: { success: true, status: "activated", message: "..." }]
        |
        v
[JS: Cập nhật UI plugin đó → status "done" (màu xanh lục neon)]
        |
        v
[JS: Lấy plugin tiếp theo trong Queue → Lặp lại]
        |
        v
[Khi Queue rỗng → Hiện thông báo "✅ Đã hoàn tất cài đặt X plugin"]
        |
        v
[Refresh bảng Installed Plugins tự động]
```

---

## REST API Endpoints

| Method | Endpoint                | Mô tả                                   | Auth  |
|--------|-------------------------|-----------------------------------------|-------|
| GET    | `/wdm-qi/v1/installed`  | Lấy tất cả plugin đã cài + trạng thái  | Admin |
| POST   | `/wdm-qi/v1/install`    | Cài đặt + kích hoạt 1 plugin theo slug  | Admin |
| POST   | `/wdm-qi/v1/toggle`     | Bật/tắt plugin đã cài                  | Admin |
| GET    | `/wdm-qi/v1/search`     | Tìm kiếm plugin trên WP.org             | Admin |
| GET    | `/wdm-qi/v1/favorites`  | Lấy danh sách plugin hay dùng           | Admin |
| POST   | `/wdm-qi/v1/favorites`  | Lưu danh sách plugin hay dùng           | Admin |

---

## Cấu Trúc Dữ Liệu wp_options

**Key**: `wdm_qi_favorites`

```json
[
  { "slug": "classic-editor",          "name": "Classic Editor" },
  { "slug": "contact-form-7",          "name": "Contact Form 7" },
  { "slug": "advanced-custom-fields",  "name": "Advanced Custom Fields" },
  { "slug": "elementor",               "name": "Elementor" },
  { "slug": "rank-math",               "name": "Rank Math SEO" },
  { "slug": "wordfence",               "name": "Wordfence Security" },
  { "slug": "litespeed-cache",         "name": "LiteSpeed Cache" },
  { "slug": "woocommerce",             "name": "WooCommerce" },
  { "slug": "wp-mail-smtp",            "name": "WP Mail SMTP" },
  { "slug": "updraftplus",             "name": "UpdraftPlus Backup" }
]
```
