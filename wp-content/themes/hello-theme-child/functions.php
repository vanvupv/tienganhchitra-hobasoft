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
 * 1. giang_vien       : Đội ngũ giảng viên
 * 2. khoa_hoc         : Chương trình đào tạo / Khóa học
 * 3. hoc_vien         : Bảng vàng học viên xuất sắc
 * 4. du_an_cong_dong  : Dự án cộng đồng (Taxonomy: danh_muc_du_an)
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

    // 4. Post Type: Dự Án Cộng Đồng
    register_post_type('du_an_cong_dong', array(
        'labels' => array(
            'name'               => __('Dự Án Cộng Đồng', 'tienganh-chitra'),
            'singular_name'      => __('Dự Án Cộng Đồng', 'tienganh-chitra'),
            'menu_name'          => __('Dự Án Cộng Đồng', 'tienganh-chitra'),
            'all_items'          => __('Tất Cả Dự Án', 'tienganh-chitra'),
            'add_new'            => __('Thêm Dự Án Mới', 'tienganh-chitra'),
            'add_new_item'       => __('Thêm Dự Án Mới', 'tienganh-chitra'),
            'edit_item'          => __('Chỉnh Sửa Dự Án', 'tienganh-chitra'),
            'new_item'           => __('Dự Án Mới', 'tienganh-chitra'),
            'view_item'          => __('Xem Dự Án', 'tienganh-chitra'),
            'search_items'       => __('Tìm Kiếm Dự Án', 'tienganh-chitra'),
            'not_found'          => __('Không tìm thấy dự án nào', 'tienganh-chitra'),
        ),
        'public'             => true,
        'has_archive'        => true,
        'show_in_rest'       => true, // Kích hoạt Gutenberg, Elementor Loop Grid & Dynamic Tags
        'menu_icon'          => 'dashicons-heart',
        'supports'           => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
        'rewrite'            => array('slug' => 'du-an-cong-dong', 'with_front' => false),
    ));

    // Taxonomy: Danh Mục Dự Án Cộng Đồng
    register_taxonomy('danh_muc_du_an', 'du_an_cong_dong', array(
        'labels' => array(
            'name'              => __('Danh Mục Dự Án', 'tienganh-chitra'),
            'singular_name'     => __('Danh Mục Dự Án', 'tienganh-chitra'),
            'search_items'      => __('Tìm Danh Mục', 'tienganh-chitra'),
            'all_items'         => __('Tất Cả Danh Mục', 'tienganh-chitra'),
            'parent_item'       => __('Danh Mục Cha', 'tienganh-chitra'),
            'parent_item_colon' => __('Danh Mục Cha:', 'tienganh-chitra'),
            'edit_item'         => __('Chỉnh Sửa Danh Mục', 'tienganh-chitra'),
            'update_item'       => __('Cập Nhật Danh Mục', 'tienganh-chitra'),
            'add_new_item'      => __('Thêm Danh Mục Mới', 'tienganh-chitra'),
            'new_item_name'     => __('Tên Danh Mục Mới', 'tienganh-chitra'),
            'menu_name'         => __('Danh Mục Dự Án', 'tienganh-chitra'),
        ),
        'hierarchical'      => true,
        'show_ui'           => true,
        'show_admin_column' => true,
        'show_in_rest'      => true,
        'query_var'         => true,
        'rewrite'           => array('slug' => 'danh-muc-du-an'),
    ));
}

/**
 * ============================================================================
 * ĐĂNG KÝ TRƯỜNG "THÀNH TÍCH" (thanh_tich) CHO POST TYPE hoc_vien
 * ============================================================================
 */
// 1. Đăng ký Post Meta chuẩn REST API để Elementor Dynamic Tags tự động nhận diện
add_action('init', 'tienganh_chitra_register_hoc_vien_meta');
function tienganh_chitra_register_hoc_vien_meta()
{
    register_post_meta('hoc_vien', 'thanh_tich', array(
        'show_in_rest'      => true,
        'single'            => true,
        'type'              => 'string',
        'sanitize_callback' => 'sanitize_text_field',
        'auth_callback'     => function () {
            return current_user_can('edit_posts');
        }
    ));
}

// 2. Meta Box hiển thị trong Admin khi chỉnh sửa Học Viên
add_action('add_meta_boxes', 'tienganh_chitra_add_hoc_vien_meta_box');
function tienganh_chitra_add_hoc_vien_meta_box()
{
    add_meta_box(
        'hoc_vien_thanh_tich_box',
        __('Thông Tin Thành Tích Học Viên', 'tienganh-chitra'),
        'tienganh_chitra_render_hoc_vien_meta_box',
        'hoc_vien',
        'normal',
        'high'
    );
}

function tienganh_chitra_render_hoc_vien_meta_box($post)
{
    wp_nonce_field('tienganh_chitra_save_thanh_tich', 'hoc_vien_thanh_tich_nonce');
    $value = get_post_meta($post->ID, 'thanh_tich', true);
    ?>
    <div style="padding: 10px 0;">
        <label for="thanh_tich" style="display:block; font-weight: 600; margin-bottom: 8px; font-size: 14px;">
            <?php _e('Thành tích nổi bật (Ví dụ: IELTS 8.0 Overall, Giải Nhất HSG, Học bổng ĐH Sydney...):', 'tienganh-chitra'); ?>
        </label>
        <input type="text" id="thanh_tich" name="thanh_tich" value="<?php echo esc_attr($value); ?>" 
               placeholder="🏆 IELTS 8.0 Overall" style="width: 100%; max-width: 500px; padding: 8px 12px; font-size: 14px; border-radius: 4px; border: 1px solid #ccc;" />
        <p style="color: #666; font-size: 13px; margin-top: 6px;">
            <?php _e('Trường này sẽ được tự động hiển thị nổi bật dưới tên học viên trong thẻ Bảng Vàng (Loop Item Học Viên).', 'tienganh-chitra'); ?>
        </p>
    </div>
    <?php
}

add_action('save_post_hoc_vien', 'tienganh_chitra_save_hoc_vien_meta');
function tienganh_chitra_save_hoc_vien_meta($post_id)
{
    if (!isset($_POST['hoc_vien_thanh_tich_nonce']) || !wp_verify_nonce($_POST['hoc_vien_thanh_tich_nonce'], 'tienganh_chitra_save_thanh_tich')) {
        return;
    }
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }
    if (!current_user_can('edit_post', $post_id)) {
        return;
    }
    if (isset($_POST['thanh_tich'])) {
        update_post_meta($post_id, 'thanh_tich', sanitize_text_field($_POST['thanh_tich']));
    }
}

// 3. Tự động đăng ký ACF Field Group nếu plugin ACF / SCF đang hoạt động
add_action('acf/init', 'tienganh_chitra_register_acf_thanh_tich');
function tienganh_chitra_register_acf_thanh_tich()
{
    if (function_exists('acf_add_local_field_group')) {
        acf_add_local_field_group(array(
            'key' => 'group_hoc_vien_thanh_tich',
            'title' => 'Thông Tin Học Viên Xuất Sắc',
            'fields' => array(
                array(
                    'key' => 'field_thanh_tich',
                    'label' => 'Thành Tích Đạt Được',
                    'name' => 'thanh_tich',
                    'type' => 'text',
                    'instructions' => 'Nhập thành tích nổi bật của học viên (Ví dụ: 🏆 IELTS 8.0 Overall, Giải Nhất Tỉnh...)',
                    'required' => 0,
                    'placeholder' => '🏆 IELTS 8.0 Overall',
                ),
            ),
            'location' => array(
                array(
                    array(
                        'param' => 'post_type',
                        'operator' => '==',
                        'value' => 'hoc_vien',
                    ),
                ),
            ),
            'menu_order' => 0,
            'position' => 'normal',
            'style' => 'default',
        ));
    }
}

/**
 * ============================================================================
 * TỰ ĐỘNG CĂN GIỮA SLIDE ACTIVE (centeredSlides: true) CHO WIDGET REVIEWS
 * ============================================================================
 */
add_action('wp_footer', 'tienganh_chitra_custom_swiper_centered_script', 99);
function tienganh_chitra_custom_swiper_centered_script()
{
    ?>
    <script>
    (function($) {
        $(window).on('elementor/frontend/init', function() {
            if (window.elementorFrontend && elementorFrontend.hooks) {
                elementorFrontend.hooks.addAction('frontend/element_ready/reviews.default', function($scope) {
                    var $container = $scope.find('.elementor-main-swiper');
                    if ($container.length) {
                        var enableCentered = function() {
                            var swiper = $container.data('swiper');
                            if (swiper && !swiper.params.centeredSlides) {
                                swiper.params.centeredSlides = true;
                                swiper.params.slideToClickedSlide = true;
                                $container.addClass('is-centered');
                                swiper.update();
                            }
                        };
                        setTimeout(enableCentered, 100);
                        setTimeout(enableCentered, 400);
                    }
                });
            }
        });
    })(jQuery);
    </script>
    <?php
}
