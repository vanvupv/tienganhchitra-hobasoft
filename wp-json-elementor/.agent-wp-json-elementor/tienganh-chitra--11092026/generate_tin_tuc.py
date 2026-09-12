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
    SECTION 2: KHỐI BÀI VIẾT NỔI BẬT (Featured Post)
    - Boxed 1200px
    - Thẻ ngang: Cột trái ảnh lớn (45%), Cột phải nội dung thông báo nổi bật (55%)
    """
    featured_img_col = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 45},
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
                        "url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=1000&auto=format&fit=crop",
                        "id": ""
                    },
                    "image_size": "large",
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
        ]
    }

    featured_content_col = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "width": {"unit": "%", "size": 52},
            "width_mobile": {"unit": "%", "size": 100},
            "flex_direction": "column",
            "align_items": "flex-start",
            "justify_content": "center"
        },
        "elements": [
            # Tag Thông báo
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "THÔNG BÁO MỚI NHẤT",
                    "header_size": "span",
                    "align": "left",
                    "title_color": COLOR_PRIMARY_RED,
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
            # Tiêu đề H3
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "THÔNG BÁO V/V LỊCH NGHỈ LỄ & KẾ HOẠCH HỌC TẬP MỚI NHẤT NĂM HỌC 2026",
                    "header_size": "h3",
                    "align": "left",
                    "title_color": COLOR_TEXT_BLACK,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 22},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.3},
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
            # Meta ngày / tác giả
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "👤 Ban Giám Hiệu  •  🕒 09/07/2026 10:26",
                    "header_size": "span",
                    "align": "left",
                    "title_color": COLOR_TEXT_MUTED,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 13},
                    "typography_font_weight": "500",
                    "typography_line_height": {"unit": "em", "size": 1.4},
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
            # Tóm tắt
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": (
                        "<p>Trung tâm Tiếng Anh Chị Trà xin trân trọng thông báo đến Quý phụ huynh và toàn thể học sinh "
                        "lịch nghỉ lễ chính thức cùng kế hoạch học bù chi tiết nhằm đảm bảo tối đa tiến độ và chất lượng đào tạo các khóa học...</p>"
                    ),
                    "align": "left",
                    "text_color": COLOR_TEXT_BODY,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 15},
                    "typography_line_height": {"unit": "em", "size": 1.6}
                },
                "elements": []
            },
            # Nút Đọc tiếp
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "button",
                "isInner": False,
                "settings": {
                    "text": "Đọc tiếp »",
                    "align": "left",
                    "button_text_color": COLOR_BTN_ORANGE,
                    "background_color": "rgba(0,0,0,0)",
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 14},
                    "typography_font_weight": "700",
                    "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
                },
                "elements": []
            }
        ]
    }

    featured_card = {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "justify_content": "space-between",
            "align_items": "center",
            "background_background": "classic",
            "background_color": COLOR_TEXT_WHITE,
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {"unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": True},
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": 0,
                "vertical": 6,
                "blur": 20,
                "spread": 0,
                "color": "rgba(0, 0, 0, 0.05)"
            },
            "padding": {"unit": "px", "top": "24", "right": "24", "bottom": "24", "left": "24", "isLinked": True}
        },
        "elements": [featured_img_col, featured_content_col]
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
        "elements": [featured_card]
    }

def build_section_3_posts_grid():
    """
    SECTION 3: DANH SÁCH BÀI VIẾT (Posts Grid) & PHÂN TRANG
    - Boxed 1200px
    - Widget 'posts' 3 cột Desktop / 2 cột Tablet / 1 cột Mobile
    - 6 bài/trang (2 hàng x 3 cột)
    - Phân trang đầy đủ số trang và Prev/Next: '< 1 2 3 ... >'
    """
    posts_settings = {
        "_skin": "classic",
        "posts_post_type": "post",
        "classic_columns": "3",
        "classic_columns_tablet": "2",
        "classic_columns_mobile": "1",
        "classic_posts_per_page": "6",
        "classic_show_image": "yes",
        "classic_image_size": "medium_large",
        "classic_show_title": "yes",
        "classic_title_color": COLOR_TEXT_BLACK,
        "classic_title_tag": "h3",
        "classic_show_excerpt": "yes",
        "classic_excerpt_color": COLOR_TEXT_BODY,
        "classic_excerpt_length": 15,
        "classic_meta_data": ["author", "date"],
        "classic_show_read_more": "yes",
        "classic_read_more_text": "Xem chi tiết →",
        "classic_read_more_color": COLOR_BTN_ORANGE,
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
        "pagination_spacing": {"unit": "px", "size": 12}
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
