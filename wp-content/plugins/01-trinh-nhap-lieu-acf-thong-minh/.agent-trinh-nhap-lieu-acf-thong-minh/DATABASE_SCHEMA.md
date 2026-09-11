# CẤU TRÚC CƠ SỞ DỮ LIỆU & LƯU TRỮ (DATABASE_SCHEMA.md)

---

## 📊 1. WORDPRESS OPTIONS (`wp_options`)

Plugin lưu trữ các cấu hình và registry trong bảng `wp_options`:

| Option Name | Kiểu dữ liệu | Mô tả | Ví dụ giá trị |
|---|---|---|---|
| `wpsai_gemini_api_key` | `string` | Khóa API Google Gemini để gọi AI | `AQ.Ab8RN6K7vlHV...` |
| `wpsai_extension_api_key` | `string` | Khóa xác thực REST API cho Chrome Extension. Tự sinh nếu trống (`wp_generate_password(24, false)`) | `xK8mP2vN9wQ3rT7y...` |
| `wpsai_snapshots_registry` | `array` (serialized) | Danh sách metadata snapshot đã lưu. Mỗi phần tử chứa: `id`, `name`, `post_type`, `post_count`, `file_path`, `created_at`, `file_size_formatted` | `[{id: "snap_xxx", name: "Sản phẩm tháng 8", ...}]` |

---

## 📁 2. HỆ THỐNG FILE LƯU TRỮ

### 2.1 Thư mục Snapshot đơn tệp

```text
wp-content/uploads/wpsai-snapshots/
├── .htaccess           # "Options -Indexes\nDeny from all"
├── index.php           # "<?php // Silence is golden."
├── snap_1691234567.json
└── snap_1691345678.json
```

**Cấu trúc file snapshot JSON:**
```json
{
  "meta": {
    "name": "Dữ liệu sản phẩm tháng 8",
    "post_type": "product",
    "post_count": 45,
    "created_at": "2026-08-06 10:30:00"
  },
  "schema": [
    {"name": "acf_gia_ban", "label": "[ACF] Giá bán", "type": "acf_number"},
    {"name": "acf_dien_tich", "label": "[ACF] Diện tích", "type": "acf_number"}
  ],
  "posts": [
    {
      "post_id": 123,
      "post_title": "Căn hộ cao cấp quận 7",
      "post_content": "<p>Nội dung chi tiết...</p>",
      "acf_gia_ban": "5000000000",
      "acf_dien_tich": "85"
    }
  ]
}
```

### 2.2 Thư mục Cây Phân Cấp (Tree Repository)

```text
wp-content/uploads/wpsai-tree-repository/
├── .htaccess
├── index.php
├── manifest.json          # Chỉ mục cây (~5-50 KB)
├── product/
│   ├── chunk-node-pt-product-1.json    # ≤ 50 bài viết
│   └── chunk-node-pt-product-2.json
└── post/
    └── chunk-node-post-category-5-1.json
```

**Cấu trúc manifest.json:**
```json
{
  "version": "1.0.0",
  "updated_at": "2026-08-06 15:00:00",
  "nodes": [
    {
      "id": "node-pt-product",
      "label": "Sản phẩm (product)",
      "type": "post_type",
      "post_type": "product",
      "post_count": 120,
      "chunks": [
        {"file_rel": "product/chunk-node-pt-product-1.json", "count": 50, "size": "45 KB"},
        {"file_rel": "product/chunk-node-pt-product-2.json", "count": 50, "size": "42 KB"}
      ],
      "children": [
        {
          "id": "node-product-product_cat",
          "label": "Danh mục sản phẩm (product_cat)",
          "type": "taxonomy",
          "taxonomy": "product_cat",
          "children": [
            {
              "id": "node-product-product_cat-15",
              "label": "Bất Động Sản",
              "type": "term",
              "term_id": 15,
              "post_count": 30,
              "chunks": []
            }
          ]
        }
      ]
    },
    {
      "id": "node-workflows",
      "label": "Luồng Xử Lý & Prompt AI Mẫu",
      "type": "workflows",
      "children": [
        {"id": "node-wf-prompt-bds", "label": "Prompt Sinh Bài BĐS", "type": "workflow_item", "file_path": "workflows/prompt-bds.json"}
      ]
    }
  ]
}
```

**Cấu trúc file chunk JSON:**
```json
{
  "meta": {
    "node_id": "node-pt-product",
    "post_type": "product",
    "count": 50,
    "chunk_num": 1,
    "created_at": "2026-08-06 15:00:00"
  },
  "schema": [],
  "posts": [
    {"post_id": 101, "post_title": "...", "acf_gia_ban": "..."}
  ]
}
```

---

## 🏷️ 3. POST META KEYS

Plugin tương tác với các meta keys sau thông qua Engine:

| Meta Key | Nguồn | Mô tả |
|---|---|---|
| `_thumbnail_id` | WordPress Core | ID ảnh đại diện (Featured Image) |
| `{acf_field_name}` | ACF | Tên trường ACF (ví dụ: `gia_ban`, `dien_tich`) |
| `_{acf_field_name}` | ACF Internal | Reference key nội bộ ACF (tự động, plugin bỏ qua khi quét) |
| `{any_custom_key}` | Custom Meta | Bất kỳ meta key tùy chỉnh nào (import qua tiền tố `meta_*`) |

---

## 🔐 4. MÔ HÌNH BẢO MẬT

| Lớp bảo mật | Cơ chế | Áp dụng cho |
|---|---|---|
| **Nonce Verification** | `check_ajax_referer('wpsai_import_nonce_action', 'nonce')` | Tất cả AJAX endpoints |
| **Capability Check** | `current_user_can('manage_options')` | Tất cả AJAX endpoints |
| **REST API Key** | Header `X-WPSAI-API-KEY` hoặc param `api_key` so khớp `wp_options` | REST API endpoints |
| **File Protection** | `.htaccess` (`Deny from all`) + `index.php` trống | Thư mục snapshot/tree |
| **Input Sanitization** | `sanitize_text_field()`, `wp_kses_post()`, `intval()`, `esc_url_raw()` | Tất cả input |
