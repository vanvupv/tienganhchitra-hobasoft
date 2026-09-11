<?php
/**
 * Lớp WP_ACF_Smart_Importer_Generator
 * Chịu trách nhiệm phân tích cấu trúc trường và sinh dữ liệu mẫu ngẫu nhiên (Rule-based) hoặc qua AI.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_ACF_Smart_Importer_Generator {

    /**
     * Sinh danh sách dữ liệu mẫu dựa trên thuật toán Rule-based
     *
     * @param string $post_type Custom Post Type đích
     * @param int    $count Số lượng bài viết ảo cần sinh
     * @param int    $ref_post_id ID bài viết mẫu cụ thể dùng làm tham chiếu
     * @return array Mảng chứa các hàng dữ liệu dạng key-value
     */
    /**
     * Sinh danh sách dữ liệu mẫu dựa trên thuật toán Rule-based
     *
     * @param string $post_type Custom Post Type đích
     * @param int    $count Số lượng bài viết ảo cần sinh
     * @param int    $ref_post_id ID bài viết mẫu cụ thể dùng làm tham chiếu
     * @param string $gen_type Loại sinh: 'new' (tạo mới) hoặc 'existing' (bổ sung bài viết cũ)
     * @return array|WP_Error Mảng chứa các hàng dữ liệu dạng key-value hoặc đối tượng WP_Error
     */
    public static function generate_rule_based_data( $post_type, $count = 10, $ref_post_id = 0, $gen_type = 'new', $fields = array(), $user_topic = '', $length = 'medium', $tone = 'seo', $lang = 'vi' ) {
        $generated_rows = array();

        // Nếu không có fields truyền từ client, tự quét
        if ( empty( $fields ) ) {
            $acf_fields = self::get_acf_fields_for_post_type( $post_type );
            $fields = array(
                array( 'name' => 'post_title', 'type' => 'wp_core', 'label' => 'Tiêu đề' ),
                array( 'name' => 'post_content', 'type' => 'wp_core', 'label' => 'Nội dung' ),
                array( 'name' => 'post_excerpt', 'type' => 'wp_core', 'label' => 'Mô tả ngắn' ),
                array( 'name' => 'post_date', 'type' => 'wp_core', 'label' => 'Ngày đăng' ),
                array( 'name' => 'featured_image', 'type' => 'wp_core', 'label' => 'Ảnh đại diện' ),
            );
            foreach ( $acf_fields as $f ) {
                $fields[] = array(
                    'name'    => 'acf_' . $f['name'],
                    'label'   => $f['label'],
                    'type'    => 'acf_' . $f['type'],
                    'choices' => $f['choices'],
                );
            }

            // Quét các taxonomy công khai của Post Type
            $taxonomies = get_object_taxonomies( $post_type, 'objects' );
            if ( is_array( $taxonomies ) ) {
                foreach ( $taxonomies as $tax_slug => $tax_obj ) {
                    if ( $tax_obj->public ) {
                        $fields[] = array(
                            'name'  => 'tax_' . $tax_slug,
                            'label' => '[Taxonomy] ' . $tax_obj->label . ' (' . $tax_slug . ')',
                            'type'  => 'taxonomy',
                        );
                    }
                }
            }
        }

        // Lấy danh sách bài viết tham chiếu để phân tích giá trị mẫu
        $existing_posts = array();
        if ( $ref_post_id > 0 && get_post( $ref_post_id ) ) {
            $existing_posts = array( get_post( $ref_post_id ) );
        } else {
            $existing_posts = get_posts( array(
                'post_type'      => $post_type,
                'posts_per_page' => 5,
                'post_status'    => 'any',
            ) );
        }

        // Danh sách từ khóa Lorem tiếng Việt
        $lorem_titles = array(
            'Tin tức thị trường nổi bật trong ngày',
            'Giải pháp tối ưu hóa hiệu suất làm việc hiệu quả',
            'Đánh giá chi tiết trải nghiệm người dùng thực tế',
            'Cập nhật xu hướng phát triển công nghệ mới nhất',
            'Hướng dẫn thiết lập hệ thống từ cơ bản đến nâng cao',
            'Bí quyết cải thiện doanh số bán hàng đột phá',
            'Khám phá không gian thiết kế sang trọng đẳng cấp',
            'Tìm hiểu quy trình vận hành tiêu chuẩn quốc tế',
        );

        $lorem_paragraphs = array(
            'Đây là nội dung mô tả chi tiết được sinh ra tự động để kiểm thử giao diện và cấu trúc cơ sở dữ liệu. Hệ thống hỗ trợ xử lý dữ liệu ảo vô cùng nhanh chóng.',
            'Với mong muốn đem lại trải nghiệm tốt nhất, chúng tôi không ngừng cải tiến quy trình và áp dụng công nghệ mới. Dưới đây là các thông số chi tiết cần lưu ý khi vận hành.',
            'Bài viết kiểm tra hiển thị này chứa các thông tin giả định phục vụ quá trình thiết kế giao diện (UI/UX) và kiểm soát lỗi hoạt động của hệ thống cơ sở dữ liệu WordPress.',
        );

        if ( 'existing' === $gen_type ) {
            $existing_posts_to_fill = get_posts( array(
                'post_type'      => $post_type,
                'posts_per_page' => $count,
                'post_status'    => 'any',
            ) );

            if ( empty( $existing_posts_to_fill ) ) {
                return new WP_Error( 'no_posts', __( 'Không tìm thấy bài viết nào có sẵn trên hệ thống để bổ sung dữ liệu.', 'wp-acf-smart-importer' ) );
            }

            $i = 0;
            foreach ( $existing_posts_to_fill as $post ) {
                $i++;
                $row = array(
                    'post_id' => $post->ID,
                );

                foreach ( $fields as $field ) {
                    $f_name = $field['name'];
                    if ( $f_name === 'post_id' ) {
                        continue;
                    }
                    
                    $current_val = '';
                    if ( in_array( $f_name, array( 'post_title', 'post_content', 'post_excerpt', 'post_date', 'featured_image', 'post_name' ) ) ) {
                        if ( $f_name === 'featured_image' ) {
                            $current_val = get_the_post_thumbnail_url( $post->ID, 'full' );
                        } else {
                            $current_val = $post->{$f_name};
                        }
                    } elseif ( strpos( $f_name, 'acf_' ) === 0 ) {
                        $acf_name = substr( $f_name, 4 );
                        $current_val = self::get_acf_field_value( $acf_name, $post->ID );
                    } elseif ( strpos( $f_name, 'meta_' ) === 0 ) {
                        $meta_key = substr( $f_name, 5 );
                        $current_val = get_post_meta( $post->ID, $meta_key, true );
                    }

                    if ( ! self::is_value_empty( $current_val ) ) {
                        if ( is_array( $current_val ) ) {
                            $row[ $f_name ] = json_encode( $current_val, JSON_UNESCAPED_UNICODE );
                        } else {
                            $row[ $f_name ] = $current_val;
                        }
                    } else {
                        $row[ $f_name ] = self::generate_field_value_by_rule( $field, $existing_posts, $i, $lorem_titles, $lorem_paragraphs );
                    }
                }
                $generated_rows[] = $row;
            }
        } else {
            // Sinh mới hoàn toàn
            for ( $i = 1; $i <= $count; $i++ ) {
                $row = array();
                foreach ( $fields as $field ) {
                    $f_name = $field['name'];
                    if ( $f_name === 'post_id' ) {
                        continue;
                    }
                    $row[ $f_name ] = self::generate_field_value_by_rule( $field, $existing_posts, $i, $lorem_titles, $lorem_paragraphs );
                }
                $generated_rows[] = $row;
            }
        }

        return $generated_rows;
    }

    /**
     * Hàm helper sinh dữ liệu mẫu dựa theo luật
     */
    private static function generate_field_value_by_rule( $field, $existing_posts, $i, $lorem_titles, $lorem_paragraphs ) {
        $f_name = $field['name'];
        $f_type = $field['type'];
        $choices = isset( $field['choices'] ) ? $field['choices'] : array();

        if ( ! empty( $existing_posts ) ) {
            $ref_post = $existing_posts[ array_rand( $existing_posts ) ];
            
            if ( $f_name === 'post_title' ) {
                return $ref_post->post_title . ' (Mẫu #' . $i . ')';
            } elseif ( $f_name === 'post_content' ) {
                return $ref_post->post_content;
            } elseif ( $f_name === 'post_excerpt' ) {
                return $ref_post->post_excerpt;
            } elseif ( $f_name === 'post_date' ) {
                return date( 'Y-m-d H:i:s', strtotime( "-$i days" ) );
            } elseif ( $f_name === 'featured_image' ) {
                $img = get_the_post_thumbnail_url( $ref_post->ID, 'full' );
                return ! empty( $img ) ? $img : 'https://picsum.photos/800/600?random=' . $i;
            } elseif ( $f_name === 'post_name' ) {
                return '';
            }
        } else {
            if ( $f_name === 'post_title' ) {
                return $lorem_titles[ array_rand( $lorem_titles ) ] . ' (Mẫu #' . $i . ')';
            } elseif ( $f_name === 'post_content' ) {
                return $lorem_paragraphs[ array_rand( $lorem_paragraphs ) ] . "\n\n" . $lorem_paragraphs[ array_rand( $lorem_paragraphs ) ];
            } elseif ( $f_name === 'post_excerpt' ) {
                return 'Mô tả ngắn mẫu cho bài viết số ' . $i;
            } elseif ( $f_name === 'post_date' ) {
                return date( 'Y-m-d H:i:s', strtotime( "-$i days" ) );
            } elseif ( $f_name === 'featured_image' ) {
                return 'https://picsum.photos/800/600?random=' . $i;
            } elseif ( $f_name === 'post_name' ) {
                return '';
            }
        }

        $clean_type = str_replace( array( 'acf_', 'meta_' ), '', $f_type );

        $existing_values = array();
        foreach ( $existing_posts as $ep ) {
            $val = '';
            if ( strpos( $f_name, 'acf_' ) === 0 ) {
                $val = self::get_acf_field_value( substr( $f_name, 4 ), $ep->ID );
            } elseif ( strpos( $f_name, 'meta_' ) === 0 ) {
                $val = get_post_meta( $ep->ID, substr( $f_name, 5 ), true );
            }
            if ( ! self::is_value_empty( $val ) ) {
                $existing_values[] = $val;
            }
        }

        switch ( $clean_type ) {
            case 'taxonomy':
                $taxonomy = substr( $f_name, 4 );
                $terms = get_terms( array(
                    'taxonomy'   => $taxonomy,
                    'hide_empty' => false,
                    'number'     => 10,
                ) );
                if ( ! is_wp_error( $terms ) && ! empty( $terms ) ) {
                    $term_names = wp_list_pluck( $terms, 'name' );
                    shuffle( $term_names );
                    if ( is_taxonomy_hierarchical( $taxonomy ) ) {
                        if ( count( $term_names ) >= 2 ) {
                            return $term_names[0] . ' > ' . $term_names[1];
                        }
                        return $term_names[0];
                    } else {
                        return implode( ', ', array_slice( $term_names, 0, min( 3, count( $term_names ) ) ) );
                    }
                }
                if ( $taxonomy === 'category' ) {
                    $cats = array(
                        'Tin tức > Xã hội',
                        'Kinh doanh > Đầu tư',
                        'Bất động sản > Căn hộ',
                        'Công nghệ > Phần mềm',
                        'Du lịch > Ẩm thực'
                    );
                    return $cats[ array_rand( $cats ) ];
                } elseif ( $taxonomy === 'post_tag' ) {
                    $tags = array(
                        'Xu hướng, Nổi bật, Hot',
                        'Hướng dẫn, Chia sẻ, Kinh nghiệm',
                        'WordPress, Plugin, Website',
                        'Đời sống, Sức khỏe, Gia đình'
                    );
                    return $tags[ array_rand( $tags ) ];
                } else {
                    $tax_label = ucwords( str_replace( array( '-', '_' ), ' ', $taxonomy ) );
                    return 'Danh mục ' . $tax_label . ' > Phân nhóm ' . $i;
                }

            case 'number':
                if ( ! empty( $existing_values ) ) {
                    $numeric_vals = array_filter( $existing_values, 'is_numeric' );
                    if ( ! empty( $numeric_vals ) ) {
                        return rand( min( $numeric_vals ), max( $numeric_vals ) );
                    }
                }
                return rand( 100, 10000 );

            case 'select':
            case 'checkbox':
            case 'radio':
                if ( ! empty( $choices ) ) {
                    $choice_keys = array_keys( $choices );
                    if ( $clean_type === 'checkbox' || ( isset( $field['multiple'] ) && $field['multiple'] ) ) {
                        $rand_keys = (array) array_rand( $choice_keys, min( 2, count( $choice_keys ) ) );
                        $chosen = array();
                        foreach ( $rand_keys as $rk ) {
                            $chosen[] = $choice_keys[ $rk ];
                        }
                        return implode( ',', $chosen );
                    }
                    return $choice_keys[ array_rand( $choice_keys ) ];
                }
                return 'Option ' . chr( 65 + rand( 0, 2 ) );

            case 'true_false':
            case 'boolean':
                return rand( 0, 1 ) ? '1' : '0';

            case 'image':
            case 'file':
                return 'https://picsum.photos/800/600?random=' . ( $i * 10 + rand( 1, 9 ) );

            case 'date_picker':
                return date( 'Ymd', strtotime( "+$i days" ) );

            case 'email':
                return 'user_' . $i . '@example.com';

            case 'url':
                return 'https://example.com/item-' . $i;

            default:
                if ( ! empty( $existing_values ) ) {
                    $rand_val = $existing_values[ array_rand( $existing_values ) ];
                    return is_array( $rand_val ) ? json_encode( $rand_val, JSON_UNESCAPED_UNICODE ) : $rand_val;
                }
                return 'Dữ liệu mẫu #' . $i . ' cho ' . $field['label'];
        }
    }

    /**
     * Sinh danh sách dữ liệu mẫu bằng cách gọi API Gemini
     *
     * @param string $post_type CPT đích
     * @param int    $count Số lượng bài viết ảo cần sinh
     * @param string $api_key Khóa API Gemini
     * @param int    $ref_post_id ID bài viết mẫu cụ thể dùng làm tham chiếu
     * @param string $gen_type Loại sinh: 'new' hoặc 'existing'
     * @return array|WP_Error Danh sách dữ liệu mẫu hoặc lỗi WP_Error
     */
    public static function generate_ai_based_data( $post_type, $count = 5, $api_key = '', $ref_post_id = 0, $gen_type = 'new', $fields = array(), $user_topic = '', $selected_post_ids = array(), $layout_template = '', $custom_titles = array(), $length = 'medium', $tone = 'seo', $lang = 'vi' ) {
        if ( empty( $api_key ) ) {
            return new WP_Error( 'missing_key', __( 'Chưa cấu hình Gemini API Key.', 'wp-acf-smart-importer' ) );
        }

        // Nếu không có fields truyền từ client, tự quét
        if ( empty( $fields ) ) {
            $acf_fields = self::get_acf_fields_for_post_type( $post_type );
            $fields = array(
                array( 'name' => 'post_title', 'type' => 'wp_core', 'label' => 'Tiêu đề' ),
                array( 'name' => 'post_content', 'type' => 'wp_core', 'label' => 'Nội dung' ),
                array( 'name' => 'post_excerpt', 'type' => 'wp_core', 'label' => 'Mô tả ngắn' ),
                array( 'name' => 'post_date', 'type' => 'wp_core', 'label' => 'Ngày đăng' ),
                array( 'name' => 'featured_image', 'type' => 'wp_core', 'label' => 'Ảnh đại diện' ),
            );
            foreach ( $acf_fields as $f ) {
                $fields[] = array(
                    'name'    => 'acf_' . $f['name'],
                    'label'   => $f['label'],
                    'type'    => 'acf_' . $f['type'],
                    'choices' => $f['choices'],
                );
            }

            // Quét các taxonomy công khai của Post Type
            $taxonomies = get_object_taxonomies( $post_type, 'objects' );
            if ( is_array( $taxonomies ) ) {
                foreach ( $taxonomies as $tax_slug => $tax_obj ) {
                    if ( $tax_obj->public ) {
                        $fields[] = array(
                            'name'  => 'tax_' . $tax_slug,
                            'label' => '[Taxonomy] ' . $tax_obj->label . ' (' . $tax_slug . ')',
                            'type'  => 'taxonomy',
                        );
                    }
                }
            }
        }

        // 1. Phân tích cấu trúc trường và tạo Schema gợi ý cho AI
        $schema_desc = array();

        foreach ( $fields as $field ) {
            $f_name = $field['name'];
            $f_type = $field['type'];
            $f_label = $field['label'];
            $choices = isset( $field['choices'] ) ? $field['choices'] : array();

            if ( $f_name === 'post_title' ) {
                $schema_desc['post_title'] = 'Tiêu đề bài viết (văn bản tiếng Việt, thực tế, hấp dẫn)';
            } elseif ( $f_name === 'post_content' ) {
                $schema_desc['post_content'] = 'Nội dung chi tiết bài viết (dài khoảng 2-3 đoạn văn bằng tiếng Việt phong phú, tự nhiên)';
            } elseif ( $f_name === 'post_excerpt' ) {
                $schema_desc['post_excerpt'] = 'Mô tả ngắn của bài viết (1-2 câu tiếng Việt)';
            } elseif ( $f_name === 'post_date' ) {
                $schema_desc['post_date'] = 'Ngày đăng bài viết (định dạng YYYY-MM-DD HH:MM:SS)';
            } elseif ( $f_name === 'featured_image' ) {
                $schema_desc['featured_image'] = 'Mô tả ngắn gọn bằng tiếng Anh về chủ đề ảnh tương ứng của bài viết để tìm kiếm ảnh (ví dụ: "modern office space", "vietnamese traditional food")';
            } elseif ( $f_name === 'post_name' ) {
                $schema_desc['post_name'] = 'Đường dẫn tĩnh slug của bài viết (ví dụ: "gioi-thieu-du-an-a")';
            } elseif ( strpos( $f_name, 'tax_' ) === 0 ) {
                $taxonomy = substr( $f_name, 4 );
                $schema_desc[ $f_name ] = 'Trường phân loại/chuyên mục "' . $f_label . '" (' . $f_name . '). ' .
                    'BẮT BUỘC sinh dạng đường dẫn phân cấp phân tách bằng dấu ">" (Ví dụ: "Bất động sản > Chung cư" hoặc "Kinh doanh > Khởi nghiệp"). ' .
                    'Nếu là tag/thẻ phẳng, có thể trả về các thẻ cách nhau bằng dấu phẩy (Ví dụ: "Tin hot, Khám phá, WordPress").';
            } elseif ( strpos( $f_type, 'image' ) !== false || strpos( $f_type, 'file' ) !== false ) {
                $schema_desc[ $f_name ] = 'Mô tả ngắn gọn bằng tiếng Anh về chủ đề ảnh/tài liệu tương ứng để tìm kiếm ảnh (ví dụ: "luxury apartment kitchen", "corporate meeting room")';
            } else {
                $clean_type = str_replace( array( 'acf_', 'meta_' ), '', $f_type );
                $desc = 'Trường dữ liệu "' . $f_label . '" (' . $f_name . ') kiểu "' . $clean_type . '"';
                if ( ! empty( $choices ) ) {
                    $desc .= ' có các giá trị lựa chọn bắt buộc sau: [' . implode( ', ', array_keys( $choices ) ) . ']';
                }
                $schema_desc[ $f_name ] = $desc;
            }
        }

        // 2. Thiết lập prompt và ví dụ tham chiếu
        $examples = array();
        $prompt = '';

        if ( 'existing' === $gen_type ) {
            if ( ! empty( $selected_post_ids ) ) {
                $existing_posts_to_fill = get_posts( array(
                    'post_type'      => $post_type,
                    'post__in'       => $selected_post_ids,
                    'orderby'        => 'post__in',
                    'posts_per_page' => $count,
                    'post_status'    => 'any',
                ) );
            } else {
                $existing_posts_to_fill = get_posts( array(
                    'post_type'      => $post_type,
                    'posts_per_page' => $count,
                    'post_status'    => 'any',
                ) );
            }

            if ( empty( $existing_posts_to_fill ) ) {
                return new WP_Error( 'no_posts', __( 'Không tìm thấy bài viết nào có sẵn trên hệ thống để bổ sung dữ liệu.', 'wp-acf-smart-importer' ) );
            }

            $prompt = "Bạn là trợ lý ảo kiểm thử WordPress. Nhiệm vụ của bạn là điền dữ liệu mẫu chất lượng cao cho các bài viết đã có sẵn trong danh sách dưới đây dưới dạng một JSON Array sạch. Cấu trúc từng đối tượng JSON trong mảng phải chứa khóa 'post_id' (khớp chính xác ID bài viết được cung cấp) cùng các trường mặc định và các trường tùy chỉnh tương ứng.\n";
            if ( ! empty( $user_topic ) ) {
                $prompt .= "YÊU CẦU CHỦ ĐỀ NỘI DUNG: " . $user_topic . "\n";
            }
            $prompt .= "Cấu trúc trường đích gồm:\n";
            $prompt .= json_encode( array_merge( array('post_id' => 'Bắt buộc khớp chính xác ID bài viết được cung cấp'), $schema_desc), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) . "\n\n";
            
            $list_to_fill = array();
            foreach ( $existing_posts_to_fill as $idx => $p ) {
                // Sử dụng custom title tương ứng nếu có
                $title = ( ! empty( $custom_titles ) && isset( $custom_titles[ $idx ] ) ) ? $custom_titles[ $idx ] : $p->post_title;
                $list_to_fill[] = array(
                    'post_id'      => $p->ID,
                    'post_title'   => $title,
                    'post_content' => wp_strip_all_tags( $p->post_content ),
                );
            }
            $prompt .= "Danh sách bài viết cần bạn điền trường:\n";
            $prompt .= json_encode( $list_to_fill, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) . "\n\n";
        } else {
            // Sinh bài viết mới
            $existing_posts = array();
            if ( $ref_post_id > 0 && get_post( $ref_post_id ) ) {
                $existing_posts = array( get_post( $ref_post_id ) );
            } else {
                $existing_posts = get_posts( array(
                    'post_type'      => $post_type,
                    'posts_per_page' => 2,
                    'post_status'    => 'any',
                ) );
            }

            if ( ! empty( $existing_posts ) ) {
                foreach ( $existing_posts as $post ) {
                    $ex = array();
                    foreach ( $fields as $field ) {
                        $f_name = $field['name'];
                        if ( $f_name === 'post_id' ) {
                            continue;
                        }
                        $val = '';
                        if ( in_array( $f_name, array( 'post_title', 'post_content', 'post_excerpt', 'post_date', 'featured_image', 'post_name' ) ) ) {
                            if ( $f_name === 'featured_image' ) {
                                $val = get_the_post_thumbnail_url( $post->ID, 'full' );
                            } elseif ( $f_name === 'post_content' ) {
                                $val = mb_substr( wp_strip_all_tags( $post->post_content ), 0, 500, 'UTF-8' );
                            } else {
                                $val = $post->{$f_name};
                            }
                        } elseif ( strpos( $f_name, 'acf_' ) === 0 ) {
                            $val = self::get_acf_field_value( substr( $f_name, 4 ), $post->ID );
                        } elseif ( strpos( $f_name, 'meta_' ) === 0 ) {
                            $val = get_post_meta( $post->ID, substr( $f_name, 5 ), true );
                        }

                        if ( is_array( $val ) || is_object( $val ) ) {
                            $val = json_encode( $val, JSON_UNESCAPED_UNICODE );
                        } elseif ( is_string( $val ) && strlen( $val ) > 500 ) {
                            $val = mb_substr( $val, 0, 500, 'UTF-8' );
                        }
                        $ex[ $f_name ] = $val !== null ? $val : '';
                    }
                    $examples[] = $ex;
                }
            }

            if ( ! empty( $custom_titles ) ) {
                $prompt = "Bạn là trợ lý ảo viết nội dung WordPress chuyên nghiệp. Nhiệm vụ của bạn là sinh ra đúng " . intval( $count ) . " bài viết mới dạng JSON Array với các tiêu đề (post_title) khớp BẮT BUỘC 100% theo danh sách tiêu đề dưới đây. Không tự ý sửa đổi từ ngữ trong tiêu đề:\n";
                $prompt .= json_encode( $custom_titles, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) . "\n\n";
                if ( ! empty( $user_topic ) ) {
                    $prompt .= "YÊU CẦU CHỦ ĐỀ NỘI DUNG: " . $user_topic . "\n";
                }
                $prompt .= "Cấu trúc từng đối tượng JSON trong mảng phải chứa chính xác các key sau đây:\n";
                $prompt .= json_encode( $schema_desc, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) . "\n\n";
            } else if ( ! empty( $examples ) ) {
                $prompt = "Bạn là trợ lý ảo viết nội dung WordPress chuyên nghiệp. Nhiệm vụ của bạn là nhân bản bài viết chuẩn (bài viết mẫu tham chiếu) thành " . intval( $count ) . " bài viết khác nhau cùng chủ đề. Các bài viết mới này phải có cấu trúc trường dữ liệu y hệt bài mẫu, nhưng nội dung (tiêu đề, nội dung chi tiết, mô tả ngắn, và các văn bản của trường ACF) phải được viết lại hoàn toàn độc nhất, hấp dẫn, không trùng lặp câu chữ với bài mẫu và với nhau.\n";
                if ( ! empty( $user_topic ) ) {
                    $prompt .= "YÊU CẦU CHỦ ĐỀ NỘI DUNG: " . $user_topic . "\n";
                }
                $prompt .= "Cấu trúc từng đối tượng JSON trong mảng phải chứa chính xác các key sau đây:\n";
                $prompt .= json_encode( $schema_desc, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) . "\n\n";
                $prompt .= "Đây là thông tin chi tiết của Bài Viết Mẫu (Bài chuẩn) để bạn nhân bản:\n";
                $prompt .= json_encode( $examples, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) . "\n\n";
            } else {
                $prompt = "Bạn là trợ lý ảo kiểm thử WordPress. Nhiệm vụ của bạn là sinh ra đúng " . intval( $count ) . " bài viết mẫu chất lượng cao cho Post Type '" . esc_attr( $post_type ) . "' dưới dạng định dạng JSON Array sạch.\n";
                if ( ! empty( $user_topic ) ) {
                    $prompt .= "YÊU CẦU CHỦ ĐỀ NỘI DUNG: " . $user_topic . "\n";
                }
                $prompt .= "Cấu trúc từng đối tượng JSON trong mảng phải chứa chính xác các key sau đây:\n";
                $prompt .= json_encode( $schema_desc, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) . "\n\n";
            }
        }

        if ( 'new' === $gen_type && empty( $custom_titles ) ) {
            $existing_titles_raw = get_posts( array(
                'post_type'      => $post_type,
                'posts_per_page' => 40,
                'post_status'    => 'any',
                'fields'         => 'ids',
            ) );
            $existing_titles = array();
            if ( ! empty( $existing_titles_raw ) ) {
                foreach ( $existing_titles_raw as $pid ) {
                    $t = get_the_title( $pid );
                    if ( ! empty( $t ) ) {
                        $existing_titles[] = $t;
                    }
                }
            }
            if ( ! empty( $existing_titles ) ) {
                $prompt .= "BẮT BUỘC TRÁNH TRÙNG LẶP TIÊU ĐỀ: Hệ thống đã có các bài viết mang tiêu đề dưới đây. Hãy đảm bảo 100% các tiêu đề (post_title) bạn sinh mới hoàn toàn độc đáo, sáng tạo, KHÔNG ĐƯỢC trùng lặp với danh sách sau:\n";
                $prompt .= json_encode( $existing_titles, JSON_UNESCAPED_UNICODE ) . "\n\n";
            }
        }

        if ( ! empty( $layout_template ) ) {
            $prompt .= "BẮT BUỘC NỘI DUNG CHI TIẾT (Trường 'post_content') của mỗi bài viết phải được viết theo đúng bố cục (layout) dưới đây. Hãy viết đầy đủ nội dung chi tiết lấp đầy các đề mục, không để lại placeholder hay text ghi chú:\n";
            $prompt .= $layout_template . "\n\n";
        }

        $prompt .= "YÊU CẦU ĐỘ DÀI & VĂN PHONG:\n";
        $prompt .= "- Độ dài bài viết: " . ( 'short' === $length ? 'Ngắn (~300-500 từ)' : ( 'long' === $length ? 'Dài chuẩn SEO (~1200-2000 từ)' : 'Vừa (~600-1000 từ)' ) ) . "\n";
        $prompt .= "- Văn phong: " . ( 'sales' === $tone ? 'Thuyết phục, tập trung bán hàng' : ( 'friendly' === $tone ? 'Thân thiện, chia sẻ kinh nghiệm' : ( 'news' === $tone ? 'Trang trọng, báo chí tin tức' : 'Chuyên nghiệp, chuẩn SEO' ) ) ) . "\n";
        $prompt .= "- Ngôn ngữ bài viết: " . ( 'en' === $lang ? 'Tiếng Anh (English)' : 'Tiếng Việt (Vietnamese)' ) . "\n\n";

        $prompt .= "YÊU CẦU QUAN TRỌNG:\n";
        $prompt .= "1. Nội dung phải hoàn toàn viết bằng " . ( 'en' === $lang ? 'Tiếng Anh (English)' : 'Tiếng Việt' ) . " phong phú, tự nhiên, không sáo rỗng.\n";
        $prompt .= "2. Đồng nhất ngữ nghĩa chủ đề (Semantic Theme Cohesion): Mỗi đối tượng (bài viết) trong mảng JSON được sinh ra phải tập trung vào một chủ đề hoặc kịch bản thực tế cụ thể. Tất cả các trường (Tiêu đề, Nội dung, ACF và mô tả ảnh tìm kiếm) của cùng một đối tượng phải liên quan chặt chẽ với nhau để tạo thành một bài viết hoàn chỉnh có nghĩa.\n";
        $prompt .= "3. Bắt buộc các trường có lựa chọn (choices) phải lấy giá trị từ danh sách lựa chọn quy định ở trên.\n";
        $prompt .= "4. Các trường dạng ảnh hoặc file (ví dụ: featured_image hoặc ACF image): Hãy viết mô tả ngắn gọn bằng tiếng Anh (ví dụ: \"vietnamese coffee shop\", \"modern minimalist living room\") để hệ thống tự động tìm kiếm hình ảnh thực tế chất lượng cao phù hợp.\n";
        $prompt .= "5. CHỈ TRẢ VỀ mã JSON nguyên bản, không nằm trong khối code markdown (không bắt đầu bằng ```json và không kết thúc bằng ```), không có văn bản giải thích nào khác ngoài chuỗi JSON.";

        $api_result = self::call_gemini_api_static( $prompt, $api_key, true );

        if ( is_wp_error( $api_result ) ) {
            return $api_result;
        }

        $raw_json = trim( $api_result );
        
        // Giải mã JSON phản hồi
        $parsed_rows = json_decode( $raw_json, true );

        if ( ! is_array( $parsed_rows ) ) {
            $clean_json = preg_replace('/^```(?:json)?/i', '', $raw_json);
            $clean_json = preg_replace('/```$/', '', $clean_json);
            $parsed_rows = json_decode( trim( $clean_json ), true );
            
            if ( ! is_array( $parsed_rows ) ) {
                return new WP_Error( 'json_invalid', 'AI không phản hồi đúng định dạng JSON Array hợp lệ. Vui lòng thử lại.' );
            }
        }

        // Hậu xử lý ảnh
        foreach ( $parsed_rows as &$row ) {
            if ( isset( $row['featured_image'] ) && ! filter_var( $row['featured_image'], FILTER_VALIDATE_URL ) ) {
                $kw = trim( $row['featured_image'], " ._-" );
                $row['featured_image'] = "https://loremflickr.com/800/600/" . urlencode( str_replace( ' ', ',', $kw ) ) . "?lock=" . rand(1, 1000);
            }
            foreach ( $fields as $field ) {
                $f_name = $field['name'];
                $f_type = $field['type'];
                if ( strpos( $f_type, 'image' ) !== false || strpos( $f_type, 'file' ) !== false ) {
                    if ( isset( $row[ $f_name ] ) && ! filter_var( $row[ $f_name ], FILTER_VALIDATE_URL ) ) {
                        $kw = trim( $row[ $f_name ], " ._-" );
                        $row[ $f_name ] = "https://loremflickr.com/800/600/" . urlencode( str_replace( ' ', ',', $kw ) ) . "?lock=" . rand(1, 1000);
                    }
                }
            }
        }

        return $parsed_rows;
    }

    /**
     * Lấy giá trị trường ACF một cách an toàn, tránh lỗi Fatal nếu ACF bị vô hiệu hóa
     */
    public static function get_acf_field_value( $field_name, $post_id ) {
        if ( function_exists( 'get_field' ) ) {
            return get_field( $field_name, $post_id );
        }
        return get_post_meta( $post_id, $field_name, true );
    }

    /**
     * Kiểm tra xem giá trị trường có thực sự trống không (bảo toàn 0 và false)
     */
    public static function is_value_empty( $val ) {
        if ( $val === null || $val === '' ) {
            return true;
        }
        if ( is_array( $val ) && empty( $val ) ) {
            return true;
        }
        return false;
    }

    /**
     * Lấy danh sách tất cả các trường ACF của một Post Type nhất định
     *
     * @param string $post_type Post Type cần lấy trường
     * @return array Danh sách trường ACF thu gọn
     */
    public static function get_acf_fields_for_post_type( $post_type ) {
        $fields = array();

        if ( ! function_exists( 'acf_get_field_groups' ) ) {
            return $fields;
        }

        // Lấy tất cả các nhóm trường ACF
        $groups = acf_get_field_groups();

        foreach ( $groups as $group ) {
            // Lấy quy tắc hiển thị (location rules) của nhóm này
            $locations = isset( $group['location'] ) ? $group['location'] : array();
            if ( empty( $locations ) && isset( $group['ID'] ) && $group['ID'] > 0 ) {
                $locations = acf_get_field_group_location( $group['ID'] );
            }
            
            $is_matched = false;

            if ( is_array( $locations ) ) {
                foreach ( $locations as $group_rules ) {
                    if ( ! is_array( $group_rules ) ) {
                        continue;
                    }
                    foreach ( $group_rules as $rule ) {
                        if ( isset( $rule['param'] ) && $rule['param'] === 'post_type' && isset( $rule['operator'] ) && $rule['operator'] === '==' ) {
                            if ( isset( $rule['value'] ) && $rule['value'] === $post_type ) {
                                $is_matched = true;
                                break;
                            }
                        }
                        // Nếu nhóm trường áp dụng cho "Mọi bài viết"
                        if ( isset( $rule['param'] ) && $rule['param'] === 'post_type' && isset( $rule['operator'] ) && $rule['operator'] === '==' ) {
                            if ( isset( $rule['value'] ) && $rule['value'] === 'post' && $post_type === 'post' ) {
                                $is_matched = true;
                                break;
                            }
                        }
                    }
                    if ( $is_matched ) {
                        break;
                    }
                }
            }

            // Nếu nhóm trường khớp với Post Type, lấy tất cả các trường trong nhóm đó
            if ( $is_matched ) {
                $group_fields = acf_get_fields( $group['key'] );
                if ( is_array( $group_fields ) ) {
                    foreach ( $group_fields as $gf ) {
                        $fields[] = array(
                            'name'    => $gf['name'],
                            'label'   => $gf['label'],
                            'type'    => $gf['type'],
                            'choices' => isset( $gf['choices'] ) ? $gf['choices'] : array(),
                            'multiple'=> isset( $gf['multiple'] ) ? $gf['multiple'] : false,
                            'key'     => $gf['key'],
                        );
                    }
                }
            }
        }

        return $fields;
    }

    /**
     * Phân tích cấu trúc bài viết mẫu để tìm vị trí ảnh (Image Slots)
     *
     * @param int $post_id ID bài viết mẫu
     * @return array|WP_Error Danh sách Image Slots hoặc lỗi
     */
    public static function analyze_template_structure( $post_id ) {
        $post = get_post( $post_id );
        if ( ! $post ) {
            return new WP_Error( 'invalid_post', __( 'Bài viết mẫu không tồn tại.', 'wp-acf-smart-importer' ) );
        }

        $content = $post->post_content;
        if ( empty( $content ) ) {
            return new WP_Error( 'empty_content', __( 'Bài viết mẫu không có nội dung.', 'wp-acf-smart-importer' ) );
        }

        $slots = array();
        $slot_index = 0;

        // Tìm tất cả các thẻ <img> và wrapper bao quanh chúng
        // Pattern 1: WordPress Block Image - <figure class="wp-block-image ..."><img .../></figure>
        // Pattern 2: Classic Editor - <img ... /> standalone hoặc trong <p>, <div>
        // Pattern 3: <figure><img .../><figcaption>...</figcaption></figure>

        // Sử dụng DOMDocument để parse HTML an toàn
        $dom = new DOMDocument();
        // Suppress warnings từ HTML không chuẩn
        libxml_use_internal_errors( true );
        $dom->loadHTML( '<?xml encoding="UTF-8"><div id="wpsai-root">' . $content . '</div>', LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD );
        libxml_clear_errors();

        $images = $dom->getElementsByTagName( 'img' );
        $processed_parents = array();

        foreach ( $images as $img ) {
            $slot = array(
                'index'       => $slot_index,
                'wrapper_tag' => '',
                'wrapper_class' => '',
                'img_class'   => $img->getAttribute( 'class' ) ?: '',
                'position'    => 'standalone', // standalone, after_heading, within_figure
                'nearby_heading' => '',
            );

            // Kiểm tra parent node
            $parent = $img->parentNode;
            if ( $parent && $parent->nodeName !== '#document' && $parent->getAttribute('id') !== 'wpsai-root' ) {
                $parent_tag = strtolower( $parent->nodeName );
                $parent_class = $parent->getAttribute( 'class' ) ?: '';

                if ( $parent_tag === 'figure' || $parent_tag === 'div' || $parent_tag === 'p' ) {
                    $slot['wrapper_tag'] = $parent_tag;
                    $slot['wrapper_class'] = $parent_class;

                    if ( $parent_tag === 'figure' ) {
                        $slot['position'] = 'within_figure';
                    }

                    // Kiểm tra grandparent
                    $grandparent = $parent->parentNode;
                    if ( $grandparent && $grandparent->nodeName !== '#document' && $grandparent->getAttribute('id') !== 'wpsai-root' ) {
                        $gp_tag = strtolower( $grandparent->nodeName );
                        $gp_class = $grandparent->getAttribute( 'class' ) ?: '';
                        if ( strpos( $gp_class, 'wp-block-image' ) !== false ) {
                            $slot['wrapper_tag'] = $gp_tag;
                            $slot['wrapper_class'] = $gp_class;
                        }
                    }
                }
            }

            // Tìm heading gần nhất phía trước ảnh
            $prev_sibling = $parent ? $parent->previousSibling : $img->previousSibling;
            while ( $prev_sibling ) {
                if ( $prev_sibling->nodeType === XML_ELEMENT_NODE ) {
                    $tag = strtolower( $prev_sibling->nodeName );
                    if ( in_array( $tag, array( 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' ) ) ) {
                        $slot['nearby_heading'] = $prev_sibling->textContent;
                        $slot['position'] = 'after_heading';
                        break;
                    }
                }
                $prev_sibling = $prev_sibling->previousSibling;
            }

            $slots[] = $slot;
            $slot_index++;
        }

        // Thông tin tổng hợp về bài mẫu
        $result = array(
            'post_id'     => $post_id,
            'post_title'  => $post->post_title,
            'total_images' => count( $slots ),
            'slots'       => $slots,
            'headings'    => array(),
        );

        // Lấy danh sách heading trong bài
        $headings = $dom->getElementsByTagName( 'h2' );
        foreach ( $headings as $h ) {
            $result['headings'][] = $h->textContent;
        }
        $h3s = $dom->getElementsByTagName( 'h3' );
        foreach ( $h3s as $h ) {
            $result['headings'][] = $h->textContent;
        }

        return $result;
    }

    /**
     * Chèn ảnh từ kho ảnh (Image Pool) vào nội dung bài viết
     *
     * @param string $content     Nội dung HTML đã sinh bởi AI
     * @param array  $image_ids   Danh sách attachment IDs từ kho ảnh
     * @param array  $slots       Danh sách Image Slots từ phân tích bài mẫu (có thể rỗng)
     * @param string $mode        Chế độ phân bổ: 'sequential', 'random', 'cycle'
     * @param bool   $set_featured Có gán ảnh đầu tiên làm Featured Image không
     * @return array Kết quả gồm 'content' (đã chèn ảnh) và 'featured_image_id' (nếu có)
     */
    public static function inject_images_into_content( $content, $image_ids, $slots = array(), $mode = 'sequential', $set_featured = true ) {
        if ( empty( $image_ids ) || empty( $content ) ) {
            return array(
                'content'            => $content,
                'featured_image_id'  => 0,
            );
        }

        $featured_image_id = 0;
        $pool = $image_ids; // Copy để xử lý

        // Nếu set_featured = true, lấy ảnh đầu tiên làm Featured Image
        if ( $set_featured && ! empty( $pool ) ) {
            $featured_image_id = intval( array_shift( $pool ) );
        }

        // Nếu không còn ảnh trong pool sau khi lấy featured
        if ( empty( $pool ) ) {
            return array(
                'content'            => $content,
                'featured_image_id'  => $featured_image_id,
            );
        }

        // Xác định vị trí chèn ảnh
        $insert_positions = array();

        if ( ! empty( $slots ) && is_array( $slots ) ) {
            // Chế độ 1: Dựa vào bài mẫu - chèn ảnh theo vị trí trong template
            // Tìm các heading trong content AI để chèn ảnh sau chúng
            foreach ( $slots as $slot ) {
                if ( ! empty( $slot['nearby_heading'] ) ) {
                    $insert_positions[] = array(
                        'type'    => 'after_heading',
                        'heading' => $slot['nearby_heading'],
                        'wrapper' => $slot['wrapper_tag'],
                        'class'   => $slot['wrapper_class'],
                    );
                } else {
                    $insert_positions[] = array(
                        'type' => 'auto',
                    );
                }
            }
        }

        // Nếu không có slots từ bài mẫu hoặc slots rỗng, dùng chế độ tự động
        if ( empty( $insert_positions ) ) {
            // Tìm tất cả heading h2, h3 trong content
            preg_match_all( '/<h[23][^>]*>.*?<\/h[23]>/si', $content, $heading_matches, PREG_OFFSET_MATCH );

            if ( ! empty( $heading_matches[0] ) ) {
                foreach ( $heading_matches[0] as $match ) {
                    $insert_positions[] = array(
                        'type'   => 'after_heading_auto',
                        'offset' => $match[1] + strlen( $match[0] ),
                    );
                }
            }
        }

        // Nếu vẫn không tìm được vị trí chèn, chèn ảnh sau mỗi đoạn </p>
        if ( empty( $insert_positions ) ) {
            preg_match_all( '/<\/p>/i', $content, $p_matches, PREG_OFFSET_MATCH );
            if ( ! empty( $p_matches[0] ) ) {
                // Chèn sau mỗi 2 đoạn văn
                $p_count = 0;
                foreach ( $p_matches[0] as $match ) {
                    $p_count++;
                    if ( $p_count % 2 === 0 ) {
                        $insert_positions[] = array(
                            'type'   => 'after_paragraph',
                            'offset' => $match[1] + strlen( $match[0] ),
                        );
                    }
                }
            }
        }

        if ( empty( $insert_positions ) ) {
            // Fallback: chèn ảnh cuối nội dung
            $insert_positions[] = array(
                'type'   => 'append',
                'offset' => strlen( $content ),
            );
        }

        // Phân bổ ảnh cho các vị trí dựa theo mode
        $assigned_images = self::distribute_images( $pool, count( $insert_positions ), $mode );

        // Thực hiện chèn ảnh vào content
        // Sắp xếp positions theo offset giảm dần để chèn từ cuối lên (tránh offset bị lệch)
        if ( isset( $insert_positions[0]['offset'] ) ) {
            // Chế độ offset-based (auto)
            usort( $insert_positions, function ( $a, $b ) {
                $oa = isset( $a['offset'] ) ? $a['offset'] : 0;
                $ob = isset( $b['offset'] ) ? $b['offset'] : 0;
                return $ob - $oa; // Giảm dần
            } );

            // Re-distribute sau khi sort
            $assigned_images = self::distribute_images( $pool, count( $insert_positions ), $mode );

            foreach ( $insert_positions as $idx => $pos ) {
                if ( ! isset( $assigned_images[ $idx ] ) ) {
                    continue;
                }

                $img_id = $assigned_images[ $idx ];
                $img_url = wp_get_attachment_image_url( $img_id, 'large' );
                $img_alt = get_post_meta( $img_id, '_wp_attachment_image_alt', true );
                if ( empty( $img_alt ) ) {
                    $img_alt = get_the_title( $img_id );
                }

                if ( $img_url ) {
                    $img_html = "\n" . '<figure class="wp-block-image size-large wpsai-auto-image">' .
                        '<img src="' . esc_url( $img_url ) . '" alt="' . esc_attr( $img_alt ) . '" class="wp-image-' . intval( $img_id ) . '"/>' .
                        '</figure>' . "\n";

                    $offset = isset( $pos['offset'] ) ? $pos['offset'] : strlen( $content );
                    $content = substr_replace( $content, $img_html, $offset, 0 );
                }
            }
        } else {
            // Chế độ heading-based (từ bài mẫu) - chèn sau các heading tương tự
            $dom = new DOMDocument();
            libxml_use_internal_errors( true );
            $dom->loadHTML( '<?xml encoding="UTF-8"><div id="wpsai-root">' . $content . '</div>', LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD );
            libxml_clear_errors();

            $headings = array();
            foreach ( array( 'h2', 'h3' ) as $tag ) {
                $elements = $dom->getElementsByTagName( $tag );
                foreach ( $elements as $el ) {
                    $headings[] = $el;
                }
            }

            $img_idx = 0;
            foreach ( $headings as $heading_node ) {
                if ( $img_idx >= count( $assigned_images ) ) {
                    break;
                }

                $img_id = $assigned_images[ $img_idx ];
                $img_url = wp_get_attachment_image_url( $img_id, 'large' );
                $img_alt = get_post_meta( $img_id, '_wp_attachment_image_alt', true );
                if ( empty( $img_alt ) ) {
                    $img_alt = get_the_title( $img_id );
                }

                if ( $img_url ) {
                    // Tạo element figure > img
                    $figure = $dom->createElement( 'figure' );
                    $figure->setAttribute( 'class', 'wp-block-image size-large wpsai-auto-image' );

                    $img_el = $dom->createElement( 'img' );
                    $img_el->setAttribute( 'src', $img_url );
                    $img_el->setAttribute( 'alt', $img_alt );
                    $img_el->setAttribute( 'class', 'wp-image-' . intval( $img_id ) );
                    $figure->appendChild( $img_el );

                    // Chèn figure sau heading node
                    $next = $heading_node->nextSibling;
                    if ( $next ) {
                        $heading_node->parentNode->insertBefore( $figure, $next );
                    } else {
                        $heading_node->parentNode->appendChild( $figure );
                    }
                }

                $img_idx++;
            }

            // Lấy lại content từ DOM
            $root = $dom->getElementById( 'wpsai-root' );
            if ( $root ) {
                $inner_html = '';
                foreach ( $root->childNodes as $child ) {
                    $inner_html .= $dom->saveHTML( $child );
                }
                $content = $inner_html;
            }
        }

        return array(
            'content'            => $content,
            'featured_image_id'  => $featured_image_id,
        );
    }

    /**
     * Phân bổ ảnh cho các vị trí dựa theo chế độ
     *
     * @param array  $pool    Danh sách attachment IDs
     * @param int    $count   Số vị trí cần phân bổ
     * @param string $mode    Chế độ: sequential, random, cycle
     * @return array Mảng attachment IDs đã phân bổ
     */
    private static function distribute_images( $pool, $count, $mode = 'sequential' ) {
        if ( empty( $pool ) || $count <= 0 ) {
            return array();
        }

        $result = array();

        switch ( $mode ) {
            case 'random':
                for ( $i = 0; $i < $count; $i++ ) {
                    $result[] = $pool[ array_rand( $pool ) ];
                }
                break;

            case 'cycle':
            case 'sequential':
            default:
                for ( $i = 0; $i < $count; $i++ ) {
                    $result[] = $pool[ $i % count( $pool ) ];
                }
                break;
        }

        return $result;
    }

    /**
     * Tự động khám phá danh sách các model khả dụng cho API Key hiện tại
     */
    private static function get_available_gemini_endpoints( $api_key ) {
        $cache_key = 'wpsai_endpoints_' . substr( md5( $api_key ), 0, 10 );
        $cached = get_transient( $cache_key );
        if ( ! empty( $cached ) && is_array( $cached ) ) {
            return $cached;
        }

        $endpoints = array();

        // 1. Thử gọi API ListModels để lấy danh sách model thực tế được hỗ trợ
        $list_url = 'https://generativelanguage.googleapis.com/v1beta/models?key=' . $api_key;
        $response = wp_remote_get( $list_url, array( 'timeout' => 15 ) );
        if ( ! is_wp_error( $response ) && 200 === wp_remote_retrieve_response_code( $response ) ) {
            $body = json_decode( wp_remote_retrieve_body( $response ), true );
            if ( ! empty( $body['models'] ) && is_array( $body['models'] ) ) {
                foreach ( $body['models'] as $m ) {
                    $methods = isset( $m['supportedGenerationMethods'] ) ? $m['supportedGenerationMethods'] : array();
                    if ( in_array( 'generateContent', $methods ) ) {
                        $model_name = str_replace( 'models/', '', $m['name'] );
                        // Ưu tiên các model flash trước
                        if ( strpos( $model_name, 'flash' ) !== false ) {
                            array_unshift( $endpoints, array(
                                'url'   => 'https://generativelanguage.googleapis.com/v1beta/models/' . $model_name . ':generateContent?key=' . $api_key,
                                'model' => $model_name,
                                'ver'   => 'v1beta'
                            ) );
                        } else {
                            $endpoints[] = array(
                                'url'   => 'https://generativelanguage.googleapis.com/v1beta/models/' . $model_name . ':generateContent?key=' . $api_key,
                                'model' => $model_name,
                                'ver'   => 'v1beta'
                            );
                        }
                    }
                }
            }
        }

        // 2. Nếu không lấy được qua ListModels, dùng danh sách fallback chuẩn
        if ( empty( $endpoints ) ) {
            $fallback_models = array(
                'gemini-3.6-flash',
                'gemini-3.6-pro',
                'gemini-2.5-flash',
                'gemini-2.0-flash',
                'gemini-1.5-flash'
            );
            foreach ( $fallback_models as $fm ) {
                $endpoints[] = array(
                    'url'   => 'https://generativelanguage.googleapis.com/v1beta/models/' . $fm . ':generateContent?key=' . $api_key,
                    'model' => $fm,
                    'ver'   => 'v1beta'
                );
            }
        }

        set_transient( $cache_key, $endpoints, 1800 );
        return $endpoints;
    }

    /**
     * Helper tĩnh gọi API Gemini có khả năng quay vòng model và endpoint dự phòng
     */
    private static function call_gemini_api_static( $prompt, $api_key, $response_mime_json = false ) {
        if ( function_exists( 'set_time_limit' ) ) {
            @set_time_limit( 180 );
        }

        $endpoints = self::get_available_gemini_endpoints( $api_key );

        $error_log = array();
        foreach ( $endpoints as $ep ) {
            $body = array(
                'contents' => array(
                    array(
                        'parts' => array(
                            array( 'text' => $prompt )
                        )
                    )
                )
            );

            if ( $response_mime_json && strpos( $ep['url'], 'v1beta' ) !== false ) {
                $body['generationConfig'] = array(
                    'responseMimeType' => 'application/json'
                );
            }

            $response = wp_remote_post( $ep['url'], array(
                'headers'   => array( 'Content-Type' => 'application/json' ),
                'body'      => json_encode( $body, JSON_UNESCAPED_UNICODE ),
                'timeout'   => 90,
            ) );

            if ( is_wp_error( $response ) ) {
                $error_log[] = "[{$ep['model']} ({$ep['ver']})] WP_Error: " . $response->get_error_message();
                continue;
            }

            $code = wp_remote_retrieve_response_code( $response );
            if ( 200 !== $code ) {
                $res_body = wp_remote_retrieve_body( $response );
                $error_log[] = "[{$ep['model']} ({$ep['ver']})] HTTP {$code}: " . $res_body;
                continue;
            }

            $res_body = wp_remote_retrieve_body( $response );
            $res_data = json_decode( $res_body, true );

            if ( ! empty( $res_data['candidates'][0]['content']['parts'][0]['text'] ) ) {
                return $res_data['candidates'][0]['content']['parts'][0]['text'];
            }
        }

        return new WP_Error( 'gemini_failed', __( 'Tất cả các models/endpoints kết nối Gemini đều thất bại. Nhật ký lỗi chi tiết: ', 'wp-acf-smart-importer' ) . implode( ' --- ', $error_log ) );
    }
}
