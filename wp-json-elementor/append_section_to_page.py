import json
import zipfile
import os

def create_product_carousel_section():
    """Tạo cấu trúc JSON chuẩn cho Section Sản Phẩm Mới & Khăn Ướt (4 Products Carousel)"""
    return {
        "id": "sec_new_products_carousel",
        "elType": "section",
        "isInner": False,
        "settings": {
            "background_background": "classic",
            "background_color": "#FAF9F6",
            "padding": {"unit": "px", "top": "70", "right": "40", "bottom": "70", "left": "40", "isLinked": False}
        },
        "elements": [
            {
                "id": "col_new_products_container",
                "elType": "column",
                "isInner": False,
                "settings": {"_column_size": 100},
                "elements": [
                    {
                        "id": "widget_new_products_heading",
                        "elType": "widget",
                        "isInner": False,
                        "widgetType": "heading",
                        "settings": {
                            "title": "SẢN PHẨM MỚI & BỘ SẢN PHẨM KHĂN ƯỚT DỊU NHẸ",
                            "header_size": "h2",
                            "align": "center",
                            "title_color": "#1B5B65",
                            "typography_font_size": {"unit": "px", "size": "32"},
                            "typography_font_weight": "800"
                        }
                    },
                    {
                        "id": "sec_inner_products_4cols",
                        "elType": "section",
                        "isInner": True,
                        "settings": {},
                        "elements": [
                            # CARD 1: Phấn Phủ Baby Powder
                            {
                                "id": "col_prod_1",
                                "elType": "column",
                                "isInner": False,
                                "settings": {"_column_size": 25, "_inline_size": 25},
                                "elements": [
                                    {
                                        "id": "widget_prod_1_img",
                                        "elType": "widget",
                                        "isInner": False,
                                        "widgetType": "image",
                                        "settings": {
                                            "image": {"url": "https://via.placeholder.com/300x300/ffffff/1B5B65?text=Phan+Phu+Baby+Powder"},
                                            "align": "center"
                                        }
                                    },
                                    {
                                        "id": "widget_prod_1_title",
                                        "elType": "widget",
                                        "isInner": False,
                                        "widgetType": "heading",
                                        "settings": {
                                            "title": "<span style='background:#009AA5; color:#fff; font-size:11px; padding:3px 8px; border-radius:4px;'>NEW</span> Phấn Phủ Dịu Nhẹ Em Bé GOONGBE 25g",
                                            "header_size": "h4",
                                            "align": "center",
                                            "title_color": "#333333",
                                            "typography_font_size": {"unit": "px", "size": "15"}
                                        }
                                    }
                                ]
                            },
                            # CARD 2: Baby Hip Cleanser
                            {
                                "id": "col_prod_2",
                                "elType": "column",
                                "isInner": False,
                                "settings": {"_column_size": 25, "_inline_size": 25},
                                "elements": [
                                    {
                                        "id": "widget_prod_2_img",
                                        "elType": "widget",
                                        "isInner": False,
                                        "widgetType": "image",
                                        "settings": {
                                            "image": {"url": "https://via.placeholder.com/300x300/ffffff/1B5B65?text=Baby+Hip+Cleanser"},
                                            "align": "center"
                                        }
                                    },
                                    {
                                        "id": "widget_prod_2_title",
                                        "elType": "widget",
                                        "isInner": False,
                                        "widgetType": "heading",
                                        "settings": {
                                            "title": "<span style='background:#009AA5; color:#fff; font-size:11px; padding:3px 8px; border-radius:4px;'>NEW</span> Sữa Tắm Vệ Sinh Em Bé Baby Hip Cleanser",
                                            "header_size": "h4",
                                            "align": "center",
                                            "title_color": "#333333",
                                            "typography_font_size": {"unit": "px", "size": "15"}
                                        }
                                    }
                                ]
                            },
                            # CARD 3: Khăn Giấy Ướt Baby Wipes
                            {
                                "id": "col_prod_3",
                                "elType": "column",
                                "isInner": False,
                                "settings": {"_column_size": 25, "_inline_size": 25},
                                "elements": [
                                    {
                                        "id": "widget_prod_3_img",
                                        "elType": "widget",
                                        "isInner": False,
                                        "widgetType": "image",
                                        "settings": {
                                            "image": {"url": "https://via.placeholder.com/300x300/ffffff/1B5B65?text=Baby+Wipes+Tissue"},
                                            "align": "center"
                                        }
                                    },
                                    {
                                        "id": "widget_prod_3_title",
                                        "elType": "widget",
                                        "isInner": False,
                                        "widgetType": "heading",
                                        "settings": {
                                            "title": "<span style='background:#009AA5; color:#fff; font-size:11px; padding:3px 8px; border-radius:4px;'>NEW</span> Khăn Ướt Em Bé An Toàn GOONGBE 70 Tờ",
                                            "header_size": "h4",
                                            "align": "center",
                                            "title_color": "#333333",
                                            "typography_font_size": {"unit": "px", "size": "15"}
                                        }
                                    }
                                ]
                            },
                            # CARD 4: Khăn Ướt Gia Đình
                            {
                                "id": "col_prod_4",
                                "elType": "column",
                                "isInner": False,
                                "settings": {"_column_size": 25, "_inline_size": 25},
                                "elements": [
                                    {
                                        "id": "widget_prod_4_img",
                                        "elType": "widget",
                                        "isInner": False,
                                        "widgetType": "image",
                                        "settings": {
                                            "image": {"url": "https://via.placeholder.com/300x300/ffffff/1B5B65?text=Family+Soft+Wipes"},
                                            "align": "center"
                                        }
                                    },
                                    {
                                        "id": "widget_prod_4_title",
                                        "elType": "widget",
                                        "isInner": False,
                                        "widgetType": "heading",
                                        "settings": {
                                            "title": "Khăn Ướt Dịu Nhẹ Gia Đình GOONGBE 100 Tờ",
                                            "header_size": "h4",
                                            "align": "center",
                                            "title_color": "#333333",
                                            "typography_font_size": {"unit": "px", "size": "15"}
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

def append_section_to_existing_json(page_json_path, position="end", insert_index=None):
    """
    Hàm chèn Section mới vào file JSON trang có sẵn:
    - position = 'end': Thêm vào cuối trang.
    - position = 'start': Chèn vào đầu trang.
    - position = 'index': Chèn vào vị trí cụ thể (insert_index).
    """
    if not os.path.exists(page_json_path):
        print(f"Error: File {page_json_path} not found.")
        return

    with open(page_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_section = create_product_carousel_section()

    if position == 'end':
        data['content'].append(new_section)
        print("[SUCCESS] Added new section to the END of the page!")
    elif position == 'start':
        data['content'].insert(0, new_section)
        print("[SUCCESS] Added new section to the START of the page!")
    elif position == 'index' and insert_index is not None:
        data['content'].insert(insert_index, new_section)
        print(f"[SUCCESS] Inserted new section at index {insert_index}!")

    # Ghi lại file JSON
    with open(page_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Nén lại file ZIP tương ứng
    zip_path = page_json_path.replace('.json', '.zip')
    with open(zip_path, 'w') as f_zip:
        pass # Create/overwrite
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(page_json_path, arcname=os.path.basename(page_json_path))

    print(f"[COMPLETED] Updated {page_json_path} and recreated {zip_path} successfully!")

if __name__ == "__main__":
    target_json = "wp-json-elementor/goongbe-homepage-elementor-template.json"
    # Chèn Section Sản phẩm mới vào vị trí index 4 (Sau Best Sellers, trước Mây Mascot)
    append_section_to_existing_json(target_json, position="index", insert_index=4)

