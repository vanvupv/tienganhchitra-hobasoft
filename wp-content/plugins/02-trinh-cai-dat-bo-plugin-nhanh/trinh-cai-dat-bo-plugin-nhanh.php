<?php
/**
 * Plugin Name:  Trình Cài Đặt Bộ Plugin Nhanh (WDM Quick Stack Installer)
 * Plugin URI:   https://wdm-portal.dev
 * Description:  Cài đặt hàng loạt plugin WordPress từ danh sách yêu thích chỉ với 1 click. Tích hợp tìm kiếm trực tiếp WP.org, bảng quản lý plugin đã cài, và console tiến trình cài đặt theo thời gian thực.
 * Version:      1.0.0
 * Author:       WDM Portal Team
 * License:      GPL-2.0+
 * Text Domain:  wdm-qi
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// =============================================
// CONSTANTS
// =============================================
define( 'WDM_QI_VERSION',  '1.0.0' );
define( 'WDM_QI_DIR',      plugin_dir_path( __FILE__ ) );
define( 'WDM_QI_URL',      plugin_dir_url( __FILE__ ) );
define( 'WDM_QI_BASENAME', plugin_basename( __FILE__ ) );

// =============================================
// LOAD CLASSES
// =============================================
require_once WDM_QI_DIR . 'includes/class-wdm-qi-db.php';
require_once WDM_QI_DIR . 'includes/class-wdm-qi-installer.php';
require_once WDM_QI_DIR . 'includes/class-wdm-qi-api.php';
require_once WDM_QI_DIR . 'includes/class-security-scanner.php';
require_once WDM_QI_DIR . 'includes/class-security-backup.php';
require_once WDM_QI_DIR . 'includes/class-security-ajax-handler.php';

// Khởi tạo Ajax Handler cho Security Shield
new WP_Security_Shield_Ajax_Handler();

// =============================================
// ADMIN MENU
// =============================================
add_action( 'admin_menu', 'wdm_qi_register_menu' );

function wdm_qi_register_menu() {
    add_menu_page(
        'Quick Stack Installer & Security',
        '⚡ Installer & Shield',
        'manage_options',
        'wdm-quick-installer',
        'wdm_qi_render_page',
        'dashicons-plugins-checked',
        75
    );

    add_submenu_page(
        'wdm-quick-installer',
        'Cài Đặt Bộ Plugin Nhanh',
        'Cài Đặt Plugin Nhanh',
        'manage_options',
        'wdm-quick-installer',
        'wdm_qi_render_page'
    );

    add_submenu_page(
        'wdm-quick-installer',
        'Lá Chắn Bảo Mật (WP Security Shield)',
        'Lá Chắn Bảo Mật',
        'manage_options',
        'wp-security-shield',
        'wp_security_shield_render_page'
    );
}

// =============================================
// RENDER PAGES
// =============================================
function wdm_qi_render_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'Bạn không có quyền truy cập trang này.' );
    }
    include WDM_QI_DIR . 'templates/main-page.php';
}

function wp_security_shield_render_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'Bạn không có quyền truy cập trang này.' );
    }
    include WDM_QI_DIR . 'templates/security-admin-page.php';
}

// =============================================
// ENQUEUE ASSETS (chỉ load trên trang plugin)
// =============================================
add_action( 'admin_enqueue_scripts', 'wdm_qi_enqueue_assets' );

function wdm_qi_enqueue_assets( $hook ) {
    if ( strpos( $hook, 'wp-security-shield' ) !== false ) {
        wp_enqueue_style( 'wp-security-shield-admin-css', WDM_QI_URL . 'assets/css/admin.css', array(), WDM_QI_VERSION );
        wp_enqueue_style( 'wp-security-shield-scan-css', WDM_QI_URL . 'assets/css/scan.css', array(), WDM_QI_VERSION );
        wp_enqueue_style( 'wp-security-shield-backup-css', WDM_QI_URL . 'assets/css/backup.css', array(), WDM_QI_VERSION );
        wp_enqueue_style( 'wp-security-shield-core-css', WDM_QI_URL . 'assets/css/core.css', array(), WDM_QI_VERSION );
        wp_enqueue_style( 'wp-security-shield-plugins-css', WDM_QI_URL . 'assets/css/plugins.css', array(), WDM_QI_VERSION );
        wp_enqueue_style( 'wp-security-shield-pages-css', WDM_QI_URL . 'assets/css/pages.css', array(), WDM_QI_VERSION );
        wp_enqueue_style( 'wp-security-shield-workflow-css', WDM_QI_URL . 'assets/css/workflow.css', array(), WDM_QI_VERSION );

        wp_enqueue_script( 'wp-security-shield-admin-js', WDM_QI_URL . 'assets/js/admin.js', array( 'jquery' ), WDM_QI_VERSION, true );
        wp_localize_script( 'wp-security-shield-admin-js', 'wpSecurityShield', array(
            'ajax_url' => admin_url( 'admin-ajax.php' ),
            'nonce'    => wp_create_nonce( 'wp_security_shield_nonce' )
        ) );
        return;
    }

    // Chỉ load trên trang của plugin installer
    if ( 'toplevel_page_wdm-quick-installer' !== $hook ) {
        return;
    }

    // CSS
    wp_enqueue_style(
        'wdm-qi-style',
        WDM_QI_URL . 'assets/css/admin-style.css',
        array(),
        WDM_QI_VERSION
    );

    // Lucide Icons (CDN)
    wp_enqueue_script(
        'lucide-icons',
        'https://unpkg.com/lucide@latest/dist/umd/lucide.min.js',
        array(),
        null,
        true
    );

    // JS chính
    wp_enqueue_script(
        'wdm-qi-queue',
        WDM_QI_URL . 'assets/js/installer-queue.js',
        array( 'lucide-icons' ),
        WDM_QI_VERSION,
        true
    );

    // Sử dụng định dạng rest_route để đảm bảo hoạt động ổn định trên mọi cấu hình Permalinks (ngay cả khi rewrite rules của Nginx/Apache chưa flush sau khi chuyển hosting)
    $api_url = add_query_arg( 'rest_route', '/wdm-qi/v1', home_url( '/' ) );

    // Truyền dữ liệu từ PHP sang JS
    wp_localize_script( 'wdm-qi-queue', 'wdmQiSettings', array(
        'apiUrl' => esc_url_raw( $api_url ),
        'nonce'  => wp_create_nonce( 'wp_rest' ),
        'siteUrl' => get_site_url(),
    ) );
}

// =============================================
// INIT REST API
// =============================================
add_action( 'rest_api_init', array( 'WDM_QI_API', 'register_routes' ) );

// =============================================
// HOOK ON PLUGIN DELETION (BEFORE AND AFTER FILES REMOVED)
// =============================================
add_action( 'delete_plugin', 'wdm_qi_on_delete_plugin' );
add_action( 'deleted_plugin', 'wdm_qi_on_deleted_plugin', 10, 2 );

function wdm_qi_on_delete_plugin( $plugin_file ) {
    $parts = explode( '/', $plugin_file );
    $slug = count( $parts ) > 1 ? $parts[0] : basename( $plugin_file, '.php' );

    if ( $slug === 'wdm-quick-installer' || $slug === 'trinh-cai-dat-bo-plugin-nhanh' || $slug === 'trinh-quan-ly-plugin-tuy-bien' ) {
        return;
    }

    // Đọc metadata của plugin trước khi tệp tin bị xóa hẳn khỏi đĩa
    require_once ABSPATH . 'wp-admin/includes/plugin.php';
    $plugin_data = get_plugin_data( WP_PLUGIN_DIR . '/' . $plugin_file );
    $version = isset( $plugin_data['Version'] ) ? $plugin_data['Version'] : '';
    $name    = isset( $plugin_data['Name'] ) ? $plugin_data['Name'] : $slug;

    // Lưu tạm vào transient trong 5 phút
    set_transient( 'wdm_qi_deleted_ver_' . $slug, array( 'version' => $version, 'name' => $name ), 300 );
}

function wdm_qi_on_deleted_plugin( $plugin_file, $deleted ) {
    if ( $deleted ) {
        $parts = explode( '/', $plugin_file );
        $slug = count( $parts ) > 1 ? $parts[0] : basename( $plugin_file, '.php' );

        if ( $slug === 'wdm-quick-installer' || $slug === 'trinh-quan-ly-plugin-tuy-bien' ) {
            return;
        }

        // Lấy lại dữ liệu phiên bản từ transient
        $deleted_data = get_transient( 'wdm_qi_deleted_ver_' . $slug );
        delete_transient( 'wdm_qi_deleted_ver_' . $slug );

        $version = isset( $deleted_data['version'] ) ? $deleted_data['version'] : '';
        $name    = isset( $deleted_data['name'] ) ? $deleted_data['name'] : '';

        // Truy vấn WP.org API lấy icon đại diện
        require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
        $api = plugins_api( 'plugin_information', array(
            'slug'   => $slug,
            'fields' => array( 'sections' => false, 'reviews' => false ),
        ) );

        if ( ! is_wp_error( $api ) ) {
            if ( empty( $name ) ) {
                $name = $api->name;
            }
            $icons = isset( $api->icons ) ? (array) $api->icons : array();
            $icon_url = $icons['1x'] ?? $icons['default'] ?? '';
            WDM_QI_DB::add_to_history( $slug, $name, $icon_url, $version );
        } elseif ( ! empty( $name ) ) {
            $icon_url = 'https://ps.w.org/' . $slug . '/assets/icon-128x128.png';
            WDM_QI_DB::add_to_history( $slug, $name, $icon_url, $version );
        }
    }
}
