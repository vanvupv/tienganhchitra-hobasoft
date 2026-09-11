<?php
/**
 * Lớp WP_ACF_Smart_Importer_Scraper
 * Chịu trách nhiệm tải nội dung HTML từ URL và bóc tách dữ liệu sử dụng CSS Selectors hoặc XPath.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_ACF_Smart_Importer_Scraper {

    /**
     * Chuyển đổi bộ chọn CSS cơ bản sang biểu thức XPath
     * Hỗ trợ các bộ chọn đơn giản như: h1, .title, #content, div.entry-content, .class tag
     * Nếu chuỗi đầu vào bắt đầu bằng / hoặc ( thì được coi như là XPath thô.
     *
     * @param string $selector Bộ chọn CSS hoặc XPath
     * @return string Biểu thức XPath tương ứng
     */
    public static function css_to_xpath( $selector ) {
        $selector = trim( $selector );
        if ( empty( $selector ) ) {
            return '';
        }

        // Nếu bắt đầu bằng / hoặc ( thì coi như là XPath thô sẵn có, giữ nguyên
        if ( strpos( $selector, '/' ) === 0 || strpos( $selector, '(' ) === 0 ) {
            return $selector;
        }

        // Tách các bộ chọn phân cấp bằng khoảng trắng
        $parts = explode( ' ', $selector );
        $xpath_parts = array();

        foreach ( $parts as $part ) {
            $part = trim( $part );
            if ( empty( $part ) ) {
                continue;
            }

            // Phân tích cú pháp ví dụ: div.entry-content hoặc .title hoặc #content
            if ( preg_match( '/^([a-zA-Z0-9\-\*]*)([\.\#])([a-zA-Z0-9\-\_]+)$/', $part, $matches ) ) {
                $tag  = ! empty( $matches[1] ) ? $matches[1] : '*';
                $type = $matches[2]; // . hoặc #
                $name = $matches[3];

                if ( '.' === $type ) {
                    $xpath_parts[] = $tag . "[contains(concat(' ', normalize-space(@class), ' '), ' " . $name . " ')]";
                } else {
                    $xpath_parts[] = $tag . "[@id='" . $name . "']";
                }
            } elseif ( preg_match( '/^[a-zA-Z0-9\-]+$/', $part ) ) {
                // Chỉ là tag (ví dụ: h1, article)
                $xpath_parts[] = $part;
            } else {
                $xpath_parts[] = '*';
            }
        }

        return '//' . implode( '//', $xpath_parts );
    }

    /**
     * Tải và bóc tách dữ liệu từ URL
     *
     * @param string $url URL trang web cần cào
     * @param array  $selectors Mảng chứa bộ chọn cho: title, content, image, remove
     * @return array|WP_Error Mảng kết quả bóc tách được hoặc đối tượng lỗi WP_Error
     */
    public static function scrape_url( $url, $selectors = array() ) {
        if ( empty( $url ) || ! filter_var( $url, FILTER_VALIDATE_URL ) ) {
            return new WP_Error( 'invalid_url', __( 'Đường dẫn URL không hợp lệ.', 'wp-acf-smart-importer' ) );
        }

        // Tải HTML từ URL qua wp_remote_get
        $response = wp_remote_get( $url, array(
            'timeout'    => 30,
            'user-agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sslverify'  => false, // Tránh lỗi SSL trên môi trường localhost
        ) );

        if ( is_wp_error( $response ) ) {
            return $response;
        }

        $html = wp_remote_retrieve_body( $response );
        if ( empty( $html ) ) {
            return new WP_Error( 'empty_html', __( 'Máy chủ không trả về nội dung HTML. Vui lòng kiểm tra lại URL.', 'wp-acf-smart-importer' ) );
        }

        // Khởi tạo DOMDocument
        $dom = new DOMDocument();
        // Bỏ qua các cảnh báo lỗi cú pháp HTML5 hoặc thiếu tag đóng của HTML nguồn
        libxml_use_internal_errors( true );
        // Ép kiểu mã hóa UTF-8 khi nạp HTML
        $dom->loadHTML( '<?xml encoding="utf-8" ?>' . $html );
        libxml_clear_errors();

        $xpath = new DOMXPath( $dom );

        $result = array(
            'title'          => '',
            'content'        => '',
            'featured_image' => '',
        );

        // 1. Bóc tách Tiêu đề (Title)
        $title_selector = isset( $selectors['title'] ) ? self::css_to_xpath( $selectors['title'] ) : '';
        if ( ! empty( $title_selector ) ) {
            $elements = $xpath->query( $title_selector );
            if ( $elements && $elements->length > 0 ) {
                $result['title'] = trim( $elements->item( 0 )->textContent );
            }
        }

        // 2. Bóc tách Nội dung (Content)
        $content_selector = isset( $selectors['content'] ) ? self::css_to_xpath( $selectors['content'] ) : '';
        if ( ! empty( $content_selector ) ) {
            $elements = $xpath->query( $content_selector );
            if ( $elements && $elements->length > 0 ) {
                $node = $elements->item( 0 );

                // 2a. Loại bỏ các phần tử thừa (Quảng cáo, bài viết liên quan...) nếu có cấu hình
                $remove_selector = isset( $selectors['remove'] ) ? self::css_to_xpath( $selectors['remove'] ) : '';
                if ( ! empty( $remove_selector ) ) {
                    $remove_nodes = $xpath->query( $remove_selector, $node );
                    if ( $remove_nodes ) {
                        // Lưu danh sách node cần xóa trước rồi xóa sau để tránh lỗi duyệt cây DOM thay đổi
                        $nodes_to_delete = array();
                        foreach ( $remove_nodes as $rn ) {
                            $nodes_to_delete[] = $rn;
                        }
                        foreach ( $nodes_to_delete as $node_to_delete ) {
                            if ( $node_to_delete->parentNode ) {
                                $node_to_delete->parentNode->removeChild( $node_to_delete );
                            }
                        }
                    }
                }

                // 2b. Lấy HTML của node nội dung bài viết
                $content_html = '';
                foreach ( $node->childNodes as $child ) {
                    $content_html .= $dom->saveHTML( $child );
                }
                $result['content'] = $content_html;
            }
        }

        // 3. Bóc tách Ảnh đại diện (Featured Image)
        $image_selector = isset( $selectors['image'] ) ? self::css_to_xpath( $selectors['image'] ) : '';
        if ( ! empty( $image_selector ) ) {
            $elements = $xpath->query( $image_selector );
            if ( $elements && $elements->length > 0 ) {
                $img_node = $elements->item( 0 );
                if ( 'img' === strtolower( $img_node->nodeName ) ) {
                    // Ưu tiên các thuộc tính lazy-load trước
                    $src = $img_node->getAttribute( 'data-src' );
                    if ( empty( $src ) ) {
                        $src = $img_node->getAttribute( 'data-original' );
                    }
                    if ( empty( $src ) ) {
                        $src = $img_node->getAttribute( 'src' );
                    }
                    $result['featured_image'] = $src;
                } else {
                    // Nếu là thẻ meta (như meta property="og:image") hoặc thẻ liên kết
                    $src = $img_node->getAttribute( 'content' );
                    if ( empty( $src ) ) {
                        $src = $img_node->getAttribute( 'href' );
                    }
                    $result['featured_image'] = $src;
                }
            }
        }

        // 4. Giải quyết các đường dẫn ảnh tương đối (Relative URLs) sang đường dẫn tuyệt đối (Absolute URLs)
        $url_parts = parse_url( $url );
        $base_url  = $url_parts['scheme'] . '://' . $url_parts['host'];

        if ( ! empty( $result['featured_image'] ) ) {
            $img_url = trim( $result['featured_image'] );
            if ( strpos( $img_url, '//' ) === 0 ) {
                $result['featured_image'] = $url_parts['scheme'] . ':' . $img_url;
            } elseif ( strpos( $img_url, '/' ) === 0 ) {
                $result['featured_image'] = $base_url . $img_url;
            } elseif ( ! filter_var( $img_url, FILTER_VALIDATE_URL ) ) {
                // Tương đối so với URL thư mục hiện tại của bài viết
                $path = isset( $url_parts['path'] ) ? dirname( $url_parts['path'] ) : '';
                $result['featured_image'] = $base_url . '/' . trim( $path, '/' ) . '/' . $img_url;
            }
        }

        return $result;
    }
}
