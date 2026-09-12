import json
import zipfile
import os
import uuid

def gen_id():
    return uuid.uuid4().hex[:8]

# ==============================================================================
# BẢNG MÃ MÀU CHUẨN DỰ ÁN TIẾNG ANH CHỊ TRÀ
# ==============================================================================
COLOR_PRIMARY_BLUE  = "#007BFF"  # Màu chủ đạo - Xanh dương
COLOR_PRIMARY_GREEN = "#28A745"  # Màu chủ đạo - Xanh lá
COLOR_TEXT_BLACK    = "#000000"  # Màu văn bản chuẩn
COLOR_TEXT_WHITE    = "#FFFFFF"  # Màu chữ trên nền màu
COLOR_BTN_ORANGE    = "#ED9717"  # Màu nút nổi bật - Màu cam
COLOR_BORDER_GRAY   = "#DEE2E6"  # Màu viền phẳng tinh tế

def create_container(direction="column", content_width="boxed", width=1200, padding_top="30", padding_bottom="30", padding_left="40", padding_right="40", bg_color="", bg_gradient=None):
    """Tạo Flexbox Container chuẩn Elementor 3.x - HOÀN TOÀN KHÔNG DÙNG CUSTOM CSS"""
    settings = {
        "flex_direction": direction,
        "content_width": content_width,
        "padding": {
            "unit": "px",
            "top": str(padding_top),
            "right": str(padding_right),
            "bottom": str(padding_bottom),
            "left": str(padding_left),
            "isLinked": False
        }
    }
    if content_width == "boxed" and width:
        settings["width"] = {"unit": "px", "size": width}
    if bg_color:
        settings["background_background"] = "classic"
        settings["background_color"] = bg_color
    if bg_gradient:
        settings["background_background"] = "gradient"
        settings["background_color"] = bg_gradient.get("color", COLOR_PRIMARY_GREEN)
        settings["background_color_b"] = bg_gradient.get("color_b", "#1E7E34")
        settings["background_gradient_type"] = bg_gradient.get("type", "linear")
        settings["background_gradient_angle"] = {"unit": "deg", "size": bg_gradient.get("angle", 135)}

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": settings,
        "elements": []
    }

def create_heading(title, size="h2", align="center", color=COLOR_TEXT_BLACK, font_size=28, font_weight="800"):
    """Tạo Heading thuần Elementor Native Settings"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "heading",
        "isInner": False,
        "settings": {
            "title": title,
            "header_size": size,
            "align": align,
            "title_color": color,
            "typography_typography": "custom",
            "typography_font_family": "Plus Jakarta Sans",
            "typography_font_size": {"unit": "px", "size": font_size},
            "typography_font_weight": str(font_weight),
            "typography_line_height": {"unit": "em", "size": 1.2}
        },
        "elements": []
    }

def create_text_editor(text, align="center", color=COLOR_TEXT_BLACK, font_size=15):
    """Tạo Text Editor thuần Elementor Native Settings"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "text-editor",
        "isInner": False,
        "settings": {
            "editor": text,
            "align": align,
            "text_color": color,
            "typography_typography": "custom",
            "typography_font_family": "Plus Jakarta Sans",
            "typography_font_size": {"unit": "px", "size": font_size},
            "typography_line_height": {"unit": "em", "size": 1.6}
        },
        "elements": []
    }

def create_divider(color=COLOR_BTN_ORANGE, width=80):
    """Tạo Divider thuần Elementor Native Settings"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "divider",
        "isInner": False,
        "settings": {
            "color": color,
            "weight": {"unit": "px", "size": 3},
            "width": {"unit": "px", "size": width},
            "align": "center",
            "gap": {"unit": "px", "size": 15}
        },
        "elements": []
    }

def create_posts_widget(post_type="post", columns="3", posts_per_page="3", show_image="yes", show_title="yes", title_color=COLOR_TEXT_BLACK, show_excerpt="yes", excerpt_color=COLOR_TEXT_BLACK, show_read_more="yes", read_more_text="Xem thêm »", read_more_color=COLOR_BTN_ORANGE, bg_box_color="", border_box_color="", border_radius=8, content_padding=15):
    """
    Sinh Widget Posts thuần 100% Cài đặt gốc Elementor Pro:
    - Query tự động theo Post Type (giang_vien, khoa_hoc, hoc_vien, post)
    - Tự động lấy Featured Image (Ảnh đại diện), Tiêu đề, Trích dẫn và Link chi tiết
    - 100% KHÔNG DÙNG CUSTOM CSS, KHÔNG DÙNG BOX-SHADOW
    """
    settings = {
        "_skin": "classic",
        "posts_post_type": post_type,
        "classic_columns": str(columns),
        "classic_columns_tablet": "2",
        "classic_columns_mobile": "1",
        "classic_posts_per_page": str(posts_per_page),
        "classic_show_image": show_image,
        "classic_image_size": "medium_large",
        "classic_show_title": show_title,
        "classic_title_color": title_color,
        "classic_show_excerpt": show_excerpt,
        "classic_excerpt_color": excerpt_color,
        "classic_show_read_more": show_read_more,
        "classic_read_more_text": read_more_text,
        "classic_read_more_color": read_more_color,
        "classic_meta_data": ["date"] if post_type == "post" else [],
        "classic_content_padding": {
            "unit": "px",
            "top": str(content_padding),
            "right": str(content_padding),
            "bottom": str(content_padding),
            "left": str(content_padding),
            "isLinked": True
        }
    }

    if bg_box_color:
        settings["classic_box_bg_color"] = bg_box_color
    if border_box_color:
        settings["classic_box_border_color"] = border_box_color
        settings["classic_box_border_width"] = {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}
    if border_radius:
        settings["classic_box_border_radius"] = {"unit": "px", "top": str(border_radius), "right": str(border_radius), "bottom": str(border_radius), "left": str(border_radius), "isLinked": True}

    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "posts",
        "isInner": False,
        "settings": settings,
        "elements": []
    }

def create_loop_carousel_widget(post_type="post", slides_to_show="4", posts_per_page=8, template_id=""):
    """
    Sinh Widget Loop Carousel chuẩn Native của Elementor Pro 3.35+:
    - Động cơ Swiper.js native, vuốt trượt cảm ứng mượt mà trên mobile
    - Query động Custom Post Types (giang_vien, hoc_vien, post)
    - Tự động căn chỉnh chiều cao các thẻ (equal_height: yes)
    - Tích hợp sẵn Navigation Arrows và Pagination Dots
    """
    settings = {
        "_skin": "post",
        "post_query_post_type": post_type,
        "posts_per_page": posts_per_page,
        "slides_to_show": str(slides_to_show),
        "slides_to_show_tablet": "2",
        "slides_to_show_mobile": "1",
        "slides_to_scroll": "1",
        "equal_height": "yes",
        "autoplay": "yes",
        "autoplay_speed": 4000,
        "pause_on_hover": "yes",
        "pause_on_interaction": "yes",
        "infinite": "yes",
        "speed": 500,
        "arrows": "yes",
        "pagination": "dots",
        "arrows_color": COLOR_BTN_ORANGE,
        "dots_color": COLOR_BTN_ORANGE,
        "image_spacing_custom": {"unit": "px", "size": 20}
    }
    if template_id:
        settings["template_id"] = str(template_id)

    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "loop-carousel",
        "isInner": False,
        "settings": settings,
        "elements": []
    }

def create_reviews_widget(slides, slides_per_view=3):
    """
    Sinh Widget Reviews chính thức của Elementor Pro:
    - 100% Cài đặt gốc, KHÔNG DÙNG CUSTOM CSS, KHÔNG DÙNG BOX-SHADOW
    """
    slides_data = []
    for idx, s in enumerate(slides):
        slides_data.append({
            "_id": f"rev_slide_{idx + 1}",
            "image": {"url": s.get("avatar", "")},
            "name": s.get("name", "Học viên"),
            "title": s.get("job", "Phụ huynh"),
            "rating": s.get("rating", 5),
            "content": s.get("quote", "")
        })

    settings = {
        "slides": slides_data,
        "slides_per_view": str(slides_per_view),
        "slides_per_view_tablet": "2",
        "slides_per_view_mobile": "1",
        "slides_to_scroll": "1",
        "show_arrows": "yes",
        "pagination": "dots",
        "speed": 500,
        "autoplay": "yes",
        "autoplay_speed": 4000,
        "loop": "yes",
        "pause_on_hover": "yes",
        "name_color": COLOR_TEXT_BLACK,
        "title_color": "#64748B",
        "content_color": COLOR_TEXT_BLACK,
        "star_color": COLOR_BTN_ORANGE,
        "arrows_color": COLOR_BTN_ORANGE
    }

    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "reviews",
        "isInner": False,
        "settings": settings,
        "elements": []
    }

def create_popout_course_card(bg_color, img_url, title, desc, link="#"):
    """
    Tạo Container Thẻ Khóa Học 3D Pop-out chuẩn xác 100% theo Mẫu (Ảnh 3):
    - Cấu trúc 2 tầng chuẩn:
      + Tầng 1 (box-image): Nhân vật 3D nổi bật đè lên với margin-bottom âm (-140px), z-index 3 (không bị mask cắt).
      + Tầng 2 (box-text): Khối nền đỏ (#CD2828) với padding-top 155px,
        tích hợp Mask SVG Data-URI Vector chuẩn xác (không phụ thuộc domain ngoài, không bị lỗi CORS),
        đồng thời có custom_css cho Elementor Pro và class 'sla-card-mask' cho CSS tùy biến.
    """
    card_id = gen_id()
    img_id = gen_id()
    box_text_id = gen_id()
    title_id = gen_id()
    desc_id = gen_id()
    btn_id = gen_id()

    mask_svg = "data:image/svg+xml,%3Csvg viewBox='0 0 360 420' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M180 0 C280 0, 360 40, 360 120 L360 360 C360 400, 310 420, 180 420 C50 420, 0 400, 0 360 L0 120 C0 40, 80 0, 180 0 Z' fill='black'/%3E%3C/svg%3E"
    custom_css_mask = (
        "selector {\n"
        f"  -webkit-mask-image: url(\"{mask_svg}\");\n"
        f"  mask-image: url(\"{mask_svg}\");\n"
        "  -webkit-mask-size: 100% 100%;\n"
        "  mask-size: 100% 100%;\n"
        "  -webkit-mask-repeat: no-repeat;\n"
        "  mask-repeat: no-repeat;\n"
        "  -webkit-mask-position: center;\n"
        "  mask-position: center;\n"
        "}"
    )

    return {
        "id": card_id,
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "width": {"unit": "%", "size": 31.5},
            "width_tablet": {"unit": "%", "size": 48},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "flex-start",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
            "margin": {"unit": "px", "top": "20", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
            "overflow": "visible"
        },
        "elements": [
            # TẦNG 1: ẢNH NHÂN VẬT 3D ĐÈ LÊN TRÊN (KHÔNG BỊ CẮT XÉN)
            {
                "id": img_id,
                "elType": "widget",
                "widgetType": "image",
                "isInner": False,
                "settings": {
                    "image": {
                        "url": img_url,
                        "id": 0
                    },
                    "image_size": "full",
                    "align": "center",
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "-140",
                        "left": "0",
                        "isLinked": False
                    },
                    "_margin_mobile": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "-120",
                        "left": "0",
                        "isLinked": False
                    },
                    "_z_index": 3
                },
                "elements": []
            },
            # TẦNG 2: HỘP NỘI DUNG VĂN BẢN (NỀN ĐỎ + MASK DÁNG VÒM CONG 2 ĐẦU CHUẨN MẪU)
            {
                "id": box_text_id,
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "column",
                    "align_items": "center",
                    "justify_content": "space-between",
                    "background_background": "classic",
                    "background_color": bg_color,
                    # Bo góc vòm cong sâu ở 2 đầu (Fallback hoàn hảo cho mọi trình duyệt)
                    "border_radius": {
                        "unit": "px",
                        "top": "80",
                        "right": "80",
                        "bottom": "45",
                        "left": "45",
                        "isLinked": False
                    },
                    "padding": {
                        "unit": "px",
                        "top": "155",
                        "right": "24",
                        "bottom": "35",
                        "left": "24",
                        "isLinked": False
                    },
                    "padding_mobile": {
                        "unit": "px",
                        "top": "135",
                        "right": "20",
                        "bottom": "30",
                        "left": "20",
                        "isLinked": False
                    },
                    "_css_classes": "sla-card-mask",
                    "custom_css": custom_css_mask
                },
                "elements": [
                    {
                        "id": title_id,
                        "elType": "widget",
                        "widgetType": "heading",
                        "isInner": False,
                        "settings": {
                            "title": title,
                            "header_size": "h3",
                            "align": "center",
                            "title_color": COLOR_TEXT_WHITE,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 22},
                            "typography_font_size_mobile": {"unit": "px", "size": 20},
                            "typography_font_weight": "800",
                            "typography_line_height": {"unit": "em", "size": 1.2},
                            "_margin": {
                                "unit": "px",
                                "top": "0",
                                "right": "0",
                                "bottom": "12",
                                "left": "0",
                                "isLinked": False
                            }
                        },
                        "elements": []
                    },
                    {
                        "id": desc_id,
                        "elType": "widget",
                        "widgetType": "text-editor",
                        "isInner": False,
                        "settings": {
                            "editor": f"<p>{desc}</p>",
                            "align": "center",
                            "text_color": "rgba(255, 255, 255, 0.95)",
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "typography_line_height": {"unit": "em", "size": 1.6},
                            "_margin": {
                                "unit": "px",
                                "top": "0",
                                "right": "0",
                                "bottom": "25",
                                "left": "0",
                                "isLinked": False
                            }
                        },
                        "elements": []
                    },
                    {
                        "id": btn_id,
                        "elType": "widget",
                        "widgetType": "button",
                        "isInner": False,
                        "settings": {
                            "text": "→",
                            "link": {"url": link, "is_external": "", "nofollow": ""},
                            "align": "center",
                            "button_text_color": "#222222",
                            "background_color": "#FFFFFF",
                            "border_radius": {
                                "unit": "px",
                                "top": "99",
                                "right": "99",
                                "bottom": "99",
                                "left": "99",
                                "isLinked": True
                            },
                            "padding": {
                                "unit": "px",
                                "top": "10",
                                "right": "18",
                                "bottom": "10",
                                "left": "18",
                                "isLinked": False
                            },
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 22},
                            "typography_font_weight": "900"
                        },
                        "elements": []
                    }
                ]
            }
        ]
    }

def build_homepage_json():
    # -------------------------------------------------------------
    # SECTION 1: BANNER FULL WIDTH
    # -------------------------------------------------------------
    sec1 = create_container(content_width="full", padding_top="0", padding_bottom="0", padding_left="0", padding_right="0")
    sec1["settings"]["stretch_section"] = "section-stretched"
    sec1["settings"]["layout"] = "full_width"
    sec1["elements"].append({
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "image",
        "isInner": False,
        "settings": {
            "image": {
                "url": "https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=1920&auto=format&fit=crop",
                "id": 0
            },
            "image_size": "full",
            "align": "center"
        },
        "elements": []
    })

    # -------------------------------------------------------------
    # SECTION 2: ĐỘI NGŨ GIẢNG VIÊN - LOOP CAROUSEL (Post Type: giang_vien)
    # -------------------------------------------------------------
    sec2 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="45",
        padding_bottom="45",
        padding_left="20",
        padding_right="20"
    )
    sec2["elements"].append(create_heading("ĐỘI NGŨ GIẢNG VIÊN TẠI TIẾNG ANH CHỊ TRÀ", size="h2", align="center", color=COLOR_PRIMARY_GREEN, font_size=28, font_weight="800"))
    sec2["elements"].append(create_divider(color=COLOR_BTN_ORANGE, width=90))
    sec2["elements"].append(create_text_editor(
        "<p>Chặng đường phía trước còn nhiều gian nan, nhưng với tâm huyết và say mê ngành giáo dục tri thức của mình, đội ngũ giảng viên luôn tràn đầy năng lượng đồng hành cùng học viên tiến về phía trước.</p>",
        align="center",
        color="#4A5568",
        font_size=15
    ))

    # Widget Loop Carousel query Post Type giang_vien (4 Slides trên Desktop, Swiper Slider Native)
    sec2["elements"].append(create_loop_carousel_widget(
        post_type="giang_vien",
        slides_to_show="4",
        posts_per_page=8
    ))

    # -------------------------------------------------------------
    # SECTION 3: CHƯƠNG TRÌNH ĐÀO TẠO TIẾNG ANH (Chuẩn 100% theo Mẫu Ảnh 3 - Đỏ Đồng Bộ + Dáng Bo 2 Đầu)
    # -------------------------------------------------------------
    sec3 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="45",
        padding_bottom="45",
        padding_left="20",
        padding_right="20"
    )
    sec3["elements"].append(create_heading("CHƯƠNG TRÌNH ĐÀO TẠO TIẾNG ANH", size="h2", align="center", color=COLOR_PRIMARY_BLUE, font_size=28, font_weight="800"))
    sec3["elements"].append(create_divider(color=COLOR_BTN_ORANGE, width=80))

    # Row container chứa 3 thẻ khóa học pop-out
    courses_row = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "flex_direction_tablet": "row",
            "flex_direction_mobile": "column",
            "justify_content": "space-between",
            "align_items": "stretch",
            "flex_wrap": "wrap",
            "gap": {"unit": "px", "size": 25, "column": 25, "row": 30},
            "padding": {"unit": "px", "top": "15", "right": "0", "bottom": "15", "left": "0", "isLinked": False}
        },
        "elements": [
            # Thẻ 1: KINDY (4–6 tuổi) - Bé gái đọc sách + số 1 (Đỏ #CD2828)
            create_popout_course_card(
                bg_color="#CD2828",
                img_url="https://hocvienngoaingusla.edu.vn/wp-content/uploads/2025/05/image-program-5-1.png",
                title="KINDY (4–6 tuổi)",
                desc="Chương trình KINDY giúp trẻ mẫu giáo làm quen tiếng Anh qua vui chơi và tương tác. Khóa 21 tháng, học song ngữ với giáo viên Việt Nam và nước ngoài, trẻ nắm được từ vựng cơ bản và chỉ dẫn đơn giản.",
                link="#kindy-4-6-tuoi"
            ),
            # Thẻ 2: GET READY (5–7 tuổi) - Bé gái cầm ống nhòm, bảng vẽ, mặt trời (Đỏ #CD2828)
            create_popout_course_card(
                bg_color="#CD2828",
                img_url="https://hocvienngoaingusla.edu.vn/wp-content/uploads/2025/05/image-program-1-1.png",
                title="GET READY (5–7 tuổi)",
                desc="Chương trình GET READY giúp học sinh làm quen tiếng Anh trước Cambridge Pre A1. Học song ngữ 50% cùng giáo viên Việt Nam, 50% cùng giáo viên nước ngoài. Sau khóa học, học sinh nắm 120–140 từ vựng, sử dụng giáo trình Academy Star Starter + Alphabet và đạt trình độ tương đương lớp 2, sẵn sàng học STARTERS.",
                link="#get-ready-5-7-tuoi"
            ),
            # Thẻ 3: STARTERS (6–8 tuổi) - Bé trai cầm robot + huy hiệu code (Đỏ #CD2828)
            create_popout_course_card(
                bg_color="#CD2828",
                img_url="https://hocvienngoaingusla.edu.vn/wp-content/uploads/2025/05/image-program-6-1.png",
                title="STARTERS (6–8 tuổi)",
                desc="Khóa STARTERS giúp học sinh phát triển giao tiếp cơ bản và làm quen cấu trúc bài thi Cambridge Starters. Học 18 tháng, 50% cùng giáo viên Việt Nam, 50% cùng giáo viên nước ngoài, sử dụng giáo trình Academy Star 1, 2 kết hợp Jolly Phonics, xây dựng nền tảng để học MOVERS.",
                link="#starters-6-8-tuoi"
            )
        ]
    }
    sec3["elements"].append(courses_row)

    # -------------------------------------------------------------
    # SECTION 4: PHỤ HUYNH & HỌC VIÊN NÓI GÌ - KHÔNG MÀU NỀN (WIDGET REVIEWS)
    # -------------------------------------------------------------
    sec4 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="45",
        padding_bottom="45",
        padding_left="20",
        padding_right="20"
    )
    sec4["elements"].append(create_heading("Phụ huynh & Học viên nói gì", size="h2", align="center", color=COLOR_TEXT_BLACK, font_size=30, font_weight="800"))
    sec4["elements"].append(create_divider(color=COLOR_BTN_ORANGE, width=70))

    reviews_slides = [
        {
            "name": "Chị Lê Thu Hà",
            "job": "Kinh doanh tự do",
            "rating": 5,
            "quote": "“Tôi lựa chọn Tiếng Anh Chị Trà vì chương trình học bài bản và môi trường tương tác rất hiện đại. Con tôi từ rụt rè nay rất hào hứng đi học và tự tin sử dụng tiếng Anh mỗi ngày.”",
            "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop"
        },
        {
            "name": "Anh Trần Minh Hoàng",
            "job": "Kỹ sư",
            "rating": 5,
            "quote": "“Trung tâm có lộ trình học khoa học, giáo viên trách nhiệm và báo cáo kết quả học tập minh bạch. Con tôi học tập nghiêm túc hơn và có sự tiến bộ rõ rệt qua từng tháng.”",
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop"
        },
        {
            "name": "Anh Phạm Quang Huy",
            "job": "Giáo viên",
            "rating": 5,
            "quote": "“Là người làm trong ngành giáo dục, tôi đánh giá cao phương pháp giảng dạy tại đây. Nội dung học phù hợp, dễ tiếp thu và theo sát năng lực thực tế của từng học viên.”",
            "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop"
        }
    ]

    sec4["elements"].append(create_reviews_widget(
        slides=reviews_slides,
        slides_per_view=3
    ))

    # -------------------------------------------------------------
    # SECTION 5: HỌC VIÊN XUẤT SẮC - LOOP CAROUSEL (Post Type: hoc_vien)
    # -------------------------------------------------------------
    sec5 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="45",
        padding_bottom="45",
        padding_left="20",
        padding_right="20"
    )
    sec5["elements"].append(create_heading("BẢNG VÀNG HỌC VIÊN XUẤT SẮC", size="h2", align="center", color=COLOR_PRIMARY_GREEN, font_size=28, font_weight="800"))
    sec5["elements"].append(create_divider(color=COLOR_BTN_ORANGE, width=90))
    sec5["elements"].append(create_text_editor(
        "<p>Vinh danh những gương mặt xuất sắc đạt thành tích cao trong các kỳ thi quốc tế và tiến bộ vượt bậc sau khóa học tại Tiếng Anh Chị Trà. Click vào ảnh để xem chi tiết câu chuyện học viên.</p>",
        align="center",
        color="#4A5568",
        font_size=15
    ))

    # Widget Loop Carousel query Post Type hoc_vien (4 Slides trên Desktop, Swiper Slider Native)
    sec5["elements"].append(create_loop_carousel_widget(
        post_type="hoc_vien",
        slides_to_show="4",
        posts_per_page=8
    ))

    # -------------------------------------------------------------
    # SECTION 6: BÀI VIẾT MỚI NHẤT - LOOP CAROUSEL (Blog / Post Type: post)
    # -------------------------------------------------------------
    sec6 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="45",
        padding_bottom="45",
        padding_left="20",
        padding_right="20"
    )
    sec6["elements"].append(create_heading("BÀI VIẾT MỚI NHẤT & KINH NGHIỆM HỌC", size="h2", align="center", color=COLOR_TEXT_BLACK, font_size=28, font_weight="800"))
    sec6["elements"].append(create_divider(color=COLOR_PRIMARY_BLUE, width=80))

    # Widget Loop Carousel query Post Type post (3 Slides trên Desktop, Swiper Slider Native)
    sec6["elements"].append(create_loop_carousel_widget(
        post_type="post",
        slides_to_show="3",
        posts_per_page=6
    ))

    # -------------------------------------------------------------
    # TẬP HỢP TOÀN BỘ CÁC SECTION VÀO ROOT TEMPLATE
    # -------------------------------------------------------------
    template = {
        "version": "0.4",
        "title": "Trang Chủ Tiếng Anh Chị Trà",
        "type": "page",
        "page_settings": [],
        "content": [sec1, sec2, sec3, sec4, sec5, sec6]
    }

    return template

def build_loop_item_giang_vien():
    """
    1. Template Loop Item: ĐỘI NGŨ GIẢNG VIÊN
    - Ảnh chân dung giảng viên thanh lịch: height 240px, object-fit cover
    - Tên giảng viên trang trọng, căn giữa, màu đen
    - Bằng cấp / Chuyên môn giảng dạy nổi bật màu xanh lá thương hiệu
    """
    card = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "flex_direction": "column",
            "content_width": "full",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "18", "left": "0", "isLinked": False},
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_PRIMARY_GREEN,
            "border_radius": {"unit": "px", "top": "10", "right": "10", "bottom": "10", "left": "10", "isLinked": True},
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "overflow": "hidden"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "theme-post-featured-image",
                "isInner": False,
                "settings": {
                    "image_size": "medium_large",
                    "link_to": "post",
                    "height": {"unit": "px", "size": 240},
                    "height_mobile": {"unit": "px", "size": 200},
                    "object_fit": "cover"
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "flex_direction": "column",
                    "align_items": "center",
                    "padding": {"unit": "px", "top": "14", "right": "15", "bottom": "0", "left": "15", "isLinked": False}
                },
                "elements": [
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "theme-post-title",
                        "isInner": False,
                        "settings": {
                            "header_size": "h3",
                            "align": "center",
                            "title_color": COLOR_TEXT_BLACK,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 18},
                            "typography_font_weight": "700",
                            "typography_line_height": {"unit": "em", "size": 1.2},
                            "link_to": "post"
                        },
                        "elements": []
                    },
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "theme-post-excerpt",
                        "isInner": False,
                        "settings": {
                            "align": "center",
                            "text_color": COLOR_PRIMARY_GREEN,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "typography_font_weight": "600",
                            "excerpt_length": 14
                        },
                        "elements": []
                    }
                ]
            }
        ]
    }
    return {
        "version": "0.4",
        "title": "Loop Item - Đội Ngũ Giảng Viên",
        "type": "loop-item",
        "page_settings": [],
        "content": [card]
    }

def build_loop_item_hoc_vien():
    """
    2. Template Loop Item: BẢNG VÀNG HỌC VIÊN XUẤT SẮC
    - Ảnh chân dung học viên rạng rỡ: height 210px, object-fit cover
    - Tên học viên H3 căn giữa
    - Điểm số IELTS / Thành tích nổi bật màu Cam #ED9717 thu hút
    """
    card = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "flex_direction": "column",
            "content_width": "full",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "18", "left": "0", "isLinked": False},
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_PRIMARY_GREEN,
            "border_radius": {"unit": "px", "top": "10", "right": "10", "bottom": "10", "left": "10", "isLinked": True},
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "overflow": "hidden"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "theme-post-featured-image",
                "isInner": False,
                "settings": {
                    "image_size": "medium_large",
                    "link_to": "post",
                    "height": {"unit": "px", "size": 210},
                    "height_mobile": {"unit": "px", "size": 180},
                    "object_fit": "cover"
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "flex_direction": "column",
                    "align_items": "center",
                    "padding": {"unit": "px", "top": "14", "right": "15", "bottom": "0", "left": "15", "isLinked": False}
                },
                "elements": [
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "theme-post-title",
                        "isInner": False,
                        "settings": {
                            "header_size": "h3",
                            "align": "center",
                            "title_color": COLOR_TEXT_BLACK,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 17},
                            "typography_font_weight": "700",
                            "typography_line_height": {"unit": "em", "size": 1.2},
                            "link_to": "post"
                        },
                        "elements": []
                    },
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "theme-post-excerpt",
                        "isInner": False,
                        "settings": {
                            "align": "center",
                            "text_color": COLOR_BTN_ORANGE,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "typography_font_weight": "700",
                            "excerpt_length": 14
                        },
                        "elements": []
                    }
                ]
            }
        ]
    }
    return {
        "version": "0.4",
        "title": "Loop Item - Bảng Vàng Học Viên",
        "type": "loop-item",
        "page_settings": [],
        "content": [card]
    }

def build_loop_item_blog():
    """
    3. Template Loop Item: BÀI VIẾT TIN TỨC & KINH NGHIỆM HỌC (CHUẨN 100% THEO ẢNH MẪU)
    - Khung viền phẳng 1px solid #E5E7EB, nền trắng #FFFFFF
    - Ảnh bài viết: height 240px (mobile 200px), object-fit cover
    - Thứ tự nội dung chuẩn ảnh mẫu:
      1. Tiêu đề bài viết H3 in đậm (font 18px, weight 700, line-height 1.35, màu đen #000000)
      2. Ngày tháng đăng bài (font 13px, màu xám nhạt #9CA3AF, KHÔNG ICON LỊCH)
      3. Đoạn trích dẫn tóm tắt (font 14px, line-height 1.6, màu #4B5563)
      4. Nút "ĐỌC TIẾP →" in hoa, màu cam nổi bật #E67E22, không nền
    """
    card = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "flex_direction": "column",
            "content_width": "full",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": "#E5E7EB",
            "border_radius": {"unit": "px", "top": "2", "right": "2", "bottom": "2", "left": "2", "isLinked": True},
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "overflow": "hidden"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "theme-post-featured-image",
                "isInner": False,
                "settings": {
                    "image_size": "full",
                    "link_to": "post",
                    "height": {"unit": "px", "size": 240},
                    "height_mobile": {"unit": "px", "size": 200},
                    "object_fit": "cover"
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "flex_direction": "column",
                    "align_items": "flex-start",
                    "padding": {"unit": "px", "top": "22", "right": "22", "bottom": "24", "left": "22", "isLinked": False}
                },
                "elements": [
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "theme-post-title",
                        "isInner": False,
                        "settings": {
                            "header_size": "h3",
                            "align": "left",
                            "title_color": COLOR_TEXT_BLACK,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 18},
                            "typography_font_weight": "800",
                            "typography_line_height": {"unit": "em", "size": 1.2},
                            "link_to": "post",
                            "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "6", "left": "0", "isLinked": False}
                        },
                        "elements": []
                    },
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "post-info",
                        "isInner": False,
                        "settings": {
                            "icon_list": [
                                {
                                    "_id": "meta_date",
                                    "type": "date",
                                    "show_icon": "none"
                                }
                            ],
                            "text_color": "#9CA3AF",
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 13},
                            "typography_font_weight": "400",
                            "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "14", "left": "0", "isLinked": False}
                        },
                        "elements": []
                    },
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "theme-post-excerpt",
                        "isInner": False,
                        "settings": {
                            "align": "left",
                            "text_color": "#4B5563",
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "typography_line_height": {"unit": "em", "size": 1.6},
                            "excerpt_length": 25,
                            "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "18", "left": "0", "isLinked": False}
                        },
                        "elements": []
                    },
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "button",
                        "isInner": False,
                        "settings": {
                            "text": "ĐỌC TIẾP →",
                            "align": "left",
                            "button_text_color": "#E67E22",
                            "background_color": "rgba(0, 0, 0, 0)",
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 13},
                            "typography_font_weight": "700",
                            "typography_letter_spacing": {"unit": "px", "size": 0.5},
                            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
                        },
                        "elements": []
                    }
                ]
            }
        ]
    }
def build_loop_item_khoa_hoc_3d():
    """
    4. Template Loop Item: KHÓA HỌC 3D POP-OUT (Dành cho Loop Grid nếu cần query động)
    - Container bo góc 35px, nền đỏ #CD2828 (hoặc dynamic/custom)
    - Nhân vật Featured Image nhô lên top: -105px
    - Tiêu đề H3 trắng
    - Trích dẫn ngắn màu trắng
    - Nút tròn mũi tên trắng bo góc 99px
    """
    card = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "flex_direction": "column",
            "content_width": "full",
            "align_items": "center",
            "justify_content": "space-between",
            "background_background": "classic",
            "background_color": "#CD2828",
            "border_radius": {"unit": "px", "top": "35", "right": "35", "bottom": "35", "left": "35", "isLinked": True},
            "padding": {"unit": "px", "top": "0", "right": "24", "bottom": "35", "left": "24", "isLinked": False},
            "margin": {"unit": "px", "top": "110", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
            "margin_mobile": {"unit": "px", "top": "90", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
            "overflow": "visible"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "theme-post-featured-image",
                "isInner": False,
                "settings": {
                    "image_size": "full",
                    "link_to": "post",
                    "align": "center",
                    "_margin": {"unit": "px", "top": "-105", "right": "0", "bottom": "15", "left": "0", "isLinked": False},
                    "_margin_mobile": {"unit": "px", "top": "-85", "right": "0", "bottom": "15", "left": "0", "isLinked": False},
                    "_z_index": 2
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "theme-post-title",
                "isInner": False,
                "settings": {
                    "header_size": "h3",
                    "align": "center",
                    "title_color": COLOR_TEXT_WHITE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 22},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "link_to": "post",
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "12", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "theme-post-excerpt",
                "isInner": False,
                "settings": {
                    "align": "center",
                    "text_color": "rgba(255, 255, 255, 0.95)",
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 14},
                    "typography_line_height": {"unit": "em", "size": 1.6},
                    "excerpt_length": 25,
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "button",
                "isInner": False,
                "settings": {
                    "text": "→",
                    "align": "center",
                    "button_text_color": "#222222",
                    "background_color": "#FFFFFF",
                    "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                    "padding": {"unit": "px", "top": "10", "right": "18", "bottom": "10", "left": "18", "isLinked": False},
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 22},
                    "typography_font_weight": "900"
                },
                "elements": []
            }
        ]
    }
    return {
        "version": "0.4",
        "title": "Loop Item - Khóa Học 3D Pop-out",
        "type": "loop-item",
        "page_settings": [],
        "content": [card]
    }

def save_and_zip(data, base_name, out_dir):
    json_p = os.path.join(out_dir, f"{base_name}.json")
    zip_p = os.path.join(out_dir, f"{base_name}.zip")
    with open(json_p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with zipfile.ZipFile(zip_p, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_p, f"{base_name}.json")
    print(f"[SUCCESS] Exported {base_name}.zip")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Trang Chủ Elementor
    homepage_tpl = build_homepage_json()
    save_and_zip(homepage_tpl, "trang-chu-elementor", out_dir)

    # 2. Loop Item 1: Giảng viên
    giang_vien_tpl = build_loop_item_giang_vien()
    save_and_zip(giang_vien_tpl, "loop-item-giang-vien", out_dir)

    # 3. Loop Item 2: Bảng vàng học viên
    hoc_vien_tpl = build_loop_item_hoc_vien()
    save_and_zip(hoc_vien_tpl, "loop-item-hoc-vien", out_dir)

    # 4. Loop Item 3: Blog tin tức
    blog_tpl = build_loop_item_blog()
    save_and_zip(blog_tpl, "loop-item-blog", out_dir)

    # 5. Loop Item 4: Khóa học 3D Pop-out
    khoa_hoc_tpl = build_loop_item_khoa_hoc_3d()
    save_and_zip(khoa_hoc_tpl, "loop-item-khoa-hoc-3d", out_dir)

    print("\n[ALL DONE] Hoan thanh tao 1 Trang chu + 4 Loop Item Templates rieng biet!")
