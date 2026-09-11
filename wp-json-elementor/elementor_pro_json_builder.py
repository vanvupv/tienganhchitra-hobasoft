import json
import zipfile
import os

class ElementorProJsonBuilder:
    """
    SCRIPT CHUYÊN DỤNG TỰ ĐỘNG HÓA SINH JSON ELEMENTOR PRO CHUẨN 100%
    Hỗ trợ sinh Full Page, Standalone Section và Clipboard Array cho Ctrl+V Paste.
    """

    def __init__(self, title="Elementor Pro Generated Template"):
        self.title = title
        self.version = "3.0.0"
        self.elementor_version = "3.35.1"
        self.content = []

    def add_fullwidth_container(self, bg_color="#FAF9F6", padding_top="60", padding_bottom="60"):
        """Tạo Root Section Container Full Width 100vw chuẩn Elementor Pro"""
        return {
            "id": f"sec_root_{len(self.content) + 100}",
            "elType": "section",
            "isInner": False,
            "settings": {
                "layout": "full_width",
                "stretch_section": "section-stretched",
                "background_background": "classic",
                "background_color": bg_color,
                "padding": {"unit": "px", "top": str(padding_top), "right": "0", "bottom": str(padding_bottom), "left": "0", "isLinked": False}
            },
            "elements": []
        }

    def build_media_carousel_widget(self, slides_data, slides_per_view=4, slides_to_scroll=1, equal_height=True):
        """Sinh Widget Media Carousel trượt 4 sản phẩm chuẩn 100%"""
        slides_list = []
        for idx, item in enumerate(slides_data):
            slides_list.append({
                "_id": f"slide_{idx + 1000}",
                "image": {"url": item.get("image_url", "https://via.placeholder.com/400x400")},
                "title": item.get("title", ""),
                "badge_text": item.get("badge_text", ""),
                "badge_color": item.get("badge_color", "#009AA5"),
                "link": {"url": item.get("link_url", "#")}
            })

        return {
            "id": f"widget_carousel_{len(slides_list)}",
            "elType": "widget",
            "isInner": False,
            "widgetType": "media-carousel",
            "settings": {
                "skin": "carousel",
                "slides_per_view": str(slides_per_view),
                "slides_per_view_tablet": "2",
                "slides_per_view_mobile": "1",
                "slides_to_scroll": str(slides_to_scroll),
                "image_size": "full",
                "equal_height": "yes" if equal_height else "no",
                "image_height": {"unit": "px", "size": "320"},
                "navigation": "both",
                "arrow_color": "#009AA5",
                "autoplay": "yes",
                "autoplay_speed": 4000,
                "pause_on_hover": "yes",
                "infinite": "yes",
                "slides": slides_list
            }
        }

    def build_post_meta_bar_container(self, view_count=8, comment_count=0, heart_color="#EF4444"):
        """Sinh Container Flexbox Meta Bar (Mắt 👁️ + Chat 💬 bên trái, Trái tim ❤️ bên phải)"""
        return {
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
                                "title_text": str(view_count),
                                "position": "left",
                                "icon_color": "#333333",
                                "title_color": "#0EA5E9"
                            }
                        },
                        {
                            "id": "widget_comment_count",
                            "elType": "widget",
                            "isInner": False,
                            "widgetType": "icon-box",
                            "settings": {
                                "selected_icon": {"value": "far fa-comment", "library": "fa-regular"},
                                "title_text": str(comment_count),
                                "position": "left",
                                "icon_color": "#333333",
                                "title_color": "#0EA5E9"
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
                                "primary_color": heart_color,
                                "size": {"unit": "px", "size": "20"}
                            }
                        }
                    ]
                }
            ]
        }

    def export_all(self, base_filename):
        """Xuất đầy đủ 3 định dạng: Full Page JSON, Standalone Section ZIP, và Clipboard Array JSON"""
        # 1. Full Page JSON & ZIP
        page_data = {
            "version": self.version,
            "title": self.title,
            "type": "page",
            "elementor_version": self.elementor_version,
            "content": self.content,
            "page_settings": {}
        }
        json_path = f"wp-json-elementor/{base_filename}.json"
        zip_path = f"wp-json-elementor/{base_filename}.zip"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)

        with open(zip_path, "w") as f:
            pass
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(json_path, arcname=os.path.basename(json_path))

        # 2. Clipboard Array JSON (Bọc mảng cho Ctrl+V paste)
        clipboard_path = f"wp-json-elementor/{base_filename}-clipboard-array.json"
        with open(clipboard_path, "w", encoding="utf-8") as f:
            json.dump(self.content, f, ensure_ascii=False, indent=2)

        print(f"[SUCCESS] Exported Page Template: {json_path}")
        print(f"[SUCCESS] Exported ZIP Archive: {zip_path}")
        print(f"[SUCCESS] Exported Clipboard Array: {clipboard_path}")

if __name__ == "__main__":
    builder = ElementorProJsonBuilder("Trang Chủ GOONGBE VN - Auto Generated")
    
    # Thêm Section Carousel 4 Sản phẩm
    sec1 = builder.add_fullwidth_container(bg_color="#FAF9F6")
    carousel_widget = builder.build_media_carousel_widget([
        {"title": "Phấn Phủ Dịu Nhẹ Em Bé GOONGBE 25g", "badge_text": "New"},
        {"title": "Sữa Tắm Vệ Sinh Em Bé Baby Hip Cleanser 300ml", "badge_text": "New"},
        {"title": "Khăn Ướt Em Bé An Toàn GOONGBE 70 Tờ", "badge_text": "New"},
        {"title": "Khăn Ướt Dịu Nhẹ Gia Đình GOONGBE 100 Tờ", "badge_text": ""}
    ], slides_per_view=4, slides_to_scroll=1, equal_height=True)
    sec1["elements"].append({"id": "col_1", "elType": "column", "isInner": False, "settings": {"_column_size": 100}, "elements": [carousel_widget]})
    builder.content.append(sec1)

    # Thêm Section Meta Bar (Mắt + Chat bên trái, Trái tim bên phải)
    meta_container = builder.build_post_meta_bar_container(view_count=8, comment_count=0, heart_color="#EF4444")
    builder.content.append(meta_container)

    # Xuất toàn bộ
    builder.export_all("goongbe-auto-builder-master")
