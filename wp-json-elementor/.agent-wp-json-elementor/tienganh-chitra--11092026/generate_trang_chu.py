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
            "typography_line_height": {"unit": "em", "size": 1.3}
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
    # SECTION 3: CHƯƠNG TRÌNH ĐÀO TẠO (Post Type: khoa_hoc) - DUY NHẤT DÙNG WIDGET POSTS LƯỚI 3 CỘT
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

    # Widget Posts query Post Type khoa_hoc (3 Cột) - Nền thẻ trắng, viền xanh dương tinh tế
    sec3["elements"].append(create_posts_widget(
        post_type="khoa_hoc",
        columns="3",
        posts_per_page="3",
        show_image="yes",
        show_title="yes",
        title_color=COLOR_TEXT_BLACK,
        show_excerpt="yes",
        excerpt_color="#4A5568",
        show_read_more="yes",
        read_more_text="TÌM HIỂU KHÓA HỌC »",
        read_more_color=COLOR_BTN_ORANGE,
        bg_box_color="#FFFFFF",
        border_box_color=COLOR_PRIMARY_BLUE,
        border_radius=8,
        content_padding=16
    ))

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
    3. Template Loop Item: BÀI VIẾT TIN TỨC & KINH NGHIỆM HỌC
    - Ảnh bài viết tỷ lệ 16:9 chuẩn báo chí: height 185px, object-fit cover
    - Căn lề trái toàn bộ: Ngày đăng bài nhỏ -> Tiêu đề bài viết -> Tóm tắt -> Nút ĐỌC TIẾP
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
            "border_color": COLOR_BORDER_GRAY,
            "border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True},
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
                    "height": {"unit": "px", "size": 185},
                    "height_mobile": {"unit": "px", "size": 160},
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
                    "padding": {"unit": "px", "top": "14", "right": "16", "bottom": "0", "left": "16", "isLinked": False}
                },
                "elements": [
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "post-info",
                        "isInner": False,
                        "settings": {
                            "icon_list": [
                                {
                                    "_id": "meta_date",
                                    "type": "date"
                                }
                            ],
                            "icon_color": "#64748B",
                            "text_color": "#64748B",
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 12}
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
                            "align": "left",
                            "title_color": COLOR_TEXT_BLACK,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 17},
                            "typography_font_weight": "700",
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
                            "align": "left",
                            "text_color": "#4A5568",
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "excerpt_length": 16
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
                            "button_text_color": COLOR_BTN_ORANGE,
                            "background_color": "rgba(0, 0, 0, 0)",
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 13},
                            "typography_font_weight": "700",
                            "padding": {"unit": "px", "top": "4", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        },
                        "elements": []
                    }
                ]
            }
        ]
    }
    return {
        "version": "0.4",
        "title": "Loop Item - Blog Tin Tức",
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
    out_dir = r"wp-json-elementor\.agent-wp-json-elementor\tienganh-chitra--11092026"

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

    print("\n[ALL DONE] Hoan thanh tao 1 Trang chu + 3 Loop Item Templates rieng biet!")
