import json
import zipfile
import os

def build_goongbe_footer_container():
    """
    Sinh mã JSON Elementor Pro 3.35 & Core 4.2.1 chuẩn 100% FLEXBOX CONTAINER theo đúng 2 yêu cầu cụ thể của User:
    
    1. Khối 1: Có Container Outer bọc ngoài (nền trong suốt), bên trong chứa:
       - Inner Container Wrap (Nền xanh #009AA5, position: relative) bọc 3 cột con 33.333%.
       - Widget Hình ảnh Logo Bông hoa Cyan thuộc Khối 1 với position: absolute (bottom: -26px).
    2. Khối 2: Đẩy Widget Hình ảnh sang Khối 1, Khối 2 chỉ còn Tiêu đề, Social Icons, Divider và Copyright Text.
    """

    # CONTAINER 1 OUTER: Khối bọc ngoài (Nền trong suốt)
    container_1_outer = {
        "id": "cnt_footer_sec1_outer",
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "transparent",
            "padding": {"unit": "px", "top": "40", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
            "margin": {"unit": "px", "top": "0", "right": "auto", "bottom": "-60", "left": "auto", "isLinked": False},
            "z_index": 1
        },
        "elements": [
            # KHỐI CONTAINER BỌC BÊN TRONG (INNER WRAPPER) MANG NỀN XANH #009AA5 VÀ POSITION RELATIVE
            {
                "id": "cnt_footer_inner_wrap",
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "row",
                    "flex_wrap": "nowrap",
                    "background_background": "classic",
                    "background_color": "#009AA5",
                    "padding": {"unit": "px", "top": "45", "right": "30", "bottom": "45", "left": "30", "isLinked": False},
                    "position": "relative"
                },
                "elements": [
                    # CỘT CON 1: Địa chỉ & SĐT (33.333%)
                    {
                        "id": "cnt_footer_col_1",
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "width": {"unit": "%", "size": 33.333},
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
                    # CỘT CON 2: Thời gian làm việc (33.333%)
                    {
                        "id": "cnt_footer_col_2",
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "width": {"unit": "%", "size": 33.333},
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
                    # CỘT CON 3: Thời gian giao hàng (33.333%)
                    {
                        "id": "cnt_footer_col_3",
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "width": {"unit": "%", "size": 33.333}
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
            },
            # WIDGET HÌNH ẢNH BÔNG HOA CYAN THUỘC CONTAINER 1 VỚI POSITION ABSOLUTE
            {
                "id": "w_footer_flower_icon_abs",
                "elType": "widget",
                "isInner": False,
                "widgetType": "image",
                "settings": {
                    "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/footer-svg.svg"},
                    "align": "center",
                    "width": {"unit": "px", "size": 52},
                    "_position": "absolute",
                    "_element_vertical_align": "bottom",
                    "_offset_y": {"unit": "px", "size": -26},
                    "_offset_orientation_v": "start",
                    "_element_width": "initial",
                    "margin": {"unit": "px", "top": "-26", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                }
            }
        ]
    }

    # CONTAINER 2: Khối liên hệ & Bản quyền Footer (Nền #E5F6F8, Flex Direction: column)
    container_2 = {
        "id": "cnt_footer_copyright_bar",
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#E5F6F8",
            "padding": {"unit": "px", "top": "45", "right": "40", "bottom": "40", "left": "40", "isLinked": False}
        },
        "elements": [
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

    content_containers = [
        container_1_outer,
        container_2
    ]

    # Full Section / Template JSON (Matching Version 0.4 and Elementor Pro 3.35.1)
    full_template = {
        "version": "0.4",
        "title": "Footer -- 04082026",
        "type": "footer",
        "elementor_version": "3.35.1",
        "content": content_containers,
        "page_settings": []
    }

    # PATHS
    json_path = "wp-json-elementor/goongbe-footer-section.json"
    zip_path = "wp-json-elementor/goongbe-footer-section.zip"
    clipboard_path = "wp-json-elementor/goongbe-footer-section-clipboard.json"
    
    user_json_path = "0. FOOTER -- 04082026/elementor-443-2026-08-05.json"
    user_zip_path = "0. FOOTER -- 04082026/elementor-443-2026-08-05.zip"

    # Save to wp-json-elementor/
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_template, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_containers, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    # Save directly to 0. FOOTER -- 04082026/
    with open(user_json_path, "w", encoding="utf-8") as f:
        json.dump(full_template, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(user_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(user_json_path, arcname=os.path.basename(user_json_path))

    print(f"[SUCCESS] Exported Outer+Inner Container Flexbox Footer JSON to {json_path} & {user_json_path}")
    print(f"[SUCCESS] Exported Outer+Inner Container Flexbox Footer ZIP to {zip_path} & {user_zip_path}")

if __name__ == "__main__":
    build_goongbe_footer_container()
