import json
import zipfile
import os

def generate_post_meta_bar_json():
    """
    Tạo đoạn mã JSON chuẩn Elementor Flexbox Container cho thanh Meta Bar:
    - Đường kẻ viền mỏng ở trên (border-top: 1px solid #E5E7EB)
    - Khối 1 (Bên trái): Icon mắt 👁️ + Lượt xem '8' & Icon chat 💬 + Số comment '0'
    - Khối 2 (Bên phải): Icon trái tim ❤️ (Màu đỏ viền #EF4444)
    """
    meta_bar_json = {
        "version": "3.0.0",
        "title": "Container Thanh Lượt Xem - Bình Luận & Yêu Thích (Meta Bar)",
        "type": "container",
        "elementor_version": "3.35.1",
        "content": [
            {
                "id": "container_meta_bar_root",
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
                    # KHỐI 1 (BÊN TRÁI): ICON MẮT 👁️ + CHAT 💬
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
                            # ITEM 1: LƯỢT XEM (ICON MẮT + SỐ 8)
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
                            # ITEM 2: BÌNH LUẬN (ICON CHAT + SỐ 0)
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
                    # KHỐI 2 (BÊN PHẢI): ICON TRÁI TIM ❤️
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
                                    "primary_color": "#EF4444", # Màu đỏ nhạt viền trái tim
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

    json_filename = "wp-json-elementor/goongbe-post-meta-bar-container.json"
    zip_filename = "wp-json-elementor/goongbe-post-meta-bar-container.zip"

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(meta_bar_json, f, ensure_ascii=False, indent=2)

    with open(zip_filename, "w") as f:
        pass
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_filename, arcname=os.path.basename(json_filename))

    print(f"[SUCCESS] Exported Meta Bar JSON: {json_filename}")
    print(f"[SUCCESS] Exported Meta Bar ZIP Template: {zip_filename}")
    return meta_bar_json

if __name__ == "__main__":
    generate_post_meta_bar_json()
