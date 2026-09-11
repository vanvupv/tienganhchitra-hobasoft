<?php
/**
 * Script Nạp Trực Tiếp Template Elementor vào WordPress Database
 * Thư mục: wp-json-elementor/
 */

define('WP_USE_THEMES', false);

// Tìm wp-load.php ở thư mục gốc WordPress
if (file_exists(__DIR__ . '/../wp-load.php')) {
    require_once __DIR__ . '/../wp-load.php';
} elseif (file_exists(__DIR__ . '/wp-load.php')) {
    require_once __DIR__ . '/wp-load.php';
} else {
    die("Error: Cannot locate wp-load.php file.\n");
}

if (!class_exists('\Elementor\Plugin')) {
    die("Error: Elementor plugin is not installed or activated.\n");
}

$json_file = __DIR__ . '/goongbe-homepage-elementor-template.json';
if (!file_exists($json_file)) {
    die("Error: JSON Template file not found at: {$json_file}\n");
}

$json_content = json_decode(file_get_contents($json_file), true);
if (!$json_content || !isset($json_content['content'])) {
    die("Error: Invalid Elementor JSON structure.\n");
}

// 1. Tạo Post mới trong bảng wp_posts với post_type = 'elementor_library'
$post_data = [
    'post_title'    => 'Trang Chủ GOONGBE VN (Imported)',
    'post_status'   => 'publish',
    'post_type'     => 'elementor_library',
    'post_author'   => 1,
];

$post_id = wp_insert_post($post_data);

if (is_wp_error($post_id)) {
    die("Error inserting post: " . $post_id->get_error_message() . "\n");
}

// 2. Thiết lập Meta Data chuẩn cho Elementor Builder
update_post_meta($post_id, '_elementor_edit_mode', 'builder');
update_post_meta($post_id, '_elementor_template_type', 'page');
update_post_meta($post_id, '_elementor_version', '3.35.1');
update_post_meta($post_id, '_elementor_data', wp_slash(json_encode($json_content['content'])));

// 3. Phân loại Taxonomy elementor_library_type = 'page'
wp_set_object_terms($post_id, 'page', 'elementor_library_type');

echo "<div style='font-family: Arial; padding: 20px; background: #e8f6f9; border: 1px solid #4cb9cc; color: #1b5b65; border-radius: 8px;'>";
echo "<h2>🎉 IMPORT THÀNH CÔNG ELEMENTOR TEMPLATE!</h2>";
echo "<p><strong>ID Mẫu (Post ID):</strong> {$post_id}</p>";
echo "<p><strong>Tên Mẫu:</strong> {$json_content['title']}</p>";
echo "<p>👉 Bạn có thể vào <strong>WordPress Admin -> Saved Templates</strong> để xem và chèn mẫu này vào bất kỳ trang nào!</p>";
echo "</div>";
