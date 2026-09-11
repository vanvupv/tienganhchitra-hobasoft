import json
import os

def build_goongbe_product_reviews_json():
    """
    Sinh mã JSON Elementor Pro 3.35.1 / Core 4.2.1 chuẩn 100% FLEXBOX CONTAINER (elType: "container")
    cho KHỐI ĐÁNH GIÁ SẢN PHẨM & BÌNH LUẬN GOONGBE theo đúng mã màu thương hiệu chuẩn:
    
    - Mã màu nền: #E3F7F8
    - Mã tiêu đề: #1B5B65
    - Mã màu giá: #ed9717
    - Màu nút giỏ hàng: #24558f
    - Màu nền xanh nhạt: #ddf3ff
    - Màu nền hồng: #FEF7F7
    - Ngôi sao đánh giá: Màu vàng #ed9717 / #f59e0b
    """

    custom_reviews_css = """
    /* 1. TIÊU ĐỀ & TỔNG ĐÁNH GIÁ */
    selector .woocommerce-Reviews-title,
    selector h2.woocommerce-Reviews-title {
        color: #1B5B65 !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        font-family: 'Roboto', sans-serif !important;
        margin-bottom: 20px !important;
    }

    /* 2. KHUNG THẺ BÌNH LUẬN (COMMENT CARD) */
    selector .commentlist li.comment .comment_container,
    selector ol.commentlist li .comment_container {
        background-color: #ddf3ff !important; /* Nền xanh nhạt chuẩn */
        border: 1px solid #bfe3fc !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 2px 8px rgba(27, 91, 101, 0.05) !important;
    }

    /* 3. TÊN NGUỜI BÌNH LUẬN & NGÀY ĐĂNG */
    selector .comment-text .meta strong {
        color: #1B5B65 !important;
        font-size: 15px !important;
        font-weight: 800 !important;
    }
    selector .comment-text .meta time {
        color: #64748B !important;
        font-size: 13px !important;
    }

    /* 4. ĐÁNH GIÁ NGÔI SAO MÀU VÀNG #ed9717 */
    selector .star-rating,
    selector p.stars a,
    selector .star-rating span::before,
    selector p.stars a::before {
        color: #ed9717 !important; /* Ngôi sao màu vàng chuẩn */
    }

    /* 5. FORM VIẾT ĐÁNH GIÁ MỚI */
    selector #review_form_wrapper {
        background-color: #FEF7F7 !important; /* Nền hồng dịu chuẩn */
        border: 1px solid #FCDDEC !important;
        border-radius: 12px !important;
        padding: 20px 25px !important;
        margin-top: 25px !important;
    }

    selector #reply-title {
        color: #1B5B65 !important;
        font-size: 18px !important;
        font-weight: 800 !important;
    }

    selector input[type="text"],
    selector input[type="email"],
    selector textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #94A3B8 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        color: #1E293B !important;
    }

    selector input[type="text"]:focus,
    selector input[type="email"]:focus,
    selector textarea:focus {
        border-color: #1B5B65 !important;
        outline: none !important;
    }

    /* 6. NÚT GỬI ĐÌNH LUẬN (GỬI ĐỊ) MÀU XANH GIỎ HÀNG #24558f */
    selector #submit,
    selector input[type="submit"] {
        background-color: #24558f !important; /* Màu nút giỏ hàng chuẩn */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 30px !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    selector #submit:hover,
    selector input[type="submit"]:hover {
        background-color: #1B3E6B !important;
        transform: translateY(-1px);
    }
    """

    content_containers = [
        {
            "id": "cnt_product_reviews_main",
            "elType": "container",
            "isInner": False,
            "settings": {
                "content_width": "boxed",
                "flex_direction": "column",
                "background_background": "classic",
                "background_color": "#E3F7F8",
                "padding": {"unit": "px", "top": "35", "right": "30", "bottom": "35", "left": "30", "isLinked": False},
                "border_radius": {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16", "isLinked": True},
                "margin": {"unit": "px", "top": "30", "right": "auto", "bottom": "30", "left": "auto", "isLinked": False}
            },
            "elements": [
                # TIÊU ĐỀ SECTION
                {
                    "id": "w_reviews_sec_heading",
                    "elType": "widget",
                    "widgetType": "heading",
                    "settings": {
                        "title": "Đánh giá sản phẩm",
                        "align": "center",
                        "title_color": "#1B5B65",
                        "typography_font_size": {"unit": "px", "size": 28},
                        "typography_font_weight": "800",
                        "typography_font_family": "Roboto",
                        "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
                    }
                },
                # KHỐI TABS BÌNH LUẬN (TAB 1: FB COMMENTS - TAB 2: BÌNH LUẬN MẶC ĐỊNH)
                {
                    "id": "cnt_reviews_tabs_header",
                    "elType": "container",
                    "isInner": True,
                    "settings": {
                        "content_width": "full",
                        "flex_direction": "row",
                        "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "20", "left": "0", "isLinked": False}
                    },
                    "elements": [
                        {
                            "id": "w_tab_fb_btn",
                            "elType": "widget",
                            "widgetType": "button",
                            "settings": {
                                "text": "BÌNH LUẬN FACEBOOK",
                                "align": "center",
                                "background_color": "#24558f",
                                "button_text_color": "#FFFFFF",
                                "width": {"unit": "%", "size": 50},
                                "border_radius": {"unit": "px", "top": "8", "right": "0", "bottom": "0", "left": "8", "isLinked": False}
                            }
                        },
                        {
                            "id": "w_tab_default_btn",
                            "elType": "widget",
                            "widgetType": "button",
                            "settings": {
                                "text": "BÌNH LUẬN MẶC ĐỊNH",
                                "align": "center",
                                "background_color": "#ed9717",
                                "button_text_color": "#FFFFFF",
                                "width": {"unit": "%", "size": 50},
                                "border_radius": {"unit": "px", "top": "0", "right": "8", "bottom": "8", "left": "0", "isLinked": False}
                            }
                        }
                    ]
                },
                # WIDGET POST COMMENTS VỚI CUSTOM CSS MÀU THƯƠNG HIỆU CHUẨN
                {
                    "id": "w_reviews_post_comments",
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "post-comments",
                    "settings": {
                        "custom_css": custom_reviews_css,
                        "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                    }
                }
            ]
        }
    ]

    full_template = {
        "version": "0.4",
        "title": "GOONGBE Product Reviews Section (Brand Styled Comments)",
        "type": "section",
        "elementor_version": "3.35.1",
        "content": content_containers,
        "page_settings": []
    }

    json_path = "wp-json-elementor/goongbe-product-reviews-section.json"
    clipboard_path = "wp-json-elementor/goongbe-product-reviews-section-clipboard.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(full_template, f, ensure_ascii=False, indent=2)

    with open(clipboard_path, "w", encoding="utf-8") as f:
        json.dump(content_containers, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Exported Product Reviews JSON to {json_path}")
    print(f"[SUCCESS] Exported Product Reviews Clipboard JSON to {clipboard_path}")

if __name__ == "__main__":
    build_goongbe_product_reviews_json()
