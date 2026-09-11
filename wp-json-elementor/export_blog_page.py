import json
import zipfile
import os

def build_goongbe_blog_page():
    """
    Sinh mã JSON Elementor Pro 3.35 chuẩn cho TRANG BLOG & BÀI VIẾT GOONGBE (Blog Page):
    Thừa hưởng 100% màu sắc (#1B5B65, #009AA5, #E5F6F8), font Roboto từ Trang Chủ Chuẩn 1.
    Gồm 3 Section chuẩn:
    - Section 1: Hero Featured Post (Khối nội dung 2 cột: Tiêu đề, mô tả, nút & hình ảnh)
    - Section 2: Sub-Hero Featured Article (Khối nội dung 2 cột: Tiêu đề, mô tả, nút & hình ảnh)
    - Section 3: Danh sách bài viết Blogs (Widget Posts Grid 3 Cột: Hình ảnh, tiêu đề, ngày đăng)
    """

    # SECTION 1: Hero Featured Post (2 Cột)
    sec1_hero_blog = {
        "id": "sec_blog_hero",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_blog_hero_left",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 50, "_inline_size": 50, "content_position": "middle"},
                "elements": [
                    {
                        "id": "w_blog_hero_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "MẸO CHĂM SÓC DA BÉ",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 34},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto"
                        }
                    },
                    {
                        "id": "w_blog_hero_desc",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='color: #555; font-size: 16px; line-height: 1.7; margin: 15px 0 25px 0;'>Hướng dẫn từ các chuyên gia da liễu hàng đầu giúp mẹ xây dựng quy trình tắm và dưỡng ẩm dịu lành nhất cho bé yêu ngay từ những ngày đầu đời.</p>"
                        }
                    },
                    {
                        "id": "w_blog_hero_btn",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "XEM BÀI VIẾT",
                            "background_color": "#1B5B65",
                            "button_text_color": "#FFFFFF",
                            "border_radius": {"unit": "px", "top": "25", "right": "25", "bottom": "25", "left": "25", "isLinked": True},
                            "padding": {"unit": "px", "top": "12", "right": "30", "bottom": "12", "left": "30", "isLinked": False}
                        }
                    }
                ]
            },
            {
                "id": "col_blog_hero_right",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 50, "_inline_size": 50, "content_position": "middle"},
                "elements": [
                    {
                        "id": "w_blog_hero_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/GOONGBE-Cong-Bo-Dat-Chuan-Chung-Nhan-Dermatest-Muc-Cao-Nhat.jpg"},
                            "align": "center",
                            "border_radius": {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16"}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 2: Sub-Hero Featured Article (2 Cột)
    sec2_sub_blog = {
        "id": "sec_blog_sub_hero",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "50", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_blog_sub_left",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 50, "_inline_size": 50, "content_position": "middle"},
                "elements": [
                    {
                        "id": "w_blog_sub_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "BÍ QUYẾT CHỌN SẢN PHẨM AN TOÀN CHO TRẺ SƠ SINH",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 28},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto"
                        }
                    },
                    {
                        "id": "w_blog_sub_desc",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='color: #555; font-size: 15px; line-height: 1.7; margin: 15px 0 25px 0;'>Làn da trẻ sơ sinh mỏng hơn 30% so với người lớn. Khám phá lý do tại sao phức hợp thảo dược tự nhiên Oji Relief Complex™ là sự lựa chọn an toàn hàng đầu được bác sĩ khuyên dùng.</p>"
                        }
                    },
                    {
                        "id": "w_blog_sub_btn",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "ĐỌC NGAY",
                            "background_color": "#FFFFFF",
                            "button_text_color": "#1B5B65",
                            "border_border": "solid",
                            "border_color": "#1B5B65",
                            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1"},
                            "border_radius": {"unit": "px", "top": "25", "right": "25", "bottom": "25", "left": "25", "isLinked": True},
                            "padding": {"unit": "px", "top": "10", "right": "30", "bottom": "10", "left": "30", "isLinked": False}
                        }
                    }
                ]
            },
            {
                "id": "col_blog_sub_right",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 50, "_inline_size": 50, "content_position": "middle"},
                "elements": [
                    {
                        "id": "w_blog_sub_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/GOONGBE-Va-Hanh-Trinh-Nang-Chuan-Cham-Soc-Lan-Da-Tre-Em-Tai-Viet-Nam.jpg"},
                            "align": "center",
                            "border_radius": {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16"}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 3: Danh sách bài viết Blogs (Widget Posts Grid 3 Cột)
    sec3_posts_grid = {
        "id": "sec_blog_grid_catalog",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "50", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_blog_grid_main",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_blog_catalog_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "TẤT CẢ BÀI VIẾT & KINH NGHIỆM CHO MẸ",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 32},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "35", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": "w_blog_posts_widget",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "posts",
                        "settings": {
                            "classic_columns": "3",
                            "classic_show_read_more": "yes",
                            "read_more_text": "Đọc tiếp »",
                            "classic_meta_data": ["date", "comments"]
                        }
                    }
                ]
            }
        ]
    }

    content_sections = [
        sec1_hero_blog,
        sec2_sub_blog,
        sec3_posts_grid
    ]

    # Full Page JSON
    full_page = {
        "version": "3.0.0",
        "title": "Trang Tin Tức / Blog (Blog & Articles Page)",
        "type": "page",
        "elementor_version": "3.35.1",
        "content": content_sections,
        "page_settings": []
    }

    json_path = "wp-json-elementor/goongbe-page-blog.json"
    zip_path = "wp-json-elementor/goongbe-page-blog.zip"
    clipboard_path = "wp-json-elementor/goongbe-page-blog-clipboard.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_page, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_sections, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported Blog Page JSON: {json_path}")
    print(f"[SUCCESS] Exported Blog Page ZIP: {zip_path}")
    print(f"[SUCCESS] Exported Blog Page Clipboard: {clipboard_path}")

if __name__ == "__main__":
    build_goongbe_blog_page()
