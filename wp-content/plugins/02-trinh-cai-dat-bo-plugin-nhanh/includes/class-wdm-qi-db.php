<?php
/**
 * WDM Quick Installer — Database & Options Manager
 * Quản lý danh sách Plugin Hay Dùng (Favorites) lưu trong wp_options
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WDM_QI_DB {

    const OPTION_FAVORITES = 'wdm_qi_favorites';
    const OPTION_HISTORY   = 'wdm_qi_history';

    /**
     * Danh sách plugin hay dùng mặc định (seeded)
     */
    public static function get_default_favorites() {
        return array(
            array( 'slug' => 'classic-editor',         'name' => 'Classic Editor',           'category' => 'editor' ),
            array( 'slug' => 'classic-widgets',         'name' => 'Classic Widgets',          'category' => 'editor' ),
            array( 'slug' => 'contact-form-7',          'name' => 'Contact Form 7',           'category' => 'forms' ),
            array( 'slug' => 'advanced-custom-fields',  'name' => 'Advanced Custom Fields',   'category' => 'dev' ),
            array( 'slug' => 'elementor',               'name' => 'Elementor',                'category' => 'builder' ),
            array( 'slug' => 'rank-math',               'name' => 'Rank Math SEO',            'category' => 'seo' ),
            array( 'slug' => 'wordfence',               'name' => 'Wordfence Security',       'category' => 'security' ),
            array( 'slug' => 'litespeed-cache',         'name' => 'LiteSpeed Cache',          'category' => 'performance' ),
            array( 'slug' => 'woocommerce',             'name' => 'WooCommerce',              'category' => 'ecommerce' ),
            array( 'slug' => 'wp-mail-smtp',            'name' => 'WP Mail SMTP',             'category' => 'utility' ),
            array( 'slug' => 'updraftplus',             'name' => 'UpdraftPlus Backup',       'category' => 'backup' ),
            array( 'slug' => 'duplicate-post',          'name' => 'Yoast Duplicate Post',     'category' => 'utility' ),
            array( 'slug' => 'wp-super-cache',          'name' => 'WP Super Cache',           'category' => 'performance' ),
            array( 'slug' => 'really-simple-ssl',       'name' => 'Really Simple SSL',        'category' => 'security' ),
            array( 'slug' => 'redirection',             'name' => 'Redirection',              'category' => 'seo' ),
        );
    }

    /**
     * Lấy danh sách plugin hay dùng
     *
     * @return array
     */
    public static function get_favorites() {
        $favorites = get_option( self::OPTION_FAVORITES, null );

        if ( is_null( $favorites ) ) {
            $favorites = self::get_default_favorites();
            update_option( self::OPTION_FAVORITES, $favorites );
        }

        return is_array( $favorites ) ? $favorites : array();
    }

    /**
     * Lưu danh sách plugin hay dùng
     *
     * @param array $favorites
     * @return bool
     */
    public static function save_favorites( $favorites ) {
        if ( ! is_array( $favorites ) ) {
            return false;
        }

        $sanitized = array();
        foreach ( $favorites as $item ) {
            if ( empty( $item['slug'] ) ) continue;
            $sanitized[] = array(
                'slug'     => sanitize_text_field( $item['slug'] ),
                'name'     => sanitize_text_field( $item['name'] ?? '' ),
                'category' => sanitize_text_field( $item['category'] ?? 'utility' ),
            );
        }

        return update_option( self::OPTION_FAVORITES, $sanitized );
    }

    /**
     * Trích xuất slug từ tên tệp plugin
     */
    private static function extract_slug( $file ) {
        $parts = explode( '/', $file );
        if ( count( $parts ) > 1 ) {
            return $parts[0];
        }
        return basename( $file, '.php' );
    }

    /**
     * Lấy danh sách lịch sử cài đặt (tự động seed từ các plugin đang cài nếu trống)
     */
    public static function get_history() {
        $history = get_option( self::OPTION_HISTORY, null );

        if ( is_null( $history ) ) {
            $history = array();
            $all_plugins = get_plugins();
            foreach ( $all_plugins as $file => $data ) {
                $slug = self::extract_slug( $file );
                if ( $slug === 'wdm-quick-installer' || $slug === 'trinh-quan-ly-plugin-tuy-bien' ) {
                    continue;
                }
                $history[] = array(
                    'slug'        => $slug,
                    'name'        => $data['Name'],
                    'icon'        => 'https://ps.w.org/' . $slug . '/assets/icon-128x128.png',
                    'version'     => $data['Version'],
                    'installed_at'=> current_time( 'mysql' ),
                );
            }
            update_option( self::OPTION_HISTORY, $history );
        }

        return is_array( $history ) ? $history : array();
    }

    /**
     * Thêm một plugin vào lịch sử cài đặt
     */
    public static function add_to_history( $slug, $name, $icon = '', $version = '' ) {
        if ( empty( $slug ) ) {
            return false;
        }

        $history = self::get_history();

        // Chỉ xóa trùng lặp nếu trùng cả slug và số phiên bản (để cho phép lưu nhiều phiên bản)
        $history = array_filter( $history, function( $item ) use ( $slug, $version ) {
            $item_ver = isset( $item['version'] ) ? $item['version'] : '';
            return !( $item['slug'] === $slug && $item_ver === $version );
        } );

        $history[] = array(
            'slug'        => sanitize_text_field( $slug ),
            'name'        => sanitize_text_field( $name ),
            'icon'        => esc_url_raw( $icon ),
            'version'     => sanitize_text_field( $version ),
            'installed_at'=> current_time( 'mysql' ),
        );

        // Giới hạn lịch sử lưu tối đa 50 plugin gần nhất
        if ( count( $history ) > 50 ) {
            $history = array_slice( $history, -50 );
        }

        return update_option( self::OPTION_HISTORY, array_values( $history ) );
    }

    /**
     * Xóa sạch lịch sử cài đặt
     */
    public static function clear_history() {
        return delete_option( self::OPTION_HISTORY );
    }
}
