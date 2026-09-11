<?php
/**
 * Theme functions and definitions.
 *
 * For additional information on potential customization options,
 * read the developers' documentation:
 *
 * https://developers.elementor.com/docs/hello-elementor-theme/
 *
 * @package HelloElementorChild
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly.
}

// Tự động cập nhật version theo thời gian sửa file, vĩnh viễn không lo dính cache
define('HELLO_ELEMENTOR_CHILD_VERSION', file_exists(get_stylesheet_directory() . '/style.css') ? filemtime(get_stylesheet_directory() . '/style.css') : '2.0.1');

/**
 * Load child theme scripts & styles.
 *
 * @return void
 */
function hello_elementor_child_scripts_styles()
{
    wp_enqueue_style(
        'hello-elementor-child-style',
        get_stylesheet_directory_uri() . '/style.css',
        [
            'hello-elementor-theme-style',
        ],
        HELLO_ELEMENTOR_CHILD_VERSION
    );
}
add_action('wp_enqueue_scripts', 'hello_elementor_child_scripts_styles', 20);

/**
 * ============================================================================
 * ĐĂNG KÝ CUSTOM POST TYPES DỰ ÁN TIẾNG ANH CHỊ TRÀ
 * 1. giang_vien  : Đội ngũ giảng viên
 * 2. khoa_hoc    : Chương trình đào tạo / Khóa học
 * 3. hoc_vien    : Bảng vàng học viên xuất sắc
 * ============================================================================
 */
add_action('init', 'tienganh_chitra_register_custom_post_types');
function tienganh_chitra_register_custom_post_types()
{
    // 1. Post Type: Đội Ngũ Giảng Viên
    register_post_type('giang_vien', array(
        'labels' => array(
            'name'               => __('Giảng Viên', 'tienganh-chitra'),
            'singular_name'      => __('Giảng Viên', 'tienganh-chitra'),
            'menu_name'          => __('Đội Ngũ Giảng Viên', 'tienganh-chitra'),
            'all_items'          => __('Tất Cả Giảng Viên', 'tienganh-chitra'),
            'add_new'            => __('Thêm Giảng Viên Mới', 'tienganh-chitra'),
            'add_new_item'       => __('Thêm Giảng Viên Mới', 'tienganh-chitra'),
            'edit_item'          => __('Chỉnh Sửa Giảng Viên', 'tienganh-chitra'),
            'new_item'           => __('Giảng Viên Mới', 'tienganh-chitra'),
            'view_item'          => __('Xem Giảng Viên', 'tienganh-chitra'),
            'search_items'       => __('Tìm Kiếm Giảng Viên', 'tienganh-chitra'),
            'not_found'          => __('Không tìm thấy giảng viên nào', 'tienganh-chitra'),
        ),
        'public'             => true,
        'has_archive'        => true,
        'show_in_rest'       => true, // Kích hoạt Gutenberg & Elementor Loop Grid
        'menu_icon'          => 'dashicons-businesswoman',
        'supports'           => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
        'rewrite'            => array('slug' => 'giang-vien', 'with_front' => false),
    ));

    // 2. Post Type: Chương Trình Đào Tạo / Khóa Học
    register_post_type('khoa_hoc', array(
        'labels' => array(
            'name'               => __('Khóa Học', 'tienganh-chitra'),
            'singular_name'      => __('Khóa Học', 'tienganh-chitra'),
            'menu_name'          => __('Chương Trình Đào Tạo', 'tienganh-chitra'),
            'all_items'          => __('Tất Cả Khóa Học', 'tienganh-chitra'),
            'add_new'            => __('Thêm Khóa Học Mới', 'tienganh-chitra'),
            'add_new_item'       => __('Thêm Khóa Học Mới', 'tienganh-chitra'),
            'edit_item'          => __('Chỉnh Sửa Khóa Học', 'tienganh-chitra'),
            'new_item'           => __('Khóa Học Mới', 'tienganh-chitra'),
            'view_item'          => __('Xem Khóa Học', 'tienganh-chitra'),
            'search_items'       => __('Tìm Kiếm Khóa Học', 'tienganh-chitra'),
            'not_found'          => __('Không tìm thấy khóa học nào', 'tienganh-chitra'),
        ),
        'public'             => true,
        'has_archive'        => true,
        'show_in_rest'       => true,
        'menu_icon'          => 'dashicons-welcome-learn-more',
        'supports'           => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
        'rewrite'            => array('slug' => 'khoa-hoc', 'with_front' => false),
    ));

    // 3. Post Type: Bảng Vàng Học Viên Xuất Sắc
    register_post_type('hoc_vien', array(
        'labels' => array(
            'name'               => __('Học Viên Xuất Sắc', 'tienganh-chitra'),
            'singular_name'      => __('Học Viên Xuất Sắc', 'tienganh-chitra'),
            'menu_name'          => __('Bảng Vàng Học Viên', 'tienganh-chitra'),
            'all_items'          => __('Tất Cả Học Viên', 'tienganh-chitra'),
            'add_new'            => __('Thêm Học Viên Mới', 'tienganh-chitra'),
            'add_new_item'       => __('Thêm Học Viên Mới', 'tienganh-chitra'),
            'edit_item'          => __('Chỉnh Sửa Học Viên', 'tienganh-chitra'),
            'new_item'           => __('Học Viên Mới', 'tienganh-chitra'),
            'view_item'          => __('Xem Chi Tiết Học Viên', 'tienganh-chitra'),
            'search_items'       => __('Tìm Kiếm Học Viên', 'tienganh-chitra'),
            'not_found'          => __('Không tìm thấy học viên nào', 'tienganh-chitra'),
        ),
        'public'             => true,
        'has_archive'        => true,
        'show_in_rest'       => true,
        'menu_icon'          => 'dashicons-awards',
        'supports'           => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
        'rewrite'            => array('slug' => 'hoc-vien-xuat-sac', 'with_front' => false),
    ));
}

