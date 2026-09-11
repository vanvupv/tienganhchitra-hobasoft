import json
import zipfile
import os

def build_goongbe_product_catalog_container():
    """
    Sinh mã JSON Elementor Pro 3.35.1 / Core 4.2.1 chuẩn 100% FLEXBOX CONTAINER (elType: "container")
    cho TRANG DANH SÁCH SẢN PHẨM GOONGBE VIỆT NAM (Bổ sung Widget Giỏ Hàng WooCommerce Menu Cart):
    
    - Section 1: Banner Top Full Width + WIDGET GIỎ HÀNG NỔI (woocommerce-menu-cart) góc phải.
    - Section 2: Danh sách Sản phẩm WooCommerce Products (2 Cột) + Nút THÊM VÀO GIỎ HÀNG (AJAX Add To Cart).
    - Section 3: 3 Khối Call-To-Action (Điểm bán GOONGBE, Mua hàng online, Hotline 1800 8179).
    - Section 4: Chức năng 'Đặt mua hàng nhanh' (Form Đặt Hàng Nhanh & Hình ảnh bộ sản phẩm GOONGBE).
    """

    # SECTION 1: Banner Top Full Width + Widget Giỏ Hàng Nổi (Menu Cart)
    sec1_banner = {
        "id": "cnt_prod_sec1_banner",
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
            "margin": {"unit": "px", "top": "0", "right": "auto", "bottom": "40", "left": "auto", "isLinked": False},
            "position": "relative"
        },
        "elements": [
            # WIDGET SLIDES BANNER
            {
                "id": "w_prod_banner_slides",
                "elType": "widget",
                "isInner": False,
                "widgetType": "slides",
                "settings": {
                    "slides": [
                        {
                            "heading": "",
                            "description": "",
                            "button_text": "",
                            "background_color": "",
                            "background_image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/Banner-1.jpg"},
                            "_id": "slide_prod_1"
                        }
                    ],
                    "slides_height": {"unit": "vh", "size": 60}
                }
            },
            # WIDGET GIỎ HÀNG WOOCOMMERCE MENU CART NỔI (GÓC TRÊN BÊN PHẢI)
            {
                "id": "w_prod_menu_cart_top",
                "elType": "widget",
                "isInner": False,
                "widgetType": "woocommerce-menu-cart",
                "settings": {
                    "icon": "bag-light",
                    "items_indicator": "bubble",
                    "hide_empty_indicator": "no",
                    "cart_type": "side-cart",
                    "align": "right",
                    "cart_icon_color": "#1B5B65",
                    "_position": "absolute",
                    "_offset_x": {"unit": "px", "size": 25},
                    "_offset_y": {"unit": "px", "size": 20},
                    "_offset_orientation_h": "end",
                    "z_index": 999
                }
            }
        ]
    }

    # SECTION 2: Danh Sách Sản Phẩm Động (Dùng Widget Posts & WC-Products Chuẩn Elementor Pro 2 Cột)
    sec2_products_list = {
        "id": "cnt_prod_sec2_catalog",
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "flex_direction": "column",
            "padding": {"unit": "px", "top": "40", "right": "20", "bottom": "40", "left": "20", "isLinked": False}
        },
        "elements": [
            # TIÊU ĐỀ SECTION
            {
                "id": "w_prod_main_heading",
                "elType": "widget",
                "isInner": False,
                "widgetType": "heading",
                "settings": {
                    "title": "Gia đình GOONGBE",
                    "align": "center",
                    "title_color": "#1B5B65",
                    "typography_font_size": {"unit": "px", "size": 32},
                    "typography_font_weight": "800",
                    "typography_font_family": "Roboto",
                    "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "30", "left": "0", "isLinked": False}
                }
            },
            # WIDGET POSTS / PRODUCTS GRID 2 CỘT CHUẨN ELEMENTOR PRO
            {
                "id": "w_prod_posts_grid",
                "elType": "widget",
                "isInner": False,
                "widgetType": "posts",
                "settings": {
                    "posts_post_type": "product",
                    "posts_posts_per_page": 12,
                    "columns": 2,
                    "columns_tablet": 2,
                    "columns_mobile": 1,
                    "classic_show_image": "yes",
                    "classic_show_title": "yes",
                    "classic_show_excerpt": "yes",
                    "classic_show_read_more": "yes",
                    "classic_read_more_text": "XEM CHI TIẾT & GIỎ HÀNG",
                    "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "20", "left": "0", "isLinked": False}
                }
            },
            # WIDGET WOOCOMMERCE PRODUCTS CHUẨN ELEMENTOR PRO KHÈM NÚT THÊM VÀO GIỎ
            {
                "id": "w_prod_wc_grid",
                "elType": "widget",
                "isInner": False,
                "widgetType": "wc-products",
                "settings": {
                    "posts_per_page": 12,
                    "columns": 2,
                    "columns_tablet": 2,
                    "columns_mobile": 1,
                    "show_image": "yes",
                    "show_title": "yes",
                    "show_price": "yes",
                    "show_button": "yes",
                    "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                }
            }
        ]
    }

    # SECTION 3: 3 Khối Hình Ảnh / Call-To-Action (Điểm bán, Mua hàng online, Hotline)
    sec3_cta_blocks = {
        "id": "cnt_prod_sec3_cta",
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "flex_direction": "row",
            "flex_wrap": "nowrap",
            "padding": {"unit": "px", "top": "30", "right": "20", "bottom": "50", "left": "20", "isLinked": False}
        },
        "elements": [
            {
                "id": "cnt_cta_item_1",
                "elType": "container",
                "isInner": True,
                "settings": {
                    "width": {"unit": "%", "size": 32},
                    "background_background": "classic",
                    "background_color": "#009AA5",
                    "padding": {"unit": "px", "top": "25", "right": "20", "bottom": "25", "left": "20", "isLinked": False},
                    "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True}
                },
                "elements": [
                    {
                        "id": "w_cta_text_1",
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": "Điểm bán sản phẩm<br><strong>GOONGBE</strong>",
                            "align": "center",
                            "title_color": "#FFFFFF",
                            "typography_font_size": {"unit": "px", "size": 18},
                            "typography_font_family": "Roboto"
                        }
                    }
                ]
            },
            {
                "id": "cnt_cta_item_2",
                "elType": "container",
                "isInner": True,
                "settings": {
                    "width": {"unit": "%", "size": 32},
                    "background_background": "classic",
                    "background_color": "#38BDF8",
                    "padding": {"unit": "px", "top": "25", "right": "20", "bottom": "25", "left": "20", "isLinked": False},
                    "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True}
                },
                "elements": [
                    {
                        "id": "w_cta_text_2",
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": "Mua hàng Online<br><strong>Thanh toán tại nhà</strong>",
                            "align": "center",
                            "title_color": "#FFFFFF",
                            "typography_font_size": {"unit": "px", "size": 18},
                            "typography_font_family": "Roboto"
                        }
                    }
                ]
            },
            {
                "id": "cnt_cta_item_3",
                "elType": "container",
                "isInner": True,
                "settings": {
                    "width": {"unit": "%", "size": 32},
                    "background_background": "classic",
                    "background_color": "#0088CC",
                    "padding": {"unit": "px", "top": "25", "right": "20", "bottom": "25", "left": "20", "isLinked": False},
                    "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True}
                },
                "elements": [
                    {
                        "id": "w_cta_text_3",
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": "Hotline Hỗ Trợ<br><strong>1800 8179 (Miễn phí)</strong>",
                            "align": "center",
                            "title_color": "#FFFFFF",
                            "typography_font_size": {"unit": "px", "size": 18},
                            "typography_font_family": "Roboto"
                        }
                    }
                ]
            }
        ]
    }

    # SECTION 4: Chức Năng Đặt Mua Hàng Nhanh (Form Đặt Hàng & Ảnh Sản Phẩm)
    sec4_quick_order = {
        "id": "sec_prod_sec4_order",
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "background_background": "classic",
            "background_color": "#FFF9F5",
            "padding": {"unit": "px", "top": "50", "right": "40", "bottom": "50", "left": "40", "isLinked": False}
        },
        "elements": [
            # CỘT TRÁI: Form Đặt Mua Hàng Nhanh
            {
                "id": "cnt_order_form_col",
                "elType": "container",
                "isInner": True,
                "settings": {
                    "width": {"unit": "%", "size": 55},
                    "padding": {"unit": "px", "top": "10", "right": "20", "bottom": "10", "left": "20", "isLinked": False}
                },
                "elements": [
                    {
                        "id": "w_order_heading",
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": "Đặt mua GOONGBE",
                            "align": "left",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": 26},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "15", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": "w_order_form",
                        "elType": "widget",
                        "widgetType": "form",
                        "settings": {
                            "form_name": "Form Đặt Mua GOONGBE Nhanh",
                            "form_fields": [
                                {"field_type": "select", "field_label": "Sản phẩm chọn mua", "placeholder": "Chọn sản phẩm", "_id": "f_prod"},
                                {"field_type": "number", "field_label": "Số lượng", "placeholder": "1", "_id": "f_qty"},
                                {"field_type": "text", "field_label": "Họ và tên", "placeholder": "Nhập họ tên...", "_id": "f_name"},
                                {"field_type": "tel", "field_label": "Số điện thoại", "placeholder": "Nhập SĐT...", "_id": "f_phone"},
                                {"field_type": "textarea", "field_label": "Địa chỉ giao hàng & Ghi chú", "placeholder": "Nhập địa chỉ cụ thể...", "_id": "f_addr"}
                            ],
                            "button_text": "ĐẶT HÀNG NGAY",
                            "button_background_color": "#F39C12"
                        }
                    }
                ]
            },
            # CỘT PHẢI: Hình Ảnh Trọn Bộ GOONGBE
            {
                "id": "cnt_order_img_col",
                "elType": "container",
                "isInner": True,
                "settings": {
                    "width": {"unit": "%", "size": 42},
                    "flex_direction": "column",
                    "justify_content": "center",
                    "align_items": "center"
                },
                "elements": [
                    {
                        "id": "w_order_img",
                        "elType": "widget",
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "http://chamomdemo.demoweb360.top/wp-content/uploads/2026/08/Goongbe-500X500.jpg"},
                            "align": "center",
                            "width": {"unit": "%", "size": 90}
                        }
                    },
                    {
                        "id": "w_order_hotline_text",
                        "elType": "widget",
                        "widgetType": "heading",
                        "settings": {
                            "title": "Hotline CSKH: <strong>1800 8179</strong>",
                            "align": "center",
                            "title_color": "#E67E22",
                            "typography_font_size": {"unit": "px", "size": 20},
                            "typography_font_weight": "800",
                            "typography_font_family": "Roboto",
                            "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        }
                    }
                ]
            }
        ]
    }

    content_containers = [
        sec1_banner,
        sec2_products_list,
        sec3_cta_blocks,
        sec4_quick_order
    ]

    full_template = {
        "version": "0.4",
        "title": "GOONGBE Product Catalog Page Template (WooCommerce Menu Cart & Products Grid)",
        "type": "page",
        "elementor_version": "3.35.1",
        "content": content_containers,
        "page_settings": []
    }

    json_path = "wp-json-elementor/goongbe-page-product-catalog.json"
    zip_path = "wp-json-elementor/goongbe-page-product-catalog.zip"
    clipboard_path = "wp-json-elementor/goongbe-page-product-catalog-clipboard.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_template, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_containers, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported Elementor Pro WooCommerce Menu Cart & Products Grid JSON to {json_path}")
    print(f"[SUCCESS] Exported Elementor Pro WooCommerce Menu Cart & Products Grid ZIP to {zip_path}")

if __name__ == "__main__":
    build_goongbe_product_catalog_container()
