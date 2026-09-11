import json
import zipfile
import os

def build_goongbe_ingredients_page():
    """
    Sinh mã JSON Elementor Pro 3.35 chuẩn cho TRANG THÀNH PHẦN GOONGBE (Ingredients Page):
    Thừa hưởng 100% màu sắc (#1B5B65, #009AA5, #E5F6F8), font Roboto từ Trang Chủ Chuẩn 1.
    Gồm 4 Section chuẩn:
    - Section 1: Banner Image Full Width (60vh)
    - Section 2: CHĂM SÓC HOÀNG GIA CHO TẤT CẢ (Tiêu đề, mô tả, Widget Image & Commercial Video)
    - Section 3: Nguồn gốc Thảo Dược Hoàng Gia (Tiêu đề, Content & Gallery ảnh chậu tắm, hoa sen, bình gốm)
    - Section 4: Các thành phần chính của dòng sản phẩm em bé (Tiêu đề, mô tả, Slide 'Năm Cây' thảo dược, Đồ thị % kiểm nghiệm)
    """

    # SECTION 1: Banner Image Full Width
    sec1_banner = {
        "id": "sec_ing_banner",
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "full_width",
            "stretch_section": "section-stretched",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [
            {
                "id": "col_ing_banner",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_ing_slides",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "slides",
                        "settings": {
                            "slides_name": "Slides",
                            "slides": [
                                {
                                    "_id": "slide_ing_1",
                                    "heading": "",
                                    "description": "",
                                    "button_text": "",
                                    "background_image": {
                                        "url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/Banner-1.jpg"
                                    }
                                }
                            ],
                            "slides_height": {"unit": "vh", "size": 60}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 2: CHĂM SÓC HOÀNG GIA CHO TẤT CẢ (Tiêu đề, Mô tả, Widget Image & Commercial Video)
    sec2_royal_care = {
        "id": "sec_ing_royal_care",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_royal_care_main",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_royal_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "CHĂM SÓC HOÀNG GIA CHO TẤT CẢ",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 34},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto"
                        }
                    },
                    {
                        "id": "w_royal_desc",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='text-align: center; color: #555; font-size: 16px; max-width: 860px; margin: 15px auto 30px auto; line-height: 1.6;'>Phương pháp tắm thảo dược Oji-tang được sử dụng để chăm sóc làn da của các hoàng tử triều đại Joseon. GOONGBE kế thừa và nâng tầm thành phức hợp Royal TheraTea Guard™ dịu lành nhất cho trẻ sơ sinh và trẻ nhỏ.</p>"
                        }
                    },
                    {
                        "id": "w_royal_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/GOONGBE-Va-Hanh-Trinh-Nang-Chuan-Cham-Soc-Lan-Da-Tre-Em-Tai-Viet-Nam.jpg"},
                            "align": "center",
                            "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12"},
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "30", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": "w_royal_video",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "video",
                        "settings": {
                            "video_type": "hosted",
                            "hosted_url": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/file.mp4"},
                            "autoplay": "yes",
                            "loop": "yes"
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 3: Nguồn Gốc Thảo Dược Hoàng Gia (Tiêu đề, Content & Gallery Ảnh)
    sec3_origin = {
        "id": "sec_ing_origin",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_origin_main",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_origin_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "NGUỒN GỐC",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 32},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": "w_origin_img_bath",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/OUR-STORY_2.jpg"},
                            "align": "center",
                            "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12"},
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": "w_origin_content",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='color: #444; font-size: 15px; line-height: 1.8; max-width: 900px; margin: 0 auto 30px auto;'>Nguồn gốc của Oji Relief Complex™ bắt đầu từ cuốn sách y học cổ truyền Joseon 'Đông Y Bảo Giám'. Nước tắm Oji-tang được đun từ 5 loại cây thảo dược quý hiếm giúp hạ nhiệt làn da mẫn cảm và nuôi dưỡng màng ẩm mịn màng cho các nguyên tử hoàng tộc Hàn Quốc.</p>"
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 4: Các Thành Phần Chính Của Dòng Sản Phẩm Em Bé (Tiêu đề, Slide "Năm Cây", Đồ thị % kiểm nghiệm)
    sec4_five_herbs = {
        "id": "sec_ing_five_herbs",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_herbs_main",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_herbs_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Các thành phần chính của dòng sản phẩm dành cho em bé",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 30},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "20", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": "w_herbs_desc",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='text-align: center; color: #666; font-size: 15px; max-width: 860px; margin: 0 auto 30px auto;'>Phức hợp 5 loại thảo dược thiên nhiên Oji Relief Complex™ nhẹ nhàng xoa dịu làn da mẫn cảm của em bé:</p>"
                        }
                    },
                    # SLIDE / CAROUSEL "NĂM CÂY" THẢO DƯỢC
                    {
                        "id": "w_herbs_carousel",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "media-carousel",
                        "settings": {
                            "slides_per_view": "3",
                            "slides": [
                                {"title": "Lá đào - Làm dịu mẩn đỏ", "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/section-2-anh-1-1.avif"}},
                                {"title": "Cây liễu trắng - Giảm ngứa rát", "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/section-2-anh-2-1.avif"}},
                                {"title": "Cây hòe - Kháng khuẩn tự nhiên", "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/section-2-anh-3-1.avif"}},
                                {"title": "Lá dâu tằm - Tăng cường độ ẩm", "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/May-1.avif"}}
                            ]
                        }
                    },
                    # ĐỒ THỊ KẾT QUẢ KIỂM NGHIỆM % HẠ NHIỆT & TĂNG ĐỘ ẨM
                    {
                        "id": "w_herbs_chart_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/Science-based-skincare_3.jpg"},
                            "align": "center",
                            "margin": {"unit": "px", "top": "35", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        }
                    }
                ]
            }
        ]
    }

    content_sections = [
        sec1_banner,
        sec2_royal_care,
        sec3_origin,
        sec4_five_herbs
    ]

    # Full Page JSON
    full_page = {
        "version": "3.0.0",
        "title": "Trang Thành Phần GOONGBE (Ingredients Page)",
        "type": "page",
        "elementor_version": "3.35.1",
        "content": content_sections,
        "page_settings": []
    }

    json_path = "wp-json-elementor/goongbe-page-ingredients.json"
    zip_path = "wp-json-elementor/goongbe-page-ingredients.zip"
    clipboard_path = "wp-json-elementor/goongbe-page-ingredients-clipboard.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_page, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_sections, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported Ingredients Page JSON: {json_path}")
    print(f"[SUCCESS] Exported Ingredients Page ZIP: {zip_path}")
    print(f"[SUCCESS] Exported Ingredients Page Clipboard: {clipboard_path}")

if __name__ == "__main__":
    build_goongbe_ingredients_page()
