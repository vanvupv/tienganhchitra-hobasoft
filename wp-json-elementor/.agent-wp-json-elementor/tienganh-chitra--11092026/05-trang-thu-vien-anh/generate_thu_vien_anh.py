import json
import zipfile
import os
import uuid

def gen_id():
    return uuid.uuid4().hex[:8]

# ==============================================================================
# BẢNG MÃ MÀU CHUẨN DỰ ÁN TIẾNG ANH CHỊ TRÀ
# ==============================================================================
COLOR_PRIMARY_BLUE  = "#007BFF"  # Xanh dương nhận diện (Tab active, Button, Heading)
COLOR_PRIMARY_GREEN = "#28A745"  # Xanh lá nhận diện
COLOR_PRIMARY_RED   = "#C8102E"  # Đỏ thương hiệu SLA / Chị Trà
COLOR_TEXT_BLACK    = "#111827"  # Màu tiêu đề sẫm
COLOR_TEXT_BODY     = "#4B5563"  # Màu nội dung văn bản
COLOR_TEXT_MUTED    = "#6B7280"  # Màu nhãn xám
COLOR_TEXT_WHITE    = "#FFFFFF"  # Màu trắng
COLOR_BTN_ORANGE    = "#ED9717"  # Màu cam điểm nhấn
COLOR_BORDER_LIGHT  = "#E5E7EB"  # Màu viền phẳng tinh tế

def build_section_1_banner():
    """
    SECTION 1: HERO BANNER (Full-width Container)
    - Ảnh nền hoạt động học tập sôi nổi
    - Background Overlay đen mờ (opacity 0.48)
    - Cụm tiêu đề kép căn giữa: 'PHOTO GALLERY' và 'THƯ VIỆN HÌNH ẢNH'
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
                "url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=1600&auto=format&fit=crop",
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
                    "title": "PHOTO GALLERY",
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
                    "title": "THƯ VIỆN HÌNH ẢNH",
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

def build_section_2_gallery():
    """
    SECTION 2: KHỐI THƯ VIỆN ẢNH CÓ TAB LỌC (Filterable Gallery Section)
    - Boxed 1200px
    - Tiêu đề H2: 'THƯ VIỆN ẢNH' màu xanh dương #007BFF
    - Widget 'gallery' dạng Multiple:
      * 4 nhóm: Lớp học, Hoạt động ngoại khóa, Lễ tốt nghiệp, Giao lưu quốc tế
      * Filter Bar dạng nút tròn Pill (TẤT CẢ active xanh dương)
      * Bố cục Masonry 4 cột Desktop / 2 cột Tablet / 1 cột Mobile
      * Dải dải mờ tối ở chân ảnh với tiêu đề ảnh màu trắng
      * Bo góc ảnh 16px, Lightbox native mở to
    - Nút 'XEM THÊM' ở đáy
    """
    galleries_data = [
        {
            "_id": gen_id(),
            "gallery_title": "LỚP HỌC",
            "multiple_gallery": [
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1577896851231-70ef18881754?q=80&w=800&auto=format&fit=crop",
                    "title": "Lớp học giao tiếp vui vẻ"
                },
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=800&auto=format&fit=crop",
                    "title": "Học viên thuyết trình tiếng Anh"
                },
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=800&auto=format&fit=crop",
                    "title": "Không gian lớp học tương tác"
                }
            ]
        },
        {
            "_id": gen_id(),
            "gallery_title": "HOẠT ĐỘNG NGOẠI KHÓA",
            "multiple_gallery": [
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=800&auto=format&fit=crop",
                    "title": "Dã ngoại học thuật thực tế"
                },
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?q=80&w=800&auto=format&fit=crop",
                    "title": "English Speaking Club sôi nổi"
                },
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=800&auto=format&fit=crop",
                    "title": "Hoạt động gắn kết học viên"
                }
            ]
        },
        {
            "_id": gen_id(),
            "gallery_title": "LỄ TỐT NGHIỆP",
            "multiple_gallery": [
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=800&auto=format&fit=crop",
                    "title": "Lễ Tốt Nghiệp Khóa K45"
                },
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?q=80&w=800&auto=format&fit=crop",
                    "title": "Vinh danh học viên xuất sắc"
                },
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1531545514256-b1400bc00f31?q=80&w=800&auto=format&fit=crop",
                    "title": "Khoảnh khắc nhận chứng chỉ quốc tế"
                }
            ]
        },
        {
            "_id": gen_id(),
            "gallery_title": "GIAO LƯU QUỐC TẾ",
            "multiple_gallery": [
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=800&auto=format&fit=crop",
                    "title": "Native English & Mentors"
                },
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=800&auto=format&fit=crop",
                    "title": "Ethnic Food & Culture Exchange"
                },
                {
                    "id": "",
                    "url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=800&auto=format&fit=crop",
                    "title": "Góc đọc sách thư viện quốc tế"
                }
            ]
        }
    ]

    gallery_widget = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "gallery",
        "isInner": False,
        "settings": {
            "gallery_type": "multiple",
            "galleries": galleries_data,
            "gallery_columns": "4",
            "gallery_columns_tablet": "2",
            "gallery_columns_mobile": "1",
            "gallery_layout": "masonry",
            "gap": {"unit": "px", "size": 20},
            # Filter bar
            "filter_bar": "yes",
            "filter_bar_all_title": "TẤT CẢ",
            "filter_bar_align": "center",
            "filter_bar_color": "#374151",
            "filter_bar_color_active": COLOR_TEXT_WHITE,
            "filter_bar_bg_color_active": COLOR_PRIMARY_BLUE,
            "filter_bar_border_radius": {
                "unit": "px",
                "top": "99",
                "right": "99",
                "bottom": "99",
                "left": "99",
                "isLinked": True
            },
            "filter_bar_padding": {
                "unit": "px",
                "top": "8",
                "right": "20",
                "bottom": "8",
                "left": "20",
                "isLinked": False
            },
            "filter_bar_gap": {"unit": "px", "size": 12},
            # Overlay & Title
            "overlay_background": "gradient",
            "overlay_color": "rgba(0, 0, 0, 0)",
            "overlay_color_b": "rgba(0, 0, 0, 0.75)",
            "overlay_gradient_type": "linear",
            "overlay_gradient_angle": {"unit": "deg", "size": 180},
            "overlay_title": "title",
            "overlay_title_color": COLOR_TEXT_WHITE,
            "overlay_title_typography_typography": "custom",
            "overlay_title_typography_font_family": "Plus Jakarta Sans",
            "overlay_title_typography_font_size": {"unit": "px", "size": 14},
            "overlay_title_typography_font_weight": "700",
            "overlay_animation": "fade-in",
            # Image Styling
            "image_border_radius": {
                "unit": "px",
                "top": "16",
                "right": "16",
                "bottom": "16",
                "left": "16",
                "isLinked": True
            },
            "image_box_shadow_box_shadow_type": "yes",
            "image_box_shadow_box_shadow": {
                "horizontal": 0,
                "vertical": 6,
                "blur": 20,
                "spread": 0,
                "color": "rgba(0, 0, 0, 0.08)"
            },
            "open_lightbox": "yes"
        },
        "elements": []
    }

    # Nút Xem Thêm ở chân trang
    load_more_btn = {
        "id": gen_id(),
        "elType": "widget",
        "widgetType": "button",
        "isInner": False,
        "settings": {
            "text": "XEM THÊM",
            "align": "center",
            "button_text_color": COLOR_TEXT_WHITE,
            "background_color": COLOR_PRIMARY_BLUE,
            "border_radius": {
                "unit": "px",
                "top": "99",
                "right": "99",
                "bottom": "99",
                "left": "99",
                "isLinked": True
            },
            "padding": {
                "unit": "px",
                "top": "12",
                "right": "36",
                "bottom": "12",
                "left": "36",
                "isLinked": False
            },
            "typography_typography": "custom",
            "typography_font_family": "Plus Jakarta Sans",
            "typography_font_size": {"unit": "px", "size": 15},
            "typography_font_weight": "700",
            "_margin": {
                "unit": "px",
                "top": "36",
                "right": "0",
                "bottom": "0",
                "left": "0",
                "isLinked": False
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
            "padding": {
                "unit": "px",
                "top": "60",
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
                    "title": "THƯ VIỆN ẢNH",
                    "header_size": "h2",
                    "align": "center",
                    "title_color": COLOR_PRIMARY_BLUE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 32},
                    "typography_font_weight": "800",
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
            # Widget Gallery Filterable
            gallery_widget,
            # Nút Xem Thêm
            load_more_btn
        ]
    }

def build_thu_vien_anh_page_json():
    """Xây dựng gói Page Template hoàn chỉnh cho Trang Thư Viện Ảnh"""
    sec1 = build_section_1_banner()
    sec2 = build_section_2_gallery()

    return {
        "version": "0.4",
        "title": "Trang Thư Viện Ảnh - Tiếng Anh Chị Trà",
        "type": "page",
        "page_settings": [],
        "content": [sec1, sec2]
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
    page_data = build_thu_vien_anh_page_json()
    save_and_zip(page_data, "trang-thu-vien-anh-elementor", out_dir)
    print("\n[COMPLETED] Successfully generated Trang Thu Vien Anh Elementor JSON & ZIP!")
