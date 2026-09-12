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
COLOR_BTN_ORANGE    = "#ED9717"  # Màu cam điểm nhấn nút
COLOR_BORDER_LIGHT  = "#E5E7EB"  # Màu viền phẳng tinh tế

def build_section_1_banner():
    """
    SECTION 1: HERO BANNER (Full-width Container)
    - Ảnh nền hoạt động / sự kiện trung tâm
    - Background Overlay đen mờ (opacity 0.48)
    - Cụm tiêu đề kép căn giữa: 'NEWS & EVENTS' và 'TIN TỨC & SỰ KIỆN'
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
                "url": "https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=1600&auto=format&fit=crop",
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
                    "title": "NEWS & EVENTS",
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
                    "title": "TIN TỨC & SỰ KIỆN",
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

def build_section_2_featured_post():
    """
    SECTION 2: KHỐI BÀI VIẾT NỔI BẬT LẤY ĐỘNG 100% (Dynamic Featured Post)
    - Boxed 1200px
    - Widget 'posts' (Skin: cards):
      * Lấy động 1 bài mới nhất (posts_per_page: 1)
      * Ảnh nằm bên trái, nội dung bên phải (image_position: left)
      * Tự động kéo Featured Image, Title, Date, Author, Excerpt và Link the_permalink()
      * Tự động lấy Badge danh mục (Category)
    """
    featured_settings = {
        "_skin": "cards",
        "posts_post_type": "post",
        "cards_columns": "1",
        "cards_posts_per_page": "1",
        "cards_image_position": "left",
        "cards_image_size": "large",
        "cards_show_badge": "yes",
        "cards_badge_taxonomy": "category",
        "cards_badge_color": COLOR_TEXT_WHITE,
        "cards_badge_bg_color": COLOR_PRIMARY_RED,
        "cards_badge_radius": {"unit": "px", "size": 4},
        "cards_badge_typography_typography": "custom",
        "cards_badge_typography_font_family": "Plus Jakarta Sans",
        "cards_badge_typography_font_size": {"unit": "px", "size": 12},
        "cards_badge_typography_font_weight": "700",
        "cards_badge_typography_text_transform": "uppercase",
        "cards_show_avatar": "none",
        "cards_show_title": "yes",
        "cards_title_tag": "h3",
        "cards_title_color": COLOR_TEXT_BLACK,
        "cards_title_typography_typography": "custom",
        "cards_title_typography_font_family": "Plus Jakarta Sans",
        "cards_title_typography_font_size": {"unit": "px", "size": 24},
        "cards_title_typography_font_weight": "800",
        "cards_title_typography_line_height": {"unit": "em", "size": 1.2},
        "cards_show_excerpt": "yes",
        "cards_excerpt_length": 32,
        "cards_excerpt_color": COLOR_TEXT_BODY,
        "cards_excerpt_typography_typography": "custom",
        "cards_excerpt_typography_font_family": "Plus Jakarta Sans",
        "cards_excerpt_typography_font_size": {"unit": "px", "size": 15},
        "cards_excerpt_typography_line_height": {"unit": "em", "size": 1.6},
        "cards_meta_data": ["author", "date"],
        "cards_meta_color": COLOR_TEXT_MUTED,
        "cards_meta_separator": "•",
        "cards_show_read_more": "yes",
        "cards_read_more_text": "Đọc tiếp »",
        "cards_read_more_color": COLOR_BTN_ORANGE,
        "cards_read_more_typography_typography": "custom",
        "cards_read_more_typography_font_family": "Plus Jakarta Sans",
        "cards_read_more_typography_font_size": {"unit": "px", "size": 14},
        "cards_read_more_typography_font_weight": "700",
        "cards_box_bg_color": COLOR_TEXT_WHITE,
        "cards_box_border_color": COLOR_BORDER_LIGHT,
        "cards_box_border_width": {
            "unit": "px",
            "top": "1",
            "right": "1",
            "bottom": "1",
            "left": "1",
            "isLinked": True
        },
        "cards_box_border_radius": {
            "unit": "px",
            "top": "12",
            "right": "12",
            "bottom": "12",
            "left": "12",
            "isLinked": True
        },
        "cards_box_shadow_box_shadow_type": "yes",
        "cards_box_shadow_box_shadow": {
            "horizontal": 0,
            "vertical": 6,
            "blur": 20,
            "spread": 0,
            "color": "rgba(0, 0, 0, 0.05)"
        },
        "cards_content_padding": {
            "unit": "px",
            "top": "24",
            "right": "28",
            "bottom": "24",
            "left": "28",
            "isLinked": False
        }
    }

    featured_widget = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "posts",
        "isInner": False,
        "settings": featured_settings,
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
            "padding": {
                "unit": "px",
                "top": "50",
                "right": "20",
                "bottom": "20",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [featured_widget]
    }

def build_section_3_posts_grid():
    """
    SECTION 3: DANH SÁCH BÀI VIẾT (Posts Grid) & PHÂN TRANG
    - Boxed 1200px
    - Widget 'posts' 3 cột Desktop / 2 cột Tablet / 1 cột Mobile
    - 6 bài/trang (2 hàng x 3 cột)
    - offset: 1 (Bỏ qua bài viết đầu tiên đã hiển thị ở Section 2 để KHÔNG BỊ TRÙNG LẶP)
    - Phân trang đầy đủ số trang và Prev/Next: '< 1 2 3 ... >'
    """
    posts_settings = {
        "_skin": "classic",
        "posts_post_type": "post",
        "classic_columns": "3",
        "classic_columns_tablet": "2",
        "classic_columns_mobile": "1",
        "classic_posts_per_page": "6",
        "offset": 1,
        "posts_offset": 1,
        "classic_show_image": "yes",
        "classic_image_size": "medium_large",
        "classic_show_title": "yes",
        "classic_title_tag": "h3",
        "classic_title_color": COLOR_TEXT_BLACK,
        "classic_title_typography_typography": "custom",
        "classic_title_typography_font_family": "Plus Jakarta Sans",
        "classic_title_typography_font_size": {"unit": "px", "size": 18},
        "classic_title_typography_font_weight": "700",
        "classic_title_typography_line_height": {"unit": "em", "size": 1.2},
        "classic_show_excerpt": "yes",
        "classic_excerpt_color": COLOR_TEXT_BODY,
        "classic_excerpt_length": 16,
        "classic_excerpt_typography_typography": "custom",
        "classic_excerpt_typography_font_family": "Plus Jakarta Sans",
        "classic_excerpt_typography_font_size": {"unit": "px", "size": 14},
        "classic_excerpt_typography_line_height": {"unit": "em", "size": 1.5},
        "classic_meta_data": ["author", "date"],
        "classic_meta_color": COLOR_TEXT_MUTED,
        "classic_meta_separator": "•",
        "classic_show_read_more": "yes",
        "classic_read_more_text": "Xem chi tiết →",
        "classic_read_more_color": COLOR_BTN_ORANGE,
        "classic_read_more_typography_typography": "custom",
        "classic_read_more_typography_font_family": "Plus Jakarta Sans",
        "classic_read_more_typography_font_size": {"unit": "px", "size": 13},
        "classic_read_more_typography_font_weight": "700",
        "classic_box_bg_color": COLOR_TEXT_WHITE,
        "classic_box_border_color": COLOR_BORDER_LIGHT,
        "classic_box_border_width": {
            "unit": "px",
            "top": "1",
            "right": "1",
            "bottom": "1",
            "left": "1",
            "isLinked": True
        },
        "classic_box_border_radius": {
            "unit": "px",
            "top": "10",
            "right": "10",
            "bottom": "10",
            "left": "10",
            "isLinked": True
        },
        "classic_content_padding": {
            "unit": "px",
            "top": "18",
            "right": "18",
            "bottom": "20",
            "left": "18",
            "isLinked": False
        },
        # Phân trang
        "pagination_type": "numbers_and_prev_next",
        "pagination_prev_label": "‹",
        "pagination_next_label": "›",
        "pagination_page_limit": "5",
        "pagination_align": "left",
        "pagination_spacing": {"unit": "px", "size": 12},
        "pagination_color": COLOR_TEXT_BODY,
        "pagination_typography_typography": "custom",
        "pagination_typography_font_family": "Plus Jakarta Sans",
        "pagination_typography_font_size": {"unit": "px", "size": 14},
        "pagination_typography_font_weight": "600"
    }

    posts_widget = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "posts",
        "isInner": False,
        "settings": posts_settings,
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
            "padding": {
                "unit": "px",
                "top": "10",
                "right": "20",
                "bottom": "80",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [posts_widget]
    }

def build_tin_tuc_page_json():
    """Xây dựng gói Page Template hoàn chỉnh cho Trang Tin Tức & Sự Kiện"""
    sec1 = build_section_1_banner()
    sec2 = build_section_2_featured_post()
    sec3 = build_section_3_posts_grid()

    return {
        "version": "0.4",
        "title": "Trang Tin Tức - Tiếng Anh Chị Trà",
        "type": "page",
        "page_settings": [],
        "content": [sec1, sec2, sec3]
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
    page_data = build_tin_tuc_page_json()
    save_and_zip(page_data, "trang-tin-tuc-elementor", out_dir)
    print("\n[COMPLETED] Successfully generated Trang Tin Tuc Elementor JSON & ZIP!")
