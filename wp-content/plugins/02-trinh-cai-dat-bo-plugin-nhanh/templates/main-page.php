<?php
/**
 * WDM Quick Installer — Main Admin Page Template
 * Giao diện 3 cột: Favorites + Search | Queue Console | Installed Table
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

$favorites = WDM_QI_DB::get_favorites();
?>
<div class="wdm-qi-wrap">

  <!-- ==========================================
       HEADER
       ========================================== -->
  <div class="wdm-qi-header">
    <div class="wdm-qi-header-left">
      <div class="wdm-qi-brand-icon">
        <i data-lucide="zap"></i>
      </div>
      <div>
        <h1 class="wdm-qi-title">Quick Stack Installer</h1>
        <p class="wdm-qi-subtitle">Cài đặt hàng loạt plugin WordPress chỉ với một click chuột</p>
      </div>
    </div>
    <div class="wdm-qi-header-stats" id="wdm-qi-header-stats">
      <div class="wdm-qi-stat-badge" id="wdm-qi-stat-total">
        <i data-lucide="layers"></i>
        <span id="wdm-qi-stat-total-val">—</span> đã cài
      </div>
      <div class="wdm-qi-stat-badge active" id="wdm-qi-stat-active">
        <i data-lucide="check-circle"></i>
        <span id="wdm-qi-stat-active-val">—</span> đang bật
      </div>
    </div>
  </div>

  <!-- ==========================================
       MAIN GRID: 3 COLUMNS
       ========================================== -->
  <div class="wdm-qi-grid">

    <!-- =========================================
         CỘT 1 (TRÁI): FAVORITES + WP.ORG SEARCH
         ========================================= -->
    <aside class="wdm-qi-col wdm-qi-col-left">

      <!-- Khu vực 1: Plugin Hay Dùng (Favorites) -->
      <div class="wdm-qi-card">
        <div class="wdm-qi-card-header">
          <span class="wdm-qi-card-title">
            <i data-lucide="star"></i> Plugin Hay Dùng
          </span>
          <span class="wdm-qi-card-badge"><?php echo count( $favorites ); ?></span>
        </div>

        <!-- Bộ lọc category -->
        <div class="wdm-qi-category-tabs" id="wdm-qi-cat-tabs">
          <button class="wdm-qi-cat-tab active" data-cat="all">Tất cả</button>
          <button class="wdm-qi-cat-tab" data-cat="editor">Editor</button>
          <button class="wdm-qi-cat-tab" data-cat="seo">SEO</button>
          <button class="wdm-qi-cat-tab" data-cat="security">Bảo mật</button>
          <button class="wdm-qi-cat-tab" data-cat="performance">Tốc độ</button>
          <button class="wdm-qi-cat-tab" data-cat="builder">Builder</button>
          <button class="wdm-qi-cat-tab" data-cat="forms">Form</button>
          <button class="wdm-qi-cat-tab" data-cat="ecommerce">Shop</button>
          <button class="wdm-qi-cat-tab" data-cat="backup">Backup</button>
          <button class="wdm-qi-cat-tab" data-cat="utility">Tiện ích</button>
          <button class="wdm-qi-cat-tab" data-cat="dev">Dev</button>
        </div>

        <!-- Danh sách plugin Favorites -->
        <div class="wdm-qi-favorites-list" id="wdm-qi-favorites-list">
          <?php foreach ( $favorites as $fav ) : 
              $icon_url = 'https://ps.w.org/' . $fav['slug'] . '/assets/icon-128x128.png';
          ?>
          <label class="wdm-qi-fav-item" data-cat="<?php echo esc_attr( $fav['category'] ); ?>" data-slug="<?php echo esc_attr( $fav['slug'] ); ?>">
            <input type="checkbox" class="wdm-qi-fav-checkbox" value="<?php echo esc_attr( $fav['slug'] ); ?>" data-name="<?php echo esc_attr( $fav['name'] ); ?>">
            
            <img src="<?php echo esc_url( $icon_url ); ?>" class="wdm-qi-fav-icon" alt="<?php echo esc_attr( $fav['name'] ); ?>" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
            <div class="wdm-qi-fav-icon-placeholder" style="display:none;"><i data-lucide="package"></i></div>

            <span class="wdm-qi-fav-name"><?php echo esc_html( $fav['name'] ); ?></span>
            <div style="display: flex; align-items: center; gap: 4px; margin-left: auto;">
              <button type="button" class="wdm-qi-fav-details-btn wdm-qi-history-details-btn" data-slug="<?php echo esc_attr( $fav['slug'] ); ?>" title="Xem chi tiết" style="margin-right: 4px;">
                <i data-lucide="info"></i>
              </button>
              <span class="wdm-qi-fav-status" data-slug="<?php echo esc_attr( $fav['slug'] ); ?>">
                <!-- JS sẽ điền trạng thái -->
              </span>
            </div>
          </label>
          <?php endforeach; ?>
        </div>

        <!-- Nút thêm vào hàng đợi -->
        <div style="padding: 12px 0 4px;">
          <button class="wdm-qi-btn wdm-qi-btn-primary wdm-qi-btn-full" id="wdm-qi-btn-add-favorites">
            <i data-lucide="plus-circle"></i> Thêm đã chọn vào hàng đợi
          </button>
        </div>
      </div>

      <!-- Khu vực 2: Tìm kiếm WP.org trực tiếp -->
      <div class="wdm-qi-card" style="margin-top: 16px;">
        <div class="wdm-qi-card-header">
          <span class="wdm-qi-card-title">
            <i data-lucide="search"></i> Tìm Kiếm WP.org
          </span>
        </div>

        <div class="wdm-qi-search-wrapper">
          <i data-lucide="search" class="wdm-qi-search-icon"></i>
          <input type="text" id="wdm-qi-wporg-search" class="wdm-qi-search-input" placeholder="Gõ tên plugin... (vd: elementor)">
          <div class="wdm-qi-search-spinner" id="wdm-qi-search-spinner" style="display:none;">
            <i data-lucide="loader-2"></i>
          </div>
        </div>

        <!-- Kết quả tìm kiếm -->
        <div class="wdm-qi-search-results" id="wdm-qi-search-results">
          <div class="wdm-qi-search-placeholder">
            <i data-lucide="package-search"></i>
            <p>Gõ từ khóa để tìm plugin từ kho WordPress.org</p>
          </div>
        </div>
      </div>

      <!-- Khu vực 3: Lịch Sử Cài Đặt -->
      <div class="wdm-qi-card" style="margin-top: 16px;">
        <div class="wdm-qi-card-header" style="margin-bottom: 8px;">
          <span class="wdm-qi-card-title">
            <i data-lucide="history"></i> Lịch Sử Cài Đặt
          </span>
          <div style="display: flex; gap: 4px;">
            <button class="wdm-qi-btn-text" id="wdm-qi-btn-add-all-history" title="Chọn cài lại tất cả" style="color: var(--qi-primary);">
              <i data-lucide="check-square"></i>
            </button>
            <button class="wdm-qi-btn-text" id="wdm-qi-btn-clear-history" title="Xóa lịch sử">
              <i data-lucide="trash-2"></i>
            </button>
          </div>
        </div>

        <!-- Danh sách Lịch sử -->
        <div class="wdm-qi-history-list" id="wdm-qi-history-list">
          <div class="wdm-qi-history-loading">
            <i data-lucide="loader-2" class="spin"></i>
            <span>Đang tải lịch sử...</span>
          </div>
        </div>
      </div>

    </aside>

    <!-- =========================================
         CỘT 2 (GIỮA): QUEUE CONSOLE
         ========================================= -->
    <section class="wdm-qi-col wdm-qi-col-center">
      <div class="wdm-qi-card wdm-qi-col-center-card">

        <div class="wdm-qi-card-header">
          <span class="wdm-qi-card-title">
            <i data-lucide="list-todo"></i> Hàng Đợi Cài Đặt
          </span>
          <span class="wdm-qi-card-badge" id="wdm-qi-queue-count">0</span>
        </div>

        <!-- Danh sách Queue -->
        <div class="wdm-qi-queue-list" id="wdm-qi-queue-list">
          <div class="wdm-qi-queue-empty" id="wdm-qi-queue-empty">
            <i data-lucide="inbox"></i>
            <p>Hàng đợi trống. Chọn plugin từ cột trái để thêm vào.</p>
          </div>
        </div>

        <!-- Nút bắt đầu cài đặt -->
        <div class="wdm-qi-queue-actions">
          <button class="wdm-qi-btn wdm-qi-btn-install wdm-qi-btn-full" id="wdm-qi-btn-install-all" disabled>
            <i data-lucide="zap"></i> Bắt Đầu Cài Đặt Hàng Loạt
          </button>
          <button class="wdm-qi-btn wdm-qi-btn-ghost wdm-qi-btn-full" id="wdm-qi-btn-clear-queue" style="margin-top: 8px;">
            <i data-lucide="x-circle"></i> Xóa hàng đợi
          </button>
        </div>

        <!-- Console Tiến Trình -->
        <div class="wdm-qi-console" id="wdm-qi-console" style="display:none;">
          <div class="wdm-qi-console-header">
            <i data-lucide="terminal"></i>
            <span>Console Cài Đặt</span>
            <span class="wdm-qi-console-progress-text" id="wdm-qi-progress-text">0 / 0</span>
          </div>
          <div class="wdm-qi-progress-bar-outer">
            <div class="wdm-qi-progress-bar-inner" id="wdm-qi-progress-bar" style="width: 0%;"></div>
          </div>
          <div class="wdm-qi-console-log" id="wdm-qi-console-log">
            <!-- Log entries sẽ được thêm bởi JS -->
          </div>
          <div class="wdm-qi-console-summary" id="wdm-qi-console-summary" style="display:none;">
            <!-- Tổng kết sau khi hoàn tất -->
          </div>
        </div>

      </div>
    </section>

    <!-- =========================================
         CỘT 3 (PHẢI): INSTALLED PLUGINS TABLE
         ========================================= -->
    <aside class="wdm-qi-col wdm-qi-col-right">
      <div class="wdm-qi-card wdm-qi-col-right-card">

        <div class="wdm-qi-card-header">
          <span class="wdm-qi-card-title">
            <i data-lucide="layers"></i> Plugin Đã Cài
          </span>
        </div>

        <!-- Bộ lọc trạng thái + tìm kiếm -->
        <div class="wdm-qi-table-filters">
          <div class="wdm-qi-table-search-wrapper">
            <i data-lucide="search" class="wdm-qi-table-search-icon"></i>
            <input type="text" id="wdm-qi-table-search" class="wdm-qi-table-search-input" placeholder="Lọc nhanh tên plugin...">
          </div>
          <div class="wdm-qi-status-filter-tabs" id="wdm-qi-status-tabs">
            <button class="wdm-qi-status-tab active" data-status="all">Tất cả</button>
            <button class="wdm-qi-status-tab" data-status="active">Đang bật</button>
            <button class="wdm-qi-status-tab" data-status="inactive">Đang tắt</button>
          </div>
        </div>

        <!-- Bảng danh sách plugin -->
        <div class="wdm-qi-table-container" id="wdm-qi-table-container">
          <div class="wdm-qi-table-loading">
            <i data-lucide="loader-2" class="spin"></i>
            <span>Đang tải danh sách plugin...</span>
          </div>
        </div>

      </div>
    </aside>

  </div><!-- /.wdm-qi-grid -->

  <!-- Toast container -->
  <div id="wdm-qi-toast-container" class="wdm-qi-toast-container"></div>

  <!-- Modal Chi Tiết Plugin (Glassmorphism Split-Pane) -->
  <div class="wdm-qi-modal-overlay" id="wdm-qi-details-modal" style="display: none;">
    <div class="wdm-qi-modal-container">
      <button class="wdm-qi-modal-close" id="wdm-qi-details-close" title="Đóng">
        <i data-lucide="x"></i>
      </button>
      
      <div class="wdm-qi-modal-split-layout">
        <!-- Sidebar danh sách plugin bên trái -->
        <aside class="wdm-qi-modal-list-sidebar" id="wdm-qi-modal-list-sidebar">
          <!-- JS load danh sách -->
        </aside>
        
        <!-- Nội dung chi tiết bên phải -->
        <main class="wdm-qi-modal-detail-pane">
          <div class="wdm-qi-modal-body" id="wdm-qi-details-body">
            <!-- JS load chi tiết -->
          </div>
        </main>
      </div>
    </div>
  </div>

</div><!-- /.wdm-qi-wrap -->
