<?php
/**
 * Lớp WP_ACF_Smart_Importer_Tree
 * Quản lý Kho Dữ Liệu Mẫu dạng Cây Phân Cấp (Tree Hierarchy) & Phân Mảnh Dữ Liệu (Chunking)
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_ACF_Smart_Importer_Tree {

    /**
     * Thư mục lưu trữ gốc của Tree Repository
     */
    public static function get_tree_dir() {
        $upload_dir = wp_upload_dir();
        $dir = trailingslashit( $upload_dir['basedir'] ) . 'wpsai-tree-repository';
        if ( ! file_exists( $dir ) ) {
            wp_mkdir_p( $dir );
            file_put_contents( $dir . '/.htaccess', "Options -Indexes\nDeny from all\n" );
            file_put_contents( $dir . '/index.php', '<?php // Silence is golden.' );
        }
        return $dir;
    }

    /**
     * Đọc tệp chỉ mục cây manifest.json
     */
    public static function get_manifest() {
        $file = self::get_tree_dir() . '/manifest.json';
        if ( ! file_exists( $file ) ) {
            return self::build_default_manifest();
        }

        $content = file_get_contents( $file );
        $data = json_decode( $content, true );
        return ( json_last_error() === JSON_ERROR_NONE && is_array( $data ) ) ? $data : self::build_default_manifest();
    }

    /**
     * Khởi tạo cấu trúc chỉ mục cây mặc định từ Post Types và Taxonomies hiện có
     */
    public static function build_default_manifest() {
        $post_types = get_post_types( array( 'public' => true ), 'objects' );
        $nodes = array();

        foreach ( $post_types as $slug => $obj ) {
            if ( in_array( $slug, array( 'attachment', 'revision', 'nav_menu_item', 'custom_css', 'customize_changeset', 'oembed_cache', 'user_request', 'wp_block', 'wp_template', 'wp_template_part', 'wp_navigation' ) ) ) {
                continue;
            }

            // Đếm số lượng bài viết hiện tại
            $count_obj = wp_count_posts( $slug );
            $total_posts = isset( $count_obj->publish ) ? intval( $count_obj->publish ) : 0;

            // Đọc các taxonomy thuộc post type này
            $taxonomies = get_object_taxonomies( $slug, 'objects' );
            $sub_nodes = array();

            if ( is_array( $taxonomies ) ) {
                foreach ( $taxonomies as $tax_slug => $tax_obj ) {
                    if ( ! $tax_obj->public ) {
                        continue;
                    }
                    $terms = get_terms( array(
                        'taxonomy'   => $tax_slug,
                        'hide_empty' => false,
                    ) );

                    $term_children = array();
                    if ( ! is_wp_error( $terms ) && is_array( $terms ) ) {
                        foreach ( $terms as $t ) {
                            $term_children[] = array(
                                'id'         => 'node-' . $slug . '-' . $tax_slug . '-' . $t->term_id,
                                'label'      => $t->name,
                                'type'       => 'term',
                                'slug'       => $t->slug,
                                'term_id'    => $t->term_id,
                                'taxonomy'   => $tax_slug,
                                'post_type'  => $slug,
                                'post_count' => $t->count,
                                'chunks'     => array(),
                            );
                        }
                    }

                    $sub_nodes[] = array(
                        'id'         => 'node-' . $slug . '-' . $tax_slug,
                        'label'      => $tax_obj->label . ' (' . $tax_slug . ')',
                        'type'       => 'taxonomy',
                        'taxonomy'   => $tax_slug,
                        'post_type'  => $slug,
                        'children'   => $term_children,
                    );
                }
            }

            $nodes[] = array(
                'id'         => 'node-pt-' . $slug,
                'label'      => $obj->label . ' (' . $slug . ')',
                'type'       => 'post_type',
                'post_type'  => $slug,
                'post_count' => $total_posts,
                'children'   => $sub_nodes,
                'chunks'     => array(),
            );
        }

        // Bổ sung nút Luồng Xử Lý & Prompt Mẫu
        $nodes[] = array(
            'id'       => 'node-workflows',
            'label'    => 'Luồng Xử Lý & Prompt AI Mẫu',
            'type'     => 'workflows',
            'children' => array(
                array(
                    'id'        => 'node-wf-prompt-bds',
                    'label'     => 'Prompt Sinh Bài Viết Bất Động Sản',
                    'type'      => 'workflow_item',
                    'file_path' => 'workflows/prompt-bds.json',
                ),
                array(
                    'id'        => 'node-wf-prompt-ecommerce',
                    'label'     => 'Prompt Mô Tả Sản Phẩm Chuẩn SEO',
                    'type'      => 'workflow_item',
                    'file_path' => 'workflows/prompt-ecommerce.json',
                ),
            ),
        );

        $manifest = array(
            'version'    => '1.0.0',
            'updated_at' => current_time( 'Y-m-d H:i:s' ),
            'nodes'      => $nodes,
        );

        self::save_manifest( $manifest );
        return $manifest;
    }

    /**
     * Ghi tệp manifest.json
     */
    public static function save_manifest( $manifest ) {
        $manifest['updated_at'] = current_time( 'Y-m-d H:i:s' );
        $file = self::get_tree_dir() . '/manifest.json';
        file_put_contents( $file, wp_json_encode( $manifest, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );
    }

    /**
     * Lưu chunk dữ liệu cho một nút cụ thể
     */
    public static function save_chunk_for_node( $node_id, $post_type, $posts_data, $schema = array() ) {
        $base_dir = self::get_tree_dir() . '/' . sanitize_file_name( $post_type );
        if ( ! file_exists( $base_dir ) ) {
            wp_mkdir_p( $base_dir );
        }

        // Tách dữ liệu thành từng chunk tối đa 50 bài viết / file
        $chunk_size = 50;
        $batches = array_chunk( $posts_data, $chunk_size );
        $chunk_files = array();

        foreach ( $batches as $index => $batch ) {
            $filename = 'chunk-' . sanitize_file_name( $node_id ) . '-' . ( $index + 1 ) . '.json';
            $filepath = $base_dir . '/' . $filename;
            $rel_path = sanitize_file_name( $post_type ) . '/' . $filename;

            $chunk_content = array(
                'meta' => array(
                    'node_id'    => $node_id,
                    'post_type'  => $post_type,
                    'count'      => count( $batch ),
                    'chunk_num'  => $index + 1,
                    'created_at' => current_time( 'Y-m-d H:i:s' ),
                ),
                'schema' => $schema,
                'posts'  => $batch,
            );

            file_put_contents( $filepath, wp_json_encode( $chunk_content, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );
            $chunk_files[] = array(
                'file_rel' => $rel_path,
                'count'    => count( $batch ),
                'size'     => size_format( filesize( $filepath ) ),
            );
        }

        // Cập nhật thông tin chunk vào manifest
        $manifest = self::get_manifest();
        self::update_manifest_node_chunks( $manifest['nodes'], $node_id, $chunk_files, count( $posts_data ) );
        self::save_manifest( $manifest );

        return $chunk_files;
    }

    /**
     * Đệ quy cập nhật thông tin chunks của Nút trên Cây Manifest
     */
    private static function update_manifest_node_chunks( &$nodes, $node_id, $chunk_files, $total_posts ) {
        foreach ( $nodes as &$node ) {
            if ( isset( $node['id'] ) && $node['id'] === $node_id ) {
                $node['chunks'] = $chunk_files;
                $node['post_count'] = $total_posts;
                return true;
            }
            if ( ! empty( $node['children'] ) && is_array( $node['children'] ) ) {
                if ( self::update_manifest_node_chunks( $node['children'], $node_id, $chunk_files, $total_posts ) ) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Đọc nội dung chunk của nút dữ liệu
     */
    public static function read_node_data( $file_rel ) {
        $filepath = self::get_tree_dir() . '/' . ltrim( $file_rel, '/' );
        if ( ! file_exists( $filepath ) ) {
            return new WP_Error( 'file_not_found', __( 'File chunk không tồn tại.', 'wp-acf-smart-importer' ) );
        }

        $content = file_get_contents( $filepath );
        $data = json_decode( $content, true );
        if ( json_last_error() !== JSON_ERROR_NONE ) {
            return new WP_Error( 'json_invalid', __( 'File chunk bị hỏng.', 'wp-acf-smart-importer' ) );
        }

        return $data;
    }
}
