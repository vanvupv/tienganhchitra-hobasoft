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

# ==============================================================================
# SECTION 1: BANNER (ĐẦU TRANG)
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
            # 1. Tagline H5
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
            # 2. Main Title H1
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

# ==============================================================================
# SECTION 2: BREADCRUMB (YOAST SEO)
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
            # Widget Yoast Breadcrumbs native
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "yoast-breadcrumbs",
                "isInner": False,
                "settings": {},
                "elements": []
            },
            # Shortcode fallback cho trường hợp chưa kích hoạt module Yoast trong Elementor
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
# SECTION 3: DANH SÁCH BÀI VIẾT THEO DANH MỤC (NỘI DUNG CHÍNH ~70%)
# ==============================================================================
def build_section_3_left_content():
    """
    Cột Trái chứa toàn bộ Section 3:
    3.1 Khối bài viết nổi bật: Widget 'posts' (Skin: cards, ảnh trái, tiêu đề, mô tả, nút)
    3.2 Thanh tiêu đề: | TIN TỨC MỚI NHẤT + Xem tất cả →
    3.3 Lưới bài viết: Widget 'posts' (Skin: classic, 3 cột x 3 hàng, gồm ảnh, tiêu đề, mô tả, nút + phân trang)
    """

    # 3.1 Khối bài viết nổi bật (Featured Post Card)
    featured_post_widget = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "posts",
        "isInner": False,
        "settings": {
            "_skin": "cards",
            "posts_post_type": "post",
            "cards_columns": "1",
            "cards_posts_per_page": "1",
            "cards_image_position": "left",
            "cards_image_size": "large",
            "cards_show_badge": "yes",
            "cards_badge_taxonomy": "category",
            "cards_badge_color": COLOR_TAG_TEXT_BLUE,
            "cards_badge_bg_color": COLOR_TAG_BG_BLUE,
            "cards_badge_radius": {"unit": "px", "size": 20},
            "cards_badge_typography_typography": "custom",
            "cards_badge_typography_font_family": "Plus Jakarta Sans",
            "cards_badge_typography_font_size": {"unit": "px", "size": 12},
            "cards_badge_typography_font_weight": "700",
            "cards_show_avatar": "none",
            "cards_show_title": "yes",
            "cards_title_tag": "h3",
            "cards_title_color": COLOR_NAVY_TITLE,
            "cards_title_typography_typography": "custom",
            "cards_title_typography_font_family": "Plus Jakarta Sans",
            "cards_title_typography_font_size": {"unit": "px", "size": 20},
            "cards_title_typography_font_size_mobile": {"unit": "px", "size": 17},
            "cards_title_typography_font_weight": "800",
            "cards_title_typography_line_height": {"unit": "em", "size": 1.3},
            "cards_show_excerpt": "yes",
            "cards_excerpt_length": 32,
            "cards_excerpt_color": COLOR_TEXT_BODY,
            "cards_excerpt_typography_typography": "custom",
            "cards_excerpt_typography_font_family": "Plus Jakarta Sans",
            "cards_excerpt_typography_font_size": {"unit": "px", "size": 13.5},
            "cards_excerpt_typography_line_height": {"unit": "em", "size": 1.6},
            "cards_meta_data": ["date"],
            "cards_meta_color": COLOR_TEXT_MUTED,
            "cards_show_read_more": "yes",
            "cards_read_more_text": "Xem chi tiết →",
            "cards_read_more_color": COLOR_TEXT_WHITE,
            "cards_read_more_typography_typography": "custom",
            "cards_read_more_typography_font_family": "Plus Jakarta Sans",
            "cards_read_more_typography_font_size": {"unit": "px", "size": 13},
            "cards_read_more_typography_font_weight": "700",
            "cards_box_bg_color": COLOR_TEXT_WHITE,
            "cards_box_border_color": COLOR_BORDER_LIGHT,
            "cards_box_border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "cards_box_border_radius": {"unit": "px", "top": "16", "right": "16", "bottom": "16", "left": "16", "isLinked": True},
            "cards_box_shadow_box_shadow_type": "yes",
            "cards_box_shadow_box_shadow": {
                "horizontal": 0,
                "vertical": 6,
                "blur": 24,
                "spread": 0,
                "color": "rgba(0, 45, 98, 0.06)"
            },
            "cards_content_padding": {"unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": True},
            "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "25", "left": "0", "isLinked": False}
        },
        "elements": []
    }

    # 3.2 Thanh tiêu đề: | TIN TỨC MỚI NHẤT + Xem tất cả →
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

    # 3.3 Lưới 9 bài viết theo danh mục & Phân trang: Widget 'posts' (Skin: classic)
    posts_grid_widget = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "posts",
        "isInner": False,
        "settings": {
            "_skin": "classic",
            "posts_post_type": "post",
            "classic_columns": "3",
            "classic_columns_tablet": "2",
            "classic_columns_mobile": "1",
            "classic_posts_per_page": "9",
            "offset": 1,
            "posts_offset": 1,
            "classic_show_image": "yes",
            "classic_image_size": "medium_large",
            "classic_show_title": "yes",
            "classic_title_tag": "h4",
            "classic_title_color": COLOR_NAVY_TITLE,
            "classic_title_typography_typography": "custom",
            "classic_title_typography_font_family": "Plus Jakarta Sans",
            "classic_title_typography_font_size": {"unit": "px", "size": 14.5},
            "classic_title_typography_font_weight": "700",
            "classic_title_typography_line_height": {"unit": "em", "size": 1.3},
            "classic_show_excerpt": "yes",
            "classic_excerpt_length": 16,
            "classic_excerpt_color": COLOR_TEXT_BODY,
            "classic_excerpt_typography_typography": "custom",
            "classic_excerpt_typography_font_family": "Plus Jakarta Sans",
            "classic_excerpt_typography_font_size": {"unit": "px", "size": 12.5},
            "classic_excerpt_typography_line_height": {"unit": "em", "size": 1.5},
            "classic_meta_data": ["date"],
            "classic_meta_color": COLOR_TEXT_MUTED,
            "classic_show_read_more": "yes",
            "classic_read_more_text": "Xem chi tiết →",
            "classic_read_more_color": COLOR_PRIMARY_BLUE,
            "classic_read_more_typography_typography": "custom",
            "classic_read_more_typography_font_family": "Plus Jakarta Sans",
            "classic_read_more_typography_font_size": {"unit": "px", "size": 12.5},
            "classic_read_more_typography_font_weight": "700",
            "classic_box_bg_color": COLOR_TEXT_WHITE,
            "classic_box_border_color": COLOR_BORDER_LIGHT,
            "classic_box_border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "classic_box_border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True},
            "classic_content_padding": {"unit": "px", "top": "12", "right": "12", "bottom": "16", "left": "12", "isLinked": False},
            # Phân trang native
            "pagination_type": "numbers_and_prev_next",
            "pagination_prev_label": "‹",
            "pagination_next_label": "›",
            "pagination_page_limit": "5",
            "pagination_align": "center",
            "pagination_spacing": {"unit": "px", "size": 10},
            "pagination_color": COLOR_TEXT_BODY,
            "pagination_active_color": COLOR_TEXT_WHITE,
            "pagination_active_bg_color": COLOR_PRIMARY_BLUE,
            "pagination_typography_typography": "custom",
            "pagination_typography_font_family": "Plus Jakarta Sans",
            "pagination_typography_font_size": {"unit": "px", "size": 13},
            "pagination_typography_font_weight": "600"
        },
        "elements": []
    }

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 68},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column"
        },
        "elements": [
            featured_post_widget,
            heading_bar,
            posts_grid_widget
        ]
    }

# ==============================================================================
# SECTION 4: SIDEBAR (THANH SEARCH, DANH MỤC TIN TỨC, BÀI VIẾT NỔI BẬT) (~30%)
# ==============================================================================
def build_section_4_sidebar():
    """
    Cột Phải chứa toàn bộ Section 4:
    4.1 Thanh search: Widget 'search-form' native
    4.2 Danh mục tin tức: Widget 'wp-widget-categories' native
    4.3 Bài viết nổi bật: Widget 'posts' native (Skin: classic, 1 cột mini)
    4.4 Banner CTA tuyển sinh
    """

    # 4.1 Thanh search
    search_card = {
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

    # 4.2 Danh mục tin tức (Widget wp-widget-categories native của WordPress)
    categories_card = {
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
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "wp-widget-categories",
                "isInner": False,
                "settings": {
                    "title": "",
                    "count": "yes",
                    "hierarchical": "no",
                    "dropdown": "no"
                },
                "elements": []
            }
        ]
    }

    # 4.3 Bài viết nổi bật (Widget 'posts' skin classic mini)
    popular_posts_card = {
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
                    "_margin": {"unit": "px", "top": "0", "right": "0", "bottom": "10", "left": "0", "isLinked": False}
                },
                "elements": []
            },
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "posts",
                "isInner": False,
                "settings": {
                    "_skin": "classic",
                    "posts_post_type": "post",
                    "classic_columns": "1",
                    "classic_posts_per_page": "4",
                    "classic_image_position": "left",
                    "classic_image_size": "thumbnail",
                    "classic_image_width": {"unit": "%", "size": 28},
                    "classic_show_title": "yes",
                    "classic_title_tag": "h5",
                    "classic_title_color": COLOR_NAVY_TITLE,
                    "classic_title_typography_typography": "custom",
                    "classic_title_typography_font_family": "Plus Jakarta Sans",
                    "classic_title_typography_font_size": {"unit": "px", "size": 12.5},
                    "classic_title_typography_font_weight": "700",
                    "classic_title_typography_line_height": {"unit": "em", "size": 1.3},
                    "classic_show_excerpt": "none",
                    "classic_show_read_more": "none",
                    "classic_meta_data": ["date"],
                    "classic_meta_color": COLOR_TEXT_MUTED
                },
                "elements": []
            }
        ]
    }

    # 4.4 Banner CTA Tuyển sinh
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

    cta_card = {
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

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 32},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "gap": {"unit": "px", "size": 22}
        },
        "elements": [
            search_card,
            categories_card,
            popular_posts_card,
            cta_card
        ]
    }

# ==============================================================================
# BODY CONTAINER 2 CỘT (CHỨA SECTION 3 VÀ SECTION 4)
# ==============================================================================
def build_body_container():
    left_sec3 = build_section_3_left_content()
    right_sec4 = build_section_4_sidebar()

    return {
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
        "elements": [left_sec3, right_sec4]
    }

# ==============================================================================
# HÀM XÂY DỰNG FILE JSON HOÀN CHỈNH
# ==============================================================================
def build_danh_muc_bai_viet_json():
    sec1 = build_section_1_banner()
    sec2 = build_section_2_breadcrumb()
    body = build_body_container()

    return {
        "version": "0.4",
        "title": "Trang Danh Mục Bài Viết - Tiếng Anh Chị Trà",
        "type": "page",
        "page_settings": [],
        "content": [sec1, sec2, body]
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
