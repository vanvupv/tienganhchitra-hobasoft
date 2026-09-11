import json
import zipfile
import os

def build_goongbe_about_page():
    """
    Sinh mã JSON Elementor Pro 3.35 chuẩn cho TRANG GIỚI THIỆU GOONGBE (About Us):
    Thừa hưởng 100% tông màu (#1B5B65, #009AA5, #E5F6F8), typography Roboto và layout từ Trang Chủ Chuẩn 1.
    Gồm 6 Section:
    - Section 1: Banner Full Width (80vh)
    - Section 2: Tiêu đề "VỀ GOONGBE" & Nội dung mô tả
    - Section 3: Khối Content (Câu chuyện Goongbe - Nội dung bên trái, Ảnh bên phải)
    - Section 4: Khối 3 Cột (3 Ảnh + Tiêu đề công thức khoa học)
    - Section 5: Khối Content nền xanh dịu #E5F6F8 (Thương hiệu được bác sĩ khuyên dùng)
    - Section 6: Khối Content (Thành phần Oji Relief Complex - Nội dung bên trái, Ảnh minh họa bên phải)
    """

    # SECTION 1: Banner Full Width
    sec1_banner = {
        "id": "sec_about_banner",
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "full_width",
            "stretch_section": "section-stretched",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [
            {
                "id": "col_banner",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "widget_about_slides",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "slides",
                        "settings": {
                            "slides_name": "Slides",
                            "slides": [
                                {
                                    "_id": "slide_about_1",
                                    "heading": "",
                                    "description": "",
                                    "button_text": "",
                                    "background_image": {
                                        "url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/Banner-1.jpg"
                                    }
                                }
                            ],
                            "slides_height": {"unit": "vh", "size": 75}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 2: Tiêu đề & Nội dung mô tả
    sec2_title_intro = {
        "id": "sec_about_title_intro",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "40", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_title_intro",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_about_heading_main",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "VỀ GOONGBE",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 34},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto"
                        }
                    },
                    {
                        "id": "w_about_intro_desc",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='text-align: center; color: #555; font-size: 16px; max-width: 860px; margin: 15px auto 0 auto; line-height: 1.6;'>Tại sao nên chọn Goongbe để chăm sóc làn da nhạy cảm của bé? Cùng khám phá lịch sử thương hiệu, các nghiên cứu khoa học đằng sau mỗi sản phẩm cũng như sự quan tâm, chăm sóc mà chúng tôi dành cho làn da nhạy cảm của bé.</p>"
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 3: Khối Content (Câu chuyện Goongbe - Nội dung trái, Ảnh phải)
    sec3_story = {
        "id": "sec_about_story",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "50", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_story_left",
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 50,
                    "_inline_size": 50,
                    "content_position": "middle"
                },
                "elements": [
                    {
                        "id": "w_story_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "CÂU CHUYỆN GOONGBE",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 28},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto"
                        }
                    },
                    {
                        "id": "w_story_desc",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='color: #555; font-size: 15px; line-height: 1.7; margin: 15px 0 25px 0;'>Trong suốt nhiều năm qua, GOONGBE luôn cam kết mang đến những giá trị tiến trình khoa học chăm sóc da dịu lành nhất cho trẻ sơ sinh và trẻ nhỏ. Chúng tôi cam kết sử dụng các chiết xuất thảo dược tự nhiên lành tính giúp bảo vệ làn da bé trước mọi tác động của môi trường.</p>"
                        }
                    },
                    {
                        "id": "w_story_btn",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "XEM THÊM",
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
                "id": "col_story_right",
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 50,
                    "_inline_size": 50,
                    "content_position": "middle"
                },
                "elements": [
                    {
                        "id": "w_story_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {
                                "url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/GOONGBE-Va-Hanh-Trinh-Nang-Chuan-Cham-Soc-Lan-Da-Tre-Em-Tai-Viet-Nam.jpg"
                            },
                            "align": "center",
                            "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12"}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 4: Khối 3 Hình ảnh + Tiêu đề
    sec4_three_cards = {
        "id": "sec_about_three_cards",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "40", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_card_1",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 33, "_inline_size": 33.33},
                "elements": [
                    {
                        "id": "w_card_1_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/section-2-anh-1.avif"},
                            "border_radius": {"unit": "px", "top": "10", "right": "10", "bottom": "10", "left": "10"}
                        }
                    },
                    {
                        "id": "w_card_1_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "CÔNG THỨC KHOA HỌC CHO DA NHẠY CẢM",
                            "header_size": "h4",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": "16"},
                            "typography_font_weight": "700",
                            "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        }
                    }
                ]
            },
            {
                "id": "col_card_2",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 33, "_inline_size": 33.33},
                "elements": [
                    {
                        "id": "w_card_2_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/section-2-anh-2.avif"},
                            "border_radius": {"unit": "px", "top": "10", "right": "10", "bottom": "10", "left": "10"}
                        }
                    },
                    {
                        "id": "w_card_2_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "CHUYÊN GIA VỀ DA NHẠY CẢM",
                            "header_size": "h4",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": "16"},
                            "typography_font_weight": "700",
                            "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        }
                    }
                ]
            },
            {
                "id": "col_card_3",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 33, "_inline_size": 33.33},
                "elements": [
                    {
                        "id": "w_card_3_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/section-2-anh-3.avif"},
                            "border_radius": {"unit": "px", "top": "10", "right": "10", "bottom": "10", "left": "10"}
                        }
                    },
                    {
                        "id": "w_card_3_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "5 DẤU HIỆU DA NHẠY CẢM BÉ YÊU",
                            "header_size": "h4",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": "16"},
                            "typography_font_weight": "700",
                            "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 5: Khối Content Nền Màu Khác (#E5F6F8 - Thương hiệu được bác sĩ khuyên dùng)
    sec5_pastel_bg = {
        "id": "sec_about_pastel_bg",
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": "#E5F6F8",
            "padding": {"unit": "px", "top": "70", "right": "50", "bottom": "70", "left": "50", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_pastel_left",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_pastel_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "#1 THƯƠNG HIỆU CHO DA NHẠY CẢM ĐƯỢC BÁC SĨ KHUYÊN DÙNG",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 28},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto"
                        }
                    },
                    {
                        "id": "w_pastel_desc",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='color: #444; font-size: 15px; line-height: 1.7; margin: 15px 0 25px 0; max-width: 900px;'>Chúng tôi luôn hợp tác chặt chẽ với các bác sĩ da liễu và chuyên gia chăm sóc sức khỏe để thực hiện hơn 550 nghiên cứu lâm sàng trên hơn 22.000 bệnh nhân nhằm đạt được tính hiệu quả và an toàn vượt trội cho sản phẩm chăm sóc da em bé. Đạt tiêu chuẩn kiểm nghiệm Dermatest Excellent mức cao nhất từ Đức.</p>"
                        }
                    },
                    {
                        "id": "w_pastel_btn",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "XEM THÊM",
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
            }
        ]
    }

    # SECTION 6: Khối Content (Thành phần Oji Relief Complex - Nội dung trái, Ảnh phải)
    sec6_ingredients = {
        "id": "sec_about_ingredients",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "70", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_ing_left",
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 50,
                    "_inline_size": 50,
                    "content_position": "middle"
                },
                "elements": [
                    {
                        "id": "w_ing_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "THÀNH PHẦN OJI RELIEF COMPLEX™",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 28},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto"
                        }
                    },
                    {
                        "id": "w_ing_desc",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='color: #555; font-size: 15px; line-height: 1.7; margin: 15px 0 25px 0;'>Phức hợp thảo dược 5 thành phần tự nhiên (Hydrating Glycerin, Niacinamide Vitamin B3, Panthenol Pro-Vitamin B5) giúp làm dịu tức thì làn da mẩn đỏ, tạo màng ẩm tự nhiên bảo vệ da bé khỏe mạnh suốt 72 giờ.</p>"
                        }
                    },
                    {
                        "id": "w_ing_btn",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "KHÁM PHÁ THÊM",
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
                "id": "col_ing_right",
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 50,
                    "_inline_size": 50,
                    "content_position": "middle"
                },
                "elements": [
                    {
                        "id": "w_ing_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {
                                "url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/May-1.avif"
                            },
                            "align": "center"
                        }
                    }
                ]
            }
        ]
    }

    content_sections = [
        sec1_banner,
        sec2_title_intro,
        sec3_story,
        sec4_three_cards,
        sec5_pastel_bg,
        sec6_ingredients
    ]

    # Full Page JSON
    full_page = {
        "version": "3.0.0",
        "title": "Trang Giới Thiệu GOONGBE (About Us)",
        "type": "page",
        "elementor_version": "3.35.1",
        "content": content_sections,
        "page_settings": []
    }

    json_path = "wp-json-elementor/goongbe-page-about-us.json"
    zip_path = "wp-json-elementor/goongbe-page-about-us.zip"
    clipboard_path = "wp-json-elementor/goongbe-page-about-us-clipboard.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_page, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_sections, f, ensure_ascii=False, indent=2)

    with open(zip_path, "w") as f:
        pass
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported About Page JSON: {json_path}")
    print(f"[SUCCESS] Exported About Page ZIP: {zip_path}")
    print(f"[SUCCESS] Exported About Page Clipboard: {clipboard_path}")

if __name__ == "__main__":
    build_goongbe_about_page()
