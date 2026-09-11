import json
import zipfile
import os

def generate_elementor_json():
    # Helper to generate unique element IDs
    id_counter = 1000
    def get_id(prefix="el"):
        nonlocal id_counter
        id_counter += 1
        return f"{prefix}_{id_counter}"

    # Colors
    PRIMARY_COLOR = "#1B5B65"
    ACCENT_COLOR = "#4CB9CC"
    TEXT_COLOR = "#333333"
    MUTED_TEXT = "#666666"

    sections = []

    # ==========================================
    # SECTION 1: HERO BANNER
    # ==========================================
    sec1 = {
        "id": get_id("sec"),
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "full_width",
            "background_background": "classic",
            "background_color": "#E8F6F9",
            "padding": {"unit": "px", "top": "80", "right": "40", "bottom": "80", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 50, "_inline_size": 50},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "GOONGBE BABY COLLECTION",
                            "header_size": "h4",
                            "title_color": ACCENT_COLOR,
                            "typography_typography": "custom",
                            "typography_font_size": {"unit": "px", "size": "16"},
                            "typography_font_weight": "700",
                            "typography_letter_spacing": {"unit": "px", "size": "2"}
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "AN TOÀN CHO BÉ YÊU TỪ NHỮNG NGÀY ĐẦU ĐỜI",
                            "header_size": "h1",
                            "title_color": PRIMARY_COLOR,
                            "typography_typography": "custom",
                            "typography_font_size": {"unit": "px", "size": "42"},
                            "typography_font_weight": "800",
                            "typography_line_height": {"unit": "em", "size": "1.2"}
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='font-size: 16px; color: #555555; line-height: 1.6;'>Sản phẩm chăm sóc da Hoàng Gia Hàn Quốc dành riêng cho trẻ sơ sinh & trẻ nhỏ. Chiết xuất 100% thảo dược thiên nhiên lành tính, bảo vệ làn da bé luôn mềm mịn và khỏe mạnh.</p>"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "KHÁM PHÁ NGAY",
                            "link": {"url": "#bestseller"},
                            "button_type": "info",
                            "background_color": PRIMARY_COLOR,
                            "button_text_color": "#FFFFFF",
                            "border_radius": {"unit": "px", "top": "30", "right": "30", "bottom": "30", "left": "30"},
                            "padding": {"unit": "px", "top": "15", "right": "35", "bottom": "15", "left": "35", "isLinked": False}
                        }
                    }
                ]
            },
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 50, "_inline_size": 50},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "https://via.placeholder.com/600x400/4CB9CC/ffffff?text=Goongbe+Baby+Collection"},
                            "caption_source": "none",
                            "align": "center"
                        }
                    }
                ]
            }
        ]
    }
    sections.append(sec1)

    # ==========================================
    # SECTION 2: DANH MỤC SẢN PHẨM NỔI BẬT (2 HÀNG X 2 CỘT)
    # ==========================================
    row1_cols = [
        {
            "id": get_id("col"),
            "elType": "column",
            "isInner": False,
            "settings": {"_column_size": 50, "_inline_size": 50},
            "elements": [
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": "https://via.placeholder.com/600x350/E8F6F9/1B5B65?text=NEW+Chong+Nang+Goongbe"},
                        "align": "center",
                        "border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8"}
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "heading",
                    "settings": {
                        "title": "<span style='background:#FF6B35; color:#fff; font-size:12px; font-weight:bold; padding:4px 12px; border-radius:4px; margin-right:8px;'>NEW</span> Bộ sản phẩm chống nắng GOONGBE",
                        "header_size": "h4",
                        "align": "center",
                        "title_color": PRIMARY_COLOR,
                        "typography_font_size": {"unit": "px", "size": "17"},
                        "typography_font_weight": "700",
                        "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
                    }
                }
            ]
        },
        {
            "id": get_id("col"),
            "elType": "column",
            "isInner": False,
            "settings": {"_column_size": 50, "_inline_size": 50},
            "elements": [
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": "https://via.placeholder.com/600x350/D8F1F5/1B5B65?text=BEST+Nang+Cap+Ao+Duoc"},
                        "align": "center",
                        "border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8"}
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "heading",
                    "settings": {
                        "title": "<span style='background:#009AA5; color:#fff; font-size:12px; font-weight:bold; padding:4px 12px; border-radius:4px; margin-right:8px;'>BEST</span> Bộ Sản Phẩm GOONGBE Nâng Cấp Áo Dược",
                        "header_size": "h4",
                        "align": "center",
                        "title_color": PRIMARY_COLOR,
                        "typography_font_size": {"unit": "px", "size": "17"},
                        "typography_font_weight": "700",
                        "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
                    }
                }
            ]
        }
    ]

    row2_cols = [
        {
            "id": get_id("col"),
            "elType": "column",
            "isInner": False,
            "settings": {"_column_size": 50, "_inline_size": 50},
            "elements": [
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": "https://via.placeholder.com/600x350/FFF3B0/1B5B65?text=GOONGBE+x+YUMMA+Yellow"},
                        "align": "center",
                        "border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8"}
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "heading",
                    "settings": {
                        "title": "Bộ Sản Phẩm GOONGBE x YUMMA Chăm Sóc Da Bé",
                        "header_size": "h4",
                        "align": "center",
                        "title_color": PRIMARY_COLOR,
                        "typography_font_size": {"unit": "px", "size": "17"},
                        "typography_font_weight": "700",
                        "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "15", "left": "0", "isLinked": False}
                    }
                }
            ]
        },
        {
            "id": get_id("col"),
            "elType": "column",
            "isInner": False,
            "settings": {"_column_size": 50, "_inline_size": 50},
            "elements": [
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": "https://via.placeholder.com/600x350/C7F9CC/1B5B65?text=GOONGBE+x+YUMMA+Green"},
                        "align": "center",
                        "border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8"}
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "heading",
                    "settings": {
                        "title": "Dòng Sản Phẩm Trẻ Em GOONGBE x YUMMA",
                        "header_size": "h4",
                        "align": "center",
                        "title_color": PRIMARY_COLOR,
                        "typography_font_size": {"unit": "px", "size": "17"},
                        "typography_font_weight": "700",
                        "margin": {"unit": "px", "top": "15", "right": "0", "bottom": "15", "left": "0", "isLinked": False}
                    }
                }
            ]
        }
    ]

    sec2 = {
        "id": get_id("sec"),
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": get_id("col_header"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "DANH MỤC SẢN PHẨM NỔI BẬT",
                            "header_size": "h2",
                            "align": "center",
                            "title_color": PRIMARY_COLOR,
                            "typography_font_size": {"unit": "px", "size": "32"},
                            "typography_font_weight": "800"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='text-align: center; color: #666; font-size: 16px; margin-bottom: 40px;'>Chăm sóc dịu nhẹ và nâng niu làn da bé trong những năm tháng đầu đời</p>"
                        }
                    },
                    {
                        "id": get_id("sec_inner_row1"),
                        "elType": "section",
                        "isInner": True,
                        "settings": {},
                        "elements": row1_cols
                    },
                    {
                        "id": get_id("sec_inner_row2"),
                        "elType": "section",
                        "isInner": True,
                        "settings": {},
                        "elements": row2_cols
                    }
                ]
            }
        ]
    }
    sections.append(sec2)

    # ==========================================
    # SECTION 3: FEATURED PROMO BANNER (DƯỠNG ẨM 48H)
    # ==========================================
    sec3 = {
        "id": get_id("sec"),
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": "#D8F1F5",
            "padding": {"unit": "px", "top": "70", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "DƯỠNG ẨM TOÀN THÂN 48 GIỜ PHỤC HỒI DA NHẠY CẢM",
                            "header_size": "h2",
                            "align": "center",
                            "title_color": PRIMARY_COLOR,
                            "typography_font_size": {"unit": "px", "size": "34"},
                            "typography_font_weight": "800"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='text-align: center; color: #444; font-size: 17px; max-width: 800px; margin: 0 auto 25px auto;'>Công thức độc quyền Oji Relief Complex từ 5 loại thảo dược Hoàng Gia Hàn Quốc giúp tăng cường hàng rào tự nhiên, cấp ẩm chuyên sâu và ngăn ngừa mẩn đỏ cho bé.</p>"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "TÌM HIỂU CÔNG THỨC OJI RELIEF",
                            "align": "center",
                            "background_color": PRIMARY_COLOR,
                            "button_text_color": "#FFFFFF",
                            "border_radius": {"unit": "px", "top": "25", "right": "25", "bottom": "25", "left": "25"}
                        }
                    }
                ]
            }
        ]
    }
    sections.append(sec3)

    # ==========================================
    # SECTION 4: BEST SELLERS (TOP SẢN PHẨM BÁN CHẠY)
    # ==========================================
    sec4_cols = []
    products = [
        {"name": "Kem Dưỡng Ẩm Pri-mmune Moisture Cream 180ml", "price": "650.000đ", "tag": "BESTSELLER"},
        {"name": "Sữa Tắm Gội 2in1 Pri-mmune Shampoo & Bath 350ml", "price": "520.000đ", "tag": "TOP 1"},
        {"name": "Sữa Dưỡng Thể Pri-mmune Moisture Lotion 350ml", "price": "580.000đ", "tag": "HOT"},
        {"name": "Kem Chống Nắng Dạng Thỏi Fresh Sun Stick SPF50+", "price": "490.000đ", "tag": "NEW"}
    ]

    for p in products:
        sec4_cols.append({
            "id": get_id("col"),
            "elType": "column",
            "isInner": False,
            "settings": {"_column_size": 25, "_inline_size": 25},
            "elements": [
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": "https://via.placeholder.com/260x260/ffffff/1B5B65?text=Goongbe+Product"},
                        "align": "center"
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "heading",
                    "settings": {
                        "title": f"<span style='color:#4CB9CC; font-size:12px; font-weight:bold;'>[{p['tag']}]</span><br>{p['name']}",
                        "header_size": "h4",
                        "align": "center",
                        "title_color": TEXT_COLOR,
                        "typography_font_size": {"unit": "px", "size": "15"},
                        "typography_font_weight": "600"
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p style='text-align: center; color: #1B5B65; font-weight: bold; font-size: 16px;'>{p['price']}</p>"
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "button",
                    "settings": {
                        "text": "THÊM VÀO GIỎ",
                        "align": "center",
                        "background_color": "#4CB9CC",
                        "button_text_color": "#FFFFFF",
                        "border_radius": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20"}
                    }
                }
            ]
        })

    sec4 = {
        "id": get_id("sec"),
        "elType": "section",
        "isInner": False,
        "settings": {
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "GOONGBE's Best Sellers",
                            "header_size": "h2",
                            "align": "center",
                            "title_color": PRIMARY_COLOR,
                            "typography_font_size": {"unit": "px", "size": "32"},
                            "typography_font_weight": "800"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='text-align: center; color: #666; font-size: 16px; margin-bottom: 30px;'>Bộ 3 sản phẩm bán chạy nhất: Kem dưỡng ẩm - Sữa tắm gội - Lotion</p>"
                        }
                    },
                    {
                        "id": get_id("sec_inner"),
                        "elType": "section",
                        "isInner": True,
                        "settings": {},
                        "elements": sec4_cols
                    }
                ]
            }
        ]
    }
    sections.append(sec4)

    # ==========================================
    # SECTION 5: MÂY - NHÂN VẬT HOẠT HÌNH (GOONGBE MASCOT VIETNAM)
    # ==========================================
    sec_may = {
        "id": get_id("sec"),
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": "#E5F6F8",
            "padding": {"unit": "px", "top": "70", "right": "50", "bottom": "70", "left": "50", "isLinked": False}
        },
        "elements": [
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 50, "_inline_size": 50},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Mây - Nhân vật hoạt hình tại thị trường Việt Nam",
                            "header_size": "h2",
                            "title_color": PRIMARY_COLOR,
                            "typography_font_size": {"unit": "px", "size": "30"},
                            "typography_font_weight": "700"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "divider",
                        "settings": {
                            "color": ACCENT_COLOR,
                            "weight": {"unit": "px", "size": "3"},
                            "width": {"unit": "%", "size": "15"},
                            "align": "left",
                            "gap": {"unit": "px", "size": "15"}
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='color: #444444; font-size: 16px; line-height: 1.7; margin-top: 15px; margin-bottom: 25px;'>MÂY – nhân vật hoạt hình siêu đáng yêu từ GOONGBE đã chính thức \"đổ bộ\" tại Việt Nam! Với đôi má hồng xinh xắn, bước nhảy lả lướt và chiếc mũ đỏ nổi bật. Nhân vật Mây hứa hẹn sẽ là người bạn đồng hành cùng các bé trong những hoạt động siêu đáng yêu, siêu thú vị sắp tới của Goongbe tại Việt Nam!</p>"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "Xem trên Youtube",
                            "link": {"url": "https://www.youtube.com/@GOONGBEVietNam"},
                            "button_type": "default",
                            "background_color": "#FFFFFF",
                            "button_text_color": ACCENT_COLOR,
                            "border_border": "solid",
                            "border_color": ACCENT_COLOR,
                            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1"},
                            "border_radius": {"unit": "px", "top": "4", "right": "4", "bottom": "4", "left": "4"},
                            "padding": {"unit": "px", "top": "12", "right": "30", "bottom": "12", "left": "30", "isLinked": False}
                        }
                    }
                ]
            },
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 50, "_inline_size": 50},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "image",
                        "settings": {
                            "image": {"url": "https://via.placeholder.com/550x400/E5F6F8/1B5B65?text=May+-+Goongbe+Mascot"},
                            "align": "center"
                        }
                    }
                ]
            }
        ]
    }
    sections.append(sec_may)

    # ==========================================
    # SECTION 6: ĐỐI TÁC CHÍNH THỨC (OFFICIAL PARTNERS)
    # ==========================================
    partners = [
        {"name": "Olive Young", "desc": "Hệ thống mỹ phẩm số 1 Hàn Quốc", "img": "https://via.placeholder.com/200x80/ffffff/1B5B65?text=OLIVE+YOUNG"},
        {"name": "Shinsegae", "desc": "TTTM Cao cấp Shinsegae", "img": "https://via.placeholder.com/200x80/ffffff/1B5B65?text=SHINSEGAE"},
        {"name": "Hyundai Mall", "desc": "Hệ thống Bách hóa Hyundai", "img": "https://via.placeholder.com/200x80/ffffff/1B5B65?text=HYUNDAI"},
        {"name": "Lotte Mart", "desc": "Siêu thị & TTTM Lotte", "img": "https://via.placeholder.com/200x80/ffffff/1B5B65?text=LOTTE"},
        {"name": "Concung", "desc": "Chuỗi siêu thị Mẹ & Bé toàn quốc", "img": "https://via.placeholder.com/200x80/ffffff/1B5B65?text=CON+CUNG"},
        {"name": "Shopee Mall", "desc": "Gian hàng chính hãng Shopee", "img": "https://via.placeholder.com/200x80/ffffff/1B5B65?text=SHOPEE+MALL"}
    ]

    partner_cols = []
    for partner in partners:
        partner_cols.append({
            "id": get_id("col"),
            "elType": "column",
            "isInner": False,
            "settings": {"_column_size": 16.66, "_inline_size": 16.66},
            "elements": [
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": partner["img"]},
                        "align": "center",
                        "border_border": "solid",
                        "border_color": "#E5E7EB",
                        "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1"},
                        "border_radius": {"unit": "px", "top": "10", "right": "10", "bottom": "10", "left": "10"}
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "heading",
                    "settings": {
                        "title": partner["name"],
                        "header_size": "h5",
                        "align": "center",
                        "title_color": PRIMARY_COLOR,
                        "typography_font_size": {"unit": "px", "size": "14"},
                        "typography_font_weight": "700"
                    }
                }
            ]
        })

    sec_partners = {
        "id": get_id("sec"),
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": "#F4FAFC",
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "ĐỐI TÁC CHÍNH THỨC",
                            "header_size": "h2",
                            "align": "center",
                            "title_color": PRIMARY_COLOR,
                            "typography_font_size": {"unit": "px", "size": "32"},
                            "typography_font_weight": "800"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='text-align: center; color: #666; font-size: 16px; margin-bottom: 35px;'>GOONGBE tự hào hợp tác cùng các hệ thống phân phối & bán lẻ uy tín hàng đầu</p>"
                        }
                    },
                    {
                        "id": get_id("sec_inner"),
                        "elType": "section",
                        "isInner": True,
                        "settings": {},
                        "elements": partner_cols
                    }
                ]
            }
        ]
    }
    sections.append(sec_partners)

    # ==========================================
    # SECTION 7: GOONGBE'S NEWS (TIN TỨC VÀ TRUYỀN THÔNG - QUERY POST MOCKUP)
    # ==========================================
    news_cols = []
    posts_mock = [
        {
            "tag": "LỜI KHUYÊN BÁC SĨ",
            "title": "Chuyên gia da liễu hướng dẫn chọn kem dưỡng ẩm an toàn cho trẻ sơ sinh",
            "date": "03/08/2026",
            "excerpt": "Làn da trẻ sơ sinh mỏng hơn 30% so với người lớn, việc lựa chọn sản phẩm chứa phức hợp thảo dược tự nhiên lành tính giúp bảo vệ màng ẩm mỏng mong của bé...",
            "img": "https://via.placeholder.com/400x250/1B5B65/ffffff?text=Bac+Si+Da+Lieu"
        },
        {
            "tag": "SỰ KIỆN Y KHOA",
            "title": "Goongbe đồng hành cùng Hội thảo Khoa học Chăm sóc da Nhi khoa 2026",
            "date": "28/07/2026",
            "excerpt": "Hơn 200 bác sĩ da liễu đầu ngành đã tham dự và đánh giá cao hiệu quả thực tế của dòng sản phẩm Pri-mmune trong việc làm dịu da viêm cơ địa ở trẻ nhỏ...",
            "img": "https://via.placeholder.com/400x250/4CB9CC/ffffff?text=Hoi+Thao+Y+Khoa"
        },
        {
            "tag": "TIN NỔI BẬT",
            "title": "Ra mắt dòng sản phẩm Pri-mmune thế hệ mới nâng cấp gấp 2 lần dưỡng chất",
            "date": "15/07/2026",
            "excerpt": "Đột phá với công thức Oji Relief Complex giúp tăng cường sức đề kháng cho làn da bé ngay từ những tháng đầu đời trước tác động môi trường bên ngoài...",
            "img": "https://via.placeholder.com/400x250/1B5B65/ffffff?text=Su+Kien+Ra+Mat"
        }
    ]

    for post in posts_mock:
        news_cols.append({
            "id": get_id("col"),
            "elType": "column",
            "isInner": False,
            "settings": {"_column_size": 33, "_inline_size": 33.33},
            "elements": [
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "image",
                    "settings": {
                        "image": {"url": post["img"]},
                        "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "0", "left": "0"}
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<span style='background: #E8F6F9; color: #1B5B65; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px;'>{post['tag']}</span> <span style='color: #888; font-size: 12px; margin-left: 10px;'>📅 {post['date']}</span>"
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "heading",
                    "settings": {
                        "title": post["title"],
                        "header_size": "h3",
                        "title_color": TEXT_COLOR,
                        "typography_font_size": {"unit": "px", "size": "17"},
                        "typography_font_weight": "700",
                        "typography_line_height": {"unit": "em", "size": "1.3"}
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "text-editor",
                    "settings": {
                        "editor": f"<p style='color: #666666; font-size: 14px; line-height: 1.5;'>{post['excerpt']}</p>"
                    }
                },
                {
                    "id": get_id("widget"),
                    "elType": "widget",
                    "isInner": False,
                    "widgetType": "button",
                    "settings": {
                        "text": "Đọc tiếp →",
                        "button_type": "link",
                        "button_text_color": PRIMARY_COLOR,
                        "typography_font_weight": "700"
                    }
                }
            ]
        })

    sec7 = {
        "id": get_id("sec"),
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": "#FAF9F6",
            "padding": {"unit": "px", "top": "70", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "GOONGBE's News",
                            "header_size": "h2",
                            "align": "center",
                            "title_color": PRIMARY_COLOR,
                            "typography_font_size": {"unit": "px", "size": "34"},
                            "typography_font_weight": "800"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "Tin tức & Truyền thông",
                            "header_size": "h4",
                            "align": "center",
                            "title_color": ACCENT_COLOR,
                            "typography_font_size": {"unit": "px", "size": "20"},
                            "typography_font_weight": "600",
                            "margin": {"unit": "px", "top": "-10", "right": "0", "bottom": "35", "left": "0", "isLinked": False}
                        }
                    },
                    {
                        "id": get_id("sec_inner"),
                        "elType": "section",
                        "isInner": True,
                        "settings": {},
                        "elements": news_cols
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "XEM TẤT CẢ TIN TỨC",
                            "align": "center",
                            "background_color": PRIMARY_COLOR,
                            "button_text_color": "#FFFFFF",
                            "border_radius": {"unit": "px", "top": "25", "right": "25", "bottom": "25", "left": "25"},
                            "margin": {"unit": "px", "top": "35", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        }
                    }
                ]
            }
        ]
    }
    sections.append(sec7)

    # ==========================================
    # SECTION 8: FOOTER CTA BANNER (KHÔNG BAO GỒM FOOTER)
    # ==========================================
    sec8 = {
        "id": get_id("sec"),
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": PRIMARY_COLOR,
            "padding": {"unit": "px", "top": "60", "right": "40", "bottom": "60", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": get_id("col"),
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "DÀNH CHO LÀN DA NHẠY CẢM CỦA BÉ YÊU",
                            "header_size": "h2",
                            "align": "center",
                            "title_color": "#FFFFFF",
                            "typography_font_size": {"unit": "px", "size": "30"},
                            "typography_font_weight": "700"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "text-editor",
                        "settings": {
                            "editor": "<p style='text-align: center; color: #E8F6F9; font-size: 16px; margin-bottom: 25px;'>Hãy để Goongbe cùng mẹ bảo vệ làn da bé mỗi ngày với tình yêu thương dịu nhẹ nhất từ thiên nhiên.</p>"
                        }
                    },
                    {
                        "id": get_id("widget"),
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "button",
                        "settings": {
                            "text": "LIÊN HỆ TƯ VẤN NGAY",
                            "align": "center",
                            "background_color": ACCENT_COLOR,
                            "button_text_color": "#FFFFFF",
                            "border_radius": {"unit": "px", "top": "25", "right": "25", "bottom": "25", "left": "25"}
                        }
                    }
                ]
            }
        ]
    }
    sections.append(sec8)

    # Elementor 3.x Standard Export Root Format
    elementor_export = {
        "version": "3.0.0",
        "elementor_version": "3.35.1",
        "title": "Trang Chủ GOONGBE VN - Cha & Mom",
        "type": "page",
        "page_settings": {},
        "content": sections
    }

    return elementor_export

if __name__ == "__main__":
    data = generate_elementor_json()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "goongbe-homepage-elementor-template.json")
    zip_path = os.path.join(script_dir, "goongbe-homepage-elementor-template.zip")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname="goongbe-homepage-elementor-template.json")

    print("Success updating elementor template inside wp-json-elementor directory!")
