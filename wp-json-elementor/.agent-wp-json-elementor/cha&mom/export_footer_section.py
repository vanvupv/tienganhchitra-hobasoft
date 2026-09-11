import json
import zipfile
import os

def build_goongbe_footer_section():
    """
    Sinh mã JSON Elementor Pro 3.35 chuẩn cho MẪU FOOTER SECTION GOONGBE VIỆT NAM (Sửa dứt điểm lỗi tự nhảy số 10%):
    
    Nguyên nhân lỗi tự nảy số 10%:
    Do xếp Widget Hình Ảnh đứng cùng cấp với Inner Section bên trong 1 Outer Column, khiến bộ lắng nghe sự kiện
    JS của Elementor Editor bị vỡ DOM Validator và ép giá trị _inline_size về 10%.
    
    Cấu trúc mới chuẩn 100% Elementor:
    - Section 1: Nền xanh #009AA5, chứa 3 Cột thông tin (Địa chỉ, Giờ làm việc, Giờ giao hàng) chia đều 33.333%.
    - Section 2: Nền #E5F6F8, chứa Cột đơn (100% full width) bao gồm:
        1. Widget Hình Ảnh Logo Bông Hoa Cyan (Căn giữa, margin-top: -26px đè lên ranh giới giữa 2 section).
        2. Widget Tiêu đề 'Liên hệ GOONGBE Việt Nam'.
        3. Widget Social Icons.
        4. Widget Divider.
        5. Widget Text Editor (Thông tin bản quyền GOMI CORPORATION).
    """

    # SECTION 1: Khối thông tin 3 Cột (Nền xanh #009AA5, Bo góc nhẹ, Padding 45px)
    sec1_support_info = {
        "id": "sec_footer_info_box",
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "boxed",
            "background_background": "classic",
            "background_color": "#009AA5",
            "padding": {"unit": "px", "top": "45", "right": "30", "bottom": "45", "left": "30", "isLinked": False},
            "margin": {"unit": "px", "top": "40", "right": "auto", "bottom": "0", "left": "auto", "isLinked": False}
        },
        "elements": [
            # CỘT 1: Địa chỉ & SĐT (33.333%)
            {
                "id": "col_footer_sup_1",
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 33.333,
                    "border_border": "solid",
                    "border_color": "rgba(255, 255, 255, 0.3)",
                    "border_width": {"unit": "px", "top": "0", "right": "1", "bottom": "0", "left": "0", "isLinked": False}
                },
                "elements": [
                    {
                        "id": "w_footer_sup1_text",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": """
                            <div style="text-align: center; color: #FFFFFF; font-family: Roboto, sans-serif; line-height: 1.6; padding: 0 15px;">
                                <p style="font-size: 14px; font-weight: 700; margin-bottom: 12px;">Số 67, đường số 6, Khu dân cư Cityland ParkHills, phường Gò Vấp, Thành phố Hồ Chí Minh</p>
                                <p style="font-size: 15px; font-weight: 800; margin-bottom: 0;">SĐT: (+84-28) 7306 9796</p>
                            </div>
                            """
                        }
                    }
                ]
            },
            # CỘT 2: Thời gian làm việc (33.333%)
            {
                "id": "col_footer_sup_2",
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 33.333,
                    "border_border": "solid",
                    "border_color": "rgba(255, 255, 255, 0.3)",
                    "border_width": {"unit": "px", "top": "0", "right": "1", "bottom": "0", "left": "0", "isLinked": False}
                },
                "elements": [
                    {
                        "id": "w_footer_sup2_text",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": """
                            <div style="text-align: center; color: #FFFFFF; font-family: Roboto, sans-serif; line-height: 1.6; padding: 0 15px;">
                                <p style="font-size: 15px; font-weight: 700; margin-bottom: 15px;">Thời gian làm việc</p>
                                <p style="font-size: 14px; font-weight: 800; margin-bottom: 0;">T2 - T6: 9:00 - 18:00</p>
                            </div>
                            """
                        }
                    }
                ]
            },
            # CỘT 3: Thời gian giao hàng (33.333%)
            {
                "id": "col_footer_sup_3",
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 33.333
                },
                "elements": [
                    {
                        "id": "w_footer_sup3_text",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": """
                            <div style="text-align: center; color: #FFFFFF; font-family: Roboto, sans-serif; line-height: 1.6; padding: 0 15px;">
                                <p style="font-size: 15px; font-weight: 700; margin-bottom: 15px;">Thời gian giao hàng</p>
                                <p style="font-size: 14px; font-weight: 800; margin-bottom: 0;">T2 - T7: 9:00 - 18:00</p>
                            </div>
                            """
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 2: Khối liên hệ & Bản quyền Footer (Định dạng 1 Cột 100% cực kỳ chuẩn)
    sec2_social_copyright = {
        "id": "sec_footer_copyright_bar",
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "full_width",
            "background_background": "classic",
            "background_color": "#E5F6F8",
            "padding": {"unit": "px", "top": "20", "right": "40", "bottom": "40", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_footer_social_main",
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 100
                },
                "elements": [
                    # HÌNH ẢNH BÔNG HOA CYAN ĐẶT ĐẦU SECTION 2 VỚI MARGIN NỔI BẬT LÊN SECTION 1
                    {
                        "id": "w_footer_flower_icon_abs",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/footer-svg.svg"},
                            "align": "center",
                            "width": {"unit": "px", "size": 52},
                            "margin": {"unit": "px", "top": "-46", "right": "0", "bottom": "20", "left": "0", "isLinked": False}
                        }
                    },
                    # TIÊU ĐỀ LIÊN HỆ
                    {
                        "id": "w_footer_contact_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Liên hệ GOONGBE Việt Nam",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 16},
                            "typography_font_weight": "700",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "15", "left": "0", "isLinked": False}
                        }
                    },
                    # WIDGET SOCIAL ICONS
                    {
                        "id": "w_footer_social_icons",
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
                            "icon_primary_color": "#8D99AE",
                            "icon_secondary_color": "#FFFFFF",
                            "icon_size": {"unit": "px", "size": 18}
                        }
                    },
                    # DIVIDER LINE
                    {
                        "id": "w_footer_divider",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "divider",
                        "settings": {
                            "color": "rgba(27, 91, 101, 0.2)",
                            "weight": {"unit": "px", "size": 1},
                            "gap": {"unit": "px", "size": 25}
                        }
                    },
                    # MÔ TẢ BẢN QUYỀN VÀ ĐỊA CHỈ PHÁP LÝ GOMI CORPORATION
                    {
                        "id": "w_footer_copyright_text",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": """
                            <div style="text-align: center; color: #1B5B65; font-family: Roboto, sans-serif; font-size: 13px; line-height: 1.7; max-width: 950px; margin: 0 auto;">
                                <p style="font-weight: 700; margin-bottom: 5px;">2025 © CÔNG TY CỔ PHẦN GOMI CORPORATION</p>
                                <p style="margin-bottom: 0;">ĐC: 15A Nguyễn Trung Trực, Phường Bình Lợi Trung, Thành Phố Hồ Chí Minh, Việt Nam. - ĐC nhận chứng từ: Số 67, đường số 6, KDC Cityland ParkHills, Phường Gò Vấp, TP.HCM</p>
                            </div>
                            """
                        }
                    }
                ]
            }
        ]
    }

    content_sections = [
        sec1_support_info,
        sec2_social_copyright
    ]

    # Full Section / Template JSON
    full_template = {
        "version": "3.0.0",
        "title": "GOONGBE Footer Section Template (Fixed DOM Hierarchy)",
        "type": "section",
        "elementor_version": "3.35.1",
        "content": content_sections,
        "page_settings": []
    }

    json_path = "wp-json-elementor/goongbe-footer-section.json"
    zip_path = "wp-json-elementor/goongbe-footer-section.zip"
    clipboard_path = "wp-json-elementor/goongbe-footer-section-clipboard.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_template, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_sections, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported Fixed DOM Hierarchy Footer Section JSON: {json_path}")
    print(f"[SUCCESS] Exported Fixed DOM Hierarchy Footer Section ZIP: {zip_path}")
    print(f"[SUCCESS] Exported Fixed DOM Hierarchy Footer Section Clipboard: {clipboard_path}")

if __name__ == "__main__":
    build_goongbe_footer_section()
