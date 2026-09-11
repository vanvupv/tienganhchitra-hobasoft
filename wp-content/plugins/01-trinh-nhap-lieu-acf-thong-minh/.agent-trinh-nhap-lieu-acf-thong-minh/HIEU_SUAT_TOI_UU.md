# HIỆU SUẤT TỐI ƯU & KỸ THUẬT (HIEU_SUAT_TOI_UU.md)

Tài liệu mô tả các **phương pháp tối ưu hiệu suất** đã áp dụng trong plugin, giải thích lý do và cách hoạt động.

---

## ⚡ 1. XỬ LÝ FILE EXCEL TẠI CLIENT (CLIENT-SIDE PARSING)

### Vấn đề
Nếu upload file Excel lên server rồi parse bằng PHP (PHPSpreadsheet), sẽ tốn RAM server, I/O đĩa, và thời gian truyền tải.

### Giải pháp đã áp dụng
- Sử dụng **SheetJS (XLSX.js v0.18.5)** parse file trực tiếp trên trình duyệt.
- Không gửi file Excel lên server → Không tốn bandwidth upload.
- Chỉ gửi từng dòng dữ liệu JSON qua AJAX khi import.

### Lợi ích
| Chỉ số | Upload lên Server | Parse tại Client (hiện tại) |
|---|---|---|
| RAM Server | Cao (PHPSpreadsheet ~50MB cho file lớn) | **0 MB** |
| Thời gian | Upload + Parse | Chỉ Parse (~instant) |
| Bandwidth | Toàn bộ file | Chỉ data JSON từng dòng |

---

## 🔄 2. IMPORT TUẦN TỰ VỚI DELAY (SEQUENTIAL AJAX WITH THROTTLE)

### Vấn đề
Gửi đồng thời hàng trăm AJAX request sẽ làm sập MySQL connection pool và vượt quá `max_execution_time`.

### Giải pháp đã áp dụng
```javascript
// Import từng dòng tuần tự, delay 200ms giữa các request
function importNextRow() {
    if (currentIndex >= totalRows) { done(); return; }
    $.post(ajaxurl, { action: 'wpsai_import_row', ... }, function(res) {
        currentIndex++;
        setTimeout(importNextRow, 200);  // Throttle 200ms
    });
}
```

### Lợi ích
- MySQL chỉ xử lý 1 INSERT/UPDATE tại mỗi thời điểm.
- Tránh `max_connections` exceeded.
- Progress bar cập nhật real-time từng dòng.
- Nếu 1 dòng lỗi → vẫn tiếp tục các dòng sau (không crash cả batch).

---

## 📦 3. PHÂN MẢNH DỮ LIỆU (CHUNKING)

### Vấn đề
Nếu lưu 500+ bài viết vào 1 file JSON duy nhất:
- File JSON có thể đạt 10-50 MB.
- `file_get_contents()` + `json_decode()` tốn ~100MB RAM.
- `max_execution_time` PHP (30s) có thể bị vượt.

### Giải pháp đã áp dụng
```php
// Tách dữ liệu thành từng chunk tối đa 50 bài / file
$chunk_size = 50;
$batches = array_chunk( $posts_data, $chunk_size );
foreach ( $batches as $index => $batch ) {
    // Mỗi batch lưu thành 1 file JSON riêng biệt (~30-80 KB)
    file_put_contents( $filepath, wp_json_encode( $chunk_content ) );
}
```

### So sánh hiệu suất

| Chỉ số | 1 file lớn (500 bài) | Chunking (10 files × 50 bài) |
|---|---|---|
| RAM khi đọc | ~80-120 MB | ~8-15 MB (chỉ đọc 1 chunk) |
| Thời gian đọc | 3-5 giây | 0.1-0.3 giây |
| Rủi ro timeout | Cao | **Rất thấp** |
| Khả năng lazy-load | Không | **Có** (chỉ load chunk khi click) |

---

## 🌳 4. CHỈ MỤC CÂY SIÊU NHẸ (MANIFEST LAZY LOADING)

### Vấn đề
Nếu phải scan toàn bộ database mỗi khi mở tab Kho Dữ Liệu → Chậm, timeout.

### Giải pháp đã áp dụng
- Lưu 1 file `manifest.json` (~5-50 KB) chứa **chỉ metadata** (tên nút, số bài, danh sách file chunk).
- Khi mở tab → Chỉ đọc manifest (~instant).
- Khi click nút cụ thể → Mới gọi AJAX đọc file chunk tương ứng (**Lazy Loading**).

---

## ⏱️ 5. TĂNG THỜI GIAN THỰC THI CHO TÁC VỤ NẶNG

### Giải pháp đã áp dụng
```php
// Cho các tác vụ quét dữ liệu lớn và gọi AI
if ( function_exists( 'set_time_limit' ) ) {
    @set_time_limit( 180 );  // 3 phút thay vì 30 giây mặc định
}

// Timeout HTTP khi gọi Gemini API
wp_remote_post( $url, array(
    'timeout' => 90,  // 90 giây thay vì 5 giây mặc định
) );
```

| Cấu hình | Mặc định PHP | Plugin đặt lại |
|---|---|---|
| `max_execution_time` | 30 giây | **180 giây** (cho quét/AI) |
| `wp_remote_post timeout` | 5 giây | **90 giây** (cho Gemini API) |

---

## 🔄 6. CƠ CHẾ QUAY VÒNG MODEL (FAILOVER)

### Vấn đề
API Gemini có thể lỗi do: Model bị disable, Rate limit, Region block, phiên bản API thay đổi.

### Giải pháp đã áp dụng
```php
$endpoints = array(
    'gemini-2.5-flash (v1beta)',   // Ưu tiên 1
    'gemini-2.0-flash (v1beta)',   // Ưu tiên 2
    'gemini-2.5-pro (v1beta)',     // Ưu tiên 3
    'gemini-flash-latest (v1beta)',// Ưu tiên 4
    'gemini-2.5-flash (v1)',       // Fallback cuối
);
foreach ( $endpoints as $ep ) {
    $response = wp_remote_post( $ep['url'], ... );
    if ( success ) return $response;  // Dừng ngay khi thành công
    $last_error = $error;             // Ghi lỗi, thử tiếp
}
return WP_Error( $last_error );       // Tất cả thất bại
```

### Lợi ích
- Tỷ lệ thành công cao hơn ~95% so với chỉ dùng 1 endpoint.
- Tự động chuyển model khi model chính bị lỗi tạm thời.

---

## 🛡️ 7. ACF FALLBACK AN TOÀN

### Vấn đề
Plugin ACF có thể bị vô hiệu hóa hoặc chưa cài đặt.

### Giải pháp đã áp dụng
```php
public static function get_acf_field_value( $field_name, $post_id ) {
    if ( function_exists( 'get_field' ) ) {
        return get_field( $field_name, $post_id );  // ACF API
    }
    return get_post_meta( $post_id, $field_name, true );  // Fallback WP Core
}
```

| Tình huống | Hành vi |
|---|---|
| ACF Active | Dùng `get_field()` / `update_field()` / `acf_get_field_groups()` |
| ACF Disabled | Fallback sang `get_post_meta()` / `update_post_meta()` |
| ACF Not Installed | Tất cả hàm ACF bị skip, plugin vẫn hoạt động với WP Core fields |

---

## 📊 8. GIỚI HẠN QUERY AN TOÀN

| Tác vụ | Giới hạn | Lý do |
|---|---|---|
| Quét snapshot | 500 bài/lần | Tránh timeout PHP 30s |
| Quét tree node | 200 bài/lần | Phân mảnh thành chunk 50 bài/file |
| Sinh AI 1 batch | 20 bài/lần | Giới hạn context window Gemini |
| Sinh rule-based | 100 bài/lần | Tránh RAM spike |
| Export | Không giới hạn (`-1`) | Client-side processing (SheetJS + JSZip) |

---

## 🎯 9. TỐI ƯU GIAO DIỆN FRONTEND

| Kỹ thuật | Chi tiết |
|---|---|
| **Conditional Asset Loading** | CSS/JS chỉ nạp khi hook = `toplevel_page_wp-acf-smart-importer`, không ảnh hưởng trang admin khác |
| **Tab Lazy Render** | Chỉ section tab đang active được hiển thị (`display: block`), các tab khác ẩn (`display: none`) |
| **DOM Delegation** | Sử dụng `$(document).on('click', '.dynamic-btn', ...)` cho các phần tử được render động |
| **HTML Escaping** | `$('<span>').text(value).html()` để tránh XSS khi render dữ liệu vào bảng |
| **Blob Download** | Xuất JSON/Excel tại client bằng `Blob` + `URL.createObjectURL()`, không cần round-trip server |
