<?php
/**
 * WP Security Shield - Bộ Quét Mã Độc
 * Quét file đệ quy trong thư mục uploads, themes và quét cơ sở dữ liệu.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_Security_Shield_Scanner {

    private $signatures = array(
        'eval_base64'       => '/eval\s*\(\s*base64_decode/i',
        'eval_gzinflate'    => '/eval\s*\(\s*gzinflate/i',
        'eval_str_rot13'    => '/eval\s*\(\s*str_rot13/i',
        'shell_exec'        => '/shell_exec\s*\(/i',
        'system_call'       => '/\bsystem\s*\(/i',
        'passthru_call'     => '/passthru\s*\(/i',
        'exec_call'         => '/\bexec\s*\(/i',
        'popen_call'        => '/popen\s*\(/i',
        'proc_open'         => '/proc_open\s*\(/i',
        'assert_call'       => '/assert\s*\(\s*(\\\$_POST|\\\$_GET|\\\$_REQUEST)/i',
        'double_post'       => '/\$_POST\s*\[\s*[\'"]\w+[\'"]\s*\]\s*\(\s*\$_POST/i',
        'php_backdoor'      => '/(c99shell|r57shell|wsofip|vuln_scanner|cmd\.php|c100\.php)/i',
        'hex_obfuscation'   => '/\\\\x[0-9a-fA-F]{2}\\\\x[0-9a-fA-F]{2}/i',
    );

    private $js_signatures = array(
        'js_eval'           => '/eval\s*\(\s*(String\.fromCharCode|unescape|atob)/i',
        'js_redirect'       => '/window\.location\.(replace|href)\s*=\s*[\'"]http/i',
        'js_document_write' => '/document\.write\s*\(\s*unescape/i',
        'js_hidden_iframe'  => '/iframe\s+[^>]*style\s*=\s*[\'"]\s*display\s*:\s*none/i',
        'js_suspicious_src' => '/<script[^>]+src\s*=\s*[\'"]https?:\/\/[^\'"]+\.(ru|xyz|tk|click|info|gq|cf|ml|ga|top|pw)\//i',
    );

    public function __construct() {}

    private function get_all_php_signatures() {
        $sigs = $this->signatures;
        $dynamic = get_option( 'wp_security_shield_dynamic_rules', array() );
        if ( isset( $dynamic['php_signatures'] ) && is_array( $dynamic['php_signatures'] ) ) {
            foreach ( $dynamic['php_signatures'] as $name => $pattern ) {
                $sigs[$name] = $pattern;
            }
        }
        return $sigs;
    }

    private function get_all_js_signatures() {
        $sigs = $this->js_signatures;
        $dynamic = get_option( 'wp_security_shield_dynamic_rules', array() );
        if ( isset( $dynamic['js_signatures'] ) && is_array( $dynamic['js_signatures'] ) ) {
            foreach ( $dynamic['js_signatures'] as $name => $pattern ) {
                $sigs[$name] = $pattern;
            }
        }
        return $sigs;
    }

    public function fetch_remote_rules() {
        $url = get_option( 'wp_security_shield_rules_url', site_url( '/rules.json' ) );
        if ( empty( $url ) ) return false;

        $response = wp_remote_get( $url, array( 'timeout' => 10, 'sslverify' => false ) );
        if ( is_wp_error( $response ) || wp_remote_retrieve_response_code( $response ) !== 200 ) {
            return false;
        }

        $body = wp_remote_retrieve_body( $response );
        $json = json_decode( $body, true );
        if ( ! $json || ! is_array( $json ) ) return false;

        update_option( 'wp_security_shield_dynamic_rules', $json );
        update_option( 'wp_security_shield_rules_last_updated', date( 'Y-m-d H:i:s' ) );
        return true;
    }

    public function scan_uploads() {
        $upload_dir = wp_upload_dir();
        $target_path = $upload_dir['basedir'];
        
        $issues = array();
        $logs = array();
        
        if ( ! is_dir( $target_path ) ) {
            $logs[] = array( 'msg' => 'Thư mục Uploads không tồn tại hoặc không đọc được.', 'type' => 'warning' );
            return array( 'issues' => $issues, 'logs' => $logs );
        }

        $logs[] = array( 'msg' => 'Bắt đầu duyệt thư mục: ' . $target_path, 'type' => 'info' );
        
        $files = $this->get_files_recursive( $target_path );
        $logs[] = array( 'msg' => 'Tìm thấy ' . count( $files ) . ' tệp trong thư mục uploads.', 'type' => 'info' );
        
        $php_count = 0;
        $malware_count = 0;

        foreach ( $files as $file ) {
            $ext = strtolower( pathinfo( $file, PATHINFO_EXTENSION ) );
            $filename = basename( $file );
            
            if ( in_array( $ext, array( 'php', 'phtml', 'php3', 'php4', 'php5', 'phps', 'suspected' ) ) ) {
                $issues[] = array(
                    'file'   => $this->get_relative_path( $file ),
                    'type'   => 'PHP File In Uploads',
                    'reason' => 'Thư mục uploads chỉ chứa ảnh/tài liệu. Tệp thực thi PHP tại đây rất nguy hiểm và thường là backdoor.'
                );
                $php_count++;
                continue;
            }

            if ( preg_match( '/\.(php|phtml|php3|php4|php5|phps)\./i', $filename ) ) {
                $issues[] = array(
                    'file'   => $this->get_relative_path( $file ),
                    'type'   => 'Double Extension',
                    'reason' => 'Tệp tin chứa hai đuôi mở rộng, có nguy cơ qua mặt bộ lọc của WordPress để thực thi mã độc.'
                );
                $php_count++;
                continue;
            }

            if ( in_array( $ext, array( 'txt', 'html', 'htm', 'js', 'png', 'jpg', 'jpeg', 'gif' ) ) ) {
                $file_size = @filesize( $file );
                if ( $file_size > 0 && $file_size < 1024 * 1024 ) {
                    $content = @file_get_contents( $file );
                    if ( $content ) {
                        if ( $ext !== 'txt' && ( strpos( $content, '<?php' ) !== false || strpos( $content, '<?=' ) !== false ) ) {
                            $issues[] = array(
                                'file'   => $this->get_relative_path( $file ),
                                'type'   => 'PHP Code In Non-PHP File',
                                'reason' => 'Phát hiện mã PHP nhúng ẩn bên trong tệp tin định dạng ' . strtoupper( $ext ) . '.'
                            );
                            $malware_count++;
                            continue;
                        }

                        foreach ( $this->get_all_php_signatures() as $sig_name => $pattern ) {
                            if ( preg_match( $pattern, $content ) ) {
                                $issues[] = array(
                                    'file'   => $this->get_relative_path( $file ),
                                    'type'   => 'Suspicious Content Signature',
                                    'reason' => 'Nội dung khớp với mẫu mã độc nghi vấn: <strong>' . $sig_name . '</strong>.'
                                );
                                $malware_count++;
                                break;
                            }
                        }
                    }
                }
            }
        }

        $logs[] = array( 'msg' => "Quét uploads hoàn tất. Phát hiện $php_count file PHP bất hợp pháp và $malware_count nội dung nghi ngờ.", 'type' => ($php_count + $malware_count > 0 ? 'warning' : 'success') );
        
        return array( 'issues' => $issues, 'logs' => $logs );
    }

    public function scan_themes() {
        $themes_dir = get_theme_root();
        
        $issues = array();
        $logs = array();

        if ( ! is_dir( $themes_dir ) ) {
            $logs[] = array( 'msg' => 'Thư mục Themes không tồn tại.', 'type' => 'warning' );
            return array( 'issues' => $issues, 'logs' => $logs );
        }

        $logs[] = array( 'msg' => 'Bắt đầu duyệt thư mục themes: ' . $themes_dir, 'type' => 'info' );
        $files = $this->get_files_recursive( $themes_dir );
        $logs[] = array( 'msg' => 'Tìm thấy ' . count( $files ) . ' tệp nguồn trong các thư mục themes.', 'type' => 'info' );

        $malware_count = 0;

        foreach ( $files as $file ) {
            $ext = strtolower( pathinfo( $file, PATHINFO_EXTENSION ) );
            if ( in_array( $ext, array( 'php', 'js', 'html' ) ) ) {
                $file_size = @filesize( $file );
                if ( $file_size > 0 && $file_size < 1.5 * 1024 * 1024 ) {
                    $content = @file_get_contents( $file );
                    if ( $content ) {
                        foreach ( $this->get_all_php_signatures() as $sig_name => $pattern ) {
                            if ( preg_match( $pattern, $content ) ) {
                                $issues[] = array(
                                    'file'   => $this->get_relative_path( $file ),
                                    'type'   => 'Malware Signature In Theme',
                                    'reason' => 'Tệp code của theme chứa mẫu mã độc/lệnh thực thi nguy hiểm: <strong>' . $sig_name . '</strong>.'
                                );
                                $malware_count++;
                                break;
                            }
                        }
                    }
                }
            }
        }

        $logs[] = array( 'msg' => "Quét theme hoàn tất. Tìm thấy $malware_count file chứa mã đáng ngờ.", 'type' => ($malware_count > 0 ? 'warning' : 'success') );
        
        return array( 'issues' => $issues, 'logs' => $logs );
    }

    public function scan_database() {
        global $wpdb;
        $issues = array();
        $logs = array();

        $logs[] = array( 'msg' => 'Bắt đầu quét Cơ sở dữ liệu CSDL...', 'type' => 'info' );

        $posts = $wpdb->get_results( "SELECT ID, post_title, post_content FROM {$wpdb->posts} WHERE post_status = 'publish'" );
        $post_issue_count = 0;

        $spam_keywords = array(
            'casino', 'betting', 'gambling', 'poker', 'viagra', 'roulette', 'slot machine', 
            'cá cược', 'sòng bạc', 'nhà cái', 'quay hũ', 'bắn cá', 'soi cầu', 'tỷ lệ kèo', 
            'lô đề', 'đánh bài'
        );

        if ( ! empty( $posts ) ) {
            foreach ( $posts as $post ) {
                $content = $post->post_content;
                if ( empty( $content ) ) continue;

                $suspicious = false;
                $matched_reason = '';

                foreach ( $this->get_all_js_signatures() as $sig_name => $pattern ) {
                    if ( preg_match( $pattern, $content ) ) {
                        $suspicious = true;
                        $matched_reason = "Nội dung bài viết chứa mã JS trùng khớp chữ ký độc hại: " . $sig_name;
                        break;
                    }
                }

                if ( ! $suspicious && preg_match_all( '/<script[^>]+src\s*=\s*[\'"]([^\'"]+)[\'"]/i', $content, $matches ) ) {
                    foreach ( $matches[1] as $src_url ) {
                        $parsed_url = parse_url( $src_url );
                        if ( isset( $parsed_url['host'] ) && strpos( home_url(), $parsed_url['host'] ) === false ) {
                            $allowed_cdns = array( 'google.com', 'googleapis.com', 'gstatic.com', 'cloudflare.com', 'jquery.com', 'bootstrapcdn.com', 'facebook.net' );
                            $is_allowed = false;
                            foreach ( $allowed_cdns as $cdn ) {
                                if ( strpos( $parsed_url['host'], $cdn ) !== false ) {
                                    $is_allowed = true;
                                    break;
                                }
                            }
                            if ( ! $is_allowed ) {
                                $suspicious = true;
                                $matched_reason = "Nạp script từ nguồn bên ngoài lạ: " . esc_html($src_url);
                                break;
                            }
                        }
                    }
                }

                if ( $suspicious ) {
                    $issues[] = array(
                        'table'      => $wpdb->posts,
                        'key'        => 'post_id=' . $post->ID,
                        'issue_type' => 'Suspicious Post Content',
                        'detail'     => 'Bài viết "' . esc_html($post->post_title) . '" (ID: ' . $post->ID . ') chứa nội dung bất thường: ' . $matched_reason
                    );
                    $post_issue_count++;
                }
            }
        }
        $logs[] = array( 'msg' => "Quét bài viết xong. Phát hiện $post_issue_count bài viết chứa nội dung/script đáng nghi.", 'type' => ($post_issue_count > 0 ? 'warning' : 'success') );

        return array( 'issues' => $issues, 'logs' => $logs );
    }

    private function get_files_recursive( $dir ) {
        $file_list = array();
        if ( ! is_dir( $dir ) ) return $file_list;

        $items = @scandir( $dir );
        if ( ! $items ) return $file_list;

        foreach ( $items as $item ) {
            if ( $item === '.' || $item === '..' ) continue;
            $path = $dir . DIRECTORY_SEPARATOR . $item;
            if ( is_dir( $path ) ) {
                $file_list = array_merge( $file_list, $this->get_files_recursive( $path ) );
            } else {
                $file_list[] = $path;
            }
        }
        return $file_list;
    }

    private function get_relative_path( $absolute_path ) {
        $abs = wp_normalize_path( ABSPATH );
        $path = wp_normalize_path( $absolute_path );
        return str_replace( $abs, '', $path );
    }
}
