import json
import zipfile
import os

def build_goongbe_product_list_page():
    """
    Sinh mã JSON Elementor Pro 3.35 chuẩn cho TRANG DANH SÁCH SẢN PHẨM GOONGBE (Product Catalog Page):
    Thừa hưởng 100% màu sắc (#1B5B65, #009AA5, #E5F6F8), font Roboto và thiết lập từ Trang Chủ Chuẩn 1.
    Gồm 5 Section chuẩn:
    - Section 1: Hero Banner Top Banner Slider Full Width
    - Section 2: Tiêu đề "Gia đình GOONGBE" & Lưới Thẻ Sản Phẩm 2 Cột (Thẻ sản phẩm + Giá + Mô tả + 2 Nút)
    - Section 3: Thanh Call-To-Action (3 Banner Nổi Bật: Điểm Bán, Mua Online, Hotline CSKH)
    - Section 4: Khối Form Đặt Mua Nhanh (Form nhập thông tin + Ảnh trọn bộ sản phẩm)
    - Section 5: Footer Thương Hiệu GOONGBE
    """

    # SECTION 1: Banner Top Full Width
    sec1_top_banner = {
        "id": "sec_prod_banner",
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "full_width",
            "stretch_section": "section-stretched",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [
            {
                "id": "col_prod_banner",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_prod_slides",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "slides",
                        "settings": {
                            "slides_name": "Slides",
                            "slides": [
                                {
                                    "_id": "slide_prod_1",
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

    # SECTION 2: Tiêu đề "Gia đình GOONGBE" & Lưới Thẻ Sản Phẩm Grid
    sec2_product_grid = {
        "id": "sec_prod_grid_catalog",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_prod_catalog_main",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_prod_main_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Gia đình GOONGBE",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 34},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "40", "left": "0", "isLinked": False}
                        }
                    },
                    # DẢI SẢN PHẨM ROW 1 (2 CỘT)
                    {
                        "id": "inner_sec_row_1",
                        "elType": "section",
                        "isInner": True,
                        "settings": {"margin": {"unit": "px", "top": "0", "right": "0", "bottom": "35", "left": "0", "isLinked": False}},
                        "elements": [
                            # SẢN PHẨM 1
                            {
                                "id": "col_prod_item_1",
                                "elType": "column",
                                "isInner": True,
                                "settings": {"_column_size": 50, "_inline_size": 50},
                                "elements": [
                                    {"id": "w_p1_img", "elType": "widget", "isInner": False, "widgetType": "image", "settings": {"image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/SECTION-3-1.avif"}, "align": "center", "width": {"unit": "px", "size": 220}}},
                                    {"id": "w_p1_title", "elType": "widget", "isInner": False, "widgetType": "heading", "settings": {"title": "Kem dưỡng ẩm dịu nhẹ GOONGBE Pri-mmune 350ml", "align": "center", "title_color": "#1B5B65", "typography_font_size": {"unit": "px", "size": 17}, "typography_font_weight": "700"}},
                                    {"id": "w_p1_price", "elType": "widget", "isInner": False, "widgetType": "heading", "settings": {"title": "Giá: <span style='color:#009AA5; font-size:20px;'>269.000 đ</span>", "align": "center", "typography_font_size": {"unit": "px", "size": 15}}},
                                    {"id": "w_p1_desc", "elType": "widget", "isInner": False, "widgetType": "text-editor", "settings": {"editor": "<p style='text-align:center; color:#666; font-size:13px;'>Phức hợp thảo dược Oji Relief Complex giúp dưỡng ẩm sâu 72h cho làn da bé sơ sinh...</p>"}},
                                    # 2 NÚT HÀNH ĐỘNG
                                    {
                                        "id": "inner_btn_box_1",
                                        "elType": "container",
                                        "isInner": True,
                                        "settings": {"content_width": "full", "flex_direction": "row", "justify_content": "center", "gap": {"unit": "px", "size": 12}},
                                        "elements": [
                                            {"id": "w_p1_buy_btn", "elType": "widget", "isInner": False, "widgetType": "button", "settings": {"text": "MUA NGAY", "background_color": "#009AA5", "button_text_color": "#FFFFFF", "border_radius": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}}},
                                            {"id": "w_p1_adv_btn", "elType": "widget", "isInner": False, "widgetType": "button", "settings": {"text": "TƯ VẤN NGAY", "background_color": "#1B5B65", "button_text_color": "#FFFFFF", "border_radius": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}}}
                                        ]
                                    }
                                ]
                            },
                            # SẢN PHẨM 2
                            {
                                "id": "col_prod_item_2",
                                "elType": "column",
                                "isInner": True,
                                "settings": {"_column_size": 50, "_inline_size": 50},
                                "elements": [
                                    {"id": "w_p2_img", "elType": "widget", "isInner": False, "widgetType": "image", "settings": {"image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/sECTION-3-2.jpg"}, "align": "center", "width": {"unit": "px", "size": 220}}},
                                    {"id": "w_p2_title", "elType": "widget", "isInner": False, "widgetType": "heading", "settings": {"title": "Sữa tắm gội toàn thân em bé GOONGBE 350ml", "align": "center", "title_color": "#1B5B65", "typography_font_size": {"unit": "px", "size": 17}, "typography_font_weight": "700"}},
                                    {"id": "w_p2_price", "elType": "widget", "isInner": False, "widgetType": "heading", "settings": {"title": "Giá: <span style='color:#009AA5; font-size:20px;'>289.000 đ</span>", "align": "center", "typography_font_size": {"unit": "px", "size": 15}}},
                                    {"id": "w_p2_desc", "elType": "widget", "isInner": False, "widgetType": "text-editor", "settings": {"editor": "<p style='text-align:center; color:#666; font-size:13px;'>Công thức bọt mịn dịu lành không làm cay mắt bé, làm sạch nhẹ nhàng và bảo vệ màng ẩm...</p>"}},
                                    {
                                        "id": "inner_btn_box_2",
                                        "elType": "container",
                                        "isInner": True,
                                        "settings": {"content_width": "full", "flex_direction": "row", "justify_content": "center", "gap": {"unit": "px", "size": 12}},
                                        "elements": [
                                            {"id": "w_p2_buy_btn", "elType": "widget", "isInner": False, "widgetType": "button", "settings": {"text": "MUA NGAY", "background_color": "#009AA5", "button_text_color": "#FFFFFF", "border_radius": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}}},
                                            {"id": "w_p2_adv_btn", "elType": "widget", "isInner": False, "widgetType": "button", "settings": {"text": "TƯ VẤN NGAY", "background_color": "#1B5B65", "button_text_color": "#FFFFFF", "border_radius": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True}}}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # SECTION 3: Thanh Call-To-Action (3 Banner Nổi Bật Nhanh: Điểm bán, Mua Online, Hotline)
    sec3_cta_grid = {
        "id": "sec_prod_cta_bar",
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "40", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_cta_1",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 33, "_inline_size": 33.33},
                "elements": [
                    {
                        "id": "w_cta_box_1",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "icon-box",
                        "settings": {
                            "title_text": "Điểm bán GOONGBE",
                            "description_text": "Xem danh sách các điểm bán chính hãng gần bạn nhất",
                            "icon_color": "#009AA5",
                            "title_color": "#1B5B65"
                        }
                    }
                ]
            },
            {
                "id": "col_cta_2",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 33, "_inline_size": 33.33},
                "elements": [
                    {
                        "id": "w_cta_box_2",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "icon-box",
                        "settings": {
                            "title_text": "Mua hàng online",
                            "description_text": "Thanh toán tiện lợi khi nhận hàng, giao nhanh toàn quốc",
                            "icon_color": "#009AA5",
                            "title_color": "#1B5B65"
                        }
                    }
                ]
            },
            {
                "id": "col_cta_3",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 33, "_inline_size": 33.33},
                "elements": [
                    {
                        "id": "w_cta_box_3",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "icon-box",
                        "settings": {
                            "title_text": "1800 8179 (Miễn phí)",
                            "description_text": "Tổng đài tư vấn chăm sóc da em bé từ chuyên gia",
                            "icon_color": "#009AA5",
                            "title_color": "#1B5B65"
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 4: Khối Form Đặt Mua Hàng Nhanh (Nền nhạt #E5F6F8)
    sec4_quick_checkout = {
        "id": "sec_prod_quick_checkout",
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": "#E5F6F8",
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_checkout_left",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 60, "_inline_size": 60},
                "elements": [
                    {
                        "id": "w_chk_title",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Đặt mua sản phẩm GOONGBE",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 26},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto"
                        }
                    },
                    {
                        "id": "w_chk_form",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "form",
                        "settings": {
                            "form_name": "Form Đặt Hàng Nhanh",
                            "button_text": "ĐẶT HÀNG NGAY",
                            "button_background_color": "#009AA5"
                        }
                    }
                ]
            },
            {
                "id": "col_checkout_right",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 40, "_inline_size": 40, "content_position": "middle"},
                "elements": [
                    {
                        "id": "w_chk_img",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/Goongbe-500X500.jpg"},
                            "align": "center"
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 5: Footer Thương Hiệu GOONGBE
    sec5_footer = {
        "id": "sec_prod_footer",
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": "#1B5B65",
            "padding": {"unit": "px", "top": "50", "right": "40", "bottom": "50", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_footer_main",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "w_footer_text",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='color:#FFF; text-align:center; font-size:14px;'>© 2026 GOONGBE VIỆT NAM - Thương hiệu chăm sóc làn da trẻ em uy tín từ Hàn Quốc.</p>"
                        }
                    }
                ]
            }
        ]
    }

    content_sections = [
        sec1_top_banner,
        sec2_product_grid,
        sec3_cta_grid,
        sec4_quick_checkout,
        sec5_footer
    ]

    # Full Page JSON
    full_page = {
        "version": "3.0.0",
        "title": "Trang Danh Sách Sản Phẩm GOONGBE (Product Catalog)",
        "type": "page",
        "elementor_version": "3.35.1",
        "content": content_sections,
        "page_settings": []
    }

    json_path = "wp-json-elementor/goongbe-page-product-catalog.json"
    zip_path = "wp-json-elementor/goongbe-page-product-catalog.zip"
    clipboard_path = "wp-json-elementor/goongbe-page-product-catalog-clipboard.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_page, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_sections, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported Product Catalog Page JSON: {json_path}")
    print(f"[SUCCESS] Exported Product Catalog Page ZIP: {zip_path}")
    print(f"[SUCCESS] Exported Product Catalog Page Clipboard: {clipboard_path}")

if __name__ == "__main__":
    build_goongbe_product_list_page()
