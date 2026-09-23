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

def build_section_1_hero_and_breadcrumb():
    """
    SECTION 1: HERO BANNER & BREADCRUMB
    - Hero Banner: Nền xanh nhạt #F0F7FF, họa tiết tinh tế, tiêu đề kép 'TIN TỨC & SỰ KIỆN'
    - Breadcrumb Bar: Trang chủ > Tin tức & sự kiện
    """
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

    # Breadcrumb Container
    breadcrumb_container = {
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
                "bottom": "8",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": '<p style="margin: 0; font-size: 13px; color: #6B7280; font-family: \'Plus Jakarta Sans\', sans-serif;"><span style="color: #4B5563;">🏠 Trang chủ</span> <span style="margin: 0 6px; color: #9CA3AF;">›</span> <span style="color: #007BFF; font-weight: 600;">Tin tức & sự kiện</span></p>'
                },
                "elements": []
            }
        ]
    }

    return banner_container, breadcrumb_container

def create_date_badge_html(day="07", month="Th5", year="2025"):
    """Tạo badge ngày tháng bo tròn đè lên góc ảnh đại diện"""
    return f"""<div style="background: #007BFF; color: #ffffff; border-radius: 8px; width: 48px; padding: 6px 2px; text-align: center; box-shadow: 0 4px 10px rgba(0, 123, 255, 0.35); font-family: 'Plus Jakarta Sans', sans-serif; line-height: 1.1;">
  <div style="font-size: 17px; font-weight: 800; letter-spacing: -0.5px;">{day}</div>
  <div style="font-size: 10px; font-weight: 700; text-transform: uppercase; margin-top: 2px;">{month}</div>
  <div style="font-size: 10px; opacity: 0.9; margin-top: 1px;">{year}</div>
</div>"""

def build_featured_card():
    """
    Khối Bài Viết Nổi Bật Đầu Trang (Featured Post Card)
    - Khung trắng bo góc 16px, đổ bóng nhẹ
    - Desktop: 2 cột ngang (Ảnh trái 48%, Nội dung phải 52%)
    - Mobile: 1 cột dọc (Ảnh trên, Nội dung dưới, kèm 3 dots phân trang phía dưới)
    """
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
            # Date Badge Absolute Overlay
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "html",
                "isInner": False,
                "settings": {
                    "html": create_date_badge_html("07", "Th5", "2025"),
                    "_position": "absolute",
                    "_offset_orientation_h": "start",
                    "_offset_x": {"unit": "px", "size": 12},
                    "_offset_orientation_v": "start",
                    "_offset_y": {"unit": "px", "size": 12},
                    "z_index": 2
                },
                "elements": []
            }
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
            # Tag pill danh mục
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "html",
                "isInner": False,
                "settings": {
                    "html": '<span style="display: inline-block; background-color: #EBF5FF; color: #007BFF; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 20px; font-family: \'Plus Jakarta Sans\', sans-serif;">Tin tức</span>',
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "10", "left": "0", "isLinked": False}
                },
                "elements": []
            },
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
                    "editor": '<p style="font-size: 13.5px; line-height: 1.6; color: #556987; margin: 0; font-family: \'Plus Jakarta Sans\', sans-serif;">Chương trình được thiết kế theo lộ trình rõ ràng, phù hợp với từng độ tuổi và mục tiêu học tập, giúp học viên phát triển toàn diện 4 kỹ năng: Nghe – Nói – Đọc – Viết.</p>',
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

    # Card Featured Container
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

    # Mobile Dots Indicators (Chỉ hiển thị trên mobile theo ảnh 2)
    mobile_dots = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "html",
        "isInner": False,
        "settings": {
            "html": '<div style="display: flex; justify-content: center; gap: 8px; margin-bottom: 25px;"><span style="width: 8px; height: 8px; border-radius: 50%; background: #007BFF; display: inline-block;"></span><span style="width: 8px; height: 8px; border-radius: 50%; background: #D1E5F8; display: inline-block;"></span><span style="width: 8px; height: 8px; border-radius: 50%; background: #D1E5F8; display: inline-block;"></span></div>',
            "hide_desktop": "default",
            "hide_tablet": "default",
            "hide_mobile": ""
        },
        "elements": []
    }

    return card_wrapper, mobile_dots

def build_heading_bar():
    """Thanh tiêu đề: '| TIN TỨC MỚI NHẤT' + 'Xem tất cả →'"""
    return {
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

# Dữ liệu 9 bài viết mẫu chuẩn xác theo đúng mockup ảnh
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
    """Xây dựng 1 Card bài viết trên Desktop (Dạng thẻ đứng 3 cột)"""
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
            # Ảnh + Date Badge Overlay
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
                    {
                        "id": gen_id(),
                        "elType": "widget",
                        "widgetType": "html",
                        "isInner": False,
                        "settings": {
                            "html": create_date_badge_html(p["day"], p["month"], p["year"]),
                            "_position": "absolute",
                            "_offset_orientation_h": "start",
                            "_offset_x": {"unit": "px", "size": 8},
                            "_offset_orientation_v": "start",
                            "_offset_y": {"unit": "px", "size": 8},
                            "z_index": 2
                        },
                        "elements": []
                    }
                ]
            },
            # Tag pill
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "html",
                "isInner": False,
                "settings": {
                    "html": f'<span style="display: inline-block; background-color: #EBF5FF; color: #007BFF; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 15px; font-family: \'Plus Jakarta Sans\', sans-serif;">{p["tag"]}</span>',
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "8", "left": "0", "isLinked": False}
                },
                "elements": []
            },
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
            # Excerpt
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": f'<p style="font-size: 12.5px; line-height: 1.5; color: #556987; margin: 0; font-family: \'Plus Jakarta Sans\', sans-serif;">{p["excerpt"]}</p>',
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
    Xây dựng 1 hàng bài viết trên Mobile theo đúng ảnh 2:
    - Thumbnail bên trái kèm Date Badge
    - Bên phải là Tag Pill + Tiêu đề bài viết
    - Icon mũi tên '>' ở góc phải
    """
    html_code = f"""
<div style="display: flex; align-items: center; justify-content: space-between; background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 10px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); font-family: 'Plus Jakarta Sans', sans-serif;">
  <div style="display: flex; align-items: center; gap: 12px; flex: 1;">
    <div style="position: relative; width: 85px; height: 68px; flex-shrink: 0; border-radius: 8px; overflow: hidden;">
      <img src="{p['image']}" alt="{p['title']}" style="width: 100%; height: 100%; object-fit: cover;" />
      <div style="position: absolute; top: 4px; left: 4px; background: #007BFF; color: #fff; border-radius: 4px; width: 34px; padding: 2px 0; text-align: center; line-height: 1;">
        <span style="font-size: 11px; font-weight: 800; display: block;">{p['day']}</span>
        <span style="font-size: 7.5px; font-weight: 600; text-transform: uppercase;">{p['month']}</span>
      </div>
    </div>
    <div style="flex: 1; min-width: 0;">
      <span style="display: inline-block; background-color: #EBF5FF; color: #007BFF; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 10px; margin-bottom: 4px;">{p['tag']}</span>
      <h4 style="margin: 0; font-size: 13px; font-weight: 700; line-height: 1.3; color: #002D62; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">{p['title']}</h4>
    </div>
  </div>
  <div style="color: #9CA3AF; font-size: 16px; font-weight: bold; margin-left: 8px; flex-shrink: 0;">›</div>
</div>
"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "html",
        "isInner": False,
        "settings": {
            "html": html_code.strip()
        },
        "elements": []
    }

def build_posts_grid_container():
    """Lưới 9 bài viết Desktop (3 cột) và Container ẩn/hiện theo Responsive"""
    # 1. Desktop Grid (3 cột x 3 hàng)
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
            "hide_mobile": "hidden"  # Ẩn trên mobile vì mobile dùng layout List Item ngang
        },
        "elements": [build_desktop_post_card(p) for p in POSTS_DATA]
    }

    # 2. Mobile Horizontal List (Hiển thị 3 bài đầu tiên theo ảnh 2 mobile)
    mobile_list = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "hide_desktop": "hidden",
            "hide_tablet": "hidden"  # Chỉ hiển thị trên mobile
        },
        "elements": [build_mobile_horizontal_list_item(p) for p in POSTS_DATA[:3]]
    }

    return desktop_grid, mobile_list

def build_pagination():
    """Cụm phân trang: <  1  2  3  4  >"""
    html_pagination = """
<div style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 35px; font-family: 'Plus Jakarta Sans', sans-serif;">
  <a href="#" style="display: inline-flex; justify-content: center; align-items: center; width: 32px; height: 32px; border-radius: 50%; color: #6B7280; text-decoration: none; font-size: 13px; font-weight: 600;">‹</a>
  <span style="display: inline-flex; justify-content: center; align-items: center; width: 32px; height: 32px; border-radius: 50%; background-color: #007BFF; color: #FFFFFF; font-size: 13px; font-weight: 700; box-shadow: 0 2px 8px rgba(0, 123, 255, 0.35);">1</span>
  <a href="#" style="display: inline-flex; justify-content: center; align-items: center; width: 32px; height: 32px; border-radius: 50%; color: #4B5563; text-decoration: none; font-size: 13px; font-weight: 600;">2</a>
  <a href="#" style="display: inline-flex; justify-content: center; align-items: center; width: 32px; height: 32px; border-radius: 50%; color: #4B5563; text-decoration: none; font-size: 13px; font-weight: 600;">3</a>
  <a href="#" style="display: inline-flex; justify-content: center; align-items: center; width: 32px; height: 32px; border-radius: 50%; color: #4B5563; text-decoration: none; font-size: 13px; font-weight: 600;">4</a>
  <a href="#" style="display: inline-flex; justify-content: center; align-items: center; width: 32px; height: 32px; border-radius: 50%; color: #6B7280; text-decoration: none; font-size: 13px; font-weight: 600;">›</a>
</div>
"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "html",
        "isInner": False,
        "settings": {
            "html": html_pagination.strip(),
            "hide_mobile": "hidden"
        },
        "elements": []
    }

# ==============================================================================
# CÁC WIDGET BÊN CỘT PHẢI (SIDEBAR)
# ==============================================================================

def build_sidebar_search_widget():
    """Sidebar Widget 1: Tìm kiếm bài viết"""
    html_search = """
<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 18px; box-shadow: 0 4px 16px rgba(0, 45, 98, 0.04); font-family: 'Plus Jakarta Sans', sans-serif;">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
    <span style="color: #007BFF; font-size: 16px;">🔍</span>
    <h4 style="margin: 0; font-size: 15px; font-weight: 800; color: #002D62;">Tìm kiếm bài viết</h4>
  </div>
  <div style="display: flex; gap: 8px;">
    <input type="text" placeholder="Nhập từ khóa..." style="flex: 1; border: 1px solid #E5E7EB; border-radius: 8px; padding: 9px 12px; font-size: 13px; outline: none; background: #F9FAFB;" />
    <button type="button" style="background: #007BFF; color: #fff; border: none; border-radius: 8px; padding: 0 14px; cursor: pointer; display: flex; align-items: center; justify-content: center;">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </button>
  </div>
</div>
"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "html",
        "isInner": False,
        "settings": {"html": html_search.strip()},
        "elements": []
    }

def build_sidebar_categories_widget():
    """Sidebar Widget 2: Danh mục tin tức"""
    cats = [
        {"name": "Tin tức", "count": 24},
        {"name": "Sự kiện", "count": 18},
        {"name": "Hoạt động ngoại khóa", "count": 12},
        {"name": "Chương trình đào tạo", "count": 10},
        {"name": "Kinh nghiệm học tập", "count": 8},
    ]

    items_html = ""
    for c in cats:
        items_html += f"""
    <li style="display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px dashed #F0F2F5;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span style="width: 6px; height: 6px; border-radius: 50%; background: #93C5FD; display: inline-block;"></span>
        <a href="#" style="color: #4B5563; font-size: 13.5px; font-weight: 600; text-decoration: none; transition: color 0.2s;">{c['name']}</a>
      </div>
      <span style="background: #EBF5FF; color: #007BFF; font-size: 11px; font-weight: 700; border-radius: 12px; padding: 2px 8px;">{c['count']}</span>
    </li>
"""

    html_cat = f"""
<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 18px; box-shadow: 0 4px 16px rgba(0, 45, 98, 0.04); font-family: 'Plus Jakarta Sans', sans-serif;">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
    <span style="color: #007BFF; font-size: 16px;">📁</span>
    <h4 style="margin: 0; font-size: 15px; font-weight: 800; color: #002D62;">Danh mục tin tức</h4>
  </div>
  <ul style="list-style: none; padding: 0; margin: 0;">
    {items_html.strip()}
  </ul>
</div>
"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "html",
        "isInner": False,
        "settings": {"html": html_cat.strip()},
        "elements": []
    }

def build_sidebar_popular_posts_widget():
    """Sidebar Widget 3: Bài viết nổi bật (4 bài mini hàng ngang)"""
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

    items_html = ""
    for p in pop_posts:
        items_html += f"""
    <div style="display: flex; gap: 12px; align-items: center; padding: 10px 0; border-bottom: 1px dashed #F0F2F5;">
      <img src="{p['thumb']}" alt="{p['title']}" style="width: 60px; height: 50px; border-radius: 8px; object-fit: cover; flex-shrink: 0;" />
      <div style="flex: 1; min-width: 0;">
        <a href="#" style="color: #002D62; font-size: 12.5px; font-weight: 700; line-height: 1.3; text-decoration: none; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 4px;">{p['title']}</a>
        <div style="color: #6B7280; font-size: 11px; display: flex; align-items: center; gap: 4px;">
          <span>🕒</span> {p['date']}
        </div>
      </div>
    </div>
"""

    html_pop = f"""
<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; padding: 18px; box-shadow: 0 4px 16px rgba(0, 45, 98, 0.04); font-family: 'Plus Jakarta Sans', sans-serif;">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
    <span style="color: #007BFF; font-size: 16px;">📰</span>
    <h4 style="margin: 0; font-size: 15px; font-weight: 800; color: #002D62;">Bài viết nổi bật</h4>
  </div>
  {items_html.strip()}
</div>
"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "html",
        "isInner": False,
        "settings": {"html": html_pop.strip()},
        "elements": []
    }

def build_sidebar_cta_banner():
    """Sidebar Widget 4: Banner CTA Tuyển sinh (Cùng con tự tin chinh phục tiếng Anh)"""
    html_cta = """
<div style="position: relative; overflow: hidden; background: linear-gradient(135deg, #E6F3FF 0%, #CCE6FF 100%); border: 1px solid #B8DCFF; border-radius: 16px; padding: 22px 18px; box-shadow: 0 8px 24px rgba(0, 123, 255, 0.08); font-family: 'Plus Jakarta Sans', sans-serif;">
  <div style="position: relative; z-index: 2; max-width: 60%;">
    <h3 style="margin: 0 0 6px 0; font-size: 18px; font-weight: 800; color: #007BFF; line-height: 1.3; font-style: italic;">Cùng con tự tin chinh phục tiếng Anh</h3>
    <p style="margin: 0 0 14px 0; font-size: 11.5px; color: #4B5563; font-weight: 500;">Kiến tạo tương lai vững chắc!</p>
    <a href="#" style="display: inline-block; background: #007BFF; color: #FFFFFF; font-size: 12px; font-weight: 700; padding: 7px 16px; border-radius: 20px; text-decoration: none; box-shadow: 0 3px 10px rgba(0, 123, 255, 0.35);">Đăng ký ngay →</a>
  </div>
  <div style="position: absolute; right: 0; bottom: 0; width: 45%; max-height: 100%; display: flex; align-items: flex-end; justify-content: flex-end;">
    <img src="https://images.unsplash.com/photo-1544717305-2782549b5136?q=80&w=400&auto=format&fit=crop" alt="Học viên Tiếng Anh Chị Trà" style="width: 110%; object-fit: contain; pointer-events: none;" />
  </div>
</div>
"""
    return {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "html",
        "isInner": False,
        "settings": {"html": html_cta.strip()},
        "elements": []
    }

def build_section_2_main_body():
    """
    SECTION 2: THÂN TRANG 2 CỘT (Main Content + Sidebar)
    - Boxed 1240px
    - Desktop: Cột Trái 68%, Cột Phải 32%
    - Mobile: Xếp dọc 1 cột (100% width)
    """
    # 1. CỘT TRÁI (Main Content)
    featured_card, mobile_dots = build_featured_card()
    heading_bar = build_heading_bar()
    desktop_grid, mobile_list = build_posts_grid_container()
    pagination = build_pagination()

    # Mobile CTA Banner xuất hiện ở cuối content trên mobile theo ảnh 2
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

    # 2. CỘT PHẢI (Sidebar Widgets - Ẩn trên mobile theo ảnh 2 vì mobile có bố cục riêng)
    right_column = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 32},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "gap": {"unit": "px", "size": 22},
            "hide_mobile": "hidden"  # Ẩn sidebar trên mobile theo đúng thiết kế ảnh 2
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
    print("\n[COMPLETED] Successfully generated Danh Muc Bai Viet Elementor JSON & ZIP!")
