import json
import zipfile
import os

def generate_single_section_slider_template():
    """
    Tạo file JSON Template độc lập của DUY NHẤT 1 Section:
    - Bố cục: Full Width (Tràn toàn màn hình)
    - Widget: Elementor Media / Image Carousel Widget (hoặc Slides Widget)
    - Cấu hình Slide: Hiển thị 4 Slides cùng lúc, trượt 1 Slide mỗi lần (slides_to_show: 4, slides_to_scroll: 1)
    - Chiều cao ảnh: Bằng nhau 100% (Aspect ratio 1:1, Height 320px)
    """
    single_section_json = {
        "version": "3.0.0",
        "title": "Section Slide 4 Sản Phẩm Mới & Khăn Ướt GOONGBE (Full Width 4 Slides)",
        "type": "section",
        "elementor_version": "3.35.1",
        "content": [
            {
                "id": "sec_san_pham_moi_carousel_fullwidth",
                "elType": "section",
                "isInner": False,
                "settings": {
                    "layout": "full_width", # Bố cục toàn màn hình
                    "stretch_section": "section-stretched", # Stretch tràn lề 100vw
                    "background_background": "classic",
                    "background_color": "#FAF9F6",
                    "padding": {"unit": "px", "top": "60", "right": "0", "bottom": "60", "left": "0", "isLinked": False}
                },
                "elements": [
                    {
                        "id": "col_carousel_wrapper",
                        "elType": "column",
                        "isInner": False,
                        "settings": {"_column_size": 100},
                        "elements": [
                            # TIÊU ĐỀ KHỐI SLIDE
                            {
                                "id": "widget_carousel_title",
                                "elType": "widget",
                                "isInner": False,
                                "widgetType": "heading",
                                "settings": {
                                    "title": "SẢN PHẨM MỚI & BỘ KHĂN ƯỚT DỊU NHẸ GOONGBE",
                                    "header_size": "h2",
                                    "align": "center",
                                    "title_color": "#1B5B65",
                                    "typography_font_size": {"unit": "px", "size": "30"},
                                    "typography_font_weight": "800",
                                    "margin": {"unit": "px", "top": "0", "right": "0", "bottom": "30", "left": "0", "isLinked": False}
                                }
                            },
                            # WIDGET CAROUSEL / SLIDE 4 ITEMS (SLIDES TO SHOW: 4, SCROLL: 1)
                            {
                                "id": "widget_product_slider_4cols",
                                "elType": "widget",
                                "isInner": False,
                                "widgetType": "media-carousel", # Elementor Pro Carousel Engine
                                "settings": {
                                    "skin": "carousel",
                                    "slides_per_view": "4", # Hiển thị 4 slide trên màn hình
                                    "slides_per_view_tablet": "2", # Tablet 2 slide
                                    "slides_per_view_mobile": "1", # Mobile 1 slide
                                    "slides_to_scroll": "1", # Trượt 1 slide mỗi lần
                                    "image_size": "full",
                                    "equal_height": "yes", # Chiều cao các ảnh bằng nhau 100%
                                    "image_height": {"unit": "px", "size": "320"},
                                    "navigation": "both", # Arrows + Dots
                                    "arrow_color": "#009AA5", # Nút mũi tên màu xanh ngọc
                                    "arrow_size": {"unit": "px", "size": "24"},
                                    "autoplay": "yes",
                                    "autoplay_speed": 4000,
                                    "pause_on_hover": "yes",
                                    "infinite": "yes",
                                    "effect": "slide",
                                    "slides": [
                                        # SLIDE 1: Phấn phủ em bé (Badge New + Dermatest)
                                        {
                                            "_id": "slide_item_1",
                                            "image": {
                                                "url": "https://via.placeholder.com/400x400/FFFFFF/009AA5?text=Phan+Phu+Goongbe+25g"
                                            },
                                            "title": "Phấn Phủ Dịu Nhẹ Em Bé GOONGBE 25g",
                                            "badge_text": "New",
                                            "badge_color": "#009AA5",
                                            "seal_image": "Dermatest Excellent 2023",
                                            "link": {"url": "#product-phan-phu"}
                                        },
                                        # SLIDE 2: Baby Hip Cleanser (Badge New + Dermatest)
                                        {
                                            "_id": "slide_item_2",
                                            "image": {
                                                "url": "https://via.placeholder.com/400x400/FFFFFF/009AA5?text=Baby+Hip+Cleanser"
                                            },
                                            "title": "Sữa Tắm Vệ Sinh Em Bé Baby Hip Cleanser 300ml",
                                            "badge_text": "New",
                                            "badge_color": "#009AA5",
                                            "seal_image": "Dermatest Excellent 2023",
                                            "link": {"url": "#product-hip-cleanser"}
                                        },
                                        # SLIDE 3: Khăn Giấy Ướt Baby Wipes (Badge New + Dermatest)
                                        {
                                            "_id": "slide_item_3",
                                            "image": {
                                                "url": "https://via.placeholder.com/400x400/FFFFFF/009AA5?text=Khăn+Ướt+Goongbe+70+Tờ"
                                            },
                                            "title": "Khăn Ướt Em Bé An Toàn GOONGBE 70 Tờ",
                                            "badge_text": "New",
                                            "badge_color": "#009AA5",
                                            "seal_image": "Dermatest Excellent 2023",
                                            "link": {"url": "#product-baby-wipes"}
                                        },
                                        # SLIDE 4: Khăn Ướt Gia Đình (Dermatest)
                                        {
                                            "_id": "slide_item_4",
                                            "image": {
                                                "url": "https://via.placeholder.com/400x400/FFFFFF/009AA5?text=Khăn+Ướt+Gia+Đình+100+Tờ"
                                            },
                                            "title": "Khăn Ướt Dịu Nhẹ Gia Đình GOONGBE 100 Tờ",
                                            "badge_text": "",
                                            "badge_color": "",
                                            "seal_image": "Dermatest Excellent 2023",
                                            "link": {"url": "#product-family-wipes"}
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        ],
        "page_settings": {}
    }

    json_filename = "wp-json-elementor/goongbe-section-san-pham-moi-khan-uot.json"
    zip_filename = "wp-json-elementor/goongbe-section-san-pham-moi-khan-uot.zip"

    # Save JSON file
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(single_section_json, f, ensure_ascii=False, indent=2)

    # Compress into ZIP template file
    with open(zip_filename, "w") as f:
        pass
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(json_filename, arcname=os.path.basename(json_filename))

    print(f"[SUCCESS] Updated Single Section JSON Slider: {json_filename}")
    print(f"[SUCCESS] Recreated ZIP Template: {zip_filename}")

if __name__ == "__main__":
    generate_single_section_slider_template()
