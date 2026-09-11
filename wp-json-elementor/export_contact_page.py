import json
import zipfile
import os

def build_goongbe_contact_page():
    """
    Sinh mã JSON Elementor Pro 3.35 chuẩn cho TRANG LIÊN HỆ GOONGBE VIỆT NAM (Contact Us Page):
    Thừa hưởng 100% màu sắc (#1B5B65, #009AA5, #E5F6F8), font Roboto từ Trang Chủ Chuẩn 1.
    Gồm 5 Section chuẩn:
    - Section 1: Banner Top (Tiêu đề 'Liên Hệ' & Ảnh nền hero)
    - Section 2: Bản đồ định vị (Widget Google Maps)
    - Section 3: Đoạn văn mô tả thông tin công ty (CÔNG TY CỔ PHẦN GOMI CORPORATION)
    - Section 4: Form Đăng ký làm đối tác GOONGBE (Widget Form Elementor)
    - Section 5: 'Kết nối với Goongbe ngay' (Widget Social Icons & Khối 3 cột thông tin hỗ trợ)
    """

    # SECTION 1: Banner Top (Full Width 45vh)
    sec1_banner_contact = {
        "id": "sec_contact_banner",
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "full_width",
            "stretch_section": "section-stretched",
            "background_background": "classic",
            "background_image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/Banner-1.jpg"},
            "background_position": "center center",
            "background_size": "cover",
            "padding": {"unit": "px", "top": "100", "right": "40", "bottom": "100", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_contact_banner",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_contact_banner_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Liên Hệ",
                            "align": "left",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 42},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "100", "isLinked": False}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 2: Widget Google Maps
    sec2_maps = {
        "id": "sec_contact_map",
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "full_width",
            "stretch_section": "section-stretched",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [
            {
                "id": "col_contact_map",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_contact_gmap",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "google_maps",
                        "settings": {
                            "address": "Số 67, đường số 6, Khu dân cư Cityland ParkHills, phường Gò Vấp, Thành phố Hồ Chí Minh",
                            "zoom": {"size": 15},
                            "height": {"unit": "px", "size": 400}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 3: Đoạn văn mô tả thông tin công ty
    sec3_company_info = {
        "id": "sec_contact_info",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "40", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_contact_info",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_contact_info_text",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": """
                            <div style="font-family: Roboto, sans-serif; max-width: 900px; margin: 0 auto; line-height: 1.8; font-size: 15px;">
                                <h3 style="color: #009AA5; font-weight: 800; font-size: 20px; margin-bottom: 10px;">GOONGBE Việt Nam:</h3>
                                <p style="color: #333; margin-bottom: 8px;"><strong>Công ty chịu trách nhiệm nhập khẩu và phân phối sản phẩm tại Việt Nam:</strong> CÔNG TY CỔ PHẦN GOMI CORPORATION</p>
                                <p style="color: #333; margin-bottom: 8px;"><strong>Địa chỉ:</strong> Số 67, đường số 6, Khu dân cư Cityland ParkHills, phường Gò Vấp, Thành phố Hồ Chí Minh</p>
                                <p style="color: #333; margin-bottom: 0;"><strong>Hotline:</strong> <span style="color: #009AA5; font-weight: 700;">(+84) 1900 638 078</span></p>
                            </div>
                            """
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 4: Widget Form "Đăng kí làm đối tác GOONGBE"
    sec4_form = {
        "id": "sec_contact_form",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "30", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_contact_form",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_contact_form_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Đăng kí làm đối tác GOONGBE",
                            "title_color": "#009AA5",
                            "typography_font_size": {"unit": "px", "size": 26},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": "w_contact_form_widget",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "form",
                        "settings": {
                            "form_name": "Form Đăng Ký Đối Tác GOONGBE",
                            "form_fields": [
                                {"custom_id": "ho", "field_type": "text", "field_label": "Họ *", "width": "50"},
                                {"custom_id": "ten", "field_type": "text", "field_label": "Tên *", "width": "50"},
                                {"custom_id": "email", "field_type": "email", "field_label": "Email *", "width": "50"},
                                {"custom_id": "sdt", "field_type": "tel", "field_label": "Số điện thoại *", "width": "50"},
                                {
                                    "custom_id": "phan_loai",
                                    "field_type": "radio",
                                    "field_label": "Bạn liên hệ từ Công ty / Cá nhân *",
                                    "field_options": "Công ty\nCá nhân",
                                    "width": "50"
                                },
                                {"custom_id": "ten_cong_ty", "field_type": "text", "field_label": "Tên công ty liên hệ", "width": "50"},
                                {"custom_id": "thong_tin_hop_tac", "field_type": "textarea", "field_label": "Thông tin hợp tác", "width": "100"}
                            ],
                            "button_text": "Gửi yêu cầu",
                            "button_background_color": "#009AA5",
                            "button_text_color": "#FFFFFF",
                            "button_border_radius": {"unit": "px", "top": "6", "right": "6", "bottom": "6", "left": "6"}
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 5: "Kết nối với Goongbe ngay" (Widget Social Icons & Khối 3 Cột)
    sec5_social = {
        "id": "sec_contact_social",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "50", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_contact_social",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_social_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Kết nối với Goongbe ngay",
                            "align": "center",
                            "title_color": "#009AA5",
                            "typography_font_size": {"unit": "px", "size": 28},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "20", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": "w_social_icons",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "social-icons",
                        "settings": {
                            "align": "center",
                            "social_icon_list": [
                                {"social_icon": {"value": "fab fa-facebook-f", "library": "fa-brands"}, "link": {"url": "https://facebook.com"}},
                                {"social_icon": {"value": "fab fa-instagram", "library": "fa-brands"}, "link": {"url": "https://instagram.com"}},
                                {"social_icon": {"value": "fab fa-youtube", "library": "fa-brands"}, "link": {"url": "https://youtube.com"}},
                                {"social_icon": {"value": "fab fa-tiktok", "library": "fa-brands"}, "link": {"url": "https://tiktok.com"}}
                            ],
                            "icon_color": "custom",
                            "icon_primary_color": "#888888",
                            "icon_secondary_color": "#FFFFFF",
                            "icon_size": {"unit": "px", "size": 20}
                        }
                    },
                    # INNER BOX 3 CỘT THÔNG TIN HỖ TRỢ NỀN XANH TƯƠI #009AA5
                    {
                        "id": "sec_contact_support_bar",
                        "elType": "section",
                        "isInner": True,
                        "settings": {
                            "background_background": "classic",
                            "background_color": "#009AA5",
                            "padding": {"unit": "px", "top": "35", "right": "30", "bottom": "35", "left": "30", "isLinked": False},
                            "margin": {"unit": "px", "top": "45", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        },
                        "elements": [
                            {
                                "id": "col_support_1",
                                "elType": "column",
                                "isInner": True,
                                "settings": {"_column_size": 33.33, "_inline_size": 33.33},
                                "elements": [
                                    {
                                        "id": "w_sup1_text",
                                        "elType": "widget",
                                        "isInner": True,
                                        "widgetType": "text-editor",
                                        "settings": {
                                            "editor": "<p style='color: #FFFFFF; font-size: 14px; text-align: center; line-height: 1.6;'><strong>Số 67, đường số 6, Khu dân cư Cityland ParkHills, phường Gò Vấp, TP. Hồ Chí Minh</strong><br><br><strong>SDT:</strong> (+84-28) 7306 9798</p>"
                                        }
                                    }
                                ]
                            },
                            {
                                "id": "col_support_2",
                                "elType": "column",
                                "isInner": True,
                                "settings": {"_column_size": 33.33, "_inline_size": 33.33},
                                "elements": [
                                    {
                                        "id": "w_sup2_text",
                                        "elType": "widget",
                                        "isInner": True,
                                        "widgetType": "text-editor",
                                        "settings": {
                                            "editor": "<p style='color: #FFFFFF; font-size: 14px; text-align: center; line-height: 1.6;'><strong>Thời gian làm việc</strong><br><br><strong>T2 - T6:</strong> 9:00 - 18:00</p>"
                                        }
                                    }
                                ]
                            },
                            {
                                "id": "col_support_3",
                                "elType": "column",
                                "isInner": True,
                                "settings": {"_column_size": 33.33, "_inline_size": 33.33},
                                "elements": [
                                    {
                                        "id": "w_sup3_text",
                                        "elType": "widget",
                                        "isInner": True,
                                        "widgetType": "text-editor",
                                        "settings": {
                                            "editor": "<p style='color: #FFFFFF; font-size: 14px; text-align: center; line-height: 1.6;'><strong>Thời gian giao hàng</strong><br><br><strong>T2 - T7:</strong> 9:00 - 18:00</p>"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    content_sections = [
        sec1_banner_contact,
        sec2_maps,
        sec3_company_info,
        sec4_form,
        sec5_social
    ]

    # Full Page JSON
    full_page = {
        "version": "3.0.0",
        "title": "Trang Liên Hệ GOONGBE Việt Nam (Contact Us Page)",
        "type": "page",
        "elementor_version": "3.35.1",
        "content": content_sections,
        "page_settings": []
    }

    json_path = "wp-json-elementor/goongbe-page-contact.json"
    zip_path = "wp-json-elementor/goongbe-page-contact.zip"
    clipboard_path = "wp-json-elementor/goongbe-page-contact-clipboard.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_page, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_sections, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported Contact Page JSON: {json_path}")
    print(f"[SUCCESS] Exported Contact Page ZIP: {zip_path}")
    print(f"[SUCCESS] Exported Contact Page Clipboard: {clipboard_path}")

if __name__ == "__main__":
    build_goongbe_contact_page()
