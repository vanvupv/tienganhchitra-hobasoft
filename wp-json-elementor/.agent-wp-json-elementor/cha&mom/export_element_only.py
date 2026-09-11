import json

def export_element_only():
    """Tạo file JSON rút gọn CHỈ BỒ NỘI DUNG CONTAINER (Không có header version/type) dùng để Paste trực tiếp vào Container có sẵn"""
    element_json = {
        "id": "container_meta_bar_paste_inner",
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "justify_content": "space-between",
            "align_items": "center",
            "padding": {"unit": "px", "top": "12", "right": "0", "bottom": "12", "left": "0", "isLinked": False},
            "border_border": "solid",
            "border_width": {"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
            "border_color": "#E5E7EB"
        },
        "elements": [
            {
                "id": "container_left_stats",
                "elType": "container",
                "isInner": True,
                "settings": {
                    "content_width": "full",
                    "flex_direction": "row",
                    "align_items": "center",
                    "gap": {"unit": "px", "size": "24"}
                },
                "elements": [
                    {
                        "id": "widget_view_count",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "icon-box",
                        "settings": {
                            "selected_icon": {"value": "far fa-eye", "library": "fa-regular"},
                            "title_text": "8",
                            "position": "left",
                            "icon_color": "#333333",
                            "title_color": "#0EA5E9",
                            "icon_size": {"unit": "px", "size": "18"},
                            "typography_font_size": {"unit": "px", "size": "14"},
                            "typography_font_weight": "600"
                        }
                    },
                    {
                        "id": "widget_comment_count",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "icon-box",
                        "settings": {
                            "selected_icon": {"value": "far fa-comment", "library": "fa-regular"},
                            "title_text": "0",
                            "position": "left",
                            "icon_color": "#333333",
                            "title_color": "#0EA5E9",
                            "icon_size": {"unit": "px", "size": "18"},
                            "typography_font_size": {"unit": "px", "size": "14"},
                            "typography_font_weight": "600"
                        }
                    }
                ]
            },
            {
                "id": "container_right_heart",
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
                        "id": "widget_heart_icon",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "icon",
                        "settings": {
                            "selected_icon": {"value": "far fa-heart", "library": "fa-regular"},
                            "primary_color": "#EF4444",
                            "size": {"unit": "px", "size": "20"},
                            "hover_primary_color": "#DC2626"
                        }
                    }
                ]
            }
        ]
    }

    json_path = "wp-json-elementor/goongbe-post-meta-bar-element-only.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(element_json, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Exported Element-only JSON for Container Paste: {json_path}")

if __name__ == "__main__":
    export_element_only()
