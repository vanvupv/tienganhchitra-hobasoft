<?php
/**
 * WDM Quick Installer — Core Installer Engine
 * Xử lý cài đặt, kích hoạt, tắt plugin sử dụng WordPress Core APIs
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WDM_QI_Installer {

    /**
     * Load các thư viện WordPress Admin cần thiết cho việc cài đặt
     */
    private static function load_wp_admin_libs() {
        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/misc.php';
        require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
        require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
        require_once ABSPATH . 'wp-admin/includes/plugin.php';
        WP_Filesystem();
    }

    /**
     * Cài đặt và kích hoạt plugin theo slug
     *
     * @param  string $slug  Slug plugin trên WP.org (vd: classic-editor)
     * @return array  { success, status, message }
     */
    public static function install_plugin( $slug, $version = '' ) {
        $slug = sanitize_text_field( $slug );
        $version = sanitize_text_field( $version );
        if ( empty( $slug ) ) {
            return array(
                'success' => false,
                'status'  => 'error',
                'message' => 'Slug plugin không hợp lệ.',
            );
        }

        self::load_wp_admin_libs();

        // Kiểm tra nếu plugin đã được cài, chỉ cần activate nếu đúng phiên bản
        $plugin_file = self::find_plugin_file( $slug );
        if ( $plugin_file ) {
            $all_plugins = get_plugins();
            $installed_version = isset( $all_plugins[$plugin_file]['Version'] ) ? $all_plugins[$plugin_file]['Version'] : '';
            
            // Nếu có yêu cầu phiên bản cụ thể mà bản đã cài trong máy lại khác phiên bản đó,
            // ta bỏ qua nhánh này để tiến hành tải bản đè từ WP.org
            $is_correct_version = empty( $version ) || ( $installed_version === $version );

            if ( $is_correct_version ) {
                if ( is_plugin_active( $plugin_file ) ) {
                    return array(
                        'success' => true,
                        'status'  => 'already_active',
                        'message' => 'Plugin đã được cài đặt và kích hoạt trước đó.',
                        'plugin'  => $plugin_file,
                    );
                }
                // Đã cài nhưng chưa active
                $activated = activate_plugin( $plugin_file );
                if ( is_wp_error( $activated ) ) {
                    return array(
                        'success' => false,
                        'status'  => 'activation_error',
                        'message' => $activated->get_error_message(),
                    );
                }

                // Ghi nhận vào lịch sử cài đặt
                $name = isset( $all_plugins[$plugin_file]['Name'] ) ? $all_plugins[$plugin_file]['Name'] : $slug;
                $icon = 'https://ps.w.org/' . $slug . '/assets/icon-128x128.png';
                WDM_QI_DB::add_to_history( $slug, $name, $icon, $installed_version );

                return array(
                    'success' => true,
                    'status'  => 'activated',
                    'message' => 'Plugin đã được kích hoạt thành công.',
                    'plugin'  => $plugin_file,
                );
            }
        }

        // Tra cứu thông tin từ WP.org
        $api = plugins_api( 'plugin_information', array(
            'slug'   => $slug,
            'fields' => array( 'sections' => false, 'reviews' => false ),
        ) );

        if ( is_wp_error( $api ) ) {
            return array(
                'success' => false,
                'status'  => 'api_error',
                'message' => 'Không tìm thấy thông tin plugin "' . $slug . '" trên WordPress.org.',
            );
        }

        // Xác định link download (nếu có version thì tự tạo link bản cũ)
        if ( ! empty( $version ) ) {
            $download_link = 'https://downloads.wordpress.org/plugin/' . $slug . '.' . $version . '.zip';
        } else {
            $download_link = $api->download_link;
        }

        // Khởi tạo Upgrader với Skin im lặng
        $skin     = new Automatic_Upgrader_Skin();
        $upgrader = new Plugin_Upgrader( $skin );
        $result   = $upgrader->install( $download_link );

        if ( is_wp_error( $result ) ) {
            return array(
                'success' => false,
                'status'  => 'install_error',
                'message' => $result->get_error_message(),
            );
        }

        if ( ! $result ) {
            return array(
                'success' => false,
                'status'  => 'install_failed',
                'message' => 'Cài đặt thất bại. Kiểm tra quyền ghi thư mục wp-content/plugins.',
            );
        }

        // Tìm file kích hoạt chính của plugin vừa cài
        $plugin_file = self::find_plugin_file( $slug );
        if ( ! $plugin_file ) {
            return array(
                'success' => false,
                'status'  => 'file_not_found',
                'message' => 'Plugin đã cài nhưng không tìm được file chính để kích hoạt.',
            );
        }

        // Kích hoạt plugin
        $activated = activate_plugin( $plugin_file );
        if ( is_wp_error( $activated ) ) {
            return array(
                'success' => false,
                'status'  => 'activation_error',
                'message' => $activated->get_error_message(),
            );
        }

        // Ghi nhận vào lịch sử cài đặt
        $all_plugins = get_plugins();
        $installed_version = isset( $all_plugins[$plugin_file]['Version'] ) ? $all_plugins[$plugin_file]['Version'] : ( ! empty( $version ) ? $version : $api->version );
        $icons = isset( $api->icons ) ? (array) $api->icons : array();
        $icon_url = $icons['1x'] ?? $icons['default'] ?? '';
        WDM_QI_DB::add_to_history( $slug, $api->name, $icon_url, $installed_version );

        return array(
            'success' => true,
            'status'  => 'installed_activated',
            'message' => 'Cài đặt và kích hoạt thành công!',
            'plugin'  => $plugin_file,
        );
    }

    /**
     * Bật hoặc tắt một plugin đã cài
     *
     * @param  string $plugin_file  Đường dẫn file chính (vd: classic-editor/classic-editor.php)
     * @param  string $action       'activate' | 'deactivate'
     * @return array
     */
    public static function toggle_plugin( $plugin_file, $action ) {
        self::load_wp_admin_libs();

        $plugin_file = sanitize_text_field( $plugin_file );

        if ( 'activate' === $action ) {
            $result = activate_plugin( $plugin_file );
            if ( is_wp_error( $result ) ) {
                return array( 'success' => false, 'message' => $result->get_error_message() );
            }
            return array( 'success' => true, 'status' => 'activated', 'message' => 'Plugin đã kích hoạt.' );
        }

        if ( 'deactivate' === $action ) {
            deactivate_plugins( $plugin_file );
            return array( 'success' => true, 'status' => 'deactivated', 'message' => 'Plugin đã tắt.' );
        }

        return array( 'success' => false, 'message' => 'Hành động không hợp lệ.' );
    }

    /**
     * Lấy danh sách tất cả plugin đã cài + trạng thái
     *
     * @return array
     */
    public static function get_installed_plugins() {
        self::load_wp_admin_libs();

        $all_plugins = get_plugins();
        $result      = array();

        foreach ( $all_plugins as $file => $data ) {
            $slug = self::extract_slug_from_file( $file );
            $result[] = array(
                'file'    => $file,
                'slug'    => $slug,
                'name'    => $data['Name'],
                'version' => $data['Version'],
                'author'  => wp_strip_all_tags( $data['Author'] ),
                'active'  => is_plugin_active( $file ),
            );
        }

        // Sắp xếp: active trước, sau đó theo tên ABC
        usort( $result, function( $a, $b ) {
            if ( $a['active'] !== $b['active'] ) {
                return $b['active'] - $a['active'];
            }
            return strcmp( $a['name'], $b['name'] );
        } );

        return $result;
    }

    /**
     * Tìm đường dẫn file chính của plugin theo slug
     *
     * @param  string $slug
     * @return string|false
     */
    public static function find_plugin_file( $slug ) {
        $all_plugins = get_plugins();
        foreach ( $all_plugins as $file => $data ) {
            // Trường hợp thư mục trùng slug: classic-editor/classic-editor.php
            if ( strpos( $file, $slug . '/' ) === 0 ) {
                return $file;
            }
            // Trường hợp plugin single-file: hello.php
            if ( basename( $file, '.php' ) === $slug ) {
                return $file;
            }
        }
        return false;
    }

    /**
     * Trích xuất slug từ đường dẫn file plugin
     *
     * @param  string $file  (vd: classic-editor/classic-editor.php)
     * @return string
     */
    private static function extract_slug_from_file( $file ) {
        $parts = explode( '/', $file );
        if ( count( $parts ) > 1 ) {
            return $parts[0]; // Thư mục plugin là slug
        }
        return basename( $file, '.php' ); // Single-file plugin
    }
}
