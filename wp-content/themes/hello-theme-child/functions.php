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
