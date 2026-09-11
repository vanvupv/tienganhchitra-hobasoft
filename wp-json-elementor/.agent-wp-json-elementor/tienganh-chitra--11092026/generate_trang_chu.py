import json
import zipfile
import os
import uuid

def gen_id():
    return uuid.uuid4().hex[:8]

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
        settings["background_color"] = bg_gradient.get("color", "#0D9488")
        settings["background_color_b"] = bg_gradient.get("color_b", "#0F766E")
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

def create_heading(title, size="h2", align="center", color="#1E293B", font_size=32, font_weight="800"):
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

def create_text_editor(text, align="center", color="#475569", font_size=16):
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

def create_image(image_url, align="center", border_radius=0, link_url=""):
    settings = {
        "image": {"url": image_url, "id": 0},
        "image_size": "full",
        "align": align
    }
    if border_radius:
        settings["border_radius"] = {"unit": "px", "top": str(border_radius), "right": str(border_radius), "bottom": str(border_radius), "left": str(border_radius), "isLinked": True}
    if link_url:
        settings["link_to"] = "custom"
        settings["link"] = {"url": link_url, "is_external": False, "nofollow": False}

    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "image",
        "isInner": False,
        "settings": settings,
        "elements": []
    }

def create_button(text, url="#", bg_color="#1B5B65", text_color="#FFFFFF", align="center", border_radius=8):
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "button",
        "isInner": False,
        "settings": {
            "text": text,
            "link": {"url": url, "is_external": False, "nofollow": False},
            "align": align,
            "button_text_color": text_color,
            "background_color": bg_color,
            "border_radius": {"unit": "px", "top": str(border_radius), "right": str(border_radius), "bottom": str(border_radius), "left": str(border_radius), "isLinked": True},
            "typography_typography": "custom",
            "typography_font_family": "Plus Jakarta Sans",
            "typography_font_weight": "700"
        },
        "elements": []
    }

def create_divider(color="#E5A83B", width=80):
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

def build_homepage_json():
    # -------------------------------------------------------------
    # SECTION 1: BANNER FULL WIDTH
    # -------------------------------------------------------------
    sec1 = create_container(content_width="full", padding_top="0", padding_bottom="0", padding_left="0", padding_right="0")
    sec1["settings"]["stretch_section"] = "section-stretched"
    sec1["settings"]["layout"] = "full_width"
    sec1["elements"].append(
        create_image(
            image_url="https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=1920&auto=format&fit=crop",
            align="center"
        )
    )

    # -------------------------------------------------------------
    # SECTION 2: ĐỘI NGŨ GIẢNG VIÊN (Post Type: giang_vien)
    # Nền Gradient Xanh Ngọc / Teal bám sát ảnh thiết kế
    # -------------------------------------------------------------
    sec2 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_gradient={"color": "#0D9488", "color_b": "#0F766E", "type": "linear", "angle": 135}
    )
    sec2["elements"].append(create_heading("ĐỘI NGŨ GIẢNG VIÊN TẠI TIẾNG ANH CHỊ TRÀ", size="h2", align="center", color="#FFFFFF", font_size=28, font_weight="800"))
    sec2["elements"].append(create_divider(color="#FBBF24", width=90))
    sec2["elements"].append(create_text_editor(
        "<p>Chặng đường phía trước còn nhiều gian nan, nhưng với tâm huyết và say mê ngành giáo dục tri thức của mình, đội ngũ giảng viên luôn tràn đầy năng lượng đồng hành cùng học viên tiến về phía trước.</p>",
        align="center",
        color="#E2E8F0",
        font_size=15
    ))

    # Grid 4 Cột Giảng Viên
    grid_teachers = create_container(direction="row", content_width="full", padding_top="20", padding_bottom="10", padding_left="0", padding_right="0")
    grid_teachers["settings"]["flex_wrap"] = "wrap"
    grid_teachers["settings"]["justify_content"] = "space-between"

    teachers_data = [
        {"name": "Cô Thu Trà (Founder)", "role": "IELTS 8.5 - 10 năm kinh nghiệm", "img": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=600&auto=format&fit=crop"},
        {"name": "Cô Hoàng Yến", "role": "Thạc Sĩ TESOL - Chuyên gia Ngữ âm", "img": "https://images.unsplash.com/photo-1580894732444-8ecded7900cd?q=80&w=600&auto=format&fit=crop"},
        {"name": "Thầy Tuấn Dũng", "role": "IELTS 8.0 - Luyện thi cấp tốc", "img": "https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=600&auto=format&fit=crop"},
        {"name": "Cô Mai Phương", "role": "Cử nhân Sư Phạm Anh xuất sắc", "img": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=600&auto=format&fit=crop"}
    ]

    for t in teachers_data:
        card = create_container(direction="column", content_width="full", padding_top="10", padding_bottom="15", padding_left="10", padding_right="10", bg_color="rgba(255,255,255,0.08)")
        card["settings"]["width"] = {"unit": "%", "size": 23.5}
        card["settings"]["border_radius"] = {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True}
        card["settings"]["border_border"] = "solid"
        card["settings"]["border_width"] = {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}
        card["settings"]["border_color"] = "rgba(255,255,255,0.2)"
        card["settings"]["custom_css"] = "selector { transition: all 0.3s ease; } selector:hover { transform: translateY(-6px); box-shadow: 0 12px 24px rgba(0,0,0,0.2); }"
        
        card["elements"].append(create_image(t["img"], align="center", border_radius=8))
        card["elements"].append(create_heading(t["name"], size="h3", align="center", color="#FFFFFF", font_size=17, font_weight="700"))
        card["elements"].append(create_text_editor(f"<p>{t['role']}</p>", align="center", color="#FDE047", font_size=13))
        grid_teachers["elements"].append(card)

    sec2["elements"].append(grid_teachers)

    # -------------------------------------------------------------
    # SECTION 3: CHƯƠNG TRÌNH ĐÀO TẠO (Khóa học: khoa_hoc)
    # Nền Xanh Dương Đậm bám sát ảnh 3
    # -------------------------------------------------------------
    sec3 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_color="#1B64B8"
    )
    sec3["elements"].append(create_heading("CHƯƠNG TRÌNH ĐÀO TẠO TIẾNG ANH", size="h2", align="center", color="#FFFFFF", font_size=28, font_weight="800"))
    sec3["elements"].append(create_divider(color="#FFFFFF", width=80))

    grid_courses = create_container(direction="row", content_width="full", padding_top="20", padding_bottom="10", padding_left="0", padding_right="0")
    grid_courses["settings"]["flex_wrap"] = "wrap"
    grid_courses["settings"]["justify_content"] = "space-between"

    courses_data = [
        {
            "level": "LEVEL 1 – TIẾNG ANH MẤT GỐC",
            "title": "Khóa Học Nền Tảng Cho Người Bắt Đầu",
            "desc": "Xây dựng lại toàn bộ bảng phiên âm chuẩn IPA, lấy lại cảm hứng và tự tin giao tiếp các chủ đề đời sống cơ bản.",
            "img": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=800&auto=format&fit=crop"
        },
        {
            "level": "LEVEL 2 – GIAO TIẾP PHẢN XẠ",
            "title": "Phản Xạ Tự Nhiên & Làm Chủ Ngữ Điệu",
            "desc": "Luyện tư duy phản xạ bằng tiếng Anh trực tiếp, nói lưu loát không dịch ngầm trong đầu, mở rộng 1.000+ từ vựng thông dụng.",
            "img": "https://images.unsplash.com/photo-1531482615713-2afd69097998?q=80&w=800&auto=format&fit=crop"
        },
        {
            "level": "LEVEL 3 – CHINH PHỤC IELTS",
            "title": "Luyện Thi IELTS Chuyên Sâu 6.5 - 7.5+",
            "desc": "Chiến lược làm bài thực chiến 4 kỹ năng Nghe - Nói - Đọc - Viết, cam kết đầu ra bằng văn bản với lộ trình tinh gọn.",
            "img": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=800&auto=format&fit=crop"
        }
    ]

    for c in courses_data:
        c_card = create_container(direction="column", content_width="full", padding_top="0", padding_bottom="15", padding_left="0", padding_right="0", bg_color="#FFFFFF")
        c_card["settings"]["width"] = {"unit": "%", "size": 31.8}
        c_card["settings"]["border_radius"] = {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True}
        c_card["settings"]["custom_css"] = "selector { overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.15); transition: all 0.3s ease; } selector:hover { transform: translateY(-6px); }"

        # Ảnh khóa học
        c_card["elements"].append(create_image(c["img"], align="center"))

        # Dải banner xanh đậm bên dưới ảnh
        badge_box = create_container(direction="column", content_width="full", padding_top="10", padding_bottom="10", padding_left="15", padding_right="15", bg_color="#0A4D92")
        badge_box["elements"].append(create_heading(c["level"], size="h4", align="center", color="#FFFFFF", font_size=13, font_weight="800"))
        c_card["elements"].append(badge_box)

        # Khối nội dung
        content_box = create_container(direction="column", content_width="full", padding_top="15", padding_bottom="10", padding_left="18", padding_right="18")
        content_box["elements"].append(create_heading(c["title"], size="h3", align="left", color="#1E293B", font_size=16, font_weight="700"))
        content_box["elements"].append(create_text_editor(f"<p>{c['desc']}</p>", align="left", color="#64748B", font_size=13))
        content_box["elements"].append(create_button("TÌM HIỂU KHÓA HỌC", url="#", bg_color="#0A4D92", text_color="#FFFFFF", align="left", border_radius=6))
        c_card["elements"].append(content_box)

        grid_courses["elements"].append(c_card)

    sec3["elements"].append(grid_courses)

    # -------------------------------------------------------------
    # SECTION 4: PHỤ HUYNH & HỌC VIÊN NÓI GÌ (Reviews / Testimonial)
    # Nền Xanh Nhạt Pastel + Card viền đỏ bám sát ảnh 4
    # -------------------------------------------------------------
    sec4 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_color="#E6F7FA"
    )
    sec4["elements"].append(create_heading("Phụ huynh & Học viên nói gì", size="h2", align="center", color="#0F172A", font_size=32, font_weight="800"))

    grid_reviews = create_container(direction="row", content_width="full", padding_top="30", padding_bottom="15", padding_left="0", padding_right="0")
    grid_reviews["settings"]["flex_wrap"] = "wrap"
    grid_reviews["settings"]["justify_content"] = "space-between"

    reviews_data = [
        {
            "name": "Chị Lê Thu Hà",
            "job": "Kinh doanh tự do",
            "quote": "“Tôi lựa chọn Tiếng Anh Chị Trà vì chương trình học bài bản và môi trường tương tác rất hiện đại. Con tôi từ rụt rè nay rất hào hứng đi học và tự tin sử dụng tiếng Anh mỗi ngày.”",
            "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=200&auto=format&fit=crop",
            "active": False
        },
        {
            "name": "Anh Trần Minh Hoàng",
            "job": "Kỹ sư",
            "quote": "“Trung tâm có lộ trình học khoa học, giáo viên trách nhiệm và báo cáo kết quả học tập minh bạch. Con tôi học tập nghiêm túc hơn và có sự tiến bộ rõ rệt qua từng tháng.”",
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop",
            "active": True
        },
        {
            "name": "Anh Phạm Quang Huy",
            "job": "Giáo viên",
            "quote": "“Là người làm trong ngành giáo dục, tôi đánh giá cao phương pháp giảng dạy tại đây. Nội dung học phù hợp, dễ tiếp thu và theo sát năng lực thực tế của từng học viên.”",
            "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=200&auto=format&fit=crop",
            "active": False
        }
    ]

    for r in reviews_data:
        r_card = create_container(direction="column", content_width="full", padding_top="35", padding_bottom="25", padding_left="22", padding_right="22", bg_color="#FFFFFF")
        r_card["settings"]["width"] = {"unit": "%", "size": 31.8}
        border_width = "4" if r["active"] else "3"
        border_color = "#B91C1C" if r["active"] else "#DC2626"
        r_card["settings"]["border_border"] = "solid"
        r_card["settings"]["border_width"] = {"unit": "px", "top": border_width, "right": border_width, "bottom": border_width, "left": border_width, "isLinked": True}
        r_card["settings"]["border_radius"] = {"unit": "px", "top": "28", "right": "16", "bottom": "28", "left": "16", "isLinked": False}
        r_card["settings"]["custom_css"] = "selector { box-shadow: 0 10px 25px rgba(0,0,0,0.06); transition: all 0.3s ease; } selector:hover { transform: translateY(-6px); }"

        # Avatar
        r_card["elements"].append(create_image(r["avatar"], align="center", border_radius=50))
        r_card["elements"].append(create_heading(r["name"], size="h3", align="center", color="#1E293B", font_size=18, font_weight="700"))
        r_card["elements"].append(create_text_editor(f"<p>{r['job']}</p>", align="center", color="#94A3B8", font_size=13))
        # 5 sao
        r_card["elements"].append(create_heading("★★★★★", size="h4", align="center", color="#F59E0B", font_size=20, font_weight="800"))
        # Quote
        r_card["elements"].append(create_text_editor(f"<p>{r['quote']}</p>", align="center", color="#334155", font_size=14))

        grid_reviews["elements"].append(r_card)

    sec4["elements"].append(grid_reviews)

    # Nút điều hướng đỏ tròn
    nav_box = create_container(direction="row", content_width="full", padding_top="10", padding_bottom="10", padding_left="0", padding_right="0")
    nav_box["settings"]["justify_content"] = "center"
    nav_box["settings"]["gap"] = {"unit": "px", "size": 15}
    nav_box["elements"].append(create_button("‹", url="#", bg_color="#B91C1C", text_color="#FFFFFF", border_radius=50))
    nav_box["elements"].append(create_button("›", url="#", bg_color="#B91C1C", text_color="#FFFFFF", border_radius=50))
    sec4["elements"].append(nav_box)

    # -------------------------------------------------------------
    # SECTION 5: HỌC VIÊN XUẤT SẮC (Post Type: hoc_vien)
    # Click ra bài viết chi tiết học viên, bám sát ảnh 5
    # -------------------------------------------------------------
    sec5 = create_container(
        direction="column",
        content_width="boxed",
        width=1200,
        padding_top="30",
        padding_bottom="30",
        padding_left="40",
        padding_right="40",
        bg_gradient={"color": "#047857", "color_b": "#065F46", "type": "linear", "angle": 135}
    )
    sec5["elements"].append(create_heading("BẢNG VÀNG HỌC VIÊN XUẤT SẮC", size="h2", align="center", color="#FFFFFF", font_size=28, font_weight="800"))
    sec5["elements"].append(create_divider(color="#FDE047", width=90))
    sec5["elements"].append(create_text_editor(
        "<p>Vinh danh những gương mặt xuất sắc đạt thành tích cao trong các kỳ thi quốc tế và tiến bộ vượt bậc sau khóa học tại Tiếng Anh Chị Trà.</p>",
        align="center",
        color="#E2E8F0",
        font_size=15
    ))

    grid_students = create_container(direction="row", content_width="full", padding_top="20", padding_bottom="10", padding_left="0", padding_right="0")
    grid_students["settings"]["flex_wrap"] = "wrap"
    grid_students["settings"]["justify_content"] = "space-between"

    students_data = [
        {"name": "HOÀNG KHÁNH", "badge": "IELTS 7.5 Overrall", "url": "/hoc-vien-xuat-sac/hoang-khanh", "img": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=600&auto=format&fit=crop"},
        {"name": "MINH ANH", "badge": "Bứt phá Giao tiếp 30 ngày", "url": "/hoc-vien-xuat-sac/minh-anh", "img": "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=600&auto=format&fit=crop"},
        {"name": "ĐỨC THÀNH", "badge": "IELTS 8.0 Listening", "url": "/hoc-vien-xuat-sac/duc-thanh", "img": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?q=80&w=600&auto=format&fit=crop"},
        {"name": "PHƯƠNG LINH", "badge": "Thủ khoa đầu ra TOEIC 900", "url": "/hoc-vien-xuat-sac/phuong-linh", "img": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=600&auto=format&fit=crop"}
    ]

    for s in students_data:
        s_card = create_container(direction="column", content_width="full", padding_top="8", padding_bottom="15", padding_left="8", padding_right="8", bg_color="rgba(255,255,255,0.08)")
        s_card["settings"]["width"] = {"unit": "%", "size": 23.5}
        s_card["settings"]["border_radius"] = {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True}
        s_card["settings"]["border_border"] = "solid"
        s_card["settings"]["border_width"] = {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True}
        s_card["settings"]["border_color"] = "rgba(255,255,255,0.2)"
        s_card["settings"]["custom_css"] = "selector { transition: all 0.3s ease; cursor: pointer; } selector:hover { transform: translateY(-6px); box-shadow: 0 12px 24px rgba(0,0,0,0.25); }"

        # Ảnh chân dung có link tới bài viết chi tiết
        s_card["elements"].append(create_image(s["img"], align="center", border_radius=8, link_url=s["url"]))
        s_card["elements"].append(create_heading(s["name"], size="h3", align="center", color="#FFFFFF", font_size=16, font_weight="800"))
        s_card["elements"].append(create_text_editor(f"<p>{s['badge']}</p>", align="center", color="#FDE047", font_size=13))
        s_card["elements"].append(create_button("Xem Bài Viết →", url=s["url"], bg_color="rgba(255,255,255,0.2)", text_color="#FFFFFF", border_radius=20))

        grid_students["elements"].append(s_card)

    sec5["elements"].append(grid_students)

    # -------------------------------------------------------------
    # SECTION 6: BÀI VIẾT MỚI NHẤT (Blog / Tin tức)
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
    sec6["elements"].append(create_heading("BÀI VIẾT MỚI NHẤT & KINH NGHIỆM HỌC", size="h2", align="center", color="#0F172A", font_size=28, font_weight="800"))
    sec6["elements"].append(create_divider(color="#0D9488", width=80))

    grid_blogs = create_container(direction="row", content_width="full", padding_top="20", padding_bottom="10", padding_left="0", padding_right="0")
    grid_blogs["settings"]["flex_wrap"] = "wrap"
    grid_blogs["settings"]["justify_content"] = "space-between"

    blogs_data = [
        {
            "title": "5 Bí Quyết Lấy Lại Căn Bản Tiếng Anh Sau 30 Ngày",
            "desc": "Phương pháp tiếp cận tự nhiên giúp người mất gốc phá bỏ nỗi sợ giao tiếp và ghi nhớ từ vựng dễ dàng.",
            "date": "11/09/2026",
            "img": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=800&auto=format&fit=crop"
        },
        {
            "title": "Cách Luyện Phát Âm Chuẩn Quốc Tế Theo Bảng IPA",
            "desc": "Hướng dẫn chi tiết khẩu hình miệng và nguyên tắc nối âm, nuốt âm chuẩn như người bản xứ.",
            "date": "10/09/2026",
            "img": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=800&auto=format&fit=crop"
        },
        {
            "title": "Lộ Trình Tự Học IELTS Từ Con Số 0 Lên 6.5+",
            "desc": "Chia sẻ kinh nghiệm phân bổ thời gian và các bộ tài liệu thực chiến chất lượng cao nhất hiện nay.",
            "date": "09/09/2026",
            "img": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=800&auto=format&fit=crop"
        }
    ]

    for b in blogs_data:
        b_card = create_container(direction="column", content_width="full", padding_top="0", padding_bottom="20", padding_left="0", padding_right="0", bg_color="#F8FAFC")
        b_card["settings"]["width"] = {"unit": "%", "size": 31.8}
        b_card["settings"]["border_radius"] = {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True}
        b_card["settings"]["custom_css"] = "selector { overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: all 0.3s ease; } selector:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }"

        b_card["elements"].append(create_image(b["img"], align="center"))
        b_content = create_container(direction="column", content_width="full", padding_top="15", padding_bottom="10", padding_left="18", padding_right="18")
        b_content["elements"].append(create_text_editor(f"<p style='color:#0D9488; font-weight:700; margin:0;'>📅 {b['date']}</p>", align="left", font_size=12))
        b_content["elements"].append(create_heading(b["title"], size="h3", align="left", color="#1E293B", font_size=16, font_weight="700"))
        b_content["elements"].append(create_text_editor(f"<p>{b['desc']}</p>", align="left", color="#64748B", font_size=13))
        b_content["elements"].append(create_button("ĐỌC TIẾP →", url="#", bg_color="#0D9488", text_color="#FFFFFF", align="left", border_radius=6))
        b_card["elements"].append(b_content)

        grid_blogs["elements"].append(b_card)

    sec6["elements"].append(grid_blogs)

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

    print(f"[SUCCESS] Da sinh thanh cong file JSON: {json_path}")
    print(f"[SUCCESS] Da dong goi ZIP thanh cong: {zip_path}")
