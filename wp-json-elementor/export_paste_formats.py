import json

def export_all_paste_formats():
    """Xuất 2 định dạng mã JSON chuẩn Clipboard cho Elementor (Ctrl+V)"""
    
    # 1. CONTAINER FORMAT (Bọc trong mảng Array [...])
    container_array = [
        {
            "id": "container_meta_bar_paste_array",
            "elType": "container",
            "isInner": False,
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
    ]

    # 2. LEGACY SECTION FORMAT (Dành cho web chưa bật Flexbox Container)
    legacy_section_array = [
        {
            "id": "sec_meta_bar_legacy",
            "elType": "section",
            "isInner": False,
            "settings": {
                "padding": {"unit": "px", "top": "12", "right": "0", "bottom": "12", "left": "0", "isLinked": False},
                "border_border": "solid",
                "border_width": {"unit": "px", "top": "1", "right": "0", "bottom": "0", "left": "0", "isLinked": False},
                "border_color": "#E5E7EB"
            },
            "elements": [
                {
                    "id": "col_left_stats",
                    "elType": "column",
                    "isInner": False,
                    "settings": {"_column_size": 50, "_inline_size": 50},
                    "elements": [
                        {
                            "id": "w_view",
                            "elType": "widget",
                            "isInner": False,
                            "widgetType": "icon-box",
                            "settings": {
                                "selected_icon": {"value": "far fa-eye", "library": "fa-regular"},
                                "title_text": "8",
                                "position": "left",
                                "title_color": "#0EA5E9"
                            }
                        },
                        {
                            "id": "w_comment",
                            "elType": "widget",
                            "isInner": False,
                            "widgetType": "icon-box",
                            "settings": {
                                "selected_icon": {"value": "far fa-comment", "library": "fa-regular"},
                                "title_text": "0",
                                "position": "left",
                                "title_color": "#0EA5E9"
                            }
                        }
                    ]
                },
                {
                    "id": "col_right_heart",
                    "elType": "column",
                    "isInner": False,
                    "settings": {"_column_size": 50, "_inline_size": 50},
                    "elements": [
                        {
                            "id": "w_heart",
                            "elType": "widget",
                            "isInner": False,
                            "widgetType": "icon",
                            "settings": {
                                "selected_icon": {"value": "far fa-heart", "library": "fa-regular"},
                                "primary_color": "#EF4444",
                                "align": "right"
                            }
                        }
                    ]
                }
            ]
        }
    ]

    with open("wp-json-elementor/meta-bar-clipboard-container.json", "w", encoding="utf-8") as f:
        json.dump(container_array, f, ensure_ascii=False, indent=2)

    with open("wp-json-elementor/meta-bar-clipboard-legacy-section.json", "w", encoding="utf-8") as f:
        json.dump(legacy_section_array, f, ensure_ascii=False, indent=2)

    print("[SUCCESS] Exported Clipboard Container & Legacy Section JSON formats successfully.")

if __name__ == "__main__":
    export_all_paste_formats()
