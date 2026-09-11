<?php
/**
 * Lớp WP_ACF_Smart_Importer_Engine
 * Thực hiện quá trình chèn bài viết và cập nhật dữ liệu ACF.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_ACF_Smart_Importer_Engine {

    /**
     * Nhập một bài viết đơn lẻ từ dữ liệu dòng đã map
     *
     * @param array  $row Dòng dữ liệu thô dạng key-value
     * @param array  $mapping Sơ đồ ánh xạ (ví dụ: array('post_title' => 'col_0', 'acf_truong_1' => 'col_1'))
     * @param string $post_type Custom Post Type đích
     * @param string $post_status Trạng thái mặc định (draft, publish, pending)
     * @return int|WP_Error ID của bài viết được tạo hoặc đối tượng lỗi WP_Error
     */
    public static function import_single_row( $row, $mapping, $post_type = 'post', $post_status = 'draft' ) {
        // Trích xuất các trường mặc định của WordPress
        $post_title   = isset( $mapping['post_title'] ) && isset( $row[ $mapping['post_title'] ] ) ? sanitize_text_field( $row[ $mapping['post_title'] ] ) : '';
        $post_content = isset( $mapping['post_content'] ) && isset( $row[ $mapping['post_content'] ] ) ? wp_kses_post( $row[ $mapping['post_content'] ] ) : '';
        $post_excerpt = isset( $mapping['post_excerpt'] ) && isset( $row[ $mapping['post_excerpt'] ] ) ? sanitize_textarea_field( $row[ $mapping['post_excerpt'] ] ) : '';
        $post_date    = isset( $mapping['post_date'] ) && isset( $row[ $mapping['post_date'] ] ) ? sanitize_text_field( $row[ $mapping['post_date'] ] ) : '';

        // Đảm bảo có Tiêu đề tối thiểu
        if ( empty( $post_title ) ) {
            $post_title = __( 'Bài viết tự động - ' . current_time( 'Y-m-d H:i:s' ), 'wp-acf-smart-importer' );
        }

        $post_data = array(
            'post_title'   => $post_title,
            'post_content' => $post_content,
            'post_excerpt' => $post_excerpt,
            'post_status'  => $post_status,
            'post_type'    => $post_type,
        );

        // Định dạng ngày nếu có cấu hình
        if ( ! empty( $post_date ) ) {
            $parsed_time = strtotime( $post_date );
            if ( $parsed_time ) {
                $post_data['post_date'] = date( 'Y-m-d H:i:s', $parsed_time );
            }
        }

        // Kiểm tra xem có cần cập nhật bài viết cũ hay không
        $target_post_id = 0;
        if ( isset( $mapping['post_id'] ) && isset( $row[ $mapping['post_id'] ] ) ) {
            $target_post_id = intval( $row[ $mapping['post_id'] ] );
        }

        if ( $target_post_id > 0 && get_post( $target_post_id ) ) {
            // Cập nhật bài viết cũ
            $post_data['ID'] = $target_post_id;
            $post_id = wp_update_post( $post_data );
        } else {
            // Tạo bài viết mới
            $post_id = wp_insert_post( $post_data );
        }

        if ( is_wp_error( $post_id ) ) {
            return $post_id;
        }

        // Tự động khởi tạo cấu hình chuẩn cho WooCommerce Product
        if ( 'product' === $post_type ) {
            if ( taxonomy_exists( 'product_type' ) ) {
                wp_set_object_terms( $post_id, 'simple', 'product_type' );
            }
            if ( ! get_post_meta( $post_id, '_stock_status', true ) ) {
                update_post_meta( $post_id, '_stock_status', 'instock' );
            }
            if ( ! get_post_meta( $post_id, '_visibility', true ) ) {
                update_post_meta( $post_id, '_visibility', 'visible' );
            }
        }

        // Xử lý Featured Image (Ảnh đại diện)
        if ( isset( $mapping['featured_image'] ) && isset( $row[ $mapping['featured_image'] ] ) ) {
            $image_source = trim( $row[ $mapping['featured_image'] ] );
            if ( ! empty( $image_source ) ) {
                $attachment_id = self::handle_media_import( $image_source, $post_id );
                if ( $attachment_id && ! is_wp_error( $attachment_id ) ) {
                    set_post_thumbnail( $post_id, $attachment_id );
                }
            }
        }

        // Xử lý lưu các trường ACF & Custom Meta
        foreach ( $mapping as $destination => $source_col ) {
            if ( ! isset( $row[ $source_col ] ) ) {
                continue;
            }

            $field_val = $row[ $source_col ];

            // Nếu đang cập nhật bài viết cũ và giá trị bị trống, bỏ qua để tránh ghi đè mất dữ liệu cũ
            if ( $target_post_id > 0 && ( $field_val === '' || $field_val === null ) ) {
                continue;
            }

            if ( strpos( $destination, 'acf_' ) === 0 ) {
                $acf_field_key = substr( $destination, 4 ); // Lấy field name thực tế

                if ( function_exists( 'update_field' ) ) {
                    // Lấy thông tin cấu hình của ACF field để định dạng đầu vào phù hợp
                    $acf_field = acf_get_field( $acf_field_key );

                    if ( $acf_field ) {
                        $field_type = $acf_field['type'];

                        // Định dạng giá trị dựa trên loại trường
                        switch ( $field_type ) {
                            case 'image':
                            case 'file':
                                if ( filter_var( $field_val, FILTER_VALIDATE_URL ) ) {
                                    $file_id = self::handle_media_import( $field_val, $post_id );
                                    if ( $file_id && ! is_wp_error( $file_id ) ) {
                                        $field_val = $file_id;
                                    }
                                }
                                break;
                            case 'checkbox':
                            case 'select':
                                if ( ! empty( $acf_field['multiple'] ) || $field_type === 'checkbox' ) {
                                    if ( is_string( $field_val ) ) {
                                        $field_val = array_map( 'trim', explode( ',', $field_val ) );
                                    }
                                }
                                break;
                            case 'number':
                                $field_val = floatval( $field_val );
                                break;
                            case 'boolean':
                            case 'true_false':
                                $field_val = filter_var( $field_val, FILTER_VALIDATE_BOOLEAN );
                                break;
                        }
                    }
                    update_field( $acf_field_key, $field_val, $post_id );
                } else {
                    update_post_meta( $post_id, $acf_field_key, $field_val );
                }
            } elseif ( strpos( $destination, 'tax_' ) === 0 ) {
                $taxonomy = substr( $destination, 4 );
                self::handle_taxonomy_import( $post_id, $field_val, $taxonomy );
            } elseif ( strpos( $destination, 'meta_' ) === 0 ) {
                $meta_key = substr( $destination, 5 );
                
                // Nếu giá trị có thể là JSON
                $decoded = json_decode( html_entity_decode( $field_val ), true );
                $save_val = ( $decoded !== null ) ? $decoded : $field_val;

                update_post_meta( $post_id, $meta_key, $save_val );
            }
        }

        // Đồng bộ giá bán sản phẩm WooCommerce nếu có
        if ( 'product' === $post_type ) {
            $reg_price = get_post_meta( $post_id, '_regular_price', true );
            $sale_price = get_post_meta( $post_id, '_sale_price', true );
            if ( ! empty( $sale_price ) ) {
                update_post_meta( $post_id, '_price', $sale_price );
            } elseif ( ! empty( $reg_price ) ) {
                update_post_meta( $post_id, '_price', $reg_price );
            }
        }

        return $post_id;
    }

    /**
     * Tải và thêm file media từ URL ngoài hoặc xử lý ID media có sẵn
     *
     * @param string $file_url Đường dẫn URL của file ảnh/tài liệu ngoài
     * @param int    $post_id ID bài viết để gắn kết
     * @return int|bool ID đính kèm (attachment) hoặc false nếu lỗi
     */
    public static function handle_media_import( $file_url, $post_id ) {
        if ( empty( $file_url ) ) {
            return false;
        }

        // Nếu đã là một số nguyên (ID media nội bộ), trả về luôn
        if ( is_numeric( $file_url ) && intval( $file_url ) > 0 ) {
            return intval( $file_url );
        }

        if ( ! filter_var( $file_url, FILTER_VALIDATE_URL ) ) {
            return false;
        }

        // Bao gồm các thư viện cần thiết để xử lý media sideload trong WordPress
        require_once ABSPATH . 'wp-admin/includes/image.php';
        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/media.php';

        // Tải tạm file về máy chủ
        $tmp = download_url( $file_url );

        if ( is_wp_error( $tmp ) ) {
            return false;
        }

        // Lấy tên file gốc
        $file_name = basename( parse_url( $file_url, PHP_URL_PATH ) );
        if ( empty( $file_name ) ) {
            $file_name = 'imported-image-' . time() . '.jpg';
        }

        $file_array = array(
            'name'     => $file_name,
            'tmp_name' => $tmp,
        );

        // Lưu vào Media Library
        $attachment_id = media_handle_sideload( $file_array, $post_id );

        // Nếu lỗi, xóa file tạm
        if ( is_wp_error( $attachment_id ) ) {
            @unlink( $file_array['tmp_name'] );
            return false;
        }

        return $attachment_id;
    }

    /**
     * Xử lý nhập chuyên mục phân cấp và gán vào bài viết
     *
     * @param int    $post_id ID bài viết
     * @param string $term_path_str Chuỗi đường dẫn phân cấp (Ví dụ: "Bất động sản > Chung cư, Tin tức > Dự án")
     * @param string $taxonomy Tên Taxonomy phân loại
     */
    public static function handle_taxonomy_import( $post_id, $term_path_str, $taxonomy, $append = false ) {
        if ( empty( $term_path_str ) || empty( $taxonomy ) ) {
            return;
        }

        // Tách các đường dẫn bằng dấu phẩy
        $paths = array_map( 'trim', explode( ',', $term_path_str ) );
        $all_term_ids = array();

        foreach ( $paths as $path ) {
            if ( empty( $path ) ) {
                continue;
            }

            // Tách từng cấp của đường dẫn bằng dấu >
            $levels = array_map( 'trim', explode( '>', $path ) );
            $parent_id = 0;

            foreach ( $levels as $level_name ) {
                if ( empty( $level_name ) ) {
                    continue;
                }

                // Kiểm tra xem term đã tồn tại ở cấp này chưa
                $term = term_exists( $level_name, $taxonomy, $parent_id );

                if ( $term ) {
                    // Nếu đã tồn tại, lấy ID
                    if ( is_array( $term ) ) {
                        $parent_id = intval( $term['term_id'] );
                    } else {
                        $parent_id = intval( $term );
                    }
                } else {
                    // Nếu chưa tồn tại, tạo mới
                    $args = array();
                    if ( $parent_id > 0 ) {
                        $args['parent'] = $parent_id;
                    }
                    
                    $inserted = wp_insert_term( $level_name, $taxonomy, $args );

                    if ( ! is_wp_error( $inserted ) && is_array( $inserted ) ) {
                        $parent_id = intval( $inserted['term_id'] );
                    } else {
                        break; // Nếu lỗi thì dừng nhánh này
                    }
                }

                // Lưu ID term vào danh sách gán
                if ( $parent_id > 0 ) {
                    $all_term_ids[] = $parent_id;
                }
            }
        }

        // Gán các terms vào bài viết (thay thế hoàn toàn terms cũ nếu $append = false, hoặc thêm vào nếu $append = true)
        if ( ! empty( $all_term_ids ) ) {
            wp_set_object_terms( $post_id, array_unique( $all_term_ids ), $taxonomy, $append );
        }
    }
}
