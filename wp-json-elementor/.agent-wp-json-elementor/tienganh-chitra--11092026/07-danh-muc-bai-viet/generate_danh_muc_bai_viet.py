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
COLOR_TEXT_BODY       = "#4B5563"  # Màu nội dung văn bản (xám trung tính)
COLOR_TEXT_MUTED      = "#6B7280"  # Màu nhãn xám / ngày tháng
COLOR_TEXT_WHITE      = "#FFFFFF"  # Màu trắng
COLOR_BG_LIGHT_BLUE   = "#F0F7FF"  # Nền xanh nhạt hero banner
COLOR_TAG_BG_BLUE     = "#EBF5FF"  # Nền tag danh mục pill
COLOR_TAG_TEXT_BLUE   = "#007BFF"  # Màu chữ tag pill
COLOR_BORDER_LIGHT    = "#E5E7EB"  # Viền thẻ bài viết
COLOR_BTN_HOVER       = "#0056b3"  # Màu nút hover

# ==============================================================================
# HÀM HỖ TRỢ TẠO CÁC NATIVE ELEMENTOR WIDGETS
# ==============================================================================

def create_date_badge_container(day="07", month="Th5", year="2025", is_mini=False):
    """
    Tạo Date Badge hoàn toàn bằng 100% Native Container + Heading Widgets
    Không dùng bất kỳ thẻ HTML nào!
    """
    width_px = 38 if is_mini else 50
    day_size = 12 if is_mini else 18
    sub_size = 8 if is_mini else 10
    pad_tb   = "3" if is_mini else "6"

    badge_elements = [
        # Số ngày (Day)
        {
            "id": gen_id(),
            "elType": "widget",
            "widgetType": "heading",
            "isInner": False,
            "settings": {
                "title": day,
                "header_size": "span",
                "align": "center",
                "title_color": COLOR_TEXT_WHITE,
                "typography_typography": "custom",
                "typography_font_family": "Plus Jakarta Sans",
                "typography_font_size": {"unit": "px", "size": day_size},
                "typography_font_weight": "800",
                "typography_line_height": {"unit": "em", "size": 1.1},
                "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
            },
            "elements": []
        },
        # Tháng (Month)
        {
            "id": gen_id(),
            "elType": "widget",
            "widgetType": "heading",
            "isInner": False,
            "settings": {
                "title": month,
                "header_size": "span",
                "align": "center",
                "title_color": COLOR_TEXT_WHITE,
                "typography_typography": "custom",
                "typography_font_family": "Plus Jakarta Sans",
                "typography_font_size": {"unit": "px", "size": sub_size},
                "typography_font_weight": "700",
                "typography_text_transform": "uppercase",
                "typography_line_height": {"unit": "em", "size": 1.1},
                "_margin": {"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
            },
            "elements": []
        }
    ]

    if not is_mini:
        # Năm (Year)
        badge_elements.append({
            "id": gen_id(),
            "elType": "widget",
            "widgetType": "heading",
            "isInner": False,
            "settings": {
                "title": year,
                "header_size": "span",
                "align": "center",
                "title_color": "rgba(255, 255, 255, 0.9)",
                "typography_typography": "custom",
                "typography_font_family": "Plus Jakarta Sans",
                "typography_font_size": {"unit": "px", "size": sub_size},
                "typography_font_weight": "500",
                "typography_line_height": {"unit": "em", "size": 1.1},
                "_margin": {"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False}
            },
            "elements": []
        })

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "position": "absolute",
            "_position": "absolute",
            "_offset_orientation_h": "start",
            "_offset_x": {"unit": "px", "size": 8 if is_mini else 12},
            "_offset_orientation_v": "start",
            "_offset_y": {"unit": "px", "size": 8 if is_mini else 12},
            "z_index": 2,
            "content_width": "full",
            "width": {"unit": "px", "size": width_px},
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center",
            "background_background": "classic",
            "background_color": COLOR_PRIMARY_BLUE,
            "border_radius": {"unit": "px", "top": "6" if is_mini else "8", "right": "6" if is_mini else "8", "bottom": "6" if is_mini else "8", "left": "6" if is_mini else "8", "isLinked": True},
            "padding": {"unit": "px", "top": pad_tb, "right": "2", "bottom": pad_tb, "left": "2", "isLinked": False},
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {"horizontal": 0, "vertical": 4, "blur": 10, "spread": 0, "color": "rgba(0, 123, 255, 0.35)"}
        },
        "elements": badge_elements
    }

def create_category_pill_widget(tag_name):
    """
    Tạo Tag danh mục pill bằng 100% Native Elementor Button Widget
    """
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "button",
        "isInner": False,
        "settings": {
            "text": tag_name,
            "link": {"url": "#", "is_external": False, "nofollow": False},
            "size": "xs",
            "button_type": "default",
            "background_color": COLOR_TAG_BG_BLUE,
            "button_text_color": COLOR_TAG_TEXT_BLUE,
            "border_radius": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True},
            "typography_typography": "custom",
            "typography_font_family": "Plus Jakarta Sans",
            "typography_font_size": {"unit": "px", "size": 11.5},
            "typography_font_weight": "700",
            "padding": {"unit": "px", "top": "3", "right": "10", "bottom": "3", "left": "10", "isLinked": False},
            "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "8", "left": "0", "isLinked": False}
        },
        "elements": []
    }

# ==============================================================================
# SECTION 1: HERO BANNER & BREADCRUMB
# ==============================================================================

def build_section_1_hero_and_breadcrumb():
    banner_container = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "justify_content": "center",
            "align_items": "center",
            "min_height": {"unit": "px", "size": 170},
            "min_height_mobile": {"unit": "px", "size": 130},
            "padding": {
                "unit": "px",
                "top": "36",
                "right": "20",
                "bottom": "30",
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
            # Tagline
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "TIN TỨC & SỰ KIỆN",
                    "header_size": "h5",
                    "align": "center",
                    "title_color": COLOR_PRIMARY_BLUE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 12},
                    "typography_font_weight": "700",
                    "typography_text_transform": "uppercase",
                    "typography_letter_spacing": {"unit": "px", "size": 2},
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "8", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            # Main Title
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "TIN TỨC & SỰ KIỆN",
                    "header_size": "h1",
                    "align": "center",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 36},
                    "typography_font_size_mobile": {"unit": "px", "size": 26},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2}
                },
                "elements": []
            }
        ]
    }

    # Breadcrumb Container sử dụng các widget Heading native
    breadcrumb_container = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1240},
            "flex_direction": "row",
            "align_items": "center",
            "gap": {"unit": "px", "size": 8},
            "padding": {
                "unit": "px",
                "top": "16",
                "right": "20",
                "bottom": "8",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "🏠 Trang chủ",
                    "header_size": "span",
                    "title_color": COLOR_TEXT_BODY,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "link": {"url": "#", "is_external": False, "nofollow": False}
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "›",
                    "header_size": "span",
                    "title_color": "#9CA3AF",
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13}
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "Tin tức & sự kiện",
                    "header_size": "span",
                    "title_color": COLOR_PRIMARY_BLUE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "typography_font_weight": "600"
                },
                "elements": []
            }
        ]
    }

    return banner_container, breadcrumb_container

# ==============================================================================
# SECTION 2: KHỐI BÀI VIẾT NỔI BẬT (FEATURED CARD)
# ==============================================================================

def build_featured_card():
    img_col = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 48},
            "width_mobile": {"unit": "%", "size": 100},
            "position": "relative",
            "flex_direction": "column"
        },
        "elements": [
            # Ảnh bài viết lớn
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "image",
                "isInner": False,
                "settings": {
                    "image": {
                        "url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=1000&auto=format&fit=crop",
                        "id": ""
                    },
                    "image_size": "large",
                    "image_border_radius": {
                        "unit": "px",
                        "top": "12",
                        "right": "12",
                        "bottom": "12",
                        "left": "12",
                        "isLinked": True
                    }
                },
                "elements": []
            },
            # Date Badge Native Container
            create_date_badge_container("07", "Th5", "2025")
        ]
    }

    content_col = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 52},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "justify_content": "center",
            "align_items": "flex-start",
            "padding": {
                "unit": "px",
                "top": "10",
                "right": "10",
                "bottom": "10",
                "left": "15",
                "isLinked": False
            },
            "padding_mobile": {
                "unit": "px",
                "top": "15",
                "right": "0",
                "bottom": "5",
                "left": "0",
                "isLinked": False
            }
        },
        "elements": [
            # Tag pill widget
            create_category_pill_widget("Tin tức"),
            # Tiêu đề bài viết nổi bật
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "GÓI LỘ TRÌNH TĂNG CƯỜNG KỸ NĂNG TIẾNG ANH – BƯỚC ĐỆM VỮNG CHẮC CHO TƯƠNG LAI",
                    "header_size": "h3",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 20},
                    "typography_font_size_mobile": {"unit": "px", "size": 17},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.3},
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "12", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            # Trích dẫn bài viết
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": "<p>Chương trình được thiết kế theo lộ trình rõ ràng, phù hợp với từng độ tuổi và mục tiêu học tập, giúp học viên phát triển toàn diện 4 kỹ năng: Nghe – Nói – Đọc – Viết.</p>",
                    "text_color": "#556987",
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13.5},
                    "typography_line_height": {"unit": "em", "size": 1.6},
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "18", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            # Nút Xem chi tiết
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "button",
                "isInner": False,
                "settings": {
                    "text": "Xem chi tiết →",
                    "link": {"url": "#", "is_external": False, "nofollow": False},
                    "size": "sm",
                    "button_type": "default",
                    "background_color": COLOR_PRIMARY_BLUE,
                    "button_text_color": COLOR_TEXT_WHITE,
                    "border_radius": {"unit": "px", "top": "30", "right": "30", "bottom": "30", "left": "30", "isLinked": True},
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "typography_font_weight": "700",
                    "padding": {"unit": "px", "top": "10", "right": "22", "bottom": "10", "left": "22", "isLinked": False}
                },
                "elements": []
            }
        ]
    }

    card_wrapper = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "flex_direction_mobile": "column",
            "align_items": "center",
            "background_background": "classic",
            "background_color": COLOR_TEXT_WHITE,
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16", "isLinked": True},
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": 0,
                "vertical": 6,
                "blur": 24,
                "spread": 0,
                "color": "rgba(0, 45, 98, 0.06)"
            },
            "padding": {"unit": "px", "top": "18", "right": "18", "bottom": "18", "left": "18", "isLinked": True},
            "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
        },
        "elements": [img_col, content_col]
    }

    # Mobile Dots Indicators bằng Container Flexbox native (3 dots ● ○ ○)
    dot_active = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "px", "size": 8},
            "min_height": {"unit": "px", "size": 8},
            "border_radius": {"unit": "px", "top": "50", "right": "50", "bottom": "50", "left": "50", "isLinked": True},
            "background_background": "classic",
            "background_color": COLOR_PRIMARY_BLUE
        },
        "elements": []
    }
    dot_inactive_1 = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "px", "size": 8},
            "min_height": {"unit": "px", "size": 8},
            "border_radius": {"unit": "px", "top": "50", "right": "50", "bottom": "50", "left": "50", "isLinked": True},
            "background_background": "classic",
            "background_color": "#D1E5F8"
        },
        "elements": []
    }
    dot_inactive_2 = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "px", "size": 8},
            "min_height": {"unit": "px", "size": 8},
            "border_radius": {"unit": "px", "top": "50", "right": "50", "bottom": "50", "left": "50", "isLinked": True},
            "background_background": "classic",
            "background_color": "#D1E5F8"
        },
        "elements": []
    }

    mobile_dots_container = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "justify_content": "center",
            "align_items": "center",
            "gap": {"unit": "px", "size": 8},
            "hide_desktop": "hidden",
            "hide_tablet": "hidden",
            "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
        },
        "elements": [dot_active, dot_inactive_1, dot_inactive_2]
    }

    return card_wrapper, mobile_dots_container

# ==============================================================================
# BÀI VIẾT DỮ LIỆU & LƯỚI CARD
# ==============================================================================

POSTS_DATA = [
    {
        "day": "05", "month": "Th5", "year": "2025",
        "tag": "Chương trình đào tạo",
        "title": "PHƯƠNG PHÁP HỌC TIẾNG ANH HIỆU QUẢ DÀNH CHO HỌC SINH THCS",
        "excerpt": "Với phương pháp học tập hiện đại, kết hợp giữa lý thuyết và thực hành, học viên sẽ được rèn luyện kỹ năng toàn diện...",
        "image": "https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=800&auto=format&fit=crop"
    },
    {
        "day": "03", "month": "Th5", "year": "2025",
        "tag": "Hoạt động ngoại khóa",
        "title": "CÁC HOẠT ĐỘNG NGOẠI KHÓA GIÚP HỌC VIÊN TỰ TIN HƠN",
        "excerpt": "Không chỉ học trên lớp, các hoạt động ngoại khóa tại trung tâm giúp học viên rèn luyện kỹ năng mềm, phát triển tư duy...",
        "image": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=800&auto=format&fit=crop"
    },
    {
        "day": "01", "month": "Th5", "year": "2025",
        "tag": "Tin tức",
        "title": "LỢI ÍCH CỦA VIỆC HỌC TIẾNG ANH SỚM CHO TRẺ",
        "excerpt": "Học tiếng Anh từ sớm giúp trẻ hình thành sự tư duy linh hoạt, tăng khả năng giao tiếp và mở rộng cơ hội học tập trong tương lai.",
        "image": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?q=80&w=800&auto=format&fit=crop"
    },
    {
        "day": "28", "month": "Th4", "year": "2025",
        "tag": "Sự kiện",
        "title": "CHƯƠNG TRÌNH GIAO LƯU TIẾNG ANH TẠI TRƯỜNG THCS",
        "excerpt": "Chương trình giao lưu với giáo viên bản ngữ đã mang đến nhiều trải nghiệm thú vị, giúp học viên tự tin hơn khi sử dụng Tiếng Anh.",
        "image": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?q=80&w=800&auto=format&fit=crop"
    },
    {
        "day": "26", "month": "Th4", "year": "2025",
        "tag": "Kinh nghiệm học tập",
        "title": "5 TIPS GIÚP BẠN CẢI THIỆN KỸ NĂNG NGHE TIẾNG ANH NHANH CHÓNG",
        "excerpt": "Từ việc luyện nghe mỗi ngày đến sử dụng các nguồn tài liệu đón hộp, những mẹo nhỏ dưới đây sẽ giúp bạn tiến bộ rõ rệt.",
        "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=800&auto=format&fit=crop"
    },
    {
        "day": "20", "month": "Th4", "year": "2025",
        "tag": "Hoạt động ngoại khóa",
        "title": "HỌC VIÊN TIẾNG ANH CHỊ TRÀ ĐẠT THÀNH TÍCH CAO TRONG KỲ THI",
        "excerpt": "Những nỗ lực không ngừng nghỉ đã mang lại kết quả đáng tự hào cho các bạn học viên trong kỳ thi vừa qua.",
        "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=800&auto=format&fit=crop"
    },
    {
        "day": "15", "month": "Th4", "year": "2025",
        "tag": "Chương trình đào tạo",
        "title": "HÀNH TRÌNH TRẢI NGHIỆM TIẾNG ANH TẠI TRẠI HÈ 2025",
        "excerpt": "Trại hè tiếng Anh là cơ hội để học viên rèn luyện kỹ năng, khám phá văn hóa và tạo nên những kỷ niệm đáng nhớ.",
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=800&auto=format&fit=crop"
    },
    {
        "day": "10", "month": "Th4", "year": "2025",
        "tag": "Tin tức",
        "title": "TỔNG KẾT KHOÁ HỌC THÁNG 4/2025",
        "excerpt": "Cùng nhìn lại những khoảnh khắc đáng nhớ, thành tích nổi bật và sự tiến bộ của các học viên trong tháng 4 vừa qua.",
        "image": "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=800&auto=format&fit=crop"
    },
    {
        "day": "05", "month": "Th4", "year": "2025",
        "tag": "Sự kiện",
        "title": "VINH DANH HỌC VIÊN XUẤT SẮC QUÝ I/2025",
        "excerpt": "Cùng vinh danh những gương mặt tiêu biểu đã nỗ lực và đạt thành tích xuất sắc trong học tập và rèn luyện.",
        "image": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?q=80&w=800&auto=format&fit=crop"
    }
]

def build_desktop_post_card(p):
    """
    Card bài viết Desktop chuẩn 100% Native Container và Widgets:
    - Image widget + Date Badge Container
    - Button widget dạng Tag Pill
    - Heading widget H4 (Tiêu đề)
    - Text-Editor widget (Trích dẫn)
    - Heading widget (Link Xem chi tiết)
    """
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": COLOR_TEXT_WHITE,
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True},
            "padding": {"unit": "px", "top": "12", "right": "12", "bottom": "16", "left": "12", "isLinked": False}
        },
        "elements": [
            # Ảnh + Date Badge Container
            {
                "id": gen_id(),
                "elType": "container",
                "isInner": True,
                "settings": {
                    "position": "relative",
                    "width": {"unit": "%", "size": 100},
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "12", "left": "0", "isLinked": False}
                },
                "elements": [
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "image",
                        "isInner": False,
                        "settings": {
                            "image": {"url": p["image"], "id": ""},
                            "image_size": "medium_large",
                            "image_border_radius": {"unit": "px", "top": "10", "right": "10", "bottom": "10", "left": "10", "isLinked": True}
                        },
                        "elements": []
                    },
                    create_date_badge_container(p["day"], p["month"], p["year"])
                ]
            },
            # Tag Pill button
            create_category_pill_widget(p["tag"]),
            # Tiêu đề H4
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": p["title"],
                    "header_size": "h4",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 14.5},
                    "typography_font_weight": "700",
                    "typography_line_height": {"unit": "em", "size": 1.3},
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "8", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            # Trích dẫn bài viết
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": f"<p>{p['excerpt']}</p>",
                    "text_color": "#556987",
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 12.5},
                    "typography_line_height": {"unit": "em", "size": 1.5},
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "12", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            # Link Xem chi tiết
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "Xem chi tiết →",
                    "header_size": "span",
                    "title_color": COLOR_PRIMARY_BLUE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 12.5},
                    "typography_font_weight": "700",
                    "link": {"url": "#", "is_external": False, "nofollow": False}
                },
                "elements": []
            }
        ]
    }

def build_mobile_horizontal_list_item(p):
    """
    Card bài viết hàng ngang trên Mobile (100% Native Container + Widgets):
    - Left: Container Thumbnail (Image + Mini Date Badge)
    - Middle: Container Info (Category Pill Button + Heading Title)
    - Right: Native Icon Widget (fas fa-chevron-right)
    """
    # Thumbnail Container
    thumb_container = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "position": "relative",
            "width": {"unit": "px", "size": 85},
            "flex_shrink": "0"
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "image",
                "isInner": False,
                "settings": {
                    "image": {"url": p["image"], "id": ""},
                    "image_size": "medium",
                    "image_border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True}
                },
                "elements": []
            },
            create_date_badge_container(p["day"], p["month"], p["year"], is_mini=True)
        ]
    }

    # Info Container
    info_container = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "flex_grow": "1",
            "flex_direction": "column",
            "align_items": "flex-start",
            "padding": {"unit": "px", "top": "0", "right": "8", "bottom": "0", "left": "12", "isLinked": False}
        },
        "elements": [
            create_category_pill_widget(p["tag"]),
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": p["title"],
                    "header_size": "h4",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "typography_font_weight": "700",
                    "typography_line_height": {"unit": "em", "size": 1.3}
                },
                "elements": []
            }
        ]
    }

    # Arrow Icon
    arrow_icon = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "icon",
        "isInner": False,
        "settings": {
            "selected_icon": {"value": "fas fa-chevron-right", "library": "fa-solid"},
            "size": {"unit": "px", "size": 13},
            "primary_color": "#9CA3AF"
        },
        "elements": []
    }

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "align_items": "center",
            "justify_content": "space-between",
            "background_background": "classic",
            "background_color": COLOR_TEXT_WHITE,
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True},
            "padding": {"unit": "px", "top": "10", "right": "12", "bottom": "10", "left": "10", "isLinked": False},
            "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "12", "left": "0", "isLinked": False}
        },
        "elements": [thumb_container, info_container, arrow_icon]
    }

# ==============================================================================
# PHÂN TRANG (PAGINATION) BẰNG NATIVE BUTTON WIDGETS
# ==============================================================================

def build_pagination():
    def create_page_btn(text, is_active=False):
        return {
            "id": gen_id(),
            "elType": "widget",
            "widgetType": "button",
            "isInner": False,
            "settings": {
                "text": text,
                "link": {"url": "#", "is_external": False, "nofollow": False},
                "size": "xs",
                "button_type": "default",
                "background_color": COLOR_PRIMARY_BLUE if is_active else "transparent",
                "button_text_color": COLOR_TEXT_WHITE if is_active else "#4B5563",
                "border_radius": {"unit": "px", "top": "50", "right": "50", "bottom": "50", "left": "50", "isLinked": True},
                "typography_typography": "custom",
                "typography_font_family": "Plus Jakarta Sans",
                "typography_font_size": {"unit": "px", "size": 13},
                "typography_font_weight": "700" if is_active else "600",
                "padding": {"unit": "px", "top": "6", "right": "12", "bottom": "6", "left": "12", "isLinked": False}
            },
            "elements": []
        }

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "justify_content": "center",
            "align_items": "center",
            "gap": {"unit": "px", "size": 6},
            "_margin": {"unit": "px", "top": "35", "right": "0", "bottom": "10", "left": "0", "isLinked": False},
            "hide_mobile": "hidden"
        },
        "elements": [
            create_page_btn("‹"),
            create_page_btn("1", is_active=True),
            create_page_btn("2"),
            create_page_btn("3"),
            create_page_btn("4"),
            create_page_btn("›")
        ]
    }

# ==============================================================================
# CỘT PHẢI (SIDEBAR) 100% NATIVE WIDGETS
# ==============================================================================

def build_sidebar_search_widget():
    """Sidebar 1: Native Search-Form Widget"""
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": COLOR_TEXT_WHITE,
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {"unit": "px", "top": "14", "right": "14", "bottom": "14", "left": "14", "isLinked": True},
            "padding": {"unit": "px", "top": "18", "right": "18", "bottom": "18", "left": "18", "isLinked": True}
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "🔍 Tìm kiếm bài viết",
                    "header_size": "h4",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 15},
                    "typography_font_weight": "800",
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "14", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "search-form",
                "isInner": False,
                "settings": {
                    "skin": "classic",
                    "placeholder": "Nhập từ khóa...",
                    "button_type": "icon",
                    "icon": {"value": "fas fa-search", "library": "fa-solid"},
                    "button_color": COLOR_PRIMARY_BLUE,
                    "button_text_color": COLOR_TEXT_WHITE,
                    "border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True}
                },
                "elements": []
            }
        ]
    }

def build_sidebar_categories_widget():
    """Sidebar 2: Native Category Rows với Icon và Badge Button"""
    cats = [
        {"name": "Tin tức", "count": 24},
        {"name": "Sự kiện", "count": 18},
        {"name": "Hoạt động ngoại khóa", "count": 12},
        {"name": "Chương trình đào tạo", "count": 10},
        {"name": "Kinh nghiệm học tập", "count": 8}
    ]

    cat_rows = []
    for c in cats:
        cat_rows.append({
            "id": gen_id(),
            "elType": "container",
            "isInner": True,
            "settings": {
                "content_width": "full",
                "flex_direction": "row",
                "justify_content": "space-between",
                "align_items": "center",
                "padding": {"unit": "px", "top": "8", "right": "0", "bottom": "8", "left": "0", "isLinked": False},
                "border_border": "dashed",
                "border_width": {"unit": "px", "top": "0", "right": "0", "bottom": "1", "left": "0", "isLinked": False},
                "border_color": "#F0F2F5"
            },
            "elements": [
                # Left: Dot icon + Category name
                {
                    "id": gen_id(),
                    "elType": "container",
                    "isInner": True,
                    "settings": {
                        "flex_direction": "row",
                        "align_items": "center",
                        "gap": {"unit": "px", "size": 8}
                    },
                    "elements": [
                        {
                            "id": gen_id(),
                            "elType": "widget",
                            "widgetType": "icon",
                            "isInner": False,
                            "settings": {
                                "selected_icon": {"value": "fas fa-circle", "library": "fa-solid"},
                                "size": {"unit": "px", "size": 6},
                                "primary_color": "#93C5FD"
                            },
                            "elements": []
                        },
                        {
                            "id": gen_id(),
                            "elType": "widget",
                            "widgetType": "heading",
                            "isInner": False,
                            "settings": {
                                "title": c["name"],
                                "header_size": "span",
                                "title_color": COLOR_TEXT_BODY,
                                "typography_typography": "custom",
                                "typography_font_family": "Plus Jakarta Sans",
                                "typography_font_size": {"unit": "px", "size": 13.5},
                                "typography_font_weight": "600",
                                "link": {"url": "#", "is_external": False, "nofollow": False}
                            },
                            "elements": []
                        }
                    ]
                },
                # Right: Count badge
                {
                    "id": gen_id(),
                    "elType": "widget",
                    "widgetType": "button",
                    "isInner": False,
                    "settings": {
                        "text": str(c["count"]),
                        "size": "xs",
                        "background_color": COLOR_TAG_BG_BLUE,
                        "button_text_color": COLOR_TAG_TEXT_BLUE,
                        "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True},
                        "typography_typography": "custom",
                        "typography_font_family": "Plus Jakarta Sans",
                        "typography_font_size": {"unit": "px", "size": 11},
                        "typography_font_weight": "700",
                        "padding": {"unit": "px", "top": "2", "right": "8", "bottom": "2", "left": "8", "isLinked": False}
                    },
                    "elements": []
                }
            ]
        })

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": COLOR_TEXT_WHITE,
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {"unit": "px", "top": "14", "right": "14", "bottom": "14", "left": "14", "isLinked": True},
            "padding": {"unit": "px", "top": "18", "right": "18", "bottom": "14", "left": "18", "isLinked": True}
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "📁 Danh mục tin tức",
                    "header_size": "h4",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 15},
                    "typography_font_weight": "800",
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "10", "left": "0", "isLinked": False}
                },
                "elements": []
            }
        ] + cat_rows
    }

def build_sidebar_popular_posts_widget():
    """Sidebar 3: Bài viết nổi bật mini (Image + Heading widgets)"""
    pop_posts = [
        {
            "title": "Gói lộ trình tăng cường kỹ năng tiếng Anh – Bước đệm vững chắc cho tương lai",
            "date": "07/05/2025",
            "thumb": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=200&auto=format&fit=crop"
        },
        {
            "title": "Chương trình giao lưu tiếng Anh tại trường THCS",
            "date": "28/04/2025",
            "thumb": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?q=80&w=200&auto=format&fit=crop"
        },
        {
            "title": "5 tips giúp bạn cải thiện kỹ năng nghe tiếng Anh nhanh chóng",
            "date": "26/04/2025",
            "thumb": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=200&auto=format&fit=crop"
        },
        {
            "title": "Học viên đạt thành tích cao trong kỳ thi",
            "date": "07/05/2025",
            "thumb": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=200&auto=format&fit=crop"
        }
    ]

    post_rows = []
    for p in pop_posts:
        post_rows.append({
            "id": gen_id(),
            "elType": "container",
            "isInner": True,
            "settings": {
                "content_width": "full",
                "flex_direction": "row",
                "align_items": "center",
                "gap": {"unit": "px", "size": 12},
                "padding": {"unit": "px", "top": "10", "right": "0", "bottom": "10", "left": "0", "isLinked": False},
                "border_border": "dashed",
                "border_width": {"unit": "px", "top": "0", "right": "0", "bottom": "1", "left": "0", "isLinked": False},
                "border_color": "#F0F2F5"
            },
            "elements": [
                # Thumbnail
                {
                    "id": gen_id(),
                    "elType": "widget",
                    "widgetType": "image",
                    "isInner": False,
                    "settings": {
                        "image": {"url": p["thumb"], "id": ""},
                        "image_size": "thumbnail",
                        "width": {"unit": "px", "size": 60},
                        "image_border_radius": {"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True}
                    },
                    "elements": []
                },
                # Content
                {
                    "id": gen_id(),
                    "elType": "container",
                    "isInner": True,
                    "settings": {
                        "flex_grow": "1",
                        "flex_direction": "column"
                    },
                    "elements": [
                        {
                            "id": gen_id(),
                            "elType": "widget",
                            "widgetType": "heading",
                            "isInner": False,
                            "settings": {
                                "title": p["title"],
                                "header_size": "h5",
                                "title_color": COLOR_NAVY_TITLE,
                                "typography_typography": "custom",
                                "typography_font_family": "Plus Jakarta Sans",
                                "typography_font_size": {"unit": "px", "size": 12.5},
                                "typography_font_weight": "700",
                                "typography_line_height": {"unit": "em", "size": 1.3},
                                "link": {"url": "#", "is_external": False, "nofollow": False},
                                "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "4", "left": "0", "isLinked": False}
                            },
                            "elements": []
                        },
                        {
                            "id": gen_id(),
                            "elType": "widget",
                            "widgetType": "heading",
                            "isInner": False,
                            "settings": {
                                "title": "🕒 " + p["date"],
                                "header_size": "span",
                                "title_color": COLOR_TEXT_MUTED,
                                "typography_typography": "custom",
                                "typography_font_family": "Plus Jakarta Sans",
                                "typography_font_size": {"unit": "px", "size": 11}
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
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "background_background": "classic",
            "background_color": COLOR_TEXT_WHITE,
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {"unit": "px", "top": "14", "right": "14", "bottom": "14", "left": "14", "isLinked": True},
            "padding": {"unit": "px", "top": "18", "right": "18", "bottom": "14", "left": "18", "isLinked": True}
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "📰 Bài viết nổi bật",
                    "header_size": "h4",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 15},
                    "typography_font_weight": "800",
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "6", "left": "0", "isLinked": False}
                },
                "elements": []
            }
        ] + post_rows
    }

def build_sidebar_cta_banner():
    """Sidebar 4: Banner CTA Tuyển sinh bằng Native Containers & Widgets"""
    left_cta = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 60},
            "flex_direction": "column",
            "align_items": "flex-start",
            "justify_content": "center",
            "z_index": 2
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "Cùng con tự tin chinh phục tiếng Anh",
                    "header_size": "h4",
                    "title_color": COLOR_PRIMARY_BLUE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 18},
                    "typography_font_weight": "800",
                    "typography_font_style": "italic",
                    "typography_line_height": {"unit": "em", "size": 1.3},
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "6", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "Kiến tạo tương lai vững chắc!",
                    "header_size": "p",
                    "title_color": COLOR_TEXT_BODY,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 11.5},
                    "typography_font_weight": "500",
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "14", "left": "0", "isLinked": False}
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
                    "link": {"url": "#", "is_external": False, "nofollow": False},
                    "size": "xs",
                    "background_color": COLOR_PRIMARY_BLUE,
                    "button_text_color": COLOR_TEXT_WHITE,
                    "border_radius": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True},
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 12},
                    "typography_font_weight": "700",
                    "padding": {"unit": "px", "top": "7", "right": "16", "bottom": "7", "left": "16", "isLinked": False}
                },
                "elements": []
            }
        ]
    }

    right_cta = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 40},
            "position": "absolute",
            "_position": "absolute",
            "_offset_orientation_h": "end",
            "_offset_x": {"unit": "px", "size": 0},
            "_offset_orientation_v": "end",
            "_offset_y": {"unit": "px", "size": 0},
            "z_index": 1
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "image",
                "isInner": False,
                "settings": {
                    "image": {
                        "url": "https://images.unsplash.com/photo-1544717305-2782549b5136?q=80&w=400&auto=format&fit=crop",
                        "id": ""
                    },
                    "image_size": "medium"
                },
                "elements": []
            }
        ]
    }

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "position": "relative",
            "overflow": "hidden",
            "flex_direction": "row",
            "background_background": "gradient",
            "background_color": "#E6F3FF",
            "background_color_b": "#CCE6FF",
            "background_gradient_type": "linear",
            "background_gradient_angle": {"unit": "deg", "size": 135},
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": "#B8DCFF",
            "border_radius": {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16", "isLinked": True},
            "padding": {"unit": "px", "top": "22", "right": "18", "bottom": "22", "left": "18", "isLinked": True}
        },
        "elements": [left_cta, right_cta]
    }

# ==============================================================================
# SECTION 2: THÂN TRANG 2 CỘT TỔNG HỢP
# ==============================================================================

def build_section_2_main_body():
    # 1. CỘT TRÁI (Main Content)
    featured_card, mobile_dots = build_featured_card()

    # Thanh tiêu đề "| TIN TỨC MỚI NHẤT" + "Xem tất cả →"
    heading_bar = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "justify_content": "space-between",
            "align_items": "center",
            "_margin": {"unit": "px", "top": "5", "right": "0", "bottom": "18", "left": "0", "isLinked": False}
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "| TIN TỨC MỚI NHẤT",
                    "header_size": "h3",
                    "title_color": COLOR_NAVY_TITLE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 18},
                    "typography_font_weight": "800"
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "Xem tất cả →",
                    "header_size": "h6",
                    "title_color": COLOR_PRIMARY_BLUE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "typography_font_weight": "700",
                    "link": {"url": "#", "is_external": False, "nofollow": False}
                },
                "elements": []
            }
        ]
    }

    # Lưới bài viết Desktop (3 cột Grid)
    desktop_grid = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "container_type": "grid",
            "grid_columns_grid": {"unit": "custom", "size": 3},
            "grid_columns_grid_tablet": {"unit": "custom", "size": 2},
            "grid_columns_grid_mobile": {"unit": "custom", "size": 1},
            "grid_gap": {"unit": "px", "row": 20, "column": 20, "isLinked": True},
            "hide_mobile": "hidden"
        },
        "elements": [build_desktop_post_card(p) for p in POSTS_DATA]
    }

    # Lưới bài viết Mobile (Horizontal List theo ảnh 2)
    mobile_list = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "hide_desktop": "hidden",
            "hide_tablet": "hidden"
        },
        "elements": [build_mobile_horizontal_list_item(p) for p in POSTS_DATA[:3]]
    }

    # Cụm Phân trang
    pagination = build_pagination()

    # Mobile CTA Banner đặt ở cuối nội dung trên điện thoại
    mobile_cta = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "hide_desktop": "hidden",
            "hide_tablet": "hidden",
            "_margin": {"unit": "px", "top": "20", "right": "0", "bottom": "10", "left": "0", "isLinked": False}
        },
        "elements": [build_sidebar_cta_banner()]
    }

    left_column = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 68},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column"
        },
        "elements": [
            featured_card,
            mobile_dots,
            heading_bar,
            desktop_grid,
            mobile_list,
            pagination,
            mobile_cta
        ]
    }

    # 2. CỘT PHẢI (Sidebar Widgets - Ẩn trên mobile theo ảnh 2)
    right_column = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 32},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "gap": {"unit": "px", "size": 22},
            "hide_mobile": "hidden"
        },
        "elements": [
            build_sidebar_search_widget(),
            build_sidebar_categories_widget(),
            build_sidebar_popular_posts_widget(),
            build_sidebar_cta_banner()
        ]
    }

    # Wrapper 2 Cột Boxed 1240px
    main_container = {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1240},
            "flex_direction": "row",
            "flex_direction_mobile": "column",
            "align_items": "flex-start",
            "gap": {"unit": "px", "size": 30},
            "padding": {
                "unit": "px",
                "top": "15",
                "right": "20",
                "bottom": "60",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [left_column, right_column]
    }

    return main_container

def build_danh_muc_bai_viet_json():
    """Xây dựng gói Page Template hoàn chỉnh cho Trang Danh Mục Bài Viết"""
    sec1_banner, sec1_breadcrumb = build_section_1_hero_and_breadcrumb()
    sec2_main = build_section_2_main_body()

    return {
        "version": "0.4",
        "title": "Trang Danh Mục Bài Viết - Tiếng Anh Chị Trà",
        "type": "page",
        "page_settings": [],
        "content": [sec1_banner, sec1_breadcrumb, sec2_main]
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
    page_data = build_danh_muc_bai_viet_json()
    save_and_zip(page_data, "danh-muc-bai-viet-elementor", out_dir)
    print("\n[COMPLETED] Successfully generated Danh Muc Bai Viet Elementor JSON & ZIP (100% Native Widgets)!")
