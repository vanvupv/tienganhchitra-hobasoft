<?php
/**
 * WDM Quick Installer — REST API Controller
 * Đăng ký tất cả các REST endpoints phục vụ Frontend JS Queue
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WDM_QI_API {

    const NAMESPACE = 'wdm-qi/v1';

    /**
     * Đăng ký tất cả REST routes
     */
    public static function register_routes() {
        // --- Installed Plugins ---
        register_rest_route( self::NAMESPACE, '/installed', array(
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => array( __CLASS__, 'get_installed' ),
            'permission_callback' => array( __CLASS__, 'admin_permission' ),
        ) );

        // --- Install Plugin ---
        register_rest_route( self::NAMESPACE, '/install', array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => array( __CLASS__, 'install_plugin' ),
            'permission_callback' => array( __CLASS__, 'admin_permission' ),
            'args'                => array(
                'slug' => array(
                    'required'          => true,
                    'sanitize_callback' => 'sanitize_text_field',
                ),
                'version' => array(
                    'required'          => false,
                    'sanitize_callback' => 'sanitize_text_field',
                    'default'           => '',
                ),
            ),
        ) );

        // --- Toggle Plugin (activate/deactivate) ---
        register_rest_route( self::NAMESPACE, '/toggle', array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => array( __CLASS__, 'toggle_plugin' ),
            'permission_callback' => array( __CLASS__, 'admin_permission' ),
            'args'                => array(
                'plugin_file' => array(
                    'required'          => true,
                    'sanitize_callback' => 'sanitize_text_field',
                ),
                'action' => array(
                    'required'          => true,
                    'sanitize_callback' => 'sanitize_text_field',
                ),
            ),
        ) );

        // --- Search WP.org ---
        register_rest_route( self::NAMESPACE, '/search', array(
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => array( __CLASS__, 'search_wporg' ),
            'permission_callback' => array( __CLASS__, 'admin_permission' ),
            'args'                => array(
                'q' => array(
                    'required'          => true,
                    'sanitize_callback' => 'sanitize_text_field',
                ),
            ),
        ) );

        // --- Get Favorites ---
        register_rest_route( self::NAMESPACE, '/favorites', array(
            array(
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => array( __CLASS__, 'get_favorites' ),
                'permission_callback' => array( __CLASS__, 'admin_permission' ),
            ),
            array(
                'methods'             => WP_REST_Server::CREATABLE,
                'callback'            => array( __CLASS__, 'save_favorites' ),
                'permission_callback' => array( __CLASS__, 'admin_permission' ),
            ),
        ) );

        // --- History ---
        register_rest_route( self::NAMESPACE, '/history', array(
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => array( __CLASS__, 'get_history' ),
            'permission_callback' => array( __CLASS__, 'admin_permission' ),
        ) );

        register_rest_route( self::NAMESPACE, '/history/clear', array(
            'methods'             => WP_REST_Server::CREATABLE,
            'callback'            => array( __CLASS__, 'clear_history' ),
            'permission_callback' => array( __CLASS__, 'admin_permission' ),
        ) );

        // --- Details ---
        register_rest_route( self::NAMESPACE, '/details', array(
            'methods'             => WP_REST_Server::READABLE,
            'callback'            => array( __CLASS__, 'get_details' ),
            'permission_callback' => array( __CLASS__, 'admin_permission' ),
            'args'                => array(
                'slug' => array(
                    'required'          => true,
                    'sanitize_callback' => 'sanitize_text_field',
                ),
            ),
        ) );
    }

    /**
     * Permission: Chỉ cho phép Admin
     */
    public static function admin_permission() {
        return current_user_can( 'manage_options' );
    }

    /**
     * GET /installed — Lấy danh sách plugin đã cài
     */
    public static function get_installed( WP_REST_Request $request ) {
        $plugins = WDM_QI_Installer::get_installed_plugins();
        return rest_ensure_response( array(
            'success' => true,
            'plugins' => $plugins,
            'total'   => count( $plugins ),
        ) );
    }

    /**
     * POST /install — Cài đặt và kích hoạt plugin
     */
    public static function install_plugin( WP_REST_Request $request ) {
        $slug    = $request->get_param( 'slug' );
        $version = $request->get_param( 'version' );
        $result  = WDM_QI_Installer::install_plugin( $slug, $version );

        $status_code = $result['success'] ? 200 : 500;
        return new WP_REST_Response( $result, $status_code );
    }

    /**
     * POST /toggle — Bật/tắt plugin
     */
    public static function toggle_plugin( WP_REST_Request $request ) {
        $plugin_file = $request->get_param( 'plugin_file' );
        $action      = $request->get_param( 'action' );

        if ( ! in_array( $action, array( 'activate', 'deactivate' ), true ) ) {
            return new WP_REST_Response( array(
                'success' => false,
                'message' => 'Action không hợp lệ. Chỉ chấp nhận: activate | deactivate.',
            ), 400 );
        }

        $result = WDM_QI_Installer::toggle_plugin( $plugin_file, $action );
        return rest_ensure_response( $result );
    }

    /**
     * GET /search?q={keyword} — Tìm kiếm plugin trên WP.org
     */
    public static function search_wporg( WP_REST_Request $request ) {
        $query = $request->get_param( 'q' );

        if ( strlen( $query ) < 2 ) {
            return rest_ensure_response( array( 'success' => false, 'plugins' => array(), 'message' => 'Từ khóa quá ngắn.' ) );
        }

        require_once ABSPATH . 'wp-admin/includes/plugin-install.php';

        $api = plugins_api( 'query_plugins', array(
            'search'   => $query,
            'per_page' => 10,
            'fields'   => array(
                'short_description' => true,
                'icons'             => true,
                'rating'            => true,
                'num_ratings'       => true,
                'downloaded'        => true,
                'sections'          => false,
                'reviews'           => false,
            ),
        ) );

        if ( is_wp_error( $api ) ) {
            return new WP_REST_Response( array(
                'success' => false,
                'message' => 'Không thể kết nối tới WordPress.org.',
                'plugins' => array(),
            ), 502 );
        }

        $plugins = array();
        if ( ! empty( $api->plugins ) ) {
            foreach ( $api->plugins as $plugin ) {
                $p = (array) $plugin;
                $icons = isset( $p['icons'] ) ? (array) $p['icons'] : array();
                $icon_url = $icons['1x'] ?? $icons['default'] ?? '';

                $plugins[] = array(
                    'slug'              => $p['slug'] ?? '',
                    'name'              => $p['name'] ?? '',
                    'author'            => wp_strip_all_tags( $p['author'] ?? '' ),
                    'rating'            => round( ( $p['rating'] ?? 0 ) / 20, 1 ), // Convert 0-100 to 0-5
                    'num_ratings'       => $p['num_ratings'] ?? 0,
                    'downloaded'        => $p['downloaded'] ?? 0,
                    'short_description' => $p['short_description'] ?? '',
                    'icon'              => $icon_url,
                );
            }
        }

        return rest_ensure_response( array(
            'success' => true,
            'plugins' => $plugins,
            'total'   => count( $plugins ),
        ) );
    }

    /**
     * GET /favorites — Lấy danh sách plugin hay dùng
     */
    public static function get_favorites( WP_REST_Request $request ) {
        $favorites = WDM_QI_DB::get_favorites();
        return rest_ensure_response( array(
            'success'   => true,
            'favorites' => $favorites,
        ) );
    }

    /**
     * POST /favorites — Lưu danh sách plugin hay dùng
     */
    public static function save_favorites( WP_REST_Request $request ) {
        $body = $request->get_json_params();
        $favorites = isset( $body['favorites'] ) ? $body['favorites'] : array();

        $saved = WDM_QI_DB::save_favorites( $favorites );

        if ( ! $saved ) {
            return new WP_REST_Response( array(
                'success' => false,
                'message' => 'Lưu dữ liệu thất bại.',
            ), 500 );
        }

        return rest_ensure_response( array(
            'success' => true,
            'message' => 'Đã lưu danh sách plugin hay dùng.',
        ) );
    }

    /**
     * GET /history — Lấy danh sách lịch sử cài đặt
     */
    public static function get_history( WP_REST_Request $request ) {
        $history = WDM_QI_DB::get_history();
        return rest_ensure_response( array(
            'success' => true,
            'history' => $history,
        ) );
    }

    /**
     * POST /history/clear — Xóa sạch lịch sử cài đặt
     */
    public static function clear_history( WP_REST_Request $request ) {
        $cleared = WDM_QI_DB::clear_history();
        return rest_ensure_response( array(
            'success' => $cleared,
            'message' => $cleared ? 'Đã xóa lịch sử cài đặt.' : 'Xóa lịch sử cài đặt thất bại hoặc lịch sử trống.',
        ) );
    }

    /**
     * GET /details — Lấy thông tin chi tiết plugin từ WordPress.org
     */
    public static function get_details( WP_REST_Request $request ) {
        $slug = $request->get_param( 'slug' );
        require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
        $api = plugins_api( 'plugin_information', array(
            'slug'   => $slug,
            'fields' => array(
                'sections'        => true,
                'screenshots'     => true,
                'banners'         => true,
                'ratings'         => true,
                'active_installs' => true,
            ),
        ) );

        if ( is_wp_error( $api ) ) {
            return new WP_REST_Response( array(
                'success' => false,
                'message' => $api->get_error_message(),
            ), 500 );
        }

        $sections    = isset( $api->sections ) ? (array) $api->sections : array();
        $screenshots = isset( $api->screenshots ) ? (array) $api->screenshots : array();
        $banners     = isset( $api->banners ) ? (array) $api->banners : array();
        $icons       = isset( $api->icons ) ? (array) $api->icons : array();

        return rest_ensure_response( array(
            'success'         => true,
            'name'            => $api->name,
            'slug'            => $api->slug,
            'version'         => $api->version,
            'author'          => $api->author,
            'rating'          => $api->rating,
            'num_ratings'     => $api->num_ratings,
            'active_installs' => $api->active_installs,
            'last_updated'    => $api->last_updated,
            'requires'        => $api->requires,
            'tested'          => $api->tested,
            'sections'        => $sections,
            'screenshots'     => $screenshots,
            'banners'         => $banners,
            'icon'            => $icons['1x'] ?? $icons['default'] ?? 'https://ps.w.org/' . $slug . '/assets/icon-128x128.png',
        ) );
    }
}
