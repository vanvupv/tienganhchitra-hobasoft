import json
import zipfile
import os

def build_wix_strip_parallax_json():
    """
    Sinh Section JSON 2 Cột chuẩn Wix Column Strip:
    - Cột 1 (Bên trái): Chứa ảnh sản phẩm đứng yên GOONGBE 500x500
    - Cột 2 (Bên phải): Cột có nền ảnh Parallax (Vertical Scroll / Fixed Attachment) 
      chiều cao 797px, cuộn từ đầu đến cuối khi scroll trang.
    """
    
    col1_left = {
        "id": "col_left_static_img",
        "elType": "column",
        "isInner": False,
        "settings": {
            "_column_size": 50,
            "_inline_size": 50,
            "padding": {"unit": "px", "top": "40", "right": "40", "bottom": "40", "left": "40", "isLinked": False},
            "content_position": "middle"
        },
        "elements": [
            {
                "id": "widget_goongbe_product_img",
                "elType": "widget",
                "isInner": False,
                "widgetType": "image",
                "settings": {
                    "image": {
                        "url": "https://static.wixstatic.com/media/c25106_260ad4b102ce48628dc29d9eec812d63~mv2.jpg/v1/fill/w_488,h_459,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/Goongbe-500X500.jpg"
                    },
                    "image_size": "full",
                    "align": "center",
                    "caption_source": "none"
                }
            }
        ]
    }

    col2_right_parallax = {
        "id": "col_right_parallax_bg",
        "elType": "column",
        "isInner": False,
        "settings": {
            "_column_size": 50,
            "_inline_size": 50,
            "min_height": {"unit": "px", "size": "797"},
            "background_background": "classic",
            "background_image": {
                "url": "https://static.wixstatic.com/media/c25106_6d599c39adc64b8b8254af5ae994ed67~mv2.jpg/v1/fill/w_953,h_797,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/c25106_6d599c39adc64b8b8254af5ae994ed67~mv2.jpg"
            },
            "background_position": "center center",
            "background_repeat": "no-repeat",
            "background_size": "cover",
            "background_attachment": "fixed",  # Cố định nền tạo hiệu ứng cuộn ảnh từ đầu đến cuối (Parallax)
            # Elementor Pro Motion Effects
            "motion_fx_scrolling": "yes",
            "motion_fx_translateY_effect": "yes",
            "motion_fx_translateY_speed": {"unit": "px", "size": "3"},
            "motion_fx_translateY_direction": "up"
        },
        "elements": []
    }

    root_section = {
        "id": "sec_wix_parallax_strip",
        "elType": "section",
        "isInner": False,
        "settings": {
            "layout": "full_width",
            "stretch_section": "section-stretched",
            "gap": "no",
            "content_position": "middle",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [col1_left, col2_right_parallax]
    }

    # Format Array Clipboard dùng cho Paste Ctrl+V
    clipboard_array = [root_section]
    clipboard_json_path = "wp-json-elementor/goongbe-section-parallax-strip-clipboard.json"
    with open(clipboard_json_path, "w", encoding="utf-8") as f:
        json.dump(clipboard_array, f, ensure_ascii=False, indent=2)

    # Format Template ZIP 3.35 Import 1-Click
    full_template = {
        "version": "3.0.0",
        "title": "GOONGBE Parallax Column Strip Section",
        "type": "section",
        "elementor_version": "3.35.1",
        "content": [root_section],
        "page_settings": {}
    }
    
    zip_json_path = "wp-json-elementor/goongbe-section-parallax-strip.json"
    zip_path = "wp-json-elementor/goongbe-section-parallax-strip.zip"

    with open(zip_json_path, "w", encoding="utf-8") as f:
        json.dump(full_template, f, ensure_ascii=False, indent=2)

    with open(zip_path, "w") as f:
        pass
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(zip_json_path, arcname=os.path.basename(zip_json_path))

    print(f"[SUCCESS] Exported Parallax Strip JSON: {zip_json_path}")
    print(f"[SUCCESS] Exported Parallax Strip ZIP: {zip_path}")
    print(f"[SUCCESS] Exported Parallax Clipboard JSON: {clipboard_json_path}")

if __name__ == "__main__":
    build_wix_strip_parallax_json()
