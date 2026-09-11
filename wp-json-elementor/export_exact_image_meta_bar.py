import json
import zipfile
import os

def export_perfect_aligned_meta_bar():
    """
    FIX HOÀN TOÀN LỖI LỆCH TRỤC DỌC (BUG-06):
    Tách Icon và Text thành 2 phần tử riêng biệt trong Sub-container Flexbox
    với align_items: center và line_height: 1.
    Đảm bảo 100% Icon mắt 👁️ và số 8 nằm THẲNG HÀNG CHÍNH GIỮA TUYỆT ĐỐI!
    """
    aligned_meta_bar = [
        {
            "id": "sec_meta_bar_perfect_align",
            "elType": "container",
            "isInner": False,
            "settings": {
                "content_width": "full",
                "flex_direction": "row",
                "justify_content": "space-between",
                "align_items": "center",
                "padding": {"unit": "px", "top": "10", "right": "0", "bottom": "10", "left": "0", "isLinked": False},
                "border_border": "solid",
                "border_width": {"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
                "border_color": "#EEF2F6"
            },
            "elements": [
                {
                    "id": "container_left_group",
                    "elType": "container",
                    "isInner": True,
                    "settings": {
                        "content_width": "full",
                        "flex_direction": "row",
                        "align_items": "center",
                        "gap": {"unit": "px", "size": "20"}
                    },
                    "elements": [
                        # Item 1: Lượt xem (Icon + Số 8) trong 1 Flexbox Row siêu phẳng
                        {
                            "id": "item_view_flex_row",
                            "elType": "container",
                            "isInner": True,
                            "settings": {
                                "content_width": "full",
                                "flex_direction": "row",
                                "align_items": "center",
                                "gap": {"unit": "px", "size": "6"}
                            },
                            "elements": [
                                {
                                    "id": "icon_eye_widget",
                                    "elType": "widget",
                                    "isInner": False,
                                    "widgetType": "icon",
                                    "settings": {
                                        "selected_icon": {"value": "far fa-eye", "library": "fa-regular"},
                                        "primary_color": "#64748B",
                                        "size": {"unit": "px", "size": "16"}
                                    }
                                },
                                {
                                    "id": "text_view_count_widget",
                                    "elType": "widget",
                                    "isInner": False,
                                    "widgetType": "heading",
                                    "settings": {
                                        "title": "8",
                                        "header_size": "span",
                                        "title_color": "#475569",
                                        "typography_font_size": {"unit": "px", "size": "13"},
                                        "typography_font_weight": "500",
                                        "typography_line_height": {"unit": "em", "size": "1"}
                                    }
                                }
                            ]
                        },
                        # Item 2: Bình luận (Icon + Số 0) trong 1 Flexbox Row siêu phẳng
                        {
                            "id": "item_comment_flex_row",
                            "elType": "container",
                            "isInner": True,
                            "settings": {
                                "content_width": "full",
                                "flex_direction": "row",
                                "align_items": "center",
                                "gap": {"unit": "px", "size": "6"}
                            },
                            "elements": [
                                {
                                    "id": "icon_comment_widget",
                                    "elType": "widget",
                                    "isInner": False,
                                    "widgetType": "icon",
                                    "settings": {
                                        "selected_icon": {"value": "far fa-comment", "library": "fa-regular"},
                                        "primary_color": "#64748B",
                                        "size": {"unit": "px", "size": "16"}
                                    }
                                },
                                {
                                    "id": "text_comment_count_widget",
                                    "elType": "widget",
                                    "isInner": False,
                                    "widgetType": "heading",
                                    "settings": {
                                        "title": "0",
                                        "header_size": "span",
                                        "title_color": "#475569",
                                        "typography_font_size": {"unit": "px", "size": "13"},
                                        "typography_font_weight": "500",
                                        "typography_line_height": {"unit": "em", "size": "1"}
                                    }
                                }
                            ]
                        }
                    ]
                },
                {
                    "id": "container_right_heart_group",
                    "elType": "container",
                    "isInner": True,
                    "settings": {
                        "content_width": "full",
                        "flex_direction": "row",
                        "justify_content": "flex-end",
                        "align_items": "center"
                    },
                    "elements": [
                        {
                            "id": "icon_heart_widget",
                            "elType": "widget",
                            "isInner": False,
                            "widgetType": "icon",
                            "settings": {
                                "selected_icon": {"value": "far fa-heart", "library": "fa-regular"},
                                "primary_color": "#FB7185",
                                "size": {"unit": "px", "size": "18"},
                                "hover_primary_color": "#E11D48"
                            }
                        }
                    ]
                }
            ]
        }
    ]

    # Save JSON & ZIP
    json_path = "wp-json-elementor/meta-bar-perfect-aligned.json"
    zip_path = "wp-json-elementor/meta-bar-perfect-aligned.zip"
    
    full_template = {
        "version": "3.0.0",
        "title": "Perfect Vertical Aligned Meta Bar",
        "type": "section",
        "elementor_version": "3.35.1",
        "content": aligned_meta_bar,
        "page_settings": {}
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(aligned_meta_bar, f, ensure_ascii=False, indent=2)

    with open(zip_path, "w") as f:
        pass
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported Perfect Aligned JSON: {json_path}")
    print(f"[SUCCESS] Exported Perfect Aligned ZIP: {zip_path}")

if __name__ == "__main__":
    export_perfect_aligned_meta_bar()
