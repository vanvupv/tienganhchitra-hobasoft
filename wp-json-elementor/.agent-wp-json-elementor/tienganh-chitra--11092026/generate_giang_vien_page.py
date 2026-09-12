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
COLOR_PRIMARY_GREEN = "#28A745"  # Xanh lá nhận diện giảng viên
COLOR_PRIMARY_RED   = "#C8102E"  # Đỏ thương hiệu SLA / Chị Trà
COLOR_TEXT_BLACK    = "#111827"  # Màu tiêu đề sẫm
COLOR_TEXT_BODY     = "#4B5563"  # Màu nội dung văn bản
COLOR_TEXT_MUTED    = "#6B7280"  # Màu nhãn xám
COLOR_TEXT_WHITE    = "#FFFFFF"  # Màu trắng
COLOR_BTN_ORANGE    = "#ED9717"  # Màu cam điểm nhấn nút
COLOR_BORDER_LIGHT  = "#F0F0F0"  # Màu viền phẳng tinh tế

def build_section_1_banner():
    """
    SECTION 1: HERO BANNER (Full-width Container)
    - Ảnh nền đội ngũ giảng viên / phòng học
    - Background Overlay đen mờ (opacity 0.48)
    - Cụm tiêu đề kép căn giữa: 'OUR TEACHERS' và 'ĐỘI NGŨ GIẢNG VIÊN TÂM HUYẾT'
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
                    "title": "OUR TEACHERS",
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
                    "title": "ĐỘI NGŨ GIẢNG VIÊN TÂM HUYẾT",
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
    SECTION 2: TIÊU ĐỀ & ĐOẠN MÔ TẢ NGẮN (Intro Section)
    - Boxed 960px căn giữa
    - Tiêu đề H2 line-height 1.2
    - Đoạn văn bản giới thiệu về trình độ, sứ mệnh và phương pháp truyền cảm hứng
    """
    desc_text = (
        "Tại Tiếng Anh Chị Trà, mỗi thầy cô không chỉ là người truyền thụ tri thức mà còn là người bạn đồng hành "
        "tin cậy, thấu hiểu tâm lý lứa tuổi và khơi gợi niềm đam mê tiếng Anh tự nhiên trong mỗi học sinh. "
        "Đội ngũ giáo viên 100% đạt chuẩn sư phạm quốc tế (IELTS 8.0+, TESOL, CELTA) với phương pháp giảng dạy "
        "tương tác sinh động, luôn theo sát tiến độ từng em để phát huy tối đa tiềm năng ngôn ngữ."
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
                "bottom": "25",
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
                    "title": "CHUYÊN MÔN & TẬN TÂM",
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
                    "title": "NGƯỜI THẦY TRUYỀN CẢM HỨNG VÀ ĐỒNG HÀNH CÙNG CON",
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

def build_section_3_posts():
    """
    SECTION 3: POSTS DANH SÁCH GIẢNG VIÊN (Teachers Grid)
    - Boxed 1200px
    - Widget posts kết nối CPT 'giang_vien'
    - Lưới 4 cột Desktop / 2 cột Tablet / 1 cột Mobile
    - Thẻ card viền xanh lá #28A745, bo góc 10px, có phân trang số trang
    """
    posts_settings = {
        "_skin": "classic",
        "posts_post_type": "giang_vien",
        "classic_columns": "4",
        "classic_columns_tablet": "2",
        "classic_columns_mobile": "1",
        "classic_posts_per_page": "8",
        "classic_show_image": "yes",
        "classic_image_size": "medium_large",
        "classic_show_title": "yes",
        "classic_title_color": COLOR_TEXT_BLACK,
        "classic_title_tag": "h3",
        "classic_show_excerpt": "yes",
        "classic_excerpt_color": COLOR_TEXT_BODY,
        "classic_excerpt_length": 18,
        "classic_show_read_more": "yes",
        "classic_read_more_text": "Xem hồ sơ →",
        "classic_read_more_color": COLOR_BTN_ORANGE,
        "classic_box_bg_color": COLOR_TEXT_WHITE,
        "classic_box_border_color": COLOR_PRIMARY_GREEN,
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
            "top": "16",
            "right": "16",
            "bottom": "18",
            "left": "16",
            "isLinked": False
        },
        "pagination_type": "numbers",
        "pagination_page_limit": "5",
        "pagination_numbers_spacing": {"unit": "px", "size": 10}
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
                "top": "20",
                "right": "20",
                "bottom": "80",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [posts_widget]
    }

def build_giang_vien_page_json():
    """Xây dựng gói Page Template hoàn chỉnh cho Trang Giảng Viên"""
    sec1 = build_section_1_banner()
    sec2 = build_section_2_intro()
    sec3 = build_section_3_posts()

    return {
        "version": "0.4",
        "title": "Trang Giảng Viên - Tiếng Anh Chị Trà",
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
    page_data = build_giang_vien_page_json()
    save_and_zip(page_data, "trang-giang-vien-elementor", out_dir)
    print("\n[COMPLETED] Successfully generated Trang Giang Vien Elementor JSON & ZIP!")
