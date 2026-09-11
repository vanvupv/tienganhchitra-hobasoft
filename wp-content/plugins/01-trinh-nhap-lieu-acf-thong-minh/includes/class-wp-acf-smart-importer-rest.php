<?php
/**
 * Lớp WP_ACF_Smart_Importer_REST
 * Đăng ký các endpoints REST API của WordPress để kết nối với Chrome Extension.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_ACF_Smart_Importer_REST {

    /**
     * Khởi tạo REST routes & CORS hooks
     */
    public function __construct() {
        add_action( 'rest_api_init', array( $this, 'register_routes' ) );
        add_filter( 'rest_allowed_cors_headers', array( $this, 'add_allowed_headers' ) );
        add_action( 'rest_pre_serve_request', array( $this, 'send_cors_headers' ), 10, 4 );
    }

    /**
     * Đăng ký các header bổ sung được phép gửi trong request CORS
     */
    public function add_allowed_headers( $headers ) {
        $headers[] = 'X-WPSAI-API-KEY';
        return $headers;
    }

    /**
     * Gửi các header CORS cho các yêu cầu REST API
     */
    public function send_cors_headers( $served, $result, $request, $server ) {
        $server->send_header( 'Access-Control-Allow-Origin', '*' );
        $server->send_header( 'Access-Control-Allow-Headers', 'X-WPSAI-API-KEY, Content-Type, Authorization' );
        $server->send_header( 'Access-Control-Allow-Methods', 'GET, POST, OPTIONS' );
        return $served;
    }

    /**
     * Đăng ký các REST API routes
     */
    public function register_routes() {
        register_rest_route( 'wpsai/v1', '/connect', array(
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => array( $this, 'handle_connect' ),
            'permission_callback' => array( $this, 'verify_permission' ),
        ) );

        register_rest_route( 'wpsai/v1', '/post-types', array(
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => array( $this, 'handle_get_post_types' ),
            'permission_callback' => array( $this, 'verify_permission' ),
        ) );

        register_rest_route( 'wpsai/v1', '/import', array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => array( $this, 'handle_import' ),
            'permission_callback' => array( $this, 'verify_permission' ),
        ) );
    }

    /**
     * Xác minh quyền truy cập bằng API Key
     */
    public function verify_permission( $request ) {
        $provided_key = $request->get_header( 'X-WPSAI-API-KEY' );
        if ( empty( $provided_key ) ) {
            $provided_key = $request->get_param( 'api_key' );
        }
        
        $saved_key = get_option( 'wpsai_extension_api_key', '' );
        
        // Nếu option trống, tự sinh một key ngẫu nhiên và lưu
        if ( empty( $saved_key ) ) {
            $saved_key = wp_generate_password( 24, false );
            update_option( 'wpsai_extension_api_key', $saved_key );
        }

        if ( empty( $provided_key ) || $provided_key !== $saved_key ) {
            return new WP_Error( 'rest_forbidden', __( 'API Key không hợp lệ hoặc thiếu.', 'wp-acf-smart-importer' ), array( 'status' => 403 ) );
        }

        return true;
    }

    /**
     * Kiểm tra kết nối từ Chrome Extension
     */
    public function handle_connect( $request ) {
        return rest_ensure_response( array(
            'success'   => true,
            'site_name' => get_bloginfo( 'name' ),
            'message'   => __( 'Kết nối thành công tới WordPress Smart Importer.', 'wp-acf-smart-importer' ),
        ) );
    }

    /**
     * Trả về danh sách Post Types và Taxonomies cho extension dropdowns
     */
    public function handle_get_post_types( $request ) {
        $post_types = get_post_types( array( 'public' => true ), 'objects' );
        $result = array();

        foreach ( $post_types as $slug => $obj ) {
            // Loại bỏ các post types hệ thống
            if ( in_array( $slug, array( 'attachment', 'revision', 'nav_menu_item', 'custom_css', 'customize_changeset', 'oembed_cache', 'user_request', 'wp_block', 'wp_template', 'wp_template_part', 'wp_navigation' ) ) ) {
                continue;
            }

            // Lấy các taxonomy công khai của Post Type
            $taxonomies = get_object_taxonomies( $slug, 'objects' );
            $formatted_taxes = array();
            
            foreach ( $taxonomies as $tax_slug => $tax_obj ) {
                if ( ! $tax_obj->public ) {
                    continue;
                }
                $formatted_taxes[] = array(
                    'slug'  => $tax_slug,
                    'label' => $tax_obj->label . ' (' . $tax_slug . ')',
                );
            }

            $result[] = array(
                'slug'       => $slug,
                'label'      => $obj->label . ' (' . $slug . ')',
                'taxonomies' => $formatted_taxes,
            );
        }

        return rest_ensure_response( array(
            'success' => true,
            'data'    => $result,
        ) );
  }

    /**
     * Nhập bài viết được cào từ Extension
     */
    public function handle_import( $request ) {
        $params = $request->get_json_params();
        if ( empty( $params ) ) {
            $params = $request->get_params();
        }

        $title       = isset( $params['title'] ) ? sanitize_text_field( $params['title'] ) : '';
        $content     = isset( $params['content'] ) ? wp_kses_post( $params['content'] ) : '';
        $image_url   = isset( $params['featured_image'] ) ? esc_url_raw( $params['featured_image'] ) : '';
        $post_type   = isset( $params['post_type'] ) ? sanitize_text_field( $params['post_type'] ) : 'post';
        $post_status = isset( $params['post_status'] ) ? sanitize_text_field( $params['post_status'] ) : 'draft';
        $taxonomy    = isset( $params['taxonomy'] ) ? sanitize_text_field( $params['taxonomy'] ) : '';
        $terms       = isset( $params['terms'] ) ? sanitize_text_field( $params['terms'] ) : '';

        if ( empty( $title ) ) {
            return new WP_Error( 'missing_title', __( 'Tiêu đề bài viết không được để trống.', 'wp-acf-smart-importer' ), array( 'status' => 400 ) );
        }

        // Chuẩn bị dòng và sơ đồ ánh xạ cho import engine
        $row = array(
            'title'          => $title,
            'content'        => $content,
            'featured_image' => $image_url,
        );

        $mapping = array(
            'post_title'     => 'title',
            'post_content'   => 'content',
            'featured_image' => 'featured_image',
        );

        if ( ! empty( $taxonomy ) && ! empty( $terms ) ) {
            $row['taxonomy_terms'] = $terms;
            $mapping[ 'tax_' . $taxonomy ] = 'taxonomy_terms';
        }

        // Tự động nhận diện các trường tùy chỉnh (custom fields) gửi kèm từ extension
        foreach ( $params as $key => $val ) {
            if ( ! in_array( $key, array( 'title', 'content', 'featured_image', 'post_type', 'post_status', 'taxonomy', 'terms', 'api_key' ) ) ) {
                $row[ $key ] = sanitize_text_field( $val );
                $mapping[ 'acf_' . $key ] = $key;
            }
        }

        // Gọi trực tiếp Engine để lưu
        require_once WPSAI_PATH . 'includes/class-wp-acf-smart-importer-engine.php';
        $post_id = WP_ACF_Smart_Importer_Engine::import_single_row( $row, $mapping, $post_type, $post_status );

        if ( is_wp_error( $post_id ) ) {
            return new WP_Error( 'import_failed', $post_id->get_error_message(), array( 'status' => 500 ) );
        }

        return rest_ensure_response( array(
            'success'   => true,
            'post_id'   => $post_id,
            'title'     => get_the_title( $post_id ),
            'permalink' => get_permalink( $post_id ),
            'message'   => __( 'Đã nhập bài viết thành công từ Chrome Extension!', 'wp-acf-smart-importer' ),
        ) );
    }
}
new WP_ACF_Smart_Importer_REST();
