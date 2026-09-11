import json
import zipfile
import os

def create_elementor_335_exact_meta_bar():
    """Tạo file JSON Template chuẩn 100% cho Elementor Pro 3.35.x / 3.35.1"""
    template_335 = {
        "version": "3.0.0",
        "title": "Elementor Pro 3.35 Meta Bar Container",
        "type": "section",
        "elementor_version": "3.35.1",
        "content": [
            {
                "id": "container_meta_bar_335",
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
                        "id": "col_left_stats_335",
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
                                "id": "w_eye_335",
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
                                "id": "w_chat_335",
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
                        "id": "col_right_heart_335",
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
                                "id": "w_heart_335",
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
        ],
        "page_settings": {}
    }

    json_path = "wp-json-elementor/goongbe-meta-bar-elementor-335.json"
    zip_path = "wp-json-elementor/goongbe-meta-bar-elementor-335.zip"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(template_335, f, ensure_ascii=False, indent=2)

    with open(zip_path, "w") as f:
        pass
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_path, arcname=os.path.basename(json_path))

    print(f"[SUCCESS] Exported Elementor 3.35 JSON: {json_path}")
    print(f"[SUCCESS] Exported Elementor 3.35 ZIP: {zip_path}")

if __name__ == "__main__":
    create_elementor_335_exact_meta_bar()
