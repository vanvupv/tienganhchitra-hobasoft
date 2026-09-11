import json
import zipfile
import os
import uuid

def gen_id():
    return uuid.uuid4().hex[:8]

# ==============================================================================
# BẢNG MÃ MÀU CHUẨN DỰ ÁN TIẾNG ANH CHỊ TRÀ (BRAND COLOR TOKENS)
# ==============================================================================
COLOR_PRIMARY_BLUE  = "#007BFF"  # Màu chủ đạo - Xanh dương
COLOR_PRIMARY_GREEN = "#28A745"  # Màu chủ đạo - Xanh lá
COLOR_TEXT_MAIN     = "#000000"  # Màu văn bản
COLOR_TEXT_WHITE    = "#FFFFFF"  # Màu chữ trên nền tối
COLOR_BTN_ACCENT    = "#ED9717"  # Màu nút nổi bật - Màu cam
COLOR_BORDER_LIGHT  = "#E2E8F0"  # Viền phân cách nhẹ (thay thế box-shadow)

def create_container(direction="column", content_width="boxed", width=1200, padding_top="30", padding_bottom="30", padding_left="40", padding_right="40", bg_color="", bg_gradient=None, custom_css=""):
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
    if custom_css:
        settings["custom_css"] = custom_css

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": settings,
        "elements": []
    }

def create_heading(title, size="h2", align="center", color=COLOR_TEXT_MAIN, font_size=32, font_weight="800"):
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

def create_text_editor(text, align="center", color=COLOR_TEXT_MAIN, font_size=16):
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

def create_divider(color=COLOR_BTN_ACCENT, width=80):
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

def create_posts_widget(post_type="post", columns="3", posts_per_page="3", skin="classic", show_excerpt="yes", show_read_more="yes", read_more_text="Xem thêm »", custom_css=""):
    """
    Sinh Elementor Pro Posts Widget chuẩn:
    - Query động dữ liệu theo post_type: giang_vien, khoa_hoc, hoc_vien, post.
    - TUYỆT ĐỐI KHÔNG DÙNG BOX-SHADOW.
    """
    prefix = f"{skin}_" if skin in ["classic", "cards"] else "classic_"
    
    settings = {
        "_skin": skin,
        "posts_post_type": post_type,
        f"{prefix}columns": str(columns),
        f"{prefix}columns_tablet": "2",
        f"{prefix}columns_mobile": "1",
        f"{prefix}posts_per_page": str(posts_per_page),
        f"{prefix}show_image": "yes",
        f"{prefix}image_size": "medium_large",
        f"{prefix}show_title": "yes",
        f"{prefix}show_excerpt": show_excerpt,
        f"{prefix}show_read_more": show_read_more,
        "read_more_text": read_more_text,
        f"{prefix}meta_data": ["date"] if post_type == "post" else []
    }

    if skin == "cards":
        settings[f"{prefix}show_badge"] = "none"
        settings[f"{prefix}show_avatar"] = "none"

    if custom_css:
        settings["custom_css"] = custom_css

    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "posts",
        "isInner": False,
        "settings": settings,
        "elements": []
    }

def create_reviews_widget(slides, slides_per_view=3, custom_css=""):
    """
    Sinh Elementor Pro Reviews Widget chuẩn:
    - widgetType: 'reviews'
    - slides repeater với các trường: image, name, title, rating, content.
    - TUYỆT ĐỐI KHÔNG DÙNG BOX-SHADOW.
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
        "pause_on_hover": "yes"
    }
    if custom_css:
        settings["custom_css"] = custom_css

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
    # SECTION 2: ĐỘI NGŨ GIẢNG VIÊN (Post Type: giang_vien) - MÀU XANH LÁ #28A745
    # -------------------------------------------------------------
    sec2 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_gradient={"color": COLOR_PRIMARY_GREEN, "color_b": "#1E7E34", "type": "linear", "angle": 135}
    )
    sec2["elements"].append(create_heading("ĐỘI NGŨ GIẢNG VIÊN TẠI TIẾNG ANH CHỊ TRÀ", size="h2", align="center", color=COLOR_TEXT_WHITE, font_size=28, font_weight="800"))
    sec2["elements"].append(create_divider(color=COLOR_BTN_ACCENT, width=90))
    sec2["elements"].append(create_text_editor(
        "<p>Chặng đường phía trước còn nhiều gian nan, nhưng với tâm huyết và say mê ngành giáo dục tri thức của mình, đội ngũ giảng viên luôn tràn đầy năng lượng đồng hành cùng học viên tiến về phía trước.</p>",
        align="center",
        color="#F8FAFC",
        font_size=15
    ))

    # Widget Posts query Post Type giang_vien (4 Cột) - KHÔNG BOX-SHADOW
    css_teachers = f"""
    selector .elementor-post {{
        background: rgba(255, 255, 255, 0.12) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.35) !important;
        border-radius: 8px !important;
        padding: 10px 10px 15px 10px !important;
        box-shadow: none !important;
        transition: transform 0.25s ease, border-color 0.25s ease !important;
    }}
    selector .elementor-post:hover {{
        transform: translateY(-4px) !important;
        border-color: {COLOR_BTN_ACCENT} !important;
        box-shadow: none !important;
    }}
    selector .elementor-post__thumbnail img {{
        border-radius: 6px !important;
    }}
    selector .elementor-post__title a {{
        color: {COLOR_TEXT_WHITE} !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        text-align: center !important;
        display: block !important;
    }}
    selector .elementor-post__excerpt p {{
        color: {COLOR_BTN_ACCENT} !important;
        font-size: 13px !important;
        text-align: center !important;
        font-weight: 600 !important;
    }}
    """
    sec2["elements"].append(create_posts_widget(
        post_type="giang_vien",
        columns="4",
        posts_per_page="4",
        skin="classic",
        show_excerpt="yes",
        show_read_more="no",
        custom_css=css_teachers
    ))

    # -------------------------------------------------------------
    # SECTION 3: CHƯƠNG TRÌNH ĐÀO TẠO (Post Type: khoa_hoc) - MÀU XANH DƯƠNG #007BFF
    # -------------------------------------------------------------
    sec3 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_color=COLOR_PRIMARY_BLUE
    )
    sec3["elements"].append(create_heading("CHƯƠNG TRÌNH ĐÀO TẠO TIẾNG ANH", size="h2", align="center", color=COLOR_TEXT_WHITE, font_size=28, font_weight="800"))
    sec3["elements"].append(create_divider(color=COLOR_BTN_ACCENT, width=80))

    # Card khóa học: Viền sắc nét, KHÔNG box-shadow, nút cam #ED9717
    css_courses = f"""
    selector .elementor-post {{
        background: #FFFFFF !important;
        border: 1.5px solid #D1D5DB !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: none !important;
        transition: transform 0.25s ease, border-color 0.25s ease !important;
    }}
    selector .elementor-post:hover {{
        transform: translateY(-4px) !important;
        border-color: {COLOR_BTN_ACCENT} !important;
        box-shadow: none !important;
    }}
    selector .elementor-post__title {{
        background: #0056B3 !important;
        margin: 0 !important;
        padding: 10px 15px !important;
        text-align: center !important;
    }}
    selector .elementor-post__title a {{
        color: {COLOR_TEXT_WHITE} !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
    }}
    selector .elementor-post__text {{
        padding: 15px 18px 20px 18px !important;
    }}
    selector .elementor-post__excerpt p {{
        color: {COLOR_TEXT_MAIN} !important;
        font-size: 13px !important;
        line-height: 1.6 !important;
    }}
    selector .elementor-post__read-more {{
        display: inline-block !important;
        background: {COLOR_BTN_ACCENT} !important;
        color: {COLOR_TEXT_WHITE} !important;
        padding: 9px 20px !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin-top: 10px !important;
        box-shadow: none !important;
        transition: background 0.2s ease !important;
    }}
    selector .elementor-post__read-more:hover {{
        background: #D4830F !important;
        box-shadow: none !important;
    }}
    """
    sec3["elements"].append(create_posts_widget(
        post_type="khoa_hoc",
        columns="3",
        posts_per_page="3",
        skin="classic",
        show_excerpt="yes",
        show_read_more="yes",
        read_more_text="TÌM HIỂU KHÓA HỌC »",
        custom_css=css_courses
    ))

    # -------------------------------------------------------------
    # SECTION 4: PHỤ HUYNH & HỌC VIÊN NÓI GÌ - WIDGET REVIEWS
    # -------------------------------------------------------------
    sec4 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_color="#F0F7FF"
    )
    sec4["elements"].append(create_heading("Phụ huynh & Học viên nói gì", size="h2", align="center", color=COLOR_TEXT_MAIN, font_size=32, font_weight="800"))

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

    # Review Card: Viền xanh dương chuẩn #007BFF, sao cam #ED9717, KHÔNG box-shadow
    css_reviews = f"""
    selector .elementor-testimonial {{
        background: #FFFFFF !important;
        border: 2.5px solid {COLOR_PRIMARY_BLUE} !important;
        border-radius: 20px 12px 20px 12px !important;
        padding: 30px 22px 25px 22px !important;
        box-shadow: none !important;
        transition: transform 0.25s ease, border-color 0.25s ease !important;
    }}
    selector .elementor-testimonial:hover {{
        transform: translateY(-4px) !important;
        border-color: {COLOR_BTN_ACCENT} !important;
        box-shadow: none !important;
    }}
    selector .elementor-testimonial__image img {{
        border-radius: 50% !important;
        border: 2px solid {COLOR_PRIMARY_BLUE} !important;
    }}
    selector .elementor-testimonial__name {{
        color: {COLOR_TEXT_MAIN} !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }}
    selector .elementor-testimonial__title {{
        color: #64748B !important;
        font-size: 13px !important;
    }}
    selector .elementor-star-rating {{
        color: {COLOR_BTN_ACCENT} !important;
    }}
    selector .elementor-testimonial__text {{
        color: {COLOR_TEXT_MAIN} !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        font-style: italic !important;
    }}
    selector .elementor-swiper-button {{
        color: {COLOR_BTN_ACCENT} !important;
    }}
    """
    sec4["elements"].append(create_reviews_widget(
        slides=reviews_slides,
        slides_per_view=3,
        custom_css=css_reviews
    ))

    # -------------------------------------------------------------
    # SECTION 5: HỌC VIÊN XUẤT SẮC (Post Type: hoc_vien) - MÀU XANH LÁ #28A745
    # -------------------------------------------------------------
    sec5 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_gradient={"color": COLOR_PRIMARY_GREEN, "color_b": "#1E7E34", "type": "linear", "angle": 135}
    )
    sec5["elements"].append(create_heading("BẢNG VÀNG HỌC VIÊN XUẤT SẮC", size="h2", align="center", color=COLOR_TEXT_WHITE, font_size=28, font_weight="800"))
    sec5["elements"].append(create_divider(color=COLOR_BTN_ACCENT, width=90))
    sec5["elements"].append(create_text_editor(
        "<p>Vinh danh những gương mặt xuất sắc đạt thành tích cao trong các kỳ thi quốc tế và tiến bộ vượt bậc sau khóa học tại Tiếng Anh Chị Trà. Click vào ảnh để xem chi tiết câu chuyện học viên.</p>",
        align="center",
        color="#F8FAFC",
        font_size=15
    ))

    css_students = f"""
    selector .elementor-post {{
        background: rgba(255, 255, 255, 0.12) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.35) !important;
        border-radius: 8px !important;
        padding: 8px 8px 15px 8px !important;
        box-shadow: none !important;
        transition: transform 0.25s ease, border-color 0.25s ease !important;
        cursor: pointer !important;
    }}
    selector .elementor-post:hover {{
        transform: translateY(-4px) !important;
        border-color: {COLOR_BTN_ACCENT} !important;
        box-shadow: none !important;
    }}
    selector .elementor-post__thumbnail img {{
        border-radius: 6px !important;
    }}
    selector .elementor-post__title a {{
        color: {COLOR_TEXT_WHITE} !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        text-align: center !important;
        display: block !important;
        text-transform: uppercase !important;
        margin-top: 10px !important;
    }}
    selector .elementor-post__excerpt p {{
        color: {COLOR_BTN_ACCENT} !important;
        font-size: 13px !important;
        text-align: center !important;
        margin: 5px 0 10px 0 !important;
        font-weight: 700 !important;
    }}
    """
    sec5["elements"].append(create_posts_widget(
        post_type="hoc_vien",
        columns="4",
        posts_per_page="4",
        skin="classic",
        show_excerpt="yes",
        show_read_more="no",
        custom_css=css_students
    ))

    # -------------------------------------------------------------
    # SECTION 6: BÀI VIẾT MỚI NHẤT (Blog / Post Type: post) - NỀN TRẮNG
    # -------------------------------------------------------------
    sec6 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_color="#FFFFFF"
    )
    sec6["elements"].append(create_heading("BÀI VIẾT MỚI NHẤT & KINH NGHIỆM HỌC", size="h2", align="center", color=COLOR_TEXT_MAIN, font_size=28, font_weight="800"))
    sec6["elements"].append(create_divider(color=COLOR_PRIMARY_BLUE, width=80))

    css_blogs = f"""
    selector .elementor-post {{
        background: #F8F9FA !important;
        border: 1px solid #DEE2E6 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: none !important;
        transition: transform 0.25s ease, border-color 0.25s ease !important;
        padding-bottom: 20px !important;
    }}
    selector .elementor-post:hover {{
        transform: translateY(-4px) !important;
        border-color: {COLOR_PRIMARY_BLUE} !important;
        box-shadow: none !important;
    }}
    selector .elementor-post__text {{
        padding: 15px 18px 10px 18px !important;
    }}
    selector .elementor-post__title a {{
        color: {COLOR_TEXT_MAIN} !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }}
    selector .elementor-post__excerpt p {{
        color: {COLOR_TEXT_MAIN} !important;
        font-size: 13px !important;
    }}
    selector .elementor-post__meta-data span {{
        color: {COLOR_PRIMARY_BLUE} !important;
        font-weight: 600 !important;
        font-size: 12px !important;
    }}
    selector .elementor-post__read-more {{
        display: inline-block !important;
        background: {COLOR_BTN_ACCENT} !important;
        color: {COLOR_TEXT_WHITE} !important;
        padding: 7px 16px !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin-top: 8px !important;
        box-shadow: none !important;
        transition: background 0.2s ease !important;
    }}
    selector .elementor-post__read-more:hover {{
        background: #D4830F !important;
        box-shadow: none !important;
    }}
    """
    sec6["elements"].append(create_posts_widget(
        post_type="post",
        columns="3",
        posts_per_page="3",
        skin="classic",
        show_excerpt="yes",
        show_read_more="yes",
        read_more_text="ĐỌC TIẾP →",
        custom_css=css_blogs
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

if __name__ == "__main__":
    out_dir = r"wp-json-elementor\.agent-wp-json-elementor\tienganh-chitra--11092026"
    json_path = os.path.join(out_dir, "trang-chu-elementor.json")
    zip_path = os.path.join(out_dir, "trang-chu-elementor.zip")

    template = build_homepage_json()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, "trang-chu-elementor.json")

    print(f"[SUCCESS] Da sinh thanh cong file JSON chuan ma mau va khong box-shadow: {json_path}")
    print(f"[SUCCESS] Da dong goi ZIP thanh cong: {zip_path}")
