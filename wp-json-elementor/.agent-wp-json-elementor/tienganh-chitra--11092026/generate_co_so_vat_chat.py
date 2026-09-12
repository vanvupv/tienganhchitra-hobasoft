import json
import zipfile
import os
import uuid

def gen_id():
    return uuid.uuid4().hex[:8]

# ==============================================================================
# BẢNG MÃ MÀU CHUẨN DỰ ÁN TIẾNG ANH CHỊ TRÀ
# ==============================================================================
COLOR_PRIMARY_BLUE  = "#007BFF"  # Xanh dương nhận diện
COLOR_PRIMARY_GREEN = "#28A745"  # Xanh lá nhận diện
COLOR_PRIMARY_RED   = "#C8102E"  # Đỏ thương hiệu SLA / Chị Trà
COLOR_TEXT_BLACK    = "#111827"  # Màu tiêu đề sẫm
COLOR_TEXT_BODY     = "#4B5563"  # Màu nội dung văn bản
COLOR_TEXT_MUTED    = "#6B7280"  # Màu nhãn xám
COLOR_TEXT_WHITE    = "#FFFFFF"  # Màu trắng
COLOR_BTN_ORANGE    = "#ED9717"  # Màu cam điểm nhấn
COLOR_BORDER_LIGHT  = "#F0F0F0"  # Màu viền phẳng tinh tế

def build_section_1_banner():
    """
    SECTION 1: HERO BANNER (Full-width Container)
    - Ảnh nền cơ sở vật chất phòng học hiện đại
    - Background Overlay đen mờ (opacity 0.48)
    - Cụm tiêu đề kép căn giữa: 'MODERN FACILITIES' và 'CƠ SỞ VẬT CHẤT TIÊU CHUẨN'
    """
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "justify_content": "center",
            "align_items": "center",
            "min_height": {"unit": "px", "size": 400},
            "padding": {
                "unit": "px",
                "top": "90",
                "right": "20",
                "bottom": "90",
                "left": "20",
                "isLinked": False
            },
            "background_background": "classic",
            "background_image": {
                "url": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?q=80&w=1600&auto=format&fit=crop",
                "id": ""
            },
            "background_position": "center center",
            "background_size": "cover",
            "background_repeat": "no-repeat",
            "background_overlay_background": "classic",
            "background_overlay_color": "rgba(0, 0, 0, 0.48)"
        },
        "elements": [
            # 1. Tagline / Sub-heading
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "MODERN FACILITIES",
                    "header_size": "h5",
                    "align": "center",
                    "title_color": COLOR_TEXT_WHITE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "typography_font_weight": "700",
                    "typography_text_transform": "uppercase",
                    "typography_letter_spacing": {"unit": "px", "size": 2.5},
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
            # 2. Main Title
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "CƠ SỞ VẬT CHẤT TIÊU CHUẨN",
                    "header_size": "h1",
                    "align": "center",
                    "title_color": COLOR_TEXT_WHITE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 44},
                    "typography_font_size_mobile": {"unit": "px", "size": 30},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2}
                },
                "elements": []
            }
        ]
    }

def build_section_2_intro():
    """
    SECTION 2: KHỐI MÔ TẢ NGẮN (Intro Section)
    - Boxed 960px căn giữa
    - Tiêu đề H2 line-height 1.2
    - Đoạn văn bản giới thiệu ngắn gọn về không gian và môi trường học tập
    """
    desc_text = (
        "Bên cạnh đội ngũ giảng viên tâm huyết và giáo trình chuẩn hóa, Tiếng Anh Chị Trà luôn chú trọng đầu tư "
        "hệ thống cơ sở vật chất khang trang, hiện đại bậc nhất. Từng góc học tập, từng chiếc bàn chiếc ghế đều được "
        "thiết kế tỉ mỉ nhằm mang lại cho học sinh môi trường học tập an toàn, thân thiện, kích thích tối đa "
        "sự sáng tạo và niềm hứng khởi trong mỗi buổi học."
    )

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 960},
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center",
            "padding": {
                "unit": "px",
                "top": "60",
                "right": "20",
                "bottom": "20",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [
            # 1. Tagline nhỏ
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "MÔI TRƯỜNG HỌC TẬP LÝ TƯỞNG",
                    "header_size": "span",
                    "align": "center",
                    "title_color": COLOR_PRIMARY_GREEN,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 14},
                    "typography_font_weight": "700",
                    "typography_text_transform": "uppercase",
                    "typography_letter_spacing": {"unit": "px", "size": 1.5},
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "10",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            # 2. Main Title H2
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "KHÔNG GIAN TRUYỀN CẢM HỨNG - CHUẨN HÓA QUỐC TẾ",
                    "header_size": "h2",
                    "align": "center",
                    "title_color": COLOR_TEXT_BLACK,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 28},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "16",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            # 3. Đoạn mô tả ngắn
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": f"<p style='text-align: center;'>{desc_text}</p>",
                    "align": "center",
                    "text_color": COLOR_TEXT_BODY,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 16},
                    "typography_line_height": {"unit": "em", "size": 1.7}
                },
                "elements": []
            }
        ]
    }

def build_section_3_alternating_blocks():
    """
    SECTION 3: 2 KHỐI NỘI DUNG XEN KẼ (Z-pattern)
    - Khối 1: Ảnh phòng học (Trái) + Nội dung tiện nghi (Phải)
    - Khối 2: Nội dung công nghệ (Trái) + Ảnh trang thiết bị (Phải)
    - Cả 2 ảnh đều hỗ trợ nhấp để phóng to toàn màn hình (Lightbox)
    """
    # ----------------------------------------------------
    # Khối 1: Ảnh Trái - Nội dung Phải
    # ----------------------------------------------------
    col1_image = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 48},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "image",
                "isInner": False,
                "settings": {
                    "image": {
                        "url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1000&auto=format&fit=crop",
                        "id": ""
                    },
                    "image_size": "large",
                    "link_to": "file",
                    "open_lightbox": "yes",
                    "border_radius": {
                        "unit": "px",
                        "top": "12",
                        "right": "12",
                        "bottom": "12",
                        "left": "12",
                        "isLinked": True
                    },
                    "box_shadow_box_shadow_type": "yes",
                    "box_shadow_box_shadow": {
                        "horizontal": 0,
                        "vertical": 10,
                        "blur": 25,
                        "spread": 0,
                        "color": "rgba(0, 0, 0, 0.07)"
                    }
                },
                "elements": []
            }
        ]
    }

    col1_text = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 48},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "align_items": "flex-start",
            "justify_content": "center"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "KHÔNG GIAN TIỆN NGHI",
                    "header_size": "span",
                    "align": "left",
                    "title_color": COLOR_BTN_ORANGE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "typography_font_weight": "700",
                    "typography_text_transform": "uppercase",
                    "typography_letter_spacing": {"unit": "px", "size": 1.5},
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "8",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "PHÒNG HỌC THOÁNG MÁT & ÁNH SÁNG CHUẨN HỌC ĐƯỜNG",
                    "header_size": "h3",
                    "align": "left",
                    "title_color": COLOR_TEXT_BLACK,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 24},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "14",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": (
                        "<p>100% phòng học tại trung tâm đều được bố trí hệ thống cửa sổ đón ánh sáng tự nhiên kết hợp dàn đèn LED chống cận thị chuẩn học đường. "
                        "Hệ thống điều hòa hai chiều và máy lọc không khí đảm bảo môi trường luôn thoáng mát, bảo vệ sức khỏe cho học sinh trong suốt buổi học.</p>"
                        "<p>Bàn ghế được thiết kế công thái học linh hoạt theo từng lứa tuổi, dễ dàng di chuyển và sắp xếp theo cụm chữ U hoặc theo nhóm, "
                        "tạo điều kiện tối đa cho các hoạt động thảo luận và thuyết trình sôi nổi.</p>"
                    ),
                    "align": "left",
                    "text_color": COLOR_TEXT_BODY,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 15},
                    "typography_line_height": {"unit": "em", "size": 1.7}
                },
                "elements": []
            }
        ]
    }

    block_1 = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1200},
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "justify_content": "space-between",
            "align_items": "center",
            "padding": {
                "unit": "px",
                "top": "30",
                "right": "20",
                "bottom": "40",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [col1_image, col1_text]
    }

    # ----------------------------------------------------
    # Khối 2: Nội dung Trái - Ảnh Phải (Xen kẽ đảo chiều)
    # ----------------------------------------------------
    col2_text = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 48},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "align_items": "flex-start",
            "justify_content": "center"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "CÔNG NGHỆ HIỆN ĐẠI",
                    "header_size": "span",
                    "align": "left",
                    "title_color": COLOR_PRIMARY_BLUE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "typography_font_weight": "700",
                    "typography_text_transform": "uppercase",
                    "typography_letter_spacing": {"unit": "px", "size": 1.5},
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "8",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "TRANG THIẾT BỊ HỌC TẬP VÀ TRUYỀN THÔNG TƯƠNG TÁC",
                    "header_size": "h3",
                    "align": "left",
                    "title_color": COLOR_TEXT_BLACK,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 24},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "14",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": (
                        "<p>Các phòng học đều được tích hợp máy chiếu siêu nét và màn hình tương tác thông minh, phục vụ các bài giảng visual sống động và video thực tế. "
                        "Hệ thống âm thanh vòm chất lượng cao giúp học sinh luyện phát âm chuẩn ngữ điệu bản ngữ và rèn luyện phản xạ nghe tự nhiên.</p>"
                        "<p>Đặc biệt, trung tâm trang bị góc thư viện sách tiếng Anh phong phú với hàng trăm đầu sách truyện tranh, sách khoa học Cambridge, Oxford "
                        "và khu vực tự học thư giãn giúp các em thỏa sức khám phá tri thức ngoài giờ lên lớp.</p>"
                    ),
                    "align": "left",
                    "text_color": COLOR_TEXT_BODY,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 15},
                    "typography_line_height": {"unit": "em", "size": 1.7}
                },
                "elements": []
            }
        ]
    }

    col2_image = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 48},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "image",
                "isInner": False,
                "settings": {
                    "image": {
                        "url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1000&auto=format&fit=crop",
                        "id": ""
                    },
                    "image_size": "large",
                    "link_to": "file",
                    "open_lightbox": "yes",
                    "border_radius": {
                        "unit": "px",
                        "top": "12",
                        "right": "12",
                        "bottom": "12",
                        "left": "12",
                        "isLinked": True
                    },
                    "box_shadow_box_shadow_type": "yes",
                    "box_shadow_box_shadow": {
                        "horizontal": 0,
                        "vertical": 10,
                        "blur": 25,
                        "spread": 0,
                        "color": "rgba(0, 0, 0, 0.07)"
                    }
                },
                "elements": []
            }
        ]
    }

    block_2 = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1200},
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "justify_content": "space-between",
            "align_items": "center",
            "padding": {
                "unit": "px",
                "top": "20",
                "right": "20",
                "bottom": "40",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [col2_text, col2_image]
    }

    return [block_1, block_2]

def build_section_4_carousel():
    """
    SECTION 4: SLIDE HÌNH ẢNH THỰC TẾ (Image Carousel với Lightbox)
    - Boxed 1200px
    - Widget image-carousel native
    - Cấu hình link_to = "file" và open_lightbox = "yes" để khi nhấp vào ảnh sẽ phóng to
    - Slider 3 cột Desktop / 2 cột Tablet / 1 cột Mobile
    """
    sample_images = [
        {"id": "", "url": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?q=80&w=1000&auto=format&fit=crop"},
        {"id": "", "url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1000&auto=format&fit=crop"},
        {"id": "", "url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1000&auto=format&fit=crop"},
        {"id": "", "url": "https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=1000&auto=format&fit=crop"},
        {"id": "", "url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=1000&auto=format&fit=crop"},
        {"id": "", "url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=1000&auto=format&fit=crop"}
    ]

    carousel_widget = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "image-carousel",
        "isInner": False,
        "settings": {
            "carousel": sample_images,
            "thumbnail_size": "large",
            "slides_to_show": "3",
            "slides_to_show_tablet": "2",
            "slides_to_show_mobile": "1",
            "slides_to_scroll": "1",
            "image_stretch": "yes",
            "navigation": "both",
            "autoplay": "yes",
            "autoplay_speed": 3500,
            "pause_on_hover": "yes",
            "infinite": "yes",
            "link_to": "file",
            "open_lightbox": "yes",
            "arrows_color": COLOR_BTN_ORANGE,
            "dots_color": COLOR_BTN_ORANGE,
            "image_spacing_custom": {"unit": "px", "size": 20},
            "border_radius": {
                "unit": "px",
                "top": "10",
                "right": "10",
                "bottom": "10",
                "left": "10",
                "isLinked": True
            }
        },
        "elements": []
    }

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1200},
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center",
            "padding": {
                "unit": "px",
                "top": "30",
                "right": "20",
                "bottom": "80",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [
            # Tiêu đề H2
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "HÌNH ẢNH THỰC TẾ TẠI TRUNG TÂM",
                    "header_size": "h2",
                    "align": "center",
                    "title_color": COLOR_TEXT_BLACK,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 26},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "8",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            # Hướng dẫn phóng to
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "(Nhấp vào hình ảnh bất kỳ để phóng to toàn màn hình)",
                    "header_size": "span",
                    "align": "center",
                    "title_color": COLOR_TEXT_MUTED,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 14},
                    "typography_font_style": "italic",
                    "typography_line_height": {"unit": "em", "size": 1.4},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "28",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            # Widget Carousel
            carousel_widget
        ]
    }

def build_co_so_vat_chat_page_json():
    """Xây dựng gói Page Template hoàn chỉnh cho Trang Cơ Sở Vật Chất"""
    sec1 = build_section_1_banner()
    sec2 = build_section_2_intro()
    alternating_blocks = build_section_3_alternating_blocks()
    sec4 = build_section_4_carousel()

    content = [sec1, sec2] + alternating_blocks + [sec4]

    return {
        "version": "0.4",
        "title": "Trang Cơ Sở Vật Chất - Tiếng Anh Chị Trà",
        "type": "page",
        "page_settings": [],
        "content": content
    }

def save_and_zip(data, base_name, out_dir):
    json_path = os.path.join(out_dir, f"{base_name}.json")
    zip_path = os.path.join(out_dir, f"{base_name}.zip")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, f"{base_name}.json")
        
    print(f"[SUCCESS] Exported: {base_name}.json")
    print(f"[SUCCESS] Exported: {base_name}.zip")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    page_data = build_co_so_vat_chat_page_json()
    save_and_zip(page_data, "trang-co-so-vat-chat-elementor", out_dir)
    print("\n[COMPLETED] Successfully generated Trang Co So Vat Chat Elementor JSON & ZIP!")
