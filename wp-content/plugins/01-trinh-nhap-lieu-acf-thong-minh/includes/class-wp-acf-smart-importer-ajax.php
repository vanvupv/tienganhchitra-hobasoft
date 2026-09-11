<?php
/**
 * Lớp WP_ACF_Smart_Importer_Ajax
 * Xử lý tất cả các yêu cầu AJAX giao tiếp giữa Frontend và WP Database.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_ACF_Smart_Importer_Ajax {

    /**
     * Khởi tạo các hook AJAX
     */
    public function __construct() {
        // Đăng ký AJAX hooks
        add_action( 'wp_ajax_wpsai_get_post_types_and_fields', array( $this, 'get_post_types_and_fields' ) );
        add_action( 'wp_ajax_wpsai_get_posts_by_post_type', array( $this, 'get_posts_by_post_type' ) );
        add_action( 'wp_ajax_wpsai_import_row', array( $this, 'import_row' ) );
        add_action( 'wp_ajax_wpsai_bulk_excel_update_row', array( $this, 'bulk_excel_update_row' ) );
        add_action( 'wp_ajax_wpsai_generate_mock_data', array( $this, 'generate_mock_data' ) );
        add_action( 'wp_ajax_wpsai_save_settings', array( $this, 'save_settings' ) );
        add_action( 'wp_ajax_wpsai_create_blank_post', array( $this, 'create_blank_post' ) );
        add_action( 'wp_ajax_wpsai_scan_post_fields', array( $this, 'scan_post_fields' ) );
        add_action( 'wp_ajax_wpsai_update_post_fields_directly', array( $this, 'update_post_fields_directly' ) );
        add_action( 'wp_ajax_wpsai_get_posts_for_bulk_images', array( $this, 'get_posts_for_bulk_images' ) );
        add_action( 'wp_ajax_wpsai_set_post_thumbnail_ajax', array( $this, 'set_post_thumbnail_ajax' ) );
        add_action( 'wp_ajax_wpsai_get_posts_for_export', array( $this, 'get_posts_for_export' ) );
        add_action( 'wp_ajax_wpsai_get_export_data', array( $this, 'get_export_data' ) );
        add_action( 'wp_ajax_wpsai_create_zip_export', array( $this, 'create_zip_export' ) );
        add_action( 'wp_ajax_wpsai_get_taxonomies_for_post_type', array( $this, 'get_taxonomies_for_post_type' ) );
        add_action( 'wp_ajax_wpsai_get_terms_by_taxonomy', array( $this, 'get_terms_by_taxonomy' ) );
        add_action( 'wp_ajax_wpsai_assign_taxonomy_terms_ajax', array( $this, 'assign_taxonomy_terms_ajax' ) );
        add_action( 'wp_ajax_wpsai_scrape_preview', array( $this, 'scrape_preview' ) );
        add_action( 'wp_ajax_wpsai_scrape_and_import', array( $this, 'scrape_and_import' ) );
        add_action( 'wp_ajax_wpsai_bulk_ai_generate', array( $this, 'bulk_ai_generate' ) );
        add_action( 'wp_ajax_wpsai_analyze_template_post', array( $this, 'analyze_template_post' ) );
        add_action( 'wp_ajax_wpsai_ai_inject_images_and_import', array( $this, 'ai_inject_images_and_import' ) );
        // Project Documentation Manager hooks
        add_action( 'wp_ajax_wpsai_get_project_docs', array( $this, 'get_project_docs' ) );
        add_action( 'wp_ajax_wpsai_save_project_docs', array( $this, 'save_project_docs' ) );
        add_action( 'wp_ajax_wpsai_git_get_commits', array( $this, 'git_get_commits' ) );
        add_action( 'wp_ajax_wpsai_ai_describe_snippet', array( $this, 'ai_describe_snippet' ) );
        add_action( 'wp_ajax_wpsai_export_docs_markdown', array( $this, 'export_docs_markdown' ) );
        add_action( 'wp_ajax_wpsai_get_post_titles', array( $this, 'get_post_titles' ) );
        add_action( 'wp_ajax_wpsai_update_post_title', array( $this, 'update_post_title' ) );
        add_action( 'wp_ajax_wpsai_translate_post_titles', array( $this, 'translate_post_titles' ) );
        add_action( 'wp_ajax_wpsai_test_gemini_key', array( $this, 'test_gemini_key' ) );
        // Snapshot Data Repository hooks
        add_action( 'wp_ajax_wpsai_snapshot_scan', array( $this, 'snapshot_scan' ) );
        add_action( 'wp_ajax_wpsai_snapshot_save', array( $this, 'snapshot_save' ) );
        add_action( 'wp_ajax_wpsai_snapshot_list', array( $this, 'snapshot_list' ) );
        add_action( 'wp_ajax_wpsai_snapshot_detail', array( $this, 'snapshot_detail' ) );
        add_action( 'wp_ajax_wpsai_snapshot_restore', array( $this, 'snapshot_restore' ) );
        add_action( 'wp_ajax_wpsai_snapshot_delete', array( $this, 'snapshot_delete' ) );
        // Tree Repository hooks
        add_action( 'wp_ajax_wpsai_tree_get_manifest', array( $this, 'tree_get_manifest' ) );
        add_action( 'wp_ajax_wpsai_tree_scan_and_save_node', array( $this, 'tree_scan_and_save_node' ) );
        add_action( 'wp_ajax_wpsai_tree_get_chunk_data', array( $this, 'tree_get_chunk_data' ) );
    }

    /**
     * Bảo mật & Kiểm tra quyền hạn
     */
    private function verify_security() {
        if ( ! current_user_can( 'manage_options' ) ) {
            wp_send_json_error( array( 'message' => __( 'Bạn không có quyền thực hiện hành động này.', 'wp-acf-smart-importer' ) ) );
        }
        if ( ! isset( $_POST['nonce'] ) || ! wp_verify_nonce( $_POST['nonce'], 'wpsai_import_nonce_action' ) ) {
            wp_send_json_error( array( 'message' => __( 'Yêu cầu bảo mật không hợp lệ (Nonce expired).', 'wp-acf-smart-importer' ) ) );
        }
    }

    /**
     * Lấy danh sách bài viết thuộc Post Type để làm tham chiếu sinh dữ liệu hoặc cập nhật
     */
    public function get_posts_by_post_type() {
        $this->verify_security();
        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';

        $posts = get_posts( array(
            'post_type'      => $post_type,
            'posts_per_page' => 100,
            'post_status'    => 'any',
        ) );

        $result = array();
        foreach ( $posts as $post ) {
            $result[] = array(
                'id'    => $post->ID,
                'title' => $post->post_title . ' (ID: ' . $post->ID . ')',
            );
        }

        wp_send_json_success( $result );
    }

    /**
     * Lấy danh sách Custom Post Types và các trường đích (gồm cả ACF)
     */
    public function get_post_types_and_fields() {
        $this->verify_security();

        $post_types = get_post_types( array( 'public' => true ), 'objects' );
        $result = array();

        // Danh sách các trường mặc định của WordPress (Bổ sung post_id để hỗ trợ cập nhật bài viết cũ)
        $wp_fields = array(
            array( 'name' => 'post_id', 'label' => __( 'ID bài viết (Nếu muốn cập nhật bài cũ)', 'wp-acf-smart-importer' ), 'type' => 'wp_core' ),
            array( 'name' => 'post_title', 'label' => __( 'Tiêu đề bài viết (Title)', 'wp-acf-smart-importer' ), 'type' => 'wp_core' ),
            array( 'name' => 'post_content', 'label' => __( 'Nội dung chi tiết (Content)', 'wp-acf-smart-importer' ), 'type' => 'wp_core' ),
            array( 'name' => 'post_excerpt', 'label' => __( 'Mô tả ngắn (Excerpt)', 'wp-acf-smart-importer' ), 'type' => 'wp_core' ),
            array( 'name' => 'post_date', 'label' => __( 'Ngày đăng bài (Date)', 'wp-acf-smart-importer' ), 'type' => 'wp_core' ),
            array( 'name' => 'featured_image', 'label' => __( 'Ảnh đại diện (Featured Image)', 'wp-acf-smart-importer' ), 'type' => 'wp_core' ),
        );

        foreach ( $post_types as $slug => $obj ) {
            // Loại bỏ các post types hệ thống không cần thiết
            if ( in_array( $slug, array( 'attachment', 'revision', 'nav_menu_item', 'custom_css', 'customize_changeset', 'oembed_cache', 'user_request', 'wp_block', 'wp_template', 'wp_template_part', 'wp_navigation' ) ) ) {
                continue;
            }

            // Lấy các trường ACF
            $acf_fields = WP_ACF_Smart_Importer_Generator::get_acf_fields_for_post_type( $slug );
            
            $formatted_acf = array();
            foreach ( $acf_fields as $f ) {
                $formatted_acf[] = array(
                    'name'  => 'acf_' . $f['name'],
                    'label' => '[ACF] ' . $f['label'] . ' (' . $f['name'] . ')',
                    'type'  => $f['type'],
                );
            }

            $result[] = array(
                'slug'       => $slug,
                'label'      => $obj->label . ' (' . $slug . ')',
                'core_fields'=> $wp_fields,
                'acf_fields' => $formatted_acf,
            );
        }

        wp_send_json_success( $result );
    }

    /**
     * Nhập một dòng dữ liệu thô (gọi theo Batch từ client)
     */
    public function import_row() {
        $this->verify_security();

        $row         = isset( $_POST['row'] ) ? map_deep( $_POST['row'], 'sanitize_text_field' ) : array();
        $mapping     = isset( $_POST['mapping'] ) ? map_deep( $_POST['mapping'], 'sanitize_text_field' ) : array();
        $post_type   = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $post_status = isset( $_POST['post_status'] ) ? sanitize_text_field( $_POST['post_status'] ) : 'draft';

        if ( empty( $row ) || empty( $mapping ) ) {
            wp_send_json_error( array( 'message' => __( 'Thiếu dữ liệu dòng hoặc sơ đồ ánh xạ.', 'wp-acf-smart-importer' ) ) );
        }

        $post_id = WP_ACF_Smart_Importer_Engine::import_single_row( $row, $mapping, $post_type, $post_status );

        if ( is_wp_error( $post_id ) ) {
            wp_send_json_error( array( 'message' => $post_id->get_error_message() ) );
        }

        wp_send_json_success( array(
            'post_id'   => $post_id,
            'title'     => get_the_title( $post_id ),
            'permalink' => get_permalink( $post_id ),
            'edit_url'  => get_edit_post_link( $post_id, '' ),
        ) );
    }
 
    /**
     * Cập nhật một bài viết từ dữ liệu Excel hàng loạt
     */
    public function bulk_excel_update_row() {
        $this->verify_security();
 
        $post_id        = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0;
        $post_title     = isset( $_POST['post_title'] ) ? sanitize_text_field( $_POST['post_title'] ) : '';
        $post_content   = isset( $_POST['post_content'] ) ? wp_kses_post( $_POST['post_content'] ) : '';
        $original_url   = isset( $_POST['original_url'] ) ? esc_url_raw( $_POST['original_url'] ) : '';
        $featured_image = isset( $_POST['featured_image'] ) ? esc_url_raw( $_POST['featured_image'] ) : '';
 
        if ( ! $post_id || ! get_post( $post_id ) ) {
            wp_send_json_error( array( 'message' => __( 'ID bài viết không hợp lệ.', 'wp-acf-smart-importer' ) ) );
        }
 
        $post_data = array(
            'ID' => $post_id,
        );
 
        if ( ! empty( $post_title ) ) {
            $post_data['post_title'] = $post_title;
        }
 
        if ( ! empty( $post_content ) ) {
            $post_data['post_content'] = $post_content;
        }
 
        if ( count( $post_data ) > 1 ) {
            $updated = wp_update_post( $post_data );
            if ( is_wp_error( $updated ) ) {
                wp_send_json_error( array( 'message' => $updated->get_error_message() ) );
            }
        }
 
        // Cập nhật Meta original_url
        if ( ! empty( $original_url ) ) {
            update_post_meta( $post_id, 'original_url', $original_url );
        }
 
        // Tải ảnh đại diện nếu có
        $thumb_url = '';
        if ( ! empty( $featured_image ) ) {
            $attachment_id = WP_ACF_Smart_Importer_Engine::handle_media_import( $featured_image, $post_id );
            if ( $attachment_id && ! is_wp_error( $attachment_id ) ) {
                set_post_thumbnail( $post_id, $attachment_id );
                $thumb_url = wp_get_attachment_image_url( $attachment_id, 'thumbnail' );
            }
        }
 
        if ( empty( $thumb_url ) ) {
            $thumb_id = get_post_thumbnail_id( $post_id );
            if ( $thumb_id ) {
                $thumb_url = wp_get_attachment_image_url( $thumb_id, 'thumbnail' );
            }
        }
 
        wp_send_json_success( array(
            'post_id'   => $post_id,
            'thumb_url' => $thumb_url,
        ) );
    }

    /**
     * Sinh dữ liệu ảo (Mock Data)
     */
    public function generate_mock_data() {
        $this->verify_security();

        try {
            $post_type   = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
            $count       = isset( $_POST['count'] ) ? intval( $_POST['count'] ) : 10;
            $mode        = isset( $_POST['mode'] ) ? sanitize_text_field( $_POST['mode'] ) : 'rule';
            $ref_post_id = isset( $_POST['ref_post_id'] ) ? intval( $_POST['ref_post_id'] ) : 0;
            $gen_type    = isset( $_POST['gen_type'] ) ? sanitize_text_field( $_POST['gen_type'] ) : 'new';
            $user_topic  = isset( $_POST['topic'] ) ? sanitize_textarea_field( wp_unslash( $_POST['topic'] ) ) : '';
            $length      = isset( $_POST['length'] ) ? sanitize_text_field( $_POST['length'] ) : 'medium';
            $tone        = isset( $_POST['tone'] ) ? sanitize_text_field( $_POST['tone'] ) : 'seo';
            $lang        = isset( $_POST['lang'] ) ? sanitize_text_field( $_POST['lang'] ) : 'vi';
            
            $fields_raw  = isset( $_POST['fields'] ) ? wp_unslash( $_POST['fields'] ) : '';
            $fields      = ! empty( $fields_raw ) ? json_decode( $fields_raw, true ) : array();

            if ( $count < 1 || $count > 100 ) {
                wp_send_json_error( array( 'message' => __( 'Số lượng sinh tối thiểu là 1 và tối đa là 100 bài viết.', 'wp-acf-smart-importer' ) ) );
            }

            if ( 'ai' === $mode ) {
                $api_key = get_option( 'wpsai_gemini_api_key', '' );
                if ( empty( $api_key ) ) {
                    wp_send_json_error( array( 'message' => __( 'Lỗi: Vui lòng cấu hình Gemini API Key trước khi sử dụng tính năng AI.', 'wp-acf-smart-importer' ) ) );
                }
                $data = WP_ACF_Smart_Importer_Generator::generate_ai_based_data( $post_type, $count, $api_key, $ref_post_id, $gen_type, $fields, $user_topic, array(), '', array(), $length, $tone, $lang );
            } else {
                $data = WP_ACF_Smart_Importer_Generator::generate_rule_based_data( $post_type, $count, $ref_post_id, $gen_type, $fields, $user_topic, $length, $tone, $lang );
            }

            if ( is_wp_error( $data ) ) {
                wp_send_json_error( array( 'message' => $data->get_error_message() ) );
            }

            wp_send_json_success( array(
                'rows'    => $data,
                'message' => sprintf( __( 'Đã sinh thành công %d bản ghi mẫu thử nghiệm!', 'wp-acf-smart-importer' ), count( $data ) ),
            ) );
        } catch ( Throwable $t ) {
            wp_send_json_error( array( 'message' => 'Lỗi xử lý sinh dữ liệu: ' . $t->getMessage() ) );
        }
    }

    /**
     * Sinh dữ liệu mẫu hàng loạt bằng AI (Gemini) theo Batch
     */
    public function bulk_ai_generate() {
        $this->verify_security();

        $post_type          = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $count              = isset( $_POST['count'] ) ? intval( $_POST['count'] ) : 5;
        $user_topic         = isset( $_POST['user_topic'] ) ? sanitize_textarea_field( wp_unslash( $_POST['user_topic'] ) ) : '';
        $gen_type           = isset( $_POST['gen_type'] ) ? sanitize_text_field( $_POST['gen_type'] ) : 'new';
        
        $selected_post_ids  = array();
        if ( isset( $_POST['selected_post_ids'] ) && is_array( $_POST['selected_post_ids'] ) ) {
            $selected_post_ids = array_map( 'intval', $_POST['selected_post_ids'] );
        }

        $fields_raw         = isset( $_POST['fields'] ) ? wp_unslash( $_POST['fields'] ) : '';
        $fields             = ! empty( $fields_raw ) ? json_decode( $fields_raw, true ) : array();

        $layout_template    = isset( $_POST['layout_template'] ) ? wp_kses_post( wp_unslash( $_POST['layout_template'] ) ) : '';
        
        $custom_titles      = array();
        if ( isset( $_POST['custom_titles'] ) && is_array( $_POST['custom_titles'] ) ) {
            $custom_titles = array_map( 'sanitize_text_field', $_POST['custom_titles'] );
        }

        if ( $count < 1 || $count > 20 ) {
            wp_send_json_error( array( 'message' => __( 'Số lượng sinh mỗi đợt (batch) tối đa là 20.', 'wp-acf-smart-importer' ) ) );
        }

        $api_key = get_option( 'wpsai_gemini_api_key', '' );
        if ( empty( $api_key ) ) {
            wp_send_json_error( array( 'message' => __( 'Lỗi: Vui lòng cấu hình Gemini API Key trong tab Cấu Hình trước.', 'wp-acf-smart-importer' ) ) );
        }

        // Gọi generator model
        $data = WP_ACF_Smart_Importer_Generator::generate_ai_based_data(
            $post_type,
            $count,
            $api_key,
            0, // ref_post_id
            $gen_type,
            $fields,
            $user_topic,
            $selected_post_ids,
            $layout_template,
            $custom_titles
        );

        if ( is_wp_error( $data ) ) {
            wp_send_json_error( array( 'message' => $data->get_error_message() ) );
        }

        wp_send_json_success( array(
            'rows'    => $data,
            'message' => sprintf( __( 'Đã sinh thành công %d bản ghi từ AI!', 'wp-acf-smart-importer' ), count( $data ) ),
        ) );
    }

    /**
     * Lưu cài đặt API Key
     */
    public function save_settings() {
        $this->verify_security();

        $gemini_key = isset( $_POST['gemini_key'] ) ? sanitize_text_field( $_POST['gemini_key'] ) : '';
        
        update_option( 'wpsai_gemini_api_key', $gemini_key );

        wp_send_json_success( array( 'message' => __( 'Đã lưu cài đặt API Key thành công.', 'wp-acf-smart-importer' ) ) );
    }

    /**
     * Kiểm tra kết nối Gemini API Key trực tiếp
     */
    public function test_gemini_key() {
        $this->verify_security();

        $key = isset( $_POST['gemini_key'] ) ? sanitize_text_field( $_POST['gemini_key'] ) : '';
        if ( empty( $key ) ) {
            $key = get_option( 'wpsai_gemini_api_key', '' );
        }

        if ( empty( $key ) ) {
            wp_send_json_error( array( 'message' => __( 'Vui lòng nhập API Key để kiểm tra.', 'wp-acf-smart-importer' ) ) );
        }

        $start_time = microtime( true );
        $res = $this->call_gemini_api( 'Xin chào! Hãy phản hồi ngắn: "Kết nối API Gemini thành công!"', $key, false );
        $elapsed = round( ( microtime( true ) - $start_time ) * 1000 );

        if ( is_wp_error( $res ) ) {
            wp_send_json_error( array(
                'message' => __( 'Kiểm tra API thất bại: ', 'wp-acf-smart-importer' ) . $res->get_error_message(),
                'latency' => $elapsed
            ) );
        }

        wp_send_json_success( array(
            'message'  => __( 'Kết nối API Gemini THÀNH CÔNG!', 'wp-acf-smart-importer' ),
            'response' => trim( $res ),
            'latency'  => $elapsed . ' ms'
        ) );
    }

    /**
     * Tạo bài viết rỗng mới
     */
    public function create_blank_post() {
        $this->verify_security();
        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';

        $post_id = wp_insert_post( array(
            'post_title'  => '(Bài viết mới rỗng)',
            'post_type'   => $post_type,
            'post_status' => 'draft',
        ) );

        if ( is_wp_error( $post_id ) ) {
            wp_send_json_error( array( 'message' => $post_id->get_error_message() ) );
        }

        wp_send_json_success( array(
            'post_id' => $post_id,
            'title'   => '(Bài viết mới rỗng) (ID: ' . $post_id . ')',
        ) );
    }

    /**
     * Quét các trường của bài viết
     */
    public function scan_post_fields() {
        $this->verify_security();
        $post_id = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0;
        if ( ! $post_id || ! get_post( $post_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Bài viết không tồn tại.', 'wp-acf-smart-importer' ) ) );
        }

        $post = get_post( $post_id );
        $post_type = $post->post_type;

        // 1. Các trường core
        $core_fields = array(
            array(
                'name'          => 'post_title',
                'label'         => __( 'Tiêu đề bài viết (Title)', 'wp-acf-smart-importer' ),
                'type'          => 'wp_core',
                'current_value' => $post->post_title,
                'is_acf'        => false,
                'is_system'     => false,
            ),
            array(
                'name'          => 'post_name',
                'label'         => __( 'Đường dẫn tĩnh (Slug)', 'wp-acf-smart-importer' ),
                'type'          => 'wp_core',
                'current_value' => $post->post_name,
                'is_acf'        => false,
                'is_system'     => false,
            ),
            array(
                'name'          => 'post_content',
                'label'         => __( 'Nội dung chi tiết (Content)', 'wp-acf-smart-importer' ),
                'type'          => 'wp_core',
                'current_value' => $post->post_content,
                'is_acf'        => false,
                'is_system'     => false,
            ),
            array(
                'name'          => 'post_excerpt',
                'label'         => __( 'Mô tả ngắn (Excerpt)', 'wp-acf-smart-importer' ),
                'type'          => 'wp_core',
                'current_value' => $post->post_excerpt,
                'is_acf'        => false,
                'is_system'     => false,
            ),
            array(
                'name'          => 'post_date',
                'label'         => __( 'Ngày đăng bài (Date)', 'wp-acf-smart-importer' ),
                'type'          => 'wp_core',
                'current_value' => $post->post_date,
                'is_acf'        => false,
                'is_system'     => false,
            ),
            array(
                'name'          => 'featured_image',
                'label'         => __( 'Ảnh đại diện (Featured Image)', 'wp-acf-smart-importer' ),
                'type'          => 'wp_core',
                'current_value' => get_the_post_thumbnail_url( $post_id, 'full' ) ? get_the_post_thumbnail_url( $post_id, 'full' ) : '',
                'is_acf'        => false,
                'is_system'     => false,
            ),
        );

        // 2. Các trường ACF
        $acf_fields_schema = WP_ACF_Smart_Importer_Generator::get_acf_fields_for_post_type( $post_type );
        $acf_names = array();
        $acf_fields = array();

        foreach ( $acf_fields_schema as $f ) {
            $acf_names[] = $f['name'];
            $val = WP_ACF_Smart_Importer_Generator::get_acf_field_value( $f['name'], $post_id );
            
            if ( is_array( $val ) ) {
                $val = json_encode( $val, JSON_UNESCAPED_UNICODE );
            }

            $acf_fields[] = array(
                'name'          => 'acf_' . $f['name'],
                'label'         => '[ACF] ' . $f['label'] . ' (' . $f['name'] . ')',
                'type'          => 'acf_' . $f['type'],
                'current_value' => $val !== null ? $val : '',
                'is_acf'        => true,
                'is_system'     => false,
                'acf_key'       => isset( $f['key'] ) ? $f['key'] : '',
                'choices'       => isset( $f['choices'] ) ? $f['choices'] : array(),
            );
        }

        // 3. Các trường custom meta
        $all_meta = get_post_meta( $post_id );
        $custom_meta_fields = array();
        $ignored_keys = array(
            '_edit_lock', '_edit_last', '_pingme', '_encloseme', '_wp_page_template', 
            '_wp_attachment_metadata', '_wp_attached_file', '_thumbnail_id', 
            '_wp_trash_meta_status', '_wp_trash_meta_time'
        );

        if ( is_array( $all_meta ) ) {
            foreach ( $all_meta as $key => $values ) {
                if ( in_array( $key, $ignored_keys ) ) {
                    continue;
                }

                // Lọc bỏ ACF reference key (nếu key bắt đầu bằng _ và bỏ _ đi trùng với tên trường ACF)
                if ( strpos( $key, '_' ) === 0 ) {
                    $potential_acf_name = substr( $key, 1 );
                    if ( in_array( $potential_acf_name, $acf_names ) ) {
                        continue;
                    }
                }

                // Lọc bỏ nếu key chính là tên trường ACF
                if ( in_array( $key, $acf_names ) ) {
                    continue;
                }

                $val = isset( $values[0] ) ? $values[0] : '';
                if ( is_serialized( $val ) ) {
                    $unserialized = maybe_unserialize( $val );
                    if ( is_array( $unserialized ) || is_object( $unserialized ) ) {
                        $val = json_encode( $unserialized, JSON_UNESCAPED_UNICODE );
                    }
                }

                $is_system = ( strpos( $key, '_' ) === 0 );

                $custom_meta_fields[] = array(
                    'name'          => 'meta_' . $key,
                    'label'         => $key,
                    'type'          => 'custom_meta',
                    'current_value' => $val,
                    'is_acf'        => false,
                    'is_system'     => $is_system,
                );
            }
        }

        // 4. Các trường Taxonomy (Chuyên mục / Thẻ)
        $tax_fields = array();
        $taxonomies = get_object_taxonomies( $post_type, 'objects' );
        if ( is_array( $taxonomies ) ) {
            foreach ( $taxonomies as $tax_slug => $tax_obj ) {
                if ( ! $tax_obj->public ) {
                    continue;
                }
                
                // Lấy danh sách term hiện tại của bài viết
                $terms = wp_get_object_terms( $post_id, $tax_slug, array( 'fields' => 'names' ) );
                $terms_str = ( ! is_wp_error( $terms ) && ! empty( $terms ) ) ? implode( ' > ', $terms ) : '';

                $tax_fields[] = array(
                    'name'          => 'tax_' . $tax_slug,
                    'label'         => '[Taxonomy] ' . $tax_obj->label . ' (' . $tax_slug . ')',
                    'type'          => 'taxonomy',
                    'current_value' => $terms_str,
                    'is_acf'        => false,
                    'is_system'     => false,
                );
            }
        }

        $result_fields = array_merge( $core_fields, $acf_fields, $tax_fields, $custom_meta_fields );

        wp_send_json_success( array(
            'post_id'   => $post_id,
            'post_type' => $post_type,
            'fields'    => $result_fields,
        ) );
    }

    /**
     * Cập nhật trực tiếp các trường bài viết
     */
    public function update_post_fields_directly() {
        $this->verify_security();
        $post_id = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0;
        $fields  = isset( $_POST['fields'] ) ? map_deep( $_POST['fields'], 'wp_kses_post' ) : array();

        if ( ! $post_id || ! get_post( $post_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Bài viết không tồn tại.', 'wp-acf-smart-importer' ) ) );
        }

        $core_data = array( 'ID' => $post_id );
        $has_core = false;

        foreach ( $fields as $field_name => $val ) {
            // Core fields
            if ( in_array( $field_name, array( 'post_title', 'post_name', 'post_content', 'post_excerpt', 'post_date' ) ) ) {
                $core_data[ $field_name ] = $val;
                $has_core = true;
            } elseif ( $field_name === 'featured_image' ) {
                // Update featured image
                if ( empty( $val ) ) {
                    delete_post_thumbnail( $post_id );
                } else {
                    if ( filter_var( $val, FILTER_VALIDATE_URL ) ) {
                        $attachment_id = WP_ACF_Smart_Importer_Engine::handle_media_import( $val, $post_id );
                        if ( $attachment_id && ! is_wp_error( $attachment_id ) ) {
                            set_post_thumbnail( $post_id, $attachment_id );
                        }
                    } else if ( is_numeric( $val ) ) {
                        set_post_thumbnail( $post_id, intval( $val ) );
                    }
                }
            } elseif ( strpos( $field_name, 'acf_' ) === 0 ) {
                // ACF fields
                $acf_name = substr( $field_name, 4 );
                
                $decoded = json_decode( html_entity_decode( $val ), true );
                $save_val = ( $decoded !== null ) ? $decoded : $val;

                if ( function_exists( 'update_field' ) ) {
                    update_field( $acf_name, $save_val, $post_id );
                } else {
                    update_post_meta( $post_id, $acf_name, $save_val );
                }
            } elseif ( strpos( $field_name, 'tax_' ) === 0 ) {
                // Taxonomy fields
                $taxonomy = substr( $field_name, 4 );
                WP_ACF_Smart_Importer_Engine::handle_taxonomy_import( $post_id, $val, $taxonomy );
            } elseif ( strpos( $field_name, 'meta_' ) === 0 ) {
                // Custom meta fields
                $meta_key = substr( $field_name, 5 );
                
                $decoded = json_decode( html_entity_decode( $val ), true );
                $save_val = ( $decoded !== null ) ? $decoded : $val;

                update_post_meta( $post_id, $meta_key, $save_val );
            }
        }

        if ( $has_core ) {
            wp_update_post( $core_data );
        }

        wp_send_json_success( array( 'message' => __( 'Cập nhật bài viết thành công!', 'wp-acf-smart-importer' ) ) );
    }

    /**
     * Lấy danh sách bài viết kèm theo thông tin thumbnail hiện tại
     */
    public function get_posts_for_bulk_images() {
        $this->verify_security();
        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';

        $posts = get_posts( array(
            'post_type'      => $post_type,
            'posts_per_page' => -1,
            'post_status'    => 'any',
            'orderby'        => 'date',
            'order'          => 'DESC',
        ) );

        $result = array();
        foreach ( $posts as $post ) {
            $thumb_id = get_post_thumbnail_id( $post->ID );
            $thumb_url = '';
            if ( $thumb_id ) {
                $thumb_url = wp_get_attachment_image_url( $thumb_id, 'thumbnail' );
            }

            $result[] = array(
                'id'         => $post->ID,
                'title'      => $post->post_title ? $post->post_title : __( '(Không tiêu đề)', 'wp-acf-smart-importer' ),
                'permalink'  => get_permalink( $post->ID ),
                'thumb_url'  => $thumb_url,
                'post_date'  => get_the_date( 'Y-m-d H:i', $post->ID ),
            );
        }

        wp_send_json_success( $result );
    }

    /**
     * Gán thumbnail cho một bài viết cụ thể
     */
    public function set_post_thumbnail_ajax() {
        $this->verify_security();
        $post_id       = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0;
        $attachment_id = isset( $_POST['attachment_id'] ) ? intval( $_POST['attachment_id'] ) : 0;

        if ( ! $post_id || ! get_post( $post_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Bài viết không tồn tại.', 'wp-acf-smart-importer' ) ) );
        }

        if ( ! $attachment_id ) {
            // Xóa ảnh đại diện
            delete_post_thumbnail( $post_id );
            wp_send_json_success( array(
                'message'   => __( 'Đã xóa ảnh đại diện thành công.', 'wp-acf-smart-importer' ),
                'thumb_url' => '',
            ) );
        }

        // Kiểm tra xem media có tồn tại không
        if ( ! wp_attachment_is_image( $attachment_id ) ) {
            wp_send_json_error( array( 'message' => __( 'ID ảnh tải lên không hợp lệ hoặc không phải là hình ảnh.', 'wp-acf-smart-importer' ) ) );
        }

        $res = set_post_thumbnail( $post_id, $attachment_id );

        if ( $res ) {
            $thumb_url = wp_get_attachment_image_url( $attachment_id, 'thumbnail' );
            wp_send_json_success( array(
                'message'   => __( 'Đã gán ảnh đại diện thành công.', 'wp-acf-smart-importer' ),
                'thumb_url' => $thumb_url,
            ) );
        } else {
            wp_send_json_error( array( 'message' => __( 'Không thể gán ảnh đại diện (Có thể do lỗi hệ thống hoặc phân quyền).', 'wp-acf-smart-importer' ) ) );
        }
    }

    /**
     * Lấy danh sách Taxonomies công khai thuộc Post Type
     */
    public function get_taxonomies_for_post_type() {
        $this->verify_security();
        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';

        $taxonomies = get_object_taxonomies( $post_type, 'objects' );
        $result = array();

        if ( is_array( $taxonomies ) ) {
            foreach ( $taxonomies as $slug => $obj ) {
                if ( ! $obj->public && ! $obj->show_ui ) {
                    continue;
                }
                $result[] = array(
                    'slug'         => $slug,
                    'label'        => $obj->label . ' (' . $slug . ')',
                    'hierarchical' => $obj->hierarchical,
                );
            }
        }

        wp_send_json_success( $result );
    }

    /**
     * Lấy tất cả các Terms thuộc Taxonomy
     */
    public function get_terms_by_taxonomy() {
        $this->verify_security();
        $taxonomy = isset( $_POST['taxonomy'] ) ? sanitize_text_field( $_POST['taxonomy'] ) : 'category';

        if ( ! taxonomy_exists( $taxonomy ) ) {
            wp_send_json_error( array( 'message' => __( 'Taxonomy không tồn tại.', 'wp-acf-smart-importer' ) ) );
        }

        $terms = get_terms( array(
            'taxonomy'   => $taxonomy,
            'hide_empty' => false,
        ) );

        if ( is_wp_error( $terms ) ) {
            wp_send_json_error( array( 'message' => $terms->get_error_message() ) );
        }

        $result = array();
        foreach ( $terms as $t ) {
            $result[] = array(
                'term_id' => $t->term_id,
                'name'    => $t->name,
                'slug'    => $t->slug,
                'parent'  => $t->parent,
                'count'   => $t->count,
            );
        }

        wp_send_json_success( $result );
    }

    /**
     * Gán Taxonomy Terms cho một danh sách bài viết
     */
    public function assign_taxonomy_terms_ajax() {
        $this->verify_security();

        $post_ids = array();
        if ( isset( $_POST['post_ids'] ) && is_array( $_POST['post_ids'] ) ) {
            $post_ids = array_map( 'intval', $_POST['post_ids'] );
        } elseif ( isset( $_POST['post_id'] ) ) {
            $post_ids = array( intval( $_POST['post_id'] ) );
        }

        $taxonomy    = isset( $_POST['taxonomy'] ) ? sanitize_text_field( $_POST['taxonomy'] ) : 'category';
        $term_ids    = isset( $_POST['term_ids'] ) ? array_map( 'intval', $_POST['term_ids'] ) : array();
        $custom_path = isset( $_POST['custom_path'] ) ? sanitize_text_field( wp_unslash( $_POST['custom_path'] ) ) : '';
        $append_mode = isset( $_POST['mode'] ) && $_POST['mode'] === 'append';

        if ( empty( $post_ids ) ) {
            wp_send_json_error( array( 'message' => __( 'Vui lòng chọn ít nhất 1 bài viết.', 'wp-acf-smart-importer' ) ) );
        }

        if ( ! taxonomy_exists( $taxonomy ) ) {
            wp_send_json_error( array( 'message' => __( 'Taxonomy không tồn tại.', 'wp-acf-smart-importer' ) ) );
        }

        $last_terms_str = '';

        foreach ( $post_ids as $post_id ) {
            if ( ! get_post( $post_id ) ) {
                continue;
            }

            // Nếu có chọn term IDs trực tiếp
            if ( ! empty( $term_ids ) ) {
                wp_set_object_terms( $post_id, $term_ids, $taxonomy, $append_mode );
            }

            // Nếu có nhập đường dẫn custom path ("Cha > Con")
            if ( ! empty( $custom_path ) ) {
                WP_ACF_Smart_Importer_Engine::handle_taxonomy_import( $post_id, $custom_path, $taxonomy, $append_mode );
            }

            // Lấy chuỗi terms sau khi cập nhật
            $updated_terms = wp_get_object_terms( $post_id, $taxonomy, array( 'fields' => 'names' ) );
            $last_terms_str = ( ! is_wp_error( $updated_terms ) && ! empty( $updated_terms ) ) ? implode( ' > ', $updated_terms ) : '(Trống)';
        }

        wp_send_json_success( array(
            'message'   => sprintf( __( 'Đã gán phân loại cho %d bài viết thành công!', 'wp-acf-smart-importer' ), count( $post_ids ) ),
            'terms_str' => $last_terms_str,
        ) );
    }

    /**
     * Lấy danh sách bài viết và trường ACF phục vụ việc export
     */
    public function get_posts_for_export() {
        $this->verify_security();
        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';

        $posts = get_posts( array(
            'post_type'      => $post_type,
            'posts_per_page' => -1,
            'post_status'    => 'any',
            'orderby'        => 'date',
            'order'          => 'DESC',
        ) );

        $formatted_posts = array();
        foreach ( $posts as $post ) {
            $formatted_posts[] = array(
                'id'        => $post->ID,
                'title'     => $post->post_title ? $post->post_title : __( '(Không tiêu đề)', 'wp-acf-smart-importer' ),
                'post_date' => get_the_date( 'Y-m-d H:i', $post->ID ),
            );
        }

        // Lấy danh sách trường ACF liên quan của post type này
        $acf_schema = WP_ACF_Smart_Importer_Generator::get_acf_fields_for_post_type( $post_type );
        $acf_fields = array();
        foreach ( $acf_schema as $f ) {
            $acf_fields[] = array(
                'name'  => 'acf_' . $f['name'],
                'label' => '[ACF] ' . $f['label'] . ' (' . $f['name'] . ')',
                'type'  => $f['type'],
            );
        }

        wp_send_json_success( array(
            'posts'      => $formatted_posts,
            'acf_fields' => $acf_fields,
        ) );
    }

    /**
     * Lấy chi tiết dữ liệu bài viết để export ra Excel + giải quyết ảnh đính kèm
     */
    public function get_export_data() {
        $this->verify_security();

        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $post_ids  = isset( $_POST['post_ids'] ) ? array_map( 'intval', $_POST['post_ids'] ) : array();
        $fields    = isset( $_POST['fields'] ) ? array_map( 'sanitize_text_field', $_POST['fields'] ) : array();

        if ( empty( $post_ids ) ) {
            wp_send_json_error( array( 'message' => __( 'Vui lòng chọn ít nhất một bài viết để xuất dữ liệu.', 'wp-acf-smart-importer' ) ) );
        }

        $acf_schema = WP_ACF_Smart_Importer_Generator::get_acf_fields_for_post_type( $post_type );
        $acf_names_types = array();
        foreach ( $acf_schema as $f ) {
            $acf_names_types[ $f['name'] ] = $f['type'];
        }

        $rows = array();
        $file_mappings = array(); // [ zip_path => server_absolute_path ]
        $image_counters = array(); // Đếm để tạo tên ảnh không trùng lặp

        foreach ( $post_ids as $post_id ) {
            $post = get_post( $post_id );
            if ( ! $post ) continue;

            $row_data = array();

            // Duyệt qua danh sách trường người dùng yêu cầu xuất
            foreach ( $fields as $field_name ) {
                if ( $field_name === 'post_id' ) {
                    $row_data['post_id'] = $post->ID;
                } elseif ( $field_name === 'post_title' ) {
                    $row_data['post_title'] = $post->post_title;
                } elseif ( $field_name === 'post_name' ) {
                    $row_data['post_name'] = $post->post_name;
                } elseif ( $field_name === 'post_content' ) {
                    $row_data['post_content'] = $post->post_content;
                } elseif ( $field_name === 'post_excerpt' ) {
                    $row_data['post_excerpt'] = $post->post_excerpt;
                } elseif ( $field_name === 'post_date' ) {
                    $row_data['post_date'] = $post->post_date;
                } elseif ( $field_name === 'featured_image' ) {
                    // Xử lý ảnh đại diện
                    $thumb_id = get_post_thumbnail_id( $post->ID );
                    if ( $thumb_id ) {
                        $thumb_url = wp_get_attachment_url( $thumb_id );
                        $server_path = get_attached_file( $thumb_id );
                        
                        if ( $server_path && file_exists( $server_path ) ) {
                            $filename = basename( $server_path );
                            $zip_path = 'images/' . $post->ID . '_featured_' . $filename;
                            
                            $file_mappings[ $zip_path ] = $server_path;
                            $row_data['featured_image'] = $zip_path; // Ghi đường dẫn tương đối vào file Excel
                        } else {
                            $row_data['featured_image'] = $thumb_url; // Fallback URL
                        }
                    } else {
                        $row_data['featured_image'] = '';
                    }
                } elseif ( strpos( $field_name, 'acf_' ) === 0 ) {
                    $acf_key = substr( $field_name, 4 );
                    $field_type = isset( $acf_names_types[ $acf_key ] ) ? $acf_names_types[ $acf_key ] : '';

                    // Nếu là trường ảnh hoặc file
                    if ( in_array( $field_type, array( 'image', 'file' ) ) ) {
                        $attachment_id = $this->get_attachment_id_from_acf( $acf_key, $post->ID );
                        if ( $attachment_id ) {
                            $file_url = wp_get_attachment_url( $attachment_id );
                            $server_path = get_attached_file( $attachment_id );
                            
                            if ( $server_path && file_exists( $server_path ) ) {
                                $filename = basename( $server_path );
                                $zip_path = 'images/' . $post->ID . '_acf_' . $acf_key . '_' . $filename;
                                
                                $file_mappings[ $zip_path ] = $server_path;
                                $row_data[ $field_name ] = $zip_path;
                            } else {
                                $row_data[ $field_name ] = $file_url;
                            }
                        } else {
                            $row_data[ $field_name ] = '';
                        }
                    } else {
                        // Trường văn bản thông thường
                        $val = get_field( $acf_key, $post->ID );
                        if ( is_array( $val ) || is_object( $val ) ) {
                            $val = json_encode( $val, JSON_UNESCAPED_UNICODE );
                        }
                        $row_data[ $field_name ] = $val !== null ? $val : '';
                    }
                } elseif ( strpos( $field_name, 'meta_' ) === 0 ) {
                    $meta_key = substr( $field_name, 5 );
                    $val = get_post_meta( $post->ID, $meta_key, true );
                    if ( is_array( $val ) || is_object( $val ) ) {
                        $val = json_encode( $val, JSON_UNESCAPED_UNICODE );
                    }
                    $row_data[ $field_name ] = $val !== null ? $val : '';
                }
            }

            $rows[] = $row_data;
        }

        wp_send_json_success( array(
            'rows'          => $rows,
            'file_mappings' => $file_mappings,
        ) );
    }

    /**
     * Helper phân tích lấy Attachment ID từ ACF field hình ảnh/tài liệu
     */
    private function get_attachment_id_from_acf( $field_name, $post_id ) {
        // Thử lấy raw value (thường là attachment ID)
        $raw_val = get_field( $field_name, $post_id, false );
        if ( is_numeric( $raw_val ) && intval( $raw_val ) > 0 ) {
            return intval( $raw_val );
        }

        if ( is_string( $raw_val ) && filter_var( $raw_val, FILTER_VALIDATE_URL ) ) {
            $attachment_id = attachment_url_to_postid( $raw_val );
            if ( $attachment_id ) return $attachment_id;
        }

        if ( is_array( $raw_val ) && isset( $raw_val['ID'] ) ) {
            return intval( $raw_val['ID'] );
        }

        // Lấy formatted value để làm phương án dự phòng
        $formatted_val = get_field( $field_name, $post_id );
        if ( is_array( $formatted_val ) && isset( $formatted_val['ID'] ) ) {
            return intval( $formatted_val['ID'] );
        }
        if ( is_numeric( $formatted_val ) ) {
            return intval( $formatted_val );
        }
        if ( is_string( $formatted_val ) && filter_var( $formatted_val, FILTER_VALIDATE_URL ) ) {
            $attachment_id = attachment_url_to_postid( $formatted_val );
            if ( $attachment_id ) return $attachment_id;
        }

        return false;
    }

    /**
     * Nhận Base64 của Excel và danh sách file, đóng gói thành zip
     */
    public function create_zip_export() {
        $this->verify_security();

        $xlsx_b64   = isset( $_POST['xlsx_base64'] ) ? $_POST['xlsx_base64'] : '';
        $files_json = isset( $_POST['files'] ) ? wp_unslash( $_POST['files'] ) : '';
        $post_type  = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';

        if ( empty( $xlsx_b64 ) ) {
            wp_send_json_error( array( 'message' => __( 'Thiếu nội dung Excel.', 'wp-acf-smart-importer' ) ) );
        }

        // Đường dẫn thư mục lưu trữ zip tạm thời
        $upload_dir = wp_upload_dir();
        $temp_dir = $upload_dir['basedir'] . '/wpsai-temp';
        if ( ! file_exists( $temp_dir ) ) {
            wp_mkdir_p( $temp_dir );
        }

        // Quét dọn dẹp các tệp zip xuất cũ
        $this->cleanup_temp_dir( $temp_dir );

        // Tạo tệp Zip
        $zip_filename = 'export-' . $post_type . '-' . date( 'Ymd_His' ) . '_' . wp_generate_password( 6, false ) . '.zip';
        $zip_filepath = $temp_dir . '/' . $zip_filename;

        if ( ! class_exists( 'ZipArchive' ) ) {
            wp_send_json_error( array( 'message' => __( 'Máy chủ không hỗ trợ lớp PHP ZipArchive. Hãy liên hệ quản trị viên hosting.', 'wp-acf-smart-importer' ) ) );
        }

        $zip = new ZipArchive();
        if ( $zip->open( $zip_filepath, ZipArchive::CREATE | ZipArchive::OVERWRITE ) !== true ) {
            wp_send_json_error( array( 'message' => __( 'Không thể khởi tạo tệp ZIP.', 'wp-acf-smart-importer' ) ) );
        }

        // 1. Thêm file Excel
        $xlsx_data = base64_decode( $xlsx_b64 );
        $zip->addFromString( 'danh-sach-bai-viet.xlsx', $xlsx_data );

        // 2. Thêm các file ảnh đính kèm
        $files_to_add = json_decode( $files_json, true );
        if ( is_array( $files_to_add ) ) {
            foreach ( $files_to_add as $zip_path => $server_path ) {
                if ( file_exists( $server_path ) && is_file( $server_path ) ) {
                    $zip->addFile( $server_path, $zip_path );
                }
            }
        }

        $zip->close();

        $zip_url = $upload_dir['baseurl'] . '/wpsai-temp/' . $zip_filename;

        wp_send_json_success( array(
            'download_url' => $zip_url,
            'message'      => __( 'Đóng gói file ZIP thành công!', 'wp-acf-smart-importer' ),
        ) );
    }

    /**
     * Dọn dẹp thư mục tạm xóa file .zip > 1 giờ
     */
    private function cleanup_temp_dir( $dir ) {
        if ( ! is_dir( $dir ) ) return;
        $files = glob( $dir . '/*' );
        $now = time();
        foreach ( $files as $file ) {
            if ( is_file( $file ) ) {
                if ( $now - filemtime( $file ) >= 3600 ) {
                    @unlink( $file );
                }
            }
        }
    }

    /**
     * Xem trước nội dung cào từ URL
     */
    public function scrape_preview() {
        $this->verify_security();

        $url = isset( $_POST['url'] ) ? esc_url_raw( $_POST['url'] ) : '';
        $selectors = array(
            'title'   => isset( $_POST['title_selector'] ) ? sanitize_text_field( $_POST['title_selector'] ) : '',
            'content' => isset( $_POST['content_selector'] ) ? sanitize_text_field( $_POST['content_selector'] ) : '',
            'image'   => isset( $_POST['image_selector'] ) ? sanitize_text_field( $_POST['image_selector'] ) : '',
            'remove'  => isset( $_POST['remove_selector'] ) ? sanitize_text_field( $_POST['remove_selector'] ) : '',
        );

        if ( empty( $url ) ) {
            wp_send_json_error( array( 'message' => __( 'Vui lòng nhập URL hợp lệ.', 'wp-acf-smart-importer' ) ) );
        }

        $scraped = WP_ACF_Smart_Importer_Scraper::scrape_url( $url, $selectors );

        if ( is_wp_error( $scraped ) ) {
            wp_send_json_error( array( 'message' => $scraped->get_error_message() ) );
        }

        wp_send_json_success( $scraped );
    }

    /**
     * Cào URL và nhập làm bài viết mới
     */
    public function scrape_and_import() {
        $this->verify_security();

        $url = isset( $_POST['url'] ) ? esc_url_raw( $_POST['url'] ) : '';
        $selectors = array(
            'title'   => isset( $_POST['title_selector'] ) ? sanitize_text_field( $_POST['title_selector'] ) : '',
            'content' => isset( $_POST['content_selector'] ) ? sanitize_text_field( $_POST['content_selector'] ) : '',
            'image'   => isset( $_POST['image_selector'] ) ? sanitize_text_field( $_POST['image_selector'] ) : '',
            'remove'  => isset( $_POST['remove_selector'] ) ? sanitize_text_field( $_POST['remove_selector'] ) : '',
        );

        $post_type   = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $post_status = isset( $_POST['post_status'] ) ? sanitize_text_field( $_POST['post_status'] ) : 'draft';
        $taxonomy    = isset( $_POST['taxonomy'] ) ? sanitize_text_field( $_POST['taxonomy'] ) : '';
        $terms       = isset( $_POST['terms'] ) ? sanitize_text_field( $_POST['terms'] ) : '';

        if ( empty( $url ) ) {
            wp_send_json_error( array( 'message' => __( 'Vui lòng nhập URL hợp lệ.', 'wp-acf-smart-importer' ) ) );
        }

        // Thực thi cào
        $scraped = WP_ACF_Smart_Importer_Scraper::scrape_url( $url, $selectors );

        if ( is_wp_error( $scraped ) ) {
            wp_send_json_error( array( 'message' => $scraped->get_error_message() ) );
        }

        if ( empty( $scraped['title'] ) ) {
            wp_send_json_error( array( 'message' => __( 'Không thể cào được tiêu đề bài viết. Vui lòng kiểm tra bộ chọn (Selector) Tiêu đề.', 'wp-acf-smart-importer' ) ) );
        }

        // Chuẩn bị hàng và sơ đồ ánh xạ cho engine
        $row = array(
            'title'          => $scraped['title'],
            'content'        => $scraped['content'],
            'featured_image' => $scraped['featured_image'],
        );

        $mapping = array(
            'post_title'     => 'title',
            'post_content'   => 'content',
            'featured_image' => 'featured_image',
        );

        // Gán taxonomy nếu có
        if ( ! empty( $taxonomy ) && ! empty( $terms ) ) {
            $row['taxonomy_terms'] = $terms;
            $mapping[ 'tax_' . $taxonomy ] = 'taxonomy_terms';
        }

        // Nhập dòng đơn lẻ
        $post_id = WP_ACF_Smart_Importer_Engine::import_single_row( $row, $mapping, $post_type, $post_status );

        if ( is_wp_error( $post_id ) ) {
            wp_send_json_error( array( 'message' => $post_id->get_error_message() ) );
        }

        wp_send_json_success( array(
            'post_id'   => $post_id,
            'title'     => get_the_title( $post_id ),
            'permalink' => get_permalink( $post_id ),
            'message'   => __( 'Đã cào và nhập bài viết thành công!', 'wp-acf-smart-importer' ),
        ) );
    }

    /**
     * Phân tích cấu trúc bài viết mẫu để tìm vị trí ảnh
     */
    public function analyze_template_post() {
        $this->verify_security();

        $post_id = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0;

        if ( ! $post_id || ! get_post( $post_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Bài viết mẫu không tồn tại.', 'wp-acf-smart-importer' ) ) );
        }

        $result = WP_ACF_Smart_Importer_Generator::analyze_template_structure( $post_id );

        if ( is_wp_error( $result ) ) {
            wp_send_json_error( array( 'message' => $result->get_error_message() ) );
        }

        wp_send_json_success( $result );
    }

    /**
     * Chèn ảnh từ kho vào nội dung bài viết và import
     * Hàm này nhận nội dung AI đã sinh, chèn ảnh, rồi lưu vào DB
     */
    public function ai_inject_images_and_import() {
        $this->verify_security();

        $post_id        = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0;
        $post_title     = isset( $_POST['post_title'] ) ? sanitize_text_field( wp_unslash( $_POST['post_title'] ) ) : '';
        $post_content   = isset( $_POST['post_content'] ) ? wp_kses_post( wp_unslash( $_POST['post_content'] ) ) : '';
        $post_excerpt   = isset( $_POST['post_excerpt'] ) ? sanitize_textarea_field( wp_unslash( $_POST['post_excerpt'] ) ) : '';
        $post_type      = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $post_status    = isset( $_POST['post_status'] ) ? sanitize_text_field( $_POST['post_status'] ) : 'draft';

        // Các tham số ảnh
        $image_pool_ids   = array();
        if ( isset( $_POST['image_pool_ids'] ) && is_array( $_POST['image_pool_ids'] ) ) {
            $image_pool_ids = array_map( 'intval', $_POST['image_pool_ids'] );
        }

        $image_insert_mode = isset( $_POST['image_insert_mode'] ) ? sanitize_text_field( $_POST['image_insert_mode'] ) : 'sequential';
        $set_featured      = isset( $_POST['set_featured'] ) ? ( $_POST['set_featured'] === '1' || $_POST['set_featured'] === 'true' ) : true;

        $template_slots = array();
        if ( isset( $_POST['template_slots'] ) ) {
            $slots_raw = wp_unslash( $_POST['template_slots'] );
            if ( is_string( $slots_raw ) ) {
                $template_slots = json_decode( $slots_raw, true );
            } elseif ( is_array( $slots_raw ) ) {
                $template_slots = $slots_raw;
            }
        }

        // Nếu có ảnh trong pool, chèn vào nội dung
        $featured_image_id = 0;
        if ( ! empty( $image_pool_ids ) && ! empty( $post_content ) ) {
            $inject_result = WP_ACF_Smart_Importer_Generator::inject_images_into_content(
                $post_content,
                $image_pool_ids,
                $template_slots,
                $image_insert_mode,
                $set_featured
            );
            $post_content      = $inject_result['content'];
            $featured_image_id = $inject_result['featured_image_id'];
        }

        // Tạo hoặc cập nhật bài viết
        if ( empty( $post_title ) ) {
            $post_title = __( 'Bài viết AI - ', 'wp-acf-smart-importer' ) . current_time( 'Y-m-d H:i:s' );
        }

        $post_data = array(
            'post_title'   => $post_title,
            'post_content' => $post_content,
            'post_excerpt' => $post_excerpt,
            'post_status'  => $post_status,
            'post_type'    => $post_type,
        );

        if ( $post_id > 0 && get_post( $post_id ) ) {
            $post_data['ID'] = $post_id;
            $result_id = wp_update_post( $post_data );
        } else {
            $result_id = wp_insert_post( $post_data );
        }

        if ( is_wp_error( $result_id ) ) {
            wp_send_json_error( array( 'message' => $result_id->get_error_message() ) );
        }

        // Gán Featured Image nếu có
        if ( $featured_image_id > 0 ) {
            set_post_thumbnail( $result_id, $featured_image_id );
        }

        // Xử lý các trường ACF và taxonomy nếu có
        $extra_fields = isset( $_POST['extra_fields'] ) ? map_deep( $_POST['extra_fields'], 'wp_kses_post' ) : array();
        if ( ! empty( $extra_fields ) ) {
            foreach ( $extra_fields as $field_name => $val ) {
                if ( empty( $val ) && $val !== '0' ) {
                    continue;
                }

                if ( strpos( $field_name, 'acf_' ) === 0 ) {
                    $acf_name = substr( $field_name, 4 );
                    if ( function_exists( 'update_field' ) ) {
                        // Kiểm tra nếu là trường image/file
                        $acf_field = acf_get_field( $acf_name );
                        if ( $acf_field && in_array( $acf_field['type'], array( 'image', 'file' ) ) ) {
                            if ( filter_var( $val, FILTER_VALIDATE_URL ) ) {
                                $file_id = WP_ACF_Smart_Importer_Engine::handle_media_import( $val, $result_id );
                                if ( $file_id && ! is_wp_error( $file_id ) ) {
                                    $val = $file_id;
                                }
                            }
                        }
                        update_field( $acf_name, $val, $result_id );
                    } else {
                        update_post_meta( $result_id, $acf_name, $val );
                    }
                } elseif ( strpos( $field_name, 'tax_' ) === 0 ) {
                    $taxonomy = substr( $field_name, 4 );
                    WP_ACF_Smart_Importer_Engine::handle_taxonomy_import( $result_id, $val, $taxonomy );
                } elseif ( strpos( $field_name, 'meta_' ) === 0 ) {
                    $meta_key = substr( $field_name, 5 );
                    update_post_meta( $result_id, $meta_key, $val );
                }
            }
        }

        $thumb_url = '';
        if ( $featured_image_id > 0 ) {
            $thumb_url = wp_get_attachment_image_url( $featured_image_id, 'thumbnail' );
        }

        wp_send_json_success( array(
            'post_id'            => $result_id,
            'title'              => get_the_title( $result_id ),
            'permalink'          => get_permalink( $result_id ),
            'featured_image_id'  => $featured_image_id,
            'thumb_url'          => $thumb_url,
            'images_injected'    => count( $image_pool_ids ),
        ) );
    }

    // ==========================================
    // PROJECT DOCUMENTATION MANAGER ENDPOINTS
    // ==========================================

    /**
     * Lấy dữ liệu tài liệu dự án (DB + File + System Info)
     */
    public function get_project_docs() {
        $this->verify_security();

        $docs_data = get_option( 'wpsai_project_docs_data', array() );
        
        $docs_dir = WPSAI_PATH . 'docs';
        $json_file = $docs_dir . '/project-docs.json';
        
        $force_file = isset( $_POST['force_file_read'] ) && $_POST['force_file_read'] == '1';

        // Nếu DB rỗng hoặc bắt buộc, thử đọc từ file JSON vật lý
        if ( ( empty( $docs_data ) || $force_file ) && file_exists( $json_file ) ) {
            $file_content = file_get_contents( $json_file );
            if ( $file_content ) {
                $docs_data = json_decode( $file_content, true );
                if ( is_array( $docs_data ) ) {
                    update_option( 'wpsai_project_docs_data', $docs_data );
                }
            }
        }

        if ( ! is_array( $docs_data ) ) {
            $docs_data = array();
        }

        // Tự động quét thông tin hệ thống để bổ sung vào response
        global $wp_version;
        
        // Active Theme
        $active_theme = wp_get_theme();
        $theme_info = array(
            'name'    => $active_theme->get( 'Name' ),
            'version' => $active_theme->get( 'Version' ),
            'folder'  => get_stylesheet(),
        );

        // Active Plugins
        if ( ! function_exists( 'get_plugin_data' ) ) {
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }
        $active_plugins_opt = get_option( 'active_plugins', array() );
        $active_plugins = array();
        foreach ( $active_plugins_opt as $plugin_path ) {
            $plugin_info = get_plugin_data( WP_PLUGIN_DIR . '/' . $plugin_path );
            if ( ! empty( $plugin_info['Name'] ) ) {
                $active_plugins[] = $plugin_info['Name'] . ' (v' . $plugin_info['Version'] . ')';
            }
        }

        // Custom Post Types
        $cpts = get_post_types( array( 'public' => true, '_builtin' => false ), 'objects' );
        $cpt_list = array();
        foreach ( $cpts as $slug => $cpt ) {
            $cpt_list[] = $cpt->label . ' (' . $slug . ')';
        }

        $system_info = array(
            'wp_version'        => $wp_version,
            'php_version'       => PHP_VERSION,
            'db_version'        => $GLOBALS['wpdb']->db_version(),
            'active_theme'      => $theme_info,
            'active_plugins'    => $active_plugins,
            'custom_post_types' => $cpt_list,
        );

        // Kiểm tra xem file json đã tồn tại trên server chưa
        $file_exists = file_exists( $json_file );
        $file_time = $file_exists ? date( 'Y-m-d H:i:s', filemtime( $json_file ) ) : '';

        wp_send_json_success( array(
            'docs'         => $docs_data,
            'system_info'  => $system_info,
            'file_sync'    => array(
                'exists'    => $file_exists,
                'path'      => str_replace( ABSPATH, '', $json_file ),
                'last_sync' => $file_time,
            )
        ) );
    }

    /**
     * Lưu dữ liệu tài liệu dự án (Lưu DB + Ghi file json & markdown)
     */
    public function save_project_docs() {
        $this->verify_security();

        $docs_json = isset( $_POST['data'] ) ? wp_unslash( $_POST['data'] ) : '';
        if ( empty( $docs_json ) ) {
            wp_send_json_error( array( 'message' => __( 'Dữ liệu lưu trữ trống.', 'wp-acf-smart-importer' ) ) );
        }

        $docs_data = json_decode( $docs_json, true );
        if ( ! is_array( $docs_data ) ) {
            wp_send_json_error( array( 'message' => __( 'Định dạng dữ liệu không hợp lệ.', 'wp-acf-smart-importer' ) ) );
        }

        // Lưu vào option DB
        update_option( 'wpsai_project_docs_data', $docs_data );

        // Đảm bảo thư mục docs tồn tại
        $docs_dir = WPSAI_PATH . 'docs';
        if ( ! file_exists( $docs_dir ) ) {
            wp_mkdir_p( $docs_dir );
        }

        // 1. Ghi file JSON
        $json_file = $docs_dir . '/project-docs.json';
        $json_written = file_put_contents( $json_file, wp_json_encode( $docs_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE ) );

        // 2. Ghi file Markdown để xem trực tiếp
        $md_file = $docs_dir . '/PROJECT_DOCUMENTATION.md';
        $md_content = $this->generate_docs_markdown_content( $docs_data );
        $md_written = file_put_contents( $md_file, $md_content );

        if ( $json_written === false || $md_written === false ) {
            wp_send_json_error( array( 'message' => __( 'Lưu DB thành công nhưng không thể ghi tệp vật lý. Vui lòng kiểm tra quyền ghi thư mục docs.', 'wp-acf-smart-importer' ) ) );
        }

        wp_send_json_success( array(
            'message'   => __( 'Đã lưu tài liệu vào cơ sở dữ liệu và đồng bộ tệp vật lý thành công!', 'wp-acf-smart-importer' ),
            'last_sync' => date( 'Y-m-d H:i:s' ),
        ) );
    }

    /**
     * Đọc các commit Git gần nhất
     */
    public function git_get_commits() {
        $this->verify_security();

        $repo_path = ABSPATH; // Gốc WordPress
        if ( ! file_exists( $repo_path . '.git' ) ) {
            // Thử thư mục cha hoặc thư mục plugin xem có Git không
            if ( file_exists( WPSAI_PATH . '.git' ) ) {
                $repo_path = WPSAI_PATH;
            } elseif ( file_exists( dirname( ABSPATH ) . '/.git' ) ) {
                $repo_path = dirname( ABSPATH ) . '/';
            } else {
                wp_send_json_error( array( 'message' => __( 'Không tìm thấy thư mục .git trong dự án.', 'wp-acf-smart-importer' ) ) );
            }
        }

        // Kiểm tra shell_exec có bị disable không
        if ( ! function_exists( 'shell_exec' ) ) {
            wp_send_json_error( array( 'message' => __( 'Hàm shell_exec của PHP bị vô hiệu hóa trên máy chủ này.', 'wp-acf-smart-importer' ) ) );
        }

        // Chạy lệnh git log lấy 10 commit gần nhất
        $command = 'cd ' . escapeshellarg( $repo_path ) . ' && git log -n 15 --oneline --date=short --pretty=format:"%h|%ad|%an|%s"';
        $output = shell_exec( $command );

        if ( empty( $output ) ) {
            wp_send_json_error( array( 'message' => __( 'Không thể lấy lịch sử commit (Có thể thư mục chưa có commit nào).', 'wp-acf-smart-importer' ) ) );
        }

        $commits = array();
        $lines = explode( "\n", trim( $output ) );
        foreach ( $lines as $line ) {
            $parts = explode( '|', $line, 4 );
            if ( count( $parts ) >= 4 ) {
                $commits[] = array(
                    'hash'    => $parts[0],
                    'date'    => $parts[1],
                    'author'  => $parts[2],
                    'message' => $parts[3],
                );
            }
        }

        wp_send_json_success( $commits );
    }

    /**
     * Dùng AI viết mô tả component dựa trên code
     */
    public function ai_describe_snippet() {
        $this->verify_security();

        $api_key = get_option( 'wpsai_gemini_api_key', '' );
        if ( empty( $api_key ) ) {
            wp_send_json_error( array( 'message' => __( 'Lỗi: Vui lòng cấu hình Gemini API Key trước khi sử dụng tính năng AI.', 'wp-acf-smart-importer' ) ) );
        }

        $name = isset( $_POST['name'] ) ? sanitize_text_field( $_POST['name'] ) : '';
        $category = isset( $_POST['category'] ) ? sanitize_text_field( $_POST['category'] ) : '';
        $html = isset( $_POST['html'] ) ? wp_unslash( $_POST['html'] ) : '';
        $css  = isset( $_POST['css'] ) ? wp_unslash( $_POST['css'] ) : '';
        $js   = isset( $_POST['js'] ) ? wp_unslash( $_POST['js'] ) : '';

        if ( empty( $html ) && empty( $css ) && empty( $js ) ) {
            wp_send_json_error( array( 'message' => __( 'Vui lòng cung cấp mã nguồn để AI phân tích.', 'wp-acf-smart-importer' ) ) );
        }

        $prompt = "Bạn là một chuyên gia lập trình WordPress và Frontend.\n";
        $prompt .= "Hãy viết tài liệu hướng dẫn và mô tả kỹ thuật chi tiết bằng TIẾNG VIỆT cho UI Component/Mã nguồn dưới đây:\n\n";
        $prompt .= "Tên linh kiện: " . $name . "\n";
        $prompt .= "Danh mục: " . $category . "\n\n";
        $prompt .= "--- MÃ NGUỒN HTML ---\n" . substr( $html, 0, 3000 ) . "\n\n";
        $prompt .= "--- MÃ NGUỒN CSS ---\n" . substr( $css, 0, 3000 ) . "\n\n";
        $prompt .= "--- MÃ NGUỒN JS ---\n" . substr( $js, 0, 3000 ) . "\n\n";
        $prompt .= "Yêu cầu:\n";
        $prompt .= "1. Hãy viết 1 đoạn mô tả ngắn gọn về tính năng và trải nghiệm người dùng của component này (2-3 câu).\n";
        $prompt .= "2. Hướng dẫn sử dụng nhanh cách nhúng component này vào dự án mới (ví dụ cấu trúc CSS/JS cần lưu ý).\n";
        $prompt .= "3. Viết súc tích, chuyên nghiệp bằng Tiếng Việt. Không trả về code. Trả về định dạng Markdown ngắn gọn.";

        $api_result = $this->call_gemini_api( $prompt, $api_key, false );

        if ( is_wp_error( $api_result ) ) {
            wp_send_json_error( array( 'message' => $api_result->get_error_message() ) );
        }

        wp_send_json_success( array( 'description' => trim( $api_result ) ) );
    }

    /**
     * Xuất tài liệu Markdown đầy đủ
     */
    public function export_docs_markdown() {
        $this->verify_security();

        $docs_data = get_option( 'wpsai_project_docs_data', array() );
        if ( empty( $docs_data ) ) {
            wp_send_json_error( array( 'message' => __( 'Không có dữ liệu tài liệu để xuất.', 'wp-acf-smart-importer' ) ) );
        }

        $md_content = $this->generate_docs_markdown_content( $docs_data );
        
        $upload_dir = wp_upload_dir();
        $temp_dir = $upload_dir['basedir'] . '/wpsai-temp';
        if ( ! file_exists( $temp_dir ) ) {
            wp_mkdir_p( $temp_dir );
        }

        $filename = 'project-docs-' . date( 'Ymd_His' ) . '.md';
        $filepath = $temp_dir . '/' . $filename;
        
        $written = file_put_contents( $filepath, $md_content );
        if ( $written === false ) {
            wp_send_json_error( array( 'message' => __( 'Không thể tạo tệp xuất tạm thời trên server.', 'wp-acf-smart-importer' ) ) );
        }

        $download_url = $upload_dir['baseurl'] . '/wpsai-temp/' . $filename;
        wp_send_json_success( array(
            'download_url' => $download_url,
            'message'      => __( 'Đã tạo tệp tài liệu Markdown thành công!', 'wp-acf-smart-importer' ),
        ) );
    }

    /**
     * Lấy danh sách tiêu đề bài viết thuộc Post Type & Chuyên mục (Category / Term)
     */
    public function get_post_titles() {
        $this->verify_security();
        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $taxonomy  = isset( $_POST['taxonomy'] ) ? sanitize_text_field( $_POST['taxonomy'] ) : '';
        $term_id   = isset( $_POST['term_id'] ) ? intval( $_POST['term_id'] ) : 0;

        $args = array(
            'post_type'      => $post_type,
            'posts_per_page' => -1,
            'post_status'    => 'any',
            'orderby'        => 'title',
            'order'          => 'ASC',
        );

        if ( ! empty( $taxonomy ) && $term_id > 0 ) {
            $args['tax_query'] = array(
                array(
                    'taxonomy' => $taxonomy,
                    'field'    => 'term_id',
                    'terms'    => $term_id,
                ),
            );
        }

        $posts = get_posts( $args );
        $result = array();

        foreach ( $posts as $post ) {
            $terms_str = '';
            if ( ! empty( $taxonomy ) ) {
                $terms = wp_get_object_terms( $post->ID, $taxonomy, array( 'fields' => 'names' ) );
                if ( ! is_wp_error( $terms ) && ! empty( $terms ) ) {
                    $terms_str = implode( ', ', $terms );
                }
            } else {
                if ( 'post' === $post_type ) {
                    $terms = wp_get_object_terms( $post->ID, 'category', array( 'fields' => 'names' ) );
                    if ( ! is_wp_error( $terms ) && ! empty( $terms ) ) {
                        $terms_str = implode( ', ', $terms );
                    }
                }
            }

            $result[] = array(
                'id'        => $post->ID,
                'title'     => $post->post_title ? $post->post_title : __( '(Không tiêu đề)', 'wp-acf-smart-importer' ),
                'permalink' => get_permalink( $post->ID ),
                'terms'     => $terms_str,
                'post_date' => get_the_date( 'Y-m-d H:i', $post->ID ),
                'content'   => $post->post_content,
                'excerpt'   => $post->post_excerpt,
            );
        }

        wp_send_json_success( $result );
    }

    /**
     * Cập nhật tiêu đề mới cho một bài viết
     */
    public function update_post_title() {
        $this->verify_security();
        
        $post_id     = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0;
        $new_title   = isset( $_POST['new_title'] ) ? sanitize_text_field( $_POST['new_title'] ) : '';
        $new_content = isset( $_POST['new_content'] ) ? wp_kses_post( wp_unslash( $_POST['new_content'] ) ) : null;
        $new_excerpt = isset( $_POST['new_excerpt'] ) ? sanitize_textarea_field( wp_unslash( $_POST['new_excerpt'] ) ) : null;

        if ( ! $post_id || ! get_post( $post_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Bài viết không tồn tại.', 'wp-acf-smart-importer' ) ) );
        }

        if ( ! current_user_can( 'edit_post', $post_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Bạn không có quyền sửa bài viết này.', 'wp-acf-smart-importer' ) ) );
        }

        if ( empty( $new_title ) ) {
            wp_send_json_error( array( 'message' => __( 'Tiêu đề mới không được để trống.', 'wp-acf-smart-importer' ) ) );
        }

        $post_data = array(
            'ID'         => $post_id,
            'post_title' => $new_title,
        );

        if ( $new_content !== null ) {
            $post_data['post_content'] = $new_content;
        }
        if ( $new_excerpt !== null ) {
            $post_data['post_excerpt'] = $new_excerpt;
        }

        $updated = wp_update_post( $post_data );

        if ( is_wp_error( $updated ) ) {
            wp_send_json_error( array( 'message' => $updated->get_error_message() ) );
        }

        wp_send_json_success( array(
            'post_id'   => $post_id,
            'new_title' => $new_title,
            'message'   => __( 'Cập nhật tiêu đề thành công.', 'wp-acf-smart-importer' ),
        ) );
    }

    /**
     * Dịch danh sách tiêu đề bài viết sang ngôn ngữ đích bằng AI Gemini hoặc Google Translate
     */
    public function translate_post_titles() {
        $this->verify_security();

        $translate_content = isset( $_POST['translate_content'] ) && 'true' === $_POST['translate_content'];
        $target_lang = isset( $_POST['target_lang'] ) ? sanitize_text_field( $_POST['target_lang'] ) : 'English';
        $translator_engine = isset( $_POST['translator_engine'] ) ? sanitize_text_field( $_POST['translator_engine'] ) : 'google_translate';

        $lang_code = self::get_google_translate_lang_code( $target_lang );

        if ( 'google_translate' === $translator_engine ) {
            if ( ! $translate_content ) {
                $titles = isset( $_POST['titles'] ) ? map_deep( $_POST['titles'], 'sanitize_text_field' ) : array();
                if ( empty( $titles ) ) {
                    wp_send_json_error( array( 'message' => __( 'Danh sách tiêu đề cần dịch không được để trống.', 'wp-acf-smart-importer' ) ) );
                }

                $translated_titles = array();
                foreach ( $titles as $title ) {
                    $translated_titles[] = self::translate_via_google_free( $title, $lang_code );
                }
                wp_send_json_success( $translated_titles );
            } else {
                $posts_data = isset( $_POST['posts_data'] ) ? $_POST['posts_data'] : array();
                if ( empty( $posts_data ) ) {
                    wp_send_json_error( array( 'message' => __( 'Danh sách bài viết cần dịch không được để trống.', 'wp-acf-smart-importer' ) ) );
                }

                if ( is_string( $posts_data ) ) {
                    $posts_data = json_decode( wp_unslash( $posts_data ), true );
                }

                $translated_data = array();
                foreach ( $posts_data as $post ) {
                    $translated_data[] = array(
                        'id'      => intval( $post['id'] ),
                        'title'   => self::translate_via_google_free( $post['title'], $lang_code ),
                        'content' => self::translate_html_via_google_free( $post['content'], $lang_code ),
                        'excerpt' => self::translate_via_google_free( $post['excerpt'], $lang_code ),
                    );
                }
                wp_send_json_success( $translated_data );
            }
        } else {
            // Dịch bằng Gemini AI
            $api_key = get_option( 'wpsai_gemini_api_key', '' );
            if ( empty( $api_key ) ) {
                wp_send_json_error( array( 'message' => __( 'Lỗi: Vui lòng cấu hình Gemini API Key trong tab Cài Đặt trước.', 'wp-acf-smart-importer' ) ) );
            }

            if ( ! $translate_content ) {
                $titles = isset( $_POST['titles'] ) ? map_deep( $_POST['titles'], 'sanitize_text_field' ) : array();
                if ( empty( $titles ) ) {
                    wp_send_json_error( array( 'message' => __( 'Danh sách tiêu đề cần dịch không được để trống.', 'wp-acf-smart-importer' ) ) );
                }

                // Tạo prompt chi tiết cho Gemini
                $prompt  = "You are a professional translator.\n";
                $prompt .= "Translate the following list of post titles into the target language: " . $target_lang . ".\n\n";
                $prompt .= "Requirements:\n";
                $prompt .= "1. Return the translated titles as a JSON array of strings in the exact same order.\n";
                $prompt .= "2. Do not return any other text, explanations, or code blocks. Return only a valid JSON array of strings.\n";
                $prompt .= "3. Keep HTML entities or brand names intact if appropriate.\n\n";
                $prompt .= "List of titles to translate:\n" . json_encode( $titles, JSON_UNESCAPED_UNICODE );

                $translated_text = $this->call_gemini_api( $prompt, $api_key, true );

                if ( is_wp_error( $translated_text ) ) {
                    wp_send_json_error( array( 'message' => $translated_text->get_error_message() ) );
                }

                // Làm sạch mã block markdown nếu Gemini trả về
                $translated_text = preg_replace( '/^```(?:json)?/i', '', $translated_text );
                $translated_text = preg_replace( '/```$/i', '', $translated_text );
                $translated_text = trim( $translated_text );

                $translated_titles = json_decode( $translated_text, true );

                if ( ! is_array( $translated_titles ) ) {
                    $translated_titles = array_map( 'trim', explode( "\n", $translated_text ) );
                    $translated_titles = array_map( function( $item ) {
                        return trim( $item, " \t\n\r\0\x0B\",[]" );
                    }, $translated_titles );
                    $translated_titles = array_values( array_filter( $translated_titles ) );
                }

                wp_send_json_success( $translated_titles );
            } else {
                // Dịch cả tiêu đề, nội dung và mô tả ngắn bằng Gemini
                $posts_data = isset( $_POST['posts_data'] ) ? $_POST['posts_data'] : array();
                if ( empty( $posts_data ) ) {
                    wp_send_json_error( array( 'message' => __( 'Danh sách bài viết cần dịch không được để trống.', 'wp-acf-smart-importer' ) ) );
                }

                if ( is_string( $posts_data ) ) {
                    $posts_data = json_decode( wp_unslash( $posts_data ), true );
                }

                $items_to_translate = array();
                foreach ( $posts_data as $post ) {
                    $items_to_translate[] = array(
                        'id'      => intval( $post['id'] ),
                        'title'   => sanitize_text_field( $post['title'] ),
                        'content' => wp_kses_post( wp_unslash( $post['content'] ) ),
                        'excerpt' => sanitize_textarea_field( wp_unslash( $post['excerpt'] ) ),
                    );
                }

                $prompt  = "You are a professional translator.\n";
                $prompt .= "Translate the following list of post objects (containing title, HTML content, and excerpt) into the target language: " . $target_lang . ".\n\n";
                $prompt .= "Requirements:\n";
                $prompt .= "1. Return the output as a valid JSON array of objects with the exact same keys: 'id', 'title', 'content', and 'excerpt'.\n";
                $prompt .= "2. For the 'content' field: DO NOT break or alter any HTML tags (such as <div>, <p>, <img>, <a>, figure, and their attributes). Translate ONLY the text nodes inside the HTML.\n";
                $prompt .= "3. Keep the JSON order exactly the same.\n";
                $prompt .= "4. Do not output any markdown code blocks (like ```json) or explanations. Return ONLY the raw JSON string.\n\n";
                $prompt .= "Data to translate:\n" . json_encode( $items_to_translate, JSON_UNESCAPED_UNICODE );

                $translated_text = $this->call_gemini_api( $prompt, $api_key, true );

                if ( is_wp_error( $translated_text ) ) {
                    wp_send_json_error( array( 'message' => $translated_text->get_error_message() ) );
                }

                // Làm sạch mã block markdown nếu Gemini trả về
                $translated_text = preg_replace( '/^```(?:json)?/i', '', $translated_text );
                $translated_text = preg_replace( '/```$/i', '', $translated_text );
                $translated_text = trim( $translated_text );

                $translated_data = json_decode( $translated_text, true );

                if ( ! is_array( $translated_data ) ) {
                    wp_send_json_error( array( 'message' => __( 'Lỗi: AI không phản hồi đúng định dạng JSON Array cho nội dung.', 'wp-acf-smart-importer' ) ) );
                }

                wp_send_json_success( $translated_data );
            }
        }
    }

    /**
     * Helper sinh chuỗi nội dung Markdown từ dữ liệu tài liệu
     */
    private function generate_docs_markdown_content( $data ) {
        $project_name = ! empty( $data['overview']['name'] ) ? $data['overview']['name'] : get_bloginfo( 'name' );
        $url = ! empty( $data['overview']['url'] ) ? $data['overview']['url'] : home_url();
        $git_repo = ! empty( $data['overview']['git_repo'] ) ? $data['overview']['git_repo'] : '';
        $lead_dev = ! empty( $data['overview']['lead_dev'] ) ? $data['overview']['lead_dev'] : '';
        $desc = ! empty( $data['overview']['description'] ) ? $data['overview']['description'] : '';

        $md = "# TÀI LIỆU CHI TIẾT DỰ ÁN: " . strtoupper( $project_name ) . "\n\n";
        $md .= "Tài liệu kỹ thuật tổng hợp thông tin, nhật ký phát triển và thư viện UI components được xây dựng cho dự án.\n\n";
        
        $md .= "## 1. THÔNG TIN TỔNG QUAN (OVERVIEW)\n\n";
        $md .= "- **Tên dự án**: " . $project_name . "\n";
        $md .= "- **Website**: [" . $url . "](" . $url . ")\n";
        if ( $git_repo ) {
            $md .= "- **Repository Git**: " . $git_repo . "\n";
        }
        if ( $lead_dev ) {
            $md .= "- **Lập trình viên chính**: " . $lead_dev . "\n";
        }
        $md .= "- **Ngày tạo tài liệu**: " . date( 'Y-m-d H:i:s' ) . "\n\n";
        
        if ( $desc ) {
            $md .= "### Mô tả Dự án\n";
            $md .= $desc . "\n\n";
        }

        // Nhật ký công việc
        $md .= "## 2. NHẬT KÝ CÔNG VIỆC & CHANGELOG\n\n";
        if ( ! empty( $data['worklogs'] ) && is_array( $data['worklogs'] ) ) {
            foreach ( $data['worklogs'] as $log ) {
                $md .= "### 📅 " . ( ! empty( $log['date'] ) ? $log['date'] : date( 'Y-m-d' ) ) . " - " . $log['title'] . "\n";
                $md .= "- **Thực hiện bởi**: " . ( ! empty( $log['developer'] ) ? $log['developer'] : 'N/A' ) . "\n";
                if ( ! empty( $log['files'] ) ) {
                    $md .= "- **Files chỉnh sửa**: `" . $log['files'] . "`\n";
                }
                if ( ! empty( $log['description'] ) ) {
                    $md .= "- **Mô tả chi tiết**:\n" . $log['description'] . "\n";
                }
                $md .= "\n";
            }
        } else {
            $md .= "*(Chưa có nhật ký công việc nào được ghi nhận)*\n\n";
        }

        // UI Components
        $md .= "## 3. THƯ VIỆN UI COMPONENTS & CODE SNIPPETS\n\n";
        if ( ! empty( $data['components'] ) && is_array( $data['components'] ) ) {
            foreach ( $data['components'] as $comp ) {
                $md .= "### ❖ " . $comp['name'] . " (Phân loại: " . ( ! empty( $comp['category'] ) ? $comp['category'] : 'Chung' ) . ")\n\n";
                if ( ! empty( $comp['description'] ) ) {
                    $md .= "**Mô tả & Hướng dẫn sử dụng**:\n" . $comp['description'] . "\n\n";
                }
                
                if ( ! empty( $comp['html'] ) ) {
                    $md .= "#### HTML\n";
                    $md .= "```html\n" . $comp['html'] . "\n```\n\n";
                }
                
                if ( ! empty( $comp['css'] ) ) {
                    $md .= "#### CSS\n";
                    $md .= "```css\n" . $comp['css'] . "\n```\n\n";
                }
                
                if ( ! empty( $comp['js'] ) ) {
                    $md .= "#### Javascript\n";
                    $md .= "```javascript\n" . $comp['js'] . "\n```\n\n";
                }
                $md .= "---\n\n";
            }
        } else {
            $md .= "*(Chưa có UI component nào được tạo)*\n\n";
        }

        // Ghi chú kỹ thuật
        $md .= "## 4. GHI CHÚ KỸ THUẬT & HƯỚNG DẪN DEPLOY\n\n";
        if ( ! empty( $data['notes'] ) ) {
            $md .= $data['notes'] . "\n\n";
        } else {
            $md .= "*(Chưa có ghi chú kỹ thuật nào)*\n\n";
        }

        return $md;
    }

    /**
     * Tự động khám phá danh sách các model khả dụng cho API Key hiện tại
     */
    private function get_available_gemini_endpoints( $api_key ) {
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
     * Helper gọi API Gemini với cơ chế tự sửa lỗi, chuyển đổi dự phòng
     * và hỗ trợ quay vòng endpoint/model để tránh lỗi 404.
     */
    private function call_gemini_api( $prompt, $api_key, $response_mime_json = false ) {
        if ( function_exists( 'set_time_limit' ) ) {
            @set_time_limit( 180 );
        }

        $endpoints = $this->get_available_gemini_endpoints( $api_key );

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
                continue; // Thử model/endpoint tiếp theo
            }

            $res_body = wp_remote_retrieve_body( $response );
            $res_data = json_decode( $res_body, true );

            if ( ! empty( $res_data['candidates'][0]['content']['parts'][0]['text'] ) ) {
                return $res_data['candidates'][0]['content']['parts'][0]['text'];
            }
        }

        return new WP_Error( 'gemini_failed', __( 'Tất cả các models/endpoints kết nối Gemini đều thất bại. Nhật ký lỗi chi tiết: ', 'wp-acf-smart-importer' ) . implode( ' --- ', $error_log ) );
    }

    /**
     * Map tên ngôn ngữ sang mã ngôn ngữ Google Translate (ISO 639-1)
     */
    private static function get_google_translate_lang_code( $lang_name ) {
        $map = array(
            'English'             => 'en',
            'Japanese'            => 'ja',
            'Chinese (Simplified)' => 'zh-CN',
            'Korean'              => 'ko',
            'French'              => 'fr',
            'German'              => 'de',
            'Spanish'             => 'es',
            'Russian'             => 'ru',
            'Vietnamese'          => 'vi',
        );

        return isset( $map[ $lang_name ] ) ? $map[ $lang_name ] : 'en';
    }

    /**
     * Dịch một chuỗi văn bản thô qua Google Translate API miễn phí
     */
    public static function translate_via_google_free( $text, $target_lang_code ) {
        if ( empty( $text ) || trim( $text ) === '' ) {
            return $text;
        }

        $url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=' . urlencode( $target_lang_code ) . '&dt=t&q=' . urlencode( $text );

        $response = wp_remote_get( $url, array(
            'timeout'   => 15,
            'sslverify' => false,
        ) );

        if ( is_wp_error( $response ) ) {
            return $text; // Fallback trả về text gốc nếu lỗi
        }

        $code = wp_remote_retrieve_response_code( $response );
        if ( 200 !== $code ) {
            return $text;
        }

        $body = wp_remote_retrieve_body( $response );
        $data = json_decode( $body, true );

        if ( isset( $data[0] ) && is_array( $data[0] ) ) {
            $translated = '';
            foreach ( $data[0] as $sentence ) {
                if ( isset( $sentence[0] ) ) {
                    $translated .= $sentence[0];
                }
            }
            return $translated;
        }

        return $text;
    }

    /**
     * Dịch nội dung HTML qua Google Translate miễn phí tối ưu (1 request duy nhất)
     */
    public static function translate_html_via_google_free( $html, $target_lang_code ) {
        if ( empty( $html ) || trim( $html ) === '' ) {
            return $html;
        }

        $dom = new DOMDocument();
        libxml_use_internal_errors( true );
        // Bắt buộc nạp XML encoding UTF-8 để bảo toàn ký tự unicode
        $dom->loadHTML( '<?xml encoding="UTF-8"><div id="gt-root">' . $html . '</div>', LIBXML_HTML_NOIMPLIED | LIBXML_HTML_NODEFDTD );
        libxml_clear_errors();

        $xpath = new DOMXPath( $dom );
        $text_nodes = $xpath->query( '//text()[not(parent::script) and not(parent::style)]' );

        $texts_to_translate = array();
        $nodes_map = array();

        foreach ( $text_nodes as $node ) {
            $trimmed = trim( $node->nodeValue );
            if ( $trimmed === '' || is_numeric( $trimmed ) ) {
                continue;
            }
            $texts_to_translate[] = $node->nodeValue;
            $nodes_map[] = $node;
        }

        if ( empty( $texts_to_translate ) ) {
            return $html;
        }

        // Gộp các chuỗi bằng ký tự phân tách đặc biệt mà Google Translate không dịch
        $separator = "\n---[wpsai-sep]---\n";
        $combined_text = implode( $separator, $texts_to_translate );

        // Dịch toàn bộ văn bản gộp
        $translated_combined = self::translate_via_google_free( $combined_text, $target_lang_code );

        // Tách chuỗi dịch trở lại
        $translated_texts = explode( trim( $separator ), $translated_combined );

        foreach ( $nodes_map as $idx => $node ) {
            if ( isset( $translated_texts[ $idx ] ) ) {
                // Sử dụng htmlspecialchars để đảm bảo chuỗi gán vào node an toàn
                $node->nodeValue = htmlspecialchars( trim( $translated_texts[ $idx ] ), ENT_NOQUOTES, 'UTF-8' );
            }
        }

        $root = $dom->getElementById( 'gt-root' );
        if ( $root ) {
            $new_html = '';
            foreach ( $root->childNodes as $child ) {
                $new_html .= $dom->saveHTML( $child );
            }
            return $new_html;
        }

        return $html;
    }

    // ============================================================
    // SNAPSHOT DATA REPOSITORY - Kho Lưu Trữ Dữ Liệu Mẫu
    // ============================================================

    /**
     * Lấy đường dẫn thư mục snapshot
     */
    private function get_snapshot_dir() {
        $upload_dir = wp_upload_dir();
        $dir = trailingslashit( $upload_dir['basedir'] ) . 'wpsai-snapshots';
        if ( ! file_exists( $dir ) ) {
            wp_mkdir_p( $dir );
            // Tạo file .htaccess để bảo vệ thư mục
            file_put_contents( $dir . '/.htaccess', "Options -Indexes\nDeny from all\n" );
            file_put_contents( $dir . '/index.php', '<?php // Silence is golden.' );
        }
        return $dir;
    }

    /**
     * Quét toàn bộ bài viết của 1 Post Type -> Trả preview JSON
     */
    public function snapshot_scan() {
        $this->verify_security();
        set_time_limit( 180 );

        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $taxonomy  = isset( $_POST['taxonomy'] ) ? sanitize_text_field( $_POST['taxonomy'] ) : '';
        $term_id   = isset( $_POST['term_id'] ) ? intval( $_POST['term_id'] ) : 0;
        $paged     = isset( $_POST['paged'] ) ? intval( $_POST['paged'] ) : 1;
        $per_page  = 500;

        // Build query args
        $args = array(
            'post_type'      => $post_type,
            'posts_per_page' => $per_page,
            'paged'          => $paged,
            'post_status'    => array( 'publish', 'draft', 'pending', 'private' ),
            'orderby'        => 'ID',
            'order'          => 'ASC',
        );

        // Lọc theo Taxonomy/Term nếu có
        if ( ! empty( $taxonomy ) && $term_id > 0 ) {
            $args['tax_query'] = array(
                array(
                    'taxonomy' => $taxonomy,
                    'field'    => 'term_id',
                    'terms'    => $term_id,
                ),
            );
        }

        $query = new WP_Query( $args );
        $posts_data = array();

        // Lấy danh sách ACF fields cho Post Type
        $acf_fields = WP_ACF_Smart_Importer_Generator::get_acf_fields_for_post_type( $post_type );

        // Lấy taxonomies công khai
        $taxonomies = get_object_taxonomies( $post_type, 'objects' );
        $public_taxonomies = array();
        if ( is_array( $taxonomies ) ) {
            foreach ( $taxonomies as $tax_slug => $tax_obj ) {
                if ( $tax_obj->public ) {
                    $public_taxonomies[ $tax_slug ] = $tax_obj->label;
                }
            }
        }

        // Build schema
        $schema = array(
            array( 'name' => 'post_title', 'label' => 'Tiêu đề', 'type' => 'wp_core' ),
            array( 'name' => 'post_content', 'label' => 'Nội dung', 'type' => 'wp_core' ),
            array( 'name' => 'post_excerpt', 'label' => 'Mô tả ngắn', 'type' => 'wp_core' ),
            array( 'name' => 'post_date', 'label' => 'Ngày đăng', 'type' => 'wp_core' ),
            array( 'name' => 'post_status', 'label' => 'Trạng thái', 'type' => 'wp_core' ),
            array( 'name' => 'post_name', 'label' => 'Slug', 'type' => 'wp_core' ),
            array( 'name' => 'featured_image', 'label' => 'Ảnh đại diện', 'type' => 'wp_core' ),
        );

        foreach ( $acf_fields as $f ) {
            $schema[] = array(
                'name'  => 'acf_' . $f['name'],
                'label' => '[ACF] ' . $f['label'],
                'type'  => 'acf_' . $f['type'],
            );
        }

        foreach ( $public_taxonomies as $tax_slug => $tax_label ) {
            $schema[] = array(
                'name'  => 'tax_' . $tax_slug,
                'label' => '[Taxonomy] ' . $tax_label,
                'type'  => 'taxonomy',
            );
        }

        // Danh sách meta keys hệ thống cần loại bỏ
        $system_meta_prefixes = array( '_edit_', '_thumbnail_id', '_wp_', '_acf-', '_oembed', '_pingme', '_encloseme', '_yoast_', '_aioseo_' );

        foreach ( $query->posts as $post ) {
            $row = array(
                'post_id'      => $post->ID,
                'post_title'   => $post->post_title,
                'post_content' => $post->post_content,
                'post_excerpt' => $post->post_excerpt,
                'post_date'    => $post->post_date,
                'post_status'  => $post->post_status,
                'post_name'    => $post->post_name,
            );

            // Ảnh đại diện
            $thumb_url = get_the_post_thumbnail_url( $post->ID, 'full' );
            $row['featured_image'] = $thumb_url ? $thumb_url : '';

            // ACF Fields
            foreach ( $acf_fields as $f ) {
                $val = WP_ACF_Smart_Importer_Generator::get_acf_field_value( $f['name'], $post->ID );
                if ( is_array( $val ) ) {
                    $row[ 'acf_' . $f['name'] ] = json_encode( $val, JSON_UNESCAPED_UNICODE );
                } else {
                    $row[ 'acf_' . $f['name'] ] = $val !== null ? $val : '';
                }
            }

            // Taxonomy terms
            foreach ( $public_taxonomies as $tax_slug => $tax_label ) {
                $terms = wp_get_object_terms( $post->ID, $tax_slug, array( 'fields' => 'all' ) );
                if ( ! is_wp_error( $terms ) && ! empty( $terms ) ) {
                    // Xây đường dẫn phân cấp
                    $term_paths = array();
                    foreach ( $terms as $term ) {
                        if ( is_taxonomy_hierarchical( $tax_slug ) && $term->parent > 0 ) {
                            $ancestors = get_ancestors( $term->term_id, $tax_slug, 'taxonomy' );
                            $path_parts = array();
                            foreach ( array_reverse( $ancestors ) as $ancestor_id ) {
                                $ancestor = get_term( $ancestor_id, $tax_slug );
                                if ( $ancestor && ! is_wp_error( $ancestor ) ) {
                                    $path_parts[] = $ancestor->name;
                                }
                            }
                            $path_parts[] = $term->name;
                            $term_paths[] = implode( ' > ', $path_parts );
                        } else {
                            $term_paths[] = $term->name;
                        }
                    }
                    $row[ 'tax_' . $tax_slug ] = implode( ', ', $term_paths );
                } else {
                    $row[ 'tax_' . $tax_slug ] = '';
                }
            }

            $posts_data[] = $row;
        }

        wp_send_json_success( array(
            'schema'       => $schema,
            'posts'        => $posts_data,
            'post_count'   => $query->found_posts,
            'total_pages'  => $query->max_num_pages,
            'current_page' => $paged,
            'post_type'    => $post_type,
        ) );
    }

    /**
     * Lưu snapshot JSON lên ổ đĩa
     */
    public function snapshot_save() {
        $this->verify_security();

        $snapshot_name = isset( $_POST['snapshot_name'] ) ? sanitize_text_field( $_POST['snapshot_name'] ) : '';
        $snapshot_data = isset( $_POST['snapshot_data'] ) ? wp_unslash( $_POST['snapshot_data'] ) : '';
        $post_type     = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $post_count    = isset( $_POST['post_count'] ) ? intval( $_POST['post_count'] ) : 0;

        if ( empty( $snapshot_name ) || empty( $snapshot_data ) ) {
            wp_send_json_error( array( 'message' => __( 'Thiếu tên snapshot hoặc dữ liệu.', 'wp-acf-smart-importer' ) ) );
        }

        $data = json_decode( $snapshot_data, true );
        if ( json_last_error() !== JSON_ERROR_NONE ) {
            wp_send_json_error( array( 'message' => __( 'Dữ liệu JSON không hợp lệ.', 'wp-acf-smart-importer' ) ) );
        }

        $dir = $this->get_snapshot_dir();
        $snapshot_id = 'snapshot-' . $post_type . '-' . time() . '-' . wp_generate_password( 6, false, false );
        $filename = $snapshot_id . '.json';
        $filepath = $dir . '/' . $filename;

        // Tạo cấu trúc file JSON
        $json_content = array(
            'meta' => array(
                'id'             => $snapshot_id,
                'name'           => $snapshot_name,
                'post_type'      => $post_type,
                'post_count'     => $post_count,
                'created_at'     => current_time( 'Y-m-d H:i:s' ),
                'plugin_version' => defined( 'WPSAI_VERSION' ) ? WPSAI_VERSION : '1.0.0',
                'site_url'       => home_url(),
            ),
            'schema' => isset( $data['schema'] ) ? $data['schema'] : array(),
            'posts'  => isset( $data['posts'] ) ? $data['posts'] : array(),
        );

        $json_string = wp_json_encode( $json_content, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT );
        $written = file_put_contents( $filepath, $json_string );

        if ( false === $written ) {
            wp_send_json_error( array( 'message' => __( 'Không thể ghi file snapshot lên ổ đĩa.', 'wp-acf-smart-importer' ) ) );
        }

        // Cập nhật registry trong wp_options
        $registry = get_option( 'wpsai_snapshots_registry', array() );
        $registry[] = array(
            'id'         => $snapshot_id,
            'name'       => $snapshot_name,
            'post_type'  => $post_type,
            'post_count' => $post_count,
            'file_path'  => $filepath,
            'file_size'  => filesize( $filepath ),
            'created_at' => current_time( 'Y-m-d H:i:s' ),
        );
        update_option( 'wpsai_snapshots_registry', $registry );

        wp_send_json_success( array(
            'message'     => sprintf( __( 'Đã lưu snapshot "%s" thành công (%s).', 'wp-acf-smart-importer' ), $snapshot_name, size_format( filesize( $filepath ) ) ),
            'snapshot_id' => $snapshot_id,
        ) );
    }

    /**
     * Lấy danh sách tất cả snapshot đã lưu
     */
    public function snapshot_list() {
        $this->verify_security();

        $registry = get_option( 'wpsai_snapshots_registry', array() );

        // Kiểm tra file tồn tại thực tế
        $valid = array();
        foreach ( $registry as $item ) {
            if ( file_exists( $item['file_path'] ) ) {
                $item['file_size_formatted'] = size_format( $item['file_size'] );
                $valid[] = $item;
            }
        }

        // Cập nhật registry nếu có thay đổi
        if ( count( $valid ) !== count( $registry ) ) {
            update_option( 'wpsai_snapshots_registry', $valid );
        }

        wp_send_json_success( array(
            'snapshots' => array_reverse( $valid ), // Mới nhất lên đầu
            'total'     => count( $valid ),
        ) );
    }

    /**
     * Xem chi tiết nội dung 1 snapshot
     */
    public function snapshot_detail() {
        $this->verify_security();

        $snapshot_id = isset( $_POST['snapshot_id'] ) ? sanitize_text_field( $_POST['snapshot_id'] ) : '';
        if ( empty( $snapshot_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Thiếu ID snapshot.', 'wp-acf-smart-importer' ) ) );
        }

        $registry = get_option( 'wpsai_snapshots_registry', array() );
        $found = null;
        foreach ( $registry as $item ) {
            if ( $item['id'] === $snapshot_id ) {
                $found = $item;
                break;
            }
        }

        if ( ! $found || ! file_exists( $found['file_path'] ) ) {
            wp_send_json_error( array( 'message' => __( 'Snapshot không tồn tại hoặc file đã bị xóa.', 'wp-acf-smart-importer' ) ) );
        }

        $content = file_get_contents( $found['file_path'] );
        $data = json_decode( $content, true );

        if ( json_last_error() !== JSON_ERROR_NONE ) {
            wp_send_json_error( array( 'message' => __( 'File snapshot bị hỏng (lỗi JSON).', 'wp-acf-smart-importer' ) ) );
        }

        wp_send_json_success( array(
            'meta'   => $data['meta'],
            'schema' => $data['schema'],
            'posts'  => $data['posts'],
        ) );
    }

    /**
     * Khôi phục (import) bài viết từ snapshot
     */
    public function snapshot_restore() {
        $this->verify_security();
        set_time_limit( 300 );

        $snapshot_id  = isset( $_POST['snapshot_id'] ) ? sanitize_text_field( $_POST['snapshot_id'] ) : '';
        $restore_mode = isset( $_POST['restore_mode'] ) ? sanitize_text_field( $_POST['restore_mode'] ) : 'create_new';
        $post_index   = isset( $_POST['post_index'] ) ? intval( $_POST['post_index'] ) : 0;

        if ( empty( $snapshot_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Thiếu ID snapshot.', 'wp-acf-smart-importer' ) ) );
        }

        $registry = get_option( 'wpsai_snapshots_registry', array() );
        $found = null;
        foreach ( $registry as $item ) {
            if ( $item['id'] === $snapshot_id ) {
                $found = $item;
                break;
            }
        }

        if ( ! $found || ! file_exists( $found['file_path'] ) ) {
            wp_send_json_error( array( 'message' => __( 'Snapshot không tồn tại.', 'wp-acf-smart-importer' ) ) );
        }

        $content = file_get_contents( $found['file_path'] );
        $data = json_decode( $content, true );

        if ( ! isset( $data['posts'][ $post_index ] ) ) {
            wp_send_json_error( array( 'message' => __( 'Chỉ số bài viết không hợp lệ.', 'wp-acf-smart-importer' ) ) );
        }

        $post_data = $data['posts'][ $post_index ];
        $post_type = $data['meta']['post_type'];

        // Chuẩn bị row và mapping cho Engine
        $row = array();
        $mapping = array();
        $col_index = 0;

        foreach ( $post_data as $field_name => $field_value ) {
            if ( $field_name === 'post_id' && $restore_mode === 'create_new' ) {
                continue; // Bỏ qua post_id khi tạo mới
            }
            $col_key = 'col_' . $col_index;
            $row[ $col_key ] = $field_value;
            $mapping[ $field_name ] = $col_key;
            $col_index++;
        }

        $post_status = isset( $post_data['post_status'] ) ? $post_data['post_status'] : 'draft';
        $result_post_id = WP_ACF_Smart_Importer_Engine::import_single_row( $row, $mapping, $post_type, $post_status );

        if ( is_wp_error( $result_post_id ) ) {
            wp_send_json_error( array(
                'message'    => $result_post_id->get_error_message(),
                'post_index' => $post_index,
            ) );
        }

        wp_send_json_success( array(
            'post_id'    => $result_post_id,
            'post_title' => get_the_title( $result_post_id ),
            'permalink'  => get_permalink( $result_post_id ),
            'post_index' => $post_index,
        ) );
    }

    /**
     * Xóa 1 snapshot (file + registry)
     */
    public function snapshot_delete() {
        $this->verify_security();

        $snapshot_id = isset( $_POST['snapshot_id'] ) ? sanitize_text_field( $_POST['snapshot_id'] ) : '';
        if ( empty( $snapshot_id ) ) {
            wp_send_json_error( array( 'message' => __( 'Thiếu ID snapshot.', 'wp-acf-smart-importer' ) ) );
        }

        $registry = get_option( 'wpsai_snapshots_registry', array() );
        $new_registry = array();
        $deleted = false;

        foreach ( $registry as $item ) {
            if ( $item['id'] === $snapshot_id ) {
                // Xóa file JSON
                if ( file_exists( $item['file_path'] ) ) {
                    @unlink( $item['file_path'] );
                }
                $deleted = true;
            } else {
                $new_registry[] = $item;
            }
        }

        if ( ! $deleted ) {
            wp_send_json_error( array( 'message' => __( 'Snapshot không tồn tại trong danh sách.', 'wp-acf-smart-importer' ) ) );
        }

        update_option( 'wpsai_snapshots_registry', $new_registry );

        wp_send_json_success( array(
            'message' => __( 'Đã xóa snapshot thành công.', 'wp-acf-smart-importer' ),
        ) );
    }

    /**
     * AJAX: Lấy chỉ mục cây manifest.json
     */
    public function tree_get_manifest() {
        $this->verify_security();
        $manifest = WP_ACF_Smart_Importer_Tree::get_manifest();
        wp_send_json_success( $manifest );
    }

    /**
     * AJAX: Quét bài viết của một nút cụ thể trên Cây và lưu dạng Chunk
     */
    public function tree_scan_and_save_node() {
        $this->verify_security();
        set_time_limit( 180 );

        $node_id   = isset( $_POST['node_id'] ) ? sanitize_text_field( $_POST['node_id'] ) : '';
        $post_type = isset( $_POST['post_type'] ) ? sanitize_text_field( $_POST['post_type'] ) : 'post';
        $taxonomy  = isset( $_POST['taxonomy'] ) ? sanitize_text_field( $_POST['taxonomy'] ) : '';
        $term_id   = isset( $_POST['term_id'] ) ? intval( $_POST['term_id'] ) : 0;

        if ( empty( $node_id ) || empty( $post_type ) ) {
            wp_send_json_error( array( 'message' => __( 'Thiếu thông tin nút dữ liệu.', 'wp-acf-smart-importer' ) ) );
        }

        // Tạm sử dụng hàm quét bài viết sẵn có
        $_POST['post_type'] = $post_type;
        $_POST['taxonomy']  = $taxonomy;
        $_POST['term_id']   = $term_id;

        // Quét dữ liệu
        $args = array(
            'post_type'      => $post_type,
            'posts_per_page' => 200, // Quét tối đa 200 bài mỗi lần
            'post_status'    => array( 'publish', 'draft', 'pending', 'private' ),
            'orderby'        => 'ID',
            'order'          => 'ASC',
        );

        if ( ! empty( $taxonomy ) && $term_id > 0 ) {
            $args['tax_query'] = array(
                array(
                    'taxonomy' => $taxonomy,
                    'field'    => 'term_id',
                    'terms'    => $term_id,
                ),
            );
        }

        $query = new WP_Query( $args );
        $acf_fields = WP_ACF_Smart_Importer_Generator::get_acf_fields_for_post_type( $post_type );

        $posts_data = array();
        foreach ( $query->posts as $post ) {
            $row = array(
                'post_id'      => $post->ID,
                'post_title'   => $post->post_title,
                'post_content' => $post->post_content,
                'post_excerpt' => $post->post_excerpt,
                'post_date'    => $post->post_date,
                'post_status'  => $post->post_status,
                'featured_image' => get_the_post_thumbnail_url( $post->ID, 'full' ) ?: '',
            );

            foreach ( $acf_fields as $f ) {
                $val = WP_ACF_Smart_Importer_Generator::get_acf_field_value( $f['name'], $post->ID );
                $row[ 'acf_' . $f['name'] ] = is_array( $val ) ? json_encode( $val, JSON_UNESCAPED_UNICODE ) : ( $val !== null ? $val : '' );
            }

            $posts_data[] = $row;
        }

        if ( empty( $posts_data ) ) {
            wp_send_json_error( array( 'message' => __( 'Không tìm thấy bài viết nào thuộc nút này.', 'wp-acf-smart-importer' ) ) );
        }

        // Lưu dữ liệu vào file chunk và cập nhật chỉ mục Cây
        $chunks = WP_ACF_Smart_Importer_Tree::save_chunk_for_node( $node_id, $post_type, $posts_data );

        wp_send_json_success( array(
            'message'    => sprintf( __( 'Đã lưu %d bài viết thành %d file chunk.', 'wp-acf-smart-importer' ), count( $posts_data ), count( $chunks ) ),
            'post_count' => count( $posts_data ),
            'chunks'     => $chunks,
        ) );
    }

    /**
     * AJAX: Đọc dữ liệu từ file chunk
     */
    public function tree_get_chunk_data() {
        $this->verify_security();

        $file_rel = isset( $_POST['file_rel'] ) ? sanitize_text_field( $_POST['file_rel'] ) : '';
        if ( empty( $file_rel ) ) {
            wp_send_json_error( array( 'message' => __( 'Thiếu đường dẫn chunk.', 'wp-acf-smart-importer' ) ) );
        }

        $data = WP_ACF_Smart_Importer_Tree::read_node_data( $file_rel );
        if ( is_wp_error( $data ) ) {
            wp_send_json_error( array( 'message' => $data->get_error_message() ) );
        }

        wp_send_json_success( $data );
    }
}

