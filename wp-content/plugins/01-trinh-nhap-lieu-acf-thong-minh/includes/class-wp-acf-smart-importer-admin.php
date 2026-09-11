<?php
/**
 * Lớp WP_ACF_Smart_Importer_Admin
 * Quản lý menu trang quản trị và nạp tài nguyên giao diện.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class WP_ACF_Smart_Importer_Admin {

    /**
     * Khởi tạo các hook
     */
    public function __construct() {
        add_action( 'admin_menu', array( $this, 'register_admin_menu' ) );
        add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_admin_assets' ) );
    }

    /**
     * Đăng ký Menu Trang Quản trị
     */
    public function register_admin_menu() {
        add_menu_page(
            __( 'WP Smart Importer', 'wp-acf-smart-importer' ),
            __( 'Smart Importer', 'wp-acf-smart-importer' ),
            'manage_options',
            'wp-acf-smart-importer',
            array( $this, 'render_admin_page' ),
            'dashicons-database-import',
            80
        );

        add_submenu_page(
            'wp-acf-smart-importer',
            __( 'Nhập Liệu ACF & AI', 'wp-acf-smart-importer' ),
            __( 'Nhập Liệu ACF & AI', 'wp-acf-smart-importer' ),
            'manage_options',
            'wp-acf-smart-importer',
            array( $this, 'render_admin_page' )
        );

        add_submenu_page(
            'wp-acf-smart-importer',
            __( 'Cào Bài Viết & Web Scraper', 'wp-acf-smart-importer' ),
            __( 'Cào Bài Viết & Scraper', 'wp-acf-smart-importer' ),
            'manage_options',
            'wpsai-smart-scraper',
            array( $this, 'render_scraper_page' )
        );

        add_submenu_page(
            'wp-acf-smart-importer',
            __( 'Package JSON Import', 'wp-acf-smart-importer' ),
            __( 'Package JSON Import', 'wp-acf-smart-importer' ),
            'manage_options',
            'wpsai-package-import',
            array( $this, 'render_package_page' )
        );

        add_submenu_page(
            'wp-acf-smart-importer',
            __( 'Kết Nối & Cấu Hình API', 'wp-acf-smart-importer' ),
            __( 'Kết Nối API', 'wp-acf-smart-importer' ),
            'manage_options',
            'wpsai-api-settings',
            array( $this, 'render_api_settings_page' )
        );
    }

    public function render_scraper_page() {
        $this->render_admin_page( 'scraper' );
    }

    public function render_package_page() {
        $this->render_admin_page( 'offline-scraper' );
    }

    public function render_api_settings_page() {
        $this->render_admin_page( 'settings' );
    }

    /**
     * Nạp CSS, JS của plugin và thư viện bên thứ 3 (SheetJS)
     */
    public function enqueue_admin_assets( $hook ) {
        if ( strpos( $hook, 'wp-acf-smart-importer' ) === false && strpos( $hook, 'wpsai' ) === false ) {
            return;
        }

        // Kích hoạt thư viện Media Uploader của WordPress
        wp_enqueue_media();

        // Tải thư viện SheetJS từ CDN hỗ trợ đọc Excel tại client
        wp_enqueue_script(
            'sheetjs-xlsx',
            'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js',
            array(),
            '0.18.5',
            true
        );

        // Tải file CSS của plugin
        wp_enqueue_style(
            'wpsai-admin-style',
            WPSAI_URL . 'assets/css/admin-style.css',
            array(),
            WPSAI_VERSION
        );

        // Tải file Javascript chính của plugin
        wp_enqueue_script(
            'wpsai-admin-script',
            WPSAI_URL . 'assets/js/admin-script.js',
            array( 'jquery', 'sheetjs-xlsx' ),
            WPSAI_VERSION,
            true
        );

        // Bản địa hóa biến AJAX và Nonce bảo mật
        $js_data = array(
            'ajax_url' => admin_url( 'admin-ajax.php' ),
            'nonce'    => wp_create_nonce( 'wpsai_import_nonce_action' ),
        );
        wp_localize_script( 'wpsai-admin-script', 'wpsai_params', $js_data );
        wp_localize_script( 'wpsai-admin-script', 'wpsai_data', $js_data );
    }

    /**
     * Hiển thị HTML của trang quản trị
     */
    public function render_admin_page( $default_tab = 'dashboard' ) {
        $current_page = isset( $_GET['page'] ) ? sanitize_key( $_GET['page'] ) : '';
        if ( 'wpsai-smart-scraper' === $current_page ) {
            $default_tab = 'scraper';
        } elseif ( 'wpsai-package-import' === $current_page ) {
            $default_tab = 'offline-scraper';
        } elseif ( 'wpsai-api-settings' === $current_page ) {
            $default_tab = 'settings';
        }
        ?>
        <div class="wrap wpsai-wrap">
            <header class="wpsai-header">
                <div class="wpsai-logo-section">
                    <span class="dashicons dashicons-database-import wpsai-logo-icon"></span>
                    <div>
                        <h1>WP Smart Auto-Importer & AI Generator</h1>
                        <p class="description"><?php esc_html_e( 'Quét cấu trúc trường & Nhập liệu/Sinh dữ liệu trực quan cho WordPress và ACF.', 'wp-acf-smart-importer' ); ?></p>
                    </div>
                </div>
                <div class="wpsai-header-actions">
                    <span class="wpsai-badge"><?php echo 'v' . esc_html( WPSAI_VERSION ); ?></span>
                </div>
            </header>

            <main class="wpsai-dashboard">
                <!-- Tabs Điều hướng -->
                <nav class="wpsai-nav-tabs">
                    <a href="#dashboard" class="wpsai-nav-tab <?php echo 'dashboard' === $default_tab ? 'active' : ''; ?>" data-tab="dashboard">
                        <span class="dashicons dashicons-search"></span> <?php esc_html_e( 'Quét Cấu Trúc & Excel Mẫu', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#import-runner" class="wpsai-nav-tab <?php echo 'import-runner' === $default_tab ? 'active' : ''; ?>" data-tab="import-runner">
                        <span class="dashicons dashicons-database-import"></span> <?php esc_html_e( 'Nhập Dữ Liệu Hàng Loạt', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#bulk-images" class="wpsai-nav-tab <?php echo 'bulk-images' === $default_tab ? 'active' : ''; ?>" data-tab="bulk-images">
                        <span class="dashicons dashicons-images-alt2"></span> <?php esc_html_e( 'Thêm Ảnh Hàng Loạt', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#bulk-excel" class="wpsai-nav-tab <?php echo 'bulk-excel' === $default_tab ? 'active' : ''; ?>" data-tab="bulk-excel">
                        <span class="dashicons dashicons-media-spreadsheet"></span> <?php esc_html_e( 'Nhập Excel Hàng Loạt', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#bulk-taxonomy" class="wpsai-nav-tab <?php echo 'bulk-taxonomy' === $default_tab ? 'active' : ''; ?>" data-tab="bulk-taxonomy">
                        <span class="dashicons dashicons-category"></span> <?php esc_html_e( 'Gán Phân Loại Hàng Loạt', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#export" class="wpsai-nav-tab <?php echo 'export' === $default_tab ? 'active' : ''; ?>" data-tab="export">
                        <span class="dashicons dashicons-database-export"></span> <?php esc_html_e( 'Xuất Dữ Liệu', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#get-titles" class="wpsai-nav-tab <?php echo 'get-titles' === $default_tab ? 'active' : ''; ?>" data-tab="get-titles">
                        <span class="dashicons dashicons-editor-ul"></span> <?php esc_html_e( 'Lấy Tiêu Đề Bài Viết', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#duplicate" class="wpsai-nav-tab <?php echo 'duplicate' === $default_tab ? 'active' : ''; ?>" data-tab="duplicate">
                        <span class="dashicons dashicons-admin-page"></span> <?php esc_html_e( 'Nhân Bản Hàng Loạt', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#ai-generator" class="wpsai-nav-tab <?php echo 'ai-generator' === $default_tab ? 'active' : ''; ?>" data-tab="ai-generator">
                        <span class="dashicons dashicons-lightbulb"></span> <?php esc_html_e( 'Tạo Nội Dung AI', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#scraper" class="wpsai-nav-tab <?php echo 'scraper' === $default_tab ? 'active' : ''; ?>" data-tab="scraper">
                        <span class="dashicons dashicons-admin-links"></span> <?php esc_html_e( 'Cào Bài Viết (URL)', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#offline-scraper" class="wpsai-nav-tab <?php echo 'offline-scraper' === $default_tab ? 'active' : ''; ?>" data-tab="offline-scraper">
                        <span class="dashicons dashicons-media-code"></span> <?php esc_html_e( 'Cào HTML & Package', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#settings" class="wpsai-nav-tab <?php echo 'settings' === $default_tab ? 'active' : ''; ?>" data-tab="settings">
                        <span class="dashicons dashicons-admin-generic"></span> <?php esc_html_e( 'Cấu Hình API Key', 'wp-acf-smart-importer' ); ?>
                    </a>
                    <a href="#snapshot-repo" class="wpsai-nav-tab <?php echo 'snapshot-repo' === $default_tab ? 'active' : ''; ?>" data-tab="snapshot-repo">
                        <span class="dashicons dashicons-database"></span> <?php esc_html_e( 'Kho Dữ Liệu Mẫu', 'wp-acf-smart-importer' ); ?>
                    </a>
                </nav>

                <!-- Tab 1: Bảng Điều Khiển Chính -->
                <section id="wpsai-tab-dashboard" class="wpsai-tab-content <?php echo 'dashboard' === $default_tab ? 'active' : ''; ?>">
                    <!-- Bước 1: Chọn bài viết mẫu/đích -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Chọn Bài Viết Quét Cấu Trúc Trường', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn Post Type và bài viết đích để quét tất cả các trường cốt lõi và trường tùy chỉnh (ACF / Postmeta).', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-flex-row select-post-row" style="align-items: flex-end;">
                            <div class="wpsai-form-group">
                                <label for="wpsai-post-type"><strong><?php esc_html_e( 'Chọn Post Type:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-post-type" class="large-text">
                                    <!-- Post Types load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group">
                                <label for="wpsai-target-post"><strong><?php esc_html_e( 'Chọn Bài Viết:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-target-post" class="large-text">
                                    <option value=""><?php esc_html_e( '-- Chọn bài viết --', 'wp-acf-smart-importer' ); ?></option>
                                    <!-- Posts load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group-btn">
                                <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-create-blank-btn">
                                    <span class="dashicons dashicons-plus-alt"></span> <?php esc_html_e( 'Tạo Bài Viết Rỗng Mới', 'wp-acf-smart-importer' ); ?>
                                </button>
                                <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-scan-btn">
                                    <span class="dashicons dashicons-search"></span> <?php esc_html_e( 'Quét Các Trường Bài Viết', 'wp-acf-smart-importer' ); ?>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2: Bảng Cấu Trúc Trường & Giá Trị (Ẩn mặc định) -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-step-fields" style="display:none;">
                        <div class="wpsai-card-header-flex" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h2 style="margin: 0;"><?php esc_html_e( 'Bước 2: Cấu Trúc Các Trường & Giá Trị Bài Viết', 'wp-acf-smart-importer' ); ?></h2>
                            <div class="wpsai-card-header-actions">
                                <label class="wpsai-checkbox-label">
                                    <input type="checkbox" id="wpsai-show-system-fields" value="1">
                                    <span><?php esc_html_e( 'Hiện các trường ẩn hệ thống (Bắt đầu bằng dấu _)', 'wp-acf-smart-importer' ); ?></span>
                                </label>
                            </div>
                        </div>
                        <p class="description-p"><?php esc_html_e( 'Dưới đây là danh sách các trường được phát hiện trên bài viết này. Bạn có thể sửa trực tiếp ở cột "Giá trị hiện tại" và cập nhật nhanh, hoặc nạp file / sinh dữ liệu mẫu để điền đè.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-table-container">
                            <table class="wpsai-preview-table" id="wpsai-fields-table">
                                <thead>
                                    <tr>
                                        <th style="width: 20%;"><?php esc_html_e( 'Nhãn Trường (Label)', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 15%;"><?php esc_html_e( 'Khóa Trường (Key / Name)', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 15%;"><?php esc_html_e( 'Loại Trường', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 20%;"><?php esc_html_e( 'Giá trị hiện tại', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 15%;" class="source-mapping-col" style="display:none;"><?php esc_html_e( 'Cột Dữ Liệu Nguồn', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 15%;" class="preview-val-col" style="display:none;"><?php esc_html_e( 'Giá Trị Xem Trước', 'wp-acf-smart-importer' ); ?></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- Dữ liệu trường render động -->
                                </tbody>
                            </table>
                        </div>

                        <div class="wpsai-actions-row" style="margin-top: 15px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                            <button type="button" class="wpsai-btn wpsai-btn-success" id="wpsai-direct-update-btn">
                                <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Lưu/Cập nhật trực tiếp bài viết', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-download-sample-excel-btn" title="<?php esc_attr_e( 'Tải xuống file Excel mẫu với tiêu đề cột khớp các trường đã quét, kèm 1 dòng dữ liệu mẫu để tham khảo.', 'wp-acf-smart-importer' ); ?>">
                                <span class="dashicons dashicons-download"></span> <?php esc_html_e( 'Tải File Excel Mẫu', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-download-sample-json-btn" title="<?php esc_attr_e( 'Tải xuống file JSON mẫu chứa toàn bộ cấu trúc trường và dữ liệu mẫu chuẩn.', 'wp-acf-smart-importer' ); ?>">
                                <span class="dashicons dashicons-media-code"></span> <?php esc_html_e( 'Tải File JSON Mẫu', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-copy-ai-prompt-btn" style="border-color: #818cf8; color: #4338ca;" title="<?php esc_attr_e( 'Sao chép nhanh Prompt và Khung JSON chuẩn sang Clipboard để nạp vào ChatGPT, Claude, DeepSeek...', 'wp-acf-smart-importer' ); ?>">
                                <span class="dashicons dashicons-clipboard"></span> <?php esc_html_e( 'Copy Prompt & Khung JSON AI', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-step2-ai-toggle-btn" style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border: none; color: #fff;">
                                <span class="dashicons dashicons-superhero"></span> <?php esc_html_e( 'Tự Sinh Dữ Liệu Gemini AI', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <span id="wpsai-direct-update-msg" class="wpsai-status-msg"></span>
                        </div>

                        <!-- Khung Cấu Hình Tự Sinh Dữ Liệu Gemini AI (Hiện khi bấm nút) -->
                        <div id="wpsai-step2-ai-box" style="display:none; margin-top: 15px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 18px;">
                            <h3 style="margin-top: 0; color: #166534; display: flex; align-items: center; gap: 8px; font-size: 15px;">
                                <span class="dashicons dashicons-superhero" style="color: #16a34a; font-size: 20px; width: 20px; height: 20px;"></span>
                                <?php esc_html_e( 'Tự Động Sinh Dữ Liệu Cho Các Trường Bằng Gemini AI', 'wp-acf-smart-importer' ); ?>
                            </h3>
                            <p style="margin-bottom: 12px; color: #15803d; font-size: 13px;">
                                <?php esc_html_e( 'Gemini AI sẽ phân tích toàn bộ cấu trúc trường cốt lõi, ACF & Custom Meta của bài viết/sản phẩm này để tạo nội dung chuẩn SEO, thông số kỹ thuật và ảnh minh họa tương ứng.', 'wp-acf-smart-importer' ); ?>
                            </p>

                            <div style="display: grid; grid-template-columns: 2fr 1fr 1.5fr; gap: 12px; margin-bottom: 15px;">
                                <div>
                                    <label for="wpsai-step2-ai-topic"><strong><?php esc_html_e( 'Chủ đề / Ngữ cảnh sản phẩm:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <input type="text" id="wpsai-step2-ai-topic" class="large-text" style="width: 100%; margin-top: 4px;" placeholder="<?php esc_attr_e( 'Ví dụ: Xe Đạp Trợ Lực Điện Samebike C05...', 'wp-acf-smart-importer' ); ?>">
                                </div>
                                <div>
                                    <label for="wpsai-step2-ai-count"><strong><?php esc_html_e( 'Số lượng bài cần sinh:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <input type="number" id="wpsai-step2-ai-count" value="1" min="1" max="50" class="small-text" style="width: 100%; margin-top: 4px;">
                                </div>
                                <div>
                                    <label for="wpsai-step2-ai-target"><strong><?php esc_html_e( 'Mục tiêu áp dụng:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <select id="wpsai-step2-ai-target" style="width: 100%; margin-top: 4px;">
                                        <option value="current_post" selected><?php esc_html_e( 'Điền vào bài viết hiện tại (1 bài)', 'wp-acf-smart-importer' ); ?></option>
                                        <option value="batch_preview"><?php esc_html_e( 'Tạo N bài mẫu mới (Import hàng loạt)', 'wp-acf-smart-importer' ); ?></option>
                                    </select>
                                </div>
                            </div>

                            <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                                <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-step2-ai-run-btn" style="background: #16a34a; border-color: #15803d;">
                                    <span class="dashicons dashicons-update"></span> <?php esc_html_e( 'Khởi Chạy Sinh Dữ Liệu AI', 'wp-acf-smart-importer' ); ?>
                                </button>
                                <span id="wpsai-step2-ai-status" style="font-weight: 600; font-size: 13px;"></span>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Tab 2: Nhập Dữ Liệu Hàng Loạt -->
                <section id="wpsai-tab-import-runner" class="wpsai-tab-content <?php echo 'import-runner' === $default_tab ? 'active' : ''; ?>">
                    <!-- Bước 3: Phương thức điền dữ liệu -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-step-fill">
                        <h2><?php esc_html_e( 'Bước 1: Chọn Cách Nạp Dữ Liệu (File Excel, AI hoặc Raw Data)', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Bạn có thể tự sinh dữ liệu mẫu ngẫu nhiên (AI/Rule) hoặc tải lên file dữ liệu Excel/CSV/JSON/Google Sheet để xem trước.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-fill-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                            <!-- Cột trái: Tự sinh dữ liệu mẫu -->
                            <div class="wpsai-fill-col" style="border-right: 1px solid #eee; padding-right: 20px;">
                                <h3><span class="dashicons dashicons-admin-generic" style="color: #2563eb;"></span> <?php esc_html_e( 'Cách A: Tự Sinh Dữ Liệu Mẫu (Mock / AI Generator)', 'wp-acf-smart-importer' ); ?></h3>
                                <div class="wpsai-generator-settings" style="margin-top: 10px;">
                                    <div class="wpsai-form-group" style="margin-bottom: 10px;">
                                        <label for="wpsai-gen-topic"><strong><?php esc_html_e( 'Chủ đề / Ngữ cảnh bài viết:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="text" id="wpsai-gen-topic" class="large-text" style="width: 100%; margin-top: 4px;" placeholder="<?php esc_attr_e( 'Ví dụ: Thiết kế nội thất chung cư, Đồng hồ Thụy Sĩ, Du lịch Phú Quốc...', 'wp-acf-smart-importer' ); ?>">
                                    </div>

                                    <div class="wpsai-flex-row" style="gap: 10px; margin-bottom: 10px;">
                                        <div class="wpsai-form-group" style="flex: 1;">
                                            <label for="wpsai-gen-length"><strong><?php esc_html_e( 'Độ dài bài viết:', 'wp-acf-smart-importer' ); ?></strong></label>
                                            <select id="wpsai-gen-length" style="width: 100%; margin-top: 4px;">
                                                <option value="medium" selected><?php esc_html_e( 'Vừa (~600 - 1000 từ)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="short"><?php esc_html_e( 'Ngắn (~300 - 500 từ)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="long"><?php esc_html_e( 'Dài chuẩn SEO (~1200 - 2000 từ)', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </div>

                                        <div class="wpsai-form-group" style="flex: 1;">
                                            <label for="wpsai-gen-tone"><strong><?php esc_html_e( 'Văn phong bài viết:', 'wp-acf-smart-importer' ); ?></strong></label>
                                            <select id="wpsai-gen-tone" style="width: 100%; margin-top: 4px;">
                                                <option value="seo" selected><?php esc_html_e( 'Chuyên nghiệp & Chuẩn SEO', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="sales"><?php esc_html_e( 'Thuyết phục & Bán hàng', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="friendly"><?php esc_html_e( 'Thân thiện & Chia sẻ', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="news"><?php esc_html_e( 'Trang trọng & Tin tức', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </div>
                                    </div>

                                    <div class="wpsai-flex-row" style="gap: 10px; margin-bottom: 10px;">
                                        <div class="wpsai-form-group" style="flex: 1;">
                                            <label for="wpsai-gen-lang"><strong><?php esc_html_e( 'Ngôn ngữ:', 'wp-acf-smart-importer' ); ?></strong></label>
                                            <select id="wpsai-gen-lang" style="width: 100%; margin-top: 4px;">
                                                <option value="vi" selected><?php esc_html_e( 'Tiếng Việt (Vietnamese)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="en"><?php esc_html_e( 'Tiếng Anh (English)', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </div>

                                        <div class="wpsai-form-group" style="flex: 1;">
                                            <label for="wpsai-gen-count"><strong><?php esc_html_e( 'Số lượng bài ảo cần sinh:', 'wp-acf-smart-importer' ); ?></strong></label>
                                            <input type="number" id="wpsai-gen-count" value="5" min="1" max="100" class="small-text" style="width: 100%; margin-top: 4px;">
                                        </div>
                                    </div>

                                    <div class="wpsai-form-group" style="margin-bottom: 10px;">
                                        <label><strong><?php esc_html_e( 'Thuật toán tạo dữ liệu:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <div class="wpsai-radio-group" style="margin: 5px 0;">
                                            <label><input type="radio" name="wpsai_gen_mode" value="rule" checked> <?php esc_html_e( 'Thuật toán (Rule-based nhanh)', 'wp-acf-smart-importer' ); ?></label> &nbsp;&nbsp;
                                            <label><input type="radio" name="wpsai_gen_mode" value="ai"> <?php esc_html_e( 'Google Gemini AI (Chất lượng cao)', 'wp-acf-smart-importer' ); ?></label>
                                        </div>
                                    </div>

                                    <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-start-generate-btn" style="margin-top: 10px; width: 100%;">
                                        <span class="dashicons dashicons-lightbulb"></span> <?php esc_html_e( 'Khởi Chạy Sinh Dữ Liệu Mẫu', 'wp-acf-smart-importer' ); ?>
                                    </button>
                                </div>
                            </div>

                            <!-- Cột phải: Nhập từ File -->
                            <div class="wpsai-fill-col">
                                <h3><span class="dashicons dashicons-upload"></span> <?php esc_html_e( 'Cách B: Tải dữ liệu từ File', 'wp-acf-smart-importer' ); ?></h3>
                                <div class="wpsai-source-selector" style="margin-top: 10px; display: flex; gap: 10px; margin-bottom: 10px;">
                                    <label class="wpsai-source-option active" style="flex: 1; text-align: center;">
                                        <input type="radio" name="wpsai_source_type" value="excel" checked style="display:none;">
                                        <span class="wpsai-option-label">Excel/CSV</span>
                                    </label>
                                    <label class="wpsai-source-option" style="flex: 1; text-align: center;">
                                        <input type="radio" name="wpsai_source_type" value="gsheet" style="display:none;">
                                        <span class="wpsai-option-label">Google Sheet</span>
                                    </label>
                                    <label class="wpsai-source-option" style="flex: 1; text-align: center;">
                                        <input type="radio" name="wpsai_source_type" value="json" style="display:none;">
                                        <span class="wpsai-option-label">JSON</span>
                                    </label>
                                    <label class="wpsai-source-option" style="flex: 1; text-align: center;">
                                        <input type="radio" name="wpsai_source_type" value="notepad" style="display:none;">
                                        <span class="wpsai-option-label">Notepad</span>
                                    </label>
                                </div>

                                <div class="wpsai-source-inputs" style="margin-top: 10px;">
                                    <!-- Excel Input -->
                                    <div class="wpsai-input-group source-field-group" id="group-excel">
                                        <div class="wpsai-drag-drop-zone" id="wpsai-drop-zone" style="border: 2px dashed #ccc; padding: 20px; text-align: center; border-radius: 5px; background: #fafafa;">
                                            <span class="dashicons dashicons-cloud-upload upload-icon" style="font-size: 40px; width: 40px; height: 40px; margin-bottom: 10px; color: #888;"></span>
                                            <p><?php esc_html_e( 'Kéo thả file Excel (.xlsx, .xls, .csv) hoặc click để chọn', 'wp-acf-smart-importer' ); ?></p>
                                            <input type="file" id="wpsai-excel-file" accept=".xlsx, .xls, .csv" style="display: none;">
                                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-browse-btn"><?php esc_html_e( 'Chọn File', 'wp-acf-smart-importer' ); ?></button>
                                        </div>
                                        <div class="wpsai-file-info" style="display:none; padding: 10px; background: #e7f5ea; border-radius: 3px; display: flex; align-items: center; justify-content: space-between;">
                                            <div>
                                                <span class="dashicons dashicons-yes-alt success-icon" style="color: #46b450; margin-right: 5px;"></span>
                                                <span class="wpsai-filename" style="font-weight: bold;"></span>
                                            </div>
                                            <button type="button" class="wpsai-btn-remove" id="wpsai-remove-file" style="border:none; background:none; cursor:pointer; font-size:18px; font-weight:bold;">&times;</button>
                                        </div>
                                    </div>

                                    <!-- Google Sheets Input -->
                                    <div class="wpsai-input-group source-field-group" id="group-gsheet" style="display: none;">
                                        <input type="url" id="wpsai-gsheet-url" class="large-text" placeholder="https://docs.google.com/spreadsheets/d/.../edit?usp=sharing" style="width: 100%;">
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-load-gsheet-btn" style="margin-top:5px;"><?php esc_html_e( 'Tải Dữ Liệu Sheet', 'wp-acf-smart-importer' ); ?></button>
                                    </div>

                                    <!-- JSON Input -->
                                    <div class="wpsai-input-group source-field-group" id="group-json" style="display: none;">
                                        <input type="file" id="wpsai-json-file" accept=".json" class="button" style="margin-bottom:5px;">
                                        <textarea id="wpsai-json-raw" rows="4" class="large-text code" placeholder='[{"post_title": "Bài viết 1", "acf_price": "150000"}]' style="width: 100%;"></textarea>
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-load-json-btn" style="margin-top:5px;"><?php esc_html_e( 'Phân Tích JSON', 'wp-acf-smart-importer' ); ?></button>
                                    </div>

                                    <!-- Notepad Input -->
                                    <div class="wpsai-input-group source-field-group" id="group-notepad" style="display: none;">
                                        <div class="wpsai-notepad-settings" style="margin-bottom:5px;">
                                            <label for="wpsai-notepad-delimiter"><?php esc_html_e( 'Dấu phân tách cột:', 'wp-acf-smart-importer' ); ?></label>
                                            <select id="wpsai-notepad-delimiter">
                                                <option value="tab"><?php esc_html_e( 'Tab (Mặc định Excel)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="comma"><?php esc_html_e( 'Dấu phẩy ( , )', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="pipe"><?php esc_html_e( 'Dấu gạch đứng ( | )', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </div>
                                        <textarea id="wpsai-notepad-raw" rows="4" class="large-text" placeholder="Tiêu đề bài viết	Giá bán&#10;Sản phẩm mẫu 1	150000" style="width: 100%;"></textarea>
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-load-notepad-btn" style="margin-top:5px;"><?php esc_html_e( 'Phân Tích Văn Bản', 'wp-acf-smart-importer' ); ?></button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Bộ chuyển đổi chuyển dòng xem trước dữ liệu nạp được -->
                        <div class="wpsai-row-navigator" id="wpsai-row-navigator" style="display:none; margin-top:20px; text-align:center; padding:15px; border-top:1px solid #ddd; background:#f9f9f9; border-radius:5px;">
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-prev-row-btn">&laquo; <?php esc_html_e( 'Dòng trước', 'wp-acf-smart-importer' ); ?></button>
                            <span style="margin: 0 15px; font-weight:bold; font-size:14px;"><?php esc_html_e( 'Xem trước dòng:', 'wp-acf-smart-importer' ); ?> <strong id="wpsai-current-row-idx">0</strong> / <strong id="wpsai-total-rows-idx">0</strong></span>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-next-row-btn"><?php esc_html_e( 'Dòng sau', 'wp-acf-smart-importer' ); ?> &raquo;</button>
                        </div>
                    </div>

                    <!-- Bước 4: Cấu hình & Thực thi Import -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-step-import-execute">
                        <h2><?php esc_html_e( 'Bước 2: Cấu Hình & Thực Thi Import Dữ Liệu Hàng Loạt', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Cấu hình Post Type đích, số lượng bài viết, trạng thái và khoảng ngày tháng khởi tạo ngẫu nhiên/tuần tự như wp-dummy-content-generator.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-grid-options" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                            <!-- Cột 1: Post Type, Trạng thái & Chế độ -->
                            <div class="wpsai-option-box" style="background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
                                <h3 style="margin-top: 0; font-size: 14px; color: #1e293b;"><span class="dashicons dashicons-admin-settings" style="color: #2563eb;"></span> <?php esc_html_e( 'Cấu Hình Đích & Chế Độ Import', 'wp-acf-smart-importer' ); ?></h3>
                                
                                <div class="wpsai-form-group" style="margin-bottom: 12px;">
                                    <label for="wpsai-runner-post-type"><strong><?php esc_html_e( 'Chọn Post Type Đích:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <select id="wpsai-runner-post-type" class="large-text" style="width: 100%; margin-top: 4px;">
                                        <!-- Post Types load qua AJAX -->
                                    </select>
                                </div>

                                <div class="wpsai-form-group" style="margin-bottom: 12px;">
                                    <label for="wpsai-post-status"><strong><?php esc_html_e( 'Trạng thái bài viết mặc định:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <select id="wpsai-post-status" class="large-text" style="width: 100%; margin-top: 4px;">
                                        <option value="publish" selected><?php esc_html_e( 'Đã đăng (Publish)', 'wp-acf-smart-importer' ); ?></option>
                                        <option value="pending"><?php esc_html_e( 'Chờ duyệt (Pending)', 'wp-acf-smart-importer' ); ?></option>
                                        <option value="draft"><?php esc_html_e( 'Bản nháp (Draft)', 'wp-acf-smart-importer' ); ?></option>
                                    </select>
                                </div>

                                <div class="wpsai-form-group">
                                    <label><strong><?php esc_html_e( 'Chế độ ghi dữ liệu:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <div style="margin-top: 6px;">
                                        <label class="wpsai-radio-label">
                                            <input type="radio" name="wpsai_import_mode" value="create_batch" checked>
                                            <strong><?php esc_html_e( 'Tạo hàng loạt bài viết mới', 'wp-acf-smart-importer' ); ?></strong>
                                        </label>
                                        <br/>
                                        <label class="wpsai-radio-label" style="margin-top: 6px; display: inline-block;">
                                            <input type="radio" name="wpsai_import_mode" value="update_current">
                                            <strong><?php esc_html_e( 'Chỉ cập nhật bài viết mẫu đang chọn', 'wp-acf-smart-importer' ); ?></strong>
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <!-- Cột 2: Cấu hình Khoảng Ngày Tháng (Date Range) -->
                            <div class="wpsai-option-box" style="background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">
                                <h3 style="margin-top: 0; font-size: 14px; color: #1e293b;"><span class="dashicons dashicons-calendar-alt" style="color: #10b981;"></span> <?php esc_html_e( 'Cấu Hình Ngày Đăng Bài (Date Range)', 'wp-acf-smart-importer' ); ?></h3>
                                
                                <div class="wpsai-form-group" style="margin-bottom: 12px;">
                                    <label for="wpsai-date-mode"><strong><?php esc_html_e( 'Kiểu phát sinh ngày tạo:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <select id="wpsai-date-mode" class="large-text" style="width: 100%; margin-top: 4px;">
                                        <option value="now" selected><?php esc_html_e( 'Thời gian hiện tại (Now)', 'wp-acf-smart-importer' ); ?></option>
                                        <option value="random_range"><?php esc_html_e( 'Ngẫu nhiên trong khoảng ngày (Random Date Range)', 'wp-acf-smart-importer' ); ?></option>
                                        <option value="sequential"><?php esc_html_e( 'Tăng dần đều từ Từ Ngày -> Đến Ngày', 'wp-acf-smart-importer' ); ?></option>
                                    </select>
                                </div>

                                <div class="wpsai-date-range-inputs" id="wpsai-date-range-wrapper" style="display: none; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-date-from"><strong><?php esc_html_e( 'Từ ngày:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="date" id="wpsai-date-from" class="large-text" style="width: 100%; margin-top: 4px;">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-date-to"><strong><?php esc_html_e( 'Đến ngày:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="date" id="wpsai-date-to" class="large-text" style="width: 100%; margin-top: 4px;">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="wpsai-actions-row" style="margin-top: 15px; display: flex; align-items: center; justify-content: space-between;">
                            <div>
                                <span style="font-size: 14px; font-weight: 600; color: #475569;">
                                    <?php esc_html_e( 'Tổng số bài viết chuẩn bị tạo:', 'wp-acf-smart-importer' ); ?> 
                                    <span id="wpsai-batch-count-display" class="wpsai-badge" style="font-size: 14px; background: #2563eb;">0</span>
                                </span>
                            </div>
                            <button type="button" class="wpsai-btn wpsai-btn-primary wpsai-btn-large" id="wpsai-start-import-btn">
                                <span class="dashicons dashicons-database-import"></span> <?php esc_html_e( 'Bắt Đầu Thực Thi Nhập Liệu', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>

                    <!-- Tiến trình thực thi (Ẩn mặc định) -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-step-progress" style="display:none;">
                        <h2><?php esc_html_e( 'Tiến Trình Thực Thi', 'wp-acf-smart-importer' ); ?></h2>
                        <div class="wpsai-progress-bar-wrapper">
                            <div class="wpsai-progress-bar" id="wpsai-import-progress-bar" style="width: 0%;">0%</div>
                        </div>
                        <div class="wpsai-progress-stats" id="wpsai-import-progress-stats">
                            <p><?php esc_html_e( 'Đang chuẩn bị dữ liệu...', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        <div class="wpsai-import-log" id="wpsai-import-log">
                            <!-- Nhật ký log tiến trình -->
                        </div>
                    </div>
                </section>

                <!-- Tab: Thêm Ảnh Hàng Loạt -->
                <section id="wpsai-tab-bulk-images" class="wpsai-tab-content">
                    <!-- Bước 1: Chọn bài viết đích -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Chọn Post Type & Các Bài Viết Nhận Ảnh', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn Post Type để lấy toàn bộ bài viết, sau đó chọn các bài viết cụ thể để gán ảnh đại diện.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-form-group select-post-type-row" style="margin-bottom: 15px;">
                            <label for="wpsai-bulk-images-post-type"><strong><?php esc_html_e( 'Chọn Post Type:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <select id="wpsai-bulk-images-post-type" class="large-text" style="width: auto; min-width: 250px;">
                                <!-- Post Types load qua AJAX -->
                            </select>
                        </div>

                        <!-- Bộ lọc và Bảng danh sách bài viết -->
                        <div class="wpsai-posts-selector-wrapper" style="display:none; margin-top: 20px;">
                            <div class="wpsai-flex-row" style="margin-bottom: 10px; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <label class="wpsai-checkbox-label">
                                        <input type="checkbox" id="wpsai-bulk-images-select-all" value="1">
                                        <strong><?php esc_html_e( 'Chọn tất cả', 'wp-acf-smart-importer' ); ?></strong>
                                    </label>
                                    <span id="wpsai-bulk-images-selected-count" style="color: var(--wpsai-primary); font-weight: 600;">Đã chọn: 0/0 bài viết</span>
                                </div>
                                <div>
                                    <input type="text" id="wpsai-bulk-images-search" placeholder="<?php esc_attr_e( 'Tìm kiếm bài viết...', 'wp-acf-smart-importer' ); ?>" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); width: 250px;">
                                </div>
                            </div>

                            <div class="wpsai-table-container" style="max-height: 250px;">
                                <table class="wpsai-preview-table" id="wpsai-bulk-images-posts-table">
                                    <thead>
                                        <tr>
                                            <th style="width: 50px; text-align: center;"></th>
                                            <th style="width: 80px;"><?php esc_html_e( 'Ảnh Hiện Tại', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 80px;"><?php esc_html_e( 'ID', 'wp-acf-smart-importer' ); ?></th>
                                            <th><?php esc_html_e( 'Tiêu Đề Bài Viết', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 150px;"><?php esc_html_e( 'Ngày Tạo', 'wp-acf-smart-importer' ); ?></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Render động -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2: Chọn nhiều ảnh từ Media Library -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 2: Chọn / Tải Lên Danh Sách Ảnh', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn từ thư viện ảnh hoặc kéo thả tải lên nhiều ảnh (Đề xuất: 5 - 10 ảnh). Những ảnh này sẽ được phân phối làm ảnh đại diện cho các bài viết đã chọn.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div style="margin-top: 15px;">
                            <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-bulk-images-select-btn">
                                <span class="dashicons dashicons-images-alt2"></span> <?php esc_html_e( 'Chọn / Tải lên ảnh từ Thư viện', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-bulk-images-clear-btn" style="margin-left: 10px; display: none;">
                                <?php esc_html_e( 'Xóa danh sách ảnh đã chọn', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>

                        <!-- Grid hiển thị ảnh đã chọn -->
                        <div id="wpsai-bulk-images-preview-container" style="display: none; margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee;">
                            <p style="font-weight: 600; margin-bottom: 10px;"><?php esc_html_e( 'Danh sách ảnh đã chọn để gán:', 'wp-acf-smart-importer' ); ?> <span id="wpsai-bulk-images-count-badge" class="wpsai-badge" style="background:var(--wpsai-primary); padding:2px 8px; font-size:11px;">0 ảnh</span></p>
                            <div class="wpsai-images-preview-grid" id="wpsai-bulk-images-preview-grid">
                                <!-- Render động -->
                            </div>
                        </div>
                    </div>

                    <!-- Bước 3: Chọn thuật toán / Chế độ phân bổ -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 3: Chọn Kiểu Phân Bổ Ảnh', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Thiết lập cách thức gán tập ảnh đã chọn vào danh sách bài viết.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-generator-modes" style="margin-top: 15px;">
                            <!-- Chế độ Thứ tự -->
                            <label class="wpsai-radio-card active">
                                <input type="radio" name="wpsai_bulk_images_mode" value="sequential" checked>
                                <div class="wpsai-radio-card-content">
                                    <h4><?php esc_html_e( 'Theo Thứ Tự (Sequential)', 'wp-acf-smart-importer' ); ?></h4>
                                    <p><?php esc_html_e( 'Gán lần lượt: Bài 1 nhận ảnh 1, Bài 2 nhận ảnh 2, Bài 3 nhận ảnh 3... Lặp lại vòng tuần hoàn nếu hết ảnh.', 'wp-acf-smart-importer' ); ?></p>
                                </div>
                            </label>

                            <!-- Chế độ Ngẫu nhiên -->
                            <label class="wpsai-radio-card">
                                <input type="radio" name="wpsai_bulk_images_mode" value="random">
                                <div class="wpsai-radio-card-content">
                                    <h4><?php esc_html_e( 'Ngẫu Nhiên (Random)', 'wp-acf-smart-importer' ); ?></h4>
                                    <p><?php esc_html_e( 'Mỗi bài viết sẽ được gán ngẫu nhiên một bức ảnh từ danh sách ảnh đã chọn.', 'wp-acf-smart-importer' ); ?></p>
                                </div>
                            </label>

                            <!-- Chế độ Khoảng -->
                            <label class="wpsai-radio-card">
                                <input type="radio" name="wpsai_bulk_images_mode" value="range">
                                <div class="wpsai-radio-card-content">
                                    <h4><?php esc_html_e( 'Theo Khoảng (Range/Interval)', 'wp-acf-smart-importer' ); ?></h4>
                                    <p><?php esc_html_e( 'Cứ một khoảng N bài viết liên tiếp sẽ được gán chung 1 ảnh. Hết N bài viết tiếp theo sẽ đổi sang ảnh tiếp theo.', 'wp-acf-smart-importer' ); ?></p>
                                </div>
                            </label>
                        </div>

                        <!-- Cài đặt khoảng riêng biệt -->
                        <div id="wpsai-bulk-images-range-setting" style="display: none; margin-top: 20px; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid var(--wpsai-border-color);">
                            <div class="wpsai-form-group" style="margin-bottom: 0;">
                                <label for="wpsai-bulk-images-range-size"><strong><?php esc_html_e( 'Số lượng bài viết trên mỗi khoảng (N):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="number" id="wpsai-bulk-images-range-size" value="3" min="1" max="100" class="small-text" style="padding: 6px 10px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); margin-left: 10px;">
                                <span class="description" style="margin-left: 10px;"><?php esc_html_e( '(Mỗi ảnh sẽ được lặp lại N bài viết rồi chuyển qua ảnh kế tiếp)', 'wp-acf-smart-importer' ); ?></span>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 4: Thực thi -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 4: Thực Thi Cập Nhật', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Bắt đầu quá trình gán ảnh đại diện tự động dựa trên cấu hình đã chọn.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-actions-row">
                            <button type="button" class="wpsai-btn wpsai-btn-primary wpsai-btn-large" id="wpsai-bulk-images-start-btn">
                                <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Bắt Đầu Gán Ảnh Đại Diện', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>

                    <!-- Tiến trình gán ảnh (Ẩn mặc định) -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-bulk-images-progress-card" style="display:none;">
                        <h2><?php esc_html_e( 'Tiến Trình Thực Thi', 'wp-acf-smart-importer' ); ?></h2>
                        <div class="wpsai-progress-bar-wrapper">
                            <div class="wpsai-progress-bar" id="wpsai-bulk-images-progress-bar" style="width: 0%;">0%</div>
                        </div>
                        <div class="wpsai-progress-stats" id="wpsai-bulk-images-progress-stats">
                            <p><?php esc_html_e( 'Đang chuẩn bị dữ liệu...', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        <div class="wpsai-import-log" id="wpsai-bulk-images-log">
                            <!-- Nhật ký log tiến trình -->
                        </div>
                    </div>
                </section>

                <!-- Tab: Nhập Excel Hàng Loạt -->
                <section id="wpsai-tab-bulk-excel" class="wpsai-tab-content">
                    <!-- Bước 1: Chọn Post Type & Các Bài Viết Nhận Dữ Liệu -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Chọn Post Type & Các Bài Viết Nhận Dữ Liệu', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn Post Type để lấy danh sách bài viết, sau đó chọn các bài viết cụ thể để cập nhật từ file Excel.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-form-group select-post-type-row" style="margin-bottom: 15px;">
                            <label for="wpsai-bulk-excel-post-type"><strong><?php esc_html_e( 'Chọn Post Type:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <select id="wpsai-bulk-excel-post-type" class="large-text" style="width: auto; min-width: 250px;">
                                <!-- Post Types load qua AJAX -->
                            </select>
                        </div>

                        <!-- Bộ lọc và Bảng danh sách bài viết -->
                        <div class="wpsai-posts-selector-wrapper" id="wpsai-bulk-excel-posts-wrapper" style="display:none; margin-top: 20px;">
                            <div class="wpsai-flex-row" style="margin-bottom: 10px; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <label class="wpsai-checkbox-label">
                                        <input type="checkbox" id="wpsai-bulk-excel-select-all" value="1">
                                        <strong><?php esc_html_e( 'Chọn tất cả', 'wp-acf-smart-importer' ); ?></strong>
                                    </label>
                                    <span id="wpsai-bulk-excel-selected-count" style="color: var(--wpsai-primary); font-weight: 600;">Đã chọn: 0/0 bài viết</span>
                                </div>
                                <div>
                                    <input type="text" id="wpsai-bulk-excel-search" placeholder="<?php esc_attr_e( 'Tìm kiếm bài viết...', 'wp-acf-smart-importer' ); ?>" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); width: 250px;">
                                </div>
                            </div>

                            <div class="wpsai-table-container" style="max-height: 250px;">
                                <table class="wpsai-preview-table" id="wpsai-bulk-excel-posts-table">
                                    <thead>
                                        <tr>
                                            <th style="width: 50px; text-align: center;"></th>
                                            <th style="width: 80px;"><?php esc_html_e( 'Ảnh Hiện Tại', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 80px;"><?php esc_html_e( 'ID', 'wp-acf-smart-importer' ); ?></th>
                                            <th><?php esc_html_e( 'Tiêu Đề Bài Viết', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 150px;"><?php esc_html_e( 'Ngày Tạo', 'wp-acf-smart-importer' ); ?></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Render động -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2: Chọn / Tải Lên Nguồn Dữ Liệu -->
                    <div class="wpsai-card" id="wpsai-bulk-excel-upload-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 2: Cung Cấp Dữ Liệu Nguồn', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn tải file Excel hoặc dán văn bản trực tiếp từ Clipboard để cập nhật nhanh.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <!-- Toggle nguồn dữ liệu -->
                        <div class="wpsai-source-selector" style="margin-top: 15px; display: flex; gap: 10px; margin-bottom: 20px;">
                            <label class="wpsai-source-option wpsai-bulk-source-option active" style="flex: 1; text-align: center;">
                                <input type="radio" name="wpsai_bulk_source_mode" value="file" checked style="display:none;">
                                <span class="wpsai-option-label"><span class="dashicons dashicons-media-spreadsheet" style="margin-right: 5px; vertical-align: middle;"></span><?php esc_html_e( 'Tải File Excel/CSV', 'wp-acf-smart-importer' ); ?></span>
                            </label>
                            <label class="wpsai-source-option wpsai-bulk-source-option" style="flex: 1; text-align: center;">
                                <input type="radio" name="wpsai_bulk_source_mode" value="paste" style="display:none;">
                                <span class="wpsai-option-label"><span class="dashicons dashicons-editor-paste" style="margin-right: 5px; vertical-align: middle;"></span><?php esc_html_e( 'Dán Văn Bản (Copy-Paste)', 'wp-acf-smart-importer' ); ?></span>
                            </label>
                        </div>

                        <!-- Khung 1: Tải File Excel -->
                        <div id="wpsai-bulk-source-file-wrapper">
                            <div class="wpsai-drag-drop-zone" id="wpsai-bulk-excel-drop-zone" style="border: 2px dashed #ccc; padding: 20px; text-align: center; border-radius: 5px; background: #fafafa;">
                                <span class="dashicons dashicons-cloud-upload upload-icon" style="font-size: 40px; width: 40px; height: 40px; margin-bottom: 10px; color: #888;"></span>
                                <p><?php esc_html_e( 'Kéo thả file Excel (.xlsx, .xls, .csv) hoặc click để chọn', 'wp-acf-smart-importer' ); ?></p>
                                <input type="file" id="wpsai-bulk-excel-file" accept=".xlsx, .xls, .csv" style="display: none;">
                                <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-bulk-excel-browse-btn"><?php esc_html_e( 'Chọn File', 'wp-acf-smart-importer' ); ?></button>
                            </div>
                            <div class="wpsai-file-info" id="wpsai-bulk-excel-file-info" style="display:none; padding: 10px; background: #e7f5ea; border-radius: 3px; display: flex; align-items: center; justify-content: space-between;">
                                <div>
                                    <span class="dashicons dashicons-yes-alt success-icon" style="color: #46b450; margin-right: 5px;"></span>
                                    <span class="wpsai-filename" style="font-weight: bold;"></span>
                                </div>
                                <button type="button" class="wpsai-btn-remove" id="wpsai-bulk-excel-remove-file" style="border:none; background:none; cursor:pointer; font-size:18px; font-weight:bold;">&times;</button>
                            </div>
                        </div>

                        <!-- Khung 2: Dán Văn Bản Trực Tiếp -->
                        <div id="wpsai-bulk-source-paste-wrapper" style="display:none;">
                            <div class="wpsai-form-group" style="margin-bottom: 15px;">
                                <label><strong><?php esc_html_e( 'Kiểu dán văn bản:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <div style="margin-top: 5px; display: flex; gap: 20px;">
                                    <label style="cursor:pointer;"><input type="radio" name="wpsai_bulk_paste_type" value="tsv" checked> <?php esc_html_e( 'Dán dạng Bảng (Copy từ Excel/Sheets)', 'wp-acf-smart-importer' ); ?></label>
                                    <label style="cursor:pointer;"><input type="radio" name="wpsai_bulk_paste_type" value="separate"> <?php esc_html_e( 'Tách riêng 2 ô nhập liệu', 'wp-acf-smart-importer' ); ?></label>
                                </div>
                            </div>

                            <!-- Cách A: TSV Paste -->
                            <div id="wpsai-bulk-paste-tsv-group" style="margin-bottom: 15px;">
                                <p class="description" style="margin-bottom: 8px;">
                                    <?php esc_html_e( 'Mở Excel/Google Sheets, bôi đen 2 cột Tiêu đề và Nội dung, nhấn Ctrl+C rồi dán (Ctrl+V) vào ô dưới đây:', 'wp-acf-smart-importer' ); ?>
                                </p>
                                <textarea id="wpsai-bulk-paste-tsv-raw" rows="6" class="large-text code" style="width:100%;" placeholder="<?php esc_attr_e( "Tiêu đề bài viết\tNội dung bài viết\nBài viết mẫu 1\tNội dung bài viết 1\nBài viết mẫu 2\tNội dung bài viết 2", 'wp-acf-smart-importer' ); ?>"></textarea>
                            </div>

                            <!-- Cách B: Separate inputs -->
                            <div id="wpsai-bulk-paste-separate-group" style="margin-bottom: 15px; display:none;">
                                <div style="display: flex; gap: 15px; margin-bottom: 10px;">
                                    <div style="flex: 1;">
                                        <label for="wpsai-bulk-paste-titles"><strong><?php esc_html_e( 'Danh sách Tiêu đề (Không bắt buộc, mỗi dòng một bài):', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <textarea id="wpsai-bulk-paste-titles" rows="6" class="large-text" style="width:100%; margin-top:5px;" placeholder="<?php esc_attr_e( "Để trống nếu chỉ muốn cập nhật nội dung...\nHoặc nhập Tiêu đề 1\nTiêu đề 2", 'wp-acf-smart-importer' ); ?>"></textarea>
                                    </div>
                                    <div style="flex: 1;">
                                        <label for="wpsai-bulk-paste-contents"><strong><?php esc_html_e( 'Danh sách Nội dung (Phân cách bằng tag [split]):', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <textarea id="wpsai-bulk-paste-contents" rows="6" class="large-text" style="width:100%; margin-top:5px;" placeholder="<?php esc_attr_e( "Nội dung chi tiết 1\n[split]\nNội dung chi tiết 2\n[split]\nNội dung chi tiết 3", 'wp-acf-smart-importer' ); ?>"></textarea>
                                    </div>
                                </div>
                                <div class="wpsai-form-group">
                                    <label for="wpsai-bulk-paste-separator"><strong><?php esc_html_e( 'Ký tự phân cách nội dung:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <input type="text" id="wpsai-bulk-paste-separator" value="[split]" class="small-text" style="padding: 4px 8px; border-radius: 4px; border: 1px solid #ccc; margin-left: 5px;">
                                    <span class="description" style="margin-left: 10px;"><?php esc_html_e( '(Mặc định là [split]. Mỗi bài viết được phân tách bằng dòng chứa ký tự này)', 'wp-acf-smart-importer' ); ?></span>
                                </div>
                            </div>

                            <div style="margin-top: 15px; display: flex; gap: 10px;">
                                <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-bulk-paste-load-btn">
                                    <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Phân Tích & Nạp Dữ Liệu', 'wp-acf-smart-importer' ); ?>
                                </button>
                                <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-bulk-paste-clear-btn" style="display:none;">
                                    <?php esc_html_e( 'Xóa Dữ Liệu Đã Nạp', 'wp-acf-smart-importer' ); ?>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 3: Cấu hình ánh xạ cột -->
                    <div class="wpsai-card" id="wpsai-bulk-excel-mapping-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 3: Ánh Xạ Cột Excel Vào Các Trường Bài Viết', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Thiết lập cột nào trong Excel sẽ tương ứng với trường nào của bài viết WordPress.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-table-container">
                            <table class="wpsai-preview-table" id="wpsai-bulk-excel-mapping-table">
                                <thead>
                                    <tr>
                                        <th style="width: 40%;"><?php esc_html_e( 'Trường Bài Viết', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 60%;"><?php esc_html_e( 'Chọn Cột Excel Tương Ứng', 'wp-acf-smart-importer' ); ?></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><strong><?php esc_html_e( 'Tiêu Đề Bài Viết (Title)', 'wp-acf-smart-importer' ); ?></strong></td>
                                        <td>
                                            <select class="wpsai-bulk-excel-map-select" data-field="post_title" style="width: 100%; max-width: 300px;">
                                                <option value=""><?php esc_html_e( '-- Bỏ qua không cập nhật --', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><strong><?php esc_html_e( 'Nội Dung Chi Tiết (Content)', 'wp-acf-smart-importer' ); ?></strong></td>
                                        <td>
                                            <select class="wpsai-bulk-excel-map-select" data-field="post_content" style="width: 100%; max-width: 300px;">
                                                <option value=""><?php esc_html_e( '-- Bỏ qua không cập nhật --', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <strong><?php esc_html_e( 'Đường Dẫn Gốc (Original Link)', 'wp-acf-smart-importer' ); ?></strong>
                                            <span class="wpsai-badge" style="background:#475569; font-size: 10px; margin-left: 5px;">original_url</span>
                                        </td>
                                        <td>
                                            <select class="wpsai-bulk-excel-map-select" data-field="original_url" style="width: 100%; max-width: 300px;">
                                                <option value=""><?php esc_html_e( '-- Bỏ qua không cập nhật --', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><strong><?php esc_html_e( 'Ảnh Đại Diện (Featured Image URL)', 'wp-acf-smart-importer' ); ?></strong></td>
                                        <td>
                                            <select class="wpsai-bulk-excel-map-select" data-field="featured_image" style="width: 100%; max-width: 300px;">
                                                <option value=""><?php esc_html_e( '-- Bỏ qua không cập nhật --', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Bước 4: Thực thi cập nhật -->
                    <div class="wpsai-card" id="wpsai-bulk-excel-execute-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 4: Thực Thi Cập Nhật Hàng Loạt', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Hệ thống sẽ cập nhật tuần tự các bài viết đã chọn theo dòng trong file Excel (Bài viết #1 cập nhật dòng #1, Bài viết #2 cập nhật dòng #2...).', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-actions-row">
                            <button type="button" class="wpsai-btn wpsai-btn-primary wpsai-btn-large" id="wpsai-bulk-excel-start-btn">
                                <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Bắt Đầu Cập Nhật Bài Viết', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>

                    <!-- Tiến trình gán ảnh (Ẩn mặc định) -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-bulk-excel-progress-card" style="display:none;">
                        <h2><?php esc_html_e( 'Tiến Trình Thực Thi', 'wp-acf-smart-importer' ); ?></h2>
                        <div class="wpsai-progress-bar-wrapper">
                            <div class="wpsai-progress-bar" id="wpsai-bulk-excel-progress-bar" style="width: 0%;">0%</div>
                        </div>
                        <div class="wpsai-progress-stats" id="wpsai-bulk-excel-progress-stats">
                            <p><?php esc_html_e( 'Đang chuẩn bị dữ liệu...', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        <div class="wpsai-import-log" id="wpsai-bulk-excel-log">
                            <!-- Nhật ký log tiến trình -->
                        </div>
                    </div>
                </section>

                <!-- Tab: Gán Phân Loại Hàng Loạt -->
                <section id="wpsai-tab-bulk-taxonomy" class="wpsai-tab-content">
                    <!-- Bước 1: Chọn Post Type và bài viết -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Chọn Post Type & Các Bài Viết Nhận Phân Loại', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn Post Type để lấy danh sách bài viết, sau đó chọn các bài viết cụ thể bạn muốn gán chuyên mục/thẻ.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-flex-row" style="gap: 20px; margin-bottom: 15px; align-items: center; flex-wrap: wrap;">
                            <div class="wpsai-form-group select-post-type-row">
                                <label for="wpsai-bulk-taxonomy-post-type"><strong><?php esc_html_e( '1. Chọn Post Type:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-bulk-taxonomy-post-type" class="large-text" style="width: auto; min-width: 220px; margin-top: 4px;">
                                    <!-- Post Types load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group select-taxonomy-row">
                                <label for="wpsai-bulk-taxonomy-select"><strong><?php esc_html_e( '2. Chọn Taxonomy (Chuyên Mục / Thẻ):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-bulk-taxonomy-select" class="large-text" style="width: auto; min-width: 220px; margin-top: 4px;">
                                    <option value=""><?php esc_html_e( '-- Đang tải Taxonomy --', 'wp-acf-smart-importer' ); ?></option>
                                </select>
                            </div>
                        </div>

                        <!-- Bộ lọc và Bảng danh sách bài viết -->
                        <div class="wpsai-posts-selector-wrapper" id="wpsai-bulk-taxonomy-posts-wrapper" style="display:none; margin-top: 20px;">
                            <div class="wpsai-flex-row" style="margin-bottom: 10px; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <label class="wpsai-checkbox-label">
                                        <input type="checkbox" id="wpsai-bulk-taxonomy-select-all" value="1">
                                        <strong><?php esc_html_e( 'Chọn tất cả', 'wp-acf-smart-importer' ); ?></strong>
                                    </label>
                                    <span id="wpsai-bulk-taxonomy-selected-count" style="color: var(--wpsai-primary); font-weight: 600;">Đã chọn: 0/0 bài viết</span>
                                </div>
                                <div>
                                    <input type="text" id="wpsai-bulk-taxonomy-search" placeholder="<?php esc_attr_e( 'Tìm kiếm bài viết...', 'wp-acf-smart-importer' ); ?>" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); width: 250px;">
                                </div>
                            </div>

                            <div class="wpsai-table-container" style="max-height: 250px;">
                                <table class="wpsai-preview-table" id="wpsai-bulk-taxonomy-posts-table">
                                    <thead>
                                        <tr>
                                            <th style="width: 50px; text-align: center;"></th>
                                            <th style="width: 80px;"><?php esc_html_e( 'ID', 'wp-acf-smart-importer' ); ?></th>
                                            <th><?php esc_html_e( 'Tiêu Đề Bài Viết', 'wp-acf-smart-importer' ); ?></th>
                                            <th><?php esc_html_e( 'Phân Loại Hiện Tại', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 150px;"><?php esc_html_e( 'Ngày Tạo', 'wp-acf-smart-importer' ); ?></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Render động -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2: Chọn / Nhập Term gán -->
                    <div class="wpsai-card" id="wpsai-bulk-taxonomy-config-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 2: Chọn / Nhập Danh Mục Hoặc Thẻ Cần Gán', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Tích chọn các term sẵn có trong CSDL hoặc nhập đường dẫn phân cấp tùy ý (Ví dụ: Bất động sản > Villa).', 'wp-acf-smart-importer' ); ?></p>

                        <div class="wpsai-taxonomy-input-modes" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                            <!-- Cách A: Lựa chọn từ term hiện có -->
                            <div style="border-right: 1px solid #eee; padding-right: 20px;">
                                <h3><span class="dashicons dashicons-list-view"></span> <?php esc_html_e( 'Lựa chọn từ các Term hiện có:', 'wp-acf-smart-importer' ); ?></h3>
                                <div id="wpsai-bulk-taxonomy-existing-terms" style="max-height: 200px; overflow-y: auto; background: #f8fafc; border: 1px solid var(--wpsai-border-color); padding: 15px; border-radius: 8px; margin-top: 10px;">
                                    <p style="color: var(--wpsai-text-muted); font-style: italic;"><?php esc_html_e( 'Vui lòng chọn Taxonomy trước để tải danh sách.', 'wp-acf-smart-importer' ); ?></p>
                                </div>
                            </div>

                            <!-- Cách B: Nhập đường dẫn tùy ý -->
                            <div>
                                <h3><span class="dashicons dashicons-edit"></span> <?php esc_html_e( 'Hoặc nhập đường dẫn phân cấp / tự tạo mới:', 'wp-acf-smart-importer' ); ?></h3>
                                <div style="margin-top: 10px;">
                                    <input type="text" id="wpsai-bulk-taxonomy-custom-path" class="large-text" placeholder="<?php esc_attr_e( 'Ví dụ: Bất động sản > Chung cư, Tin tức > Dự án', 'wp-acf-smart-importer' ); ?>" style="width: 100%;">
                                    <p class="description" style="margin-top: 5px;"><?php esc_html_e( 'Hệ thống hỗ trợ dấu > để phân tách cấp cha con và dấu phẩy để gán nhiều danh mục cùng lúc. Sẽ tự động tạo nếu chưa có trong DB.', 'wp-acf-smart-importer' ); ?></p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 3: Thiết lập chế độ gán -->
                    <div class="wpsai-card" id="wpsai-bulk-taxonomy-mode-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 3: Chọn Chế Độ Gán Phân Loại', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn hành vi khi lưu: Gán thêm vào danh sách sẵn có hay ghi đè/xóa hết các term cũ.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-form-group">
                            <label class="wpsai-radio-label">
                                <input type="radio" name="wpsai_bulk_taxonomy_mode" value="append" checked>
                                <strong><?php esc_html_e( 'Gán thêm (Append)', 'wp-acf-smart-importer' ); ?></strong>
                                <span class="wpsai-radio-desc"><?php esc_html_e( 'Giữ nguyên các chuyên mục/thẻ cũ của bài viết, chỉ bổ sung thêm các phân loại mới được chọn ở Bước 2.', 'wp-acf-smart-importer' ); ?></span>
                            </label>
                            <br/>
                            <label class="wpsai-radio-label" style="margin-top: 10px; display:inline-block;">
                                <input type="radio" name="wpsai_bulk_taxonomy_mode" value="replace">
                                <strong><?php esc_html_e( 'Gán đè (Replace)', 'wp-acf-smart-importer' ); ?></strong>
                                <span class="wpsai-radio-desc"><?php esc_html_e( 'Xóa bỏ toàn bộ chuyên mục/thẻ cũ của bài viết đó và thay thế hoàn toàn bằng phân loại mới được thiết lập.', 'wp-acf-smart-importer' ); ?></span>
                            </label>
                        </div>
                    </div>

                    <!-- Bước 4: Thực thi -->
                    <div class="wpsai-card" id="wpsai-bulk-taxonomy-execute-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 4: Thực Thi Cập Nhật', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Bắt đầu cập nhật hàng loạt phân loại cho các bài viết đã chọn.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-actions-row">
                            <button type="button" class="wpsai-btn wpsai-btn-primary wpsai-btn-large" id="wpsai-bulk-taxonomy-start-btn">
                                <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Bắt Đầu Gán Phân Loại', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>

                    <!-- Tiến trình thực thi -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-bulk-taxonomy-progress-card" style="display:none;">
                        <h2><?php esc_html_e( 'Tiến Trình Thực Thi', 'wp-acf-smart-importer' ); ?></h2>
                        <div class="wpsai-progress-bar-wrapper">
                            <div class="wpsai-progress-bar" id="wpsai-bulk-taxonomy-progress-bar" style="width: 0%;">0%</div>
                        </div>
                        <div class="wpsai-progress-stats" id="wpsai-bulk-taxonomy-progress-stats">
                            <p><?php esc_html_e( 'Đang chuẩn bị dữ liệu...', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        <div class="wpsai-import-log" id="wpsai-bulk-taxonomy-log">
                            <!-- Nhật ký log tiến trình -->
                        </div>
                    </div>
                </section>

                </section>

                <!-- Tab: Xuất Dữ Liệu -->
                <section id="wpsai-tab-export" class="wpsai-tab-content">
                    <!-- Bước 1: Chọn Post Type và Bài viết -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Chọn Post Type & Các Bài Viết Cần Xuất', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn Post Type để hiển thị danh sách bài viết, sau đó chọn những bài viết bạn muốn xuất dữ liệu và hình ảnh.', 'wp-acf-smart-importer' ); ?></p>

                        <div class="wpsai-form-group select-post-type-row" style="margin-bottom: 15px;">
                            <label for="wpsai-export-post-type"><strong><?php esc_html_e( 'Chọn Post Type:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <select id="wpsai-export-post-type" class="large-text" style="width: auto; min-width: 250px;">
                                <!-- Post Types load qua AJAX -->
                            </select>
                        </div>

                        <!-- Danh sách bài viết -->
                        <div class="wpsai-posts-selector-wrapper" id="wpsai-export-posts-wrapper" style="display:none; margin-top: 20px;">
                            <div class="wpsai-flex-row" style="margin-bottom: 10px; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <label class="wpsai-checkbox-label">
                                        <input type="checkbox" id="wpsai-export-select-all" value="1">
                                        <strong><?php esc_html_e( 'Chọn tất cả', 'wp-acf-smart-importer' ); ?></strong>
                                    </label>
                                    <span id="wpsai-export-selected-count" style="color: var(--wpsai-primary); font-weight: 600;">Đã chọn: 0/0 bài viết</span>
                                </div>
                                <div>
                                    <input type="text" id="wpsai-export-search" placeholder="<?php esc_attr_e( 'Tìm kiếm bài viết...', 'wp-acf-smart-importer' ); ?>" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); width: 250px;">
                                </div>
                            </div>

                            <div class="wpsai-table-container" style="max-height: 250px;">
                                <table class="wpsai-preview-table" id="wpsai-export-posts-table">
                                    <thead>
                                        <tr>
                                            <th style="width: 50px; text-align: center;"></th>
                                            <th style="width: 80px;"><?php esc_html_e( 'ID', 'wp-acf-smart-importer' ); ?></th>
                                            <th><?php esc_html_e( 'Tiêu Đề Bài Viết', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 150px;"><?php esc_html_e( 'Ngày Tạo', 'wp-acf-smart-importer' ); ?></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Render động -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2: Chọn các trường cần xuất -->
                    <div class="wpsai-card" id="wpsai-export-fields-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 2: Chọn Các Trường Dữ Liệu Cần Xuất', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Tích chọn các trường bạn muốn xuất vào file Excel.', 'wp-acf-smart-importer' ); ?></p>

                        <!-- Các trường WordPress Mặc Định -->
                        <div style="margin-bottom: 20px;">
                            <h3 style="font-size:14px; margin-bottom: 10px; color:#475569;"><span class="dashicons dashicons-wordpress" style="vertical-align: text-bottom; margin-right: 5px;"></span><?php esc_html_e( 'Trường cốt lõi WordPress:', 'wp-acf-smart-importer' ); ?></h3>
                            <div class="wpsai-flex-row" style="gap: 15px; flex-wrap: wrap; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid var(--wpsai-border-color);">
                                <label class="wpsai-checkbox-label" style="min-width: 150px;">
                                    <input type="checkbox" name="wpsai_export_fields[]" value="post_id" checked>
                                    <span>ID bài viết</span>
                                </label>
                                <label class="wpsai-checkbox-label" style="min-width: 150px;">
                                    <input type="checkbox" name="wpsai_export_fields[]" value="post_title" checked>
                                    <span>Tiêu đề bài viết</span>
                                </label>
                                <label class="wpsai-checkbox-label" style="min-width: 150px;">
                                    <input type="checkbox" name="wpsai_export_fields[]" value="post_name" checked>
                                    <span>Đường dẫn (Slug)</span>
                                </label>
                                <label class="wpsai-checkbox-label" style="min-width: 150px;">
                                    <input type="checkbox" name="wpsai_export_fields[]" value="post_content" checked>
                                    <span>Nội dung chi tiết</span>
                                </label>
                                <label class="wpsai-checkbox-label" style="min-width: 150px;">
                                    <input type="checkbox" name="wpsai_export_fields[]" value="post_excerpt" checked>
                                    <span>Mô tả ngắn (Excerpt)</span>
                                </label>
                                <label class="wpsai-checkbox-label" style="min-width: 150px;">
                                    <input type="checkbox" name="wpsai_export_fields[]" value="post_date" checked>
                                    <span>Ngày tạo</span>
                                </label>
                                <label class="wpsai-checkbox-label" style="min-width: 150px;" title="<?php esc_attr_e( 'Nếu có ảnh, tệp ảnh sẽ được nén vào thư mục images/ trong file zip', 'wp-acf-smart-importer' ); ?>">
                                    <input type="checkbox" name="wpsai_export_fields[]" value="featured_image" checked>
                                    <span style="border-bottom: 1px dashed #64748b;"><?php esc_html_e( 'Ảnh đại diện', 'wp-acf-smart-importer' ); ?></span>
                                </label>
                            </div>
                        </div>

                        <!-- Các trường ACF (nếu có) -->
                        <div id="wpsai-export-acf-fields-section" style="display:none; margin-bottom: 10px;">
                            <h3 style="font-size:14px; margin-bottom: 10px; color:#475569;"><span class="dashicons dashicons-admin-generic" style="vertical-align: text-bottom; margin-right: 5px;"></span><?php esc_html_e( 'Trường tùy chỉnh ACF:', 'wp-acf-smart-importer' ); ?></h3>
                            <div class="wpsai-flex-row" id="wpsai-export-acf-fields-list" style="gap: 15px; flex-wrap: wrap; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid var(--wpsai-border-color);">
                                <!-- Chèn động các checkbox ACF -->
                            </div>
                        </div>
                    </div>

                    <!-- Bước 3: Thực thi xuất -->
                    <div class="wpsai-card" id="wpsai-export-execute-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 3: Thực Thi Xuất Dữ Liệu', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Nhấn nút bên dưới để đóng gói file Excel và ZIP các ảnh đính kèm của bài viết.', 'wp-acf-smart-importer' ); ?></p>

                        <div class="wpsai-actions-row">
                            <button type="button" class="wpsai-btn wpsai-btn-primary wpsai-btn-large" id="wpsai-export-start-btn">
                                <span class="dashicons dashicons-database-export"></span> <?php esc_html_e( 'Bắt Đầu Xuất File ZIP', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>

                    <!-- Tiến trình thực thi -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-export-progress-card" style="display:none;">
                        <h2><?php esc_html_e( 'Tiến Trình Thực Thi Xuất Dữ Liệu', 'wp-acf-smart-importer' ); ?></h2>
                        <div class="wpsai-progress-bar-wrapper">
                            <div class="wpsai-progress-bar" id="wpsai-export-progress-bar" style="width: 0%;">0%</div>
                        </div>
                        <div class="wpsai-progress-stats" id="wpsai-export-progress-stats">
                            <p><?php esc_html_e( 'Đang chuẩn bị kết nối...', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        
                        <!-- Đường dẫn tải file ZIP kết quả -->
                        <div id="wpsai-export-download-area" style="display:none; margin: 20px 0; padding: 20px; background: #ecfdf5; border: 2px dashed var(--wpsai-success); border-radius: var(--wpsai-radius); text-align: center;">
                            <span class="dashicons dashicons-yes-alt success-icon" style="font-size: 40px; width:40px; height:40px; margin-bottom: 10px;"></span>
                            <h3 style="color:#065f46; margin: 0 0 10px 0; font-weight:600;"><?php esc_html_e( 'Xuất Dữ Liệu Thành Công!', 'wp-acf-smart-importer' ); ?></h3>
                            <p style="color:#047857; margin-bottom: 15px;"><?php esc_html_e( 'Tệp ZIP của bạn đã được tạo hoàn tất trên máy chủ, bao gồm file Excel và thư mục ảnh đính kèm.', 'wp-acf-smart-importer' ); ?></p>
                            <a href="#" id="wpsai-export-download-link" class="wpsai-btn wpsai-btn-success wpsai-btn-large" style="text-decoration:none;" target="_blank">
                                <span class="dashicons dashicons-download"></span> <?php esc_html_e( 'Tải Xuống File ZIP Kết Quả', 'wp-acf-smart-importer' ); ?>
                            </a>
                        </div>

                        <div class="wpsai-import-log" id="wpsai-export-log">
                            <!-- Log chi tiết -->
                        </div>
                    </div>
                </section>

                </section>

                <!-- Tab: Nhân Bản Hàng Loạt -->
                <section id="wpsai-tab-duplicate" class="wpsai-tab-content">
                    <!-- Bước 1: Chọn bài viết chuẩn hoặc Sinh trực tiếp -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Chọn Nguồn Tham Chiếu', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn phương thức sinh dữ liệu: sinh trực tiếp (không cần bài mẫu, dùng khi web mới có 0 bài viết) hoặc nhân bản từ một bài viết mẫu.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-form-group" style="margin-bottom: 20px;">
                            <label><strong><?php esc_html_e( 'Nguồn dữ liệu tham chiếu:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <div class="wpsai-flex-row" style="gap: 20px; margin-top: 10px;">
                                <label class="wpsai-radio-label">
                                    <input type="radio" name="wpsai_duplicate_source_type" value="direct" checked>
                                    <strong><?php esc_html_e( 'Sinh trực tiếp (Không cần bài mẫu)', 'wp-acf-smart-importer' ); ?></strong>
                                </label>
                                <label class="wpsai-radio-label">
                                    <input type="radio" name="wpsai_duplicate_source_type" value="reference">
                                    <strong><?php esc_html_e( 'Nhân bản từ bài viết mẫu có sẵn', 'wp-acf-smart-importer' ); ?></strong>
                                </label>
                            </div>
                        </div>

                        <div class="wpsai-flex-row select-post-row" style="align-items: flex-end; border-top: 1px solid #eee; padding-top: 15px;">
                            <div class="wpsai-form-group">
                                <label for="wpsai-duplicate-post-type"><strong><?php esc_html_e( 'Chọn Post Type:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-duplicate-post-type" class="large-text" style="min-width: 250px;">
                                    <!-- Post Types load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group" id="wpsai-duplicate-ref-post-group" style="display: none;">
                                <label for="wpsai-duplicate-ref-post"><strong><?php esc_html_e( 'Chọn Bài Viết Gốc:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-duplicate-ref-post" class="large-text" style="min-width: 250px;">
                                    <option value=""><?php esc_html_e( '-- Chọn bài viết --', 'wp-acf-smart-importer' ); ?></option>
                                    <!-- Posts load qua AJAX -->
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2: Cấu hình nhân bản -->
                    <div class="wpsai-card" id="wpsai-duplicate-config-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 2: Cài Đặt Nhân Bản Hàng Loạt', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Thiết lập số lượng bản sao cần tạo, trạng thái bài viết và thuật toán sinh nội dung.', 'wp-acf-smart-importer' ); ?></p>

                        <div class="wpsai-flex-row" style="margin-bottom: 20px;">
                            <div class="wpsai-form-group">
                                <label for="wpsai-duplicate-count"><strong><?php esc_html_e( 'Số lượng bài viết cần sinh (2 - 10 bài):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="number" id="wpsai-duplicate-count" value="5" min="2" max="10" class="small-text" style="padding: 10px 14px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); width: 100px;">
                            </div>
                            <div class="wpsai-form-group">
                                <label for="wpsai-duplicate-status"><strong><?php esc_html_e( 'Trạng thái bài viết được tạo:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-duplicate-status" class="large-text" style="width: auto; min-width: 200px;">
                                    <option value="draft" selected><?php esc_html_e( 'Bản nháp (Draft)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="pending"><?php esc_html_e( 'Chờ duyệt (Pending)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="publish"><?php esc_html_e( 'Đã đăng (Publish)', 'wp-acf-smart-importer' ); ?></option>
                                </select>
                            </div>
                        </div>

                        <div class="wpsai-form-group">
                            <label><strong><?php esc_html_e( 'Chọn phương thức tạo nội dung:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <div class="wpsai-generator-modes" style="margin-top: 10px;">
                                <!-- Chế độ Rule-based -->
                                <label class="wpsai-radio-card active" style="flex: 1;">
                                    <input type="radio" name="wpsai_duplicate_mode" value="rule" checked>
                                    <div class="wpsai-radio-card-content">
                                        <h4><?php esc_html_e( 'Theo Quy Tắc (Rule-based)', 'wp-acf-smart-importer' ); ?></h4>
                                        <p><?php esc_html_e( 'Sao chép y nguyên cấu trúc, trường ACF và Custom Meta. Tiêu đề sẽ được gắn hậu tố để phân biệt (Ví dụ: "Tên bài viết (Bản sao #1)"). Hoạt động không cần API Key.', 'wp-acf-smart-importer' ); ?></p>
                                    </div>
                                </label>

                                <!-- Chế độ Gemini AI -->
                                <label class="wpsai-radio-card" style="flex: 1;">
                                    <input type="radio" name="wpsai_duplicate_mode" value="ai">
                                    <div class="wpsai-radio-card-content">
                                        <h4><?php esc_html_e( 'Tự Động Viết Lại Bằng Gemini AI', 'wp-acf-smart-importer' ); ?></h4>
                                        <p><?php esc_html_e( 'Sử dụng AI phân tích bài viết gốc. Sau đó tự động viết lại Tiêu đề, Nội dung chi tiết, Mô tả ngắn và các trường ACF dạng chữ một cách tự nhiên, độc nhất, cùng chủ đề nhưng không trùng lặp câu từ. (Yêu cầu API Key)', 'wp-acf-smart-importer' ); ?></p>
                                    </div>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 3: Thực thi -->
                    <div class="wpsai-card" id="wpsai-duplicate-execute-card" style="display:none;">
                        <h2><?php esc_html_e( 'Bước 3: Thực Thi Nhân Bản', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Nhấp nút để bắt đầu quá trình sinh dữ liệu ảo và tự động tạo các bài viết mới trên database.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-actions-row">
                            <button type="button" class="wpsai-btn wpsai-btn-primary wpsai-btn-large" id="wpsai-duplicate-start-btn">
                                <span class="dashicons dashicons-admin-page"></span> <?php esc_html_e( 'Bắt Đầu Nhân Bản Hàng Loạt', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>

                    <!-- Tiến trình thực thi -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-duplicate-progress-card" style="display:none;">
                        <h2><?php esc_html_e( 'Tiến Trình Nhân Bản', 'wp-acf-smart-importer' ); ?></h2>
                        <div class="wpsai-progress-bar-wrapper">
                            <div class="wpsai-progress-bar" id="wpsai-duplicate-progress-bar" style="width: 0%;">0%</div>
                        </div>
                        <div class="wpsai-progress-stats" id="wpsai-duplicate-progress-stats">
                            <p><?php esc_html_e( 'Đang kết nối...', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        <div class="wpsai-import-log" id="wpsai-duplicate-log">
                            <!-- Log chi tiết -->
                        </div>
                    </div>
                </section>

                <!-- Tab: Cào Bài Viết -->
                <section id="wpsai-tab-scraper" class="wpsai-tab-content">
                    <!-- Bước 1: Nhập URL nguồn -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Nhập URL Trang Web Cần Cào', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Nhập URL chi tiết của bài viết bạn muốn cào từ bất kỳ trang web nào (ví dụ: tin tức, blog).', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-form-group" style="margin-top: 15px;">
                            <label for="wpsai-scraper-url"><strong><?php esc_html_e( 'Đường dẫn URL bài viết:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <input type="url" id="wpsai-scraper-url" class="large-text" placeholder="https://example.com/bai-viet-mau" style="width: 100%; max-width: 600px; display: block; margin-top: 5px;">
                        </div>
                    </div>

                    <!-- Bước 2: Cấu hình bộ chọn selectors -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 2: Cấu Hình Bộ Chọn (Selectors) CSS / XPath', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Điền bộ chọn CSS (ví dụ: .title, #content, h1) hoặc XPath (bắt đầu bằng / hoặc () để bóc tách các trường dữ liệu.', 'wp-acf-smart-importer' ); ?></p>

                        <div class="wpsai-flex-row" style="margin-top: 15px; flex-wrap: wrap; gap: 15px;">
                            <div class="wpsai-form-group" style="flex: 1; min-width: 200px;">
                                <label for="wpsai-scraper-selector-title"><strong><?php esc_html_e( 'Bộ chọn Tiêu đề (Title):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="text" id="wpsai-scraper-selector-title" class="large-text" value="h1" placeholder="Ví dụ: h1, .title, //h1" style="width: 100%;">
                            </div>
                            <div class="wpsai-form-group" style="flex: 1; min-width: 200px;">
                                <label for="wpsai-scraper-selector-content"><strong><?php esc_html_e( 'Bộ chọn Nội dung (Content):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="text" id="wpsai-scraper-selector-content" class="large-text" value=".entry-content" placeholder="Ví dụ: .entry-content, #content, //div[@class='content']" style="width: 100%;">
                            </div>
                        </div>

                        <div class="wpsai-flex-row" style="margin-top: 15px; flex-wrap: wrap; gap: 15px;">
                            <div class="wpsai-form-group" style="flex: 1; min-width: 200px;">
                                <label for="wpsai-scraper-selector-image"><strong><?php esc_html_e( 'Bộ chọn Ảnh đại diện (Featured Image):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="text" id="wpsai-scraper-selector-image" class="large-text" value="meta[property='og:image']" placeholder="Ví dụ: .post-thumbnail img, meta[property='og:image']" style="width: 100%;">
                            </div>
                            <div class="wpsai-form-group" style="flex: 1; min-width: 200px;">
                                <label for="wpsai-scraper-selector-remove"><strong><?php esc_html_e( 'Bộ chọn phần tử muốn loại bỏ (nếu có):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="text" id="wpsai-scraper-selector-remove" class="large-text" value="" placeholder="Ví dụ: .ads-wrapper, .related-posts, script" style="width: 100%;">
                            </div>
                        </div>

                        <div class="wpsai-actions-row" style="margin-top: 20px;">
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-scraper-preview-btn">
                                <span class="dashicons dashicons-search"></span> <?php esc_html_e( 'Xem Trước Nội Dung Cào Được', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>

                        <!-- Khung Preview kết quả cào -->
                        <div id="wpsai-scraper-preview-box" class="wpsai-preview-box" style="display: none; margin-top: 20px; padding: 20px; border: 1px solid var(--wpsai-border-color); border-radius: var(--wpsai-radius); background: #f8fafc;">
                            <h3 style="margin-top: 0; color: var(--wpsai-text); border-bottom: 2px solid var(--wpsai-primary); padding-bottom: 8px;"><?php esc_html_e( 'Kết quả xem trước', 'wp-acf-smart-importer' ); ?></h3>
                            
                            <div class="wpsai-form-group" style="margin-top: 15px;">
                                <label><strong><?php esc_html_e( 'Tiêu đề cào được:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <div id="wpsai-scraper-preview-title" style="padding: 10px; background: #fff; border: 1px solid var(--wpsai-border-color); border-radius: var(--wpsai-radius); font-size: 16px; font-weight: bold; margin-top: 5px;"></div>
                            </div>

                            <div class="wpsai-form-group" style="margin-top: 15px;">
                                <label><strong><?php esc_html_e( 'Ảnh đại diện cào được:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <div id="wpsai-scraper-preview-image-container" style="margin-top: 5px;">
                                    <img id="wpsai-scraper-preview-image" src="" style="max-width: 250px; height: auto; border: 1px solid var(--wpsai-border-color); border-radius: var(--wpsai-radius); display: block;" alt="<?php esc_attr_e( 'Không tìm thấy ảnh', 'wp-acf-smart-importer' ); ?>">
                                    <span id="wpsai-scraper-preview-image-url" style="display: block; font-size: 11px; color: #64748b; margin-top: 5px; word-break: break-all;"></span>
                                </div>
                            </div>

                            <div class="wpsai-form-group" style="margin-top: 15px;">
                                <label><strong><?php esc_html_e( 'Nội dung HTML cào được:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <div id="wpsai-scraper-preview-content" class="wpsai-content-preview-div" style="padding: 15px; background: #fff; border: 1px solid var(--wpsai-border-color); border-radius: var(--wpsai-radius); max-height: 300px; overflow-y: auto; margin-top: 5px; line-height: 1.6;"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 3: Cài đặt lưu bài viết -->
                    <div class="wpsai-card" id="wpsai-scraper-settings-card" style="display: none;">
                        <h2><?php esc_html_e( 'Bước 3: Thiết Lập Lưu Trạng Thế & Phân Loại', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn Post Type đích, trạng thái bài viết và gán chuyên mục/thẻ tự động.', 'wp-acf-smart-importer' ); ?></p>

                        <div class="wpsai-flex-row" style="margin-top: 15px; flex-wrap: wrap; gap: 15px;">
                            <div class="wpsai-form-group" style="flex: 1; min-width: 200px;">
                                <label for="wpsai-scraper-post-type"><strong><?php esc_html_e( 'Chọn Post Type đích:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-scraper-post-type" class="large-text" style="width: 100%;">
                                    <!-- Post types load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group" style="flex: 1; min-width: 200px;">
                                <label for="wpsai-scraper-post-status"><strong><?php esc_html_e( 'Trạng thái bài viết:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-scraper-post-status" class="large-text" style="width: 100%;">
                                    <option value="draft" selected><?php esc_html_e( 'Bản nháp (Draft)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="pending"><?php esc_html_e( 'Chờ duyệt (Pending)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="publish"><?php esc_html_e( 'Đã đăng (Publish)', 'wp-acf-smart-importer' ); ?></option>
                                </select>
                            </div>
                        </div>

                        <!-- Gán chuyên mục/thẻ -->
                        <div class="wpsai-flex-row" style="margin-top: 15px; flex-wrap: wrap; gap: 15px;">
                            <div class="wpsai-form-group" style="flex: 1; min-width: 200px;">
                                <label for="wpsai-scraper-taxonomy"><strong><?php esc_html_e( 'Chọn Taxonomy để gán:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-scraper-taxonomy" class="large-text" style="width: 100%;">
                                    <option value=""><?php esc_html_e( '-- Chọn Taxonomy --', 'wp-acf-smart-importer' ); ?></option>
                                    <!-- Load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group" style="flex: 1; min-width: 200px;">
                                <label for="wpsai-scraper-terms"><strong><?php esc_html_e( 'Giá trị phân loại cần gán:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="text" id="wpsai-scraper-terms" class="large-text" placeholder="Ví dụ: Tin tức > Thế giới, Technology" style="width: 100%;">
                                <p class="description" style="margin-top: 5px;"><?php esc_html_e( 'Hỗ trợ dấu > để phân cấp (ví dụ: Chuyên mục cha > Chuyên mục con). Phân tách nhiều term bằng dấu phẩy.', 'wp-acf-smart-importer' ); ?></p>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 4: Thực thi cào & nhập -->
                    <div class="wpsai-card" id="wpsai-scraper-execute-card" style="display: none;">
                        <h2><?php esc_html_e( 'Bước 4: Thực Thi Cào & Đăng Bài Viết', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Nhấp nút dưới đây để tải nội dung trang web chính thức, tải ảnh đại diện và tạo bài viết mới.', 'wp-acf-smart-importer' ); ?></p>

                        <div class="wpsai-actions-row" style="margin-top: 15px;">
                            <button type="button" class="wpsai-btn wpsai-btn-primary wpsai-btn-large" id="wpsai-scraper-execute-btn">
                                <span class="dashicons dashicons-download"></span> <?php esc_html_e( 'Cào & Đăng Bài Viết Ngay', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>

                    <!-- Tiến trình & log thực thi -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-scraper-progress-card" style="display: none;">
                        <h2><?php esc_html_e( 'Tiến Trình Cào & Nhập Liệu', 'wp-acf-smart-importer' ); ?></h2>
                        <div class="wpsai-progress-bar-wrapper">
                            <div class="wpsai-progress-bar" id="wpsai-scraper-progress-bar" style="width: 0%;">0%</div>
                        </div>
                        <div class="wpsai-progress-stats" id="wpsai-scraper-progress-stats">
                            <p><?php esc_html_e( 'Đang kết nối...', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        
                        <!-- Đường dẫn bài viết kết quả -->
                        <div id="wpsai-scraper-success-area" style="display:none; margin: 20px 0; padding: 20px; background: #ecfdf5; border: 2px dashed var(--wpsai-success); border-radius: var(--wpsai-radius); text-align: center;">
                            <span class="dashicons dashicons-yes-alt success-icon" style="font-size: 40px; width:40px; height:40px; margin-bottom: 10px;"></span>
                            <h3 style="color:#065f46; margin: 0 0 10px 0; font-weight:600;"><?php esc_html_e( 'Cào và Nhập Bài Viết Thành Công!', 'wp-acf-smart-importer' ); ?></h3>
                            <a href="#" id="wpsai-scraper-result-link" class="wpsai-btn wpsai-btn-success wpsai-btn-large" style="text-decoration:none;" target="_blank">
                                <span class="dashicons dashicons-welcome-view-site"></span> <?php esc_html_e( 'Xem Bài Viết Vừa Đăng', 'wp-acf-smart-importer' ); ?>
                            </a>
                        </div>

                        <div class="wpsai-import-log" id="wpsai-scraper-log">
                            <!-- Log chi tiết -->
                        </div>
                    </div>
                </section>

                <!-- Tab: Cào HTML Offline -->
                <section id="wpsai-tab-offline-scraper" class="wpsai-tab-content">
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Nạp File HTML & Đoạn HTML Mẫu', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Nạp file HTML (lưu từ SingleFile) và dán đoạn HTML đại diện của 1 khối sản phẩm để hệ thống tự động bóc tách.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-flex-row" style="margin-top: 15px; flex-wrap: wrap; gap: 20px; align-items: flex-start;">
                            <!-- File HTML Upload Zone -->
                            <div class="wpsai-form-group" style="flex: 1; min-width: 300px;">
                                <label><strong><?php esc_html_e( 'Chọn hoặc kéo thả file HTML từ SingleFile:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <div class="wpsai-drag-drop-zone" id="wpsai-offline-drop-zone" style="border: 2px dashed #ccc; padding: 25px; text-align: center; border-radius: 6px; background: #fafafa; cursor: pointer; transition: all 0.3s;">
                                    <span class="dashicons dashicons-media-code" style="font-size: 40px; width: 40px; height: 40px; margin-bottom: 10px; color: #888;"></span>
                                    <p><?php esc_html_e( 'Kéo thả file HTML hoặc click để chọn', 'wp-acf-smart-importer' ); ?></p>
                                    <input type="file" id="wpsai-offline-file-input" accept=".html,.htm" style="display: none;">
                                    <div id="wpsai-offline-file-badge" style="display:none; padding: 10px; background: #e7f5ea; border-radius: 4px; color: #46b450; font-weight: bold; margin-top: 10px;"></div>
                                </div>
                            </div>
                            
                            <!-- Product snippet html block -->
                            <div class="wpsai-form-group" style="flex: 1; min-width: 300px;">
                                <label for="wpsai-offline-snippet"><strong><?php esc_html_e( 'Dán đoạn mã HTML của 1 khối sản phẩm mẫu (Tùy chọn):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <textarea id="wpsai-offline-snippet" rows="5" class="large-text code" placeholder="<?php esc_attr_e( 'Dán một khối HTML sản phẩm mẫu tại đây để tự động gợi ý các class...', 'wp-acf-smart-importer' ); ?>" style="width: 100%; font-family: monospace; font-size: 11px;"></textarea>
                                
                                <div id="wpsai-offline-suggestions-wrapper" style="display: none; margin-top: 10px;">
                                    <span style="font-size: 11px; font-weight: bold; display: block; margin-bottom: 5px; color: #666;"><?php esc_html_e( 'Các class & thẻ phát hiện được (Click để điền nhanh):', 'wp-acf-smart-importer' ); ?></span>
                                    <div id="wpsai-offline-suggestions" style="display: flex; flex-wrap: wrap; gap: 6px; padding: 8px; background: #f0f0f0; border-radius: 4px;"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 2: Cấu Hình Bộ Lọc Dữ Liệu', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Điền bộ chọn khung bọc ngoài cùng (Item Wrapper CSS Selector) và ánh xạ các trường dữ liệu tương ứng.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-form-group" style="margin-top: 15px;">
                            <label for="wpsai-offline-item-selector"><strong><?php esc_html_e( 'Khung bọc ngoài cùng (Item Wrapper CSS Selector):', 'wp-acf-smart-importer' ); ?></strong></label>
                            <input type="text" id="wpsai-offline-item-selector" class="large-text" value=".project-item" placeholder="Ví dụ: .product-item, .post-card" style="width: 100%; max-width: 400px; display: block; margin-top: 5px;">
                        </div>

                        <div class="wpsai-form-group" style="margin-top: 15px;">
                            <label><strong><?php esc_html_e( 'Ánh xạ các trường cột Excel (Field Mappings):', 'wp-acf-smart-importer' ); ?></strong></label>
                            <table class="wpsai-preview-table" id="wpsai-offline-mapping-table" style="margin-top: 10px;">
                                <thead>
                                    <tr>
                                        <th style="width: 35%;"><?php esc_html_e( 'Tên Trường (Cột Excel / Meta Key)', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 40%;"><?php esc_html_e( 'CSS Selector tương đối', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 20%;"><?php esc_html_e( 'Lấy thuộc tính', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 5%; text-align: center;"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr data-row-idx="0">
                                        <td><input type="text" class="field-name large-text" value="post_title" style="width:100%; padding:6px;"></td>
                                        <td><input type="text" class="field-selector large-text" value="h3, a.title" style="width:100%; padding:6px;"></td>
                                        <td>
                                            <select class="field-attr" style="width:100%; padding:5px;">
                                                <option value="text" selected><?php esc_html_e( 'Chữ (Text)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="html"><?php esc_html_e( 'Mã HTML', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="href"><?php esc_html_e( 'Link (href)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="src"><?php esc_html_e( 'Ảnh (src)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="alt"><?php esc_html_e( 'Tên ảnh / Thuộc tính alt (alt)', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </td>
                                        <td style="text-align:center;"><button type="button" class="wpsai-btn-remove wpsai-offline-delete-row" style="background:none; border:none; cursor:pointer; font-weight:bold; font-size:18px;">&times;</button></td>
                                    </tr>
                                    <tr data-row-idx="1">
                                        <td><input type="text" class="field-name large-text" value="post_content" style="width:100%; padding:6px;"></td>
                                        <td><input type="text" class="field-selector large-text" value=".entry-content, .desc" style="width:100%; padding:6px;"></td>
                                        <td>
                                            <select class="field-attr" style="width:100%; padding:5px;">
                                                <option value="text"><?php esc_html_e( 'Chữ (Text)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="html" selected><?php esc_html_e( 'Mã HTML', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="href"><?php esc_html_e( 'Link (href)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="src"><?php esc_html_e( 'Ảnh (src)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="alt"><?php esc_html_e( 'Tên ảnh / Thuộc tính alt (alt)', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </td>
                                        <td style="text-align:center;"><button type="button" class="wpsai-btn-remove wpsai-offline-delete-row" style="background:none; border:none; cursor:pointer; font-weight:bold; font-size:18px;">&times;</button></td>
                                    </tr>
                                    <tr data-row-idx="2">
                                        <td><input type="text" class="field-name large-text" value="featured_image" style="width:100%; padding:6px;"></td>
                                        <td><input type="text" class="field-selector large-text" value="img" style="width:100%; padding:6px;"></td>
                                        <td>
                                            <select class="field-attr" style="width:100%; padding:5px;">
                                                <option value="text"><?php esc_html_e( 'Chữ (Text)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="html"><?php esc_html_e( 'Mã HTML', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="href"><?php esc_html_e( 'Link (href)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="src" selected><?php esc_html_e( 'Ảnh (src)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="alt"><?php esc_html_e( 'Tên ảnh / Thuộc tính alt (alt)', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </td>
                                        <td style="text-align:center;"><button type="button" class="wpsai-btn-remove wpsai-offline-delete-row" style="background:none; border:none; cursor:pointer; font-weight:bold; font-size:18px;">&times;</button></td>
                                    </tr>
                                </tbody>
                            </table>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-offline-add-field-btn" style="margin-top: 10px;">
                                <span class="dashicons dashicons-plus-alt"></span> <?php esc_html_e( 'Thêm trường cột mới (ACF / Meta)', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>

                        <div class="wpsai-actions-row" style="margin-top: 25px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                            <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-offline-run-btn" disabled>
                                <span class="dashicons dashicons-filter"></span> <?php esc_html_e( 'Lọc & Bóc Tách HTML', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-success" id="wpsai-offline-export-btn" disabled>
                                <span class="dashicons dashicons-media-spreadsheet"></span> <?php esc_html_e( 'Xuất File Excel (.xlsx)', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-offline-export-json-btn" disabled>
                                <span class="dashicons dashicons-media-code"></span> <?php esc_html_e( 'Xuất dữ liệu JSON', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>

                        <!-- Console logger for user feedback inside WP -->
                        <div class="wpsai-import-log" id="wpsai-offline-log" style="height: 100px; margin-top: 15px; background: #f4f4f5; font-family: monospace; padding: 10px; border-left: 3px solid #10b981; overflow-y: auto;">
                            <p style="color: #64748b; margin: 0;">[Hệ thống] Đang chờ nạp file HTML...</p>
                        </div>
                    </div>

                    <!-- Lưới Xem Trước Dữ Liệu -->
                    <div class="wpsai-card" id="wpsai-offline-preview-card" style="margin-top: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h2 style="margin: 0;"><?php esc_html_e( 'Xem Trước Kết Quả Bóc Tách', 'wp-acf-smart-importer' ); ?></h2>
                            <span class="wpsai-badge" id="wpsai-offline-row-count-badge" style="background:#3b82f6;"><?php esc_html_e( 'Tổng số dòng: 0 dòng', 'wp-acf-smart-importer' ); ?></span>
                        </div>
                        <div class="wpsai-table-container" style="max-height: 400px; overflow: auto; border: 1px solid #e2e8f0; border-radius: 6px;">
                            <table class="wpsai-preview-table" id="wpsai-offline-preview-table">
                                <thead>
                                    <tr id="wpsai-offline-table-header">
                                        <!-- Header load động -->
                                    </tr>
                                </thead>
                                <tbody id="wpsai-offline-table-body">
                                    <tr>
                                        <td colspan="100" style="text-align: center; color: #94a3b8; padding: 30px 10px;">
                                            <span class="dashicons dashicons-info" style="font-size: 24px; width:24px; height:24px; vertical-align: middle; margin-right: 5px;"></span>
                                            <?php esc_html_e( 'Chưa có dữ liệu. Vui lòng nạp file HTML, cấu hình bộ lọc và nhấn nút "Lọc & Bóc Tách HTML".', 'wp-acf-smart-importer' ); ?>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <!-- Tab: Tạo Nội Dung AI -->
                <section id="wpsai-tab-ai-generator" class="wpsai-tab-content">
                    <!-- Bước 1: Chọn Post Type và các bài viết -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 1: Chọn Post Type & Các Bài Viết Cần Tạo Nội Dung Mẫu', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn Post Type để lấy danh sách bài viết, sau đó chọn các bài viết cụ thể bạn muốn điền/bổ sung nội dung mẫu bằng AI.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-form-group select-post-type-row" style="margin-bottom: 15px;">
                            <label for="wpsai-ai-generator-post-type"><strong><?php esc_html_e( 'Chọn Post Type:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <select id="wpsai-ai-generator-post-type" class="large-text" style="width: auto; min-width: 250px;">
                                <!-- Post Types load qua AJAX -->
                            </select>
                        </div>

                        <!-- Bộ lọc và Bảng danh sách bài viết -->
                        <div class="wpsai-posts-selector-wrapper" id="wpsai-ai-generator-posts-wrapper" style="display:none; margin-top: 20px;">
                            <div class="wpsai-flex-row" style="margin-bottom: 10px; justify-content: space-between; align-items: center;">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <label class="wpsai-checkbox-label">
                                        <input type="checkbox" id="wpsai-ai-generator-select-all" value="1">
                                        <strong><?php esc_html_e( 'Chọn tất cả', 'wp-acf-smart-importer' ); ?></strong>
                                    </label>
                                    <span id="wpsai-ai-generator-selected-count" style="color: var(--wpsai-primary); font-weight: 600;">Đã chọn: 0/0 bài viết</span>
                                </div>
                                <div>
                                    <input type="text" id="wpsai-ai-generator-search" placeholder="<?php esc_attr_e( 'Tìm kiếm bài viết...', 'wp-acf-smart-importer' ); ?>" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); width: 250px;">
                                </div>
                            </div>

                            <div class="wpsai-table-container" style="max-height: 250px;">
                                <table class="wpsai-preview-table" id="wpsai-ai-generator-posts-table">
                                    <thead>
                                        <tr>
                                            <th style="width: 50px; text-align: center;"></th>
                                            <th style="width: 80px;"><?php esc_html_e( 'Ảnh Hiện Tại', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 80px;"><?php esc_html_e( 'ID', 'wp-acf-smart-importer' ); ?></th>
                                            <th><?php esc_html_e( 'Tiêu Đề Bài Viết', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 150px;"><?php esc_html_e( 'Ngày Tạo', 'wp-acf-smart-importer' ); ?></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- Render động -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2: Cấu hình Yêu cầu AI -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 2: Cấu Hình Yêu Cầu Sinh Nội Dung AI', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Nhập chủ đề/mô tả ngắn liên quan đến nội dung cần sinh và cấu hình các tùy chọn chèn dữ liệu.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-form-group" style="margin-top: 15px;">
                            <label for="wpsai-ai-generator-topic"><strong><?php esc_html_e( 'Nhập chủ đề hoặc mô tả ngắn liên quan:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <textarea id="wpsai-ai-generator-topic" rows="4" style="width: 100%; max-width: 600px; display: block; margin-top: 5px; padding: 10px; border-radius: 6px; border: 1px solid var(--wpsai-border-color);" placeholder="<?php esc_attr_e( 'Ví dụ: Dịch vụ vận tải du thuyền siêu trường siêu trọng cho tập đoàn FLC từ Quảng Ninh đi Bình Định bằng đường biển...', 'wp-acf-smart-importer' ); ?>"></textarea>
                        </div>

                        <div class="wpsai-flex-row" style="margin-top: 15px; gap: 20px; flex-wrap: wrap;">
                            <div class="wpsai-form-group" style="flex: 1; min-width: 300px;">
                                <label for="wpsai-ai-generator-titles"><strong><?php esc_html_e( 'Danh sách Tiêu đề bài viết (Tùy chọn, mỗi dòng một bài):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <textarea id="wpsai-ai-generator-titles" rows="4" style="width: 100%; display: block; margin-top: 5px; padding: 10px; border-radius: 6px; border: 1px solid var(--wpsai-border-color);" placeholder="<?php esc_attr_e( "Hướng dẫn tối ưu tốc độ WordPress\nMẹo bảo mật website cơ bản", 'wp-acf-smart-importer' ); ?>"></textarea>
                                <p class="description" style="margin-top:5px; font-size:11px;"><?php esc_html_e( 'Nếu nhập danh sách này, số lượng bài viết cần sinh sẽ tự động tính theo số lượng tiêu đề đã nhập.', 'wp-acf-smart-importer' ); ?></p>
                            </div>

                            <div class="wpsai-form-group" style="flex: 1; min-width: 300px;">
                                <label for="wpsai-ai-generator-layout"><strong><?php esc_html_e( 'Bố cục nội dung chi tiết bài viết (Layout Template - Tùy chọn):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <textarea id="wpsai-ai-generator-layout" rows="4" style="width: 100%; display: block; margin-top: 5px; padding: 10px; border-radius: 6px; border: 1px solid var(--wpsai-border-color);" placeholder="<?php esc_attr_e( "<h2>Giới thiệu về [post_title]</h2>\n<p>Giới thiệu ngắn...</p>\n<h2>Các nội dung cốt lõi</h2>\n<ul><li>Ý chính 1...</li></ul>", 'wp-acf-smart-importer' ); ?>"></textarea>
                                <p class="description" style="margin-top:5px; font-size:11px;"><?php esc_html_e( 'Quy định bố cục bài viết bằng HTML hoặc Markdown. AI sẽ tự động điền nội dung chi tiết theo bố cục này.', 'wp-acf-smart-importer' ); ?></p>
                            </div>
                        </div>

                        <div class="wpsai-flex-row" style="margin-top: 15px; gap: 20px; flex-wrap: wrap;">
                            <div class="wpsai-form-group">
                                <label for="wpsai-ai-generator-count"><strong><?php esc_html_e( 'Số lượng dòng dữ liệu cần sinh:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="number" id="wpsai-ai-generator-count" value="5" min="1" max="100" class="small-text" style="padding: 10px 14px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); width: 100px; margin-top: 5px; display: block;">
                            </div>
                            
                            <div class="wpsai-form-group">
                                <label for="wpsai-ai-generator-post-status"><strong><?php esc_html_e( 'Trạng thái bài viết mặc định (nếu tạo mới):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-ai-generator-post-status" class="large-text" style="padding: 9px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); margin-top: 5px; display: block; width: auto; min-width: 180px;">
                                    <option value="draft" selected><?php esc_html_e( 'Bản nháp (Draft)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="pending"><?php esc_html_e( 'Chờ duyệt (Pending)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="publish"><?php esc_html_e( 'Đã đăng (Publish)', 'wp-acf-smart-importer' ); ?></option>
                                </select>
                            </div>
                        </div>

                        <div class="wpsai-form-group" style="margin-top: 20px;">
                            <label><strong><?php esc_html_e( 'Chế độ chèn / cập nhật dữ liệu:', 'wp-acf-smart-importer' ); ?></strong></label>
                            <div class="wpsai-generator-modes" style="margin-top: 10px; display: flex; gap: 15px; flex-wrap: wrap;">
                                <!-- Chế độ Cập nhật -->
                                <label class="wpsai-radio-card active" style="flex: 1; min-width: 250px;">
                                    <input type="radio" name="wpsai_ai_generator_import_mode" value="update_selected" checked>
                                    <div class="wpsai-radio-card-content">
                                        <h4><?php esc_html_e( 'Chỉ Cập Nhật Bài Viết Đã Chọn', 'wp-acf-smart-importer' ); ?></h4>
                                        <p><?php esc_html_e( 'Cập nhật tuần tự các bài viết đã chọn ở Bước 1. Số dòng sinh ra sẽ giới hạn theo số bài viết được chọn.', 'wp-acf-smart-importer' ); ?></p>
                                    </div>
                                </label>

                                <!-- Chế độ Kết hợp -->
                                <label class="wpsai-radio-card" style="flex: 1; min-width: 250px;">
                                    <input type="radio" name="wpsai_ai_generator_import_mode" value="update_and_create">
                                    <div class="wpsai-radio-card-content">
                                        <h4><?php esc_html_e( 'Cập Nhật & Tạo Mới Nếu Thiếu', 'wp-acf-smart-importer' ); ?></h4>
                                        <p><?php esc_html_e( 'Cập nhật các bài viết đã chọn trước. Nếu số lượng dòng cần sinh nhiều hơn số bài đã chọn, phần còn lại sẽ tự động tạo thành bài viết mới.', 'wp-acf-smart-importer' ); ?></p>
                                    </div>
                                </label>

                                <!-- Chế độ Tạo mới -->
                                <label class="wpsai-radio-card" style="flex: 1; min-width: 250px;">
                                    <input type="radio" name="wpsai_ai_generator_import_mode" value="create_only">
                                    <div class="wpsai-radio-card-content">
                                        <h4><?php esc_html_e( 'Tạo Mới Hoàn Toàn', 'wp-acf-smart-importer' ); ?></h4>
                                        <p><?php esc_html_e( 'Bỏ qua việc cập nhật các bài viết cũ. Tạo mới hoàn toàn N bài viết mới (N là số lượng dòng dữ liệu cần sinh).', 'wp-acf-smart-importer' ); ?></p>
                                    </div>
                                </label>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2b: Kho Ảnh Nội Dung -->
                    <div class="wpsai-card">
                        <h2><span class="dashicons dashicons-images-alt2" style="color: var(--wpsai-primary); margin-right: 6px;"></span> <?php esc_html_e( 'Bước 2b: Kho Ảnh Nội Dung (Tùy chọn)', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn ảnh từ Thư viện Media để tự động chèn vào nội dung bài viết khi AI sinh xong. Nếu bỏ qua bước này, bài viết sẽ không có ảnh trong nội dung.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div style="margin-top: 15px; display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                            <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-ai-image-pool-select-btn">
                                <span class="dashicons dashicons-images-alt2"></span> <?php esc_html_e( 'Chọn / Tải lên ảnh từ Thư viện', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-ai-image-pool-clear-btn" style="display: none;">
                                <?php esc_html_e( 'Xóa danh sách ảnh đã chọn', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <span id="wpsai-ai-image-pool-count-badge" class="wpsai-badge" style="background:var(--wpsai-primary); padding:3px 10px; font-size:12px; display: none;">0 ảnh</span>
                        </div>

                        <!-- Grid hiển thị ảnh đã chọn -->
                        <div id="wpsai-ai-image-pool-preview" style="display: none; margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee;">
                            <p style="font-weight: 600; margin-bottom: 10px;"><?php esc_html_e( 'Danh sách ảnh sẽ được chèn vào nội dung bài viết:', 'wp-acf-smart-importer' ); ?></p>
                            <div class="wpsai-images-preview-grid" id="wpsai-ai-image-pool-grid">
                                <!-- Render động -->
                            </div>
                        </div>

                        <!-- Cấu hình phân bổ ảnh -->
                        <div id="wpsai-ai-image-pool-settings" style="display: none; margin-top: 20px; padding: 15px; background: #f8fafc; border-radius: 8px; border: 1px solid var(--wpsai-border-color);">
                            <div class="wpsai-flex-row" style="gap: 20px; flex-wrap: wrap; align-items: flex-end;">
                                <div class="wpsai-form-group" style="margin-bottom: 0;">
                                    <label for="wpsai-ai-image-insert-mode"><strong><?php esc_html_e( 'Chế độ phân bổ ảnh:', 'wp-acf-smart-importer' ); ?></strong></label>
                                    <select id="wpsai-ai-image-insert-mode" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); margin-top: 5px; display: block; width: auto; min-width: 220px;">
                                        <option value="sequential" selected><?php esc_html_e( 'Tuần tự (Sequential) - Ảnh 1 → Bài 1, Ảnh 2 → Bài 2...', 'wp-acf-smart-importer' ); ?></option>
                                        <option value="random"><?php esc_html_e( 'Ngẫu nhiên (Random) - Mỗi bài nhận ảnh ngẫu nhiên', 'wp-acf-smart-importer' ); ?></option>
                                        <option value="cycle"><?php esc_html_e( 'Lặp vòng (Cycle) - Lặp lại từ đầu khi hết ảnh', 'wp-acf-smart-importer' ); ?></option>
                                    </select>
                                </div>

                                <div class="wpsai-form-group" style="margin-bottom: 0;">
                                    <label class="wpsai-checkbox-label" style="cursor: pointer;">
                                        <input type="checkbox" id="wpsai-ai-image-set-featured" value="1" checked>
                                        <strong><?php esc_html_e( 'Tự động gán ảnh đầu tiên làm Ảnh đại diện (Featured Image)', 'wp-acf-smart-importer' ); ?></strong>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Bước 2c: Phân Tích Bài Mẫu (Tùy chọn) -->
                    <div class="wpsai-card">
                        <h2><span class="dashicons dashicons-visibility" style="color: var(--wpsai-warning); margin-right: 6px;"></span> <?php esc_html_e( 'Bước 2c: Phân Tích Bài Mẫu (Tùy chọn)', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn một bài viết mẫu để phân tích vị trí ảnh trong nội dung. Hệ thống sẽ chèn ảnh từ Kho Ảnh vào đúng vị trí tương tự trong bài viết mới. Nếu bỏ qua, ảnh sẽ tự động chèn sau mỗi thẻ heading (h2/h3).', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-flex-row" style="margin-top: 15px; gap: 15px; align-items: flex-end; flex-wrap: wrap;">
                            <div class="wpsai-form-group" style="margin-bottom: 0; flex: 1; min-width: 250px;">
                                <label for="wpsai-ai-template-post"><strong><?php esc_html_e( 'Chọn Bài Viết Mẫu:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-ai-template-post" class="large-text" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); margin-top: 5px; display: block; width: 100%;">
                                    <option value=""><?php esc_html_e( '-- Không sử dụng bài mẫu (Tự động chèn sau heading) --', 'wp-acf-smart-importer' ); ?></option>
                                    <!-- Load động theo Post Type -->
                                </select>
                            </div>

                            <div class="wpsai-form-group-btn" style="margin-bottom: 0;">
                                <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-ai-analyze-template-btn" disabled>
                                    <span class="dashicons dashicons-search"></span> <?php esc_html_e( 'Phân Tích Cấu Trúc', 'wp-acf-smart-importer' ); ?>
                                </button>
                            </div>
                        </div>

                        <!-- Kết quả phân tích -->
                        <div id="wpsai-ai-template-result" style="display: none; margin-top: 20px; padding: 15px; background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%); border-radius: 8px; border: 1px solid #86efac;">
                            <p style="font-weight: 600; margin: 0 0 10px 0; color: #166534;">
                                <span class="dashicons dashicons-yes-alt" style="color: #16a34a;"></span> 
                                <?php esc_html_e( 'Kết quả phân tích:', 'wp-acf-smart-importer' ); ?>
                            </p>
                            <div id="wpsai-ai-template-result-detail">
                                <!-- Render động: số ảnh tìm thấy, danh sách heading -->
                            </div>
                        </div>
                    </div>

                    <!-- Bước 3: Thực thi -->
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Bước 3: Thực Thi Tiến Trình AI', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Hệ thống sẽ chia nhỏ số dòng cần sinh để gọi API Gemini theo đợt (batch), sau đó tự động lưu vào cơ sở dữ liệu.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-actions-row" style="margin-top: 15px;">
                            <button type="button" class="wpsai-btn wpsai-btn-primary wpsai-btn-large" id="wpsai-ai-generator-start-btn">
                                <span class="dashicons dashicons-lightbulb"></span> <?php esc_html_e( 'Khởi Chạy Sinh Dữ Liệu AI', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>

                    <!-- Tiến trình & log thực thi -->
                    <div class="wpsai-card wpsai-section-step" id="wpsai-ai-generator-progress-card" style="display: none;">
                        <h2><?php esc_html_e( 'Tiến Trình Sinh & Nhập Dữ Liệu AI', 'wp-acf-smart-importer' ); ?></h2>
                        <div class="wpsai-progress-bar-wrapper">
                            <div class="wpsai-progress-bar" id="wpsai-ai-generator-progress-bar" style="width: 0%;">0%</div>
                        </div>
                        <div class="wpsai-progress-stats" id="wpsai-ai-generator-progress-stats">
                            <p><?php esc_html_e( 'Đang chuẩn bị kết nối...', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        <div class="wpsai-import-log" id="wpsai-ai-generator-log">
                            <!-- Log chi tiết -->
                        </div>
                    </div>
                </section>

                <!-- Tab Lấy Tiêu Đề Bài Viết -->
                <section id="wpsai-tab-get-titles" class="wpsai-tab-content">
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Lấy Tiêu Đề Của Tất Cả Bài Viết Hiện Có', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Chọn Post Type và chuyên mục để lấy nhanh danh sách tiêu đề bài viết hiện có.', 'wp-acf-smart-importer' ); ?></p>
                        
                        <div class="wpsai-flex-row select-post-row" style="align-items: flex-end; gap: 15px;">
                            <div class="wpsai-form-group" style="flex: 1;">
                                <label for="wpsai-titles-post-type"><strong><?php esc_html_e( 'Chọn Post Type:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-titles-post-type" class="large-text" style="width: 100%;">
                                    <!-- Post Types load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group" style="flex: 1;">
                                <label for="wpsai-titles-taxonomy"><strong><?php esc_html_e( 'Chọn Phân Loại (Taxonomy):', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-titles-taxonomy" class="large-text" style="width: 100%;">
                                    <option value=""><?php esc_html_e( '-- Chọn phân loại --', 'wp-acf-smart-importer' ); ?></option>
                                    <!-- Taxonomies load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group" style="flex: 1;">
                                <label for="wpsai-titles-term"><strong><?php esc_html_e( 'Chọn Danh Mục / Term:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <select id="wpsai-titles-term" class="large-text" style="width: 100%;" disabled>
                                    <option value=""><?php esc_html_e( '-- Chọn danh mục / term --', 'wp-acf-smart-importer' ); ?></option>
                                    <!-- Terms load qua AJAX -->
                                </select>
                            </div>
                            <div class="wpsai-form-group-btn" style="flex: 0 0 auto;">
                                <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-get-titles-btn">
                                    <span class="dashicons dashicons-editor-ul"></span> <?php esc_html_e( 'Lấy Danh Sách Tiêu Đề', 'wp-acf-smart-importer' ); ?>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Kết quả Lấy Tiêu Đề (Ẩn mặc định) -->
                    <div class="wpsai-card" id="wpsai-titles-result-card" style="display: none; margin-top: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--wpsai-border-color); padding-bottom: 10px; margin-bottom: 15px;">
                            <h2 style="margin: 0;"><span class="dashicons dashicons-editor-ul" style="color: var(--wpsai-primary);"></span> <?php esc_html_e( 'Kết Quả Lấy Tiêu Đề', 'wp-acf-smart-importer' ); ?> (<span id="wpsai-titles-count">0</span> bài viết)</h2>
                            <div>
                                <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-copy-titles-btn">
                                    <span class="dashicons dashicons-admin-page"></span> <?php esc_html_e( 'Sao Chép Toàn Bộ Tiêu Đề', 'wp-acf-smart-importer' ); ?>
                                </button>
                            </div>
                        </div>

                        <!-- Render dạng Textarea (Copy-Paste) -->
                        <div class="wpsai-form-group">
                            <label for="wpsai-titles-textarea"><strong><?php esc_html_e( 'Danh sách tiêu đề (mỗi dòng một tiêu đề):', 'wp-acf-smart-importer' ); ?></strong></label>
                            <textarea id="wpsai-titles-textarea" class="large-text" rows="10" style="font-family: monospace; font-size: 13px; width: 100%; margin-top: 5px;" readonly></textarea>
                        </div>

                        <!-- Bảng chi tiết -->
                        <div class="wpsai-table-container" style="margin-top: 20px;">
                            <h3><?php esc_html_e( 'Bảng Chi Tiết Bài Viết', 'wp-acf-smart-importer' ); ?></h3>
                            <table class="wpsai-preview-table" id="wpsai-titles-table">
                                <thead>
                                    <tr>
                                        <th style="width: 40px; text-align: center;"><input type="checkbox" id="wpsai-titles-select-all" checked></th>
                                        <th style="width: 80px;"><?php esc_html_e( 'ID', 'wp-acf-smart-importer' ); ?></th>
                                        <th><?php esc_html_e( 'Tiêu Đề', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 180px;"><?php esc_html_e( 'Phân Loại', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 150px;"><?php esc_html_e( 'Ngày Tạo', 'wp-acf-smart-importer' ); ?></th>
                                        <th style="width: 100px; text-align: center;"><?php esc_html_e( 'Liên Kết', 'wp-acf-smart-importer' ); ?></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- Render động qua JS -->
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Card Cập nhật tiêu đề hàng loạt (Ẩn mặc định) -->
                    <div class="wpsai-card" id="wpsai-titles-update-card" style="display: none; margin-top: 20px; border-top: 4px solid var(--wpsai-secondary);">
                        <h2><span class="dashicons dashicons-edit" style="color: var(--wpsai-secondary);"></span> <?php esc_html_e( 'Cập Nhật Hàng Loạt Tiêu Đề Mới (Dịch / Thay thế)', 'wp-acf-smart-importer' ); ?></h2>
                        <p class="description-p"><?php esc_html_e( 'Dán danh sách tiêu đề mới hoặc chọn dịch tự động bằng AI. Hệ thống sẽ so khớp theo thứ tự dòng và cập nhật hàng loạt tiêu đề cho các bài viết được tích chọn trong bảng.', 'wp-acf-smart-importer' ); ?></p>

                        <!-- Khối Dịch thuật tự động bằng AI -->
                        <div style="background: #faf5ff; border: 1px solid #e9d5ff; border-radius: 8px; padding: 15px; margin-bottom: 20px; display: flex; align-items: flex-end; gap: 15px; flex-wrap: wrap;">
                            <div style="flex: 1; min-width: 200px;">
                                <label for="wpsai-titles-translator-engine" style="display: block; font-weight: bold; margin-bottom: 5px; color: #581c87;">
                                    <span class="dashicons dashicons-admin-tools" style="font-size: 18px; width: 18px; height: 18px; color: #8b5cf6; vertical-align: middle;"></span> <?php esc_html_e( 'Bộ máy dịch thuật:', 'wp-acf-smart-importer' ); ?>
                                </label>
                                <select id="wpsai-titles-translator-engine" class="large-text" style="width: 100%; border-color: #d8b4fe;">
                                    <option value="google_translate"><?php esc_html_e( 'Google Translate (Miễn Phí)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="gemini"><?php esc_html_e( 'Gemini AI (Cần API Key)', 'wp-acf-smart-importer' ); ?></option>
                                </select>
                            </div>
                            <div style="flex: 1; min-width: 200px;">
                                <label for="wpsai-titles-target-lang" style="display: block; font-weight: bold; margin-bottom: 5px; color: #581c87;">
                                    <span class="dashicons dashicons-translation" style="font-size: 18px; width: 18px; height: 18px; color: #8b5cf6; vertical-align: middle;"></span> <?php esc_html_e( 'Dịch sang ngôn ngữ:', 'wp-acf-smart-importer' ); ?>
                                </label>
                                <select id="wpsai-titles-target-lang" class="large-text" style="width: 100%; border-color: #d8b4fe;">
                                    <option value="English"><?php esc_html_e( 'Tiếng Anh (English)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="Japanese"><?php esc_html_e( 'Tiếng Nhật (Japanese)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="Chinese (Simplified)"><?php esc_html_e( 'Tiếng Trung Giản Thể (Chinese)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="Korean"><?php esc_html_e( 'Tiếng Hàn (Korean)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="French"><?php esc_html_e( 'Tiếng Pháp (French)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="German"><?php esc_html_e( 'Tiếng Đức (German)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="Spanish"><?php esc_html_e( 'Tiếng Tây Ban Nha (Spanish)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="Russian"><?php esc_html_e( 'Tiếng Nga (Russian)', 'wp-acf-smart-importer' ); ?></option>
                                    <option value="Vietnamese"><?php esc_html_e( 'Tiếng Việt (Vietnamese)', 'wp-acf-smart-importer' ); ?></option>
                                </select>
                            </div>
                            <div style="display: flex; align-items: center; height: 40px; margin-bottom: 2px;">
                                <label style="display: flex; align-items: center; gap: 6px; font-weight: 500; cursor: pointer; color: #5b21b6;">
                                    <input type="checkbox" id="wpsai-titles-translate-content-checkbox" style="margin: 0;" />
                                    <span><?php esc_html_e( 'Dịch cả Nội dung & Mô tả ngắn', 'wp-acf-smart-importer' ); ?></span>
                                </label>
                            </div>
                            <div>
                                <button type="button" class="wpsai-btn" id="wpsai-translate-titles-btn" style="background: #8b5cf6; border-color: #7c3aed; color: white; display: flex; align-items: center; gap: 5px; margin: 0;">
                                    <span class="dashicons dashicons-translation"></span> <?php esc_html_e( 'Dịch Tiêu Đề Bằng AI', 'wp-acf-smart-importer' ); ?>
                                </button>
                            </div>
                        </div>
                        
                        <!-- Khung thông báo lỗi Dịch thuật (Ẩn mặc định) -->
                        <div id="wpsai-titles-translation-error" style="display: none; background: #fef2f2; border: 1px solid #fee2e2; color: #b91c1c; padding: 12px 15px; border-radius: 8px; font-size: 13px; margin-bottom: 20px; line-height: 1.5; font-family: monospace; overflow-x: auto; max-height: 200px; white-space: pre-wrap;"></div>
                        
                        <div class="wpsai-form-group" style="margin-top: 15px;">
                            <label for="wpsai-titles-new-textarea"><strong><?php esc_html_e( 'Danh sách tiêu đề mới (đặt đúng thứ tự, mỗi dòng một tiêu đề):', 'wp-acf-smart-importer' ); ?></strong></label>
                            <textarea id="wpsai-titles-new-textarea" class="large-text" rows="10" style="font-family: monospace; font-size: 13px; width: 100%; margin-top: 5px;" placeholder="<?php esc_attr_e( "Tiêu đề mới 1\nTiêu đề mới 2\nTiêu đề mới 3...", 'wp-acf-smart-importer' ); ?>"></textarea>
                        </div>

                        <!-- Panel đối chiếu số lượng -->
                        <div style="display: flex; align-items: center; justify-content: space-between; background: #f8fafc; border: 1px solid var(--wpsai-border-color); padding: 12px 15px; border-radius: 8px; margin-top: 15px;">
                            <div style="font-size: 13px; color: #475569;">
                                <span><?php esc_html_e( 'Số lượng bài viết mục tiêu:', 'wp-acf-smart-importer' ); ?> <strong id="wpsai-target-posts-count" style="color: var(--wpsai-primary);">0</strong></span>
                                <span style="margin: 0 10px; color: #cbd5e1;">|</span>
                                <span><?php esc_html_e( 'Số dòng tiêu đề mới nhập vào:', 'wp-acf-smart-importer' ); ?> <strong id="wpsai-new-titles-count" style="color: var(--wpsai-primary);">0</strong></span>
                            </div>
                            <div>
                                <span id="wpsai-titles-match-badge" class="wpsai-badge-type" style="font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 4px; background: #ef4444; color: white;">
                                    <?php esc_html_e( 'Chưa khớp', 'wp-acf-smart-importer' ); ?>
                                </span>
                            </div>
                        </div>

                        <!-- Progress Bar & Logs -->
                        <div id="wpsai-titles-update-progress" style="display: none; margin-top: 20px;">
                            <div class="wpsai-progress-bar-wrapper" style="background: #e2e8f0; border-radius: 6px; overflow: hidden; height: 20px; position: relative; margin-bottom: 10px;">
                                <div id="wpsai-titles-update-progress-bar" class="wpsai-progress-bar" style="width: 0%; height: 100%; background: var(--wpsai-secondary); color: white; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; transition: width 0.2s ease;">0%</div>
                            </div>
                            <div id="wpsai-titles-update-progress-stats" style="font-size: 13px; color: var(--wpsai-text-muted); margin-bottom: 10px;"></div>
                            <div id="wpsai-titles-update-log" class="wpsai-import-log" style="max-height: 150px; overflow-y: auto; background: #fafafb; border: 1px solid #e2e8f0; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 12px; line-height: 1.5;"></div>
                        </div>

                        <!-- Nút hành động -->
                        <div style="margin-top: 20px; text-align: right;">
                            <button type="button" class="wpsai-btn wpsai-btn-success" id="wpsai-execute-update-titles-btn" style="background: var(--wpsai-secondary); border-color: var(--wpsai-secondary);" disabled>
                                <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Cập Nhật Hàng Loạt Tiêu Đề', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>
                </section>

                <!-- Tab 2: Cấu Hình API Key -->
                <section id="wpsai-tab-settings" class="wpsai-tab-content">
                    <div class="wpsai-card">
                        <h2><?php esc_html_e( 'Cấu Hình API Key Cho Tính Năng AI & Extension', 'wp-acf-smart-importer' ); ?></h2>
                        <p><?php esc_html_e( 'Cấu hình Gemini API Key và lấy API Key cho Chrome Extension.', 'wp-acf-smart-importer' ); ?></p>

                        <div class="wpsai-settings-form">
                            <div class="wpsai-form-group">
                                <label for="wpsai-gemini-key"><strong><?php esc_html_e( 'Gemini API Key:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <input type="password" id="wpsai-gemini-key" class="large-text" value="<?php echo esc_attr( get_option( 'wpsai_gemini_api_key', '' ) ); ?>" placeholder="AIzaSy...">
                                <p class="description"><?php echo sprintf( __( 'Lấy API Key miễn phí tại <a href="%s" target="_blank">Google AI Studio</a>.', 'wp-acf-smart-importer' ), 'https://aistudio.google.com/' ); ?></p>
                            </div>

                            <div class="wpsai-form-group" style="margin-top: 20px; border-top: 1px solid var(--wpsai-border-color); padding-top: 20px;">
                                <label for="wpsai-extension-key"><strong><?php esc_html_e( 'Chrome Extension API Key:', 'wp-acf-smart-importer' ); ?></strong></label>
                                <?php 
                                $ext_key = get_option( 'wpsai_extension_api_key', '' );
                                if ( empty( $ext_key ) ) {
                                    $ext_key = wp_generate_password( 24, false );
                                    update_option( 'wpsai_extension_api_key', $ext_key );
                                }
                                ?>
                                <div style="display: flex; gap: 10px; align-items: center; margin-top: 5px;">
                                    <input type="text" id="wpsai-extension-key" class="large-text" value="<?php echo esc_attr( $ext_key ); ?>" style="width: 100%; max-width: 500px; font-family: monospace; margin: 0;" readonly>
                                    <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-copy-ext-key-btn" style="margin: 0;"><?php esc_html_e( 'Sao chép Key', 'wp-acf-smart-importer' ); ?></button>
                                </div>
                                <p class="description"><?php esc_html_e( 'Sao chép khóa bí mật này và dán vào Chrome Extension để liên kết với website.', 'wp-acf-smart-importer' ); ?></p>
                            </div>

                            <div class="wpsai-actions-row" style="margin-top: 20px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                                <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-save-settings-btn"><?php esc_html_e( 'Lưu Cài Đặt', 'wp-acf-smart-importer' ); ?></button>
                                <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-test-gemini-btn" style="border-color: #8b5cf6; color: #6d28d9; background: #f5f3ff;">
                                    <span class="dashicons dashicons-admin-plugins" style="font-size: 16px; width: 16px; height: 16px; vertical-align: middle;"></span> <?php esc_html_e( 'Kiểm Tra Kết Nối API Key', 'wp-acf-smart-importer' ); ?>
                                </button>
                                <span id="wpsai-settings-msg" class="wpsai-status-msg"></span>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Tab 10: Quản Lý Tài Liệu Dự Án -->
                <section id="wpsai-tab-project-docs" class="wpsai-tab-content">
                    <div class="wpsai-card" style="background: linear-gradient(135deg, #1e1b4b 0%, #1e293b 100%); color: #fff; margin-bottom: 24px; border: none; position: relative; overflow: hidden;">
                        <div style="position: relative; z-index: 2;">
                            <h2 style="color: #fff; font-size: 22px; margin-bottom: 8px;"><span class="dashicons dashicons-portfolio" style="font-size: 24px; width: 24px; height: 24px; color: var(--wpsai-secondary);"></span> <?php esc_html_e( 'Quản Lý Tài Liệu Dự Án', 'wp-acf-smart-importer' ); ?></h2>
                            <p style="color: rgba(255, 255, 255, 0.8); margin: 0; font-size: 14px;"><?php esc_html_e( 'Ghi chép nhật ký công việc phát triển, quản lý thư viện UI Components có sandbox chạy thử và đồng bộ tệp dự án di động.', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        <div style="position: absolute; right: -50px; bottom: -50px; opacity: 0.1; font-size: 180px; width: 180px; height: 180px;" class="dashicons dashicons-portfolio"></div>
                    </div>

                    <!-- Sub-tabs Navigation -->
                    <div class="wpsai-sub-tabs-nav" style="display: flex; gap: 8px; margin-bottom: 20px; border-bottom: 2px solid var(--wpsai-border-color); padding-bottom: 2px; flex-wrap: wrap;">
                        <button class="wpsai-sub-tab-btn active" data-subtab="overview" style="display: flex; align-items: center; gap: 6px; padding: 10px 18px; border: none; background: none; color: var(--wpsai-text-muted); font-weight: 600; font-size: 14px; cursor: pointer; border-radius: 8px 8px 0 0; transition: all 0.2s ease;">
                            <span class="dashicons dashicons-info" style="font-size: 16px; width: 16px; height: 16px;"></span> <?php esc_html_e( 'Tổng Quan Dự Án', 'wp-acf-smart-importer' ); ?>
                        </button>
                        <button class="wpsai-sub-tab-btn" data-subtab="worklogs" style="display: flex; align-items: center; gap: 6px; padding: 10px 18px; border: none; background: none; color: var(--wpsai-text-muted); font-weight: 600; font-size: 14px; cursor: pointer; border-radius: 8px 8px 0 0; transition: all 0.2s ease;">
                            <span class="dashicons dashicons-welcome-write-blog" style="font-size: 16px; width: 16px; height: 16px;"></span> <?php esc_html_e( 'Nhật Ký Công Việc', 'wp-acf-smart-importer' ); ?>
                        </button>
                        <button class="wpsai-sub-tab-btn" data-subtab="ui-library" style="display: flex; align-items: center; gap: 6px; padding: 10px 18px; border: none; background: none; color: var(--wpsai-text-muted); font-weight: 600; font-size: 14px; cursor: pointer; border-radius: 8px 8px 0 0; transition: all 0.2s ease;">
                            <span class="dashicons dashicons-layout" style="font-size: 16px; width: 16px; height: 16px;"></span> <?php esc_html_e( 'Thư Viện UI Components', 'wp-acf-smart-importer' ); ?>
                        </button>
                        <button class="wpsai-sub-tab-btn" data-subtab="tech-notes" style="display: flex; align-items: center; gap: 6px; padding: 10px 18px; border: none; background: none; color: var(--wpsai-text-muted); font-weight: 600; font-size: 14px; cursor: pointer; border-radius: 8px 8px 0 0; transition: all 0.2s ease;">
                            <span class="dashicons dashicons-edit" style="font-size: 16px; width: 16px; height: 16px;"></span> <?php esc_html_e( 'Ghi Chú Kỹ Thuật', 'wp-acf-smart-importer' ); ?>
                        </button>
                        <button class="wpsai-sub-tab-btn" data-subtab="sync-export" style="display: flex; align-items: center; gap: 6px; padding: 10px 18px; border: none; background: none; color: var(--wpsai-text-muted); font-weight: 600; font-size: 14px; cursor: pointer; border-radius: 8px 8px 0 0; transition: all 0.2s ease;">
                            <span class="dashicons dashicons-update-alt" style="font-size: 16px; width: 16px; height: 16px;"></span> <?php esc_html_e( 'Đồng Bộ & Nhập Xuất', 'wp-acf-smart-importer' ); ?>
                        </button>
                    </div>

                    <!-- SUBTAB 1: TỔNG QUAN -->
                    <div id="wpsai-subtab-overview" class="wpsai-subtab-content active">
                        <div class="wpsai-flex-row">
                            <!-- Nhập thông tin dự án -->
                            <div class="wpsai-card" style="flex: 1.5; min-width: 300px;">
                                <h2><span class="dashicons dashicons-edit" style="color: var(--wpsai-primary);"></span> <?php esc_html_e( 'Thông Tin Dự Án', 'wp-acf-smart-importer' ); ?></h2>
                                <div class="wpsai-settings-form" style="margin-top: 15px;">
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-doc-project-name"><strong><?php esc_html_e( 'Tên dự án:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="text" id="wpsai-doc-project-name" class="large-text" placeholder="Ví dụ: Landing Page Bất Động Sản VinHomes">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-doc-project-url"><strong><?php esc_html_e( 'Website URL / Domain dự án:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="url" id="wpsai-doc-project-url" class="large-text" placeholder="https://example.com">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-doc-git-repo"><strong><?php esc_html_e( 'Git Repository (nếu có):', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="text" id="wpsai-doc-git-repo" class="large-text" placeholder="git@github.com:username/project.git">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-doc-lead-dev"><strong><?php esc_html_e( 'Lập trình viên chính (Lead Developer):', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="text" id="wpsai-doc-lead-dev" class="large-text" placeholder="Nguyễn Văn A">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-doc-project-desc"><strong><?php esc_html_e( 'Mô tả dự án:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <textarea id="wpsai-doc-project-desc" class="large-text" rows="5" placeholder="Ghi chú tổng quát về dự án, mục tiêu và phạm vi công việc..."></textarea>
                                    </div>
                                    <div style="margin-top: 20px;">
                                        <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-doc-save-overview-btn">
                                            <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Lưu Tất Cả Thay Đổi Tài Liệu', 'wp-acf-smart-importer' ); ?>
                                        </button>
                                        <span id="wpsai-doc-overview-msg" class="wpsai-status-msg"></span>
                                    </div>
                                </div>
                            </div>

                            <!-- Quét cấu hình hệ thống -->
                            <div class="wpsai-card" style="flex: 1; min-width: 250px; background: #fafafb;">
                                <h2><span class="dashicons dashicons-admin-generic" style="color: var(--wpsai-secondary);"></span> <?php esc_html_e( 'Cấu Hình Môi Trường Hệ Thống', 'wp-acf-smart-importer' ); ?></h2>
                                <p class="description-p" style="font-size: 13px;"><?php esc_html_e( 'Thông tin tự động quét từ website hiện tại để tham khảo cấu hình.', 'wp-acf-smart-importer' ); ?></p>
                                
                                <div id="wpsai-doc-sys-info" style="margin-top: 15px; display: flex; flex-direction: column; gap: 12px;">
                                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                                        <span style="font-weight: 600; color: #475569;"><?php esc_html_e( 'Phiên bản WordPress:', 'wp-acf-smart-importer' ); ?></span>
                                        <span id="wpsai-sys-wp" style="font-family: monospace;">-</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                                        <span style="font-weight: 600; color: #475569;"><?php esc_html_e( 'Phiên bản PHP:', 'wp-acf-smart-importer' ); ?></span>
                                        <span id="wpsai-sys-php" style="font-family: monospace;">-</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                                        <span style="font-weight: 600; color: #475569;"><?php esc_html_e( 'Cơ sở dữ liệu DB:', 'wp-acf-smart-importer' ); ?></span>
                                        <span id="wpsai-sys-db" style="font-family: monospace;">-</span>
                                    </div>
                                    <div style="display: flex; justify-content: space-between; border-bottom: 1px dashed #e2e8f0; padding-bottom: 6px;">
                                        <span style="font-weight: 600; color: #475569;"><?php esc_html_e( 'Theme kích hoạt:', 'wp-acf-smart-importer' ); ?></span>
                                        <span id="wpsai-sys-theme" style="text-align: right;">-</span>
                                    </div>
                                    
                                    <div style="margin-top: 8px;">
                                        <span style="font-weight: 600; color: #475569; display: block; margin-bottom: 6px;"><?php esc_html_e( 'Custom Post Types đã đăng ký:', 'wp-acf-smart-importer' ); ?></span>
                                        <div id="wpsai-sys-cpts" style="max-height: 100px; overflow-y: auto; background: #fff; border: 1px solid #e2e8f0; padding: 8px; border-radius: 6px; font-size: 12px; line-height: 1.5;">
                                            <!-- Render động -->
                                        </div>
                                    </div>

                                    <div style="margin-top: 8px;">
                                        <span style="font-weight: 600; color: #475569; display: block; margin-bottom: 6px;"><?php esc_html_e( 'Plugins đang kích hoạt:', 'wp-acf-smart-importer' ); ?></span>
                                        <div id="wpsai-sys-plugins" style="max-height: 120px; overflow-y: auto; background: #fff; border: 1px solid #e2e8f0; padding: 8px; border-radius: 6px; font-size: 12px; line-height: 1.5;">
                                            <!-- Render động -->
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- SUBTAB 2: NHẬT KÝ CÔNG VIỆC -->
                    <div id="wpsai-subtab-worklogs" class="wpsai-subtab-content" style="display: none;">
                        <div class="wpsai-flex-row">
                            <!-- Timeline nhật ký -->
                            <div class="wpsai-card" style="flex: 1.5; min-width: 300px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                    <h2 style="margin: 0;"><span class="dashicons dashicons-welcome-write-blog" style="color: var(--wpsai-primary);"></span> <?php esc_html_e( 'Nhật Ký Các Công Việc Đã Làm', 'wp-acf-smart-importer' ); ?></h2>
                                    <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-doc-export-changelog-btn">
                                        <span class="dashicons dashicons-media-text"></span> <?php esc_html_e( 'Xem Changelog Markdown', 'wp-acf-smart-importer' ); ?>
                                    </button>
                                </div>
                                
                                <!-- Khung hiển thị timeline -->
                                <div id="wpsai-doc-logs-timeline" style="margin-top: 20px; position: relative; padding-left: 20px; border-left: 2px solid var(--wpsai-border-color); max-height: 550px; overflow-y: auto; padding-right: 10px;">
                                    <!-- Render động -->
                                    <p style="color: var(--wpsai-text-muted); font-style: italic;"><?php esc_html_e( 'Chưa có nhật ký công việc nào được tạo. Vui lòng thêm công việc đầu tiên ở bảng bên cạnh!', 'wp-acf-smart-importer' ); ?></p>
                                </div>
                            </div>

                            <!-- Thêm log mới -->
                            <div class="wpsai-card" style="flex: 1; min-width: 250px;">
                                <h2><span class="dashicons dashicons-plus-alt" style="color: var(--wpsai-success);"></span> <?php esc_html_e( 'Thêm Công Việc Mới', 'wp-acf-smart-importer' ); ?></h2>
                                <p class="description-p"><?php esc_html_e( 'Ghi chép công việc vừa thực hiện hoặc quét tự động từ lịch sử Git.', 'wp-acf-smart-importer' ); ?></p>
                                
                                <div style="margin-bottom: 15px; display: flex; gap: 8px; flex-wrap: wrap;">
                                    <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-doc-git-load-btn" style="width: 100%; text-align: center; justify-content: center; background: #f0f9ff; border-color: #bae6fd; color: #0369a1; margin: 0;">
                                        <span class="dashicons dashicons-networking"></span> <?php esc_html_e( 'Đọc Lịch Sử Git Commit', 'wp-acf-smart-importer' ); ?>
                                    </button>
                                </div>

                                <div class="wpsai-settings-form" id="wpsai-doc-new-log-form">
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-log-title"><strong><?php esc_html_e( 'Tên công việc / Tính năng đã làm:', 'wp-acf-smart-importer' ); ?> <span style="color:red;">*</span></strong></label>
                                        <input type="text" id="wpsai-log-title" class="large-text" placeholder="Ví dụ: Thêm hàm export ZIP và tải ảnh">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-log-date"><strong><?php esc_html_e( 'Ngày hoàn thành:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="date" id="wpsai-log-date" class="large-text" value="<?php echo date('Y-m-d'); ?>">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-log-dev"><strong><?php esc_html_e( 'Lập trình viên làm:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="text" id="wpsai-log-dev" class="large-text" placeholder="Nguyễn Văn A">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-log-files"><strong><?php esc_html_e( 'Các file chỉnh sửa (cách nhau bằng dấu phẩy):', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <input type="text" id="wpsai-log-files" class="large-text" placeholder="class-importer-admin.php, admin-style.css">
                                    </div>
                                    <div class="wpsai-form-group">
                                        <label for="wpsai-log-desc"><strong><?php esc_html_e( 'Mô tả chi tiết kỹ thuật:', 'wp-acf-smart-importer' ); ?></strong></label>
                                        <textarea id="wpsai-log-desc" class="large-text" rows="4" placeholder="Ví dụ: Triển khai các hàm xử lý AJAX, kiểm tra quyền bảo mật..."></textarea>
                                    </div>
                                    
                                    <div style="margin-top: 15px;">
                                        <button type="button" class="wpsai-btn wpsai-btn-success" id="wpsai-doc-add-log-btn" style="width: 100%; justify-content: center;">
                                            <span class="dashicons dashicons-insert"></span> <?php esc_html_e( 'Thêm Công Việc Vào Nhật Ký', 'wp-acf-smart-importer' ); ?>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- SUBTAB 3: THƯ VIỆN UI COMPONENTS -->
                    <div id="wpsai-subtab-ui-library" class="wpsai-subtab-content" style="display: none;">
                        <div class="wpsai-flex-row" style="align-items: stretch;">
                            <!-- Sidebar danh sách Components -->
                            <div class="wpsai-card" style="flex: 1; min-width: 250px; display: flex; flex-direction: column; max-height: 700px; overflow-y: auto;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                                    <h2 style="margin: 0; font-size: 16px;"><span class="dashicons dashicons-layout" style="color: var(--wpsai-primary);"></span> <?php esc_html_e( 'Danh Sách UI Components', 'wp-acf-smart-importer' ); ?></h2>
                                    <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-comp-add-new-btn" style="padding: 4px 10px; font-size: 12px; margin: 0;">
                                        <span class="dashicons dashicons-plus"></span> <?php esc_html_e( 'Thêm Mới', 'wp-acf-smart-importer' ); ?>
                                    </button>
                                </div>
                                
                                <div id="wpsai-comp-list-container" style="display: flex; flex-direction: column; gap: 10px; flex: 1;">
                                    <!-- Render động -->
                                    <p style="color: var(--wpsai-text-muted); font-style: italic; font-size: 13px;"><?php esc_html_e( 'Chưa có component nào được tạo.', 'wp-acf-smart-importer' ); ?></p>
                                </div>
                            </div>

                            <!-- Workspace Chỉnh sửa & Sandbox Live Preview -->
                            <div class="wpsai-card" id="wpsai-comp-editor-panel" style="flex: 2.2; min-width: 320px; display: none;">
                                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--wpsai-border-color); padding-bottom: 12px; margin-bottom: 20px;">
                                    <h2 style="margin: 0;" id="wpsai-comp-panel-title"><span class="dashicons dashicons-edit" style="color: var(--wpsai-secondary);"></span> <?php esc_html_e( 'Biên Tập Component', 'wp-acf-smart-importer' ); ?></h2>
                                    <div style="display: flex; gap: 8px;">
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-comp-delete-btn" style="border-color: #fca5a5; color: #dc2626; margin: 0;">
                                            <span class="dashicons dashicons-trash"></span> <?php esc_html_e( 'Xóa', 'wp-acf-smart-importer' ); ?>
                                        </button>
                                        <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-comp-save-btn" style="margin: 0;">
                                            <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Lưu Component', 'wp-acf-smart-importer' ); ?>
                                        </button>
                                    </div>
                                </div>

                                <div class="wpsai-settings-form">
                                    <input type="hidden" id="wpsai-comp-id" value="">
                                    <div class="wpsai-flex-row" style="gap: 15px;">
                                        <div class="wpsai-form-group">
                                            <label for="wpsai-comp-name"><strong><?php esc_html_e( 'Tên Component:', 'wp-acf-smart-importer' ); ?></strong></label>
                                            <input type="text" id="wpsai-comp-name" class="large-text" placeholder="Ví dụ: Bảng dữ liệu Grid View">
                                        </div>
                                        <div class="wpsai-form-group">
                                            <label for="wpsai-comp-category"><strong><?php esc_html_e( 'Danh mục:', 'wp-acf-smart-importer' ); ?></strong></label>
                                            <select id="wpsai-comp-category" style="padding: 8px 12px; border-radius: 6px; border: 1px solid var(--wpsai-border-color); margin-top: 5px; display: block; width: 100%;">
                                                <option value="Table"><?php esc_html_e( 'Bảng biểu (Table)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="Form"><?php esc_html_e( 'Biểu mẫu (Form & Inputs)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="Modal"><?php esc_html_e( 'Hộp thoại (Modal & Dialog)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="Progress"><?php esc_html_e( 'Tiến trình (Progress & Loading)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="Navigation"><?php esc_html_e( 'Điều hướng (Tab & Menu)', 'wp-acf-smart-importer' ); ?></option>
                                                <option value="Other" selected><?php esc_html_e( 'Khác (Other)', 'wp-acf-smart-importer' ); ?></option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- Code Editor Tabs -->
                                    <div style="margin-top: 15px;">
                                        <div class="wpsai-comp-code-tabs" style="display: flex; gap: 4px; background: #e2e8f0; padding: 4px; border-radius: 8px; width: fit-content; margin-bottom: 12px;">
                                            <button class="wpsai-comp-code-tab-btn active" data-codetab="html" style="border: none; background: none; font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: 6px; cursor: pointer; color: #475569; transition: all 0.2s ease;">HTML</button>
                                            <button class="wpsai-comp-code-tab-btn" data-codetab="css" style="border: none; background: none; font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: 6px; cursor: pointer; color: #475569; transition: all 0.2s ease;">CSS</button>
                                            <button class="wpsai-comp-code-tab-btn" data-codetab="js" style="border: none; background: none; font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: 6px; cursor: pointer; color: #475569; transition: all 0.2s ease;">Javascript</button>
                                            <button class="wpsai-comp-code-tab-btn" data-codetab="preview" style="border: none; background: none; font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: 6px; cursor: pointer; color: #475569; transition: all 0.2s ease; display: flex; align-items: center; gap: 4px;">
                                                <span class="dashicons dashicons-visibility" style="font-size: 14px; width: 14px; height: 14px; margin-top: -2px;"></span> Preview Sandbox
                                            </button>
                                        </div>

                                        <!-- HTML Area -->
                                        <div id="wpsai-code-area-html" class="wpsai-code-tab-content active">
                                            <textarea id="wpsai-comp-html" class="large-text" rows="10" style="font-family: monospace !important; font-size: 13px !important; background: #1e293b; color: #f8fafc;" placeholder="Nhập mã nguồn HTML ở đây..."></textarea>
                                        </div>

                                        <!-- CSS Area -->
                                        <div id="wpsai-code-area-css" class="wpsai-code-tab-content" style="display: none;">
                                            <textarea id="wpsai-comp-css" class="large-text" rows="10" style="font-family: monospace !important; font-size: 13px !important; background: #1e293b; color: #f8fafc;" placeholder="Nhập mã nguồn CSS ở đây..."></textarea>
                                        </div>

                                        <!-- JS Area -->
                                        <div id="wpsai-code-area-js" class="wpsai-code-tab-content" style="display: none;">
                                            <textarea id="wpsai-comp-js" class="large-text" rows="10" style="font-family: monospace !important; font-size: 13px !important; background: #1e293b; color: #f8fafc;" placeholder="Nhập mã nguồn Javascript ở đây..."></textarea>
                                        </div>

                                        <!-- Preview Sandbox -->
                                        <div id="wpsai-code-area-preview" class="wpsai-code-tab-content" style="display: none;">
                                            <div style="background: #fff; border: 2px dashed #cbd5e1; border-radius: 8px; overflow: hidden; height: 250px;">
                                                <iframe id="wpsai-comp-sandbox-iframe" style="width: 100%; height: 100%; border: none; background: #ffffff;"></iframe>
                                            </div>
                                            <p class="description" style="margin-top: 6px;"><span class="dashicons dashicons-info" style="font-size: 13px; width: 13px; height: 13px;"></span> <?php esc_html_e( 'Nhấp chuột vào tab Preview Sandbox bất kỳ lúc nào để biên dịch và chạy tương tác trực tiếp component.', 'wp-acf-smart-importer' ); ?></p>
                                        </div>
                                    </div>

                                    <!-- Copy actions -->
                                    <div style="margin-top: 15px; display: flex; gap: 8px; flex-wrap: wrap;">
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-copy-html-btn" style="font-size: 12px; padding: 6px 12px; margin: 0;"><span class="dashicons dashicons-editor-code"></span> Copy HTML</button>
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-copy-css-btn" style="font-size: 12px; padding: 6px 12px; margin: 0;"><span class="dashicons dashicons-editor-code"></span> Copy CSS</button>
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-copy-js-btn" style="font-size: 12px; padding: 6px 12px; margin: 0;"><span class="dashicons dashicons-editor-code"></span> Copy JS</button>
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-copy-all-btn" style="font-size: 12px; padding: 6px 12px; background: #eef2ff; color: var(--wpsai-primary); border-color: #c7d2fe; margin: 0;"><span class="dashicons dashicons-admin-page"></span> Copy Toàn Bộ</button>
                                    </div>

                                    <!-- Mô tả bằng Markdown & AI Assistant -->
                                    <div class="wpsai-form-group" style="margin-top: 20px;">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                            <label for="wpsai-comp-desc"><strong><?php esc_html_e( 'Hướng dẫn sử dụng & Mô tả kỹ thuật:', 'wp-acf-smart-importer' ); ?></strong></label>
                                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-comp-ai-desc-btn" style="padding: 4px 10px; font-size: 12px; background: #fdf2f8; border-color: #fbcfe8; color: #db2777; margin: 0;">
                                                <span class="dashicons dashicons-admin-customizer"></span> <?php esc_html_e( 'AI Tự Động Viết Mô Tả', 'wp-acf-smart-importer' ); ?>
                                            </button>
                                        </div>
                                        <textarea id="wpsai-comp-desc" class="large-text" rows="5" placeholder="Nhập tài liệu hướng dẫn nhúng, class CSS cấu hình hoặc các lưu ý khác (định dạng Markdown)..."></textarea>
                                    </div>
                                </div>
                            </div>

                            <!-- Panel khi chưa chọn gì -->
                            <div class="wpsai-card" id="wpsai-comp-empty-panel" style="flex: 2.2; min-width: 320px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fafafb; min-height: 400px;">
                                <span class="dashicons dashicons-layout" style="font-size: 64px; width: 64px; height: 64px; color: #cbd5e1;"></span>
                                <h3 style="color: #64748b; margin-top: 15px; margin-bottom: 6px;"><?php esc_html_e( 'Chưa chọn UI Component', 'wp-acf-smart-importer' ); ?></h3>
                                <p style="color: #94a3b8; font-size: 13px; max-width: 300px; text-align: center; margin: 0;"><?php esc_html_e( 'Hãy bấm vào một component bên danh sách trái để xem chi tiết và sửa code, hoặc bấm "Thêm Mới" để tạo linh kiện mới.', 'wp-acf-smart-importer' ); ?></p>
                            </div>
                        </div>
                    </div>

                    <!-- SUBTAB 4: GHI CHÚ KỸ THUẬT -->
                    <div id="wpsai-subtab-tech-notes" class="wpsai-subtab-content" style="display: none;">
                        <div class="wpsai-flex-row">
                            <div class="wpsai-card" style="flex: 2; min-width: 300px;">
                                <h2><span class="dashicons dashicons-edit" style="color: var(--wpsai-primary);"></span> <?php esc_html_e( 'Ghi Chú Kỹ Thuật Dự Án (Markdown)', 'wp-acf-smart-importer' ); ?></h2>
                                <p class="description-p"><?php esc_html_e( 'Lưu lại các thông tin như cấu trúc API, Webhooks, cấu hình ACF tùy chỉnh hoặc tài khoản sandbox phục vụ phát triển lâu dài.', 'wp-acf-smart-importer' ); ?></p>
                                
                                <div style="margin-top: 15px;">
                                    <textarea id="wpsai-doc-notes-area" class="large-text" rows="15" style="font-family: monospace !important; font-size: 13px !important;" placeholder="Sử dụng cú pháp Markdown để viết ghi chú kỹ thuật..."></textarea>
                                </div>
                                <div style="margin-top: 20px;">
                                    <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-doc-save-notes-btn">
                                        <span class="dashicons dashicons-saved"></span> <?php esc_html_e( 'Lưu Ghi Chú Kỹ Thuật', 'wp-acf-smart-importer' ); ?>
                                    </button>
                                    <span id="wpsai-doc-notes-msg" class="wpsai-status-msg"></span>
                                </div>
                            </div>

                            <div class="wpsai-card" style="flex: 1; min-width: 250px; background: #fafafb;">
                                <h2><span class="dashicons dashicons-editor-help" style="color: var(--wpsai-secondary);"></span> <?php esc_html_e( 'Gợi ý Ghi Chép', 'wp-acf-smart-importer' ); ?></h2>
                                <div style="font-size: 13px; line-height: 1.6; color: var(--wpsai-text-muted);">
                                    <p>Bạn nên ghi lại các thông tin sau để dự án sau bàn giao hoặc làm lại nhanh hơn:</p>
                                    <ul style="list-style-type: disc; margin-left: 20px; display: flex; flex-direction: column; gap: 8px;">
                                        <li><strong>Thông tin Hosting/Server</strong>: Cấu hình đặc thù, phiên bản PHP tối thiểu, dung lượng upload tối đa.</li>
                                        <li><strong>Danh sách API Endpoints</strong>: Domain test, headers, cấu trúc request/response chính.</li>
                                        <li><strong>Các hook/filters custom</strong>: Khai báo trong file <code>functions.php</code> tác động đến ACF.</li>
                                        <li><strong>Mã màu thiết kế</strong>: Mã màu mã HEX chủ đạo của thương hiệu.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- SUBTAB 5: ĐỒNG BỘ & NHẬP XUẤT -->
                    <div id="wpsai-subtab-sync-export" class="wpsai-subtab-content" style="display: none;">
                        <div class="wpsai-flex-row">
                            <!-- Quản lý file JSON vật lý -->
                            <div class="wpsai-card" style="flex: 1; min-width: 250px;">
                                <h2><span class="dashicons dashicons-category" style="color: var(--wpsai-primary);"></span> <?php esc_html_e( 'Trạng Thái Đồng Bộ Tệp Cục Bộ', 'wp-acf-smart-importer' ); ?></h2>
                                <p class="description-p"><?php esc_html_e( 'Quản lý việc đồng bộ dữ liệu giữa Cơ sở dữ liệu của WordPress và file lưu trữ trên ổ đĩa dự án.', 'wp-acf-smart-importer' ); ?></p>
                                
                                <div style="background: #f8fafc; border: 1px solid var(--wpsai-border-color); border-radius: 8px; padding: 15px; margin-top: 15px;">
                                    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 12px;">
                                        <span class="dashicons dashicons-portfolio" style="color: var(--wpsai-primary);"></span>
                                        <div>
                                            <strong style="display: block; font-size: 14px;">project-docs.json</strong>
                                            <span style="font-size: 12px; color: var(--wpsai-text-muted); display: block; word-break: break-all;" id="wpsai-sync-file-path">wp-content/plugins/wp-acf-smart-importer/docs/project-docs.json</span>
                                        </div>
                                    </div>
                                    <div style="border-top: 1px solid #e2e8f0; padding-top: 10px; margin-top: 10px;">
                                        <div style="display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px;">
                                            <span>Trạng thái tệp:</span>
                                            <span id="wpsai-sync-status" style="font-weight: bold; color: #b45309;">Đang kiểm tra...</span>
                                        </div>
                                        <div style="display: flex; justify-content: space-between; font-size: 13px;">
                                            <span>Lần đồng bộ cuối:</span>
                                            <span id="wpsai-sync-last-time" style="font-family: monospace;">-</span>
                                        </div>
                                    </div>
                                </div>

                                <div style="margin-top: 20px; display: flex; flex-direction: column; gap: 10px;">
                                    <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-sync-db-to-file-btn" style="justify-content: center; margin: 0;">
                                        <span class="dashicons dashicons-upload"></span> <?php esc_html_e( 'Đồng bộ: Ghi đè DB ra File JSON', 'wp-acf-smart-importer' ); ?>
                                    </button>
                                    <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-sync-file-to-db-btn" style="justify-content: center; border-color: #bae6fd; background: #f0f9ff; color: #0369a1; margin: 0;">
                                        <span class="dashicons dashicons-download"></span> <?php esc_html_e( 'Nạp lại: Ghi đè File JSON vào DB', 'wp-acf-smart-importer' ); ?>
                                    </button>
                                </div>
                            </div>

                            <!-- Xuất Markdown & JSON -->
                            <div class="wpsai-card" style="flex: 1; min-width: 250px;">
                                <h2><span class="dashicons dashicons-share" style="color: var(--wpsai-secondary);"></span> <?php esc_html_e( 'Xuất Bản & Di Chuyển Tài Liệu', 'wp-acf-smart-importer' ); ?></h2>
                                <p class="description-p"><?php esc_html_e( 'Xuất tài liệu ra các định dạng chuẩn hoặc tải tệp backup để di chuyển sang dự án mới.', 'wp-acf-smart-importer' ); ?></p>
                                
                                <div style="display: flex; flex-direction: column; gap: 15px; margin-top: 20px;">
                                    <div style="border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px;">
                                        <strong style="display: block; font-size: 14px; margin-bottom: 6px;"><span class="dashicons dashicons-media-text" style="color: #059669; vertical-align: middle;"></span> Xuất File Báo Cáo Markdown</strong>
                                        <p style="font-size: 12px; color: var(--wpsai-text-muted); margin: 0 0 12px 0;"><?php esc_html_e( 'Tạo một file Markdown hoàn chỉnh chứa toàn bộ thông tin dự án, nhật ký công việc và thư viện source code component để đưa vào thư mục lưu trữ Git.', 'wp-acf-smart-importer' ); ?></p>
                                        <button type="button" class="wpsai-btn wpsai-btn-success" id="wpsai-export-markdown-btn" style="margin: 0;">
                                            <span class="dashicons dashicons-download"></span> <?php esc_html_e( 'Xuất và Tải File .md', 'wp-acf-smart-importer' ); ?>
                                        </button>
                                    </div>

                                    <div style="border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px;">
                                        <strong style="display: block; font-size: 14px; margin-bottom: 6px;"><span class="dashicons dashicons-backup" style="color: #6366f1; vertical-align: middle;"></span> Nhập Tài Liệu Dự Án Khác (JSON Backup)</strong>
                                        <p style="font-size: 12px; color: var(--wpsai-text-muted); margin: 0 0 12px 0;"><?php esc_html_e( 'Tải lên một file project-docs.json được xuất từ dự án khác để nhập và sao chép nhanh các components.', 'wp-acf-smart-importer' ); ?></p>
                                        <input type="file" id="wpsai-import-json-file" accept=".json" style="display: none;">
                                        <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-import-json-btn" style="margin: 0;">
                                            <span class="dashicons dashicons-upload"></span> <?php esc_html_e( 'Chọn File JSON và Nhập Dữ Liệu', 'wp-acf-smart-importer' ); ?>
                                        </button>
                                        <span id="wpsai-import-json-msg" style="display: block; margin-top: 6px; font-size: 12px; font-weight: 600;"></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Tab 12: Kho Dữ Liệu Mẫu (Snapshot Repository) -->
                <section id="wpsai-tab-snapshot-repo" class="wpsai-tab-content">
                    <!-- Header -->
                    <div class="wpsai-card" style="background: linear-gradient(135deg, #0c4a6e 0%, #155e75 50%, #164e63 100%); color: #fff; margin-bottom: 24px; border: none; position: relative; overflow: hidden;">
                        <div style="position: relative; z-index: 2;">
                            <h2 style="color: #fff; font-size: 22px; margin-bottom: 8px;"><span class="dashicons dashicons-database" style="font-size: 24px; width: 24px; height: 24px; color: #67e8f9;"></span> <?php esc_html_e( 'Kho Lưu Trữ Dữ Liệu Mẫu', 'wp-acf-smart-importer' ); ?></h2>
                            <p style="color: rgba(255, 255, 255, 0.85); margin: 0; font-size: 14px;"><?php esc_html_e( 'Quét, lưu trữ và quản lý snapshot toàn bộ dữ liệu bài viết (bao gồm ACF, Taxonomy). Tái sử dụng dữ liệu mẫu bất kỳ lúc nào.', 'wp-acf-smart-importer' ); ?></p>
                        </div>
                        <div style="position: absolute; right: -50px; bottom: -50px; opacity: 0.1; font-size: 180px; width: 180px; height: 180px;" class="dashicons dashicons-database"></div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px;">
                        <!-- Card: Quét Dữ Liệu -->
                        <div class="wpsai-card" style="margin: 0;">
                            <h3 style="margin-top: 0;"><span class="dashicons dashicons-search" style="color: var(--wpsai-primary);"></span> <?php esc_html_e( 'Quét Dữ Liệu Bài Viết', 'wp-acf-smart-importer' ); ?></h3>
                            <p style="color: #64748b; font-size: 13px;"><?php esc_html_e( 'Chọn Post Type muốn quét, hệ thống sẽ thu thập toàn bộ bài viết kèm ACF & Taxonomy.', 'wp-acf-smart-importer' ); ?></p>

                            <div style="margin-bottom: 16px;">
                                <label style="display: block; font-weight: 600; font-size: 13px; margin-bottom: 6px; color: #334155;"><?php esc_html_e( 'Post Type:', 'wp-acf-smart-importer' ); ?></label>
                                <select id="wpsai-snap-post-type" class="wpsai-input" style="width: 100%;">
                                    <option value=""><?php esc_html_e( '-- Đang tải danh sách --', 'wp-acf-smart-importer' ); ?></option>
                                </select>
                            </div>

                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                                <div>
                                    <label style="display: block; font-weight: 600; font-size: 13px; margin-bottom: 6px; color: #334155;"><?php esc_html_e( 'Lọc Taxonomy (tùy chọn):', 'wp-acf-smart-importer' ); ?></label>
                                    <select id="wpsai-snap-taxonomy" class="wpsai-input" style="width: 100%;">
                                        <option value=""><?php esc_html_e( '-- Không lọc --', 'wp-acf-smart-importer' ); ?></option>
                                    </select>
                                </div>
                                <div>
                                    <label style="display: block; font-weight: 600; font-size: 13px; margin-bottom: 6px; color: #334155;"><?php esc_html_e( 'Chuyên mục:', 'wp-acf-smart-importer' ); ?></label>
                                    <select id="wpsai-snap-term" class="wpsai-input" style="width: 100%;" disabled>
                                        <option value=""><?php esc_html_e( '-- Chọn Taxonomy trước --', 'wp-acf-smart-importer' ); ?></option>
                                    </select>
                                </div>
                            </div>

                            <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-snap-scan-btn" style="width: 100%;">
                                <span class="dashicons dashicons-search"></span> <?php esc_html_e( 'Quét Toàn Bộ Dữ Liệu', 'wp-acf-smart-importer' ); ?>
                            </button>

                            <!-- Thống kê sau quét -->
                            <div id="wpsai-snap-scan-stats" style="display: none; margin-top: 16px; padding: 16px; background: linear-gradient(135deg, #ecfdf5, #f0fdf4); border-radius: 10px; border: 1px solid #a7f3d0;">
                                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; text-align: center;">
                                    <div>
                                        <div style="font-size: 28px; font-weight: 700; color: #059669;" id="wpsai-snap-stat-posts">0</div>
                                        <div style="font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;"><?php esc_html_e( 'Bài viết', 'wp-acf-smart-importer' ); ?></div>
                                    </div>
                                    <div>
                                        <div style="font-size: 28px; font-weight: 700; color: #2563eb;" id="wpsai-snap-stat-fields">0</div>
                                        <div style="font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;"><?php esc_html_e( 'Trường dữ liệu', 'wp-acf-smart-importer' ); ?></div>
                                    </div>
                                    <div>
                                        <div style="font-size: 28px; font-weight: 700; color: #7c3aed;" id="wpsai-snap-stat-size">0 KB</div>
                                        <div style="font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;"><?php esc_html_e( 'Dung lượng', 'wp-acf-smart-importer' ); ?></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Card: Xem Trước & Lưu -->
                        <div class="wpsai-card" style="margin: 0;">
                            <h3 style="margin-top: 0;"><span class="dashicons dashicons-visibility" style="color: #7c3aed;"></span> <?php esc_html_e( 'Xem Trước & Lưu Snapshot', 'wp-acf-smart-importer' ); ?></h3>
                            <p style="color: #64748b; font-size: 13px;"><?php esc_html_e( 'Xem trước dữ liệu quét được, đặt tên và lưu vào kho.', 'wp-acf-smart-importer' ); ?></p>

                            <div id="wpsai-snap-preview-empty" style="text-align: center; padding: 40px 20px; color: #94a3b8;">
                                <span class="dashicons dashicons-database-view" style="font-size: 48px; width: 48px; height: 48px; display: block; margin: 0 auto 12px;"></span>
                                <p style="margin: 0; font-size: 14px;"><?php esc_html_e( 'Chưa có dữ liệu. Hãy chọn Post Type và bấm Quét.', 'wp-acf-smart-importer' ); ?></p>
                            </div>

                            <div id="wpsai-snap-preview-content" style="display: none;">
                                <div style="max-height: 260px; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 16px;">
                                    <table class="widefat striped" style="margin: 0; font-size: 12px;" id="wpsai-snap-preview-table">
                                        <thead><tr id="wpsai-snap-preview-thead"></tr></thead>
                                        <tbody id="wpsai-snap-preview-tbody"></tbody>
                                    </table>
                                </div>
                                <div style="display: flex; gap: 12px; align-items: flex-end;">
                                    <div style="flex: 1;">
                                        <label style="display: block; font-weight: 600; font-size: 13px; margin-bottom: 6px; color: #334155;"><?php esc_html_e( 'Tên Snapshot:', 'wp-acf-smart-importer' ); ?></label>
                                        <input type="text" id="wpsai-snap-name" class="wpsai-input" style="width: 100%;" placeholder="<?php esc_attr_e( 'Ví dụ: Dữ liệu sản phẩm tháng 8', 'wp-acf-smart-importer' ); ?>">
                                    </div>
                                    <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-snap-save-btn" style="white-space: nowrap;">
                                        <span class="dashicons dashicons-database-add"></span> <?php esc_html_e( 'Lưu Vào Kho', 'wp-acf-smart-importer' ); ?>
                                    </button>
                                </div>
                                <div id="wpsai-snap-save-msg" style="margin-top: 8px; font-size: 13px; font-weight: 600;"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Card: Cây Kho Dữ Liệu Mẫu (Tree Hierarchy View) -->
                    <div class="wpsai-card" style="margin-bottom: 24px; border: 2px solid #38bdf8; background: #f0f9ff;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div>
                                <h3 style="margin: 0; color: #0369a1;"><span class="dashicons dashicons-category" style="color: #0284c7;"></span> <?php esc_html_e( 'Cây Phân Loại Kho Dữ Liệu (Tree Repository)', 'wp-acf-smart-importer' ); ?></h3>
                                <p style="color: #0369a1; font-size: 13px; margin: 4px 0 0 0;"><?php esc_html_e( 'Duyệt theo Post Type, Chuyên mục hoặc Luồng xử lý. Mỗi nút được phân mảnh (chunk) riêng biệt giúp ứng dụng chạy siêu nhanh.', 'wp-acf-smart-importer' ); ?></p>
                            </div>
                            <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-tree-refresh-btn" style="margin: 0;">
                                <span class="dashicons dashicons-update"></span> <?php esc_html_e( 'Cập Nhật Cây Chỉ Mục', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>

                        <!-- Vùng Cây Tương Tác -->
                        <div id="wpsai-tree-view-wrapper" style="background: #ffffff; border: 1px solid #bae6fd; border-radius: 8px; padding: 16px; max-height: 400px; overflow-y: auto;">
                            <div id="wpsai-tree-loading" style="text-align: center; color: #0284c7; padding: 20px;">
                                <span class="dashicons dashicons-update wpsai-spin" style="font-size: 24px; width: 24px; height: 24px;"></span>
                                <p style="margin: 8px 0 0 0; font-size: 13px;"><?php esc_html_e( 'Đang tải cây phân cấp dữ liệu...', 'wp-acf-smart-importer' ); ?></p>
                            </div>
                            <ul id="wpsai-tree-root" style="list-style: none; margin: 0; padding: 0; display: none;"></ul>
                        </div>
                    </div>
                    <div class="wpsai-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <h3 style="margin: 0;"><span class="dashicons dashicons-archive" style="color: #0ea5e9;"></span> <?php esc_html_e( 'Kho Lưu Trữ Snapshot', 'wp-acf-smart-importer' ); ?></h3>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-snap-refresh-btn" style="margin: 0; padding: 6px 14px; font-size: 12px;">
                                <span class="dashicons dashicons-update"></span> <?php esc_html_e( 'Làm Mới', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>

                        <div id="wpsai-snap-list-empty" style="text-align: center; padding: 40px 20px; color: #94a3b8;">
                            <span class="dashicons dashicons-database-remove" style="font-size: 48px; width: 48px; height: 48px; display: block; margin: 0 auto 12px;"></span>
                            <p style="margin: 0; font-size: 14px;"><?php esc_html_e( 'Chưa có snapshot nào trong kho. Hãy quét và lưu dữ liệu trước.', 'wp-acf-smart-importer' ); ?></p>
                        </div>

                        <div id="wpsai-snap-list-content" style="display: none;">
                            <div style="overflow-x: auto;">
                                <table class="widefat striped" style="margin: 0; font-size: 13px;">
                                    <thead>
                                        <tr>
                                            <th style="width: 30px;">#</th>
                                            <th><?php esc_html_e( 'Tên Snapshot', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 120px;"><?php esc_html_e( 'Post Type', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 90px; text-align: center;"><?php esc_html_e( 'Bài viết', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 90px;"><?php esc_html_e( 'Dung lượng', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 150px;"><?php esc_html_e( 'Ngày tạo', 'wp-acf-smart-importer' ); ?></th>
                                            <th style="width: 220px; text-align: center;"><?php esc_html_e( 'Hành Động', 'wp-acf-smart-importer' ); ?></th>
                                        </tr>
                                    </thead>
                                    <tbody id="wpsai-snap-list-tbody"></tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Card: Chi Tiết Snapshot (ẩn mặc định) -->
                    <div class="wpsai-card" id="wpsai-snap-detail-card" style="display: none;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <h3 style="margin: 0;"><span class="dashicons dashicons-media-text" style="color: #2563eb;"></span> <?php esc_html_e( 'Chi Tiết Snapshot:', 'wp-acf-smart-importer' ); ?> <span id="wpsai-snap-detail-name" style="color: var(--wpsai-primary);"></span></h3>
                            <button type="button" class="wpsai-btn-remove" id="wpsai-snap-detail-close" style="font-size: 24px; font-weight: 300; padding: 0 8px;">&times;</button>
                        </div>

                        <div style="margin-bottom: 16px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                            <select id="wpsai-snap-restore-mode" class="wpsai-input" style="width: auto;">
                                <option value="create_new"><?php esc_html_e( 'Tạo bài viết mới', 'wp-acf-smart-importer' ); ?></option>
                                <option value="update_existing"><?php esc_html_e( 'Ghi đè bài viết cũ (theo post_id)', 'wp-acf-smart-importer' ); ?></option>
                            </select>
                            <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-snap-restore-btn" style="margin: 0;">
                                <span class="dashicons dashicons-backup"></span> <?php esc_html_e( 'Khôi Phục Tất Cả', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-snap-export-json-btn" style="margin: 0;">
                                <span class="dashicons dashicons-download"></span> <?php esc_html_e( 'Xuất JSON', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>

                        <!-- Progress bar khôi phục -->
                        <div id="wpsai-snap-restore-progress" style="display: none; margin-bottom: 16px;">
                            <div style="background: #e2e8f0; border-radius: 8px; overflow: hidden; height: 28px; position: relative;">
                                <div id="wpsai-snap-restore-bar" style="height: 100%; background: linear-gradient(90deg, #2563eb, #7c3aed); border-radius: 8px; transition: width 0.3s ease; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 600; font-size: 12px; min-width: 40px;">0%</div>
                            </div>
                            <div id="wpsai-snap-restore-log" style="margin-top: 8px; max-height: 150px; overflow-y: auto; font-size: 12px; padding: 8px 12px; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;"></div>
                        </div>

                        <div style="max-height: 500px; overflow: auto; border: 1px solid #e2e8f0; border-radius: 8px;">
                            <table class="widefat striped" style="margin: 0; font-size: 12px;" id="wpsai-snap-detail-table">
                                <thead><tr id="wpsai-snap-detail-thead"></tr></thead>
                                <tbody id="wpsai-snap-detail-tbody"></tbody>
                            </table>
                        </div>
                    </div>
                </section>

                <!-- Modal hiển thị Changelog Markdown -->
                <div id="wpsai-changelog-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); z-index: 99999; justify-content: center; align-items: center; padding: 20px;">
                    <div style="background: #ffffff; border-radius: 12px; width: 100%; max-width: 700px; max-height: 90vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);">
                        <div style="padding: 20px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; background: #f8fafc;">
                            <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: #0f172a;"><span class="dashicons dashicons-welcome-write-blog" style="color: var(--wpsai-primary); vertical-align: middle;"></span> <?php esc_html_e( 'Xem Nhật Ký Dạng Markdown', 'wp-acf-smart-importer' ); ?></h3>
                            <button type="button" class="wpsai-btn-remove" id="wpsai-changelog-modal-close" style="font-size: 24px; font-weight: 300; margin: 0; padding: 0 6px;">&times;</button>
                        </div>
                        <div style="padding: 20px; flex: 1; overflow-y: auto;">
                            <textarea id="wpsai-changelog-markdown-text" class="large-text" rows="15" style="font-family: monospace !important; font-size: 12px !important; width: 100%; height: 100%; padding: 12px; border-radius: 6px; border: 1px solid #cbd5e1; background: #f1f5f9; box-sizing: border-box;" readonly></textarea>
                        </div>
                        <div style="padding: 15px 20px; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end; gap: 10px; background: #f8fafc;">
                            <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-changelog-modal-copy-btn" style="margin: 0;">
                                <span class="dashicons dashicons-admin-page"></span> <?php esc_html_e( 'Sao Chép Nội Dung', 'wp-acf-smart-importer' ); ?>
                            </button>
                            <button type="button" class="wpsai-btn wpsai-btn-primary" id="wpsai-changelog-modal-ok-btn" style="margin: 0;">
                                <?php esc_html_e( 'Đóng', 'wp-acf-smart-importer' ); ?>
                            </button>
                        </div>
                    </div>
                </div>

            </main>
        </div>
        <?php
    }
}
