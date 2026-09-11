# TÀI LIỆU KIẾN TRÚC VÀ LUỒNG XỬ LÝ CHI TIẾT (ARCHITECTURE & DATA FLOWS)

Tài liệu này được lưu trữ trực tiếp trong thư mục plugin để hỗ trợ các nhà phát triển bảo trì, nâng cấp mã nguồn của **WP Smart Auto-Importer & AI Generator** về sau.

---

## 1. TỔNG QUAN KIẾN TRÚC (ARCHITECTURE OVERVIEW)

Plugin áp dụng kiến trúc hướng đối tượng (OOP) và phân tách vai trò rõ ràng giữa Client-side (Frontend) và Server-side (Backend).

```mermaid
graph TD
    subgraph Client-side (Trình duyệt)
        A[admin-script.js] <--> B[admin-style.css]
        A -->|Đọc file Excel/CSV/JSON thô| JS_Library[SheetJS/XLSX ở Client]
        A -->|Dựng Excel Base64| JS_Library
    end

    subgraph WordPress Admin UI
        C[class-wp-acf-smart-importer-admin.php] -->|Enqueue Scripts/Styles & Render HTML| A
    end

    subgraph API Gateway (AJAX Control)
        D[class-wp-acf-smart-importer-ajax.php]
    end

    subgraph Core Business Logic
        E[class-wp-acf-smart-importer-generator.php]
        F[class-wp-acf-smart-importer-engine.php]
    end

    A <-->| AJAX Request / Response | D
    D <-->| Gọi sinh dữ liệu mẫu | E
    D <-->| Gọi xử lý chèn dữ liệu | F
    E -->| API HTTP Post | Gemini[Gemini AI API]
    F -->| wp_insert_post & update_field | WP_DB[(WordPress Database)]
    F -->| Sideload ảnh ngoài | WP_Media[WP Media Library]
```

### Các tệp tin chính và nhiệm vụ:
1.  **[wp-acf-smart-importer.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/wp-acf-smart-importer.php)**: Tệp khởi động plugin (Main Plugin File), chứa khai báo thông tin plugin và khởi tạo các lớp cốt lõi.
2.  **[class-wp-acf-smart-importer-admin.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/includes/class-wp-acf-smart-importer-admin.php)**: Quản lý Menu WordPress, đăng ký enqueues scripts/styles và render mã HTML giao diện Dashboard các Tabs (bao gồm tab Lấy Tiêu Đề Bài Viết).
3.  **[class-wp-acf-smart-importer-ajax.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/includes/class-wp-acf-smart-importer-ajax.php)**: Cầu nối tiếp nhận AJAX Requests từ Frontend. Kiểm tra tính hợp lệ bảo mật (nonce) và phân quyền (`manage_options`), hỗ trợ thêm API `wpsai_get_post_titles` và `wpsai_update_post_title`.
4.  **[class-wp-acf-smart-importer-generator.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/includes/class-wp-acf-smart-importer-generator.php)**: Bộ máy sinh dữ liệu ảo bằng Rule-based hoặc Gemini AI, hỗ trợ quét nhóm trường ACF (kể cả khai báo bằng code PHP).
5.  **[class-wp-acf-smart-importer-engine.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/includes/class-wp-acf-smart-importer-engine.php)**: Công cụ import chính. Thực hiện chèn/cập nhật bài viết, sideload hình ảnh về máy chủ và gán giá trị ACF / Custom Postmeta.
6.  **[admin-script.js](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/assets/js/admin-script.js)**: Điều phối toàn bộ hoạt động ở Client: Xử lý file nguồn, điều khiển Grid Preview, quản lý hàng đợi AJAX tuần tự (batching) và hiển thị tiến trình.

---

## 2. CHI TIẾT 5 LUỒNG XỬ LÝ CHÍNH (5 CORE PROCESSING FLOWS)

---

### LUỒNG 1: QUÉT TRƯỜNG & HIỂN THỊ XEM TRƯỚC (SCHEMA DISCOVERY FLOW)

Luồng này cho phép người dùng chọn một bài viết có sẵn để quét tất cả các trường (Core WordPress, ACF và Custom Meta) và hiển thị lên bảng cấu trúc trường.

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**: ID bài viết chuẩn (`post_id`) được gửi qua AJAX POST.
*   **Xử lý (Processing)**:
    1.  `scan_post_fields()` kiểm tra bảo mật (nonce & capability).
    2.  Trích xuất 6 trường cốt lõi của WordPress (Title, Content, Excerpt, Date, Slug, Featured Image) kèm giá trị hiện tại.
    3.  Gọi `WP_ACF_Smart_Importer_Generator::get_acf_fields_for_post_type($post_type)` để tìm các nhóm trường ACF áp dụng cho Post Type đó (quét cả trong database lẫn các trường định nghĩa bằng code PHP trong `functions.php` qua `$group['location']`).
    4.  Gọi `get_post_meta()` để lấy toàn bộ Custom Meta trong bảng `wp_postmeta`, lọc bỏ các khóa hệ thống mặc định của WordPress (`_edit_lock`, `_thumbnail_id`, etc.) và ACF internal keys.
*   **Đầu ra (Output)**: Một chuỗi JSON chứa mảng các trường dạng:
    `{ name: 'acf_price', label: 'Giá bán', type: 'acf_number', current_value: '150000', is_acf: true, is_system: false, choices: [] }`
*   **Client Render**: Javascript nhận mảng trường, render bảng cấu trúc, tự động gán ô `contenteditable` để sửa trực tiếp và tự động map các cột dữ liệu nguồn khi file được tải lên ở các bước sau.

---

### LUỒNG 2: THỰC THI NHẬP LIỆU HÀNG LOẠT (BULK IMPORT FLOW)

Luồng này tiếp nhận dữ liệu dòng (đọc từ Excel hoặc tự sinh) và thực hiện chèn bài viết mới hoặc cập nhật bài viết cũ.

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**:
    *   `row`: Đối tượng dữ liệu dòng: `{ col_0: "Sản phẩm A", col_1: "150000" }`
    *   `mapping`: Bản đồ ánh xạ: `{ post_title: "col_0", acf_price: "col_1" }`
    *   `post_type`: CPT mục tiêu (ví dụ: `post`).
    *   `post_status`: Trạng thái bài viết mặc định (ví dụ: `draft`).
*   **Xử lý (Processing)**:
    1.  Client JS chạy hàng đợi đệ quy: Gửi từng dòng dữ liệu lên backend thông qua AJAX `wpsai_import_row` để tránh lỗi nghẽn hoặc timeout PHP.
    2.  Engine kiểm tra xem dòng có chứa cột ánh xạ `post_id` (nếu có cập nhật) hay không.
    3.  Gọi `wp_update_post()` để sửa bài viết cũ hoặc `wp_insert_post()` để chèn bài viết mới.
    4.  Nếu cột ánh xạ `featured_image` có giá trị URL, gọi `handle_media_import()` để tải ảnh về máy chủ tạm thời, sideload vào Media Library qua `media_handle_sideload()` và set làm ảnh đại diện.
    5.  Duyệt qua các cột ánh xạ trường tùy chỉnh:
        -   Tiền tố `acf_`: Kiểm tra loại trường. Nếu là Image/File thì sideload ảnh; nếu là Checkbox/Select nhiều giá trị thì tách chuỗi dấu phẩy thành mảng; nếu là số/logic thì ép kiểu. Gọi `update_field()` để cập nhật dữ liệu.
        -   Tiền tố `meta_`: Gọi `update_post_meta()` để lưu trực tiếp vào postmeta.
*   **Đầu ra (Output)**: Trả về ID bài viết và permalink của bài viết được tạo/cập nhật thành công.
*   **Client Feedback**: JS nhận kết quả, tăng thanh tiến trình, ghi log trực quan và tiếp tục gọi dòng tiếp theo sau 150ms.

---

### LUỒNG 3: THÊM ẢNH HÀNG LOẠT (BULK ADD IMAGES FLOW)

Luồng này nhận danh sách ảnh đã chọn ở Media Library và gán làm thumbnail cho các bài viết được lựa chọn.

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**:
    *   Mảng ID các bài viết: `[102, 103, 104, 105]`
    *   Mảng các ảnh đã chọn từ Media: `[{id: 12, url:...}, {id: 15, url:...}]`
    *   Chế độ gán: `sequential` (Thứ tự), `random` (Ngẫu nhiên), hoặc `range` (Khoảng - kèm kích thước khoảng $N$).
*   **Xử lý (Processing)**:
    1.  Client JS tính toán ánh xạ bài viết - ảnh:
        -   Thứ tự: Bài viết $i$ nhận ảnh $i \pmod{\text{số ảnh}}$.
        -   Khoảng: Bài viết $i$ nhận ảnh $\lfloor i / N \rfloor \pmod{\text{số ảnh}}$.
    2.  JS chạy vòng lặp gửi yêu cầu AJAX `wpsai_set_post_thumbnail_ajax` tuần tự cho từng bài viết.
    3.  PHP Backend nhận yêu cầu, kiểm tra bảo mật, thực hiện gọi hàm `set_post_thumbnail( $post_id, $attachment_id )`.
*   **Đầu ra (Output)**: Ảnh đại diện được gán trong WordPress, trả về URL ảnh thu nhỏ để JS cập nhật trực tiếp lên bảng danh sách bài viết thời gian thực.

---

### LUỒNG 4: NHÂN BẢN BÀI VIẾT HÀNG LOẠT (BULK DUPLICATE FLOW)

Luồng này quét bài viết mẫu, gọi AI hoặc Quy tắc để sinh ra tập dữ liệu nháp có nội dung viết lại mới, sau đó gọi Engine lưu hàng loạt bài viết mới.

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**: ID bài viết chuẩn (`ref_post_id`), số lượng bản sao cần tạo (`count`), trạng thái bài viết mục tiêu (`status`), chế độ nhân bản (`rule` hoặc `ai`).
*   **Xử lý (Processing)**:
    1.  Client JS gọi AJAX quét cấu trúc trường bài viết gốc để nắm được schema cụ thể.
    2.  Gọi AJAX sinh dữ liệu ảo (Mock generator):
        -   Nếu là `ai`: PHP Backend lấy dữ liệu bài viết gốc làm mẫu ngữ cảnh (Examples), cấu hình Prompt gửi lên Gemini AI yêu cầu viết lại nội dung mới cho tất cả các bản ghi, đảm bảo chất lượng, đúng cấu trúc trường.
        -   Nếu là `rule`: Sinh nhanh bằng quy tắc tiếp vĩ ngữ cho tiêu đề.
    3.  Backend trả về mảng dữ liệu các dòng đã được viết lại.
    4.  Client JS nhận dữ liệu và thực hiện chạy vòng lặp gửi yêu cầu AJAX `wpsai_import_row` để chèn bài viết mới và lưu ACF/Meta.
*   **Đầu ra (Output)**: Tạo thành công các bài viết mới trên Database, hiển thị link xem bài viết trên log tiến trình.

---

### LUỒNG 5: XUẤT DỮ LIỆU RA EXCEL & ZIP (EXPORT FLOW)

Luồng này trích xuất thông tin bài viết và đóng gói hình ảnh đính kèm (Ảnh đại diện & Ảnh ACF) thành gói ZIP.

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**:
    *   Mảng ID các bài viết cần xuất.
    *   Mảng tên các trường cần xuất (Ví dụ: `post_title`, `acf_price`, `featured_image`).
*   **Xử lý (Processing)**:
    1.  Client JS gửi yêu cầu lấy dữ liệu. Backend truy vấn Database:
        -   Với các cột text/số, lấy giá trị.
        -   Với trường ảnh/file (featured_image, acf_image), gọi `get_attached_file()` để tìm đường dẫn tuyệt đối local trên server.
        -   Tính toán đường dẫn tương đối trong ZIP cho ảnh (ví dụ: `images/102_featured_pic.jpg`) và thay thế giá trị này vào ô dữ liệu Excel, đồng thời lưu bản đồ file: `[ 'images/102_featured_pic.jpg' => '/var/www/.../pic.jpg' ]`.
    2.  Client nhận dữ liệu, chuyển đổi tên cột sang nhãn thân thiện (ví dụ: `post_title` -> `Tiêu đề`), dùng SheetJS xuất tệp Excel `.xlsx` ở dạng chuỗi Base64.
    3.  Client gửi chuỗi Excel Base64 và bản đồ file lên AJAX `wpsai_create_zip_export`. Backend dùng `ZipArchive` tạo file zip, giải mã Excel Base64 ghi vào zip, copy toàn bộ ảnh trong bản đồ ghi vào thư mục `images/` trong zip.
*   **Đầu ra (Output)**: URL download file ZIP (Ví dụ: `http://localhost/.../wpsai-temp/export-post-2026.zip`).

---

## 3. GIẢI THÍCH MÃ NGUỒN CỐT LÕI (LINE-BY-LINE EXPLANATION)

### 3.1 Gán ảnh đại diện bằng AJAX (Backend)
Trong file [class-wp-acf-smart-importer-ajax.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/includes/class-wp-acf-smart-importer-ajax.php#L470-L504):

```php
public function set_post_thumbnail_ajax() {
    $this->verify_security(); // 1. Xác thực nonce bảo mật và kiểm tra quyền quản trị.
    $post_id       = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0; // 2. Lấy Post ID chuyển về kiểu int.
    $attachment_id = isset( $_POST['attachment_id'] ) ? intval( $_POST['attachment_id'] ) : 0; // 3. Lấy Media ID chuyển về kiểu int.

    if ( ! $post_id || ! get_post( $post_id ) ) {
        wp_send_json_error( array( 'message' => __( 'Bài viết không tồn tại.', 'wp-acf-smart-importer' ) ) ); // 4. Báo lỗi nếu không có post.
    }

    if ( ! $attachment_id ) {
        delete_post_thumbnail( $post_id ); // 5. Nếu ID ảnh bằng 0, thực hiện xoá ảnh đại diện hiện tại.
        wp_send_json_success( array(
            'message'   => __( 'Đã xóa ảnh đại diện thành công.', 'wp-acf-smart-importer' ),
            'thumb_url' => '',
        ) );
    }

    if ( ! wp_attachment_is_image( $attachment_id ) ) {
        wp_send_json_error( array( 'message' => __( 'ID ảnh không hợp lệ.', 'wp-acf-smart-importer' ) ) ); // 6. Kiểm tra xem ID có thực sự là tệp ảnh không.
    }

    $res = set_post_thumbnail( $post_id, $attachment_id ); // 7. Thực hiện gán ảnh đại diện của bài viết trong DB.

    if ( $res ) {
        $thumb_url = wp_get_attachment_image_url( $attachment_id, 'thumbnail' ); // 8. Lấy link ảnh thu nhỏ vừa gán.
        wp_send_json_success( array(
            'message'   => __( 'Đã gán ảnh đại diện thành công.', 'wp-acf-smart-importer' ),
            'thumb_url' => $thumb_url, // 9. Gửi link ảnh thu nhỏ về client để cập nhật trực tiếp lên bảng giao diện.
        ) );
    } else {
        wp_send_json_error( array( 'message' => __( 'Không thể gán ảnh đại diện.', 'wp-acf-smart-importer' ) ) );
    }
}
```

---

### 3.2 Tải và tạo tệp ZIP xuất dữ liệu (Backend)
Trong file [class-wp-acf-smart-importer-ajax.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/includes/class-wp-acf-smart-importer-ajax.php#L701-L751):

```php
public function create_zip_export() {
    $this->verify_security(); // 1. Xác thực bảo mật.

    $xlsx_b64   = isset( $_POST['xlsx_base64'] ) ? $_POST['xlsx_base64'] : ''; // 2. Lấy chuỗi base64 của file Excel từ client.
    $files_json = isset( $_POST['files'] ) ? wp_unslash( $_POST['files'] ) : ''; // 3. Lấy chuỗi json chứa bản đồ file ảnh.
    $post_type  = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';

    if ( empty( $xlsx_b64 ) ) {
        wp_send_json_error( array( 'message' => __( 'Thiếu nội dung Excel.', 'wp-acf-smart-importer' ) ) );
    }

    $upload_dir = wp_upload_dir();
    $temp_dir = $upload_dir['basedir'] . '/wpsai-temp'; // 4. Định nghĩa thư mục lưu trữ zip tạm thời.
    if ( ! file_exists( $temp_dir ) ) {
        wp_mkdir_p( $temp_dir ); // 5. Tạo thư mục nếu chưa tồn tại.
    }

    $this->cleanup_temp_dir( $temp_dir ); // 6. Dọn dẹp xoá các file zip tạm đã tạo quá 1 giờ trước đó để giải phóng ổ cứng.

    // 7. Tạo tên file zip độc nhất có kèm mã bảo mật
    $zip_filename = 'export-' . $post_type . '-' . date( 'Ymd_His' ) . '_' . wp_generate_password( 6, false ) . '.zip';
    $zip_filepath = $temp_dir . '/' . $zip_filename;

    if ( ! class_exists( 'ZipArchive' ) ) {
        wp_send_json_error( array( 'message' => __( 'Máy chủ không hỗ trợ ZipArchive.', 'wp-acf-smart-importer' ) ) );
    }

    $zip = new ZipArchive();
    if ( $zip->open( $zip_filepath, ZipArchive::CREATE | ZipArchive::OVERWRITE ) !== true ) {
        wp_send_json_error( array( 'message' => __( 'Không thể khởi tạo tệp ZIP.', 'wp-acf-smart-importer' ) ) );
    }

    // 8. Giải mã Base64 và chèn file Excel danh-sach-bai-viet.xlsx vào thư mục gốc của file ZIP.
    $xlsx_data = base64_decode( $xlsx_b64 );
    $zip->addFromString( 'danh-sach-bai-viet.xlsx', $xlsx_data );

    // 9. Duyệt qua mảng bản đồ hình ảnh để gộp vào ZIP
    $files_to_add = json_decode( $files_json, true );
    if ( is_array( $files_to_add ) ) {
        foreach ( $files_to_add as $zip_path => $server_path ) {
            // 10. Chỉ chèn tệp nếu nó thực sự tồn tại trên ổ đĩa local của máy chủ.
            if ( file_exists( $server_path ) && is_file( $server_path ) ) {
                $zip->addFile( $server_path, $zip_path ); // Ghi tệp vào zip theo đường dẫn tương đối (images/...)
            }
        }
    }

    $zip->close(); // 11. Hoàn tất nén, đóng gói file ZIP.

    $zip_url = $upload_dir['baseurl'] . '/wpsai-temp/' . $zip_filename; // 12. Lấy URL công khai của file ZIP.
    wp_send_json_success( array(
        'download_url' => $zip_url, // 13. Trả URL tải về cho client.
        'message'      => __( 'Đóng gói file ZIP thành công!', 'wp-acf-smart-importer' ),
    ) );
}
```

---

### 3.3 Hàm đệ quy Import dữ liệu từng dòng (Client-side JS)
Trong file [admin-script.js](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/assets/js/admin-script.js#L817-L870):

```javascript
// Dòng 817: Khởi động hàm đệ quy xử lý hàng đợi
function runNext() {
    if (currentIndex >= totalRows) {
        $progressBar.css('width', '100%').text('100%'); // 1. Khi hoàn thành toàn bộ hàng đợi, đẩy thanh tiến trình lên 100%.
        $progressStats.html(`<p style="color:#46b450; font-weight:bold;">Đã hoàn thành! Thành công: ${successCount}. Lỗi: ${errorCount}.</p>`);
        $('#wpsai-start-import-btn').prop('disabled', false); // 2. Mở khoá lại nút bấm.
        
        if (importMode === 'update_current') {
            $('#wpsai-scan-btn').trigger('click'); // 3. Nếu là cập nhật bài hiện tại, tự động quét lại để cập nhật giá trị mới lên bảng.
        }
        return;
    }

    const item = queue[currentIndex]; // 4. Lấy phần tử dữ liệu dòng hiện tại trong hàng đợi.
    const displayTitle = item.row[item.mapping['post_title']] || 'Bài viết #' + (currentIndex + 1);

    $log.append(`<p>Đang xử lý ${currentIndex + 1}/${totalRows}: <strong>${displayTitle}</strong>...</p>`);
    $log.scrollTop($log[0].scrollHeight); // 5. Tự động cuộn khung log xuống dưới cùng.

    // 6. Gửi AJAX lên máy chủ xử lý lưu dòng hiện tại
    $.ajax({
        url: wpsai_params.ajax_url,
        type: 'POST',
        data: {
            action: 'wpsai_import_row',
            nonce: wpsai_params.nonce,
            row: item.row,
            mapping: item.mapping,
            post_type: postType,
            post_status: postStatus
        },
        success: function (res) {
            if (res.success) {
                successCount++; // 7. Tăng bộ đếm thành công.
                $log.append(`<p style="color:#46b450; margin:0 0 5px 15px;">✓ Thành công! ID bài viết: <a href="${res.data.permalink}" target="_blank">${res.data.post_id}</a> - ${res.data.title}</p>`);
            } else {
                errorCount++; // 8. Tăng bộ đếm thất bại.
                $log.append(`<p style="color:#dc3232; margin:0 0 5px 15px;">✗ Thất bại! Lỗi: ${res.data.message || 'Lỗi không xác định'}</p>`);
            }
            
            currentIndex++; // 9. Tiến tới dòng tiếp theo.
            const percent = Math.round((currentIndex / totalRows) * 100);
            $progressBar.css('width', percent + '%').text(percent + '%'); // 10. Cập nhật phần trăm tiến trình.
            $progressStats.html(`<p>Đang xử lý ${currentIndex}/${totalRows}. Thành công: ${successCount}, Lỗi: ${errorCount}</p>`);
            
            setTimeout(runNext, 150); // 11. Chờ 150ms rồi gọi lại chính nó đệ quy (runNext) để xử lý tiếp dòng tiếp theo.
        },
        error: function () {
            errorCount++;
            $log.append(`<p style="color:#dc3232; margin:0 0 5px 15px;">✗ Thất bại! Lỗi HTTP.</p>`);
            currentIndex++;
            setTimeout(runNext, 150); // 12. Tiếp tục xử lý kể cả khi gặp sự cố HTTP của dòng này.
        }
    });
}
```

---

### LUỒNG 6: TỰ ĐỘNG TẠO TAXONOMY PHÂN CẤP (HIERARCHICAL TAXONOMY AUTO-CREATION FLOW)

Luồng này tự động phát hiện, sinh dữ liệu mẫu và import các taxonomy phân cấp (ví dụ: Chuyên mục/Thẻ) từ chuỗi văn bản phân tách bằng ký tự `>` (ví dụ: `Bất động sản > Chung cư`).

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**:
    *   Tên trường taxonomy có tiền tố `tax_` (ví dụ: `tax_category`).
    *   Chuỗi giá trị cột phân cấp (ví dụ: `Bất động sản > Chung cư, Tin tức > Dự án`).
*   **Xử lý (Processing)**:
    1.  Quét các taxonomy đã đăng ký của Post Type thông qua hàm `get_object_taxonomies()`.
    2.  Trong quá trình sinh dữ liệu:
        -   **AI Mode**: Prompt chỉ thị cho Gemini sinh chuỗi phân cấp với dấu phân tách `>` đồng bộ với ngữ nghĩa chủ đề.
        -   **Rule-based Mode**: Tự động ghép chuỗi ngẫu nhiên hoặc lấy từ các term sẵn có.
    3.  Trong quá trình Import, Engine nhận dạng tiền tố `tax_` và tách chuỗi:
        -   Tách các nhánh bằng dấu phẩy `,` để xử lý song song nhiều danh mục.
        -   Tách từng cấp bằng dấu `>` từ trái qua phải (Cha -> Con -> Cháu).
        -   Kiểm tra sự tồn tại của term ở cấp tương ứng bằng `term_exists( $name, $taxonomy, $parent_id )`.
        -   Nếu chưa tồn tại, tự động gọi `wp_insert_term( $name, $taxonomy, array( 'parent' => $parent_id ) )` để tạo mới.
        -   Gán tất cả term ID cấp cuối và các cấp trung gian vào bài viết qua `wp_set_object_terms()`.
*   **Đầu ra (Output)**: Cấu trúc cây chuyên mục được tạo lập hoàn chỉnh trên Database của WordPress và bài viết được liên kết chính xác.

---

### LUỒNG 7: ĐỒNG NHẤT NGỮ NGHĨA CHỦ ĐỀ & TẢI ẢNH UNSPLASH (SEMANTIC THEME COHESION FLOW)

Luồng này ứng dụng Trí tuệ nhân tạo Gemini để sinh ra các bài viết ảo mà tất cả các trường dữ liệu (Title, Content, ACF và từ khóa mô tả ảnh) đều liên kết chặt chẽ với nhau theo một chủ đề duy nhất trên mỗi dòng.

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**: Khóa API Gemini, cấu trúc trường và số lượng dòng cần sinh.
*   **Xử lý (Processing)**:
    1.  Tạo Prompt chi tiết cho Gemini, hướng dẫn rõ yêu cầu đồng nhất chủ đề cho từng bài viết: "Nếu tiêu đề là về ẩm thực Việt Nam, nội dung bài viết phải nói về ẩm thực Việt Nam, các trường ACF như giá cả/địa điểm phải hợp lý, và trường ảnh phải trả về một từ khóa tiếng Anh miêu tả món ăn đó".
    2.  Yêu cầu định dạng phản hồi bắt buộc là JSON sạch (MimeType `application/json`).
    3.  Backend nhận chuỗi JSON từ Gemini, phân tích và thực hiện hậu xử lý (Post-processing) đối với các trường hình ảnh.
    4.  Mô tả ảnh dạng chữ tiếng Anh (ví dụ: `vietnamese traditional pho soup`) sẽ được mã hóa và chèn vào URL truy vấn ảnh chất lượng cao của LoremFlickr: `https://loremflickr.com/800/600/vietnamese,traditional,pho,soup`.
    5.  Khi import, Engine tải ảnh từ URL động này về máy chủ tạm thời và sideload vào WordPress Media Library.
*   **Đầu ra (Output)**: Bộ dữ liệu mẫu có chất lượng tiệm cận bài viết thật, hình ảnh minh họa khớp 100% nội dung bài viết.

---

### 3.4 Xử lý nhập chuyên mục phân cấp và gán vào bài viết (Backend)
Trong file [class-wp-acf-smart-importer-engine.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/includes/class-wp-acf-smart-importer-engine.php#L215-L275):

```php
public static function handle_taxonomy_import( $post_id, $term_path_str, $taxonomy ) {
    if ( empty( $term_path_str ) || empty( $taxonomy ) ) {
        return; // 1. Thoát sớm nếu chuỗi dữ liệu đầu vào hoặc tên taxonomy bị rỗng.
    }

    // 2. Tách các đường dẫn bằng dấu phẩy (Cho phép gán bài viết vào nhiều nhánh danh mục cùng lúc)
    $paths = array_map( 'trim', explode( ',', $term_path_str ) );
    $all_term_ids = array();

    foreach ( $paths as $path ) {
        if ( empty( $path ) ) {
            continue; // Bỏ qua nếu nhánh đường dẫn rỗng.
        }

        // 3. Tách từng cấp của đường dẫn danh mục bằng dấu ">" (Ví dụ: "Bất động sản > Chung cư")
        $levels = array_map( 'trim', explode( '>', $path ) );
        $parent_id = 0; // Bắt đầu từ gốc (không có cha)

        foreach ( $levels as $level_name ) {
            if ( empty( $level_name ) ) {
                continue; // Bỏ qua nếu tên cấp danh mục bị rỗng.
            }

            // 4. Kiểm tra xem term đã tồn tại ở cấp này (với cha $parent_id) chưa
            $term = term_exists( $level_name, $taxonomy, $parent_id );

            if ( $term ) {
                // 5. Nếu đã tồn tại, lấy term_id hiện có làm parent_id cho cấp con kế tiếp
                if ( is_array( $term ) ) {
                    $parent_id = intval( $term['term_id'] );
                } else {
                    $parent_id = intval( $term );
                }
            } else {
                // 6. Nếu chưa tồn tại, tiến hành tạo mới danh mục
                $args = array();
                if ( $parent_id > 0 ) {
                    $args['parent'] = $parent_id; // Thiết lập cha cho danh mục mới tạo
                }
                
                $inserted = wp_insert_term( $level_name, $taxonomy, $args );

                if ( ! is_wp_error( $inserted ) && is_array( $inserted ) ) {
                    $parent_id = intval( $inserted['term_id'] ); // Lấy ID vừa tạo làm cha cho cấp tiếp theo
                } else {
                    break; // Dừng nhánh xử lý này nếu xảy ra lỗi tạo term (ví dụ trùng slug...)
                }
            }

            // 7. Lưu ID term hợp lệ vào danh sách gom để chuẩn bị gán vào bài viết
            if ( $parent_id > 0 ) {
                $all_term_ids[] = $parent_id;
            }
        }
    }

    // 8. Thực hiện gán toàn bộ danh sách term IDs đã thu thập vào bài viết (thay thế hoàn toàn terms cũ nếu $append = false, hoặc gán thêm nếu $append = true)
    if ( ! empty( $all_term_ids ) ) {
        wp_set_object_terms( $post_id, array_unique( $all_term_ids ), $taxonomy, $append );
    }
}
```

---

### LUỒNG 8: GÁN PHÂN LOẠI HÀNG LOẠT (BULK TAXONOMY ASSIGNMENT FLOW)

Luồng này tiếp nhận danh sách các bài viết được chọn và thực hiện gán nhanh một taxonomy (Category, Tags hoặc Custom Taxonomy) cho toàn bộ bài viết đó.

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**:
    *   Mảng ID các bài viết: `[203, 204, 205]`
    *   Tên taxonomy cần gán: `category` hoặc `post_tag`
    *   Danh sách Term IDs (nếu chọn sẵn) hoặc Chuỗi đường dẫn phân cấp (nếu nhập tùy ý)
    *   Chế độ lưu: `append` (gán thêm) hoặc `replace` (gán đè)
*   **Xử lý (Processing)**:
    1.  Client JS tải danh sách các bài viết của Post Type đã chọn.
    2.  Gọi AJAX `wpsai_get_taxonomies_for_post_type` để lấy các taxonomy công khai của Post Type đó để hiển thị lên dropdown.
    3.  Khi thay đổi taxonomy, gửi AJAX `wpsai_get_terms_by_taxonomy` để load tất cả các term hiện có của taxonomy đó render ra checklist.
    4.  Khi bấm thực thi, Client JS chạy hàng đợi AJAX tuần tự gửi yêu cầu gán phân loại lên máy chủ thông qua AJAX `wpsai_assign_taxonomy_terms_ajax` để đảm bảo không bị quá tải.
    5.  Backend tiếp nhận, kiểm tra dữ liệu đầu vào và quyền hạn bảo mật.
    6.  Nếu nhập đường dẫn tùy chỉnh (Custom Path), gọi hàm đệ quy `WP_ACF_Smart_Importer_Engine::handle_taxonomy_import(..., $append)` để tự động tạo cây phân cấp.
    7.  Nếu chọn từ checklist term sẵn có, gọi trực tiếp `wp_set_object_terms( $post_id, $term_ids, $taxonomy, $append )`.
*   **Đầu ra (Output)**: Phân loại bài viết được cập nhật tức thì trên Database, trả về danh sách Term mới nhất của bài viết để cập nhật trực tiếp trên bảng.

---

### 3.5 Gán phân loại cho bài viết cụ thể qua AJAX (Backend)
Trong file [class-wp-acf-smart-importer-ajax.php](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/wp-acf-smart-importer/includes/class-wp-acf-smart-importer-ajax.php):

```php
public function assign_taxonomy_terms_ajax() {
    $this->verify_security(); // 1. Xác thực nonce và kiểm tra quyền hạn manage_options.
    $post_id    = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0; // 2. Lấy ID bài viết.
    $taxonomy   = isset( $_POST['taxonomy'] ) ? sanitize_text_field( $_POST['taxonomy'] ) : ''; // 3. Lấy tên taxonomy.
    $input_type = isset( $_POST['input_type'] ) ? sanitize_text_field( $_POST['input_type'] ) : 'existing'; // 4. Lấy nguồn nhập (existing hoặc custom_path).
    $mode       = isset( $_POST['mode'] ) ? sanitize_text_field( $_POST['mode'] ) : 'replace'; // 5. Lấy chế độ gán (append hoặc replace).

    if ( ! $post_id || ! get_post( $post_id ) ) {
        wp_send_json_error( array( 'message' => __( 'Bài viết không tồn tại.', 'wp-acf-smart-importer' ) ) );
    }

    if ( empty( $taxonomy ) || ! taxonomy_exists( $taxonomy ) ) {
        wp_send_json_error( array( 'message' => __( 'Taxonomy không hợp lệ.', 'wp-acf-smart-importer' ) ) );
    }

    $append = ( 'append' === $mode ); // 6. Chuyển đổi mode thành biến boolean $append để truyền vào WordPress Core.

    if ( 'existing' === $input_type ) {
        $term_ids = isset( $_POST['term_ids'] ) ? array_map( 'intval', $_POST['term_ids'] ) : array(); // 7. Thu thập mảng ID các term được chọn từ checklist.
        $res = wp_set_object_terms( $post_id, $term_ids, $taxonomy, $append ); // 8. Thực hiện gán mảng ID vào bài viết.
    } else {
        $custom_path = isset( $_POST['custom_path'] ) ? sanitize_text_field( $_POST['custom_path'] ) : ''; // 9. Lấy chuỗi đường dẫn phân cấp người dùng tự gõ.
        if ( empty( $custom_path ) ) {
            wp_send_json_error( array( 'message' => __( 'Chưa nhập đường dẫn danh mục/thẻ.', 'wp-acf-smart-importer' ) ) );
        }
        
        WP_ACF_Smart_Importer_Engine::handle_taxonomy_import( $post_id, $custom_path, $taxonomy, $append ); // 10. Gọi Engine phân tách và tạo tự động term đệ quy.
        $res = true;
    }

    if ( is_wp_error( $res ) ) {
        wp_send_json_error( array( 'message' => $res->get_error_message() ) );
    }

    // 11. Lấy danh sách tên term hiện tại của bài viết để trả về client hiển thị
    $current_terms = wp_get_object_terms( $post_id, $taxonomy, array( 'fields' => 'names' ) );
    $current_terms_str = ( ! is_wp_error( $current_terms ) && ! empty( $current_terms ) ) ? implode( ', ', $current_terms ) : __( '(Trống)', 'wp-acf-smart-importer' );

    wp_send_json_success( array(
        'message'   => __( 'Đã gán phân loại thành công.', 'wp-acf-smart-importer' ),
        'terms_str' => $current_terms_str, // Trả danh sách để JS cập nhật trực tiếp lên bảng quản trị
    ) );
}
```

---

### LUỒNG 9: CÀO BÀI VIẾT TỰ ĐỘNG (CLASSIC WEB SCRAPER FLOW)

Luồng này cho phép người dùng cào bài viết từ các trang web ngoài thông qua cấu hình bộ chọn (Selectors) CSS / XPath, tải về hình ảnh đại diện và chèn làm bài viết mới trong hệ thống WordPress.

#### Sơ đồ hoạt động:
*   **Đầu vào (Input)**:
    *   URL trang web cần cào: `https://example.com/some-article`
    *   Bộ chọn Tiêu đề (Title Selector): `h1`
    *   Bộ chọn Nội dung (Content Selector): `.entry-content`
    *   Bộ chọn Ảnh đại diện (Featured Image Selector): `meta[property="og:image"]`
    *   Bộ chọn phần tử muốn loại bỏ (Remove Selector): `.ads-wrapper, .related-posts`
    *   Post Type đích: `post` hoặc bất kỳ CPT nào.
    *   Trạng thái bài viết: `draft`, `publish` hoặc `pending`.
    *   Taxonomy và giá trị phân loại muốn gán.
*   **Xử lý (Processing)**:
    1.  **Cào xem trước (Preview)**:
        *   Client gửi AJAX `wpsai_scrape_preview` kèm theo URL và các bộ chọn.
        *   Backend tải HTML qua `wp_remote_get()` với tuỳ chọn tắt xác thực SSL trên localhost (`sslverify => false`).
        *   Sử dụng `DOMDocument` và `DOMXPath` của PHP để bóc tách thông tin.
        *   Hàm helper `css_to_xpath()` dịch các bộ chọn CSS cơ bản thành biểu thức XPath để truy vấn nhanh chóng.
        *   Cắt bỏ các nút không mong muốn dựa trên bộ chọn loại bỏ bằng hàm `removeChild()` trên cây DOM.
        *   Chuẩn hóa các đường dẫn ảnh tương đối thành đường dẫn tuyệt đối (Absolute URLs).
        *   Trả về kết quả xem trước trực quan dưới dạng JSON (Tiêu đề, ảnh đại diện, nội dung HTML làm sạch).
    2.  **Cào và đăng bài (Scrape & Import)**:
        *   Client gửi AJAX `wpsai_scrape_and_import` kèm thông số đích (Post Type, Post Status, Taxonomy, Terms).
        *   Backend cào dữ liệu và truyền trực tiếp kết quả vào Engine nhập liệu: `WP_ACF_Smart_Importer_Engine::import_single_row`.
        *   Engine tải ảnh đại diện từ URL tuyệt đối ngoài về máy chủ tạm thời, sideload vào Media Library của WordPress qua `media_handle_sideload` và gán làm thumbnail của bài viết.
        *   Engine gọi `handle_taxonomy_import` để phân tích đường dẫn phân cấp và gán các terms tương ứng cho bài viết mới.
*   **Đầu ra (Output)**: Tạo thành công bài viết WordPress hoàn chỉnh với đầy đủ tiêu đề, nội dung làm sạch, ảnh đại diện nội bộ, và gán phân loại chính xác.

---

### LUỒNG 10: TRÍCH XUẤT TIÊU ĐỀ, DỊCH THUẬT AI & CẬP NHẬT HÀNG LOẠT (POST TITLES EXTRACT, AI TRANSLATE & BULK REPLACE FLOW)

Luồng này cho phép người dùng trích xuất toàn bộ danh sách tiêu đề bài viết hiện có theo bộ lọc động, tích chọn các bài viết cụ thể, dịch tự động bằng AI Gemini sang ngôn ngữ đích mong muốn (với cơ chế tự phục hồi lỗi 404 và hiển thị lỗi trực quan), và thực hiện cập nhật hàng loạt tiêu đề đã dịch vào CSDL.

#### Sơ đồ hoạt động chi tiết:
*   **1. Quá trình Trích xuất (Extraction)**:
    - Người dùng chọn Post Type, Phân loại, Chuyên mục mục tiêu và nhấn nút lấy danh sách.
    - Client JS gửi yêu cầu AJAX `wpsai_get_post_titles` lên Backend.
    - Backend truy vấn Database qua `get_posts()` và trả về danh sách bài viết.
    - Client JS lưu thông tin bài viết vào biến cục bộ `currentExtractedPosts`, hiển thị bảng kết quả kèm cột checkbox lựa chọn và điền tiêu đề gốc vào textarea bên trái.
*   **2. Quá trình Lọc chọn & Dịch thuật AI (AI Translation)**:
    - Người dùng tích chọn các checkbox bài viết cần dịch, chọn ngôn ngữ đích (English, Japanese,...) và nhấn "Dịch Tiêu Đề Bằng AI".
    - Client JS gửi AJAX `wpsai_translate_post_titles` kèm mảng các tiêu đề được chọn lên Backend.
    - **Cơ chế gọi API Gemini tự phục hồi (Self-Healing Fallback)**:
      - Backend tuần tự duyệt qua các model và API endpoints khác nhau (`v1/models/gemini-1.5-flash`, `v1beta/models/gemini-1.5-flash`, `v1beta/models/gemini-1.5-flash-latest`,...) để phòng tránh lỗi 404 hoặc model bị deprecate.
      - Hệ thống tự động loại bỏ cấu hình `responseMimeType` trên endpoint `v1` (tránh lỗi `Unknown name` payload) và chỉ áp dụng cấu hình này trên `v1beta`.
    - **Hiển thị lỗi trực quan (Inline Error Logging)**:
      - Nếu tất cả các models/endpoints kết nối Gemini đều thất bại, Backend trả về chi tiết lỗi.
      - Client JS bắt lỗi và in trực tiếp ra khung thông báo `#wpsai-titles-translation-error` (màu đỏ, font monospace, scrollable) giúp người dùng dễ dàng theo dõi và sao chép lỗi thay vì dùng alert chặn màn hình.
    - Nếu dịch thành công, kết quả được điền trực tiếp vào textarea tiêu đề mới bên phải.
*   **3. Quá trình Đối chiếu & Xác thực (Real-time Validation)**:
    - Hệ thống đếm số dòng tiêu đề mới và so khớp với số lượng bài viết đang được tích chọn thời gian thực.
    - Hiển thị badge màu xanh **"Khớp số lượng"** nếu khớp và mở khóa nút Cập nhật; ngược lại hiển thị badge màu đỏ **"Chưa khớp"** và khóa nút.
*   **4. Quá trình Cập nhật hàng loạt (Batch Execution)**:
    - Client JS gửi yêu cầu AJAX `wpsai_update_post_title` đệ quy tuần tự cho từng bài viết được chọn.
    - Backend xác thực quyền và thực hiện `wp_update_post()` để lưu tiêu đề mới.
    - Live update tiêu đề mới lên bảng kết quả và highlight màu xanh lá cây dòng vừa lưu thành công.

