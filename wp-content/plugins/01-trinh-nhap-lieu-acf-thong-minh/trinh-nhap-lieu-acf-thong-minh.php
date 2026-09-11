<?php
/**
 * Plugin Name: Trình Nhập Liệu ACF Thông Minh
 * Plugin URI: https://github.com/google-deepmind/antigravity
 * Description: Nhập dữ liệu tự động từ Excel, Google Sheets, JSON, Notepad vào bài viết và trường ACF. Tích hợp tính năng tự động sinh dữ liệu ảo (Mock Data) thông minh qua Thuật toán hoặc Gemini AI.
 * Version: 1.0.0
 * Author: Antigravity AI
 * Author URI: https://deepmind.google/
 * License: GPL2
 * Text Domain: wp-acf-smart-importer
 */

// Ngăn chặn truy cập trực tiếp
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Định nghĩa các hằng số của plugin
define( 'WPSAI_VERSION', time() );
define( 'WPSAI_PATH', plugin_dir_path( __FILE__ ) );
define( 'WPSAI_URL', plugin_dir_url( __FILE__ ) );
define( 'WPSAI_BASENAME', plugin_basename( __FILE__ ) );

// Nạp các tệp tin cấu phần (Core files)
require_once WPSAI_PATH . 'includes/class-wp-acf-smart-importer-admin.php';
require_once WPSAI_PATH . 'includes/class-wp-acf-smart-importer-ajax.php';
require_once WPSAI_PATH . 'includes/class-wp-acf-smart-importer-engine.php';
require_once WPSAI_PATH . 'includes/class-wp-acf-smart-importer-generator.php';
require_once WPSAI_PATH . 'includes/class-wp-acf-smart-importer-scraper.php';
require_once WPSAI_PATH . 'includes/class-wp-acf-smart-importer-rest.php';
require_once WPSAI_PATH . 'includes/class-wp-acf-smart-importer-tree.php';

/**
 * Khởi tạo plugin
 */
function wpsai_init_plugin() {
    // Khởi tạo giao diện Admin
    if ( is_admin() ) {
        new WP_ACF_Smart_Importer_Admin();
        new WP_ACF_Smart_Importer_Ajax();
    }
}
add_action( 'plugins_loaded', 'wpsai_init_plugin' );

/**
 * Xử lý tương thích ngược cho endpoint cũ của Chrome Extension (/api/ext/*)
 */
function wpsai_handle_legacy_extension_routes() {
    $request_uri = $_SERVER['REQUEST_URI'];
    if ( strpos( $request_uri, '/api/ext/' ) !== false ) {
        status_header( 200 );
        header( 'Content-Type: application/json; charset=utf-8' );
        header( 'Access-Control-Allow-Origin: *' );
        header( 'Access-Control-Allow-Methods: GET, POST, OPTIONS' );
        header( 'Access-Control-Allow-Headers: Authorization, Content-Type, X-WPSAI-API-KEY' );
        
        if ( $_SERVER['REQUEST_METHOD'] === 'OPTIONS' ) {
            exit;
        }

        $api_key = get_option( 'wpsai_extension_api_key', '' );
        if ( empty( $api_key ) ) {
            $api_key = wp_generate_password( 24, false );
            update_option( 'wpsai_extension_api_key', $api_key );
        }

        echo wp_json_encode( array(
            'success'   => true,
            'site_name' => get_bloginfo( 'name' ),
            'api_key'   => $api_key,
            'token'     => $api_key,
            'message'   => 'Bridge activated successfully via compatibility route.',
        ) );
        exit;
    }
}
add_action( 'init', 'wpsai_handle_legacy_extension_routes' );

