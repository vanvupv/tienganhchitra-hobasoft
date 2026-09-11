# TÀI LIỆU TỔNG QUAN DỰ ÁN (README.md)

**Tên Plugin**: WP Smart Auto-Importer & AI Generator  
**Thư mục**: `trinh-nhap-lieu-acf-thong-minh`  
**Text Domain**: `wp-acf-smart-importer`  
**Phiên bản hiện tại**: 1.0.0  

---

## 📌 MÔ TẢ

Plugin WordPress chuyên dụng giúp **quét cấu trúc trường bài viết** (WordPress Core + ACF + Custom Meta + Taxonomy), **nhập liệu hàng loạt** (từ Excel/JSON/HTML/URL), **sinh nội dung tự động** (Rule-based hoặc Google Gemini AI), và **quản lý kho dữ liệu mẫu** (Snapshot & Tree Repository).

---

## ⚙️ YÊU CẦU HỆ THỐNG

| Mục | Yêu cầu |
|---|---|
| PHP | >= 7.4 |
| WordPress | >= 5.9 |
| ACF (Advanced Custom Fields) | Bất kỳ phiên bản (Free hoặc Pro) — **không bắt buộc**, plugin tự fallback sang `get_post_meta()` |
| Gemini API Key | Cần thiết cho tính năng Sinh AI & Nhân Bản AI |
| Extension PHP | `json`, `mbstring`, `dom`, `libxml` |

---

## 🚀 DANH SÁCH TÍNH NĂNG NỔI BẬT

1. **Bảng Điều Khiển Chính**: Quét cấu trúc trường → Mapping cột → Nhập từ Excel/JSON.
2. **Sinh Dữ Liệu Ảo**: Rule-based (nhanh, offline) hoặc Gemini AI (chất lượng cao, viết tiếng Việt).
3. **Nhân Bản Hàng Loạt**: Chọn bài mẫu → AI viết lại nội dung mới → Import tự động.
4. **Cào Dữ Liệu Web**: Nhập URL + CSS Selector → Lấy Title/Content/Image tự động.
5. **Gán Ảnh Đại Diện Hàng Loạt**: Chọn ảnh từ Media Library → Gán cho nhiều bài cùng lúc.
6. **Xuất Excel & ZIP**: Trích xuất bài viết kèm ảnh đính kèm thành gói ZIP.
7. **Cấu Hình API Key**: Lưu Gemini API Key + Kiểm tra kết nối (latency).
8. **Kết Nối Chrome Extension**: REST API Bridge cho Extension cào bài ngoài.
9. **Tài Liệu Dự Án**: Nhật ký phát triển + Thư viện UI Components.
10. **Kho Dữ Liệu Mẫu**: Quét/Lưu/Khôi phục Snapshot + Cây phân cấp phân mảnh (Tree Repository).

---

## 📂 CẤU TRÚC THƯ MỤC

```text
trinh-nhap-lieu-acf-thong-minh/
├── .agent-trinh-nhap-lieu-acf-thong-minh/   # Tài liệu Agent (bạn đang đọc)
│   ├── README.md
│   ├── LUONG_XU_LY.md
│   ├── KIEN_TRUC_SYSTEM.md
│   ├── DATABASE_SCHEMA.md
│   ├── HIEU_SUAT_TOI_UU.md
│   └── HUONG_DAN_SU_DUNG.md
├── assets/
│   ├── css/admin-style.css                  # Giao diện Admin (Glassmorphism, Dark-mode cards)
│   └── js/admin-script.js                   # Frontend JS Controller (~6100 dòng)
├── docs/
│   ├── architecture-and-flows.md            # Kiến trúc & Luồng xử lý cũ
│   └── PROJECT_DOCUMENTATION.md
├── includes/
│   ├── class-wp-acf-smart-importer-admin.php      # Render giao diện 12 Tab Admin
│   ├── class-wp-acf-smart-importer-ajax.php       # 30+ AJAX endpoints & Security
│   ├── class-wp-acf-smart-importer-engine.php     # Động cơ Import (Insert/Update/Media/Taxonomy)
│   ├── class-wp-acf-smart-importer-generator.php  # Sinh dữ liệu Rule-based + Gemini AI API
│   ├── class-wp-acf-smart-importer-scraper.php    # Cào HTML (DOMDocument + XPath)
│   ├── class-wp-acf-smart-importer-rest.php       # REST API Bridge (Chrome Extension)
│   └── class-wp-acf-smart-importer-tree.php       # Kho Cây Phân Cấp (Manifest + Chunking)
└── trinh-nhap-lieu-acf-thong-minh.php             # File khởi tạo chính (Entry Point)
```
