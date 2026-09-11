<?php
/**
 * Security Shield Admin Page — Lá Chắn Bảo Mật tích hợp vào WDM Quick Stack Installer
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Lấy thông số tổng quan ban đầu
$last_scan = get_option( 'wp_security_shield_last_scan', 'Chưa bao giờ' );
$scan_results = get_option( 'wp_security_shield_scan_results', array() );
$backups = get_option( 'wp_security_shield_backups_list', array() );

$malware_count = isset( $scan_results['total_malware'] ) ? $scan_results['total_malware'] : 0;
$missing_files_count = isset( $scan_results['total_missing'] ) ? $scan_results['total_missing'] : 0;
?>

<div class="wrap wp-security-shield-wrap">
    <div class="wp-security-shield-header">
        <div class="header-title-box">
            <span class="dashicons dashicons-shield-alt shield-brand-icon"></span>
            <h1>Lá Chắn Bảo Mật (WP Security Shield)</h1>
        </div>
        <p class="header-desc">Hệ thống bảo vệ website WordPress toàn diện: quét mã độc, phát hiện JS độc hại, sao lưu và khôi phục dữ liệu nhanh chóng.</p>
    </div>

    <nav class="nav-tab-wrapper wp-security-shield-nav-tabs">
        <a href="#overview" class="nav-tab nav-tab-active" data-tab="overview">
            <span class="dashicons dashicons-dashboard"></span> Tổng quan
        </a>
        <a href="#scan" class="nav-tab" data-tab="scan">
            <span class="dashicons dashicons-search"></span> Quét mã độc
        </a>
        <a href="#core" class="nav-tab" data-tab="core">
            <span class="dashicons dashicons-admin-generic"></span> Quản lý Core
        </a>
        <a href="#plugins" class="nav-tab" data-tab="plugins">
            <span class="dashicons dashicons-admin-plugins"></span> Quản lý Plugins
        </a>
        <a href="#pages-scan" class="nav-tab" data-tab="pages-scan">
            <span class="dashicons dashicons-admin-page"></span> Quét từng trang
        </a>
        <a href="#backup" class="nav-tab" data-tab="backup">
            <span class="dashicons dashicons-backup"></span> Bảo lưu & Khôi phục
        </a>
        <a href="#workflow" class="nav-tab" data-tab="workflow">
            <span class="dashicons dashicons-randomize"></span> Luồng xử lý
        </a>
        <a href="#suspicious-files" class="nav-tab" data-tab="suspicious-files">
            <span class="dashicons dashicons-warning"></span> File nghi ngờ
        </a>
        <a href="#docs" class="nav-tab" data-tab="docs">
            <span class="dashicons dashicons-editor-help"></span> Tài liệu bảo mật
        </a>
    </nav>

    <div class="wp-security-shield-tab-content active" id="tab-overview">
        <div class="overview-grid">
            <div class="overview-card status-card">
                <h3>Trạng thái hệ thống</h3>
                <div class="status-indicator <?php echo ($malware_count > 0) ? 'status-danger' : 'status-success'; ?>">
                    <span class="dashicons <?php echo ($malware_count > 0) ? 'dashicons-warning' : 'dashicons-yes-alt'; ?>"></span>
                    <div class="status-text">
                        <strong><?php echo ($malware_count > 0) ? 'Phát hiện nguy hại!' : 'Hệ thống an toàn'; ?></strong>
                        <p><?php echo ($malware_count > 0) ? "Đã tìm thấy $malware_count file/dữ liệu nghi vấn trong lần quét cuối." : 'Không tìm thấy tệp tin độc hại nào đáng nghi.'; ?></p>
                    </div>
                </div>
                <div class="quick-stats">
                    <p><strong>Lần quét cuối:</strong> <span><?php echo esc_html( $last_scan ); ?></span></p>
                    <p><strong>Số bản sao lưu hiện có:</strong> <span><?php echo count( $backups ); ?> bản</span></p>
                </div>
            </div>

            <div class="overview-card info-card">
                <h3>Thông tin máy chủ & Website</h3>
                <table class="info-table">
                    <tr>
                        <td>Địa chỉ IP Máy chủ:</td>
                        <td><strong><?php echo esc_html( $_SERVER['SERVER_ADDR'] ?? '127.0.0.1' ); ?></strong></td>
                    </tr>
                    <tr>
                        <td>Phiên bản PHP:</td>
                        <td><strong><?php echo esc_html( PHP_VERSION ); ?></strong></td>
                    </tr>
                    <tr>
                        <td>Phiên bản WordPress:</td>
                        <td><strong><?php echo esc_html( get_bloginfo( 'version' ) ); ?></strong></td>
                    </tr>
                    <tr>
                        <td>Giới hạn bộ nhớ PHP:</td>
                        <td><strong><?php echo esc_html( @ini_get( 'memory_limit' ) ); ?></strong></td>
                    </tr>
                    <tr>
                        <td>Thời gian thực thi tối đa:</td>
                        <td><strong><?php echo esc_html( @ini_get( 'max_execution_time' ) ); ?> giây</strong></td>
                    </tr>
                </table>
            </div>

            <div class="overview-card rules-card">
                <h3>Quy tắc Bảo mật Động (Dynamic Security Rules)</h3>
                <div style="margin-bottom: 12px;">
                    <p style="margin: 4px 0; font-size: 13px;"><strong>URL Quy tắc (JSON):</strong></p>
                    <div style="display: flex; gap: 8px;">
                        <input type="text" id="ss-rules-url-input" value="<?php echo esc_url( get_option( 'wp_security_shield_rules_url', site_url( '/rules.json' ) ) ); ?>" style="flex: 1; height: 28px; border: 1px solid var(--ss-border-color); border-radius: var(--ss-border-radius); padding: 0 8px; font-size: 12px;">
                        <button class="button" id="btn-save-rules-url">Lưu URL</button>
                    </div>
                </div>
                <div class="quick-stats" style="margin-bottom: 12px;">
                    <p><strong>Cập nhật cuối:</strong> <span id="ss-rules-last-updated" style="font-weight: 600;"><?php echo esc_html( get_option( 'wp_security_shield_rules_last_updated', 'Chưa bao giờ' ) ); ?></span></p>
                </div>
                <button class="button button-primary" id="btn-sync-rules-now" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 5px;">
                    <span class="dashicons dashicons-update spin" id="rules-sync-spinner" style="display: none; font-size: 16px; width: 16px; height: 16px; line-height: 16px; margin: 0;"></span>
                    Đồng bộ Quy tắc ngay
                </button>
            </div>
        </div>
    </div>

    <div class="wp-security-shield-tab-content" id="tab-scan">
        <div class="scan-control-panel">
            <div class="scan-left">
                <h2>Bộ máy Quét mã độc nâng cao</h2>
                <p>Hệ thống sẽ tiến hành duyệt thư mục `uploads`, thư mục `themes` hiện tại, cơ sở dữ liệu và cào nội dung trang hiển thị để tìm mã độc, mã backdoor PHP hoặc các mã JS chèn trái phép.</p>
                <button class="button button-primary button-hero" id="btn-start-scan">
                    <span class="dashicons dashicons-controls-play"></span> Bắt đầu quét toàn bộ
                </button>
            </div>
            
            <div class="scan-right">
                <div class="scan-log-box-container">
                    <h3>Nhật ký quét thời gian thực</h3>
                    <div class="scan-log-box" id="scan-log">
                        <span class="log-placeholder">Nhấn nút "Bắt đầu quét" để bắt đầu tiến hành bảo mật hệ thống.</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
