# ⚡ Trình Nhập Liệu ACF Thông Minh & AI Generator (WP Smart Auto-Importer)

Plugin chuyên dụng giúp tự động hóa 100% quy trình nhập liệu bài viết, tự sinh nội dung bằng Gemini AI, sideload hình ảnh minh họa từ URL ngoài và dịch thuật hàng loạt tiêu đề bài viết.

---

## 🌟 Tính Năng Nổi Bật

- **Schema Discovery Engine:** Tự động quét và phát hiện các nhóm trường ACF, Custom Meta Fields và Taxonomies của bài viết mẫu.
- **AI Content Generator (Gemini 1.5 Flash):** Sinh bài viết ảo đồng nhất ngữ nghĩa và tự tạo ảnh minh họa qua dịch vụ LoremFlickr.
- **Client-Side Batch Processing:** Xử lý nhập liệu tuần tự theo hàng đợi ở phía Client (JS) với độ trễ 150ms để chống tràn RAM server.
- **Hierarchical Taxonomy Creator:** Đệ quy tự động phân tách và khởi tạo cấu trúc danh mục nhiều cấp dạng `Cha > Con > Cháu`.
- **AI Titles Translator:** Quét danh sách bài viết theo chuyên mục, tích chọn và dịch thuật hàng loạt tiêu đề bằng AI Gemini.

---

## 📂 Cấu Trúc Tài Liệu

- 🖥️ [interactive_master_docs.html](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/trinh-nhap-lieu-acf-thong-minh/docs/interactive_master_docs.html) — **File Tài liệu Tổng HTML Tương tác** (Gồm Sơ đồ 7 bước SVG, Inspector Card & Modal Quản lý Phiên bản Releases v1.5.0/v1.2.0/v1.0.0).
- 📄 [specification.md](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/trinh-nhap-lieu-acf-thong-minh/docs/specification.md) — Quy chuẩn kỹ thuật các Core Classes, AJAX Handlers & Gemini REST API.
- 📄 [workflow.md](file:///d:/xampp/htdocs/11.%20BASE%20TEST%20CASE/wp-content/plugins/trinh-nhap-lieu-acf-thong-minh/docs/workflow.md) — Sơ đồ Mermaid luồng xử lý Schema Discovery, Batch Import & AI Title Translator.
