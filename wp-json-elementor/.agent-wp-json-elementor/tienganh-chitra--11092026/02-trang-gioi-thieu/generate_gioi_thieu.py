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
    - Ảnh nền tập thể giáo viên / trung tâm
    - Background Overlay tối (opacity 0.48) để chữ trắng nổi bật
    - Cụm text căn giữa: Sub-title 'WHO WE ARE' và Title 'ABOUT US'
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
            "min_height": {"unit": "px", "size": 430},
            "padding": {
                "unit": "px",
                "top": "110",
                "right": "20",
                "bottom": "140",
                "left": "20",
                "isLinked": False
            },
            "background_background": "classic",
            "background_image": {
                "url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=1600&auto=format&fit=crop",
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
                    "title": "WHO WE ARE",
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
                    "title": "ABOUT US",
                    "header_size": "h1",
                    "align": "center",
                    "title_color": COLOR_TEXT_WHITE,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 48},
                    "typography_font_size_mobile": {"unit": "px", "size": 32},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2}
                },
                "elements": []
            }
        ]
    }

def create_counter_card(icon_class, icon_color, number_text, label_text):
    """Tạo một thẻ Card thống kê nền trắng chuẩn Elementor Flexbox Container"""
    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "flex_direction": "column",
            "align_items": "center",
            "justify_content": "center",
            "width": {"unit": "%", "size": 23.5},
            "width_tablet": {"unit": "%", "size": 48},
            "width_mobile": {"unit": "%", "size": 100},
            "background_background": "classic",
            "background_color": COLOR_TEXT_WHITE,
            "border_border": "solid",
            "border_width": {
                "unit": "px",
                "top": "1",
                "right": "1",
                "bottom": "1",
                "left": "1",
                "isLinked": True
            },
            "border_color": COLOR_BORDER_LIGHT,
            "border_radius": {
                "unit": "px",
                "top": "8",
                "right": "8",
                "bottom": "8",
                "left": "8",
                "isLinked": True
            },
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": 0,
                "vertical": 10,
                "blur": 25,
                "spread": 0,
                "color": "rgba(0, 0, 0, 0.06)"
            },
            "padding": {
                "unit": "px",
                "top": "28",
                "right": "20",
                "bottom": "24",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [
            # Icon
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "icon",
                "isInner": False,
                "settings": {
                    "selected_icon": {
                        "value": icon_class,
                        "library": "fa-solid"
                    },
                    "view": "default",
                    "align": "center",
                    "primary_color": icon_color,
                    "size": {"unit": "px", "size": 36},
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
            # Con số nổi bật
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": number_text,
                    "header_size": "h3",
                    "align": "center",
                    "title_color": COLOR_TEXT_BLACK,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 32},
                    "typography_font_weight": "800",
                    "typography_line_height": {"unit": "em", "size": 1.2},
                    "_margin": {
                        "unit": "px",
                        "top": "0",
                        "right": "0",
                        "bottom": "6",
                        "left": "0",
                        "isLinked": False
                    }
                },
                "elements": []
            },
            # Nhãn mô tả bên dưới
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": label_text,
                    "header_size": "span",
                    "align": "center",
                    "title_color": COLOR_TEXT_MUTED,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 14},
                    "typography_font_weight": "500",
                    "typography_line_height": {"unit": "em", "size": 1.4}
                },
                "elements": []
            }
        ]
    }

def build_section_2_stats():
    """
    SECTION 2: 4 KHỐI THỐNG KÊ (Overlapping Cards Container)
    - Boxed 1200px
    - margin-top: -65px để đè lên ranh giới chân Banner
    - Z-index: 10
    """
    card1 = create_counter_card("fas fa-graduation-cap", COLOR_PRIMARY_BLUE, "22 +", "Giáo viên bộ môn")
    card2 = create_counter_card("fas fa-book-open", COLOR_PRIMARY_RED, "17 +", "Lớp học")
    card3 = create_counter_card("fas fa-award", COLOR_BTN_ORANGE, "18 +", "Năm hoạt động")
    card4 = create_counter_card("fas fa-users", COLOR_PRIMARY_GREEN, "21,875 +", "Học sinh đã tốt nghiệp")

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 1200},
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "justify_content": "space-between",
            "gap": {"unit": "px", "size": 20, "column": "20", "row": "20", "isLinked": True},
            "margin": {
                "unit": "px",
                "top": "-65",
                "right": "auto",
                "bottom": "0",
                "left": "auto",
                "isLinked": False
            },
            "z_index": 10,
            "position": "relative",
            "padding": {
                "unit": "px",
                "top": "0",
                "right": "20",
                "bottom": "0",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [card1, card2, card3, card4]
    }

def build_section_3_content():
    """
    SECTION 3: NỘI DUNG GIỚI THIỆU CHI TIẾT (Editorial Story Section)
    - Boxed 960px (Khổ đọc bài viết chuẩn UI/UX)
    - Tiêu đề chính H2 line-height 1.2
    - Text Editor 4 đoạn văn bản chuẩn văn phong giáo dục
    """
    html_content = (
        "<p>Khi giáo dục ngày càng phát triển, việc chọn cho con em mình môi trường học tập tốt luôn là điều trăn trở của các bậc phụ huynh. "
        "Ở trường, môn Tiếng Anh khiến nhiều học sinh gặp không ít khó khăn, bởi đa số các em chưa nắm vững kiến thức căn bản từ lớp trước, "
        "đặc biệt chưa có phương pháp tiếp cận tự nhiên và môi trường rèn luyện phản xạ giao tiếp phù hợp.</p>"
        
        "<p>Được thành lập với sứ mệnh đồng hành và thắp sáng tình yêu ngôn ngữ, <strong>Tiếng Anh Chị Trà</strong> quy tụ tập thể giảng viên "
        "giàu kinh nghiệm, chuyên môn sư phạm vững vàng cùng chương trình đào tạo chuẩn quốc tế. Chúng tôi giúp học sinh củng cố các kiến thức cơ bản "
        "và dần dần tiếp cận với các kiến thức nâng cao, rèn khả năng tư duy ngôn ngữ độc lập, tự tin làm chủ 4 kỹ năng Nghe - Nói - Đọc - Viết "
        "để đạt kết quả cao trong các kỳ thi ở trường cũng như các kỳ thi chứng chỉ Cambridge, IELTS.</p>"
        
        "<p>Nhằm đảm bảo chất lượng dạy và học tốt nhất, trung tâm duy trì <strong>sĩ số vàng không quá 15 – 20 học sinh</strong> cùng một giảng viên chính "
        "và một trợ giảng theo sát từng em. Phối hợp chặt chẽ với gia đình, chúng tôi luôn chủ động liên hệ, thông tin đến phụ huynh về tiến độ học tập, "
        "tổ chức các bài kiểm tra định kỳ để đánh giá năng lực thực tế và báo cáo kết quả chi tiết bằng <em>Phiếu báo học tập</em>. Phụ huynh hoàn toàn "
        "an tâm và thấy được sự tiến bộ rõ rệt của con qua từng khóa học.</p>"
        
        "<p><strong>Vậy Tiếng Anh Chị Trà có điểm gì đặc biệt?</strong> Không chỉ là nơi truyền đạt kiến thức, trung tâm tạo dựng môi trường "
        "học tập tương tác, thân thiện, tràn đầy cảm hứng với cơ sở vật chất hiện đại, giúp các em xóa bỏ rào cản sợ hãi tiếng Anh, tự tin mở rộng "
        "thế giới và sẵn sàng bước ra toàn cầu.</p>"
    )

    return {
        "id": gen_id(),
        "elType": "container",
        "isInner": False,
        "settings": {
            "content_width": "boxed",
            "width": {"unit": "px", "size": 960},
            "flex_direction": "column",
            "align_items": "flex-start",
            "padding": {
                "unit": "px",
                "top": "70",
                "right": "20",
                "bottom": "80",
                "left": "20",
                "isLinked": False
            }
        },
        "elements": [
            # 1. Heading H2
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "heading",
                "isInner": False,
                "settings": {
                    "title": "GIỚI THIỆU TIẾNG ANH CHỊ TRÀ",
                    "header_size": "h2",
                    "align": "left",
                    "title_color": COLOR_TEXT_BLACK,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 26},
                    "typography_font_weight": "800",
                    "typography_text_transform": "uppercase",
                    "typography_line_height": {"unit": "em", "size": 1.2},
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
            # 2. Text Editor
            {
                "id": gen_id(),
                "elType": "widget",
                "widgetType": "text-editor",
                "isInner": False,
                "settings": {
                    "editor": html_content,
                    "align": "left",
                    "text_color": COLOR_TEXT_BODY,
                    "typography_typography": "custom",
                    "typography_font_family": "Plus Jakarta Sans",
                    "typography_font_size": {"unit": "px", "size": 16},
                    "typography_line_height": {"unit": "em", "size": 1.75}
                },
                "elements": []
            }
        ]
    }

def build_about_page_json():
    """Xây dựng gói Page Template hoàn chỉnh cho Trang Giới Thiệu"""
    sec1 = build_section_1_banner()
    sec2 = build_section_2_stats()
    sec3 = build_section_3_content()

    return {
        "version": "0.4",
        "title": "Trang Giới Thiệu - Tiếng Anh Chị Trà",
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
    page_data = build_about_page_json()
    save_and_zip(page_data, "trang-gioi-thieu-elementor", out_dir)
    print("\n[COMPLETED] Successfully generated Trang Gioi Thieu Elementor JSON & ZIP!")
