# HƯỚNG DẪN SỬ DỤNG CHI TIẾT (HUONG_DAN_SU_DUNG.md)

Tài liệu hướng dẫn **từng bước thao tác** cho mỗi chức năng trong plugin, kèm ví dụ thực tế.

---

## 📋 MỤC LỤC

1. [Bảng Điều Khiển Nhập Liệu](#-1-bảng-điều-khiển-nhập-liệu)
2. [Thêm Ảnh Hàng Loạt](#-2-thêm-ảnh-hàng-loạt)
3. [Nhập Excel Hàng Loạt](#-3-nhập-excel-hàng-loạt)
4. [Gán Phân Loại Hàng Loạt](#-4-gán-phân-loại-hàng-loạt)
5. [Xuất Dữ Liệu](#-5-xuất-dữ-liệu-excel--zip)
6. [Lấy Tiêu Đề Bài Viết](#-6-lấy-tiêu-đề-bài-viết)
7. [Nhân Bản Hàng Loạt](#-7-nhân-bản-hàng-loạt)
8. [Cào Bài Viết (URL)](#-8-cào-bài-viết-từ-url)
9. [Cào HTML Offline](#-9-cào-html-offline)
10. [Tạo Nội Dung AI](#-10-tạo-nội-dung-ai-gemini)
11. [Cấu Hình API Key](#-11-cấu-hình-api-key)
12. [Tài Liệu Dự Án](#-12-tài-liệu-dự-án)
13. [Kho Dữ Liệu Mẫu](#-13-kho-dữ-liệu-mẫu-snapshot--tree)

---

## 📊 1. BẢNG ĐIỀU KHIỂN NHẬP LIỆU

> **Tab**: `Bảng Điều Khiển Nhập Liệu` (tab mặc định khi mở plugin)

### Mục đích
Quét cấu trúc trường của 1 bài viết có sẵn, sau đó nhập dữ liệu mới từ Excel/JSON bằng cách mapping cột vào trường.

### Ví dụ thực tế
**Kịch bản**: Bạn có file Excel 50 sản phẩm bất động sản, mỗi dòng gồm: Tên, Giá, Diện tích, Địa chỉ, Ảnh. Website dùng ACF để lưu "Giá bán" (`gia_ban`), "Diện tích" (`dien_tich`).

### Các bước thao tác

**Bước 1 — Chọn bài mẫu để quét cấu trúc trường**

1. Mở menu **Smart Importer** trên sidebar WordPress Admin.
2. Tại ô **"Chọn Post Type"** → Chọn `Sản phẩm (product)`.
3. Hệ thống tự tải danh sách bài viết thuộc post type đó.
4. Tại ô **"Chọn Bài Viết"** → Chọn 1 bài viết bất kỳ đã có (ví dụ: "Căn hộ mẫu Quận 7").
5. Bấm nút **"Quét Cấu Trúc Trường"**.

> **Kết quả**: Bảng hiển thị danh sách trường đã phát hiện, ví dụ:
>
> | # | Tên trường | Nhãn | Loại | Giá trị hiện tại |
> |---|---|---|---|---|
> | 1 | `post_title` | Tiêu đề bài viết | wp_core | Căn hộ mẫu Quận 7 |
> | 2 | `post_content` | Nội dung chi tiết | wp_core | `<p>Căn hộ cao cấp...</p>` |
> | 3 | `featured_image` | Ảnh đại diện | wp_core | `https://...image.jpg` |
> | 4 | `acf_gia_ban` | [ACF] Giá bán | acf_number | 5000000000 |
> | 5 | `acf_dien_tich` | [ACF] Diện tích | acf_number | 85 |
> | 6 | `tax_product_cat` | [Taxonomy] Danh mục | taxonomy | Bất động sản > Chung cư |

**Bước 2 — Tải lên file dữ liệu**

1. Bấm nút **"Tải lên file Excel/JSON"** hoặc kéo thả file.
2. Plugin đọc file tại trình duyệt (không upload lên server).
3. Bảng preview hiển thị các cột và dữ liệu trong file.

> **Lưu ý**: Plugin hỗ trợ `.xlsx`, `.xls`, `.csv`, `.json`.

**Bước 3 — Mapping cột**

1. Với mỗi cột trong file Excel, chọn trường đích tương ứng trong dropdown.
2. Ví dụ mapping:
   - Cột A `"Tên sản phẩm"` → `post_title`
   - Cột B `"Mô tả"` → `post_content`
   - Cột C `"Giá"` → `acf_gia_ban`
   - Cột D `"Diện tích"` → `acf_dien_tich`
   - Cột E `"Link ảnh"` → `featured_image`
   - Cột F `"Chuyên mục"` → `tax_product_cat`

**Bước 4 — Nhập dữ liệu**

1. Chọn **Trạng thái bài viết**: `Bản nháp (Draft)` hoặc `Xuất bản (Publish)`.
2. Bấm **"Bắt Đầu Nhập Liệu"**.
3. Progress bar chạy từng dòng: `Đang nhập dòng 1/50...`
4. Mỗi dòng thành công → Hiển thị link xem bài viết.
5. Hoàn tất → Thông báo: `✓ Đã nhập thành công 50/50 bài viết`.

> **Mẹo**: Nếu cột `Chuyên mục` chứa giá trị `"Bất động sản > Chung cư"`, plugin tự động tạo danh mục cha "Bất động sản" và con "Chung cư" nếu chưa tồn tại.

---

## 🖼️ 2. THÊM ẢNH HÀNG LOẠT

> **Tab**: `Thêm Ảnh Hàng Loạt`

### Mục đích
Gán ảnh đại diện (Featured Image) cho nhiều bài viết cùng lúc từ Media Library.

### Các bước thao tác

1. Chọn **Post Type** (ví dụ: `Bài viết (post)`).
2. Bấm **"Tải Danh Sách Bài Viết"**.
3. Bảng hiển thị toàn bộ bài viết kèm ảnh thumbnail hiện tại:

   > | # | Tiêu đề | Ảnh hiện tại | Hành động |
   > |---|---|---|---|
   > | 1 | Tin tức hôm nay | *(trống)* | [Chọn ảnh] [Xóa] |
   > | 2 | Đánh giá sản phẩm | 🖼️ | [Đổi ảnh] [Xóa] |

4. Bấm **"Chọn ảnh"** → Mở WordPress Media Library popup.
5. Chọn ảnh → Bấm **"Sử dụng ảnh này"**.
6. Ảnh được gán ngay lập tức, thumbnail cập nhật real-time trên bảng.

> **Mẹo**: Bạn có thể upload ảnh mới trực tiếp trong Media Library popup.

---

## 📑 3. NHẬP EXCEL HÀNG LOẠT

> **Tab**: `Nhập Excel Hàng Loạt`

### Mục đích
Nhập nhanh bài viết từ file Excel mà không cần quét cấu trúc trường trước (chế độ đơn giản hóa).

### Ví dụ thực tế
**Kịch bản**: Bạn có file CSV chứa 100 tin tức, cột: Title, Content, Category.

### Các bước thao tác

1. Chọn **Post Type** → `Bài viết (post)`.
2. Kéo thả file Excel vào vùng upload.
3. Plugin hiển thị preview 5 dòng đầu tiên.
4. Mapping tự động dựa trên tên cột (nếu trùng tên trường → auto-map).
5. Bấm **"Nhập Tất Cả"** → Chạy tuần tự từng dòng.

---

## 🏷️ 4. GÁN PHÂN LOẠI HÀNG LOẠT

> **Tab**: `Gán Phân Loại Hàng Loạt`

### Mục đích
Gán Category/Tag/Custom Taxonomy cho nhiều bài viết cùng lúc mà không cần mở từng bài.

### Ví dụ thực tế
**Kịch bản**: Bạn vừa import 50 bài viết nhưng quên gán chuyên mục. Giờ muốn gán tất cả vào `"Tin tức > Thời sự"`.

### Các bước thao tác

1. Chọn **Post Type** → `Bài viết (post)`.
2. Chọn **Taxonomy** → `Chuyên mục (category)`.
3. Nhập đường dẫn phân cấp: `Tin tức > Thời sự`.
4. Tick chọn các bài viết muốn gán (hoặc bấm "Chọn tất cả").
5. Bấm **"Gán Phân Loại"**.

> **Lưu ý về cú pháp**:
> - Phân cấp dùng dấu `>`: `"Cha > Con > Cháu"`
> - Nhiều đường dẫn dùng dấu `,`: `"Tin tức > Xã hội, Du lịch > Ẩm thực"`
> - Nếu chuyên mục chưa tồn tại → Tự động tạo mới.

---

## 📤 5. XUẤT DỮ LIỆU (EXCEL + ZIP)

> **Tab**: `Xuất Dữ Liệu`

### Mục đích
Trích xuất bài viết ra file Excel, đóng gói kèm ảnh đính kèm thành file ZIP.

### Ví dụ thực tế
**Kịch bản**: Bạn muốn backup 20 sản phẩm kèm ảnh đại diện và ảnh ACF gallery để di chuyển sang website khác.

### Các bước thao tác

1. Chọn **Post Type** → `Sản phẩm (product)`.
2. Bấm **"Tải Danh Sách"** → Bảng hiện toàn bộ sản phẩm.
3. Tick chọn các sản phẩm muốn xuất (hoặc "Chọn tất cả").
4. Tick chọn các trường muốn xuất:
   - ☑ `post_title` — Tiêu đề
   - ☑ `post_content` — Nội dung
   - ☑ `featured_image` — Ảnh đại diện
   - ☑ `acf_gia_ban` — Giá bán
   - ☑ `acf_gallery` — Bộ sưu tập ảnh
5. Bấm **"Xuất Excel + ZIP"**.
6. Trình duyệt tự động tải file `export_product_2026-08-06.zip` chứa:
   ```
   export.zip/
   ├── data.xlsx          # File Excel chứa dữ liệu
   └── images/
       ├── 101_featured_can-ho.jpg
       ├── 101_acf_gallery_anh1.jpg
       └── 102_featured_biet-thu.jpg
   ```

> **Lưu ý**: Trong file Excel, cột ảnh sẽ ghi đường dẫn tương đối `images/101_featured_can-ho.jpg` để khi import lại có thể tìm ảnh trong ZIP.

---

## 📝 6. LẤY TIÊU ĐỀ BÀI VIẾT

> **Tab**: `Lấy Tiêu Đề Bài Viết`

### Mục đích
Trích xuất nhanh danh sách tiêu đề của tất cả bài viết trong 1 Post Type để sao chép hoặc xuất file.

### Các bước thao tác

1. Chọn **Post Type** → `Bài viết (post)`.
2. Bấm **"Lấy Danh Sách Tiêu Đề"**.
3. Bảng hiển thị: ID | Tiêu đề | Ngày đăng | Link.
4. Bấm **"Sao chép tất cả"** → Copy danh sách tiêu đề vào clipboard.
5. Hoặc bấm **"Xuất Excel"** để tải file.

> **Ứng dụng**: Dùng để kiểm tra trùng lặp tiêu đề, hoặc tạo danh sách tiêu đề gửi cho AI viết lại nội dung.

---

## 🔁 7. NHÂN BẢN HÀNG LOẠT

> **Tab**: `Nhân Bản Hàng Loạt`

### Mục đích
Chọn 1 bài viết chuẩn → Plugin sinh ra N bản sao với nội dung được viết lại bởi AI hoặc quy tắc.

### Ví dụ thực tế
**Kịch bản**: Bạn có 1 bài viết mẫu "Căn hộ Saigon Pearl 3 phòng ngủ" rất hoàn chỉnh. Muốn tạo thêm 10 bài viết tương tự cho các dự án khác, giữ nguyên cấu trúc ACF nhưng nội dung viết lại hoàn toàn.

### Các bước thao tác

1. Chọn **Post Type** → `Bài viết (post)`.
2. Chọn **Bài viết mẫu** → `"Căn hộ Saigon Pearl 3 phòng ngủ" (ID: 819)`.
3. Bấm **"Quét Cấu Trúc Trường"**.
   > Kết quả: `✓ Đã phát hiện 35 trường dữ liệu cần nhân bản.`
4. Nhập **Số lượng bản sao**: `10`.
5. Chọn **Chế độ sinh**:
   - `Quy tắc (Rule)`: Nhanh, offline, chỉ thêm hậu tố `(Mẫu #1)` vào tiêu đề.
   - `AI (Gemini)`: Viết lại hoàn toàn nội dung, tiêu đề, mô tả bằng tiếng Việt.
6. Nếu chọn AI → Bấm **"Sinh Dữ Liệu"**.
   > Kết quả: Bảng preview 10 bản ghi mới với nội dung AI viết lại.
7. Kiểm tra dữ liệu preview → Bấm **"Nhập Tất Cả"**.
8. Progress bar chạy: `Đang nhập bản sao 1/10... 2/10...`
9. Hoàn tất → 10 bài viết mới xuất hiện trong Dashboard WordPress.

> **Lưu ý**: Chế độ AI yêu cầu **Gemini API Key** đã được cấu hình trong tab Cấu Hình.

---

## 🌐 8. CÀO BÀI VIẾT TỪ URL

> **Tab**: `Cào Bài Viết`

### Mục đích
Nhập URL trang web bất kỳ → Plugin tự động bóc tách tiêu đề, nội dung, ảnh đại diện → Import thành bài viết WordPress.

### Ví dụ thực tế
**Kịch bản**: Bạn muốn lấy bài viết từ trang `https://example.com/bai-viet/tin-tuc-hom-nay`.

### Các bước thao tác

1. Nhập **URL**: `https://example.com/bai-viet/tin-tuc-hom-nay`
2. Nhập **CSS Selectors** (hoặc XPath):
   - **Tiêu đề**: `h1.entry-title` *(lấy text của thẻ h1 class entry-title)*
   - **Nội dung**: `.entry-content` *(lấy HTML bên trong div class entry-content)*
   - **Ảnh đại diện**: `meta[property="og:image"]` *(lấy ảnh Open Graph)*
   - **Loại bỏ** *(tùy chọn)*: `.related-posts, .ads-banner` *(xóa quảng cáo, bài liên quan)*
3. Bấm **"Cào Dữ Liệu"**.
4. Kết quả preview:

   > | Trường | Giá trị bóc tách |
   > |---|---|
   > | Tiêu đề | Tin tức nổi bật hôm nay: Thị trường biến động... |
   > | Nội dung | `<p>Theo thông tin từ...</p><p>Chuyên gia nhận định...</p>` |
   > | Ảnh | `https://example.com/uploads/tin-tuc.jpg` |

5. Bấm **"Import vào WordPress"** → Chọn Post Type + Trạng thái.
6. Bài viết được tạo với nội dung đã cào.

> **Mẹo về CSS Selector**:
> - `.ten-class` → Tìm phần tử theo class
> - `#ten-id` → Tìm phần tử theo ID
> - `div.content p` → Tìm thẻ p bên trong div.content
> - Nếu bắt đầu bằng `/` → Plugin hiểu là XPath thô: `//div[@class="content"]//h1`

---

## 📄 9. CÀO HTML OFFLINE

> **Tab**: `Cào HTML Offline`

### Mục đích
Tương tự cào URL nhưng dành cho file HTML lưu sẵn trên máy (đã tải về).

### Các bước thao tác

1. Bấm **"Tải lên File HTML"** hoặc kéo thả file `.html`.
2. Nhập CSS Selectors cho tiêu đề, nội dung, ảnh (giống tab Cào URL).
3. Bấm **"Phân Tích HTML"**.
4. Preview kết quả → Bấm **"Import"** để lưu bài viết.

> **Ứng dụng**: Hữu ích khi trang web yêu cầu đăng nhập hoặc dùng JavaScript render nội dung — bạn mở trang trên Chrome, Save As HTML, rồi import file đó.

---

## 🤖 10. TẠO NỘI DUNG AI (GEMINI)

> **Tab**: `Tạo Nội Dung AI`

### Mục đích
Sinh hàng loạt bài viết mới hoàn toàn bằng AI, không cần bài mẫu, chỉ cần mô tả chủ đề.

### Ví dụ thực tế
**Kịch bản**: Bạn muốn tạo 5 bài viết về chủ đề "Ẩm thực đường phố Sài Gòn" cho blog du lịch.

### Các bước thao tác

1. Chọn **Post Type** → `Bài viết (post)`.
2. Nhập **Chủ đề**: `Ẩm thực đường phố Sài Gòn — các món ăn vặt nổi tiếng`.
3. Nhập **Số lượng**: `5`.
4. *(Tùy chọn)* Nhập danh sách **Tiêu đề tùy chỉnh**:
   ```
   Top 10 món ăn vặt Sài Gòn không thể bỏ lỡ
   Hành trình khám phá xe hủ tiếu gõ lúc nửa đêm
   Bánh tráng trộn Sài Gòn - Từ vỉa hè tới thương hiệu
   Cơm tấm Sài Gòn: Bí quyết sườn nướng than hồng
   Phở Sài Gòn vs Phở Hà Nội - Cuộc chiến vị giác
   ```
5. *(Tùy chọn)* Nhập **Layout bố cục nội dung**:
   ```
   ## Giới thiệu chung
   ## Nguồn gốc & Lịch sử
   ## Nguyên liệu & Cách chế biến
   ## Địa chỉ nổi tiếng
   ## Mức giá tham khảo
   ## Kết luận
   ```
6. Bấm **"Sinh Nội Dung AI"**.
7. Chờ 10-30 giây → AI trả về 5 bài viết hoàn chỉnh (tiếng Việt).
8. Preview bảng dữ liệu → Kiểm tra nội dung.
9. Bấm **"Nhập Tất Cả Vào WordPress"** → 5 bài viết được tạo.

> **Lưu ý quan trọng**:
> - Nếu bạn cung cấp **Tiêu đề tùy chỉnh**, AI sẽ giữ nguyên 100% tiêu đề bạn nhập, chỉ viết nội dung.
> - Nếu bạn cung cấp **Layout bố cục**, AI viết theo đúng đề mục đó.
> - Trường ảnh: AI sinh mô tả tiếng Anh (ví dụ: `"vietnamese street food pho"`) → Plugin tự chuyển thành URL ảnh stock thật.

---

## ⚙️ 11. CẤU HÌNH API KEY

> **Tab**: `Cấu Hình API Key`

### Mục đích
Lưu trữ Gemini API Key và kiểm tra kết nối.

### Các bước thao tác

1. Truy cập [Google AI Studio](https://aistudio.google.com/apikey) để lấy API Key.
2. Dán key vào ô **"Gemini API Key"**.
3. Bấm **"Kiểm Tra Kết Nối"**.
4. Kết quả:
   - ✅ `Kết nối API Gemini THÀNH CÔNG! — Latency: 450ms`
   - ❌ `Kiểm tra API thất bại: Invalid API key`
5. Bấm **"Lưu Cài Đặt"** để lưu key.

> **Mẹo**: Key miễn phí của Google có giới hạn 15 request/phút. Nếu gặp lỗi Rate Limit, đợi 1 phút rồi thử lại.

---

## 📚 12. TÀI LIỆU DỰ ÁN

> **Tab**: `Tài Liệu Dự Án`

### Mục đích
Ghi chép nhật ký phát triển, quản lý UI Components, đồng bộ tệp dự án.

### Chức năng chính
- **Nhật ký phát triển**: Ghi chú nhanh các thay đổi, quyết định kỹ thuật.
- **Thư viện UI Components**: Danh sách component có sẵn (buttons, cards, modals...) với sandbox chạy thử.
- **Xuất/Nhập tài liệu**: Backup tài liệu dự án dưới dạng JSON.

---

## 📦 13. KHO DỮ LIỆU MẪU (SNAPSHOT + TREE)

> **Tab**: `Kho Dữ Liệu Mẫu`

### Mục đích
Quét toàn bộ bài viết hiện có → Lưu thành bản sao lưu (Snapshot) → Tái sử dụng hoặc khôi phục bất kỳ lúc nào.

---

### 13.1 Quét & Lưu Snapshot

**Kịch bản**: Bạn muốn backup 45 sản phẩm bất động sản trước khi chỉnh sửa hàng loạt.

1. Chọn **Post Type** → `Sản phẩm (product)`.
2. *(Tùy chọn)* Lọc Taxonomy → `Danh mục sản phẩm` → `Bất Động Sản`.
3. Bấm **"Quét Toàn Bộ Dữ Liệu"**.
4. Thống kê hiển thị:

   > | Bài viết | Trường dữ liệu | Dung lượng |
   > |:---:|:---:|:---:|
   > | **45** | **12** | **128 KB** |

5. Bảng preview hiển thị 10 dòng đầu (ID, Tiêu đề, Trạng thái, Ngày đăng, 2 trường ACF đầu tiên).
6. Nhập tên: `Backup BĐS tháng 8-2026`.
7. Bấm **"Lưu Vào Kho"**.
8. Thông báo: `✓ Đã lưu snapshot thành công.`

---

### 13.2 Xem & Quản Lý Snapshot Đã Lưu

Bảng **Kho Lưu Trữ Snapshot** hiển thị:

> | # | Tên | Post Type | Bài viết | Dung lượng | Ngày tạo | Hành động |
> |---|---|---|:---:|---|---|---|
> | 1 | Backup BĐS tháng 8 | product | 45 | 128 KB | 2026-08-06 | [Xem] [Xóa] |
> | 2 | Tin tức tuần 31 | post | 20 | 45 KB | 2026-08-01 | [Xem] [Xóa] |

**Các hành động**:
- **Xem**: Mở bảng chi tiết toàn bộ bài viết trong snapshot.
- **Khôi phục**: Chọn chế độ → Import lại toàn bộ bài viết.
- **Xuất JSON**: Tải file snapshot về máy tính.
- **Xóa**: Xóa vĩnh viễn file snapshot khỏi server.

---

### 13.3 Khôi Phục Snapshot

1. Bấm **"Xem"** trên snapshot cần khôi phục.
2. Bảng chi tiết hiển thị toàn bộ bài viết + giá trị trường.
3. Chọn chế độ khôi phục:
   - **"Tạo bài viết mới"**: Tạo bài viết mới hoàn toàn, không ảnh hưởng bài cũ.
   - **"Ghi đè bài viết cũ (theo post_id)"**: Cập nhật bài viết cũ nếu ID trùng.
4. Bấm **"Khôi Phục Tất Cả"** → Xác nhận popup.
5. Progress bar chạy:
   ```
   ✓ Căn hộ Saigon Pearl (ID: 101)
   ✓ Biệt thự Thảo Điền (ID: 102)
   ✓ Đất nền Long An (ID: 103)
   ...
   ✓ Hoàn tất! Thành công: 45, Lỗi: 0
   ```

---

### 13.4 Cây Phân Loại Kho Dữ Liệu (Tree Repository)

Card **"Cây Phân Loại Kho Dữ Liệu"** hiển thị cấu trúc cây phân cấp:

```
📁 Sản phẩm (product)              120 bài    [Quét Nút Này]
  ├── 📂 Danh mục sản phẩm (product_cat)
  │    ├── 🏷️ Bất Động Sản           30 bài    [Quét Nút Này]
  │    ├── 🏷️ Thiết Bị Điện Tử       45 bài    [Quét Nút Này]
  │    └── 🏷️ Nội Thất               25 bài    [Quét Nút Này]
📁 Bài viết (post)                   80 bài    [Quét Nút Này]
  ├── 📂 Chuyên mục (category)
  │    ├── 🏷️ Tin tức                 50 bài
  │    └── 🏷️ Kinh doanh             30 bài
⚙️ Luồng Xử Lý & Prompt AI Mẫu
  ├── 📄 Prompt Sinh Bài BĐS
  └── 📄 Prompt Mô Tả Sản Phẩm SEO
```

**Cách sử dụng**:
1. Bấm vào mũi tên ▶ để **mở rộng** nhánh con.
2. Bấm **"Quét Nút Này"** trên bất kỳ nút nào → Plugin quét riêng bài viết thuộc danh mục đó.
3. Dữ liệu tự động chia thành file chunk nhỏ (≤ 50 bài/file).
4. Badge hiển thị số chunk đã lưu: `2 chunk(s)`.
5. Bấm **"Cập Nhật Cây Chỉ Mục"** để refresh toàn bộ cây.

> **Ưu điểm so với Snapshot**: Tree Repository phân mảnh dữ liệu theo danh mục, giúp quản lý kho mẫu **quy mô lớn** (hàng ngàn bài viết) mà không bị timeout hay tràn RAM.

---

## ❓ CÂU HỎI THƯỜNG GẶP (FAQ)

### Q: Plugin có bắt buộc cài ACF không?
**A**: Không. Plugin hoạt động bình thường với trường WordPress Core (title, content, excerpt). Nếu có ACF, plugin tự nhận diện và hỗ trợ tất cả loại trường ACF.

### Q: Tại sao sinh AI bị lỗi timeout?
**A**: Gemini API cần thời gian xử lý (10-90 giây). Plugin đã tăng timeout lên 90s. Nếu vẫn lỗi:
1. Kiểm tra API Key còn quota.
2. Giảm số lượng bài viết sinh mỗi lượt (khuyến nghị ≤ 10).
3. Kiểm tra kết nối internet server.

### Q: Dữ liệu snapshot lưu ở đâu?
**A**: File JSON lưu tại `wp-content/uploads/wpsai-snapshots/` (Snapshot đơn) và `wp-content/uploads/wpsai-tree-repository/` (Tree). Thư mục được bảo vệ bằng `.htaccess` (Deny from all).

### Q: Cào web có lấy được trang SPA (React/Vue) không?
**A**: Không trực tiếp. Plugin dùng `wp_remote_get()` lấy HTML tĩnh, không chạy JavaScript. Với trang SPA, hãy dùng tab **"Cào HTML Offline"**: Mở trang trên Chrome → Save As HTML → Upload file đó.

### Q: Có thể import lại file ZIP đã xuất không?
**A**: Có. Giải nén ZIP, lấy file `data.xlsx`, upload vào tab **"Bảng Điều Khiển Nhập Liệu"**, mapping cột và import. Ảnh trong thư mục `images/` cần upload lên Media Library trước hoặc host trên server.
