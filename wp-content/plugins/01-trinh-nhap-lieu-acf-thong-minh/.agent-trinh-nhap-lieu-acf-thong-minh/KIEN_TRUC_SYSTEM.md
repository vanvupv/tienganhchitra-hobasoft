# KIẾN TRÚC HỆ THỐNG CHI TIẾT (KIEN_TRUC_SYSTEM.md)

Tài liệu mô tả chi tiết **từng file source code**, **từng class**, **từng phương thức**, và **từng AJAX endpoint** của plugin.

---

## 🏗️ 1. FILE KHỞI TẠO CHÍNH

### `trinh-nhap-lieu-acf-thong-minh.php`

| Mục | Chi tiết |
|---|---|
| Vai trò | Plugin Entry Point — Định nghĩa hằng số, nạp tất cả class, khởi tạo đối tượng |
| Hằng số | `WPSAI_VERSION` = '1.0.0', `WPSAI_PATH` = đường dẫn thư mục, `WPSAI_URL` = URL thư mục |
| Nạp Class | `require_once` tất cả 7 file class trong `includes/` |
| Khởi tạo | `new WP_ACF_Smart_Importer_Admin()`, `new WP_ACF_Smart_Importer_Ajax()` |

---

## 🏛️ 2. CHI TIẾT TỪNG CLASS PHP

---

### Class 1: `WP_ACF_Smart_Importer_Admin`
**File**: `includes/class-wp-acf-smart-importer-admin.php` (~2400 dòng)  
**Vai trò**: Đăng ký menu admin, nạp CSS/JS, render toàn bộ giao diện HTML 12 tab.

#### Phương thức

| Phương thức | Vai trò | Chi tiết kỹ thuật |
|---|---|---|
| `__construct()` | Hook `admin_menu` + `admin_enqueue_scripts` | |
| `register_admin_menu()` | Đăng ký trang menu plugin | `add_menu_page()`, icon `dashicons-database-import`, capability `manage_options` |
| `enqueue_admin_assets($hook)` | Nạp CSS/JS có điều kiện | Chỉ nạp khi hook = `toplevel_page_wp-acf-smart-importer`. Nạp: SheetJS CDN, `admin-style.css`, `admin-script.js`. Localize: `wpsai_params` (ajax_url, nonce) |
| `render_admin_page()` | Render HTML toàn bộ 12 tab | Output trực tiếp PHP/HTML inline. Mỗi tab là 1 `<section id="wpsai-tab-xxx">` |

#### 12 Tab giao diện

| # | Tab ID | Tên | Chức năng chính |
|---|---|---|---|
| 1 | `dashboard` | Bảng Điều Khiển Chính | Quét cấu trúc trường, mapping, import Excel/JSON |
| 2 | `mock-generator` | Sinh Dữ Liệu Ảo | Sinh Rule-based / AI, preview bảng dữ liệu |
| 3 | `bulk-duplicate` | Nhân Bản Hàng Loạt | Chọn bài mẫu → AI viết lại → Import |
| 4 | `scraper` | Cào Dữ Liệu Web | Nhập URL + CSS Selectors → Bóc tách |
| 5 | `bulk-images` | Ảnh Đại Diện Hàng Loạt | Gán/xóa ảnh đại diện cho nhiều bài |
| 6 | `export` | Xuất Dữ Liệu | Export Excel + ZIP ảnh |
| 7 | `settings` | Cấu Hình API Key | Gemini API Key + Test kết nối |
| 8 | `extension` | Chrome Extension | REST API Key + Hướng dẫn kết nối |
| 9 | `edit-fields` | Sửa Trực Tiếp | Quét + chỉnh sửa trường inline |
| 10 | `project-docs` | Tài Liệu Dự Án | Nhật ký, UI Components |
| 11 | `snapshot-repo` | Kho Dữ Liệu Mẫu | Quét/Lưu/Khôi phục Snapshot + Tree |
| 12 | `changelog` | Lịch Sử Thay Đổi | Modal changelog markdown |

---

### Class 2: `WP_ACF_Smart_Importer_Ajax`
**File**: `includes/class-wp-acf-smart-importer-ajax.php` (~2600 dòng)  
**Vai trò**: Xử lý tất cả AJAX request, kiểm tra bảo mật, điều phối logic.

#### Phương thức bảo mật

| Phương thức | Vai trò |
|---|---|
| `verify_security()` | Kiểm tra `check_ajax_referer('wpsai_import_nonce_action')` + `current_user_can('manage_options')`. Nếu thất bại → `wp_send_json_error()` + `wp_die()` |

#### Bảng AJAX Endpoints đầy đủ

| # | Action Name | Phương thức PHP | Tham số chính | Chức năng |
|---|---|---|---|---|
| 1 | `wpsai_get_post_types_and_fields` | `get_post_types_and_fields()` | — | Lấy danh sách Post Types + ACF Fields |
| 2 | `wpsai_import_row` | `import_row()` | `row_data`, `mapping`, `post_type`, `post_status` | Import 1 dòng dữ liệu |
| 3 | `wpsai_generate_mock_data` | `generate_mock_data()` | `post_type`, `count`, `mode`, `ref_post_id`, `fields` | Sinh dữ liệu ảo (rule/ai) |
| 4 | `wpsai_bulk_ai_generate` | `bulk_ai_generate()` | `post_type`, `count`, `user_topic`, `custom_titles`, `layout_template` | Sinh AI nâng cao (batch) |
| 5 | `wpsai_save_settings` | `save_settings()` | `gemini_key` | Lưu API Key vào `wp_options` |
| 6 | `wpsai_test_gemini_key` | `test_gemini_key()` | `gemini_key` | Test kết nối Gemini + Đo latency (ms) |
| 7 | `wpsai_create_blank_post` | `create_blank_post()` | `post_type` | Tạo bài viết rỗng mới (draft) |
| 8 | `wpsai_scan_post_fields` | `scan_post_fields()` | `post_id` | Quét 4 nhóm trường: Core + ACF + Taxonomy + Custom Meta |
| 9 | `wpsai_update_post_fields_directly` | `update_post_fields_directly()` | `post_id`, `fields{}` | Cập nhật trực tiếp giá trị các trường |
| 10 | `wpsai_get_posts_for_bulk_images` | `get_posts_for_bulk_images()` | `post_type` | Lấy danh sách bài viết kèm thumbnail |
| 11 | `wpsai_set_post_thumbnail_ajax` | `set_post_thumbnail_ajax()` | `post_id`, `attachment_id` | Gán/Xóa ảnh đại diện |
| 12 | `wpsai_get_posts_for_export` | `get_posts_for_export()` | `post_type` | Lấy danh sách bài viết + schema ACF cho export |
| 13 | `wpsai_get_export_data` | `get_export_data()` | `post_type`, `post_ids[]`, `fields[]` | Lấy dữ liệu chi tiết + file_mappings cho ZIP |
| 14 | `wpsai_scrape_url` | `scrape_url()` | `url`, `selectors{}` | Cào dữ liệu từ URL |
| 15-20 | `wpsai_snapshot_*` | `snapshot_scan/save/list/detail/restore/delete()` | Tùy endpoint | Quản lý Snapshot JSON |
| 21 | `wpsai_tree_get_manifest` | `tree_get_manifest()` | — | Tải chỉ mục cây manifest.json |
| 22 | `wpsai_tree_scan_and_save_node` | `tree_scan_and_save_node()` | `node_id`, `post_type`, `taxonomy`, `term_id` | Quét + lưu chunk cho 1 nút cây |
| 23 | `wpsai_tree_get_chunk_data` | `tree_get_chunk_data()` | `file_rel` | Đọc dữ liệu file chunk |

#### Helper nội bộ

| Phương thức | Vai trò |
|---|---|
| `call_gemini_api($prompt, $key, $json_mode)` | Instance method gọi Gemini (dùng cho test_key) |
| `get_attachment_id_from_acf($field_name, $post_id)` | Phân tích ACF image/file field → lấy attachment ID. Thử: raw value (int), array['ID'], URL → `attachment_url_to_postid()` |

---

### Class 3: `WP_ACF_Smart_Importer_Engine`
**File**: `includes/class-wp-acf-smart-importer-engine.php` (277 dòng)  
**Vai trò**: Động cơ chèn/cập nhật bài viết, xử lý media sideload, taxonomy phân cấp.

#### Phương thức (tất cả static)

| Phương thức | Vai trò | Chi tiết |
|---|---|---|
| `import_single_row($row, $mapping, $post_type, $post_status)` | Nhập 1 bài viết | Phân tích tiền tố key → routing: `acf_*` → ACF, `tax_*` → Taxonomy, `meta_*` → Post Meta. Nếu `post_id` tồn tại → `wp_update_post()`, ngược lại → `wp_insert_post()`. ACF Image field → auto sideload URL thành attachment ID. |
| `handle_media_import($file_url, $post_id)` | Sideload media | `download_url()` → `media_handle_sideload()`. Nếu input là numeric → trả attachment ID luôn. Nếu không phải URL → return false. |
| `handle_taxonomy_import($post_id, $term_path_str, $taxonomy, $append)` | Tạo/gán taxonomy phân cấp | Tách `","` thành nhiều đường dẫn → Tách `">"` thành từng cấp → `term_exists()` hoặc `wp_insert_term()` → `wp_set_object_terms()`. |

---

### Class 4: `WP_ACF_Smart_Importer_Generator`
**File**: `includes/class-wp-acf-smart-importer-generator.php` (1097 dòng)  
**Vai trò**: Sinh dữ liệu mẫu (Rule-based + AI), quét schema ACF, phân tích ảnh bài mẫu.

#### Phương thức

| Phương thức | Vai trò |
|---|---|
| `generate_rule_based_data($post_type, $count, ...)` | Sinh dữ liệu bằng thuật toán quy tắc, không cần API |
| `generate_field_value_by_rule($field, ...)` | Helper sinh giá trị theo loại trường (text, number, select, image...) |
| `generate_ai_based_data($post_type, $count, $api_key, ...)` | Sinh dữ liệu qua Gemini AI — xây prompt, gọi API, parse JSON |
| `get_acf_fields_for_post_type($post_type)` | Quét tất cả ACF Field Groups → lọc theo location rules → trả mảng trường thu gọn |
| `get_acf_field_value($field_name, $post_id)` | Helper đọc giá trị ACF an toàn, fallback `get_post_meta()` nếu ACF disabled |
| `is_value_empty($val)` | Kiểm tra trống thông minh (bảo toàn `0` và `false`) |
| `analyze_template_structure($post_id)` | Parse HTML bài mẫu bằng DOMDocument, tìm vị trí ảnh (Image Slots) |
| `inject_images_into_content($content, $image_ids, ...)` | Chèn ảnh từ pool vào nội dung, phân bổ theo mode (sequential/random/cycle) |
| `distribute_images($pool, $count, $mode)` | Helper phân bổ ảnh cho các vị trí |
| `call_gemini_api_static($prompt, $api_key, $json_mode)` | Gọi Gemini API với failover 5 endpoint, timeout 90s |

---

### Class 5: `WP_ACF_Smart_Importer_Scraper`
**File**: `includes/class-wp-acf-smart-importer-scraper.php` (198 dòng)  
**Vai trò**: Cào HTML từ URL, chuyển đổi CSS Selector → XPath, bóc tách dữ liệu.

#### Phương thức (tất cả static)

| Phương thức | Vai trò | Chi tiết |
|---|---|---|
| `css_to_xpath($selector)` | Chuyển CSS → XPath | `.class` → `contains(@class)`, `#id` → `@id=`, `tag.class` → `tag[contains(@class)]`. Nếu bắt đầu `/` → giữ nguyên XPath thô. |
| `scrape_url($url, $selectors)` | Tải + bóc tách HTML | `wp_remote_get()` → `DOMDocument::loadHTML()` → `DOMXPath::query()`. Selector `remove` xóa node thừa trước khi lấy content. Xử lý ảnh lazy-load (data-src). |

---

### Class 6: `WP_ACF_Smart_Importer_REST`
**File**: `includes/class-wp-acf-smart-importer-rest.php` (203 dòng)  
**Vai trò**: Cung cấp REST API endpoints cho Chrome Extension.

#### Phương thức

| Phương thức | Vai trò |
|---|---|
| `register_routes()` | Đăng ký 3 routes: `/connect` (GET), `/post-types` (GET), `/import` (POST) |
| `verify_permission($request)` | Xác thực API Key từ header `X-WPSAI-API-KEY` hoặc param `api_key` |
| `handle_connect($request)` | Trả `site_name` + thông báo kết nối thành công |
| `handle_get_post_types($request)` | Trả danh sách Post Types + Taxonomies |
| `handle_import($request)` | Nhập bài viết từ Extension, map custom fields → `acf_*`, gọi `Engine::import_single_row()` |
| `add_allowed_headers($headers)` | Thêm `X-WPSAI-API-KEY` vào CORS allowed headers |
| `send_cors_headers(...)` | Gửi headers CORS: `Allow-Origin: *`, `Allow-Methods: GET, POST, OPTIONS` |

---

### Class 7: `WP_ACF_Smart_Importer_Tree`
**File**: `includes/class-wp-acf-smart-importer-tree.php` (~200 dòng)  
**Vai trò**: Quản lý kho dữ liệu phân cấp dạng cây, file manifest.json, phân mảnh JSON.

#### Phương thức (tất cả static)

| Phương thức | Vai trò | Chi tiết |
|---|---|---|
| `get_tree_dir()` | Trả đường dẫn thư mục | `wp-content/uploads/wpsai-tree-repository/`. Auto tạo + `.htaccess` bảo vệ. |
| `get_manifest()` | Đọc manifest.json | Nếu chưa tồn tại → gọi `build_default_manifest()` |
| `build_default_manifest()` | Khởi tạo cây mặc định | Quét `get_post_types()`, `get_object_taxonomies()`, `get_terms()` → tạo cấu trúc nodes phân cấp. Thêm nút "Luồng Xử Lý & Prompt AI Mẫu". |
| `save_manifest($manifest)` | Ghi manifest.json | `wp_json_encode(JSON_UNESCAPED_UNICODE \| JSON_PRETTY_PRINT)` |
| `save_chunk_for_node($node_id, $post_type, $posts_data, $schema)` | Lưu chunk phân mảnh | `array_chunk($posts_data, 50)` → lưu từng file `chunk-{node_id}-{n}.json`. Cập nhật manifest node. |
| `update_manifest_node_chunks(&$nodes, ...)` | Đệ quy cập nhật chunk info trên cây | Duyệt đệ quy `$nodes` → tìm node theo ID → cập nhật `chunks[]` và `post_count`. |
| `read_node_data($file_rel)` | Đọc file chunk | Trả `WP_Error` nếu file không tồn tại hoặc JSON invalid. |

---

## 🎨 3. FILE FRONTEND

### `assets/css/admin-style.css`
- Hệ thống CSS Variables (`--wpsai-primary`, `--wpsai-secondary`...)
- Glassmorphism cards, gradient headers
- Responsive grid layouts
- Animation: `.wpsai-spin` (rotate 360deg), hover effects

### `assets/js/admin-script.js` (~6200 dòng)
- jQuery-based, wrapped trong `jQuery(document).ready()`
- **Tab Navigation**: `data-tab` attribute → show/hide `<section>` tương ứng
- **SheetJS Integration**: Parse Excel/CSV tại client, không upload lên server
- **Sequential AJAX**: Import từng dòng tuần tự với `setTimeout(200ms)` tránh server overload
- **Snapshot Module**: IIFE quản lý quét/lưu/khôi phục/xóa snapshot
- **Tree Module**: IIFE render cây tương tác, toggle mở/gọn, quét theo nút
