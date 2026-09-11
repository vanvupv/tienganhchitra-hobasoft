<?php
/**
 * WP Security Shield - Bộ Điều Phối AJAX
 * Quản lý các yêu cầu gọi từ JavaScript Dashboard và xác minh quyền.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_Security_Shield_Ajax_Handler {

    public function __construct() {
        $ajax_actions = array(
            'security_shield_scan_uploads',
            'security_shield_scan_themes',
            'security_shield_scan_db',
            'security_shield_scan_pages',
            'security_shield_save_scan_meta',
            'security_shield_delete_file',
            'security_shield_fix_db',
            'security_shield_restore_single_file',
            'security_shield_create_backup',
            'security_shield_create_snapshot',
            'security_shield_restore_backup',
            'security_shield_delete_backup',
            'security_shield_get_uploads_list',
            'security_shield_get_posts_to_scan',
            'security_shield_scan_post_item',
            'security_shield_get_suspicious_files',
            'security_shield_add_suspicious_file',
            'security_shield_remove_suspicious_file',
            'security_shield_scan_suspicious_file',
            'security_shield_delete_suspicious_file_physically',
            'security_shield_sync_rules',
            'security_shield_save_rules_url',
            'security_shield_save_hardening_progress'
        );

        foreach ( $ajax_actions as $action ) {
            add_action( 'wp_ajax_' . $action, array( $this, $action ) );
        }
    }

    private function verify_request() {
        check_ajax_referer( 'wp_security_shield_nonce', 'nonce' );
        
        if ( ! current_user_can( 'manage_options' ) ) {
            wp_send_json_error( array( 'message' => 'Bạn không có quyền thực hiện hành động này.' ) );
        }
    }

    public function security_shield_scan_uploads() {
        $this->verify_request();
        $scanner = new WP_Security_Shield_Scanner();
        $res = $scanner->scan_uploads();
        wp_send_json_success( $res );
    }

    public function security_shield_scan_themes() {
        $this->verify_request();
        $scanner = new WP_Security_Shield_Scanner();
        $res = $scanner->scan_themes();
        wp_send_json_success( $res );
    }

    public function security_shield_scan_db() {
        $this->verify_request();
        $scanner = new WP_Security_Shield_Scanner();
        $res = $scanner->scan_database();
        wp_send_json_success( $res );
    }

    public function security_shield_scan_pages() {
        $this->verify_request();
        $scanner = new WP_Security_Shield_Scanner();
        $res = $scanner->scan_pages();
        wp_send_json_success( $res );
    }

    public function security_shield_save_scan_meta() {
        $this->verify_request();
        
        $total_malware = isset( $_POST['total_malware'] ) ? intval( $_POST['total_malware'] ) : 0;
        $total_missing = isset( $_POST['total_missing'] ) ? intval( $_POST['total_missing'] ) : 0;
        
        update_option( 'wp_security_shield_last_scan', current_time( 'mysql' ) );
        update_option( 'wp_security_shield_scan_results', array(
            'total_malware' => $total_malware,
            'total_missing' => $total_missing
        ) );
        
        wp_send_json_success();
    }

    public function security_shield_delete_file() {
        $this->verify_request();
        
        $filepath = isset( $_POST['filepath'] ) ? sanitize_text_field( $_POST['filepath'] ) : '';
        if ( empty( $filepath ) ) {
            wp_send_json_error( array( 'message' => 'Đường dẫn tệp không hợp lệ.' ) );
        }

        $absolute_path = wp_normalize_path( ABSPATH . ltrim( $filepath, '/' ) );
        $uploads_dir = wp_normalize_path( wp_upload_dir()['basedir'] );
        $themes_dir = wp_normalize_path( get_theme_root() );

        $is_in_uploads = ( strpos( $absolute_path, $uploads_dir ) === 0 );
        $is_in_themes  = ( strpos( $absolute_path, $themes_dir ) === 0 );

        if ( ! $is_in_uploads && ! $is_in_themes ) {
            wp_send_json_error( array( 'message' => 'Vì lý do bảo mật, bạn chỉ có thể xoá tệp nằm trong thư mục uploads hoặc themes.' ) );
        }

        if ( ! file_exists( $absolute_path ) ) {
            wp_send_json_error( array( 'message' => 'Tệp không tồn tại trên hệ thống.' ) );
        }

        if ( @unlink( $absolute_path ) ) {
            wp_send_json_success( array( 'message' => 'Đã xóa file độc hại thành công!' ) );
        } else {
            wp_send_json_error( array( 'message' => 'Không thể xóa file. Hãy kiểm tra lại phân quyền tệp trên máy chủ.' ) );
        }
    }

    public function security_shield_fix_db() {
        $this->verify_request();
        global $wpdb;

        $table = isset( $_POST['table'] ) ? sanitize_text_field( $_POST['table'] ) : '';
        $key   = isset( $_POST['key'] ) ? sanitize_text_field( $_POST['key'] ) : '';

        if ( empty( $table ) || empty( $key ) ) {
            wp_send_json_error( array( 'message' => 'Thông số đầu vào không đủ.' ) );
        }

        if ( $table === $wpdb->posts ) {
            preg_match( '/post_id=(\d+)/', $key, $matches );
            if ( isset( $matches[1] ) ) {
                $post_id = intval( $matches[1] );
                $post = get_post( $post_id );
                if ( $post ) {
                    $cleaned_content = preg_replace( '/<script\b[^>]*>(.*?)<\/script>/is', '', $post->post_content );
                    $cleaned_content = preg_replace( '/<iframe\b[^>]*>(.*?)<\/iframe>/is', '', $cleaned_content );
                    
                    $updated = wp_update_post( array(
                        'ID'           => $post_id,
                        'post_content' => $cleaned_content
                    ) );

                    if ( ! is_wp_error( $updated ) ) {
                        wp_send_json_success( array( 'message' => 'Đã dọn dẹp mã JS/iframe độc hại trong bài viết thành công.' ) );
                    }
                }
            }
        }

        if ( $table === $wpdb->options ) {
            preg_match( '/option_name=(.+)/', $key, $matches );
            if ( isset( $matches[1] ) ) {
                $option_name = sanitize_text_field( $matches[1] );
                
                if ( in_array( $option_name, array( 'siteurl', 'home', 'blogname', 'admin_email' ) ) ) {
                    wp_send_json_error( array( 'message' => 'Không thể chỉnh sửa tùy chọn cấu hình hệ thống cốt lõi.' ) );
                }

                if ( delete_option( $option_name ) ) {
                    wp_send_json_success( array( 'message' => 'Đã xoá tuỳ chọn cấu hình nhiễm độc thành công.' ) );
                }
            }
        }

        wp_send_json_error( array( 'message' => 'Không thể sửa chữa tự động đối tượng này.' ) );
    }

    public function security_shield_create_backup() {
        $this->verify_request();

        $backup_db       = ! empty( $_POST['backup_db'] );
        $backup_config   = ! empty( $_POST['backup_config'] );
        $backup_snapshot = ! empty( $_POST['backup_snapshot'] );

        $backup = new WP_Security_Shield_Backup();
        $res = $backup->create_backup( array(
            'db'       => $backup_db,
            'config'   => $backup_config,
            'snapshot' => $backup_snapshot
        ) );

        if ( $res['success'] ) {
            wp_send_json_success( array( 'message' => 'Đã tạo bản sao lưu thành công!' ) );
        } else {
            wp_send_json_error( array( 'message' => 'Đã có lỗi xảy ra khi tạo bản sao lưu.' ) );
        }
    }

    public function security_shield_get_posts_to_scan() {
        $this->verify_request();

        $post_types = get_post_types( array( 'public' => true ), 'names' );
        if ( isset( $post_types['attachment'] ) ) {
            unset( $post_types['attachment'] );
        }

        $posts = get_posts( array(
            'post_type'      => array_values( $post_types ),
            'post_status'    => 'publish',
            'numberposts'    => -1,
            'orderby'        => 'ID',
            'order'          => 'ASC'
        ) );

        $results = array();
        foreach ( $posts as $post ) {
            $results[] = array(
                'id'        => $post->ID,
                'title'     => $post->post_title ? $post->post_title : '(Không có tiêu đề)',
                'post_type' => $post->post_type,
                'url'       => get_permalink( $post->ID )
            );
        }

        wp_send_json_success( array( 'posts' => $results ) );
    }

    public function security_shield_scan_post_item() {
        $this->verify_request();

        $post_id = isset( $_POST['post_id'] ) ? intval( $_POST['post_id'] ) : 0;
        if ( ! $post_id ) {
            wp_send_json_error( array( 'message' => 'ID bài viết không hợp lệ.' ) );
        }

        $scanner = new WP_Security_Shield_Scanner();
        $res = $scanner->analyze_page_content( $post_id );

        if ( isset( $res['success'] ) && ! $res['success'] ) {
            wp_send_json_error( array( 'message' => $res['message'] ) );
        }

        $res['edit_url'] = get_edit_post_link( $post_id, '' );
        wp_send_json_success( $res );
    }

    public function security_shield_get_suspicious_files() {
        $this->verify_request();
        $files = get_option( 'wp_security_shield_suspicious_files', array() );
        wp_send_json_success( array( 'files' => array_values( $files ) ) );
    }

    public function security_shield_sync_rules() {
        $this->verify_request();
        $scanner = new WP_Security_Shield_Scanner();
        $res = $scanner->fetch_remote_rules();
        if ( $res ) {
            wp_send_json_success( array(
                'message'      => 'Đồng bộ quy tắc bảo mật thành công!',
                'last_updated' => get_option( 'wp_security_shield_rules_last_updated' )
            ) );
        } else {
            wp_send_json_error( array( 'message' => 'Đồng bộ quy tắc thất bại.' ) );
        }
    }

    public function security_shield_save_rules_url() {
        $this->verify_request();
        $rules_url = isset( $_POST['rules_url'] ) ? esc_url_raw( trim( $_POST['rules_url'] ) ) : '';
        if ( empty( $rules_url ) ) {
            wp_send_json_error( array( 'message' => 'Đường dẫn URL không được để trống.' ) );
        }

        update_option( 'wp_security_shield_rules_url', $rules_url );
        wp_send_json_success( array( 'message' => 'Lưu URL nguồn quy tắc thành công!' ) );
    }

    public function security_shield_save_hardening_progress() {
        $this->verify_request();
        $completed_steps = isset( $_POST['completed_steps'] ) ? array_map( 'sanitize_text_field', (array) $_POST['completed_steps'] ) : array();

        update_option( 'wp_security_shield_progress', $completed_steps );
        wp_send_json_success( array( 'message' => 'Lưu tiến độ thành công!' ) );
    }
}
