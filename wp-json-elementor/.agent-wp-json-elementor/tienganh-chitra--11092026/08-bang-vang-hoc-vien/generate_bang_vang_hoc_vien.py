import json
import zipfile
import os
import uuid

def gen_id():
    return uuid.uuid4().hex[:8]

# ==============================================================================
# BẢNG MÃ MÀU VÀ THIẾT KẾ CHUẨN DỰ ÁN TIẾNG ANH CHỊ TRÀ
# ==============================================================================
COLOR_PRIMARY_BLUE    = "#007BFF"  # Xanh dương chủ đạo
COLOR_NAVY_TITLE      = "#002D62"  # Xanh navy sẫm cho tiêu đề chính
COLOR_NAVY_DARK       = "#0F172A"  # Xanh navy đen tên học viên
COLOR_TEXT_BODY       = "#4B5563"  # Màu nội dung văn bản (xám trung tính)
COLOR_TEXT_MUTED      = "#64748B"  # Màu mô tả / nhãn xám
COLOR_TEXT_WHITE      = "#FFFFFF"  # Màu trắng
COLOR_BG_LIGHT_BLUE   = "#F0F7FF"  # Nền xanh nhạt hero banner
COLOR_TAG_BG_BLUE     = "#EBF5FF"  # Nền tag danh mục pill
COLOR_BORDER_LIGHT    = "#E2E8F0"  # Viền thẻ học viên
COLOR_GOLD_STAR       = "#F59E0B"  # Màu vàng kim huy hiệu ngôi sao

# ==============================================================================
# SECTION 1: HERO BANNER (ẢNH NHÓM HỌC VIÊN + TIÊU ĐỀ H1 + DÒNG MÔ TẢ)
# ==============================================================================
def build_section_1_banner():
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "justify_content": "center",
            "align_items": "center",
            "padding": {
                "unit": "px",
                "top": "40",
                "right": "20",
                "bottom": "40",
                "left": "20",
                "isLinked": False
            },
            "background_background": "gradient",
            "background_color": "#EAF4FF",
            "background_color_b": "#F6FAFF",
            "background_gradient_type": "linear",
            "background_gradient_angle": {"unit": "deg", "size": 180}
        },
        "elements": [
            # Inner Container 2 Cột
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "boxed",
                    "width": {"unit": "px", "size": 1240},
                    "flex_direction": "row",
                    "flex_direction_tablet": "column-reverse",
                    "justify_content": "space-between",
                    "align_items": "center",
                    "gap": {"unit": "px", "size": 40}
                },
                "elements": [
                    # Cột Trái: Ảnh nhóm 5 học viên cầm cúp & chứng chỉ
                    {
                        "id": gen_id(),
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "content_width": "full",
                            "width": {"unit": "%", "size": 48},
                            "width_tablet": {"unit": "%", "size": 100},
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
                                        "url": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/Ban-sao-cua-ANH02083-scaled-1.jpg",
                                        "id": ""
                                    },
                                    "image_size": "full",
                                    "align": "center",
                                    "border_radius": {
                                        "unit": "px",
                                        "top": "16",
                                        "right": "16",
                                        "bottom": "16",
                                        "left": "16",
                                        "isLinked": True
                                    },
                                    "box_shadow_box_shadow_type": "yes",
                                    "box_shadow_box_shadow": {
                                        "horizontal": 0,
                                        "vertical": 12,
                                        "blur": 28,
                                        "spread": 0,
                                        "color": "rgba(0, 123, 255, 0.12)"
                                    }
                                },
                                "elements": []
                            }
                        ]
                    },
                    # Cột Phải: Tiêu đề & Tagline
                    {
                        "id": gen_id(),
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "content_width": "full",
                            "width": {"unit": "%", "size": 50},
                            "width_tablet": {"unit": "%", "size": 100},
                            "flex_direction": "column",
                            "align_items": "flex-start",
                            "justify_content": "center"
                        },
                        "elements": [
                            # Tagline
                            {
                                "id": gen_id(),
                                "elType": "widget",
                                "widgetType": "heading",
                                "isInner": False,
                                "settings": {
                                    "title": "THÀNH TÍCH & TỰ HÀO",
                                    "header_size": "h5",
                                    "align": "left",
                                    "title_color": COLOR_PRIMARY_BLUE,
                                    "typography_typography": "custom",
                                    "typography_font_family": "Plus Jakarta Sans",
                                    "typography_font_size": {"unit": "px", "size": 14},
                                    "typography_font_weight": "800",
                                    "typography_text_transform": "uppercase",
                                    "typography_letter_spacing": {"unit": "px", "size": 2},
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
                            # Tiêu đề H1
                            {
                                "id": gen_id(),
                                "elType": "widget",
                                "widgetType": "heading",
                                "isInner": False,
                                "settings": {
                                    "title": "BẢNG VÀNG HỌC VIÊN",
                                    "header_size": "h1",
                                    "align": "left",
                                    "title_color": COLOR_NAVY_TITLE,
                                    "typography_typography": "custom",
                                    "typography_font_family": "Plus Jakarta Sans",
                                    "typography_font_size": {"unit": "px", "size": 42},
                                    "typography_font_size_mobile": {"unit": "px", "size": 30},
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
                            # Đoạn mô tả
                            {
                                "id": gen_id(),
                                "elType": "widget",
                                "widgetType": "text-editor",
                                "isInner": False,
                                "settings": {
                                    "editor": "<p>Những dấu ấn nổi bật trên hành trình học tập của các học viên Tiếng Anh Chị Trà.</p>",
                                    "align": "left",
                                    "text_color": COLOR_TEXT_MUTED,
                                    "typography_typography": "custom",
                                    "typography_font_family": "Plus Jakarta Sans",
                                    "typography_font_size": {"unit": "px", "size": 16},
                                    "typography_line_height": {"unit": "em", "size": 1.6}
                                },
                                "elements": []
                            }
                        ]
                    }
                ]
            }
        ]
    }

# ==============================================================================
# SECTION 2: BREADCRUMB (YOAST SEO NATIVE)
# ==============================================================================
def build_section_2_breadcrumb():
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1240},
            "flex_direction": "row",
            "align_items": "center",
            "padding": {
                "unit": "px",
                "top": "16",
                "right": "20",
                "bottom": "10",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "yoast-breadcrumbs",
                "isInner": False,
                "settings": {},
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "shortcode",
                "isInner": False,
                "settings": {
                    "shortcode": "[wpseo_breadcrumb]"
                },
                "elements": []
            }
        ]
    }

# ==============================================================================
# SECTION 3: TIÊU ĐỀ DẪN & BỘ LỌC CHỨNG CHỈ (FILTER TABS)
# ==============================================================================
def build_section_3_intro_and_tabs():
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1240},
            "flex_direction": "column",
            "align_items": "center",
            "padding": {
                "unit": "px",
                "top": "40",
                "right": "20",
                "bottom": "15",
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
                    "title": "NHỮNG DẤU ẤN ĐÁNG TỰ HÀO",
                    "header_size": "h2",
                    "align": "center",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 30},
                    "typography_font_size_mobile": {"unit": "px", "size": 22},
                    "typography_font_weight": "800",
                    "typography_text_transform": "uppercase",
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
            # Đoạn mô tả
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": "<p style=\"text-align: center; max-width: 650px; margin: 0 auto; color: #64748B; font-size: 15px; line-height: 1.6;\">Mỗi chứng chỉ, mỗi giải thưởng là một dấu mốc ghi nhận sự nỗ lực và hành trình trưởng thành của học viên tại Tiếng Anh Chị Trà.</p>",
                    "align": "center",
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
            # Container các nút lọc dạng viên thuốc (Filter Bar Tabs)
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "row",
                    "justify_content": "center",
                    "align_items": "center",
                    "flex_wrap": "wrap",
                    "gap": {"unit": "px", "size": 14}
                },
                "elements": [
                    # Tab 1: IC3 (Active)
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "button",
                        "isInner": False,
                        "settings": {
                            "text": "IC3",
                            "link": {"url": "#ic3"},
                            "align": "center",
                            "size": "md",
                            "selected_icon": {"value": "fas fa-desktop", "library": "fa-solid"},
                            "icon_align": "left",
                            "icon_indent": {"unit": "px", "size": 8},
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "typography_font_weight": "700",
                            "button_text_color": COLOR_TEXT_WHITE,
                            "background_color": COLOR_PRIMARY_BLUE,
                            "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                            "box_shadow_box_shadow_type": "yes",
                            "box_shadow_box_shadow": {
                                "horizontal": 0,
                                "vertical": 4,
                                "blur": 14,
                                "spread": 0,
                                "color": "rgba(0, 123, 255, 0.35)"
                            },
                            "padding": {"unit": "px", "top": "12", "right": "32", "bottom": "12", "left": "32", "isLinked": False}
                        },
                        "elements": []
                    },
                    # Tab 2: Cambridge
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "button",
                        "isInner": False,
                        "settings": {
                            "text": "Cambridge",
                            "link": {"url": "#cambridge"},
                            "align": "center",
                            "size": "md",
                            "selected_icon": {"value": "fas fa-shield-alt", "library": "fa-solid"},
                            "icon_align": "left",
                            "icon_indent": {"unit": "px", "size": 8},
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "typography_font_weight": "700",
                            "button_text_color": "#334155",
                            "background_color": "#FFFFFF",
                            "border_border": "solid",
                            "border_width": {"unit": "px", "top": "1.5", "right": "1.5", "bottom": "1.5", "left": "1.5", "isLinked": True},
                            "border_color": "#E2E8F0",
                            "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                            "padding": {"unit": "px", "top": "12", "right": "28", "bottom": "12", "left": "28", "isLinked": False}
                        },
                        "elements": []
                    },
                    # Tab 3: IELTS
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "button",
                        "isInner": False,
                        "settings": {
                            "text": "IELTS",
                            "link": {"url": "#ielts"},
                            "align": "center",
                            "size": "md",
                            "selected_icon": {"value": "fas fa-award", "library": "fa-solid"},
                            "icon_align": "left",
                            "icon_indent": {"unit": "px", "size": 8},
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "typography_font_weight": "700",
                            "button_text_color": "#334155",
                            "background_color": "#FFFFFF",
                            "border_border": "solid",
                            "border_width": {"unit": "px", "top": "1.5", "right": "1.5", "bottom": "1.5", "left": "1.5", "isLinked": True},
                            "border_color": "#E2E8F0",
                            "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                            "padding": {"unit": "px", "top": "12", "right": "28", "bottom": "12", "left": "28", "isLinked": False}
                        },
                        "elements": []
                    },
                    # Tab 4: Giải quốc tế
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "button",
                        "isInner": False,
                        "settings": {
                            "text": "Giải quốc tế",
                            "link": {"url": "#giai-quoc-te"},
                            "align": "center",
                            "size": "md",
                            "selected_icon": {"value": "fas fa-trophy", "library": "fa-solid"},
                            "icon_align": "left",
                            "icon_indent": {"unit": "px", "size": 8},
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 14},
                            "typography_font_weight": "700",
                            "button_text_color": "#334155",
                            "background_color": "#FFFFFF",
                            "border_border": "solid",
                            "border_width": {"unit": "px", "top": "1.5", "right": "1.5", "bottom": "1.5", "left": "1.5", "isLinked": True},
                            "border_color": "#E2E8F0",
                            "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                            "padding": {"unit": "px", "top": "12", "right": "28", "bottom": "12", "left": "28", "isLinked": False}
                        },
                        "elements": []
                    }
                ]
            }
        ]
    }

# ==============================================================================
# SECTION 4: HEADER GIỚI THIỆU CHỨNG CHỈ ĐANG CHỌN (IC3 HEADER CARD)
# ==============================================================================
def build_section_4_category_banner():
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1240},
            "padding": {
                "unit": "px",
                "top": "24",
                "right": "32",
                "bottom": "24",
                "left": "32",
                "isLinked": False
            },
            "_margin": {
                "unit": "px",
                "top": "20",
                "right": "auto",
                "bottom": "35",
                "left": "auto",
                "isLinked": False
            },
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": "#E2E8F0",
            "border_radius": {"unit": "px", "top": "18", "right": "18", "bottom": "18", "left": "18", "isLinked": True},
            "background_background": "gradient",
            "background_color": "#F8FAFC",
            "background_color_b": "#F0F7FF",
            "background_gradient_type": "linear",
            "background_gradient_angle": {"unit": "deg", "size": 90}
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "row",
                    "flex_direction_tablet": "column",
                    "justify_content": "space-between",
                    "align_items": "center",
                    "gap": {"unit": "px", "size": 24}
                },
                "elements": [
                    # Khối Trái: Icon Desktop + Tiêu đề IC3 + Mô tả
                    {
                        "id": gen_id(),
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "content_width": "full",
                            "width": {"unit": "%", "size": 65},
                            "width_tablet": {"unit": "%", "size": 100},
                            "flex_direction": "row",
                            "align_items": "center",
                            "gap": {"unit": "px", "size": 18}
                        },
                        "elements": [
                            # Icon Desktop to màu xanh
                            {
                                "id": gen_id(),
                                "elType": "widget",
                                "widgetType": "icon",
                                "isInner": False,
                                "settings": {
                                    "selected_icon": {"value": "fas fa-desktop", "library": "fa-solid"},
                                    "view": "default",
                                    "primary_color": COLOR_PRIMARY_BLUE,
                                    "size": {"unit": "px", "size": 38}
                                },
                                "elements": []
                            },
                            # Text IC3 + description
                            {
                                "id": gen_id(),
                                "elType": "container",
                                "isInner": True,
                                "settings": {
                                    "content_width": "full",
                                    "flex_direction": "column",
                                    "align_items": "flex-start",
                                    "gap": {"unit": "px", "size": 4}
                                },
                                "elements": [
                                    {
                                        "id": gen_id(),
                                        "elType": "widget",
                                        "widgetType": "heading",
                                        "isInner": False,
                                        "settings": {
                                            "title": "IC3",
                                            "header_size": "h3",
                                            "align": "left",
                                            "title_color": COLOR_NAVY_DARK,
                                            "typography_typography": "custom",
                                            "typography_font_family": "Plus Jakarta Sans",
                                            "typography_font_size": {"unit": "px", "size": 24},
                                            "typography_font_weight": "800",
                                            "typography_line_height": {"unit": "em", "size": 1.2}
                                        },
                                        "elements": []
                                    },
                                    {
                                        "id": gen_id(),
                                        "elType": "widget",
                                        "widgetType": "text-editor",
                                        "isInner": False,
                                        "settings": {
                                            "editor": "<p style=\"color: #64748B; font-size: 14px; margin: 0; line-height: 1.5;\">Chứng chỉ công nghệ thông tin quốc tế, giúp học viên trang bị kỹ năng máy tính và tư duy số trong thời đại mới.</p>",
                                            "align": "left"
                                        },
                                        "elements": []
                                    }
                                ]
                            }
                        ]
                    },
                    # Khối Phải: Huy hiệu IC3 Logo & Minh họa
                    {
                        "id": gen_id(),
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "content_width": "full",
                            "width": {"unit": "%", "size": 30},
                            "width_tablet": {"unit": "%", "size": 100},
                            "flex_direction": "row",
                            "justify_content": "flex-end",
                            "justify_content_tablet": "center",
                            "align_items": "center"
                        },
                        "elements": [
                            {
                                "id": gen_id(),
                                "elType": "widget",
                                "widgetType": "heading",
                                "isInner": False,
                                "settings": {
                                    "title": "<span style=\"color: #22C55E; font-size: 26px; font-weight: 900; letter-spacing: 1px;\">IC3</span> <span style=\"font-size: 12px; font-weight: 800; color: #334155; text-transform: uppercase;\">DIGITAL LITERACY<br>CERTIFICATION</span>",
                                    "header_size": "div",
                                    "align": "right"
                                },
                                "elements": []
                            }
                        ]
                    }
                ]
            }
        ]
    }

# ==============================================================================
# SECTION 5: LƯỚI 8 THẺ HỌC VIÊN BẢNG VÀNG & PHÂN TRANG (STUDENT GRID)
# ==============================================================================
STUDENTS_DATA = [
    {
        "name": "Nguyễn Minh Anh",
        "img": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/Ban-sao-cua-ANH02508-1-scaled-1.jpg",
        "gs": "IC3 GS6",
        "score": "Điểm số: 980/1000",
        "year": "Năm đạt: 2026"
    },
    {
        "name": "Trần Đức Minh",
        "img": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/Ban-sao-cua-ANH02524-1-scaled-1.jpg",
        "gs": "IC3 GS5",
        "score": "Điểm số: 950/1000",
        "year": "Năm đạt: 2025"
    },
    {
        "name": "Lê Khánh Linh",
        "img": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/Ban-sao-cua-ANH02556-1-scaled-1.jpg",
        "gs": "IC3 GS6",
        "score": "Điểm số: 970/1000",
        "year": "Năm đạt: 2025"
    },
    {
        "name": "Phạm Nhật Minh",
        "img": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/Ban-sao-cua-ANH02584-scaled-1.jpg",
        "gs": "IC3 GS5",
        "score": "Điểm số: 930/1000",
        "year": "Năm đạt: 2025"
    },
    {
        "name": "Đỗ Mai Anh",
        "img": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/Ban-sao-cua-ANH03316-scaled-1.jpg",
        "gs": "IC3 GS6",
        "score": "Điểm số: 965/1000",
        "year": "Năm đạt: 2024"
    },
    {
        "name": "Hoàng Gia Bảo",
        "img": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/ANH02197-scaled-1.jpg",
        "gs": "IC3 GS5",
        "score": "Điểm số: 920/1000",
        "year": "Năm đạt: 2024"
    },
    {
        "name": "Vũ Thảo My",
        "img": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/ANH02206-scaled-1.jpg",
        "gs": "IC3 GS6",
        "score": "Điểm số: 980/1000",
        "year": "Năm đạt: 2024"
    },
    {
        "name": "Ngô Đức Anh",
        "img": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/ANH02236-scaled-1.jpg",
        "gs": "IC3 GS5",
        "score": "Điểm số: 935/1000",
        "year": "Năm đạt: 2024"
    }
]

def build_student_card(data):
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "width": {"unit": "%", "size": 23.5},
            "width_tablet": {"unit": "%", "size": 48},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16", "isLinked": True},
            "overflow": "hidden",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "18", "left": "0", "isLinked": False},
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": 0,
                "vertical": 4,
                "blur": 16,
                "spread": 0,
                "color": "rgba(0, 0, 0, 0.05)"
            }
        },
        "elements": [
            # Khối Ảnh + Huy hiệu ngôi sao góc
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "position": "relative",
                    "overflow": "hidden"
                },
                "elements": [
                    # Ảnh chân dung học viên
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "image",
                        "isInner": False,
                        "settings": {
                            "image": {
                                "url": data["img"],
                                "id": ""
                            },
                            "image_size": "full",
                            "align": "center",
                            "height": {"unit": "px", "size": 200},
                            "object_fit": "cover"
                        },
                        "elements": []
                    },
                    # Huy hiệu góc phải: Ngôi sao vàng
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "icon",
                        "isInner": False,
                        "settings": {
                            "selected_icon": {"value": "fas fa-award", "library": "fa-solid"},
                            "view": "stacked",
                            "shape": "circle",
                            "primary_color": COLOR_GOLD_STAR,
                            "secondary_color": "#FFFFFF",
                            "size": {"unit": "px", "size": 16},
                            "_position": "absolute",
                            "_offset_x": {"unit": "px", "size": 12},
                            "_offset_y": {"unit": "px", "size": 12},
                            "_offset_x_end": {"unit": "px", "size": 12}
                        },
                        "elements": []
                    }
                ]
            },
            # Khối nội dung thông tin (Padding 16px)
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "column",
                    "padding": {"unit": "px", "top": "16", "right": "16", "bottom": "0", "left": "16", "isLinked": False},
                    "gap": {"unit": "px", "size": 10}
                },
                "elements": [
                    # Tên học viên
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "heading",
                        "isInner": False,
                        "settings": {
                            "title": data["name"],
                            "header_size": "h4",
                            "align": "left",
                            "title_color": COLOR_NAVY_DARK,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 17},
                            "typography_font_weight": "700",
                            "typography_line_height": {"unit": "em", "size": 1.3}
                        },
                        "elements": []
                    },
                    # Icon list 3 dòng thông số
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "icon-list",
                        "isInner": False,
                        "settings": {
                            "icon_list": [
                                {
                                    "text": data["gs"],
                                    "selected_icon": {"value": "fas fa-desktop", "library": "fa-solid"}
                                },
                                {
                                    "text": data["score"],
                                    "selected_icon": {"value": "fas fa-certificate", "library": "fa-solid"}
                                },
                                {
                                    "text": data["year"],
                                    "selected_icon": {"value": "fas fa-calendar-alt", "library": "fa-solid"}
                                }
                            ],
                            "icon_color": COLOR_PRIMARY_BLUE,
                            "icon_size": {"unit": "px", "size": 13},
                            "text_color": COLOR_TEXT_MUTED,
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 13.5},
                            "space_between": {"unit": "px", "size": 8}
                        },
                        "elements": []
                    },
                    # Nút Xem chi tiết ->
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "button",
                        "isInner": False,
                        "settings": {
                            "text": "Xem chi tiết →",
                            "link": {"url": "#"},
                            "align": "left",
                            "size": "sm",
                            "typography_typography": "custom",
                            "typography_font_family": "Plus Jakarta Sans",
                            "typography_font_size": {"unit": "px", "size": 13.5},
                            "typography_font_weight": "700",
                            "button_text_color": COLOR_PRIMARY_BLUE,
                            "background_color": "transparent",
                            "padding": {"unit": "px", "top": "4", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                        },
                        "elements": []
                    }
                ]
            }
        ]
    }

def build_section_5_student_grid():
    student_cards = [build_student_card(s) for s in STUDENTS_DATA]
    
    # Thanh phân trang số
    pagination_container = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "justify_content": "center",
            "align_items": "center",
            "gap": {"unit": "px", "size": 8},
            "_margin": {
                "unit": "px",
                "top": "35",
                "right": "0",
                "bottom": "20",
                "left": "0",
                "isLinked": False
            }
        },
        "elements": [
            # Nút Prev <
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "button",
                "isInner": False,
                "settings": {
                    "text": "‹",
                    "link": {"url": "#"},
                    "button_text_color": "#64748B",
                    "background_color": "#FFFFFF",
                    "border_border": "solid",
                    "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                    "border_color": "#E2E8F0",
                    "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                    "padding": {"unit": "px", "top": "8", "right": "14", "bottom": "8", "left": "14", "isLinked": False}
                },
                "elements": []
            },
            # Nút 1 (Active)
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "button",
                "isInner": False,
                "settings": {
                    "text": "1",
                    "link": {"url": "#"},
                    "button_text_color": "#FFFFFF",
                    "background_color": COLOR_PRIMARY_BLUE,
                    "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                    "padding": {"unit": "px", "top": "8", "right": "14", "bottom": "8", "left": "14", "isLinked": False}
                },
                "elements": []
            },
            # Nút 2
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "button",
                "isInner": False,
                "settings": {
                    "text": "2",
                    "link": {"url": "#"},
                    "button_text_color": "#64748B",
                    "background_color": "#FFFFFF",
                    "border_border": "solid",
                    "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                    "border_color": "#E2E8F0",
                    "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                    "padding": {"unit": "px", "top": "8", "right": "14", "bottom": "8", "left": "14", "isLinked": False}
                },
                "elements": []
            },
            # Nút 3
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "button",
                "isInner": False,
                "settings": {
                    "text": "3",
                    "link": {"url": "#"},
                    "button_text_color": "#64748B",
                    "background_color": "#FFFFFF",
                    "border_border": "solid",
                    "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                    "border_color": "#E2E8F0",
                    "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                    "padding": {"unit": "px", "top": "8", "right": "14", "bottom": "8", "left": "14", "isLinked": False}
                },
                "elements": []
            },
            # Nút Next >
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "button",
                "isInner": False,
                "settings": {
                    "text": "›",
                    "link": {"url": "#"},
                    "button_text_color": "#64748B",
                    "background_color": "#FFFFFF",
                    "border_border": "solid",
                    "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
                    "border_color": "#E2E8F0",
                    "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                    "padding": {"unit": "px", "top": "8", "right": "14", "bottom": "8", "left": "14", "isLinked": False}
                },
                "elements": []
            }
        ]
    }

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1240},
            "padding": {
                "unit": "px",
                "top": "10",
                "right": "20",
                "bottom": "30",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [
            # Lưới 8 Card Flexbox
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "row",
                    "flex_wrap": "wrap",
                    "justify_content": "space-between",
                    "gap": {"unit": "px", "size": 20}
                },
                "elements": student_cards
            },
            # Phân trang
            pagination_container
        ]
    }

# ==============================================================================
# SECTION 6: NHỮNG CON SỐ ẤN TƯỢNG (STATISTICS COUNTER)
# ==============================================================================
def build_section_6_stats():
    stats_items = [
        {
            "icon": "fas fa-desktop",
            "number": "150+",
            "label": "Chứng chỉ IC3"
        },
        {
            "icon": "fas fa-shield-alt",
            "number": "80+",
            "label": "Học viên đạt từ GS5 trở lên"
        },
        {
            "icon": "fas fa-trophy",
            "number": "30+",
            "label": "Học viên đạt giải quốc tế"
        },
        {
            "icon": "fas fa-star",
            "number": "100%",
            "label": "Học viên được công nhận và vinh danh"
        }
    ]

    stat_elements = []
    for item in stats_items:
        stat_elements.append({
            "id": gen_id(),
            "elType": "container",
            "isInner": True,
            "settings": {
                "content_width": "full",
                "width": {"unit": "%", "size": 23.5},
                "width_tablet": {"unit": "%", "size": 48},
                "width_mobile": {"unit": "%", "size": 100},
                "flex_direction": "row",
                "align_items": "center",
                "gap": {"unit": "px", "size": 14}
            },
            "elements": [
                # Icon lớn
                {
                    "id": gen_id(),
                    "elType": "widget",
                    "widgetType": "icon",
                    "isInner": False,
                    "settings": {
                        "selected_icon": {"value": item["icon"], "library": "fa-solid"},
                        "view": "default",
                        "primary_color": COLOR_PRIMARY_BLUE,
                        "size": {"unit": "px", "size": 36}
                    },
                    "elements": []
                },
                # Số + Nhãn
                {
                    "id": gen_id(),
                    "elType": "container",
                    "isInner": True,
                    "settings": {
                        "content_width": "full",
                        "flex_direction": "column",
                        "align_items": "flex-start",
                        "gap": {"unit": "px", "size": 2}
                    },
                    "elements": [
                        {
                            "id": gen_id(),
                            "elType": "widget",
                            "widgetType": "heading",
                            "isInner": False,
                            "settings": {
                                "title": item["number"],
                                "header_size": "h3",
                                "align": "left",
                                "title_color": COLOR_PRIMARY_BLUE,
                                "typography_typography": "custom",
                                "typography_font_family": "Plus Jakarta Sans",
                                "typography_font_size": {"unit": "px", "size": 28},
                                "typography_font_weight": "800",
                                "typography_line_height": {"unit": "em", "size": 1.2}
                            },
                            "elements": []
                        },
                        {
                            "id": gen_id(),
                            "elType": "widget",
                            "widgetType": "text-editor",
                            "isInner": False,
                            "settings": {
                                "editor": f"<p style=\"color: #64748B; font-size: 13.5px; margin: 0; line-height: 1.4;\">{item['label']}</p>",
                                "align": "left"
                            },
                            "elements": []
                        }
                    ]
                }
            ]
        })

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1240},
            "padding": {
                "unit": "px",
                "top": "30",
                "right": "35",
                "bottom": "30",
                "left": "35",
                "isLinked": False
            },
            "_margin": {
                "unit": "px",
                "top": "20",
                "right": "auto",
                "bottom": "30",
                "left": "auto",
                "isLinked": False
            },
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": "#E2E8F0",
            "border_radius": {"unit": "px", "top": "18", "right": "18", "bottom": "18", "left": "18", "isLinked": True},
            "background_background": "classic",
            "background_color": "#F8FAFC"
        },
        "elements": [
            # Tiêu đề khối
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "NHỮNG CON SỐ ẤN TƯỢNG",
                    "header_size": "h3",
                    "align": "left",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 20},
                    "typography_font_weight": "800",
                    "typography_text_transform": "uppercase",
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "24",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            # 4 Thống số dạng hàng
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "row",
                    "flex_wrap": "wrap",
                    "justify_content": "space-between",
                    "align_items": "center",
                    "gap": {"unit": "px", "size": 16}
                },
                "elements": stat_elements
            }
        ]
    }

# ==============================================================================
# SECTION 7: CALL TO ACTION BANNER (CÙNG CON TỰ TIN CHINH PHỤC TIẾNG ANH)
# ==============================================================================
def build_section_7_cta():
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1240},
            "padding": {
                "unit": "px",
                "top": "35",
                "right": "45",
                "bottom": "35",
                "left": "45",
                "isLinked": False
            },
            "_margin": {
                "unit": "px",
                "top": "15",
                "right": "auto",
                "bottom": "45",
                "left": "auto",
                "isLinked": False
            },
            "border_radius": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True},
            "background_background": "gradient",
            "background_color": "#EBF5FF",
            "background_color_b": "#E0F2FE",
            "background_gradient_type": "linear",
            "background_gradient_angle": {"unit": "deg", "size": 135}
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "row",
                    "flex_direction_tablet": "column",
                    "justify_content": "space-between",
                    "align_items": "center",
                    "gap": {"unit": "px", "size": 30}
                },
                "elements": [
                    # Cột Trái: Icon nhóm + Tiêu đề + Mô tả + Nút bấm
                    {
                        "id": gen_id(),
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "content_width": "full",
                            "width": {"unit": "%", "size": 65},
                            "width_tablet": {"unit": "%", "size": 100},
                            "flex_direction": "row",
                            "align_items": "center",
                            "gap": {"unit": "px", "size": 22}
                        },
                        "elements": [
                            # Icon Users tròn trắng
                            {
                                "id": gen_id(),
                                "elType": "widget",
                                "widgetType": "icon",
                                "isInner": False,
                                "settings": {
                                    "selected_icon": {"value": "fas fa-user-friends", "library": "fa-solid"},
                                    "view": "stacked",
                                    "shape": "circle",
                                    "primary_color": "#FFFFFF",
                                    "secondary_color": COLOR_PRIMARY_BLUE,
                                    "size": {"unit": "px", "size": 26},
                                    "box_shadow_box_shadow_type": "yes",
                                    "box_shadow_box_shadow": {
                                        "horizontal": 0,
                                        "vertical": 4,
                                        "blur": 12,
                                        "spread": 0,
                                        "color": "rgba(0, 123, 255, 0.15)"
                                    }
                                },
                                "elements": []
                            },
                            # Tiêu đề & Button
                            {
                                "id": gen_id(),
                                "elType": "container",
                                "isInner": True,
                                "settings": {
                                    "content_width": "full",
                                    "flex_direction": "column",
                                    "align_items": "flex-start",
                                    "gap": {"unit": "px", "size": 8}
                                },
                                "elements": [
                                    {
                                        "id": gen_id(),
                                        "elType": "widget",
                                        "widgetType": "heading",
                                        "isInner": False,
                                        "settings": {
                                            "title": "Cùng con tự tin chinh phục tiếng Anh",
                                            "header_size": "h3",
                                            "align": "left",
                                            "title_color": COLOR_PRIMARY_BLUE,
                                            "typography_typography": "custom",
                                            "typography_font_family": "Plus Jakarta Sans",
                                            "typography_font_size": {"unit": "px", "size": 24},
                                            "typography_font_size_mobile": {"unit": "px", "size": 20},
                                            "typography_font_weight": "800",
                                            "typography_line_height": {"unit": "em", "size": 1.2}
                                        },
                                        "elements": []
                                    },
                                    {
                                        "id": gen_id(),
                                        "elType": "widget",
                                        "widgetType": "text-editor",
                                        "isInner": False,
                                        "settings": {
                                            "editor": "<p style=\"color: #475569; font-size: 14.5px; margin: 0; line-height: 1.5;\">Kiến tạo tương lai vững chắc với chương trình học chất lượng cùng đội ngũ giáo viên chuyên nghiệp.</p>",
                                            "align": "left"
                                        },
                                        "elements": []
                                    },
                                    {
                                        "id": gen_id(),
                                        "elType": "widget",
                                        "widgetType": "button",
                                        "isInner": False,
                                        "settings": {
                                            "text": "Đăng ký ngay →",
                                            "link": {"url": "https://englishchitra.demoweb360.top/lien-he/"},
                                            "align": "left",
                                            "size": "md",
                                            "typography_typography": "custom",
                                            "typography_font_family": "Plus Jakarta Sans",
                                            "typography_font_size": {"unit": "px", "size": 14},
                                            "typography_font_weight": "700",
                                            "button_text_color": COLOR_TEXT_WHITE,
                                            "background_color": COLOR_PRIMARY_BLUE,
                                            "border_radius": {"unit": "px", "top": "99", "right": "99", "bottom": "99", "left": "99", "isLinked": True},
                                            "padding": {"unit": "px", "top": "12", "right": "28", "bottom": "12", "left": "28", "isLinked": False},
                                            "_margin": {"unit": "px", "top": "8", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
                                        },
                                        "elements": []
                                    }
                                ]
                            }
                        ]
                    },
                    # Cột Phải: Ảnh học viên nữ đeo ba lô cười tươi
                    {
                        "id": gen_id(),
                        "elType": "container",
                        "isInner": True,
                        "settings": {
                            "content_width": "full",
                            "width": {"unit": "%", "size": 30},
                            "width_tablet": {"unit": "%", "size": 100},
                            "flex_direction": "row",
                            "justify_content": "center",
                            "align_items": "center"
                        },
                        "elements": [
                            {
                                "id": gen_id(),
                                "elType": "widget",
                                "widgetType": "image",
                                "isInner": False,
                                "settings": {
                                    "image": {
                                        "url": "https://englishchitra.demoweb360.top/wp-content/uploads/2026/09/image-program-1-1-1.png",
                                        "id": ""
                                    },
                                    "image_size": "full",
                                    "align": "center",
                                    "height": {"unit": "px", "size": 180},
                                    "object_fit": "contain"
                                },
                                "elements": []
                            }
                        ]
                    }
                ]
            }
        ]
    }

# ==============================================================================
# HÀM TỔNG HỢP VÀ XUẤT FILE TỔNG THỂ
# ==============================================================================
def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(dir_path, "bang-vang-hoc-vien-elementor.json")
    zip_path = os.path.join(dir_path, "bang-vang-hoc-vien-elementor.zip")

    page_data = {
        "version": "0.4",
        "title": "Bảng Vàng Học Viên - Tiếng Anh Chị Trà",
        "type": "page",
        "page_settings": [],
        "content": [
            build_section_1_banner(),
            build_section_2_breadcrumb(),
            build_section_3_intro_and_tabs(),
            build_section_4_category_banner(),
            build_section_5_student_grid(),
            build_section_6_stats(),
            build_section_7_cta()
        ]
    }

    # Ghi file JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(page_data, f, ensure_ascii=False, indent=2)
    print("-> Da xuat JSON bang-vang-hoc-vien-elementor.json thanh cong!")

    # Đóng gói ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(json_path, arcname="bang-vang-hoc-vien-elementor.json")
    print("-> Da tao file ZIP bang-vang-hoc-vien-elementor.zip thanh cong!")

if __name__ == "__main__":
    main()
