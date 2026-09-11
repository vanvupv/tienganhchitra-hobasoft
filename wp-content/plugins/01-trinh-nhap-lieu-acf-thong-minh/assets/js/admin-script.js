jQuery(document).ready(function ($) {
    // Trạng thái dữ liệu toàn cục
    let scannedFields = [];     // Danh sách các trường đã quét từ bài viết: [{name, label, type, current_value, is_acf, is_system, choices}]
    let parsedRows = [];        // Dữ liệu dòng nạp được (Excel/JSON/Notepad hoặc Generator): [{col_0: val, col_1: val}, ...]
    let excelHeaders = [];      // Danh sách tiêu đề cột thô của file nguồn hoặc mock: ['col_0', 'col_1', ...] hoặc ['Tiêu đề', ...]
    let currentRowIdx = 0;      // Chỉ số dòng đang xem trước hiện tại
    let currentPostId = 0;      // ID bài viết đang chọn
    let postTypesAndFields = []; // Cached post types and their fields
    let currentExtractedPosts = []; // Danh sách bài viết đang hiển thị trong tab Lấy Tiêu Đề
    let currentTranslatedData = {}; // Danh sách bài viết đã dịch nội dung và mô tả ngắn

    // --- 1. ĐIỀU HƯỚNG TABS THÔNG MINH ---
    function activateTabByHash(hashStr) {
        if (!hashStr) return;
        let cleanHash = hashStr.replace('#', '').replace('wpsai-tab-', '');
        
        const $targetSection = $('#wpsai-tab-' + cleanHash);
        if ($targetSection.length) {
            $('.wpsai-nav-tab').removeClass('active');
            $(`.wpsai-nav-tab[data-tab="${cleanHash}"]`).addClass('active');

            $('.wpsai-tab-content').removeClass('active');
            $targetSection.addClass('active');

            // Highlight tương ứng trên WordPress Submenu sidebar
            $('.wp-submenu li').removeClass('current');
            $('.wp-submenu a').removeClass('current').removeAttr('aria-current');
            $(`.wp-submenu a[href*="#${cleanHash}"], .wp-submenu a[href*="#wpsai-tab-${cleanHash}"]`).addClass('current').attr('aria-current', 'page').closest('li').addClass('current');

            // Auto trigger change if opening bulk tabs via URL hash
            setTimeout(() => {
                if (cleanHash === 'bulk-taxonomy') {
                    const $select = $('#wpsai-bulk-taxonomy-post-type');
                    if ($select.length && $select.val()) $select.trigger('change');
                } else if (cleanHash === 'bulk-images') {
                    const $select = $('#wpsai-bulk-images-post-type');
                    if ($select.length && $select.val()) $select.trigger('change');
                } else if (cleanHash === 'bulk-excel') {
                    const $select = $('#wpsai-bulk-excel-post-type');
                    if ($select.length && $select.val()) $select.trigger('change');
                }
            }, 300);
        }
    }

    $('.wpsai-nav-tab').on('click', function (e) {
        e.preventDefault();
        const tabId = $(this).data('tab');
        
        $('.wpsai-nav-tab').removeClass('active');
        $(this).addClass('active');

        $('.wpsai-tab-content').removeClass('active');
        $('#wpsai-tab-' + tabId).addClass('active');

        window.location.hash = tabId;

        // Auto trigger change if opening bulk tabs
        if (tabId === 'bulk-taxonomy') {
            const $select = $('#wpsai-bulk-taxonomy-post-type');
            if ($select.length && $select.val()) {
                $select.trigger('change');
            }
        } else if (tabId === 'bulk-images') {
            const $select = $('#wpsai-bulk-images-post-type');
            if ($select.length && $select.val()) {
                $select.trigger('change');
            }
        } else if (tabId === 'bulk-excel') {
            const $select = $('#wpsai-bulk-excel-post-type');
            if ($select.length && $select.val()) {
                $select.trigger('change');
            }
        }
    });

    if (window.location.hash) {
        activateTabByHash(window.location.hash);
    }
    $(window).on('hashchange', function () {
        activateTabByHash(window.location.hash);
    });

    // --- 2. LƯU CÀI ĐẶT API KEY ---
    $('#wpsai-save-settings-btn').on('click', function () {
        const keyVal = $('#wpsai-gemini-key').val().trim();
        const $btn = $(this);
        const $msg = $('#wpsai-settings-msg');

        $btn.prop('disabled', true).text('Đang lưu...');
        $msg.removeClass('success error').text('');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_save_settings',
                nonce: wpsai_params.nonce,
                gemini_key: keyVal
            },
            success: function (res) {
                $btn.prop('disabled', false).text('Lưu Cài Đặt');
                if (res.success) {
                    $msg.addClass('success').text(res.data.message);
                } else {
                    $msg.addClass('error').text(res.data.message || 'Lỗi không xác định.');
                }
            },
            error: function () {
                $btn.prop('disabled', false).text('Lưu Cài Đặt');
                $msg.addClass('error').text('Lỗi kết nối máy chủ.');
            }
        });
    });

    // --- 2b. KIỂM TRA KẾT NỐI GEMINI API KEY ---
    $('#wpsai-test-gemini-btn').on('click', function () {
        const keyVal = $('#wpsai-gemini-key').val().trim();
        const $btn = $(this);
        const $msg = $('#wpsai-settings-msg');

        if (!keyVal) {
            $msg.removeClass('success').addClass('error').text('Vui lòng nhập API Key trước khi kiểm tra!');
            return;
        }

        $btn.prop('disabled', true).html('<span class="dashicons dashicons-update spin" style="font-size:16px; width:16px; height:16px; vertical-align:middle;"></span> Đang kiểm tra...');
        $msg.removeClass('success error').css('color', '#6b7280').text('Đang gửi request thử nghiệm tới Google Gemini...');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_test_gemini_key',
                nonce: wpsai_params.nonce,
                gemini_key: keyVal
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-plugins" style="font-size:16px; width:16px; height:16px; vertical-align:middle;"></span> Kiểm Tra Kết Nối API Key');
                if (res.success) {
                    $msg.removeClass('error').addClass('success').css('color', '#059669').html(`✓ ${res.data.message} (Thời gian phản hồi: ${res.data.latency})`);
                } else {
                    $msg.removeClass('success').addClass('error').css('color', '#dc2626').text(`✗ ${res.data.message}`);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-plugins" style="font-size:16px; width:16px; height:16px; vertical-align:middle;"></span> Kiểm Tra Kết Nối API Key');
                $msg.removeClass('success').addClass('error').css('color', '#dc2626').text('Lỗi kết nối máy chủ PHP/cURL.');
            }
        });
    });

    // Sao chép Extension API Key
    $('#wpsai-copy-ext-key-btn').on('click', function() {
        const keyVal = $('#wpsai-extension-key').val();
        navigator.clipboard.writeText(keyVal).then(() => {
            const $btn = $(this);
            const origText = $btn.text();
            $btn.text('Đã sao chép!').css('color', '#10b981');
            setTimeout(() => {
                $btn.text(origText).css('color', '');
            }, 2000);
        }).catch(err => {
            alert('Lỗi sao chép: ' + err);
        });
    });


    // --- 3. LOAD POST TYPES ---
    function loadPostTypes() {
        const $postTypeSelect = $('#wpsai-post-type');
        const $runnerPostTypeSelect = $('#wpsai-runner-post-type');
        const $bulkPostTypeSelect = $('#wpsai-bulk-images-post-type');
        const $bulkExcelPostTypeSelect = $('#wpsai-bulk-excel-post-type');
        const $bulkTaxonomyPostTypeSelect = $('#wpsai-bulk-taxonomy-post-type');
        const $exportPostTypeSelect = $('#wpsai-export-post-type');
        const $duplicatePostTypeSelect = $('#wpsai-duplicate-post-type');
        const $scraperPostTypeSelect = $('#wpsai-scraper-post-type');
        const $aiGeneratorPostTypeSelect = $('#wpsai-ai-generator-post-type');
        const $titlesPostTypeSelect = $('#wpsai-titles-post-type');
        
        $postTypeSelect.empty().append('<option value="">Đang tải...</option>');
        if ($runnerPostTypeSelect.length) $runnerPostTypeSelect.empty().append('<option value="">Đang tải...</option>');
        $bulkPostTypeSelect.empty().append('<option value="">Đang tải...</option>');
        $bulkExcelPostTypeSelect.empty().append('<option value="">Đang tải...</option>');
        $bulkTaxonomyPostTypeSelect.empty().append('<option value="">Đang tải...</option>');
        $exportPostTypeSelect.empty().append('<option value="">Đang tải...</option>');
        $duplicatePostTypeSelect.empty().append('<option value="">Đang tải...</option>');
        $scraperPostTypeSelect.empty().append('<option value="">Đang tải...</option>');
        $aiGeneratorPostTypeSelect.empty().append('<option value="">Đang tải...</option>');
        $titlesPostTypeSelect.empty().append('<option value="">Đang tải...</option>');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_post_types_and_fields',
                nonce: wpsai_params.nonce
            },
            success: function (res) {
                if (res.success) {
                    postTypesAndFields = res.data;
                    $postTypeSelect.empty();
                    if ($runnerPostTypeSelect.length) $runnerPostTypeSelect.empty();
                    $bulkPostTypeSelect.empty();
                    $bulkExcelPostTypeSelect.empty();
                    $bulkTaxonomyPostTypeSelect.empty();
                    $exportPostTypeSelect.empty();
                    $duplicatePostTypeSelect.empty();
                    $scraperPostTypeSelect.empty();
                    $aiGeneratorPostTypeSelect.empty();
                    $titlesPostTypeSelect.empty();
                    
                    res.data.forEach(pt => {
                        $postTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        if ($runnerPostTypeSelect.length) $runnerPostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        $bulkPostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        $bulkExcelPostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        $bulkTaxonomyPostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        $exportPostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        $duplicatePostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        $scraperPostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        $aiGeneratorPostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                        $titlesPostTypeSelect.append(`<option value="${pt.slug}">${pt.label}</option>`);
                    });
                    $postTypeSelect.trigger('change');
                    if ($runnerPostTypeSelect.length) $runnerPostTypeSelect.trigger('change');
                    $bulkPostTypeSelect.trigger('change');
                    $bulkExcelPostTypeSelect.trigger('change');
                    $bulkTaxonomyPostTypeSelect.trigger('change');
                    $exportPostTypeSelect.trigger('change');
                    $duplicatePostTypeSelect.trigger('change');
                    $scraperPostTypeSelect.trigger('change');
                    $aiGeneratorPostTypeSelect.trigger('change');
                    $titlesPostTypeSelect.trigger('change');
                } else {
                    console.error('Không tải được danh sách Post Types:', res.data.message);
                }
            }
        });
    }
    loadPostTypes();

    // Toggle hiển thị khoảng ngày tháng (Date Range)
    $(document).on('change', '#wpsai-date-mode', function() {
        const mode = $(this).val();
        if (mode === 'random_range' || mode === 'sequential') {
            $('#wpsai-date-range-wrapper').css('display', 'grid');
        } else {
            $('#wpsai-date-range-wrapper').hide();
        }
    });

    // --- 4. LOAD DANH SÁCH BÀI VIẾT THEO POST TYPE ---
    $('#wpsai-post-type').on('change', function () {
        const postType = $(this).val();
        const $postSelect = $('#wpsai-target-post');
        if (!postType) return;

        $postSelect.empty().append('<option value="">-- Đang tải danh sách bài viết --</option>');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_posts_by_post_type',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                $postSelect.empty();
                $postSelect.append('<option value="">-- Chọn bài viết đích --</option>');
                if (res.success && res.data.length > 0) {
                    res.data.forEach(post => {
                        $postSelect.append(`<option value="${post.id}">${post.title}</option>`);
                    });
                } else {
                    $postSelect.append('<option value="" disabled>-- Chưa có bài viết nào --</option>');
                }
            },
            error: function () {
                $postSelect.empty().append('<option value="">-- Lỗi kết nối --</option>');
            }
        });
    });

    // --- 5. TẠO BÀI VIẾT RỖNG MỚI ---
    $('#wpsai-create-blank-btn').on('click', function () {
        const postType = $('#wpsai-post-type').val();
        if (!postType) {
            alert('Vui lòng chọn Post Type trước!');
            return;
        }

        const $btn = $(this);
        $btn.prop('disabled', true).text('Đang tạo...');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_create_blank_post',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-plus-alt"></span> Tạo Bài Viết Rỗng Mới');
                if (res.success) {
                    const $postSelect = $('#wpsai-target-post');
                    // Add new option and select it
                    const newOpt = `<option value="${res.data.post_id}" selected>${res.data.title}</option>`;
                    $postSelect.append(newOpt).val(res.data.post_id).trigger('change');
                    
                    alert('Đã tạo thành công bài viết rỗng mới! Hệ thống sẽ tự động quét các trường.');
                    $('#wpsai-scan-btn').trigger('click');
                } else {
                    alert('Lỗi tạo bài viết: ' + res.data.message);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-plus-alt"></span> Tạo Bài Viết Rỗng Mới');
                alert('Lỗi kết nối máy chủ.');
            }
        });
    });

    // --- 6. QUÉT CÁC TRƯỜNG CỦA BÀI VIẾT ---
    $('#wpsai-scan-btn').on('click', function () {
        const postId = $('#wpsai-target-post').val();
        if (!postId) {
            alert('Vui lòng chọn bài viết hoặc bấm "Tạo Bài Viết Rỗng Mới"!');
            return;
        }

        const $btn = $(this);
        $btn.prop('disabled', true).html('<span class="dashicons dashicons-search"></span> Đang quét...');

        // Reset dữ liệu file nạp trước đó
        resetDataState();

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_scan_post_fields',
                nonce: wpsai_params.nonce,
                post_id: postId
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-search"></span> Quét Các Trường Bài Viết');
                if (res.success) {
                    scannedFields = res.data.fields;
                    currentPostId = res.data.post_id;
                    renderFieldsTable();
                    
                    // Hiện các bước tiếp theo
                    $('#wpsai-step-fields').fadeIn();
                    $('#wpsai-step-fill').fadeIn();

                    $('html, body').animate({
                        scrollTop: $('#wpsai-step-fields').offset().top - 40
                    }, 500);
                } else {
                    alert('Lỗi quét trường: ' + res.data.message);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-search"></span> Quét Các Trường Bài Viết');
                alert('Lỗi kết nối máy chủ khi quét trường.');
            }
        });
    });

    // Toggle hiển thị trường hệ thống ẩn
    $('#wpsai-show-system-fields').on('change', function () {
        renderFieldsTable();
    });

    // --- 7. RENDER BẢNG CẤU TRÚC TRƯỜNG ---
    function renderFieldsTable() {
        const $tbody = $('#wpsai-fields-table tbody');
        $tbody.empty();
        
        const showSystem = $('#wpsai-show-system-fields').is(':checked');
        const showSourceCol = parsedRows.length > 0;

        if (showSourceCol) {
            $('.source-mapping-col').show();
            $('.preview-val-col').show();
        } else {
            $('.source-mapping-col').hide();
            $('.preview-val-col').hide();
        }

        scannedFields.forEach((field, index) => {
            // Lọc trường hệ thống ẩn nếu không check hiển thị
            if (field.is_system && !showSystem) {
                return;
            }

            // Xử lý loại trường và class badge tương ứng
            let typeLabel = field.type;
            let typeClass = '';
            if (field.type === 'wp_core') {
                typeLabel = 'Core WordPress';
                typeClass = 'wpsai-badge-core';
            } else if (field.type.indexOf('acf_') === 0) {
                typeLabel = 'ACF (' + field.type.substring(4) + ')';
                typeClass = 'wpsai-badge-acf';
            } else if (field.type === 'custom_meta') {
                typeLabel = 'Custom Meta';
                typeClass = 'wpsai-badge-meta';
            } else if (field.type === 'taxonomy') {
                typeLabel = 'Taxonomy';
                typeClass = 'wpsai-badge-taxonomy';
            }

            // Cột giá trị hiện tại có thể sửa trực tiếp
            const valEscaped = field.current_value !== null ? field.current_value : '';
            const isSystemClass = field.is_system ? 'system-field-row' : '';

            let sourceDropdownHtml = '';
            let previewValHtml = '';

            if (showSourceCol) {
                // Render select để map cột từ file
                let options = '<option value="">-- Bỏ qua --</option>';
                excelHeaders.forEach((header, hIdx) => {
                    const isSelected = autoMatchField(field, header) ? 'selected' : '';
                    options += `<option value="col_${hIdx}" ${isSelected}>Cột: ${header}</option>`;
                });
                sourceDropdownHtml = `
                    <select class="wpsai-source-map-select" data-field-index="${index}" style="width: 100%;">
                        ${options}
                    </select>
                `;
                
                previewValHtml = `<div class="wpsai-preview-cell" id="wpsai-preview-val-${index}" contenteditable="true" data-field-index="${index}" style="min-height:20px; background:#fff; border:1px solid #ddd; padding:3px; border-radius:3px;"></div>`;
            }

            const rowHtml = `
                <tr class="${isSystemClass}" data-field-name="${field.name}">
                    <td><strong>${field.label}</strong></td>
                    <td><code>${field.name}</code></td>
                    <td><span class="wpsai-badge-type ${typeClass}">${typeLabel}</span></td>
                    <td>
                        <div class="wpsai-current-val-cell" contenteditable="true" data-field-index="${index}" style="min-height:20px; background:#fff; border:1px solid #ddd; padding:3px; border-radius:3px;">${valEscaped}</div>
                    </td>
                    ${showSourceCol ? `<td class="source-mapping-col">${sourceDropdownHtml}</td>` : ''}
                    ${showSourceCol ? `<td class="preview-val-col">${previewValHtml}</td>` : ''}
                </tr>
            `;

            $tbody.append(rowHtml);
        });

        // Xử lý sự kiện chỉnh sửa trực tiếp "Giá trị hiện tại"
        $tbody.off('blur', '.wpsai-current-val-cell').on('blur', '.wpsai-current-val-cell', function () {
            const fIdx = $(this).data('field-index');
            scannedFields[fIdx].current_value = $(this).text();
        });

        // Xử lý sự kiện thay đổi ánh xạ cột
        $tbody.off('change', '.wpsai-source-map-select').on('change', '.wpsai-source-map-select', function () {
            updatePreviewValuesForCurrentRow();
        });

        // Xử lý sự kiện sửa đổi "Giá trị xem trước"
        $tbody.off('blur', '.wpsai-preview-cell').on('blur', '.wpsai-preview-cell', function () {
            const fIdx = $(this).data('field-index');
            const selectVal = $(`.wpsai-source-map-select[data-field-index="${fIdx}"]`).val();
            const newVal = $(this).text();
            
            if (selectVal && parsedRows[currentRowIdx]) {
                parsedRows[currentRowIdx][selectVal] = newVal;
            }
        });

        // Cập nhật giá trị xem trước nếu đang có dữ liệu nạp
        if (showSourceCol) {
            updatePreviewValuesForCurrentRow();
        }
    }

    // So khớp thông minh giữa cột dữ liệu nguồn và trường bài viết
    function autoMatchField(field, colHeader) {
        const h = colHeader.toLowerCase().trim();
        const fName = field.name.toLowerCase().replace('acf_', '').replace('meta_', '').replace('tax_', '');
        const fLabel = field.label.toLowerCase();

        if (field.name === 'post_title' && (h === 'title' || h === 'tiêu đề' || h === 'tên' || h === 'name' || h === 'tên bài viết')) return true;
        if (field.name === 'post_content' && (h === 'content' || h === 'nội dung' || h === 'mô tả' || h === 'description' || h === 'nội dung chi tiết')) return true;
        if (field.name === 'post_excerpt' && (h === 'excerpt' || h === 'mô tả ngắn' || h === 'tóm tắt')) return true;
        if (field.name === 'featured_image' && (h === 'image' || h === 'ảnh' || h === 'ảnh đại diện' || h === 'featured image' || h === 'avatar' || h === 'thumbnail')) return true;
        if (field.name === 'post_date' && (h === 'date' || h === 'ngày' || h === 'ngày đăng' || h === 'created')) return true;
        if (field.name === 'post_name' && (h === 'slug' || h === 'đường dẫn' || h === 'url slug')) return true;

        if (field.name.startsWith('tax_')) {
            const taxSlug = field.name.substring(4);
            if (taxSlug === 'category' && (h === 'chuyên mục' || h === 'danh mục' || h === 'category' || h === 'categories' || h === 'phân loại')) return true;
            if (taxSlug === 'post_tag' && (h === 'thẻ' || h === 'tag' || h === 'tags' || h === 'từ khóa')) return true;
        }

        if (h === fName || h === fLabel || fName.includes(h) || h.includes(fName)) return true;

        return false;
    }

    // --- 8. CẬP NHẬT TRỰC TIẾP BÀI VIẾT ---
    $('#wpsai-direct-update-btn').on('click', function () {
        if (!currentPostId) return;

        const $btn = $(this);
        const $msg = $('#wpsai-direct-update-msg');
        $btn.prop('disabled', true).text('Đang lưu...');
        $msg.removeClass('success error').text('');

        // Thu thập các giá trị hiện tại để gửi đi
        const fieldsData = {};
        scannedFields.forEach(field => {
            fieldsData[field.name] = field.current_value;
        });

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_update_post_fields_directly',
                nonce: wpsai_params.nonce,
                post_id: currentPostId,
                fields: fieldsData
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-saved"></span> Lưu/Cập nhật trực tiếp bài viết');
                if (res.success) {
                    $msg.addClass('success').text(res.data.message);
                    setTimeout(() => $msg.text(''), 3000);
                } else {
                    $msg.addClass('error').text(res.data.message);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-saved"></span> Lưu/Cập nhật trực tiếp bài viết');
                $msg.addClass('error').text('Lỗi hệ thống không lưu được.');
            }
        });
    });

    // --- 8.1. TỰ SINH DỮ LIỆU GEMINI AI TẠI BƯỚC 2 ---
    $('#wpsai-step2-ai-toggle-btn').on('click', function () {
        const $box = $('#wpsai-step2-ai-box');
        $box.slideToggle(300);

        // Tự động điền chủ đề theo tên bài viết / sản phẩm đang chọn nếu ô đang trống
        const currentTitle = $('#wpsai-target-post option:selected').text();
        const $topicInput = $('#wpsai-step2-ai-topic');
        if (!$topicInput.val() && currentTitle && currentTitle.indexOf('ID:') !== -1) {
            const cleanTitle = currentTitle.replace(/\(ID:\s*\d+\)/g, '').replace(/\(Bài viết mới rỗng\)/g, '').trim();
            if (cleanTitle) {
                $topicInput.val(cleanTitle);
            }
        }
    });

    // Thay đổi số lượng bài viết sinh tại Bước 2
    $('#wpsai-step2-ai-count').on('input change', function () {
        const count = parseInt($(this).val()) || 1;
        if (count > 1) {
            $('#wpsai-step2-ai-target').val('batch_preview');
        } else {
            $('#wpsai-step2-ai-target').val('current_post');
        }
    });

    // Khởi chạy sinh dữ liệu bằng Gemini AI tại Bước 2
    $('#wpsai-step2-ai-run-btn').on('click', function () {
        const postType = $('#wpsai-post-type').val() || $('#wpsai-runner-post-type').val() || 'post';
        const topic = $('#wpsai-step2-ai-topic').val().trim();
        const count = parseInt($('#wpsai-step2-ai-count').val()) || 1;
        const target = $('#wpsai-step2-ai-target').val();

        if (scannedFields.length === 0) {
            alert('Vui lòng quét các trường của bài viết trước khi sinh dữ liệu!');
            return;
        }

        const $btn = $(this);
        const $status = $('#wpsai-step2-ai-status');
        $btn.prop('disabled', true).html('<span class="dashicons dashicons-update spin" style="font-size:16px; width:16px; height:16px; vertical-align:middle;"></span> Đang sinh dữ liệu AI...');
        $status.css('color', '#2563eb').text('Gemini AI đang phân tích các trường và tạo nội dung...');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_generate_mock_data',
                nonce: wpsai_params.nonce,
                post_type: postType,
                count: count,
                mode: 'ai',
                topic: topic,
                length: 'medium',
                tone: 'seo',
                lang: 'vi',
                gen_type: 'new',
                ref_post_id: currentPostId,
                fields: JSON.stringify(scannedFields)
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-update"></span> Khởi Chạy Sinh Dữ Liệu AI');
                if (res.success && res.data.rows && res.data.rows.length > 0) {
                    if (target === 'current_post' || count === 1) {
                        // Điền trực tiếp vào cột Giá trị hiện tại của bảng
                        const firstRow = res.data.rows[0];
                        scannedFields.forEach(field => {
                            if (firstRow[field.name] !== undefined) {
                                field.current_value = firstRow[field.name];
                            } else {
                                const cleanName = field.name.replace('acf_', '').replace('meta_', '');
                                if (firstRow[cleanName] !== undefined) {
                                    field.current_value = firstRow[cleanName];
                                }
                            }
                        });

                        renderFieldsTable();
                        $status.css('color', '#16a34a').html('✓ <strong>Đã điền thành công dữ liệu AI vào bảng!</strong> Hãy bấm nút <span style="background:#10b981; color:#fff; padding:2px 6px; border-radius:4px;">Lưu/Cập nhật trực tiếp bài viết</span> màu xanh bên trên để lưu vào WordPress.');
                        alert('Gemini AI đã tự động sinh và điền dữ liệu đầy đủ vào các trường của sản phẩm/bài viết này! Hãy bấm "Lưu/Cập nhật trực tiếp bài viết" để lưu.');
                    } else {
                        // Nạp vào hàng đợi Import hàng loạt
                        processJSONObjectArray(res.data.rows);
                        $status.css('color', '#16a34a').text(`✓ Đã sinh thành công ${res.data.rows.length} bài mẫu hoàn chỉnh!`);
                        
                        // Thêm khung nút hành động lưu xuất bản ngay
                        $('#wpsai-step2-ai-batch-actions').remove();
                        const actionHtml = `
                            <div id="wpsai-step2-ai-batch-actions" style="margin-top: 15px; padding: 14px; background: #ffffff; border: 2px dashed #16a34a; border-radius: 8px; display: flex; flex-direction: column; gap: 10px;">
                                <div style="color: #166534; font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
                                    <span class="dashicons dashicons-yes-alt" style="color: #16a34a; font-size: 20px;"></span> 
                                    Đã chuẩn bị sẵn sàng ${res.data.rows.length} bài mẫu! Bạn muốn thực hiện bước tiếp theo:
                                </div>
                                <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                                    <button type="button" class="wpsai-btn wpsai-btn-success" id="wpsai-step2-publish-now-btn" style="background: #16a34a; border: none; font-weight: 700; font-size: 14px; padding: 8px 18px; color:#fff; cursor:pointer;">
                                        <span class="dashicons dashicons-cloud-upload"></span> 🚀 Bấm Vào Đây Để Xuất Bản Ngay ${res.data.rows.length} Bài Lên Website
                                    </button>
                                    <button type="button" class="wpsai-btn wpsai-btn-secondary" id="wpsai-step2-switch-tab-btn" style="font-size: 13px;">
                                        <span class="dashicons dashicons-admin-settings"></span> Mở Tab Nhập Hàng Loạt (Cấu hình ngày đăng / Trạng thái nháp)
                                    </button>
                                </div>
                            </div>
                        `;
                        $('#wpsai-step2-ai-box').append(actionHtml);

                        $('#wpsai-step2-publish-now-btn').off('click').on('click', function () {
                            $('.wpsai-tab-nav[data-tab="import-runner"]').trigger('click');
                            setTimeout(() => {
                                $('#wpsai-start-import-btn').trigger('click');
                            }, 200);
                        });

                        $('#wpsai-step2-switch-tab-btn').off('click').on('click', function () {
                            $('.wpsai-tab-nav[data-tab="import-runner"]').trigger('click');
                            $('html, body').animate({
                                scrollTop: $('#wpsai-step-import-execute').offset().top - 40
                            }, 500);
                        });
                    }
                } else {
                    $status.css('color', '#dc2626').text('✗ Lỗi: ' + (res.data ? res.data.message : 'Không sinh được dữ liệu'));
                    alert('Lỗi sinh dữ liệu: ' + (res.data ? res.data.message : 'Không xác định'));
                }
            },
            error: function (xhr) {
                let errorMsg = 'Lỗi kết nối máy chủ (HTTP ' + (xhr.status || '500') + ')';
                if (xhr.responseJSON && xhr.responseJSON.data && xhr.responseJSON.data.message) {
                    errorMsg = xhr.responseJSON.data.message;
                } else if (xhr.responseText) {
                    try {
                        const parsed = JSON.parse(xhr.responseText);
                        if (parsed.data && parsed.data.message) errorMsg = parsed.data.message;
                    } catch (e) {
                        if (xhr.responseText.length < 200) errorMsg += ': ' + xhr.responseText;
                    }
                }
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-update"></span> Khởi Chạy Sinh Dữ Liệu AI');
                $status.css('color', '#dc2626').text('✗ ' + errorMsg);
                alert(errorMsg);
            }
        });
    });

    // --- 9. TẢI FILE DỮ LIỆU & ĐỔ VÀO PREVIEW ---
    $('input[name="wpsai_source_type"]').on('change', function () {
        const source = $(this).val();
        $('.wpsai-source-option').removeClass('active');
        $(this).closest('.wpsai-source-option').addClass('active');

        $('.source-field-group').hide();
        $('#group-' + source).fadeIn();
        
        resetDataStateOnly();
    });

    function resetDataState() {
        parsedRows = [];
        excelHeaders = [];
        currentRowIdx = 0;
        $('#wpsai-row-navigator').hide();
        $('#wpsai-step-import-execute').hide();
        $('#wpsai-step-progress').hide();
    }

    function resetDataStateOnly() {
        resetDataState();
        renderFieldsTable();
    }

    // Đọc Excel / CSV
    const dropZone = document.getElementById('wpsai-drop-zone');
    const fileInput = document.getElementById('wpsai-excel-file');
    const browseBtn = document.getElementById('wpsai-browse-btn');

    if (browseBtn) browseBtn.addEventListener('click', () => fileInput.click());
    if (fileInput) fileInput.addEventListener('change', handleExcelUpload);

    if (dropZone) {
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length) {
                fileInput.files = files;
                handleExcelUpload({ target: { files: files } });
            }
        });
    }

    function handleExcelUpload(e) {
        const file = e.target.files[0];
        if (!file) return;

        $('.wpsai-drag-drop-zone').hide();
        $('.wpsai-file-info').show().find('.wpsai-filename').text(file.name + ' (' + Math.round(file.size / 1024) + ' KB)');

        const reader = new FileReader();
        reader.onload = function (e) {
            const data = new Uint8Array(e.target.result);
            try {
                const workbook = XLSX.read(data, { type: 'array' });
                const firstSheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheetName];
                const rawSheetData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
                process2DArray(rawSheetData);
            } catch (err) {
                alert('Không thể đọc file Excel. Vui lòng kiểm tra lại.');
                console.error(err);
                $('#wpsai-remove-file').trigger('click');
            }
        };
        reader.readAsArrayBuffer(file);
    }

    $('#wpsai-remove-file').on('click', function () {
        fileInput.value = '';
        $('.wpsai-file-info').hide();
        $('.wpsai-drag-drop-zone').fadeIn();
        resetDataStateOnly();
    });

    // Google Sheets
    $('#wpsai-load-gsheet-btn').on('click', function () {
        const url = $('#wpsai-gsheet-url').val().trim();
        if (!url) {
            alert('Vui lòng nhập liên kết Google Sheets!');
            return;
        }

        const matches = url.match(/\/d\/([a-zA-Z0-9-_]+)/);
        if (!matches || !matches[1]) {
            alert('Đường dẫn Google Sheets không đúng.');
            return;
        }

        const spreadsheetId = matches[1];
        const csvUrl = `https://docs.google.com/spreadsheets/d/${spreadsheetId}/gviz/tq?tqx=out:csv`;

        const $btn = $(this);
        $btn.prop('disabled', true).text('Đang tải dữ liệu...');

        fetch(csvUrl)
            .then(response => {
                if (!response.ok) throw new Error('Lỗi fetch Google Sheet.');
                return response.text();
            })
            .then(csvText => {
                $btn.prop('disabled', false).text('Tải Dữ Liệu Sheet');
                parseCSV(csvText);
            })
            .catch(err => {
                $btn.prop('disabled', false).text('Tải Dữ Liệu Sheet');
                alert('Lỗi tải Google Sheet. Hãy công khai Sheet ở chế độ "Bất kỳ ai có liên kết đều xem được".');
            });
    });

    function parseCSV(text) {
        const lines = [];
        let row = [""];
        let inQuotes = false;

        for (let i = 0; i < text.length; i++) {
            let c = text[i];
            let next = text[i+1];

            if (c === '"') {
                if (inQuotes && next === '"') {
                    row[row.length - 1] += '"';
                    i++;
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (c === ',' && !inQuotes) {
                row.push("");
            } else if ((c === '\r' || c === '\n') && !inQuotes) {
                if (c === '\r' && next === '\n') { i++; }
                lines.push(row);
                row = [""];
            } else {
                row[row.length - 1] += c;
            }
        }
        if (row.length > 1 || row[0] !== "") {
            lines.push(row);
        }

        process2DArray(lines);
    }

    // JSON File
    $('#wpsai-json-file').on('change', function (e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (e) {
            $('#wpsai-json-raw').val(e.target.result);
        };
        reader.readAsText(file);
    });

    $('#wpsai-load-json-btn').on('click', function () {
        const rawJson = $('#wpsai-json-raw').val().trim();
        if (!rawJson) {
            alert('Vui lòng dán JSON hoặc chọn file JSON!');
            return;
        }

        try {
            const data = JSON.parse(rawJson);
            if (!Array.isArray(data)) {
                alert('JSON phải là một Mảng đối tượng (Array of Objects).');
                return;
            }
            processJSONObjectArray(data);
        } catch (err) {
            alert('JSON không hợp lệ.');
        }
    });

    // Notepad
    $('#wpsai-load-notepad-btn').on('click', function () {
        const rawText = $('#wpsai-notepad-raw').val().trim();
        const delimiterType = $('#wpsai-notepad-delimiter').val();
        
        if (!rawText) {
            alert('Vui lòng nhập dữ liệu Notepad!');
            return;
        }

        let delimiter = "\t";
        if (delimiterType === 'comma') delimiter = ",";
        if (delimiterType === 'pipe') delimiter = "|";

        const lines = rawText.split(/\r?\n/);
        const matrix = lines.map(line => line.split(delimiter).map(cell => cell.trim()));
        
        process2DArray(matrix);
    });

    // Xử lý nạp mảng 2D
    function process2DArray(matrix) {
        const cleanMatrix = matrix.filter(row => row.length > 0 && row.some(cell => cell !== undefined && cell !== ''));
        if (cleanMatrix.length < 2) {
            alert('Dữ liệu yêu cầu tối thiểu 1 hàng tiêu đề và 1 hàng nội dung.');
            return;
        }

        excelHeaders = cleanMatrix[0].map((h, index) => (h && h.trim()) ? h.trim() : 'Cột ' + (index + 1));

        parsedRows = [];
        for (let i = 1; i < cleanMatrix.length; i++) {
            const rowObj = {};
            excelHeaders.forEach((header, colIndex) => {
                rowObj['col_' + colIndex] = cleanMatrix[i][colIndex] !== undefined ? cleanMatrix[i][colIndex] : '';
            });
            parsedRows.push(rowObj);
        }

        setupPreviewState();
    }

    // Xử lý nạp mảng JSON
    function processJSONObjectArray(objArray) {
        if (objArray.length === 0) {
            alert('Mảng JSON rỗng.');
            return;
        }

        const keysSet = new Set();
        objArray.forEach(obj => {
            Object.keys(obj).forEach(k => keysSet.add(k));
        });

        excelHeaders = Array.from(keysSet);

        parsedRows = objArray.map(obj => {
            const rowObj = {};
            excelHeaders.forEach((key, index) => {
                const val = obj[key];
                rowObj['col_' + index] = typeof val === 'object' ? JSON.stringify(val) : val;
            });
            return rowObj;
        });

        setupPreviewState();
    }

    // Thiết lập trạng thái xem trước sau khi nạp thành công
    function setupPreviewState() {
        currentRowIdx = 0;
        
        // Cập nhật giao diện Bước 2 bảng trường
        renderFieldsTable();

        // Cập nhật Step 4 text
        $('#wpsai-batch-count-display').text(parsedRows.length);
        
        // Hiện navigator dòng và Step 4
        $('#wpsai-current-row-idx').text(1);
        $('#wpsai-total-rows-idx').text(parsedRows.length);
        $('#wpsai-row-navigator').show();
        $('#wpsai-step-import-execute').fadeIn();

        // Cuộn xuống bảng xem trước
        $('html, body').animate({
            scrollTop: $('#wpsai-step-fields').offset().top - 40
        }, 500);
    }

    // Cập nhật giá trị xem trước dựa trên dòng hiện tại
    function updatePreviewValuesForCurrentRow() {
        if (parsedRows.length === 0 || !parsedRows[currentRowIdx]) return;

        const rowData = parsedRows[currentRowIdx];

        scannedFields.forEach((field, index) => {
            const $select = $(`.wpsai-source-map-select[data-field-index="${index}"]`);
            if ($select.length === 0) return;

            const selectedCol = $select.val(); // e.g. "col_0", "col_1"
            const $previewCell = $(`#wpsai-preview-val-${index}`);

            if (selectedCol && rowData[selectedCol] !== undefined) {
                $previewCell.text(rowData[selectedCol]);
            } else {
                $previewCell.text('');
            }
        });
    }

    // Chuyển dòng xem trước
    $('#wpsai-prev-row-btn').on('click', function () {
        if (currentRowIdx > 0) {
            currentRowIdx--;
            $('#wpsai-current-row-idx').text(currentRowIdx + 1);
            updatePreviewValuesForCurrentRow();
        }
    });

    $('#wpsai-next-row-btn').on('click', function () {
        if (currentRowIdx < parsedRows.length - 1) {
            currentRowIdx++;
            $('#wpsai-current-row-idx').text(currentRowIdx + 1);
            updatePreviewValuesForCurrentRow();
        }
    });

    // --- 10. KHỞI CHẠY SINH DỮ LIỆU MẪU (MOCK DATA) ---
    $('#wpsai-start-generate-btn').on('click', function () {
        let postType = 'post';
        if ($('#wpsai-tab-import-runner').is(':visible') && $('#wpsai-runner-post-type').val()) {
            postType = $('#wpsai-runner-post-type').val();
        } else {
            postType = $('#wpsai-post-type').val() || $('#wpsai-runner-post-type').val() || 'post';
        }
        const count = parseInt($('#wpsai-gen-count').val());
        const mode = $('input[name="wpsai_gen_mode"]:checked').val();
        const topic = $('#wpsai-gen-topic').val().trim();
        const length = $('#wpsai-gen-length').val();
        const tone = $('#wpsai-gen-tone').val();
        const lang = $('#wpsai-gen-lang').val();
        
        if (isNaN(count) || count < 1 || count > 100) {
            alert('Vui lòng chọn số lượng từ 1 đến 100!');
            return;
        }

        const $btn = $(this);
        $btn.prop('disabled', true).html('<span class="dashicons dashicons-update spin" style="font-size:16px; width:16px; height:16px; vertical-align:middle;"></span> Đang tạo dữ liệu mẫu...');

        // Reset dữ liệu file nạp trước đó
        resetDataState();

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_generate_mock_data',
                nonce: wpsai_params.nonce,
                post_type: postType,
                count: count,
                mode: mode,
                topic: topic,
                length: length,
                tone: tone,
                lang: lang,
                gen_type: 'new', // Luôn tạo mới cho sinh dữ liệu mẫu
                fields: JSON.stringify(scannedFields) // Gửi cấu trúc trường đã quét để sinh khớp trường
            },
            success: function (res) {
                $btn.prop('disabled', false).text('Khởi Chạy Sinh Dữ Liệu');
                if (res.success) {
                    processJSONObjectArray(res.data.rows);
                    alert('Đã sinh thành công dữ liệu mẫu thử nghiệm! Bạn có thể xem trước giá trị ở cột "Giá trị xem trước".');
                } else {
                    alert('Lỗi sinh dữ liệu: ' + res.data.message);
                }
            },
            error: function () {
                $btn.prop('disabled', false).text('Khởi Chạy Sinh Dữ Liệu');
                alert('Lỗi kết nối máy chủ khi sinh dữ liệu mẫu.');
            }
        });
    });

    // --- 11. THỰC THI IMPORT / LƯU DỮ LIỆU ---
    $('input[name="wpsai_import_mode"]').on('change', function () {
        const mode = $(this).val();
        if (mode === 'create_batch') {
            $('.select-post-status-row').fadeIn();
        } else {
            $('.select-post-status-row').fadeOut();
        }
    });

    $('#wpsai-start-import-btn').on('click', function () {
        if (parsedRows.length === 0) {
            alert('Không có dữ liệu thô hoặc dữ liệu mẫu để thực thi import.');
            return;
        }

        // Lấy sơ đồ ánh xạ từ các dropdown trong bảng cấu trúc trường
        const mapping = {};
        let hasMapping = false;

        $('.wpsai-source-map-select').each(function () {
            const fIdx = $(this).data('field-index');
            const field = scannedFields[fIdx];
            const sourceCol = $(this).val();

            if (field && sourceCol) {
                mapping[field.name] = sourceCol;
                hasMapping = true;
            }
        });

        // Tự động ánh xạ thông minh các trường cơ bản nếu chưa có ánh xạ từ dropdown
        if (!hasMapping && excelHeaders.length > 0) {
            excelHeaders.forEach((header, hIdx) => {
                const colKey = 'col_' + hIdx;
                const hNorm = (header || '').toString().toLowerCase().trim();

                if (hNorm === 'post_title' || hNorm === 'title' || hNorm === 'tiêu đề' || hNorm === 'tên bài viết' || hNorm === 'tiêu đề bài viết') {
                    mapping['post_title'] = colKey;
                    hasMapping = true;
                } else if (hNorm === 'post_content' || hNorm === 'content' || hNorm === 'nội dung' || hNorm === 'chi tiết' || hNorm === 'nội dung bài viết') {
                    mapping['post_content'] = colKey;
                    hasMapping = true;
                } else if (hNorm === 'post_excerpt' || hNorm === 'excerpt' || hNorm === 'mô tả ngắn' || hNorm === 'tóm tắt' || hNorm === 'mô tả') {
                    mapping['post_excerpt'] = colKey;
                    hasMapping = true;
                } else if (hNorm === 'featured_image' || hNorm === 'image' || hNorm === 'ảnh đại diện' || hNorm === 'hình ảnh' || hNorm === 'thumbnail' || hNorm === 'avatar') {
                    mapping['featured_image'] = colKey;
                    hasMapping = true;
                } else if (hNorm === 'post_date' || hNorm === 'date' || hNorm === 'ngày đăng' || hNorm === 'thời gian' || hNorm === 'ngày tạo') {
                    mapping['post_date'] = colKey;
                    hasMapping = true;
                } else if (hNorm === 'category' || hNorm === 'chuyên mục' || hNorm === 'danh mục' || hNorm === 'tax_category') {
                    mapping['tax_category'] = colKey;
                    hasMapping = true;
                } else if (hNorm === 'post_tag' || hNorm === 'tag' || hNorm === 'thẻ' || hNorm === 'từ khóa' || hNorm === 'tax_post_tag') {
                    mapping['tax_post_tag'] = colKey;
                    hasMapping = true;
                } else if (header.startsWith('tax_') || header.startsWith('acf_') || header.startsWith('meta_')) {
                    mapping[header] = colKey;
                    hasMapping = true;
                } else {
                    mapping[header] = colKey;
                    hasMapping = true;
                }
            });

            // Nếu vẫn chưa xác định được post_title, mặc định gán cột đầu tiên làm title
            if (!mapping['post_title'] && excelHeaders.length > 0) {
                mapping['post_title'] = 'col_0';
                hasMapping = true;
            }
        }

        if (!hasMapping) {
            alert('Vui lòng ánh xạ ít nhất một trường cột dữ liệu nguồn!');
            return;
        }

        const importMode = $('input[name="wpsai_import_mode"]:checked').val() || 'create_batch';
        let postType = 'post';
        if ($('#wpsai-tab-import-runner').is(':visible') && $('#wpsai-runner-post-type').val()) {
            postType = $('#wpsai-runner-post-type').val();
        } else {
            postType = $('#wpsai-post-type').val() || $('#wpsai-runner-post-type').val() || 'post';
        }
        const postStatus = $('#wpsai-post-status').val() || 'publish';

        // Xử lý logic cấu hình ngày tháng (Date Range)
        const dateMode = $('#wpsai-date-mode').val() || 'now';
        const dateFromVal = $('#wpsai-date-from').val();
        const dateToVal = $('#wpsai-date-to').val();

        let dateFromTs = dateFromVal ? new Date(dateFromVal + 'T00:00:00').getTime() : Date.now() - (7 * 86400000);
        let dateToTs = dateToVal ? new Date(dateToVal + 'T23:59:59').getTime() : Date.now();
        if (dateFromTs > dateToTs) {
            const tmp = dateFromTs;
            dateFromTs = dateToTs;
            dateToTs = tmp;
        }

        function formatSqlDate(ts) {
            const d = new Date(ts);
            return d.getFullYear() + '-' +
                   String(d.getMonth() + 1).padStart(2, '0') + '-' +
                   String(d.getDate()).padStart(2, '0') + ' ' +
                   String(d.getHours()).padStart(2, '0') + ':' +
                   String(d.getMinutes()).padStart(2, '0') + ':' +
                   String(d.getSeconds()).padStart(2, '0');
        }

        function getCalculatedPostDate(index, total) {
            if (dateMode === 'random_range') {
                const randomTs = dateFromTs + Math.random() * (dateToTs - dateFromTs);
                return formatSqlDate(randomTs);
            } else if (dateMode === 'sequential') {
                const step = total > 1 ? (dateToTs - dateFromTs) / (total - 1) : 0;
                const seqTs = dateFromTs + (step * index);
                return formatSqlDate(seqTs);
            }
            return '';
        }

        // Chuần bị khung tiến trình
        const $progressCard = $('#wpsai-step-progress');
        const $progressBar = $('#wpsai-import-progress-bar');
        const $progressStats = $('#wpsai-import-progress-stats');
        const $log = $('#wpsai-import-log');

        $log.empty();
        $progressBar.css('width', '0%').text('0%');
        $progressCard.fadeIn();

        $('html, body').animate({
            scrollTop: $progressCard.offset().top - 40
        }, 500);

        $(this).prop('disabled', true);

        // Chuẩn bị hàng đợi import
        let queue = [];
        if (importMode === 'update_current') {
            // Chỉ cập nhật bài viết hiện tại
            const rowData = parsedRows[currentRowIdx];
            const customRowData = { ...rowData };
            customRowData['_temp_post_id'] = currentPostId;
            
            const customMapping = { ...mapping };
            customMapping['post_id'] = '_temp_post_id';

            const calcDate = getCalculatedPostDate(0, 1);
            if (calcDate) {
                customRowData['_custom_post_date'] = calcDate;
                customMapping['post_date'] = '_custom_post_date';
            }

            queue.push({
                row: customRowData,
                mapping: customMapping
            });
        } else {
            // Nhập hàng loạt bài mới
            parsedRows.forEach((rowData, rIdx) => {
                const customRowData = { ...rowData };
                const customMapping = { ...mapping };

                const calcDate = getCalculatedPostDate(rIdx, parsedRows.length);
                if (calcDate) {
                    customRowData['_custom_post_date'] = calcDate;
                    customMapping['post_date'] = '_custom_post_date';
                }

                queue.push({
                    row: customRowData,
                    mapping: customMapping
                });
            });
        }

        let currentIndex = 0;
        const totalRows = queue.length;
        let successCount = 0;
        let errorCount = 0;

        function runNext() {
            if (currentIndex >= totalRows) {
                $progressBar.css('width', '100%').text('100%');
                $progressStats.html(`<p style="color:#46b450; font-weight:bold;">Đã hoàn thành! Thành công: ${successCount}. Lỗi: ${errorCount}.</p>`);
                $('#wpsai-start-import-btn').prop('disabled', false);
                
                // Reload lại bảng cấu trúc trường bài viết hiện tại nếu là cập nhật
                if (importMode === 'update_current') {
                    $('#wpsai-scan-btn').trigger('click');
                }
                return;
            }

            const item = queue[currentIndex];
            const displayTitle = item.row[item.mapping['post_title']] || 'Bài viết #' + (currentIndex + 1);

            $log.append(`<p>Đang xử lý ${currentIndex + 1}/${totalRows}: <strong>${displayTitle}</strong>...</p>`);
            $log.scrollTop($log[0].scrollHeight);

            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_import_row',
                    nonce: wpsai_params.nonce,
                    row: item.row,
                    mapping: item.mapping,
                    post_type: postType,
                    post_status: postStatus
                },
                success: function (res) {
                    if (res.success) {
                        successCount++;
                        const editLink = res.data.edit_url ? ` | <a href="${res.data.edit_url}" target="_blank" style="text-decoration:underline;">[Chỉnh sửa]</a>` : '';
                        $log.append(`<p style="color:#46b450; margin:0 0 5px 15px;">✓ Thành công! [${postType}] ID: <a href="${res.data.permalink}" target="_blank"><strong>#${res.data.post_id}</strong></a> - ${res.data.title}${editLink}</p>`);
                    } else {
                        errorCount++;
                        $log.append(`<p style="color:#dc3232; margin:0 0 5px 15px;">✗ Thất bại! Lỗi: ${res.data.message || 'Lỗi không xác định'}</p>`);
                    }
                    
                    currentIndex++;
                    const percent = Math.round((currentIndex / totalRows) * 100);
                    $progressBar.css('width', percent + '%').text(percent + '%');
                    $progressStats.html(`<p>Đang xử lý ${currentIndex}/${totalRows}. Thành công: ${successCount}, Lỗi: ${errorCount}</p>`);
                    
                    setTimeout(runNext, 150);
                },
                error: function () {
                    errorCount++;
                    $log.append(`<p style="color:#dc3232; margin:0 0 5px 15px;">✗ Thất bại! Lỗi HTTP.</p>`);
                    currentIndex++;
                    setTimeout(runNext, 150);
                }
            });
        }

        runNext();
    });

    // --- 12. TẢI FILE EXCEL MẪU ---
    $('#wpsai-download-sample-excel-btn').on('click', function () {
        if (scannedFields.length === 0) {
            alert('Vui lòng quét các trường bài viết trước (Bước 1) để tạo file Excel mẫu!');
            return;
        }

        const showSystem = $('#wpsai-show-system-fields').is(':checked');

        // Lọc các trường sẽ xuất ra file mẫu
        const fieldsToExport = scannedFields.filter(field => {
            if (field.is_system && !showSystem) return false;
            return true;
        });

        if (fieldsToExport.length === 0) {
            alert('Không có trường nào để xuất file mẫu.');
            return;
        }

        // Dòng 1: Tiêu đề cột (Label dễ đọc)
        const headerLabels = fieldsToExport.map(f => f.label);

        // Dòng 2: Khóa trường (field name/key) để người dùng tham khảo khi map
        const headerKeys = fieldsToExport.map(f => f.name);

        // Dòng 3: Giá trị mẫu dựa trên loại trường
        const sampleRow = fieldsToExport.map(f => generateSampleValue(f, 1));

        // Dòng 4: Giá trị mẫu thứ 2 để minh họa thêm
        const sampleRow2 = fieldsToExport.map(f => generateSampleValue(f, 2));

        // Tạo workbook với SheetJS
        const wsData = [headerLabels, headerKeys, sampleRow, sampleRow2];
        const ws = XLSX.utils.aoa_to_sheet(wsData);

        // Tự động co giãn chiều rộng cột
        const colWidths = headerLabels.map((label, idx) => {
            const maxLen = Math.max(
                label.length,
                headerKeys[idx].length,
                String(sampleRow[idx]).length,
                String(sampleRow2[idx]).length
            );
            return { wch: Math.min(Math.max(maxLen + 2, 12), 50) };
        });
        ws['!cols'] = colWidths;

        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, 'Import Template');

        // Tên file tự động theo Post Type
        const postType = $('#wpsai-post-type').val() || 'post';
        const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
        const fileName = `mau-import-${postType}-${dateStr}.xlsx`;

        // Tải file
        XLSX.writeFile(wb, fileName);

        // Thông báo nhỏ
        const $btn = $(this);
        const originalHtml = $btn.html();
        $btn.html('<span class="dashicons dashicons-yes"></span> Đã tải xuống!').addClass('wpsai-btn-success');
        setTimeout(() => {
            $btn.html(originalHtml).removeClass('wpsai-btn-success');
        }, 2000);
    });

    // --- 12.1 TẢI FILE JSON MẪU ---
    $('#wpsai-download-sample-json-btn').on('click', function () {
        if (scannedFields.length === 0) {
            alert('Vui lòng quét các trường bài viết trước (Bước 1) để tạo file JSON mẫu!');
            return;
        }

        const showSystem = $('#wpsai-show-system-fields').is(':checked');
        const fieldsToExport = scannedFields.filter(field => {
            if (field.is_system && !showSystem) return false;
            return true;
        });

        if (fieldsToExport.length === 0) {
            alert('Không có trường nào để xuất file JSON.');
            return;
        }

        // Mẫu 1: Dữ liệu thực tế của bài viết hiện tại
        const sampleObj1 = {};
        fieldsToExport.forEach(f => {
            if (f.name === 'post_id') return;
            sampleObj1[f.name] = (f.current_value !== undefined && f.current_value !== '') ? f.current_value : generateSampleValue(f, 1);
        });

        // Mẫu 2: Dữ liệu mẫu minh họa thứ 2
        const sampleObj2 = {};
        fieldsToExport.forEach(f => {
            if (f.name === 'post_id') return;
            sampleObj2[f.name] = generateSampleValue(f, 2);
        });

        const jsonArray = [sampleObj1, sampleObj2];
        const jsonStr = JSON.stringify(jsonArray, null, 2);

        const postType = $('#wpsai-post-type').val() || 'post';
        const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, '');
        const fileName = `khung-du-lieu-${postType}-${dateStr}.json`;

        const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
        URL.revokeObjectURL(link.href);

        const $btn = $(this);
        const originalHtml = $btn.html();
        $btn.html('<span class="dashicons dashicons-yes"></span> Đã tải JSON!').addClass('wpsai-btn-success');
        setTimeout(() => {
            $btn.html(originalHtml).removeClass('wpsai-btn-success');
        }, 2000);
    });

    // --- 12.2 COPY PROMPT & KHUNG JSON CHO CÁC AI NGOÀI (ChatGPT, Claude, Gemini...) ---
    $('#wpsai-copy-ai-prompt-btn').on('click', function () {
        if (scannedFields.length === 0) {
            alert('Vui lòng quét các trường bài viết trước (Bước 1) để tạo Prompt AI!');
            return;
        }

        const showSystem = $('#wpsai-show-system-fields').is(':checked');
        const fieldsToExport = scannedFields.filter(field => {
            if (field.is_system && !showSystem) return false;
            return true;
        });

        const postType = $('#wpsai-post-type').val() || 'post';
        const schema = {};
        fieldsToExport.forEach(f => {
            if (f.name === 'post_id') return;
            let desc = f.label || f.name;
            if (f.choices && typeof f.choices === 'object') {
                desc += ` (Lựa chọn bắt buộc: ${Object.keys(f.choices).join(', ')})`;
            }
            schema[f.name] = desc;
        });

        const sampleObj = {};
        fieldsToExport.forEach(f => {
            if (f.name === 'post_id') return;
            sampleObj[f.name] = (f.current_value !== undefined && f.current_value !== '') ? f.current_value : generateSampleValue(f, 1);
        });

        let promptText = `Bạn là chuyên gia sáng tạo nội dung WordPress chuẩn SEO. Hãy viết [SỐ_LƯỢNG] bài viết/sản phẩm mới cho Post Type '${postType}' theo đúng chủ đề: [NHẬP_CHỦ_ĐỀ_TẠI_ĐÂY].\n\n`;
        promptText += `YÊU CẦU ĐỊNH DẠNG ĐẦU RA:\n`;
        promptText += `- BẮT BUỘC chỉ trả về duy nhất 1 JSON Array hợp lệ (không kèm giải thích markdown ngoài khối JSON).\n`;
        promptText += `- Cấu trúc từng đối tượng JSON trong mảng phải chứa đầy đủ các key sau đây:\n\n`;
        promptText += JSON.stringify(schema, null, 2) + `\n\n`;
        promptText += `DỮ LIỆU MẪU THAM CHIẾU (FEW-SHOT EXAMPLE):\n`;
        promptText += JSON.stringify([sampleObj], null, 2);

        navigator.clipboard.writeText(promptText).then(() => {
            const $btn = $('#wpsai-copy-ai-prompt-btn');
            const originalHtml = $btn.html();
            $btn.html('<span class="dashicons dashicons-yes"></span> Đã Copy Prompt!').addClass('wpsai-btn-success');
            alert('✓ Đã sao chép Prompt & Khung JSON AI vào Clipboard!\n\nBạn có thể dán (Ctrl + V) vào ChatGPT, Claude, Gemini hoặc DeepSeek để AI sinh dữ liệu hoàn hảo theo đúng cấu trúc.');
            setTimeout(() => {
                $btn.html(originalHtml).removeClass('wpsai-btn-success');
            }, 2500);
        }).catch(err => {
            alert('Không thể sao chép tự động: ' + err);
        });
    });

    /**
     * Sinh giá trị mẫu dựa trên loại trường
     */
    function generateSampleValue(field, rowNum) {
        const name = field.name;
        const type = field.type;

        // Taxonomy fields
        if (type === 'taxonomy' || name.indexOf('tax_') === 0) {
            const taxSlug = name.replace('tax_', '');
            if (taxSlug === 'category') {
                return rowNum % 2 === 1 ? 'Tin tức > Xã hội' : 'Bất động sản > Căn hộ';
            }
            if (taxSlug === 'post_tag') {
                return 'Xu hướng, Nổi bật, WordPress';
            }
            return 'Nhóm ' + rowNum + ' > Phân nhóm ' + rowNum;
        }

        // Core WordPress fields
        if (name === 'post_title') return 'Tiêu đề bài viết mẫu ' + rowNum;
        if (name === 'post_name') return 'bai-viet-mau-' + rowNum;
        if (name === 'post_content') return '<p>Nội dung chi tiết bài viết mẫu số ' + rowNum + '. Đây là đoạn văn mô tả sản phẩm/dịch vụ.</p>';
        if (name === 'post_excerpt') return 'Mô tả ngắn bài viết mẫu ' + rowNum;
        if (name === 'post_date') return '2025-01-' + String(rowNum).padStart(2, '0') + ' 08:00:00';
        if (name === 'featured_image') return 'https://example.com/images/sample-' + rowNum + '.jpg';

        // ACF fields - sinh dựa trên loại cụ thể
        if (type.indexOf('acf_') === 0) {
            const acfType = type.substring(4);

            switch (acfType) {
                case 'text':
                    return 'Giá trị mẫu ' + rowNum;
                case 'textarea':
                    return 'Nội dung văn bản nhiều dòng mẫu ' + rowNum;
                case 'wysiwyg':
                    return '<p>Nội dung HTML mẫu ' + rowNum + '</p>';
                case 'number':
                    return (rowNum * 100000 + Math.floor(Math.random() * 50000));
                case 'email':
                    return 'contact' + rowNum + '@example.com';
                case 'url':
                    return 'https://example.com/lien-ket-' + rowNum;
                case 'image':
                case 'file':
                    return 'https://example.com/media/file-' + rowNum + '.jpg';
                case 'select':
                case 'radio':
                    if (field.choices && typeof field.choices === 'object') {
                        const keys = Object.keys(field.choices);
                        if (keys.length > 0) {
                            return keys[(rowNum - 1) % keys.length];
                        }
                    }
                    return 'option_' + rowNum;
                case 'checkbox':
                    if (field.choices && typeof field.choices === 'object') {
                        const cKeys = Object.keys(field.choices);
                        if (cKeys.length > 0) {
                            return cKeys.slice(0, Math.min(2, cKeys.length)).join(',');
                        }
                    }
                    return 'option_1,option_2';
                case 'true_false':
                    return rowNum % 2 === 1 ? '1' : '0';
                case 'date_picker':
                    return '2025-0' + ((rowNum % 9) + 1) + '-15';
                case 'time_picker':
                    return '0' + (8 + rowNum) + ':00:00';
                case 'date_time_picker':
                    return '2025-01-' + String(rowNum).padStart(2, '0') + ' 14:30:00';
                case 'color_picker':
                    return rowNum % 2 === 1 ? '#3498db' : '#e74c3c';
                case 'google_map':
                    return JSON.stringify({lat: 21.0285, lng: 105.8542});
                case 'gallery':
                    return 'https://example.com/img1.jpg,https://example.com/img2.jpg';
                case 'repeater':
                case 'flexible_content':
                case 'group':
                    return '(Trường phức tạp - cần nhập thủ công)';
                case 'relationship':
                case 'post_object':
                    return '1';
                case 'taxonomy':
                    return 'category-' + rowNum;
                case 'oembed':
                    return 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
                default:
                    return 'Mẫu ' + rowNum;
            }
        }

        // Custom meta fields
        if (type === 'custom_meta') {
            // Nếu giá trị hiện tại có dạng giống JSON, giữ nguyên format
            if (field.current_value && (field.current_value.startsWith('{') || field.current_value.startsWith('['))) {
                return field.current_value;
            }
            return 'meta_value_' + rowNum;
        }

        return 'Mẫu ' + rowNum;
    }

    // =========================================================================
    // --- 13. XỬ LÝ THÊM ẢNH HÀNG LOẠT (BULK IMAGES TAB) ---
    // =========================================================================
    let bulkImagesPosts = [];       // Danh sách bài viết đầy đủ của Post Type đang chọn
    let bulkSelectedImages = [];    // Danh sách ảnh đã chọn để gán: [{id, url}]
    let bulkMediaFrame = null;      // Frame WP Media Library instance

    // Khi chọn Post Type thay đổi trong Tab Thêm Ảnh Hàng Loạt
    $('#wpsai-bulk-images-post-type').on('change', function () {
        const postType = $(this).val();
        if (!postType) return;

        const $postsWrapper = $('.wpsai-posts-selector-wrapper');
        const $tbody = $('#wpsai-bulk-images-posts-table tbody');
        
        $postsWrapper.show();
        $tbody.empty().append('<tr><td colspan="5" style="text-align:center;">Đang tải danh sách bài viết...</td></tr>');
        $('#wpsai-bulk-images-search').val('');
        $('#wpsai-bulk-images-select-all').prop('checked', false);

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_posts_for_bulk_images',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                if (res.success) {
                    bulkImagesPosts = res.data;
                    renderBulkImagesPostsTable();
                } else {
                    $tbody.empty().append(`<tr><td colspan="5" style="text-align:center; color:var(--wpsai-error);">Lỗi: ${res.data.message}</td></tr>`);
                }
            },
            error: function () {
                $tbody.empty().append('<tr><td colspan="5" style="text-align:center; color:var(--wpsai-error);">Lỗi kết nối máy chủ.</td></tr>');
            }
        });
    });

    // Render bảng danh sách bài viết trong Tab Thêm Ảnh Hàng Loạt
    function renderBulkImagesPostsTable() {
        const $tbody = $('#wpsai-bulk-images-posts-table tbody');
        $tbody.empty();

        if (bulkImagesPosts.length === 0) {
            $tbody.append('<tr><td colspan="5" style="text-align:center;">Không tìm thấy bài viết nào.</td></tr>');
            updateBulkSelectedCount();
            return;
        }

        bulkImagesPosts.forEach(post => {
            const thumbHtml = post.thumb_url 
                ? `<img src="${post.thumb_url}" class="wpsai-post-list-thumb" data-post-id="${post.id}" />` 
                : `<div class="wpsai-post-list-thumb" data-post-id="${post.id}" style="display:flex; align-items:center; justify-content:center; color:#94a3b8;"><span class="dashicons dashicons-format-image" style="font-size:24px; width:24px; height:24px;"></span></div>`;

            $tbody.append(`
                <tr class="bulk-image-post-row" data-post-id="${post.id}" data-title="${post.title.toLowerCase()}">
                    <td style="text-align:center; vertical-align:middle;">
                        <input type="checkbox" class="wpsai-bulk-images-post-checkbox" value="${post.id}">
                    </td>
                    <td>${thumbHtml}</td>
                    <td><code>${post.id}</code></td>
                    <td><a href="${post.permalink}" target="_blank"><strong>${post.title}</strong></a></td>
                    <td><span style="font-size:12px; color:var(--wpsai-text-muted);">${post.post_date}</span></td>
                </tr>
            `);
        });

        updateBulkSelectedCount();
    }

    // Tìm kiếm bài viết nhanh client-side
    $('#wpsai-bulk-images-search').on('input', function () {
        const query = $(this).val().toLowerCase().trim();
        if (!query) {
            $('.bulk-image-post-row').show();
            return;
        }
        $('.bulk-image-post-row').each(function () {
            const title = $(this).data('title');
            if (title.indexOf(query) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Checkbox chọn tất cả
    $('#wpsai-bulk-images-select-all').on('change', function () {
        const checked = $(this).is(':checked');
        $('.wpsai-bulk-images-post-checkbox:visible').prop('checked', checked);
        updateBulkSelectedCount();
    });

    // Sự kiện check từng dòng
    $(document).on('change', '.wpsai-bulk-images-post-checkbox', function () {
        updateBulkSelectedCount();
    });

    function updateBulkSelectedCount() {
        const total = $('.wpsai-bulk-images-post-checkbox').length;
        const selected = $('.wpsai-bulk-images-post-checkbox:checked').length;
        $('#wpsai-bulk-images-selected-count').text(`Đã chọn: ${selected}/${total} bài viết`);
        
        if (selected === total && total > 0) {
            $('#wpsai-bulk-images-select-all').prop('checked', true);
        } else {
            $('#wpsai-bulk-images-select-all').prop('checked', false);
        }
    }

    // Chọn Ảnh Từ WP Media Library
    $('#wpsai-bulk-images-select-btn').on('click', function (e) {
        e.preventDefault();

        // Tạo frame nếu chưa có
        if (!bulkMediaFrame) {
            bulkMediaFrame = wp.media({
                title: 'Chọn/Tải Lên Danh Sách Ảnh Gán Bài Viết',
                button: {
                    text: 'Thêm ảnh vào danh sách gán'
                },
                multiple: true,
                library: {
                    type: 'image'
                }
            });

            // Lắng nghe sự kiện chọn
            bulkMediaFrame.on('select', function () {
                const attachments = bulkMediaFrame.state().get('selection').toJSON();
                
                attachments.forEach(attachment => {
                    // Kiểm tra trùng lặp
                    if (!bulkSelectedImages.some(img => img.id === attachment.id)) {
                        const thumbUrl = attachment.sizes && attachment.sizes.thumbnail 
                            ? attachment.sizes.thumbnail.url 
                            : attachment.url;
                        
                        bulkSelectedImages.push({
                            id: attachment.id,
                            url: thumbUrl
                        });
                    }
                });

                renderSelectedImagesGrid();
            });
        }

        bulkMediaFrame.open();
    });

    // Render danh sách ảnh preview
    function renderSelectedImagesGrid() {
        const $grid = $('#wpsai-bulk-images-preview-grid');
        $grid.empty();

        if (bulkSelectedImages.length === 0) {
            $('#wpsai-bulk-images-preview-container').hide();
            $('#wpsai-bulk-images-clear-btn').hide();
            return;
        }

        bulkSelectedImages.forEach((img, idx) => {
            $grid.append(`
                <div class="wpsai-image-preview-item">
                    <button type="button" class="remove-btn" data-index="${idx}" title="Xóa ảnh này">&times;</button>
                    <img src="${img.url}" />
                </div>
            `);
        });

        $('#wpsai-bulk-images-count-badge').text(`${bulkSelectedImages.length} ảnh`);
        $('#wpsai-bulk-images-preview-container').fadeIn();
        $('#wpsai-bulk-images-clear-btn').fadeIn();
    }

    // Xóa ảnh đơn lẻ khỏi danh sách gán
    $(document).on('click', '.wpsai-image-preview-item .remove-btn', function () {
        const index = $(this).data('index');
        bulkSelectedImages.splice(index, 1);
        renderSelectedImagesGrid();
    });

    // Xóa toàn bộ ảnh đã chọn
    $('#wpsai-bulk-images-clear-btn').on('click', function () {
        bulkSelectedImages = [];
        renderSelectedImagesGrid();
    });

    // Chuyển đổi tab radio chế độ
    $('input[name="wpsai_bulk_images_mode"]').on('change', function () {
        const mode = $(this).val();
        
        // Cập nhật class active
        $(this).closest('.wpsai-generator-modes').find('.wpsai-radio-card').removeClass('active');
        $(this).closest('.wpsai-radio-card').addClass('active');

        if (mode === 'range') {
            $('#wpsai-bulk-images-range-setting').fadeIn();
        } else {
            $('#wpsai-bulk-images-range-setting').fadeOut();
        }
    });

    // Thực thi gán ảnh
    $('#wpsai-bulk-images-start-btn').on('click', function () {
        // Thu thập post_ids được check
        const selectedPostIds = [];
        $('.wpsai-bulk-images-post-checkbox:checked').each(function () {
            selectedPostIds.push(parseInt($(this).val()));
        });

        if (selectedPostIds.length === 0) {
            alert('Vui lòng chọn ít nhất một bài viết để gán ảnh đại diện!');
            return;
        }

        if (bulkSelectedImages.length === 0) {
            alert('Vui lòng chọn hoặc tải lên ít nhất một hình ảnh ở Bước 2!');
            return;
        }

        const mode = $('input[name="wpsai_bulk_images_mode"]:checked').val();
        let rangeSize = parseInt($('#wpsai-bulk-images-range-size').val());
        if (mode === 'range' && (isNaN(rangeSize) || rangeSize < 1)) {
            alert('Vui lòng nhập số lượng bài viết hợp lệ trên mỗi khoảng (N >= 1).');
            return;
        }

        // Tính toán danh sách phân phối gán ảnh
        const queue = [];
        selectedPostIds.forEach((postId, idx) => {
            let imgIndex = 0;

            if (mode === 'sequential') {
                imgIndex = idx % bulkSelectedImages.length;
            } else if (mode === 'random') {
                imgIndex = Math.floor(Math.random() * bulkSelectedImages.length);
            } else if (mode === 'range') {
                imgIndex = Math.floor(idx / rangeSize) % bulkSelectedImages.length;
            }

            queue.push({
                postId: postId,
                attachmentId: bulkSelectedImages[imgIndex].id,
                imgUrl: bulkSelectedImages[imgIndex].url
            });
        });

        // Thiết lập giao diện tiến trình
        const $progressCard = $('#wpsai-bulk-images-progress-card');
        const $progressBar = $('#wpsai-bulk-images-progress-bar');
        const $progressStats = $('#wpsai-bulk-images-progress-stats');
        const $log = $('#wpsai-bulk-images-log');

        $log.empty();
        $progressBar.css('width', '0%').text('0%');
        $progressCard.fadeIn();

        $('html, body').animate({
            scrollTop: $progressCard.offset().top - 40
        }, 500);

        const $btn = $(this);
        $btn.prop('disabled', true);

        let currentIndex = 0;
        const total = queue.length;
        let successCount = 0;
        let errorCount = 0;

        function runNextBulkImage() {
            if (currentIndex >= total) {
                $progressBar.css('width', '100%').text('100%');
                $progressStats.html(`<p style="color:#10b981; font-weight:bold;">Đã hoàn thành gán ảnh! Thành công: ${successCount}. Lỗi: ${errorCount}.</p>`);
                $btn.prop('disabled', false);
                return;
            }

            const item = queue[currentIndex];
            
            // Tìm tiêu đề bài viết để hiển thị log
            const postObj = bulkImagesPosts.find(p => p.id === item.postId);
            const postTitle = postObj ? postObj.title : 'Bài viết #' + item.postId;

            $log.append(`<p>Đang xử lý ${currentIndex + 1}/${total}: Bài viết <strong>"${postTitle}"</strong> (ID: ${item.postId})...</p>`);
            $log.scrollTop($log[0].scrollHeight);

            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_set_post_thumbnail_ajax',
                    nonce: wpsai_params.nonce,
                    post_id: item.postId,
                    attachment_id: item.attachmentId
                },
                success: function (res) {
                    if (res.success) {
                        successCount++;
                        $log.append(`<p class="log-success" style="margin:0 0 5px 15px;">✓ Thành công! Đã gán ảnh ID: ${item.attachmentId}</p>`);
                        
                        // Cập nhật hình ảnh thu nhỏ trực tiếp trên dòng của bảng danh sách
                        const $thumbCell = $(`.bulk-image-post-row[data-post-id="${item.postId}"] .wpsai-post-list-thumb`);
                        if ($thumbCell.length) {
                            if ($thumbCell.is('img')) {
                                $thumbCell.attr('src', res.data.thumb_url);
                            } else {
                                const newImg = `<img src="${res.data.thumb_url}" class="wpsai-post-list-thumb" data-post-id="${item.postId}" />`;
                                $thumbCell.replaceWith(newImg);
                            }
                        }
                    } else {
                        errorCount++;
                        $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi: ${res.data.message || 'Lỗi không xác định'}</p>`);
                    }

                    currentIndex++;
                    const percent = Math.round((currentIndex / total) * 100);
                    $progressBar.css('width', percent + '%').text(percent + '%');
                    $progressStats.html(`<p>Đang gán ảnh ${currentIndex}/${total}. Thành công: ${successCount}, Lỗi: ${errorCount}</p>`);
                    
                    setTimeout(runNextBulkImage, 150);
                },
                error: function () {
                    errorCount++;
                    $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi kết nối HTTP.</p>`);
                    
                    currentIndex++;
                    setTimeout(runNextBulkImage, 150);
                }
            });
        }

        runNextBulkImage();
    });

    // =========================================================================
    // --- 15. XỬ LÝ NHÂN BẢN HÀNG LOẠT (DUPLICATE TAB) ---
    // =========================================================================
    


    // =========================================================================
    // --- 14. XỬ LÝ XUẤT DỮ LIỆU (EXPORT TAB) ---
    // =========================================================================
    let exportPostsList = [];          // Danh sách bài viết để xuất
    let exportAcfFields = [];          // Danh sách trường ACF của post type được chọn

    // Thay đổi Post Type trong Tab Xuất
    $('#wpsai-export-post-type').on('change', function () {
        const postType = $(this).val();
        if (!postType) return;

        const $postsWrapper = $('#wpsai-export-posts-wrapper');
        const $tbody = $('#wpsai-export-posts-table tbody');
        const $acfSection = $('#wpsai-export-acf-fields-section');
        const $acfList = $('#wpsai-export-acf-fields-list');

        $postsWrapper.show();
        $tbody.empty().append('<tr><td colspan="4" style="text-align:center;">Đang tải danh sách bài viết...</td></tr>');
        $acfSection.hide();
        $acfList.empty();
        $('#wpsai-export-search').val('');
        $('#wpsai-export-select-all').prop('checked', false);
        $('#wpsai-export-fields-card').hide();
        $('#wpsai-export-execute-card').hide();
        $('#wpsai-export-progress-card').hide();

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_posts_for_export',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                if (res.success) {
                    exportPostsList = res.data.posts;
                    exportAcfFields = res.data.acf_fields;

                    renderExportPostsTable();

                    // Render danh sách trường ACF nếu có
                    if (exportAcfFields.length > 0) {
                        exportAcfFields.forEach(field => {
                            $acfList.append(`
                                <label class="wpsai-checkbox-label" style="min-width: 200px;">
                                    <input type="checkbox" name="wpsai_export_fields[]" value="${field.name}" checked>
                                    <span>${field.label}</span>
                                </label>
                            `);
                        });
                        $acfSection.show();
                    }

                    $('#wpsai-export-fields-card').fadeIn();
                    $('#wpsai-export-execute-card').fadeIn();
                } else {
                    $tbody.empty().append(`<tr><td colspan="4" style="text-align:center; color:var(--wpsai-error);">Lỗi: ${res.data.message}</td></tr>`);
                }
            },
            error: function () {
                $tbody.empty().append('<tr><td colspan="4" style="text-align:center; color:var(--wpsai-error);">Lỗi kết nối máy chủ.</td></tr>');
            }
        });
    });

    // Render bảng danh sách bài viết trong Tab Xuất
    function renderExportPostsTable() {
        const $tbody = $('#wpsai-export-posts-table tbody');
        $tbody.empty();

        if (exportPostsList.length === 0) {
            $tbody.append('<tr><td colspan="4" style="text-align:center;">Không tìm thấy bài viết nào.</td></tr>');
            updateExportSelectedCount();
            return;
        }

        exportPostsList.forEach(post => {
            $tbody.append(`
                <tr class="export-post-row" data-post-id="${post.id}" data-title="${post.title.toLowerCase()}">
                    <td style="text-align:center; vertical-align:middle;">
                        <input type="checkbox" class="wpsai-export-post-checkbox" value="${post.id}">
                    </td>
                    <td><code>${post.id}</code></td>
                    <td><a href="#" style="font-weight:600; pointer-events:none; color:var(--wpsai-text-main);">${post.title}</a></td>
                    <td><span style="font-size:12px; color:var(--wpsai-text-muted);">${post.post_date}</span></td>
                </tr>
            `);
        });

        updateExportSelectedCount();
    }

    // Tìm kiếm bài viết nhanh trong Tab Xuất
    $('#wpsai-export-search').on('input', function () {
        const query = $(this).val().toLowerCase().trim();
        if (!query) {
            $('.export-post-row').show();
            return;
        }
        $('.export-post-row').each(function () {
            const title = $(this).data('title');
            if (title.indexOf(query) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Checkbox chọn tất cả bài viết xuất
    $('#wpsai-export-select-all').on('change', function () {
        const checked = $(this).is(':checked');
        $('.wpsai-export-post-checkbox:visible').prop('checked', checked);
        updateExportSelectedCount();
    });

    // Sự kiện check từng dòng bài viết xuất
    $(document).on('change', '.wpsai-export-post-checkbox', function () {
        updateExportSelectedCount();
    });

    function updateExportSelectedCount() {
        const total = $('.wpsai-export-post-checkbox').length;
        const selected = $('.wpsai-export-post-checkbox:checked').length;
        $('#wpsai-export-selected-count').text(`Đã chọn: ${selected}/${total} bài viết`);

        if (selected === total && total > 0) {
            $('#wpsai-export-select-all').prop('checked', true);
        } else {
            $('#wpsai-export-select-all').prop('checked', false);
        }
    }

    // Thực thi xuất Excel và ZIP
    $('#wpsai-export-start-btn').on('click', function () {
        // Thu thập post_ids được check
        const selectedPostIds = [];
        $('.wpsai-export-post-checkbox:checked').each(function () {
            selectedPostIds.push(parseInt($(this).val()));
        });

        if (selectedPostIds.length === 0) {
            alert('Vui lòng chọn ít nhất một bài viết để xuất!');
            return;
        }

        // Thu thập fields được check
        const selectedFields = [];
        const headerLabels = {};

        $('input[name="wpsai_export_fields[]"]:checked').each(function () {
            const val = $(this).val();
            selectedFields.push(val);

            // Gán label dễ đọc cho cột Excel
            if (val === 'post_id') headerLabels['post_id'] = 'ID bài viết';
            else if (val === 'post_title') headerLabels['post_title'] = 'Tiêu đề';
            else if (val === 'post_name') headerLabels['post_name'] = 'Slug';
            else if (val === 'post_content') headerLabels['post_content'] = 'Nội dung chi tiết';
            else if (val === 'post_excerpt') headerLabels['post_excerpt'] = 'Mô tả ngắn';
            else if (val === 'post_date') headerLabels['post_date'] = 'Ngày tạo';
            else if (val === 'featured_image') headerLabels['featured_image'] = 'Ảnh đại diện (Featured Image)';
            else {
                const fieldLabelText = $(this).closest('label').find('span').text();
                headerLabels[val] = fieldLabelText;
            }
        });

        if (selectedFields.length === 0) {
            alert('Vui lòng chọn ít nhất một trường dữ liệu để xuất!');
            return;
        }

        const postType = $('#wpsai-export-post-type').val();

        // Cấu hình giao diện tiến trình
        const $progressCard = $('#wpsai-export-progress-card');
        const $progressBar = $('#wpsai-export-progress-bar');
        const $progressStats = $('#wpsai-export-progress-stats');
        const $downloadArea = $('#wpsai-export-download-area');
        const $log = $('#wpsai-export-log');

        $log.empty();
        $progressBar.css('width', '0%').text('0%');
        $downloadArea.hide();
        $progressCard.fadeIn();

        $('html, body').animate({
            scrollTop: $progressCard.offset().top - 40
        }, 500);

        const $btn = $(this);
        $btn.prop('disabled', true).text('Đang xử lý...');

        $log.append('<p><strong>Bắt đầu truy vấn dữ liệu từ máy chủ...</strong></p>');

        // Bước A: Lấy chi tiết dữ liệu và danh sách file từ backend
        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_export_data',
                nonce: wpsai_params.nonce,
                post_type: postType,
                post_ids: selectedPostIds,
                fields: selectedFields
            },
            success: function (res) {
                if (res.success) {
                    $log.append(`<p class="log-success">✓ Đã lấy dữ liệu chi tiết của ${res.data.rows.length} bài viết.</p>`);
                    $log.append(`<p>Tìm thấy ${Object.keys(res.data.file_mappings).length} tệp hình ảnh đính kèm cần đóng gói.</p>`);
                    $progressBar.css('width', '40%').text('40%');
                    $progressStats.html('<p>Đang sinh tệp Excel và chuẩn bị mã hóa...</p>');

                    try {
                        // Bước B: Dùng SheetJS tạo file Excel có cột nhãn tiếng Việt
                        const excelRows = res.data.rows.map(row => {
                            const newRow = {};
                            selectedFields.forEach(f => {
                                const label = headerLabels[f] || f;
                                let val = row[f] !== undefined ? row[f] : '';
                                if (typeof val === 'string' && val.length > 32760) {
                                    val = val.substring(0, 32760);
                                    $log.append(`<p style="color:var(--wpsai-red);">Cảnh báo: Trường "${label}" vượt giới hạn ký tự Excel, đã tự động cắt ngắn.</p>`);
                                }
                                newRow[label] = val;
                            });
                            return newRow;
                        });

                        const ws = XLSX.utils.json_to_sheet(excelRows);
                        const wb = XLSX.utils.book_new();
                        XLSX.utils.book_append_sheet(wb, ws, 'Posts Export');

                        // Co giãn chiều rộng cột
                        const colWidths = selectedFields.map(f => {
                            const label = headerLabels[f] || f;
                            return { wch: Math.min(Math.max(label.length + 3, 15), 60) };
                        });
                        ws['!cols'] = colWidths;

                        const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'base64' });

                        $log.append('<p>Đã tạo thành công cấu trúc Excel. Đang gửi dữ liệu nén tệp lên server...</p>');
                        $progressBar.css('width', '70%').text('70%');
                        $progressStats.html('<p>Đang nén file ZIP trên server...</p>');

                        // Bước C: Gửi chuỗi Excel Base64 và mappings file lên backend để đóng gói ZIP
                        $.ajax({
                            url: wpsai_params.ajax_url,
                            type: 'POST',
                            data: {
                                action: 'wpsai_create_zip_export',
                                nonce: wpsai_params.nonce,
                                xlsx_base64: wbout,
                                files: JSON.stringify(res.data.file_mappings),
                                post_type: postType
                            },
                            success: function (zipRes) {
                                $btn.prop('disabled', false).html('<span class="dashicons dashicons-database-export"></span> Bắt Đầu Xuất File ZIP');
                                if (zipRes.success) {
                                    $log.append('<p class="log-success">✓ File ZIP được đóng gói hoàn tất thành công!</p>');
                                    $progressBar.css('width', '100%').text('100%');
                                    $progressStats.html('<p style="color:#10b981; font-weight:bold;">Đã hoàn tất xuất dữ liệu!</p>');

                                    // Hiển thị nút download
                                    $('#wpsai-export-download-link').attr('href', zipRes.data.download_url);
                                    $downloadArea.fadeIn();

                                    // Tự động kích hoạt tải xuống
                                    window.location.href = zipRes.data.download_url;
                                } else {
                                    $log.append(`<p class="log-error">✗ Lỗi tạo ZIP: ${zipRes.data.message}</p>`);
                                    $progressStats.html('<p style="color:var(--wpsai-error);">Lỗi nén tệp.</p>');
                                }
                            },
                            error: function () {
                                $btn.prop('disabled', false).html('<span class="dashicons dashicons-database-export"></span> Bắt Đầu Xuất File ZIP');
                                $log.append('<p class="log-error">✗ Lỗi kết nối HTTP khi tạo ZIP.</p>');
                            }
                        });

                    } catch (err) {
                        $btn.prop('disabled', false).html('<span class="dashicons dashicons-database-export"></span> Bắt Đầu Xuất File ZIP');
                        $log.append(`<p class="log-error">✗ Lỗi xử lý Excel tại client: ${err.message}</p>`);
                        console.error(err);
                    }

                } else {
                    $btn.prop('disabled', false).html('<span class="dashicons dashicons-database-export"></span> Bắt Đầu Xuất File ZIP');
                    $log.append(`<p class="log-error">✗ Lỗi từ máy chủ: ${res.data.message}</p>`);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-database-export"></span> Bắt Đầu Xuất File ZIP');
                $log.append('<p class="log-error">✗ Lỗi kết nối HTTP khi truy vấn bài viết.</p>');
            }
        });
    });

    // =========================================================================
    // --- 16. XỬ LÝ GÁN PHÂN LOẠI HÀNG LOẠT (BULK TAXONOMY TAB) ---
    // =========================================================================
    let bulkTaxonomyPosts = []; // Danh sách bài viết đầy đủ của Post Type
    
    // Khi Post Type thay đổi trong tab Gán Phân Loại
    $('#wpsai-bulk-taxonomy-post-type').on('change', function () {
        const postType = $(this).val();
        if (!postType) return;

        const $postsWrapper = $('#wpsai-bulk-taxonomy-posts-wrapper');
        const $tbody = $('#wpsai-bulk-taxonomy-posts-table tbody');
        const $taxSelect = $('#wpsai-bulk-taxonomy-select');
        const $termsWrapper = $('#wpsai-bulk-taxonomy-existing-terms');

        $postsWrapper.show();
        $tbody.empty().append('<tr><td colspan="5" style="text-align:center;">Đang tải danh sách bài viết...</td></tr>');
        $taxSelect.empty().append('<option value="">-- Đang tải Taxonomy... --</option>');
        $termsWrapper.empty().html('<p style="color: var(--wpsai-text-muted); font-style: italic;">Vui lòng chọn Taxonomy trước để tải danh sách.</p>');

        $('#wpsai-bulk-taxonomy-config-card').hide();
        $('#wpsai-bulk-taxonomy-mode-card').hide();
        $('#wpsai-bulk-taxonomy-execute-card').hide();
        $('#wpsai-bulk-taxonomy-progress-card').hide();
        $('#wpsai-bulk-taxonomy-search').val('');
        $('#wpsai-bulk-taxonomy-select-all').prop('checked', false);

        // A. Load bài viết
        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_posts_for_bulk_images', // Có thể dùng lại vì nó đã trả về ID, Title, post_date và permalink.
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                if (res.success) {
                    bulkTaxonomyPosts = res.data;
                    renderBulkTaxonomyPostsTable();
                } else {
                    $tbody.empty().append(`<tr><td colspan="5" style="text-align:center; color:var(--wpsai-error);">Lỗi: ${res.data.message}</td></tr>`);
                }
            },
            error: function () {
                $tbody.empty().append('<tr><td colspan="5" style="text-align:center; color:var(--wpsai-error);">Lỗi kết nối máy chủ khi lấy bài viết.</td></tr>');
            }
        });

        // B. Load Taxonomies
        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_taxonomies_for_post_type',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                if (res.success && res.data.length > 0) {
                    $taxSelect.empty();
                    res.data.forEach(tax => {
                        $taxSelect.append(`<option value="${tax.slug}">${tax.label}</option>`);
                    });
                    $taxSelect.trigger('change');
                } else {
                    $taxSelect.empty().append('<option value="">Lỗi tải Taxonomy</option>');
                }
            },
            error: function () {
                $taxSelect.empty().append('<option value="">Lỗi kết nối</option>');
            }
        });
    });

    // Render bảng bài viết
    function renderBulkTaxonomyPostsTable() {
        const $tbody = $('#wpsai-bulk-taxonomy-posts-table tbody');
        $tbody.empty();

        if (bulkTaxonomyPosts.length === 0) {
            $tbody.append('<tr><td colspan="5" style="text-align:center;">Không tìm thấy bài viết nào.</td></tr>');
            updateBulkTaxonomySelectedCount();
            return;
        }

        bulkTaxonomyPosts.forEach(post => {
            $tbody.append(`
                <tr class="bulk-taxonomy-post-row" data-post-id="${post.id}" data-title="${post.title.toLowerCase()}">
                    <td style="text-align:center; vertical-align:middle;">
                        <input type="checkbox" class="wpsai-bulk-taxonomy-post-checkbox" value="${post.id}">
                    </td>
                    <td><code>${post.id}</code></td>
                    <td><a href="${post.permalink}" target="_blank"><strong>${post.title}</strong></a></td>
                    <td id="wpsai-tax-current-${post.id}" class="wpsai-current-taxonomies-cell" style="color: var(--wpsai-text-muted); font-size:12px;">-- Chọn Taxonomy để xem --</td>
                    <td><span style="font-size:12px; color:var(--wpsai-text-muted);">${post.post_date}</span></td>
                </tr>
            `);
        });

        updateBulkTaxonomySelectedCount();
    }

    // Tìm kiếm bài viết nhanh client-side
    $('#wpsai-bulk-taxonomy-search').on('input', function () {
        const query = $(this).val().toLowerCase().trim();
        if (!query) {
            $('.bulk-taxonomy-post-row').show();
            return;
        }
        $('.bulk-taxonomy-post-row').each(function () {
            const title = $(this).data('title');
            if (title.indexOf(query) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Checkbox chọn tất cả
    $('#wpsai-bulk-taxonomy-select-all').on('change', function () {
        const checked = $(this).is(':checked');
        $('.wpsai-bulk-taxonomy-post-checkbox:visible').prop('checked', checked);
        updateBulkTaxonomySelectedCount();
    });

    // Sự kiện check từng dòng
    $(document).on('change', '.wpsai-bulk-taxonomy-post-checkbox', function () {
        updateBulkTaxonomySelectedCount();
    });

    function updateBulkTaxonomySelectedCount() {
        const total = $('.wpsai-bulk-taxonomy-post-checkbox').length;
        const selected = $('.wpsai-bulk-taxonomy-post-checkbox:checked').length;
        $('#wpsai-bulk-taxonomy-selected-count').text(`Đã chọn: ${selected}/${total} bài viết`);
        
        if (selected === total && total > 0) {
            $('#wpsai-bulk-taxonomy-select-all').prop('checked', true);
        } else {
            $('#wpsai-bulk-taxonomy-select-all').prop('checked', false);
        }

        if ($('#wpsai-bulk-taxonomy-select').val()) {
            $('#wpsai-bulk-taxonomy-config-card').fadeIn();
            $('#wpsai-bulk-taxonomy-mode-card').fadeIn();
            $('#wpsai-bulk-taxonomy-execute-card').fadeIn();
        }
    }

    // Khi chọn Taxonomy thay đổi
    $('#wpsai-bulk-taxonomy-select').on('change', function () {
        const taxonomy = $(this).val();
        const $termsWrapper = $('#wpsai-bulk-taxonomy-existing-terms');

        if (!taxonomy) {
            $termsWrapper.empty().html('<p style="color: var(--wpsai-text-muted); font-style: italic;">Vui lòng chọn Taxonomy trước để tải danh sách.</p>');
            $('#wpsai-bulk-taxonomy-config-card').hide();
            $('#wpsai-bulk-taxonomy-mode-card').hide();
            $('#wpsai-bulk-taxonomy-execute-card').hide();
            return;
        }

        $termsWrapper.empty().html('<p style="color: var(--wpsai-text-muted);">Đang tải danh sách Term...</p>');
        $('#wpsai-bulk-taxonomy-config-card').fadeIn();
        updateBulkTaxonomySelectedCount();

        // 1. Tải danh sách terms hiện có
        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_terms_by_taxonomy',
                nonce: wpsai_params.nonce,
                taxonomy: taxonomy
            },
            success: function (res) {
                if (res.success) {
                    $termsWrapper.empty();
                    if (res.data.length === 0) {
                        $termsWrapper.html('<p style="color: var(--wpsai-text-muted); font-style: italic;">Không có term nào được tạo sẵn.</p>');
                    } else {
                        res.data.forEach(term => {
                            $termsWrapper.append(`
                                <label class="wpsai-checkbox-label" style="display:block; margin-bottom:8px;">
                                    <input type="checkbox" class="wpsai-bulk-taxonomy-term-checkbox" value="${term.term_id}">
                                    <span>${term.name} (${term.count} bài)</span>
                                </label>
                            `);
                        });
                    }
                } else {
                    $termsWrapper.empty().html(`<p style="color:var(--wpsai-error);">Lỗi: ${res.data.message}</p>`);
                }
            },
            error: function () {
                $termsWrapper.empty().html('<p style="color:var(--wpsai-error);">Lỗi kết nối máy chủ khi tải Terms.</p>');
            }
        });

        // 2. Cập nhật cột "Phân Loại Hiện Tại" cho từng dòng bài viết trong bảng
        const postType = $('#wpsai-bulk-taxonomy-post-type').val();
        $('.wpsai-current-taxonomies-cell').text('Đang tải...');

        // Thực hiện quét nhanh để hiển thị các terms hiện tại của các bài viết
        bulkTaxonomyPosts.forEach(post => {
            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_scan_post_fields',
                    nonce: wpsai_params.nonce,
                    post_id: post.id
                },
                success: function (res) {
                    if (res.success) {
                        const taxField = res.data.fields.find(f => f.name === 'tax_' + taxonomy);
                        const displayVal = (taxField && taxField.current_value) ? taxField.current_value : '--';
                        $(`#wpsai-tax-current-${post.id}`).text(displayVal);
                    } else {
                        $(`#wpsai-tax-current-${post.id}`).text('Lỗi quét');
                    }
                },
                error: function () {
                    $(`#wpsai-tax-current-${post.id}`).text('Lỗi kết nối');
                }
            });
        });
    });

    // Thực thi gán phân loại hàng loạt
    $('#wpsai-bulk-taxonomy-start-btn').on('click', function () {
        const selectedPostIds = [];
        $('.wpsai-bulk-taxonomy-post-checkbox:checked').each(function () {
            selectedPostIds.push(parseInt($(this).val()));
        });

        if (selectedPostIds.length === 0) {
            alert('Vui lòng chọn ít nhất một bài viết!');
            return;
        }

        const taxonomy = $('#wpsai-bulk-taxonomy-select').val();
        if (!taxonomy) {
            alert('Vui lòng chọn Taxonomy!');
            return;
        }

        // Thu thập Term IDs được check
        const selectedTermIds = [];
        $('.wpsai-bulk-taxonomy-term-checkbox:checked').each(function () {
            selectedTermIds.push(parseInt($(this).val()));
        });

        const customPath = $('#wpsai-bulk-taxonomy-custom-path').val().trim();
        const mode = $('input[name="wpsai_bulk_taxonomy_mode"]:checked').val();

        if (selectedTermIds.length === 0 && !customPath) {
            if (!confirm('Bạn không chọn term sẵn có nào và cũng không nhập đường dẫn tùy chỉnh. Hành động này sẽ XÓA HẾT các term của bài viết (nếu chọn chế độ gán đè). Bạn có chắc chắn muốn tiếp tục không?')) {
                return;
            }
        }

        // Chuẩn bị hàng đợi thực thi
        const queue = [];
        selectedPostIds.forEach(postId => {
            queue.push({
                postId: postId,
                taxonomy: taxonomy,
                termIds: selectedTermIds,
                customPath: customPath,
                inputType: customPath ? 'custom_path' : 'existing',
                mode: mode
            });
        });

        // Thiết lập giao diện tiến trình
        const $progressCard = $('#wpsai-bulk-taxonomy-progress-card');
        const $progressBar = $('#wpsai-bulk-taxonomy-progress-bar');
        const $progressStats = $('#wpsai-bulk-taxonomy-progress-stats');
        const $log = $('#wpsai-bulk-taxonomy-log');

        $log.empty();
        $progressBar.css('width', '0%').text('0%');
        $progressCard.fadeIn();

        $('html, body').animate({
            scrollTop: $progressCard.offset().top - 40
        }, 500);

        const $btn = $(this);
        $btn.prop('disabled', true).text('Đang xử lý...');

        let currentIndex = 0;
        const total = queue.length;
        let successCount = 0;
        let errorCount = 0;

        function runNextBulkTaxonomy() {
            if (currentIndex >= total) {
                $progressBar.css('width', '100%').text('100%');
                $progressStats.html(`<p style="color:#10b981; font-weight:bold;">Đã hoàn thành gán phân loại! Thành công: ${successCount}. Lỗi: ${errorCount}.</p>`);
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-saved"></span> Bắt Đầu Gán Phân Loại');
                return;
            }

            const item = queue[currentIndex];
            const postObj = bulkTaxonomyPosts.find(p => p.id === item.postId);
            const postTitle = postObj ? postObj.title : 'Bài viết #' + item.postId;

            $log.append(`<p>Đang xử lý ${currentIndex + 1}/${total}: Bài viết <strong>"${postTitle}"</strong> (ID: ${item.postId})...</p>`);
            $log.scrollTop($log[0].scrollHeight);

            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_assign_taxonomy_terms_ajax',
                    nonce: wpsai_params.nonce,
                    post_id: item.postId,
                    taxonomy: item.taxonomy,
                    term_ids: item.termIds,
                    custom_path: item.customPath,
                    input_type: item.inputType,
                    mode: item.mode
                },
                success: function (res) {
                    if (res.success) {
                        successCount++;
                        $log.append(`<p class="log-success" style="margin:0 0 5px 15px;">✓ Thành công! Danh sách Term hiện tại: <strong>${res.data.terms_str}</strong></p>`);
                        
                        // Cập nhật lại cột "Phân Loại Hiện Tại" ngay trên bảng
                        $(`#wpsai-tax-current-${item.postId}`).text(res.data.terms_str);
                    } else {
                        errorCount++;
                        $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi: ${res.data.message || 'Lỗi không xác định'}</p>`);
                    }

                    currentIndex++;
                    const percent = Math.round((currentIndex / total) * 100);
                    $progressBar.css('width', percent + '%').text(percent + '%');
                    $progressStats.html(`<p>Đang xử lý ${currentIndex}/${total}. Thành công: ${successCount}, Lỗi: ${errorCount}</p>`);
                    
                    setTimeout(runNextBulkTaxonomy, 150);
                },
                error: function () {
                    errorCount++;
                    $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi kết nối HTTP.</p>`);
                    
                    currentIndex++;
                    setTimeout(runNextBulkTaxonomy, 150);
                }
            });
        }

        runNextBulkTaxonomy();
    });

    // --- 13. CÀO BÀI VIẾT (WEB SCRAPER) ---
    // Load Taxonomies cho Post Type của Scraper
    $('#wpsai-scraper-post-type').on('change', function () {
        const postType = $(this).val();
        const $taxSelect = $('#wpsai-scraper-taxonomy');
        if (!postType) return;

        $taxSelect.empty().append('<option value="">-- Đang tải Taxonomy --</option>');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_taxonomies_for_post_type',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                $taxSelect.empty();
                $taxSelect.append('<option value="">-- Chọn Taxonomy --</option>');
                if (res.success && res.data.length > 0) {
                    res.data.forEach(tax => {
                        $taxSelect.append(`<option value="${tax.slug}">${tax.label}</option>`);
                    });
                } else {
                    $taxSelect.append('<option value="" disabled>-- Không có Taxonomy nào --</option>');
                }
            },
            error: function () {
                $taxSelect.empty().append('<option value="">-- Lỗi kết nối --</option>');
            }
        });
    });

    // Bấm nút Xem trước nội dung cào
    $('#wpsai-scraper-preview-btn').on('click', function () {
        const url = $('#wpsai-scraper-url').val().trim();
        const titleSel = $('#wpsai-scraper-selector-title').val().trim();
        const contentSel = $('#wpsai-scraper-selector-content').val().trim();
        const imageSel = $('#wpsai-scraper-selector-image').val().trim();
        const removeSel = $('#wpsai-scraper-selector-remove').val().trim();

        if (!url) {
            alert('Vui lòng nhập đường dẫn URL bài viết cần cào!');
            return;
        }

        const $btn = $(this);
        $btn.prop('disabled', true).html('<span class="dashicons dashicons-search"></span> Đang cào dữ liệu...');

        $('#wpsai-scraper-preview-box').hide();
        $('#wpsai-scraper-settings-card').hide();
        $('#wpsai-scraper-execute-card').hide();
        $('#wpsai-scraper-progress-card').hide();

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_scrape_preview',
                nonce: wpsai_params.nonce,
                url: url,
                title_selector: titleSel,
                content_selector: contentSel,
                image_selector: imageSel,
                remove_selector: removeSel
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-search"></span> Xem Trước Nội Dung Cào Được');
                if (res.success) {
                    // Hiển thị tiêu đề
                    $('#wpsai-scraper-preview-title').text(res.data.title || '(Không tìm thấy tiêu đề)');
                    
                    // Hiển thị ảnh đại diện
                    if (res.data.featured_image) {
                        $('#wpsai-scraper-preview-image').attr('src', res.data.featured_image).show();
                        $('#wpsai-scraper-preview-image-url').text(res.data.featured_image);
                    } else {
                        $('#wpsai-scraper-preview-image').hide();
                        $('#wpsai-scraper-preview-image-url').text('Không tìm thấy URL ảnh đại diện.');
                    }

                    // Hiển thị nội dung
                    $('#wpsai-scraper-preview-content').html(res.data.content || '<em>(Không tìm thấy nội dung)</em>');

                    $('#wpsai-scraper-preview-box').fadeIn();
                    $('#wpsai-scraper-settings-card').fadeIn();
                    $('#wpsai-scraper-execute-card').fadeIn();

                    $('html, body').animate({
                        scrollTop: $('#wpsai-scraper-preview-box').offset().top - 40
                    }, 500);
                } else {
                    alert('Lỗi cào dữ liệu: ' + res.data.message);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-search"></span> Xem Trước Nội Dung Cào Được');
                alert('Lỗi kết nối máy chủ khi cào dữ liệu.');
            }
        });
    });

    // Thực thi cào & nhập bài viết
    $('#wpsai-scraper-execute-btn').on('click', function () {
        const url = $('#wpsai-scraper-url').val().trim();
        const titleSel = $('#wpsai-scraper-selector-title').val().trim();
        const contentSel = $('#wpsai-scraper-selector-content').val().trim();
        const imageSel = $('#wpsai-scraper-selector-image').val().trim();
        const removeSel = $('#wpsai-scraper-selector-remove').val().trim();

        const postType = $('#wpsai-scraper-post-type').val();
        const postStatus = $('#wpsai-scraper-post-status').val();
        const taxonomy = $('#wpsai-scraper-taxonomy').val();
        const terms = $('#wpsai-scraper-terms').val().trim();

        if (!url) {
            alert('Vui lòng nhập đường dẫn URL bài viết cần cào!');
            return;
        }

        const $btn = $(this);
        $btn.prop('disabled', true).text('Đang xử lý...');

        const $progressCard = $('#wpsai-scraper-progress-card');
        const $progressBar = $('#wpsai-scraper-progress-bar');
        const $progressStats = $('#wpsai-scraper-progress-stats');
        const $log = $('#wpsai-scraper-log');
        const $successArea = $('#wpsai-scraper-success-area');

        $log.empty();
        $successArea.hide();
        $progressBar.css('width', '10%').text('10%');
        $progressStats.html('<p>Đang chuẩn bị kết nối tới trang web nguồn...</p>');
        $progressCard.fadeIn();

        $log.append('<p>Đang khởi tạo kết nối...</p>');
        $log.append(`<p>URL nguồn: <code>${url}</code></p>`);

        $('html, body').animate({
            scrollTop: $progressCard.offset().top - 40
        }, 500);

        // Gọi cào dữ liệu chính thức và import
        $progressBar.css('width', '40%').text('40%');
        $progressStats.html('<p>Đang tải HTML và phân tích cấu trúc DOM trang web...</p>');
        $log.append('<p>Đang tải nội dung và bóc tách dữ liệu theo bộ chọn...</p>');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_scrape_and_import',
                nonce: wpsai_params.nonce,
                url: url,
                title_selector: titleSel,
                content_selector: contentSel,
                image_selector: imageSel,
                remove_selector: removeSel,
                post_type: postType,
                post_status: postStatus,
                taxonomy: taxonomy,
                terms: terms
            },
            success: function (res) {
                if (res.success) {
                    $progressBar.css('width', '100%').text('100%');
                    $progressStats.html('<p style="color:#10b981; font-weight:bold;">Đã hoàn thành cào và nhập bài viết thành công!</p>');
                    $log.append('<p class="log-success">✓ Cào và bóc tách nội dung HTML thành công.</p>');
                    if (res.data.featured_image) {
                        $log.append('<p class="log-success">✓ Tải và đồng bộ ảnh đại diện thành công vào Media Library.</p>');
                    }
                    if (taxonomy && terms) {
                        $log.append(`<p class="log-success">✓ Đã thiết lập taxonomy "${taxonomy}" với các giá trị: "${terms}".</p>`);
                    }
                    $log.append(`<p class="log-success">✓ Đã tạo bài viết mới thành công. ID bài viết: <strong>${res.data.post_id}</strong></p>`);

                    $('#wpsai-scraper-result-link').attr('href', res.data.permalink);
                    $successArea.fadeIn();
                } else {
                    $progressBar.css('width', '100%').text('100%');
                    $progressStats.html('<p style="color:#ef4444; font-weight:bold;">Thực thi thất bại!</p>');
                    $log.append(`<p class="log-error">✗ Thất bại! Lỗi: ${res.data.message || 'Lỗi không xác định'}</p>`);
                }
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-download"></span> Cào & Đăng Bài Viết Ngay');
            },
            error: function () {
                $progressBar.css('width', '100%').text('100%');
                $progressStats.html('<p style="color:#ef4444; font-weight:bold;">Lỗi hệ thống!</p>');
                $log.append('<p class="log-error">✗ Thất bại! Lỗi kết nối HTTP.</p>');
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-download"></span> Cào & Đăng Bài Viết Ngay');
            }
        });
    });

    // Khi nguồn tham chiếu thay đổi ở Tab Nhân bản
    $(document).on('change', 'input[name="wpsai_duplicate_source_type"]', function () {
        const type = $(this).val();
        if (type === 'direct') {
            $('#wpsai-duplicate-ref-post-group').hide();
            $('#wpsai-duplicate-config-card').fadeIn();
            $('#wpsai-duplicate-execute-card').fadeIn();
        } else {
            $('#wpsai-duplicate-ref-post-group').show();
            const refPostId = $('#wpsai-duplicate-ref-post').val();
            if (refPostId) {
                $('#wpsai-duplicate-config-card').fadeIn();
                $('#wpsai-duplicate-execute-card').fadeIn();
            } else {
                $('#wpsai-duplicate-config-card').hide();
                $('#wpsai-duplicate-execute-card').hide();
            }
        }
    });

    // Khi Post Type thay đổi ở Tab Nhân bản
    $('#wpsai-duplicate-post-type').on('change', function () {
        const postType = $(this).val();
        const $postSelect = $('#wpsai-duplicate-ref-post');
        if (!postType) return;

        const sourceType = $('input[name="wpsai_duplicate_source_type"]:checked').val();

        $postSelect.empty().append('<option value="">-- Đang tải danh sách bài viết --</option>');
        $('#wpsai-duplicate-progress-card').hide();

        if (sourceType === 'direct') {
            $('#wpsai-duplicate-config-card').show();
            $('#wpsai-duplicate-execute-card').show();
        } else {
            $('#wpsai-duplicate-config-card').hide();
            $('#wpsai-duplicate-execute-card').hide();
        }

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_posts_by_post_type',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                $postSelect.empty();
                $postSelect.append('<option value="">-- Chọn bài viết gốc --</option>');
                if (res.success && res.data.length > 0) {
                    res.data.forEach(post => {
                        $postSelect.append(`<option value="${post.id}">${post.title}</option>`);
                    });
                } else {
                    $postSelect.append('<option value="" disabled>-- Chưa có bài viết nào --</option>');
                }
            },
            error: function () {
                $postSelect.empty().append('<option value="">-- Lỗi kết nối --</option>');
            }
        });
    });

    // Khi chọn Bài viết gốc thay đổi ở Tab Nhân bản
    $('#wpsai-duplicate-ref-post').on('change', function () {
        const postId = $(this).val();
        const sourceType = $('input[name="wpsai_duplicate_source_type"]:checked').val();
        
        if (sourceType === 'reference' && postId) {
            $('#wpsai-duplicate-config-card').fadeIn();
            $('#wpsai-duplicate-execute-card').fadeIn();
        } else if (sourceType === 'reference') {
            $('#wpsai-duplicate-config-card').hide();
            $('#wpsai-duplicate-execute-card').hide();
        }
    });

    // Bắt đầu thực thi nhân bản hàng loạt
    $('#wpsai-duplicate-start-btn').on('click', function () {
        const refPostId = parseInt($('#wpsai-duplicate-ref-post').val());
        const postType = $('#wpsai-duplicate-post-type').val();
        const count = parseInt($('#wpsai-duplicate-count').val());
        const mode = $('input[name="wpsai_duplicate_mode"]:checked').val();
        const status = $('#wpsai-duplicate-status').val();
        const sourceType = $('input[name="wpsai_duplicate_source_type"]:checked').val();

        if (sourceType === 'reference' && !refPostId) {
            alert('Vui lòng chọn bài viết gốc để nhân bản!');
            return;
        }

        if (isNaN(count) || count < 2 || count > 10) {
            alert('Vui lòng nhập số lượng nhân bản từ 2 đến 10 bài viết!');
            return;
        }

        const $btn = $(this);
        const $progressCard = $('#wpsai-duplicate-progress-card');
        const $progressBar = $('#wpsai-duplicate-progress-bar');
        const $progressStats = $('#wpsai-duplicate-progress-stats');
        const $log = $('#wpsai-duplicate-log');

        $log.empty();
        $progressBar.css('width', '0%').text('0%');
        $progressCard.fadeIn();

        $('html, body').animate({
            scrollTop: $progressCard.offset().top - 40
        }, 500);

        $btn.prop('disabled', true).text('Đang xử lý...');

        function proceedToGeneration(fields) {
            $log.append(`<p class="log-success">✓ Đã xác định ${fields.length} trường dữ liệu để sinh.</p>`);
            $progressBar.css('width', '20%').text('20%');
            $progressStats.html('<p>Đang sinh nội dung nhân bản mới...</p>');
            $log.append('<p>Đang gửi yêu cầu sinh nội dung mới lên máy chủ (có thể mất vài giây)...</p>');

            // Bước 2: Sinh dữ liệu mới
            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_generate_mock_data',
                    nonce: wpsai_params.nonce,
                    post_type: postType,
                    count: count,
                    mode: mode,
                    ref_post_id: sourceType === 'direct' ? 0 : refPostId,
                    gen_type: 'new',
                    fields: JSON.stringify(fields)
                },
                success: function (genRes) {
                    if (genRes.success) {
                        const rows = genRes.data.rows;
                        $log.append(`<p class="log-success">✓ Đã sinh thành công ${rows.length} bản ghi dữ liệu mới.</p>`);
                        $progressBar.css('width', '45%').text('45%');
                        $progressStats.html('<p>Đang tiến hành tạo các bài viết mới trên WordPress...</p>');

                        // Tạo identity mapping
                        const mapping = {};
                        fields.forEach(f => {
                            mapping[f.name] = f.name;
                        });

                        // Chạy vòng lặp lưu các bài viết mới
                        let currentIndex = 0;
                        const totalRows = rows.length;
                        let successCount = 0;
                        let errorCount = 0;

                        function runNextDuplicate() {
                            if (currentIndex >= totalRows) {
                                $progressBar.css('width', '100%').text('100%');
                                $progressStats.html(`<p style="color:#10b981; font-weight:bold;">Đã hoàn thành! Thành công: ${successCount}. Thất bại: ${errorCount}.</p>`);
                                $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-page"></span> Bắt Đầu Nhân Bản Hàng Loạt');
                                return;
                            }

                            const row = rows[currentIndex];
                            const displayTitle = row['post_title'] || 'Bản sao #' + (currentIndex + 1);

                            $log.append(`<p>Đang chèn bài viết ${currentIndex + 1}/${totalRows}: <strong>"${displayTitle}"</strong>...</p>`);
                            $log.scrollTop($log[0].scrollHeight);

                            $.ajax({
                                url: wpsai_params.ajax_url,
                                type: 'POST',
                                data: {
                                    action: 'wpsai_import_row',
                                    nonce: wpsai_params.nonce,
                                    row: row,
                                    mapping: mapping,
                                    post_type: postType,
                                    post_status: status
                                },
                                success: function (importRes) {
                                    if (importRes.success) {
                                        successCount++;
                                        $log.append(`<p class="log-success" style="margin:0 0 5px 15px;">✓ Tạo bài viết thành công! ID: <a href="${importRes.data.permalink}" target="_blank">${importRes.data.post_id}</a> - ${importRes.data.title}</p>`);
                                    } else {
                                        errorCount++;
                                        $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi: ${importRes.data.message}</p>`);
                                    }

                                    currentIndex++;
                                    const percent = 45 + Math.round((currentIndex / totalRows) * 55);
                                    $progressBar.css('width', percent + '%').text(percent + '%');
                                    $progressStats.html(`<p>Đang chèn ${currentIndex}/${totalRows}. Thành công: ${successCount}, Lỗi: ${errorCount}</p>`);

                                    setTimeout(runNextDuplicate, 150);
                                },
                                error: function () {
                                    errorCount++;
                                    $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi kết nối HTTP khi tạo bài viết.</p>`);
                                    currentIndex++;
                                    setTimeout(runNextDuplicate, 150);
                                }
                            });
                        }

                        runNextDuplicate();

                    } else {
                        $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-page"></span> Bắt Đầu Nhân Bản Hàng Loạt');
                        $log.append(`<p class="log-error">✗ Lỗi sinh dữ liệu: ${genRes.data.message}</p>`);
                    }
                },
                error: function () {
                    $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-page"></span> Bắt Đầu Nhân Bản Hàng Loạt');
                    $log.append('<p class="log-error">✗ Lỗi kết nối HTTP khi sinh dữ liệu nhân bản.</p>');
                }
            });
        }

        if (sourceType === 'direct') {
            $log.append('<p><strong>Đang chuẩn bị cấu trúc trường trực tiếp...</strong></p>');
            let fields = [];
            const ptObj = postTypesAndFields.find(pt => pt.slug === postType);
            if (ptObj) {
                if (ptObj.core_fields) {
                    ptObj.core_fields.forEach(f => {
                        fields.push({
                            name: f.name,
                            label: f.label,
                            type: f.type
                        });
                    });
                }
                if (ptObj.acf_fields) {
                    ptObj.acf_fields.forEach(f => {
                        fields.push({
                            name: f.name,
                            label: f.label,
                            type: f.type
                        });
                    });
                }
            }

            if (fields.length === 0) {
                fields = [
                    { name: 'post_title', type: 'wp_core', label: 'Tiêu đề' },
                    { name: 'post_content', type: 'wp_core', label: 'Nội dung' },
                    { name: 'post_excerpt', type: 'wp_core', label: 'Mô tả ngắn' },
                    { name: 'post_date', type: 'wp_core', label: 'Ngày đăng' },
                    { name: 'featured_image', type: 'wp_core', label: 'Ảnh đại diện' }
                ];
            }

            proceedToGeneration(fields);
        } else {
            $log.append(`<p><strong>Bắt đầu quét cấu trúc trường bài viết gốc (ID: ${refPostId})...</strong></p>`);

            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_scan_post_fields',
                    nonce: wpsai_params.nonce,
                    post_id: refPostId
                },
                success: function (scanRes) {
                    if (scanRes.success) {
                        const fields = scanRes.data.fields;
                        $log.append(`<p class="log-success">✓ Quét trường thành công. Đã phát hiện ${fields.length} trường dữ liệu cần nhân bản.</p>`);
                        proceedToGeneration(fields);
                    } else {
                        $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-page"></span> Bắt Đầu Nhân Bản Hàng Loạt');
                        $log.append(`<p class="log-error">✗ Lỗi quét bài viết gốc: ${scanRes.data.message}</p>`);
                    }
                },
                error: function () {
                    $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-page"></span> Bắt Đầu Nhân Bản Hàng Loạt');
                    $log.append('<p class="log-error">✗ Lỗi kết nối HTTP khi quét bài viết chuẩn.</p>');
                }
            });
        }
    });

    // =========================================================================

    // --- 14. XỬ LÝ NHẬP EXCEL VÀO BÀI VIẾT CHỌN (BULK EXCEL TAB) ---
    // =========================================================================
    let bulkExcelPosts = [];       // Danh sách bài viết đầy đủ
    let bulkExcelRows = [];        // Dữ liệu dòng Excel nạp được
    let bulkExcelHeaders = [];     // Tiêu đề cột Excel

    // Khi chọn Post Type thay đổi trong Tab Nhập Excel Hàng Loạt
    $('#wpsai-bulk-excel-post-type').on('change', function () {
        const postType = $(this).val();
        if (!postType) return;

        const $postsWrapper = $('#wpsai-bulk-excel-posts-wrapper');
        const $tbody = $('#wpsai-bulk-excel-posts-table tbody');
        
        $postsWrapper.show();
        $tbody.empty().append('<tr><td colspan="5" style="text-align:center;">Đang tải danh sách bài viết...</td></tr>');
        $('#wpsai-bulk-excel-search').val('');
        $('#wpsai-bulk-excel-select-all').prop('checked', false);

        // Ẩn các bước sau khi tải lại Post Type
        $('#wpsai-bulk-excel-upload-card').hide();
        $('#wpsai-bulk-excel-mapping-card').hide();
        $('#wpsai-bulk-excel-execute-card').hide();
        $('#wpsai-bulk-excel-progress-card').hide();

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_posts_for_bulk_images',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                if (res.success) {
                    bulkExcelPosts = res.data;
                    renderBulkExcelPostsTable();
                    $('#wpsai-bulk-excel-upload-card').fadeIn();
                } else {
                    $tbody.empty().append(`<tr><td colspan="5" style="text-align:center; color:var(--wpsai-error);">Lỗi: ${res.data.message}</td></tr>`);
                }
            },
            error: function () {
                $tbody.empty().append('<tr><td colspan="5" style="text-align:center; color:var(--wpsai-error);">Lỗi kết nối máy chủ.</td></tr>');
            }
        });
    });

    // Render bảng danh sách bài viết trong Tab Nhập Excel Hàng Loạt
    function renderBulkExcelPostsTable() {
        const $tbody = $('#wpsai-bulk-excel-posts-table tbody');
        $tbody.empty();

        if (bulkExcelPosts.length === 0) {
            $tbody.append('<tr><td colspan="5" style="text-align:center;">Không tìm thấy bài viết nào.</td></tr>');
            updateBulkExcelSelectedCount();
            return;
        }

        bulkExcelPosts.forEach(post => {
            const thumbHtml = post.thumb_url 
                ? `<img src="${post.thumb_url}" class="wpsai-post-list-thumb" data-post-id="${post.id}" />` 
                : `<div class="wpsai-post-list-thumb" data-post-id="${post.id}" style="display:flex; align-items:center; justify-content:center; color:#94a3b8;"><span class="dashicons dashicons-format-image" style="font-size:24px; width:24px; height:24px;"></span></div>`;

            $tbody.append(`
                <tr class="bulk-excel-post-row" data-post-id="${post.id}" data-title="${post.title.toLowerCase()}">
                    <td style="text-align:center; vertical-align:middle;">
                        <input type="checkbox" class="wpsai-bulk-excel-post-checkbox" value="${post.id}">
                    </td>
                    <td>${thumbHtml}</td>
                    <td><code>${post.id}</code></td>
                    <td><a href="${post.permalink}" target="_blank"><strong>${post.title}</strong></a></td>
                    <td><span style="font-size:12px; color:var(--wpsai-text-muted);">${post.post_date}</span></td>
                </tr>
            `);
        });

        updateBulkExcelSelectedCount();
    }

    // Tìm kiếm bài viết nhanh client-side
    $('#wpsai-bulk-excel-search').on('input', function () {
        const query = $(this).val().toLowerCase().trim();
        if (!query) {
            $('.bulk-excel-post-row').show();
            return;
        }
        $('.bulk-excel-post-row').each(function () {
            const title = $(this).data('title');
            if (title.indexOf(query) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Checkbox chọn tất cả
    $('#wpsai-bulk-excel-select-all').on('change', function () {
        const checked = $(this).is(':checked');
        $('.wpsai-bulk-excel-post-checkbox:visible').prop('checked', checked);
        updateBulkExcelSelectedCount();
    });

    // Sự kiện check từng dòng
    $(document).on('change', '.wpsai-bulk-excel-post-checkbox', function () {
        updateBulkExcelSelectedCount();
    });

    function updateBulkExcelSelectedCount() {
        const total = $('.wpsai-bulk-excel-post-checkbox').length;
        const selected = $('.wpsai-bulk-excel-post-checkbox:checked').length;
        $('#wpsai-bulk-excel-selected-count').text(`Đã chọn: ${selected}/${total} bài viết`);
        
        if (selected === total && total > 0) {
            $('#wpsai-bulk-excel-select-all').prop('checked', true);
        } else {
            $('#wpsai-bulk-excel-select-all').prop('checked', false);
        }
    }

    // Đọc Excel / CSV cho bulk-excel
    const bulkExcelDropZone = document.getElementById('wpsai-bulk-excel-drop-zone');
    const bulkExcelFileInput = document.getElementById('wpsai-bulk-excel-file');
    const bulkExcelBrowseBtn = document.getElementById('wpsai-bulk-excel-browse-btn');

    if (bulkExcelBrowseBtn) {
        bulkExcelBrowseBtn.addEventListener('click', () => bulkExcelFileInput.click());
    }
    if (bulkExcelFileInput) {
        bulkExcelFileInput.addEventListener('change', handleBulkExcelUpload);
    }

    if (bulkExcelDropZone) {
        ['dragenter', 'dragover'].forEach(eventName => {
            bulkExcelDropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                bulkExcelDropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            bulkExcelDropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                bulkExcelDropZone.classList.remove('dragover');
            }, false);
        });

        bulkExcelDropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length) {
                bulkExcelFileInput.files = files;
                handleBulkExcelUpload({ target: { files: files } });
            }
        });
    }

    function handleBulkExcelUpload(e) {
        const file = e.target.files[0];
        if (!file) return;

        $('#wpsai-bulk-excel-drop-zone').hide();
        $('#wpsai-bulk-excel-file-info').show().find('.wpsai-filename').text(file.name + ' (' + Math.round(file.size / 1024) + ' KB)');

        const reader = new FileReader();
        reader.onload = function (e) {
            const data = new Uint8Array(e.target.result);
            try {
                const workbook = XLSX.read(data, { type: 'array' });
                const firstSheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheetName];
                const rawSheetData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
                processBulkExcel2DArray(rawSheetData);
            } catch (err) {
                alert('Không thể đọc file Excel. Vui lòng kiểm tra lại.');
                console.error(err);
                $('#wpsai-bulk-excel-remove-file').trigger('click');
            }
        };
        reader.readAsArrayBuffer(file);
    }

    function processBulkExcel2DArray(matrix) {
        const cleanMatrix = matrix.filter(row => row.length > 0 && row.some(cell => cell !== undefined && cell !== ''));
        if (cleanMatrix.length < 2) {
            alert('Dữ liệu yêu cầu tối thiểu 1 hàng tiêu đề và 1 hàng nội dung.');
            return;
        }

        bulkExcelHeaders = cleanMatrix[0].map((h, index) => (h && h.trim()) ? h.trim() : 'Cột ' + (index + 1));

        bulkExcelRows = [];
        for (let i = 1; i < cleanMatrix.length; i++) {
            const rowObj = {};
            bulkExcelHeaders.forEach((header, colIndex) => {
                rowObj['col_' + colIndex] = cleanMatrix[i][colIndex] !== undefined ? cleanMatrix[i][colIndex] : '';
            });
            bulkExcelRows.push(rowObj);
        }

        // Cập nhật các select mapping
        const $selects = $('.wpsai-bulk-excel-map-select');
        $selects.each(function () {
            const $select = $(this);
            $select.empty().append('<option value="">-- Bỏ qua không cập nhật --</option>');
            bulkExcelHeaders.forEach((header, colIndex) => {
                $select.append(`<option value="col_${colIndex}">${header}</option>`);
            });
        });

        // Tự động ánh xạ khớp tên cột thông minh
        $selects.each(function () {
            const $select = $(this);
            const field = $select.data('field');
            let matchedValue = '';

            bulkExcelHeaders.forEach((header, colIndex) => {
                const headerLower = header.toLowerCase();
                if (field === 'post_title' && (headerLower.indexOf('tiêu đề') !== -1 || headerLower.indexOf('title') !== -1)) {
                    matchedValue = 'col_' + colIndex;
                } else if (field === 'post_content' && (headerLower.indexOf('nội dung') !== -1 || headerLower.indexOf('content') !== -1)) {
                    matchedValue = 'col_' + colIndex;
                } else if (field === 'original_url' && (headerLower.indexOf('đường dẫn gốc') !== -1 || headerLower.indexOf('link') !== -1 || headerLower.indexOf('url') !== -1 || headerLower.indexOf('original') !== -1 || headerLower.indexOf('path') !== -1)) {
                    matchedValue = 'col_' + colIndex;
                } else if (field === 'featured_image' && (headerLower.indexOf('ảnh') !== -1 || headerLower.indexOf('hình ảnh') !== -1 || headerLower.indexOf('image') !== -1 || headerLower.indexOf('img') !== -1 || headerLower.indexOf('thumbnail') !== -1 || headerLower.indexOf('featured') !== -1)) {
                    matchedValue = 'col_' + colIndex;
                }
            });

            if (matchedValue) {
                $select.val(matchedValue);
            }
        });

        $('#wpsai-bulk-excel-mapping-card').fadeIn();
        $('#wpsai-bulk-excel-execute-card').fadeIn();
    }

    $('#wpsai-bulk-excel-remove-file').on('click', function () {
        document.getElementById('wpsai-bulk-excel-file').value = '';
        $('#wpsai-bulk-excel-file-info').hide();
        $('#wpsai-bulk-excel-drop-zone').fadeIn();
        
        bulkExcelRows = [];
        bulkExcelHeaders = [];
        $('#wpsai-bulk-excel-mapping-card').hide();
        $('#wpsai-bulk-excel-execute-card').hide();
        $('#wpsai-bulk-excel-progress-card').hide();
    });

    // Toggle nguồn dữ liệu trong bulk-excel (Tải file vs Dán văn bản)
    $('input[name="wpsai_bulk_source_mode"]').on('change', function () {
        const mode = $(this).val();
        $('.wpsai-bulk-source-option').removeClass('active');
        $(this).closest('.wpsai-bulk-source-option').addClass('active');

        if (mode === 'file') {
            $('#wpsai-bulk-source-paste-wrapper').hide();
            $('#wpsai-bulk-source-file-wrapper').fadeIn();
        } else {
            $('#wpsai-bulk-source-file-wrapper').hide();
            $('#wpsai-bulk-source-paste-wrapper').fadeIn();
        }

        // Reset state dữ liệu hiện tại
        bulkExcelRows = [];
        bulkExcelHeaders = [];
        $('#wpsai-bulk-excel-mapping-card').hide();
        $('#wpsai-bulk-excel-execute-card').hide();
        $('#wpsai-bulk-excel-progress-card').hide();

        // Clear file input
        document.getElementById('wpsai-bulk-excel-file').value = '';
        $('#wpsai-bulk-excel-file-info').hide();
        $('#wpsai-bulk-excel-drop-zone').show();

        // Reset paste input
        $('#wpsai-bulk-paste-clear-btn').hide();
        $('#wpsai-bulk-paste-load-btn').show();
    });

    // Toggle kiểu dán văn bản (TSV vs Tách riêng)
    $('input[name="wpsai_bulk_paste_type"]').on('change', function () {
        const type = $(this).val();
        if (type === 'tsv') {
            $('#wpsai-bulk-paste-separate-group').hide();
            $('#wpsai-bulk-paste-tsv-group').fadeIn();
        } else {
            $('#wpsai-bulk-paste-tsv-group').hide();
            $('#wpsai-bulk-paste-separate-group').fadeIn();
        }
    });

    // Xử lý nạp văn bản dán trực tiếp
    $('#wpsai-bulk-paste-load-btn').on('click', function () {
        const pasteType = $('input[name="wpsai_bulk_paste_type"]:checked').val();
        let matrix = [];

        if (pasteType === 'tsv') {
            const rawText = $('#wpsai-bulk-paste-tsv-raw').val().trim();
            if (!rawText) {
                alert('Vui lòng dán dữ liệu dạng bảng từ Excel hoặc Google Sheets!');
                return;
            }
            matrix = parseTSVData(rawText);
        } else {
            const titlesRaw = $('#wpsai-bulk-paste-titles').val().trim();
            const contentsRaw = $('#wpsai-bulk-paste-contents').val().trim();
            const delimiter = $('#wpsai-bulk-paste-separator').val().trim() || '[split]';

            if (!titlesRaw && !contentsRaw) {
                alert('Vui lòng nhập danh sách Tiêu đề hoặc danh sách Nội dung!');
                return;
            }

            const titles = titlesRaw ? titlesRaw.split(/\r?\n/).map(t => t.trim()).filter(t => t !== '') : [];
            let contents = [];

            if (contentsRaw) {
                const escapedDelimiter = delimiter.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
                contents = contentsRaw.split(new RegExp('\\r?\\n?' + escapedDelimiter + '\\r?\\n?')).map(c => c.trim()).filter(c => c !== '');
            }

            const maxLen = Math.max(titles.length, contents.length);
            if (maxLen === 0) {
                alert('Không tìm thấy dữ liệu hợp lệ để nạp.');
                return;
            }

            // Tạo cấu trúc mảng 2D giống như Excel nạp vào
            if (titles.length > 0) {
                matrix.push(['Tiêu đề bài viết (Title)', 'Nội dung chi tiết (Content)']);
                for (let i = 0; i < maxLen; i++) {
                    matrix.push([
                        titles[i] || '',
                        contents[i] || ''
                    ]);
                }
            } else {
                matrix.push(['Nội dung chi tiết (Content)']);
                for (let i = 0; i < maxLen; i++) {
                    matrix.push([
                        contents[i] || ''
                    ]);
                }
            }
        }

        if (matrix.length < 2) {
            alert('Dữ liệu yêu cầu tối thiểu có tiêu đề cột và ít nhất một dòng nội dung.');
            return;
        }

        // Tái sử dụng hàm nạp mảng 2D có sẵn của plugin
        processBulkExcel2DArray(matrix);

        // Chuyển nút bấm
        $('#wpsai-bulk-paste-load-btn').hide();
        $('#wpsai-bulk-paste-clear-btn').fadeIn();
    });

    // Xóa dữ liệu dán trực tiếp
    $('#wpsai-bulk-paste-clear-btn').on('click', function () {
        $('#wpsai-bulk-paste-tsv-raw').val('');
        $('#wpsai-bulk-paste-titles').val('');
        $('#wpsai-bulk-paste-contents').val('');

        bulkExcelRows = [];
        bulkExcelHeaders = [];
        $('#wpsai-bulk-excel-mapping-card').hide();
        $('#wpsai-bulk-excel-execute-card').hide();
        $('#wpsai-bulk-excel-progress-card').hide();

        $('#wpsai-bulk-paste-clear-btn').hide();
        $('#wpsai-bulk-paste-load-btn').fadeIn();
    });

    // Hàm parser phân tích dữ liệu dạng TSV (bôi đen dán từ Excel/Google Sheets)
    function parseTSVData(text) {
        const lines = [];
        let row = [""];
        let inQuotes = false;

        for (let i = 0; i < text.length; i++) {
            let c = text[i];
            let next = text[i+1];

            if (c === '"') {
                if (inQuotes && next === '"') {
                    row[row.length - 1] += '"';
                    i++;
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (c === '\t' && !inQuotes) {
                row.push("");
            } else if ((c === '\r' || c === '\n') && !inQuotes) {
                if (c === '\r' && next === '\n') { i++; }
                lines.push(row);
                row = [""];
            } else {
                row[row.length - 1] += c;
            }
        }
        if (row.length > 1 || row[0] !== "") {
            lines.push(row);
        }

        return lines;
    }

    // Bắt đầu cập nhật hàng loạt từ Excel hoặc Văn bản dán
    $('#wpsai-bulk-excel-start-btn').on('click', function () {
        // Thu thập post_ids được check
        const selectedPostIds = [];
        $('.wpsai-bulk-excel-post-checkbox:checked').each(function () {
            selectedPostIds.push(parseInt($(this).val()));
        });

        if (selectedPostIds.length === 0) {
            alert('Vui lòng chọn ít nhất một bài viết để cập nhật!');
            return;
        }

        if (bulkExcelRows.length === 0) {
            alert('Vui lòng cung cấp dữ liệu nguồn ở Bước 2!');
            return;
        }

        // Lấy mapping
        const mapping = {};
        let hasMapping = false;
        $('.wpsai-bulk-excel-map-select').each(function () {
            const field = $(this).data('field');
            const val = $(this).val();
            if (val) {
                mapping[field] = val;
                hasMapping = true;
            }
        });

        if (!hasMapping) {
            alert('Vui lòng ánh xạ ít nhất một trường để cập nhật!');
            return;
        }

        // Giao diện tiến trình
        const $progressCard = $('#wpsai-bulk-excel-progress-card');
        const $progressBar = $('#wpsai-bulk-excel-progress-bar');
        const $progressStats = $('#wpsai-bulk-excel-progress-stats');
        const $log = $('#wpsai-bulk-excel-log');

        $log.empty();
        $progressBar.css('width', '0%').text('0%');
        $progressCard.fadeIn();

        $('html, body').animate({
            scrollTop: $progressCard.offset().top - 40
        }, 500);

        const $btn = $(this);
        $btn.prop('disabled', true);

        // Chuẩn bị hàng đợi cập nhật
        const queue = [];
        selectedPostIds.forEach((postId, idx) => {
            // Lấy dòng tương ứng tuần hoàn (giống cách phân phối sequential của ảnh)
            const excelRowIndex = idx % bulkExcelRows.length;
            const excelRow = bulkExcelRows[excelRowIndex];

            const updateData = {
                post_id: postId,
                post_title: mapping['post_title'] ? excelRow[mapping['post_title']] : '',
                post_content: mapping['post_content'] ? excelRow[mapping['post_content']] : '',
                original_url: mapping['original_url'] ? excelRow[mapping['original_url']] : '',
                featured_image: mapping['featured_image'] ? excelRow[mapping['featured_image']] : '',
            };

            queue.push(updateData);
        });

        let currentIndex = 0;
        const total = queue.length;
        let successCount = 0;
        let errorCount = 0;

        function runNextBulkExcel() {
            if (currentIndex >= total) {
                $progressBar.css('width', '100%').text('100%');
                $progressStats.html(`<p style="color:#10b981; font-weight:bold;">Đã hoàn thành cập nhật! Thành công: ${successCount}. Lỗi: ${errorCount}.</p>`);
                $btn.prop('disabled', false);
                return;
            }

            const item = queue[currentIndex];
            const postObj = bulkExcelPosts.find(p => p.id === item.post_id);
            const postTitle = postObj ? postObj.title : 'Bài viết #' + item.post_id;

            $log.append(`<p>Đang cập nhật ${currentIndex + 1}/${total}: Bài viết <strong>"${postTitle}"</strong> (ID: ${item.post_id})...</p>`);
            $log.scrollTop($log[0].scrollHeight);

            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_bulk_excel_update_row',
                    nonce: wpsai_params.nonce,
                    post_id: item.post_id,
                    post_title: item.post_title,
                    post_content: item.post_content,
                    original_url: item.original_url,
                    featured_image: item.featured_image
                },
                success: function (res) {
                    if (res.success) {
                        successCount++;
                        $log.append(`<p class="log-success" style="margin:0 0 5px 15px;">✓ Thành công! Đã cập nhật bài viết ID: ${item.post_id}</p>`);
                        
                        // Cập nhật thumbnail trong bảng nếu có
                        if (res.data && res.data.thumb_url) {
                            const $thumbCell = $(`.bulk-excel-post-row[data-post-id="${item.post_id}"] .wpsai-post-list-thumb`);
                            if ($thumbCell.length) {
                                if ($thumbCell.is('img')) {
                                    $thumbCell.attr('src', res.data.thumb_url);
                                } else {
                                    const newImg = `<img src="${res.data.thumb_url}" class="wpsai-post-list-thumb" data-post-id="${item.post_id}" />`;
                                    $thumbCell.replaceWith(newImg);
                                }
                            }
                        }
                    } else {
                        errorCount++;
                        $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi: ${res.data.message || 'Lỗi không xác định'}</p>`);
                    }

                    currentIndex++;
                    const percent = Math.round((currentIndex / total) * 100);
                    $progressBar.css('width', percent + '%').text(percent + '%');
                    $progressStats.html(`<p>Đang cập nhật bài viết ${currentIndex}/${total}. Thành công: ${successCount}, Lỗi: ${errorCount}</p>`);
                    
                    setTimeout(runNextBulkExcel, 150);
                },
                error: function () {
                    errorCount++;
                    $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi kết nối HTTP.</p>`);
                    
                    currentIndex++;
                    setTimeout(runNextBulkExcel, 150);
                }
            });
        }

        runNextBulkExcel();
    });

    // --- 16. XỬ LÝ TẠO NỘI DUNG AI (AI GENERATOR TAB) ---
    let aiGeneratorPosts = []; // Danh sách bài viết đầy đủ của Post Type đang chọn

    $('#wpsai-ai-generator-post-type').on('change', function () {
        const postType = $(this).val();
        const $tbody = $('#wpsai-ai-generator-posts-table tbody');
        if (!postType) return;

        $tbody.empty().append('<tr><td colspan="5" style="text-align:center;">Đang tải danh sách bài viết...</td></tr>');
        $('#wpsai-ai-generator-posts-wrapper').fadeIn();
        $('#wpsai-ai-generator-search').val('');
        $('#wpsai-ai-generator-select-all').prop('checked', false);

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_posts_for_bulk_images', // Dùng lại API lấy bài viết gọn gàng
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                if (res.success) {
                    aiGeneratorPosts = res.data;
                    renderAiGeneratorPostsTable();
                } else {
                    $tbody.empty().append(`<tr><td colspan="5" style="text-align:center; color:#dc3232;">Lỗi: ${res.data.message}</td></tr>`);
                }
            },
            error: function () {
                $tbody.empty().append('<tr><td colspan="5" style="text-align:center; color:#dc3232;">Lỗi kết nối máy chủ.</td></tr>');
            }
        });
    });

    function renderAiGeneratorPostsTable() {
        const $tbody = $('#wpsai-ai-generator-posts-table tbody');
        $tbody.empty();

        if (aiGeneratorPosts.length === 0) {
            $tbody.append('<tr><td colspan="5" style="text-align:center;">Không tìm thấy bài viết nào của Post Type này.</td></tr>');
            updateAiGeneratorSelectedCount();
            return;
        }

        aiGeneratorPosts.forEach(post => {
            let thumbHtml = '<span class="dashicons dashicons-format-image" style="font-size:24px; color:#888;"></span>';
            if (post.thumb_url) {
                thumbHtml = `<img src="${post.thumb_url}" class="wpsai-post-list-thumb" data-post-id="${post.id}" />`;
            }

            const row = `
                <tr class="ai-generator-post-row" data-post-id="${post.id}" data-title="${post.title.toLowerCase()}">
                    <td style="text-align:center; vertical-align:middle;">
                        <input type="checkbox" class="wpsai-ai-generator-post-checkbox" value="${post.id}">
                    </td>
                    <td style="vertical-align:middle; text-align:center;">${thumbHtml}</td>
                    <td style="vertical-align:middle; font-weight:600;">${post.id}</td>
                    <td style="vertical-align:middle;"><strong>${post.title}</strong></td>
                    <td style="vertical-align:middle; color:#64748b;">${post.date}</td>
                </tr>
            `;
            $tbody.append(row);
        });

        updateAiGeneratorSelectedCount();
    }

    // Lọc tìm kiếm bài viết
    $('#wpsai-ai-generator-search').on('input', function () {
        const term = $(this).val().toLowerCase().trim();
        if (term === '') {
            $('.ai-generator-post-row').show();
            return;
        }

        $('.ai-generator-post-row').each(function () {
            const title = $(this).data('title').toString();
            const id = $(this).data('post-id').toString();
            if (title.indexOf(term) !== -1 || id.indexOf(term) !== -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Checkbox chọn tất cả
    $('#wpsai-ai-generator-select-all').on('change', function () {
        const checked = $(this).is(':checked');
        $('.wpsai-ai-generator-post-checkbox:visible').prop('checked', checked);
        updateAiGeneratorSelectedCount();
    });

    $(document).on('change', '.wpsai-ai-generator-post-checkbox', function () {
        updateAiGeneratorSelectedCount();
    });

    function updateAiGeneratorSelectedCount() {
        const total = $('.wpsai-ai-generator-post-checkbox').length;
        const selected = $('.wpsai-ai-generator-post-checkbox:checked').length;
        $('#wpsai-ai-generator-selected-count').text(`Đã chọn: ${selected}/${total} bài viết`);
        
        if (total > 0 && selected === total) {
            $('#wpsai-ai-generator-select-all').prop('checked', true);
        } else {
            $('#wpsai-ai-generator-select-all').prop('checked', false);
        }
    }

    // Toggle active card cho radio button
    $('input[name="wpsai_ai_generator_import_mode"]').on('change', function() {
        $('input[name="wpsai_ai_generator_import_mode"]').closest('.wpsai-radio-card').removeClass('active');
        $(this).closest('.wpsai-radio-card').addClass('active');

        // Nếu chuyển sang chế độ cập nhật, khoá tự động đếm tiêu đề
        const mode = $(this).val();
        if (mode === 'update_selected') {
            const selectedCount = $('.wpsai-ai-generator-post-checkbox:checked').length;
            $('#wpsai-ai-generator-count').val(selectedCount);
        } else {
            const titlesText = $('#wpsai-ai-generator-titles').val().trim();
            if (titlesText) {
                const lines = titlesText.split(/\r?\n/).map(t => t.trim()).filter(t => t !== '');
                if (lines.length > 0) {
                    $('#wpsai-ai-generator-count').val(lines.length);
                }
            }
        }
    });

    // Tự động đếm dòng tiêu đề và cập nhật ô Số lượng
    $('#wpsai-ai-generator-titles').on('input change', function () {
        const text = $(this).val().trim();
        const importMode = $('input[name="wpsai_ai_generator_import_mode"]:checked').val();
        if (importMode !== 'update_selected' && text) {
            const lines = text.split(/\r?\n/).map(t => t.trim()).filter(t => t !== '');
            if (lines.length > 0) {
                $('#wpsai-ai-generator-count').val(lines.length);
            }
        }
    });

    // Bắt đầu thực thi AI Generator
    $('#wpsai-ai-generator-start-btn').on('click', function () {
        const postType = $('#wpsai-ai-generator-post-type').val();
        const userTopic = $('#wpsai-ai-generator-topic').val().trim();
        const genCount = parseInt($('#wpsai-ai-generator-count').val());
        const postStatus = $('#wpsai-ai-generator-post-status').val();
        const importMode = $('input[name="wpsai_ai_generator_import_mode"]:checked').val();

        // Thu thập tiêu đề và bố cục bài viết
        const titlesText = $('#wpsai-ai-generator-titles').val().trim();
        const layoutTemplate = $('#wpsai-ai-generator-layout').val().trim();
        
        let customTitles = [];
        if (titlesText) {
            customTitles = titlesText.split(/\r?\n/).map(t => t.trim()).filter(t => t !== '');
        }

        if (!postType) {
            alert('Vui lòng chọn Post Type!');
            return;
        }

        if (!userTopic) {
            alert('Vui lòng điền chủ đề hoặc mô tả ngắn để định hướng AI!');
            return;
        }

        if (isNaN(genCount) || genCount < 1 || genCount > 100) {
            alert('Số lượng dòng cần sinh phải nằm trong khoảng từ 1 đến 100!');
            return;
        }

        // Lấy danh sách các bài viết đã chọn
        const selectedPostIds = [];
        $('.wpsai-ai-generator-post-checkbox:checked').each(function () {
            selectedPostIds.push(parseInt($(this).val()));
        });

        if (importMode === 'update_selected' && selectedPostIds.length === 0) {
            alert('Bạn chọn chế độ "Chỉ Cập Nhật Bài Viết Đã Chọn", vui lòng tích chọn ít nhất 1 bài viết ở Bước 1!');
            return;
        }

        // Tính toán số dòng thực tế cần sinh và số bài cần cập nhật
        let rowsToGenerate = genCount;
        if (importMode === 'update_selected') {
            rowsToGenerate = selectedPostIds.length;
            $('#wpsai-ai-generator-count').val(rowsToGenerate); // Cập nhật lại giao diện
        } else {
            if (customTitles.length > 0) {
                rowsToGenerate = customTitles.length;
                $('#wpsai-ai-generator-count').val(rowsToGenerate);
            }
        }

        // Lấy danh sách các trường (fields) của post type từ cached data
        const ptData = postTypesAndFields.find(pt => pt.slug === postType);
        let fields = [];
        if (ptData) {
            // Tổng hợp fields: core_fields + acf_fields
            fields = [...ptData.core_fields, ...ptData.acf_fields];
        }

        // Chuẩn bị giao diện log và progress
        const $progressCard = $('#wpsai-ai-generator-progress-card');
        const $progressBar = $('#wpsai-ai-generator-progress-bar');
        const $progressStats = $('#wpsai-ai-generator-progress-stats');
        const $log = $('#wpsai-ai-generator-log');

        $log.empty();
        $progressBar.css('width', '0%').text('0%');
        $progressCard.fadeIn();

        $('html, body').animate({
            scrollTop: $progressCard.offset().top - 40
        }, 500);

        const $btn = $(this);
        $btn.prop('disabled', true).text('Đang sinh dữ liệu...');

        // Tiến trình chia batch (mỗi batch sinh 5 dòng)
        const batchSize = 5;
        const totalBatches = Math.ceil(rowsToGenerate / batchSize);
        let currentBatchIndex = 0;
        let generatedRows = [];

        $log.append(`<p style="color:#0284c7; font-weight:bold;">[Khởi tạo] Tổng số dòng cần tạo: ${rowsToGenerate} dòng (Chia làm ${totalBatches} đợt gọi AI)...</p>`);

        function runNextBatch() {
            if (currentBatchIndex >= totalBatches) {
                // Đã sinh xong toàn bộ dữ liệu mẫu từ AI, chuyển sang giai đoạn import
                $log.append(`<p style="color:#10b981; font-weight:bold;">[AI Hoàn tất] Đã nhận đủ ${generatedRows.length} dòng dữ liệu mẫu từ AI. Bắt đầu lưu dữ liệu...</p>`);
                importGeneratedRows(generatedRows);
                return;
            }

            const offset = currentBatchIndex * batchSize;
            const limit = Math.min(batchSize, rowsToGenerate - offset);
            
            // Xác định selectedPostIds và customTitles cho batch này
            let batchSelectedPostIds = [];
            let batchCustomTitles = [];
            let batchGenType = 'new';

            if (importMode === 'update_selected' || importMode === 'update_and_create') {
                batchSelectedPostIds = selectedPostIds.slice(offset, offset + limit);
                if (batchSelectedPostIds.length > 0) {
                    batchGenType = 'existing';
                }
            }

            if (customTitles.length > 0) {
                batchCustomTitles = customTitles.slice(offset, offset + limit);
            }

            $log.append(`<p><strong>[Đợt ${currentBatchIndex + 1}/${totalBatches}]</strong> Đang gọi AI sinh ${limit} dòng dữ liệu cho đợt này...</p>`);
            $log.scrollTop($log[0].scrollHeight);

            // Cập nhật progress giai đoạn gọi AI (tối đa 40%)
            const percentAI = Math.round(((currentBatchIndex) / totalBatches) * 40);
            $progressBar.css('width', percentAI + '%').text(percentAI + '%');
            $progressStats.html(`<p>Đang gọi AI sinh dữ liệu đợt ${currentBatchIndex + 1}/${totalBatches}...</p>`);

            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_bulk_ai_generate',
                    nonce: wpsai_params.nonce,
                    post_type: postType,
                    count: limit,
                    user_topic: userTopic,
                    gen_type: batchGenType,
                    selected_post_ids: batchSelectedPostIds,
                    layout_template: layoutTemplate,
                    custom_titles: batchCustomTitles,
                    fields: JSON.stringify(fields)
                },
                success: function (res) {
                    if (res.success && res.data.rows && res.data.rows.length > 0) {
                        const batchRows = res.data.rows;
                        
                        // Ghép ID bài viết gốc vào dòng dữ liệu nếu là cập nhật
                        if (batchGenType === 'existing') {
                            batchRows.forEach((row, idx) => {
                                if (batchSelectedPostIds[idx]) {
                                    row.post_id = batchSelectedPostIds[idx];
                                }
                            });
                        }

                        generatedRows = generatedRows.concat(batchRows);
                        $log.append(`<p style="color:#16a34a; margin-left:15px;">✓ Đợt ${currentBatchIndex + 1} thành công: Nhận được ${batchRows.length} dòng.</p>`);
                        
                        currentBatchIndex++;
                        setTimeout(runNextBatch, 300);
                    } else {
                        const errMsg = res.data ? res.data.message : 'Lỗi phản hồi không xác định.';
                        $log.append(`<p style="color:#dc3232; font-weight:bold;">✗ Đợt ${currentBatchIndex + 1} thất bại! Lỗi: ${errMsg}</p>`);
                        $log.append(`<p style="color:#dc3232; margin-left:15px;">Đang thử lại đợt ${currentBatchIndex + 1} sau 3 giây...</p>`);
                        $log.scrollTop($log[0].scrollHeight);
                        setTimeout(runNextBatch, 3000); // Thử lại sau 3 giây
                    }
                },
                error: function () {
                    $log.append(`<p style="color:#dc3232; font-weight:bold;">✗ Đợt ${currentBatchIndex + 1} thất bại! Lỗi kết nối HTTP.</p>`);
                    $log.append(`<p style="color:#dc3232; margin-left:15px;">Đang thử lại đợt ${currentBatchIndex + 1} sau 3 giây...</p>`);
                    $log.scrollTop($log[0].scrollHeight);
                    setTimeout(runNextBatch, 3000); // Thử lại sau 3 giây
                }
            });
        }

        function importGeneratedRows(rows) {
            const totalRows = rows.length;
            let currentImportIdx = 0;
            let successCount = 0;
            let errorCount = 0;

            // Kiểm tra xem có Image Pool không
            const hasImagePool = window.wpsaiAiImagePool && window.wpsaiAiImagePool.hasImages();
            let imagePoolIds = hasImagePool ? window.wpsaiAiImagePool.getIds() : [];
            let imageInsertMode = hasImagePool ? window.wpsaiAiImagePool.getMode() : 'sequential';
            let setFeatured = hasImagePool ? window.wpsaiAiImagePool.getSetFeatured() : false;
            let templateSlots = hasImagePool ? window.wpsaiAiImagePool.getSlots() : null;

            if (hasImagePool) {
                $log.append(`<p style="color:#7c3aed; font-weight:bold;">📷 Kho Ảnh Nội Dung: ${imagePoolIds.length} ảnh | Chế độ: ${imageInsertMode} | Featured Image: ${setFeatured ? 'Có' : 'Không'}</p>`);
                if (templateSlots && templateSlots.length > 0) {
                    $log.append(`<p style="color:#7c3aed; margin-left:15px;">Sử dụng cấu trúc bài mẫu: ${templateSlots.length} vị trí ảnh đã phân tích</p>`);
                } else {
                    $log.append(`<p style="color:#7c3aed; margin-left:15px;">Tự động chèn ảnh sau mỗi heading (h2/h3)</p>`);
                }
            }

            // Tạo mapping tương ứng: key trong JSON trùng khớp với key trường
            const mapping = {};
            fields.forEach(f => {
                mapping[f.name] = f.name;
            });
            // Ánh xạ thêm post_id nếu có
            mapping['post_id'] = 'post_id';

            function runNextImport() {
                if (currentImportIdx >= totalRows) {
                    $progressBar.css('width', '100%').text('100%');
                    $progressStats.html(`<p style="color:#10b981; font-weight:bold;">Hoàn tất tiến trình! Thành công: ${successCount}. Lỗi: ${errorCount}.</p>`);
                    $btn.prop('disabled', false).html('<span class="dashicons dashicons-lightbulb"></span> Khởi Chạy Sinh Dữ Liệu AI');
                    
                    // Reload bảng danh sách bài viết
                    $('#wpsai-ai-generator-post-type').trigger('change');
                    return;
                }

                const row = rows[currentImportIdx];
                const displayTitle = row['post_title'] || 'Bài viết mẫu #' + (currentImportIdx + 1);
                const isUpdate = !!row['post_id'];

                if (isUpdate) {
                    $log.append(`<p>Đang cập nhật bài viết ID ${row['post_id']} (${currentImportIdx + 1}/${totalRows}): <strong>"${displayTitle}"</strong>${hasImagePool ? ' + Chèn ảnh' : ''}...</p>`);
                } else {
                    $log.append(`<p>Đang tạo bài viết mới (${currentImportIdx + 1}/${totalRows}): <strong>"${displayTitle}"</strong>${hasImagePool ? ' + Chèn ảnh' : ''}...</p>`);
                }
                $log.scrollTop($log[0].scrollHeight);

                // Cập nhật progress (Từ 40% đến 100%)
                const percentImport = 40 + Math.round((currentImportIdx / totalRows) * 60);
                $progressBar.css('width', percentImport + '%').text(percentImport + '%');
                $progressStats.html(`<p>Đang lưu dữ liệu bài viết ${currentImportIdx + 1}/${totalRows}${hasImagePool ? ' (+ chèn ảnh)' : ''}...</p>`);

                if (hasImagePool) {
                    // SỬ DỤNG ENDPOINT MỚI: Chèn ảnh + import
                    // Phân bổ ảnh cho bài viết hiện tại từ pool
                    let postImageIds = [];
                    if (imageInsertMode === 'random') {
                        // Random: Chọn 3-5 ảnh ngẫu nhiên cho mỗi bài
                        const numImages = Math.min(imagePoolIds.length, Math.max(3, Math.ceil(imagePoolIds.length / totalRows)));
                        const shuffled = [...imagePoolIds].sort(() => Math.random() - 0.5);
                        postImageIds = shuffled.slice(0, numImages);
                    } else {
                        // Sequential/Cycle: Phân bổ ảnh tuần tự theo index bài viết
                        const imagesPerPost = Math.max(1, Math.ceil(imagePoolIds.length / totalRows));
                        const startIdx = (currentImportIdx * imagesPerPost) % imagePoolIds.length;
                        for (let i = 0; i < imagesPerPost; i++) {
                            postImageIds.push(imagePoolIds[(startIdx + i) % imagePoolIds.length]);
                        }
                    }

                    // Tách core fields ra khỏi row để gửi extra_fields
                    const extraFields = {};
                    const coreFieldNames = ['post_id', 'post_title', 'post_content', 'post_excerpt', 'post_date', 'post_name', 'featured_image'];
                    for (const key in row) {
                        if (!coreFieldNames.includes(key)) {
                            extraFields[key] = row[key];
                        }
                    }

                    $.ajax({
                        url: wpsai_params.ajax_url,
                        type: 'POST',
                        data: {
                            action: 'wpsai_ai_inject_images_and_import',
                            nonce: wpsai_params.nonce,
                            post_id: row['post_id'] || 0,
                            post_title: row['post_title'] || '',
                            post_content: row['post_content'] || '',
                            post_excerpt: row['post_excerpt'] || '',
                            post_type: postType,
                            post_status: postStatus,
                            image_pool_ids: postImageIds,
                            image_insert_mode: imageInsertMode,
                            set_featured: setFeatured ? '1' : '0',
                            template_slots: templateSlots ? JSON.stringify(templateSlots) : '',
                            extra_fields: extraFields
                        },
                        success: function (importRes) {
                            if (importRes.success) {
                                successCount++;
                                let imgInfo = importRes.data.featured_image_id > 0 ? ' | Featured Image ✓' : '';
                                let imgCount = importRes.data.images_injected > 0 ? ` | ${postImageIds.length} ảnh chèn` : '';
                                if (isUpdate) {
                                    $log.append(`<p class="log-success" style="margin:0 0 5px 15px;">✓ Cập nhật thành công! ID: <a href="${importRes.data.permalink}" target="_blank">${importRes.data.post_id}</a> - ${importRes.data.title}${imgInfo}${imgCount}</p>`);
                                } else {
                                    $log.append(`<p class="log-success" style="margin:0 0 5px 15px;">✓ Tạo mới thành công! ID: <a href="${importRes.data.permalink}" target="_blank">${importRes.data.post_id}</a> - ${importRes.data.title}${imgInfo}${imgCount}</p>`);
                                }
                            } else {
                                errorCount++;
                                $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi: ${importRes.data.message}</p>`);
                            }

                            currentImportIdx++;
                            setTimeout(runNextImport, 200);
                        },
                        error: function () {
                            errorCount++;
                            $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi kết nối HTTP khi lưu.</p>`);
                            currentImportIdx++;
                            setTimeout(runNextImport, 200);
                        }
                    });
                } else {
                    // ENDPOINT GỐC: Import bình thường không có ảnh
                    $.ajax({
                        url: wpsai_params.ajax_url,
                        type: 'POST',
                        data: {
                            action: 'wpsai_import_row',
                            nonce: wpsai_params.nonce,
                            row: row,
                            mapping: mapping,
                            post_type: postType,
                            post_status: postStatus
                        },
                        success: function (importRes) {
                            if (importRes.success) {
                                successCount++;
                                if (isUpdate) {
                                    $log.append(`<p class="log-success" style="margin:0 0 5px 15px;">✓ Cập nhật thành công! ID bài viết: <a href="${importRes.data.permalink}" target="_blank">${importRes.data.post_id}</a> - ${importRes.data.title}</p>`);
                                } else {
                                    $log.append(`<p class="log-success" style="margin:0 0 5px 15px;">✓ Tạo mới thành công! ID bài viết: <a href="${importRes.data.permalink}" target="_blank">${importRes.data.post_id}</a> - ${importRes.data.title}</p>`);
                                }
                            } else {
                                errorCount++;
                                $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi: ${importRes.data.message}</p>`);
                            }

                            currentImportIdx++;
                            setTimeout(runNextImport, 150);
                        },
                        error: function () {
                            errorCount++;
                            $log.append(`<p class="log-error" style="margin:0 0 5px 15px;">✗ Thất bại! Lỗi kết nối HTTP khi lưu.</p>`);
                            currentImportIdx++;
                            setTimeout(runNextImport, 150);
                        }
                    });
                }
            }

            runNextImport();
        }

        // Bắt đầu chạy batch đầu tiên
        runNextBatch();
    });

    // --- 17. XỬ LÝ KHO ẢNH NỘI DUNG CHO AI GENERATOR ---

    // Biến lưu trữ image pool
    let aiImagePoolIds = [];
    let aiTemplateSlots = null; // null = chưa phân tích, [] = đã phân tích nhưng không có slot

    // Mở Media Library để chọn ảnh cho Image Pool
    $('#wpsai-ai-image-pool-select-btn').on('click', function () {
        const frame = wp.media({
            title: 'Chọn ảnh cho Kho Ảnh Nội Dung AI',
            multiple: true,
            library: { type: 'image' },
            button: { text: 'Thêm vào Kho Ảnh' }
        });

        frame.on('select', function () {
            const attachments = frame.state().get('selection').toJSON();

            if (attachments.length === 0) return;

            // Thêm vào pool (không trùng lặp)
            attachments.forEach(function (att) {
                if (aiImagePoolIds.indexOf(att.id) === -1) {
                    aiImagePoolIds.push(att.id);
                }
            });

            renderAiImagePoolPreview(attachments);
        });

        frame.open();
    });

    // Render preview grid cho Image Pool
    function renderAiImagePoolPreview(newAttachments) {
        const $grid = $('#wpsai-ai-image-pool-grid');
        const $preview = $('#wpsai-ai-image-pool-preview');
        const $settings = $('#wpsai-ai-image-pool-settings');
        const $clearBtn = $('#wpsai-ai-image-pool-clear-btn');
        const $badge = $('#wpsai-ai-image-pool-count-badge');

        if (newAttachments && newAttachments.length > 0) {
            newAttachments.forEach(function (att) {
                const thumbUrl = att.sizes && att.sizes.thumbnail ? att.sizes.thumbnail.url : att.url;
                const $item = $(`
                    <div class="wpsai-image-preview-item" data-attachment-id="${att.id}" style="position: relative; display: inline-block; margin: 5px; border-radius: 8px; overflow: hidden; border: 2px solid #e2e8f0; transition: all 0.2s;">
                        <img src="${thumbUrl}" alt="${att.title || ''}" style="width: 100px; height: 100px; object-fit: cover; display: block;">
                        <button type="button" class="wpsai-ai-image-pool-remove-btn" data-id="${att.id}" style="position: absolute; top: 2px; right: 2px; background: rgba(220,50,50,0.85); color: #fff; border: none; border-radius: 50%; width: 22px; height: 22px; cursor: pointer; font-size: 14px; line-height: 20px; text-align: center;">×</button>
                        <span style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.6); color: #fff; font-size: 10px; text-align: center; padding: 2px;">#${$grid.children().length + 1}</span>
                    </div>
                `);
                $grid.append($item);
            });
        }

        // Cập nhật UI
        if (aiImagePoolIds.length > 0) {
            $preview.fadeIn();
            $settings.fadeIn();
            $clearBtn.show();
            $badge.text(aiImagePoolIds.length + ' ảnh').show();
        } else {
            $preview.hide();
            $settings.hide();
            $clearBtn.hide();
            $badge.hide();
        }

        // Re-index số thứ tự
        $grid.children().each(function (idx) {
            $(this).find('span:last').text('#' + (idx + 1));
        });
    }

    // Xóa ảnh khỏi pool
    $(document).on('click', '.wpsai-ai-image-pool-remove-btn', function () {
        const removeId = parseInt($(this).data('id'));
        aiImagePoolIds = aiImagePoolIds.filter(id => id !== removeId);
        $(this).closest('.wpsai-image-preview-item').remove();
        renderAiImagePoolPreview(null); // Refresh UI
    });

    // Xóa toàn bộ Image Pool
    $('#wpsai-ai-image-pool-clear-btn').on('click', function () {
        aiImagePoolIds = [];
        $('#wpsai-ai-image-pool-grid').empty();
        renderAiImagePoolPreview(null);
    });

    // --- 18. PHÂN TÍCH BÀI MẪU (TEMPLATE ANALYSIS) ---

    // Load danh sách bài viết vào dropdown template khi Post Type thay đổi
    $('#wpsai-ai-generator-post-type').on('change', function () {
        const postType = $(this).val();
        const $templateSelect = $('#wpsai-ai-template-post');
        
        $templateSelect.empty().append('<option value="">-- Không sử dụng bài mẫu (Tự động chèn sau heading) --</option>');
        aiTemplateSlots = null;
        $('#wpsai-ai-template-result').hide();
        $('#wpsai-ai-analyze-template-btn').prop('disabled', true);

        if (!postType) return;

        // Load bài viết cho dropdown template
        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_posts_by_post_type',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                if (res.success && res.data.length > 0) {
                    res.data.forEach(function (post) {
                        $templateSelect.append(`<option value="${post.id}">${post.title}</option>`);
                    });
                }
            }
        });
    });

    // Enable/disable nút phân tích khi chọn bài mẫu
    $('#wpsai-ai-template-post').on('change', function () {
        const postId = $(this).val();
        $('#wpsai-ai-analyze-template-btn').prop('disabled', !postId);
        if (!postId) {
            aiTemplateSlots = null;
            $('#wpsai-ai-template-result').hide();
        }
    });

    // Xử lý phân tích bài mẫu
    $('#wpsai-ai-analyze-template-btn').on('click', function () {
        const postId = $('#wpsai-ai-template-post').val();
        if (!postId) return;

        const $btn = $(this);
        const $result = $('#wpsai-ai-template-result');
        const $detail = $('#wpsai-ai-template-result-detail');

        $btn.prop('disabled', true).text('Đang phân tích...');
        $result.hide();

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_analyze_template_post',
                nonce: wpsai_params.nonce,
                post_id: postId
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-search"></span> Phân Tích Cấu Trúc');

                if (res.success) {
                    const data = res.data;
                    aiTemplateSlots = data.slots || [];

                    let detailHtml = '';
                    detailHtml += `<p><strong>Bài mẫu:</strong> "${data.post_title}"</p>`;
                    detailHtml += `<p><strong>Tổng số ảnh tìm thấy:</strong> <span style="font-size: 18px; color: var(--wpsai-primary); font-weight: bold;">${data.total_images}</span> vị trí</p>`;

                    if (data.headings && data.headings.length > 0) {
                        detailHtml += `<p style="margin-top: 8px;"><strong>Danh sách Heading (H2/H3):</strong></p>`;
                        detailHtml += '<ul style="margin: 5px 0 0 20px; list-style: disc;">';
                        data.headings.forEach(function (h) {
                            detailHtml += `<li style="margin-bottom: 3px;">${h}</li>`;
                        });
                        detailHtml += '</ul>';
                    }

                    if (data.total_images > 0) {
                        detailHtml += '<p style="margin-top: 10px;"><strong>Chi tiết vị trí ảnh:</strong></p>';
                        detailHtml += '<ul style="margin: 5px 0 0 20px; list-style: decimal;">';
                        data.slots.forEach(function (slot) {
                            let posText = slot.position === 'after_heading' ? `Sau heading: "${slot.nearby_heading}"` : 
                                          slot.position === 'within_figure' ? `Trong thẻ <figure>` : 'Độc lập';
                            let wrapperText = slot.wrapper_tag ? ` (Wrapper: <${slot.wrapper_tag}${slot.wrapper_class ? ' class="' + slot.wrapper_class + '"' : ''}>)` : '';
                            detailHtml += `<li style="margin-bottom: 3px; font-size: 12px;">${posText}${wrapperText}</li>`;
                        });
                        detailHtml += '</ul>';
                    } else {
                        detailHtml += '<p style="color: #b45309; margin-top: 10px;">⚠ Bài mẫu không chứa ảnh nào. Hệ thống sẽ tự động chèn ảnh sau mỗi heading (h2/h3).</p>';
                    }

                    $detail.html(detailHtml);
                    $result.fadeIn();
                } else {
                    aiTemplateSlots = null;
                    alert('Lỗi phân tích: ' + (res.data ? res.data.message : 'Không xác định'));
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-search"></span> Phân Tích Cấu Trúc');
                alert('Lỗi kết nối HTTP khi phân tích bài mẫu.');
            }
        });
    });

    // --- 19. SỬA ĐỔI HÀM importGeneratedRows ĐỂ HỖ TRỢ CHÈN ẢNH ---
    // Override hàm importGeneratedRows bên trong sự kiện click của AI Generator
    // Bằng cách thêm logic kiểm tra Image Pool trước khi gọi import

    // Lưu reference gốc của click handler để sử dụng lại
    // Thay vì override, ta sẽ thêm logic vào sự kiện click đã tồn tại
    // bằng cách thay thế hàm importGeneratedRows khi có image pool

    // Monkey-patch: Thêm một biến flag để hàm importGeneratedRows biết khi nào cần dùng endpoint mới
    window.wpsaiAiImagePool = {
        getIds: function () { return aiImagePoolIds; },
        getSlots: function () { return aiTemplateSlots; },
        getMode: function () { return $('#wpsai-ai-image-insert-mode').val() || 'sequential'; },
        getSetFeatured: function () { return $('#wpsai-ai-image-set-featured').is(':checked'); },
        hasImages: function () { return aiImagePoolIds.length > 0; }
    };

    // =========================================================================
    // 20. MODULE: QUẢN LÝ TÀI LIỆU DỰ ÁN (PROJECT DOCUMENTATION MANAGER)
    // =========================================================================

    // Trạng thái cục bộ của tài liệu dự án
    let docData = {
        overview: { name: '', url: '', git_repo: '', lead_dev: '', description: '' },
        worklogs: [],
        components: [],
        notes: ''
    };
    let activeComponentId = null;
    let docsInitialized = false;

    // Lắng nghe sự kiện chuyển Tab chính
    $('.wpsai-nav-tab').on('click', function () {
        const tabId = $(this).data('tab');
        if (tabId === 'project-docs' && !docsInitialized) {
            loadProjectDocs();
            docsInitialized = true;
        }
    });

    // Lắng nghe đổi Sub-tab trong Tài Liệu Dự Án
    $(document).on('click', '.wpsai-sub-tab-btn', function (e) {
        e.preventDefault();
        const subtab = $(this).data('subtab');
        
        $('.wpsai-sub-tab-btn').removeClass('active');
        $(this).addClass('active');

        $('.wpsai-subtab-content').removeClass('active');
        $('#wpsai-subtab-' + subtab).addClass('active');

        // Phục hồi preview sandbox nếu chuyển sang tab UI Components và có component active
        if (subtab === 'ui-library' && activeComponentId) {
            const currentTab = $('.wpsai-comp-code-tab-btn.active').data('codetab');
            if (currentTab === 'preview') {
                renderSandboxIframe();
            }
        }
    });

    // Lắng nghe đổi tab code của UI Component
    $(document).on('click', '.wpsai-comp-code-tab-btn', function (e) {
        e.preventDefault();
        const codetab = $(this).data('codetab');

        $('.wpsai-comp-code-tab-btn').removeClass('active');
        $(this).addClass('active');

        $('.wpsai-code-tab-content').removeClass('active');
        $('#wpsai-code-area-' + codetab).addClass('active');

        if (codetab === 'preview') {
            renderSandboxIframe();
        }
    });

    // Hàm gọi AJAX load toàn bộ tài liệu dự án
    function loadProjectDocs(forceFileRead = false) {
        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_project_docs',
                nonce: wpsai_params.nonce,
                force_file_read: forceFileRead ? 1 : 0
            },
            success: function (res) {
                if (res.success) {
                    const data = res.data.docs;
                    
                    // Cập nhật trạng thái cục bộ
                    docData.overview = data.overview || { name: '', url: '', git_repo: '', lead_dev: '', description: '' };
                    docData.worklogs = Array.isArray(data.worklogs) ? data.worklogs : (data.worklogs ? Object.values(data.worklogs) : []);
                    docData.components = Array.isArray(data.components) ? data.components : (data.components ? Object.values(data.components) : []);
                    docData.notes = data.notes || '';

                    // Điền vào form Overview
                    $('#wpsai-doc-project-name').val(docData.overview.name || '');
                    $('#wpsai-doc-project-url').val(docData.overview.url || '');
                    $('#wpsai-doc-git-repo').val(docData.overview.git_repo || '');
                    $('#wpsai-doc-lead-dev').val(docData.overview.lead_dev || '');
                    $('#wpsai-doc-project-desc').val(docData.overview.description || '');

                    // Cấu hình môi trường tự động
                    const sys = res.data.system_info;
                    $('#wpsai-sys-wp').text(sys.wp_version);
                    $('#wpsai-sys-php').text(sys.php_version);
                    $('#wpsai-sys-db').text(sys.db_version);
                    $('#wpsai-sys-theme').html(`<strong>${sys.active_theme.name}</strong> (v${sys.active_theme.version})<br><span style="font-size:11px;color:#64748b;">Folder: ${sys.active_theme.folder}</span>`);
                    
                    // Render CPTs
                    let cptHtml = '';
                    if (sys.custom_post_types && sys.custom_post_types.length) {
                        sys.custom_post_types.forEach(cpt => {
                            cptHtml += `<span class="wpsai-badge-type wpsai-badge-acf" style="margin:2px;">${cpt}</span> `;
                        });
                    } else {
                        cptHtml = '<span style="color:#94a3b8; font-style:italic;">Không có CPT tự định nghĩa</span>';
                    }
                    $('#wpsai-sys-cpts').html(cptHtml);

                    // Render Plugins
                    let pluginHtml = '<ul style="margin:0; padding-left:14px; list-style-type:square;">';
                    if (sys.active_plugins && sys.active_plugins.length) {
                        sys.active_plugins.forEach(plug => {
                            pluginHtml += `<li>${plug}</li>`;
                        });
                    } else {
                        pluginHtml += '<li>Không có plugin hoạt động</li>';
                    }
                    pluginHtml += '</ul>';
                    $('#wpsai-sys-plugins').html(pluginHtml);

                    // Render các tab con khác
                    renderWorklogsTimeline();
                    renderComponentsList();
                    $('#wpsai-doc-notes-area').val(docData.notes);

                    // Trạng thái Sync
                    const sync = res.data.file_sync;
                    if (sync.exists) {
                        $('#wpsai-sync-status').text('Đồng bộ thành công').css('color', 'var(--wpsai-success)');
                        $('#wpsai-sync-last-time').text(sync.last_sync);
                    } else {
                        $('#wpsai-sync-status').text('Chưa tạo tệp JSON').css('color', 'var(--wpsai-error)');
                        $('#wpsai-sync-last-time').text('Chưa đồng bộ');
                    }
                    
                    if (forceFileRead) {
                        alert('Đã nạp lại dữ liệu thành công từ file project-docs.json!');
                    }
                }
            },
            error: function () {
                console.error('Không thể tải dữ liệu tài liệu dự án.');
            }
        });
    }

    // Hàm gọi AJAX lưu toàn bộ tài liệu dự án
    function saveProjectDocs(silent = false, callback = null) {
        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_save_project_docs',
                nonce: wpsai_params.nonce,
                data: JSON.stringify(docData)
            },
            success: function (res) {
                if (res.success) {
                    $('#wpsai-sync-status').text('Đồng bộ thành công').css('color', 'var(--wpsai-success)');
                    $('#wpsai-sync-last-time').text(res.data.last_sync);
                    
                    if (!silent) {
                        alert(res.data.message);
                    }
                    if (callback) callback();
                } else {
                    alert('Lỗi: ' + res.data.message);
                }
            },
            error: function () {
                alert('Lỗi kết nối HTTP khi lưu tài liệu.');
            }
        });
    }

    // --- XỬ LÝ SUB-TAB 1: TỔNG QUAN ---
    $('#wpsai-doc-save-overview-btn').on('click', function () {
        const name = $('#wpsai-doc-project-name').val().trim();
        const url = $('#wpsai-doc-project-url').val().trim();
        const git = $('#wpsai-doc-git-repo').val().trim();
        const lead = $('#wpsai-doc-lead-dev').val().trim();
        const desc = $('#wpsai-doc-project-desc').val().trim();

        docData.overview = {
            name: name,
            url: url,
            git_repo: git,
            lead_dev: lead,
            description: desc
        };

        const $btn = $(this);
        const $msg = $('#wpsai-doc-overview-msg');
        $btn.prop('disabled', true).text('Đang lưu...');
        
        saveProjectDocs(true, function() {
            $btn.prop('disabled', false).text('Lưu Tất Cả Thay Đổi Tài Liệu');
            $msg.text('Đã lưu thành công!').css('color', 'var(--wpsai-success)').show();
            setTimeout(() => $msg.fadeOut(), 3000);
        });
    });

    // --- XỬ LÝ SUB-TAB 2: NHẬT KÝ CÔNG VIỆC ---
    // Render timeline
    function renderWorklogsTimeline() {
        const $timeline = $('#wpsai-doc-logs-timeline');
        $timeline.empty();

        if (!docData.worklogs || docData.worklogs.length === 0) {
            $timeline.html('<p style="color: var(--wpsai-text-muted); font-style: italic;">Chưa có nhật ký công việc nào được ghi nhận. Bấm thêm mới bên cạnh!</p>');
            return;
        }

        // Sắp xếp ngày từ mới nhất -> cũ nhất
        const sortedLogs = [...docData.worklogs].sort((a, b) => new Date(b.date) - new Date(a.date));

        sortedLogs.forEach((log) => {
            const isGit = log.title.toLowerCase().startsWith('git:') || log.is_git;
            const filesBadge = log.files ? `<div style="margin-top:6px;"><span class="wpsai-badge-type wpsai-badge-core" style="font-size:11px;">Files: ${log.files}</span></div>` : '';
            
            let descHtml = '';
            if (log.description) {
                descHtml = `<div class="wpsai-timeline-body">${log.description.replace(/\n/g, '<br>')}</div>`;
            }

            const itemHtml = `
                <div class="wpsai-timeline-item">
                    <div class="wpsai-timeline-dot ${isGit ? 'git-dot' : ''}"></div>
                    <div class="wpsai-timeline-header">
                        <h4 class="wpsai-timeline-title">${log.title}</h4>
                        <span class="wpsai-timeline-date">${log.date}</span>
                    </div>
                    <div class="wpsai-timeline-meta">
                        <span><span class="dashicons dashicons-admin-users" style="font-size:14px; width:14px; height:14px; vertical-align:middle; margin-right:3px;"></span>${log.developer || 'N/A'}</span>
                    </div>
                    ${descHtml}
                    ${filesBadge}
                    <div class="wpsai-timeline-actions">
                        <button type="button" class="wpsai-doc-delete-log-btn" data-title="${log.title}" style="background:none; border:none; color:var(--wpsai-error); cursor:pointer; font-size:12px; display:flex; align-items:center; gap:3px; padding:0; margin:0;">
                            <span class="dashicons dashicons-trash" style="font-size:14px; width:14px; height:14px;"></span> Xóa
                        </button>
                    </div>
                </div>
            `;
            $timeline.append(itemHtml);
        });
    }

    // Thêm log mới
    $('#wpsai-doc-add-log-btn').on('click', function () {
        const title = $('#wpsai-log-title').val().trim();
        const date = $('#wpsai-log-date').val();
        const developer = $('#wpsai-log-dev').val().trim();
        const files = $('#wpsai-log-files').val().trim();
        const description = $('#wpsai-log-desc').val().trim();

        if (!title) {
            alert('Vui lòng nhập tên công việc!');
            return;
        }

        const newLog = {
            title: title,
            date: date || new Date().toISOString().split('T')[0],
            developer: developer || 'N/A',
            files: files,
            description: description
        };

        docData.worklogs.push(newLog);
        
        saveProjectDocs(true, function() {
            // Reset form
            $('#wpsai-log-title').val('');
            $('#wpsai-log-files').val('');
            $('#wpsai-log-desc').val('');
            
            renderWorklogsTimeline();
        });
    });

    // Xóa log
    $(document).on('click', '.wpsai-doc-delete-log-btn', function () {
        const title = $(this).data('title');
        if (!confirm(`Bạn có chắc chắn muốn xóa nhật ký công việc: "${title}" không?`)) {
            return;
        }

        const idx = docData.worklogs.findIndex(item => item.title === title);
        if (idx !== -1) {
            docData.worklogs.splice(idx, 1);
            saveProjectDocs(true, function() {
                renderWorklogsTimeline();
            });
        }
    });

    // Hiển thị Changelog Markdown Modal
    $('#wpsai-doc-export-changelog-btn').on('click', function () {
        let md = `# CHANGELOG - Nhật Ký Phát Triển\n\n`;
        
        if (docData.worklogs && docData.worklogs.length) {
            // Sắp xếp ngày mới nhất
            const sortedLogs = [...docData.worklogs].sort((a, b) => new Date(b.date) - new Date(a.date));
            sortedLogs.forEach(log => {
                md += `## [${log.date}] - ${log.title}\n`;
                md += `- **Lập trình viên**: ${log.developer}\n`;
                if (log.files) {
                    md += `- **Các file tác động**: \`${log.files}\`\n`;
                }
                if (log.description) {
                    md += `- **Mô tả**:\n  ${log.description.replace(/\n/g, '\n  ')}\n`;
                }
                md += `\n`;
            });
        } else {
            md += `*(Chưa ghi nhận công việc nào)*\n`;
        }

        $('#wpsai-changelog-markdown-text').val(md);
        $('#wpsai-changelog-modal').css('display', 'flex');
    });

    // Close Modal
    $('#wpsai-changelog-modal-close, #wpsai-changelog-modal-ok-btn').on('click', function () {
        $('#wpsai-changelog-modal').hide();
    });

    // Copy Changelog
    $('#wpsai-changelog-modal-copy-btn').on('click', function () {
        const text = $('#wpsai-changelog-markdown-text').val();
        navigator.clipboard.writeText(text).then(() => {
            const $btn = $(this);
            $btn.html('<span class="dashicons dashicons-yes"></span> Đã Sao Chép!');
            setTimeout(() => {
                $btn.html('<span class="dashicons dashicons-admin-page"></span> Sao Chép Nội Dung');
            }, 2000);
        });
    });

    // Đọc lịch sử Git
    $('#wpsai-doc-git-load-btn').on('click', function () {
        const $btn = $(this);
        const origHtml = $btn.html();
        
        // Remove picker cũ nếu có
        $('#wpsai-git-commits-picker').remove();

        $btn.prop('disabled', true).text('Đang kết nối Git...');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_git_get_commits',
                nonce: wpsai_params.nonce
            },
            success: function (res) {
                $btn.prop('disabled', false).html(origHtml);
                if (res.success && res.data.length) {
                    // Tạo picker
                    let pickerHtml = `<div id="wpsai-git-commits-picker" style="background:#fff; border:1px solid #cbd5e1; border-radius:8px; max-height:220px; overflow-y:auto; margin-top:10px; box-shadow:0 10px 15px -3px rgba(0,0,0,0.1); border: 1px solid var(--wpsai-border-color); text-align:left;">`;
                    pickerHtml += `<div style="background:#f1f5f9; padding:8px 12px; font-weight:bold; font-size:12px; border-bottom:1px solid #cbd5e1; display:flex; justify-content:space-between; align-items:center;">`;
                    pickerHtml += `<span>Chọn 1 commit gần nhất để điền form:</span>`;
                    pickerHtml += `<a href="#" id="wpsai-git-picker-close" style="text-decoration:none; color:#ef4444; font-weight:bold;">Đóng</a>`;
                    pickerHtml += `</div>`;
                    
                    res.data.forEach(c => {
                        pickerHtml += `
                            <div class="wpsai-git-commit-item" data-msg="${c.message}" data-date="${c.date}" data-author="${c.author}" data-hash="${c.hash}">
                                <span class="wpsai-git-commit-hash">[${c.hash}]</span>
                                <span class="wpsai-git-commit-date">${c.date}</span>
                                <span style="font-weight:600; color:#334155;">${c.message}</span>
                                <span style="color:#64748b; font-size:11px;"> - dev: ${c.author}</span>
                            </div>
                        `;
                    });
                    pickerHtml += `</div>`;
                    $btn.after(pickerHtml);
                } else {
                    alert('Lỗi: ' + (res.data ? res.data.message : 'Không đọc được lịch sử Git.'));
                }
            },
            error: function () {
                $btn.prop('disabled', false).html(origHtml);
                alert('Lỗi kết nối HTTP khi đọc Git.');
            }
        });
    });

    // Close git picker
    $(document).on('click', '#wpsai-git-picker-close', function (e) {
        e.preventDefault();
        $('#wpsai-git-commits-picker').remove();
    });

    // Chọn commit từ Git picker
    $(document).on('click', '.wpsai-git-commit-item', function () {
        const msg = $(this).data('msg');
        const date = $(this).data('date');
        const author = $(this).data('author');
        const hash = $(this).data('hash');

        // Điền vào form
        $('#wpsai-log-title').val(`Git: ${msg} (${hash})`);
        $('#wpsai-log-date').val(date);
        $('#wpsai-log-dev').val(author);

        // Tự động xóa picker
        $('#wpsai-git-commits-picker').remove();
    });


    // --- XỬ LÝ SUB-TAB 3: THƯ VIỆN UI COMPONENTS ---
    // Render list components
    function renderComponentsList() {
        const $list = $('#wpsai-comp-list-container');
        $list.empty();

        if (!docData.components || docData.components.length === 0) {
            $list.html('<p style="color: var(--wpsai-text-muted); font-style: italic; font-size: 13px;">Chưa có component nào được tạo.</p>');
            return;
        }

        docData.components.forEach(c => {
            let badgeClass = 'wpsai-badge-core';
            if (c.category === 'Table') badgeClass = 'wpsai-badge-acf';
            else if (c.category === 'Form') badgeClass = 'wpsai-badge-meta';
            else if (c.category === 'Modal') badgeClass = 'wpsai-badge-type';
            else if (c.category === 'Progress') badgeClass = 'wpsai-badge-taxonomy';

            const activeClass = (activeComponentId && activeComponentId.toString() === c.id.toString()) ? 'active' : '';
            const desc = c.description ? c.description.replace(/[#*`]/g, '').substring(0, 45) + '...' : '(Không có mô tả)';

            const itemHtml = `
                <div class="wpsai-comp-item ${activeClass}" data-id="${c.id}">
                    <span class="wpsai-comp-item-title">${c.name}</span>
                    <span class="wpsai-comp-item-desc">${desc}</span>
                    <span class="wpsai-comp-item-badge ${badgeClass}">${c.category || 'Other'}</span>
                </div>
            `;
            $list.append(itemHtml);
        });
    }

    // Bấm Thêm mới component
    $('#wpsai-comp-add-new-btn').on('click', function () {
        activeComponentId = null;
        $('.wpsai-comp-item').removeClass('active');

        // Reset editor fields
        $('#wpsai-comp-id').val('');
        $('#wpsai-comp-name').val('');
        $('#wpsai-comp-category').val('Other');
        $('#wpsai-comp-html').val('');
        $('#wpsai-comp-css').val('');
        $('#wpsai-comp-js').val('');
        $('#wpsai-comp-desc').val('');

        $('#wpsai-comp-panel-title').html('<span class="dashicons dashicons-plus" style="color: var(--wpsai-success);"></span> Thêm UI Component Mới');
        
        $('#wpsai-comp-empty-panel').hide();
        $('#wpsai-comp-editor-panel').show();
        $('#wpsai-comp-delete-btn').hide();

        // Mở mặc định tab HTML
        $('.wpsai-comp-code-tab-btn[data-codetab="html"]').trigger('click');

        $('#wpsai-comp-name').focus();
    });

    // Chọn component từ list
    $(document).on('click', '.wpsai-comp-item', function () {
        const id = $(this).data('id');
        activeComponentId = id;

        $('.wpsai-comp-item').removeClass('active');
        $(this).addClass('active');

        const comp = docData.components.find(item => item.id.toString() === id.toString());
        if (!comp) return;

        // Điền dữ liệu vào form
        $('#wpsai-comp-id').val(comp.id);
        $('#wpsai-comp-name').val(comp.name);
        $('#wpsai-comp-category').val(comp.category || 'Other');
        $('#wpsai-comp-html').val(comp.html || '');
        $('#wpsai-comp-css').val(comp.css || '');
        $('#wpsai-comp-js').val(comp.js || '');
        $('#wpsai-comp-desc').val(comp.description || '');

        $('#wpsai-comp-panel-title').html('<span class="dashicons dashicons-edit" style="color: var(--wpsai-secondary);"></span> Biên Tập Component');

        $('#wpsai-comp-empty-panel').hide();
        $('#wpsai-comp-editor-panel').show();
        $('#wpsai-comp-delete-btn').show();

        // Tải lại preview nếu đang ở tab preview
        const currentTab = $('.wpsai-comp-code-tab-btn.active').data('codetab');
        if (currentTab === 'preview') {
            renderSandboxIframe();
        }
    });

    // Lưu Component
    $('#wpsai-comp-save-btn').on('click', function () {
        const name = $('#wpsai-comp-name').val().trim();
        const category = $('#wpsai-comp-category').val();
        const html = $('#wpsai-comp-html').val();
        const css = $('#wpsai-comp-css').val();
        const js = $('#wpsai-comp-js').val();
        const desc = $('#wpsai-comp-desc').val().trim();

        if (!name) {
            alert('Vui lòng nhập tên component!');
            return;
        }

        const id = $('#wpsai-comp-id').val() || Date.now().toString();

        const compData = {
            id: id,
            name: name,
            category: category,
            html: html,
            css: css,
            js: js,
            description: desc
        };

        const existingIdx = docData.components.findIndex(item => item.id.toString() === id.toString());

        if (existingIdx !== -1) {
            docData.components[existingIdx] = compData;
        } else {
            docData.components.push(compData);
        }

        activeComponentId = id;

        saveProjectDocs(true, function() {
            renderComponentsList();
            // Highlight lại phần tử vừa lưu
            $(`.wpsai-comp-item[data-id="${id}"]`).addClass('active');
            alert('Đã lưu UI Component thành công!');
        });
    });

    // Xóa Component
    $('#wpsai-comp-delete-btn').on('click', function () {
        const id = $('#wpsai-comp-id').val();
        const name = $('#wpsai-comp-name').val();

        if (!id) return;
        if (!confirm(`Bạn có chắc chắn muốn xóa component "${name}" không?`)) {
            return;
        }

        const idx = docData.components.findIndex(item => item.id.toString() === id.toString());
        if (idx !== -1) {
            docData.components.splice(idx, 1);
            activeComponentId = null;
            
            saveProjectDocs(true, function() {
                renderComponentsList();
                $('#wpsai-comp-editor-panel').hide();
                $('#wpsai-comp-empty-panel').show();
            });
        }
    });

    // Biên dịch Sandbox Iframe
    function renderSandboxIframe() {
        const html = $('#wpsai-comp-html').val() || '';
        const css = $('#wpsai-comp-css').val() || '';
        const js = $('#wpsai-comp-js').val() || '';
        
        const iframe = document.getElementById('wpsai-comp-sandbox-iframe');
        if (!iframe) return;

        // Xây dựng code đầy đủ
        const srcdocContent = `
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body { font-family: sans-serif; padding: 15px; margin: 0; background: #ffffff; color: #334155; }
                    /* CSS của người dùng */
                    ${css}
                </style>
            </head>
            <body>
                <!-- HTML của người dùng -->
                ${html}
                
                <!-- JS của người dùng -->
                <script>
                    try {
                        ${js}
                    } catch(e) {
                        console.error('Lỗi JS Sandbox:', e);
                        const errDiv = document.createElement('div');
                        errDiv.style.cssText = 'color:#ef4444; border:1px solid #fca5a5; background:#fef2f2; padding:10px; border-radius:6px; font-size:12px; margin-top:15px; font-family:monospace;';
                        errDiv.innerHTML = '<strong>Lỗi Javascript Sandbox:</strong> ' + e.message;
                        document.body.appendChild(errDiv);
                    }
                <\/script>
            </body>
            </html>
        `;

        iframe.srcdoc = srcdocContent;
    }

    // AI viết mô tả linh kiện
    $('#wpsai-comp-ai-desc-btn').on('click', function () {
        const $btn = $(this);
        const name = $('#wpsai-comp-name').val().trim();
        const category = $('#wpsai-comp-category').val();
        const html = $('#wpsai-comp-html').val();
        const css = $('#wpsai-comp-css').val();
        const js = $('#wpsai-comp-js').val();

        if (empty(html) && empty(css) && empty(js)) {
            alert('Vui lòng nhập code trước khi yêu cầu AI viết mô tả.');
            return;
        }

        $btn.prop('disabled', true).text('AI đang phân tích code...');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_ai_describe_snippet',
                nonce: wpsai_params.nonce,
                name: name || 'Không tên',
                category: category,
                html: html,
                css: css,
                js: js
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-customizer"></span> AI Tự Động Viết Mô Tả');
                if (res.success) {
                    $('#wpsai-comp-desc').val(res.data.description);
                } else {
                    alert('Lỗi AI: ' + res.data.message);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-admin-customizer"></span> AI Tự Động Viết Mô Tả');
                alert('Lỗi kết nối HTTP với AI.');
            }
        });
    });

    // Helper kiểm tra rỗng
    function empty(v) {
        return !v || v.trim().length === 0;
    }

    // Sao chép code riêng lẻ và toàn bộ
    function setupCopyButton(btnId, textareaId, label) {
        $(btnId).on('click', function () {
            const code = $(textareaId).val();
            if (!code) {
                alert(`Không có mã ${label} để sao chép!`);
                return;
            }

            navigator.clipboard.writeText(code).then(() => {
                const $btn = $(this);
                const origText = $btn.html();
                $btn.html('<span class="dashicons dashicons-yes" style="color:var(--wpsai-success);"></span> Đã Copy!');
                setTimeout(() => {
                    $btn.html(origText);
                }, 2000);
            });
        });
    }
    setupCopyButton('#wpsai-copy-html-btn', '#wpsai-comp-html', 'HTML');
    setupCopyButton('#wpsai-copy-css-btn', '#wpsai-comp-css', 'CSS');
    setupCopyButton('#wpsai-copy-js-btn', '#wpsai-comp-js', 'JS');

    // Copy toàn bộ (HTML + CSS + JS)
    $('#wpsai-copy-all-btn').on('click', function () {
        const html = $('#wpsai-comp-html').val() || '';
        const css = $('#wpsai-comp-css').val() || '';
        const js = $('#wpsai-comp-js').val() || '';

        if (!html && !css && !js) {
            alert('Không có mã nguồn để sao chép!');
            return;
        }

        let fullCode = '';
        if (html) fullCode += `<!-- HTML -->\n${html}\n\n`;
        if (css) fullCode += `/* CSS */\n<style>\n${css}\n</style>\n\n`;
        if (js) fullCode += `/* Javascript */\n<script>\n${js}\n<\/script>\n`;

        navigator.clipboard.writeText(fullCode).then(() => {
            const $btn = $(this);
            const origText = $btn.html();
            $btn.html('<span class="dashicons dashicons-yes" style="color:var(--wpsai-success);"></span> Đã Copy All!');
            setTimeout(() => {
                $btn.html(origText);
            }, 2000);
        });
    });


    // --- XỬ LÝ SUB-TAB 4: GHI CHÚ KỸ THUẬT ---
    $('#wpsai-doc-save-notes-btn').on('click', function () {
        const text = $('#wpsai-doc-notes-area').val();
        docData.notes = text;

        const $btn = $(this);
        const $msg = $('#wpsai-doc-notes-msg');
        $btn.prop('disabled', true).text('Đang lưu...');
        
        saveProjectDocs(true, function() {
            $btn.prop('disabled', false).text('Lưu Ghi Chú Kỹ Thuật');
            $msg.text('Đã lưu ghi chú thành công!').css('color', 'var(--wpsai-success)').show();
            setTimeout(() => $msg.fadeOut(), 3000);
        });
    });


    // --- XỬ LÝ SUB-TAB 5: ĐỒNG BỘ & NHẬP XUẤT ---
    // Ghi đè DB ra file json
    $('#wpsai-sync-db-to-file-btn').on('click', function () {
        if (!confirm('Bạn có chắc muốn ghi đè dữ liệu tài liệu hiện tại ra file project-docs.json không? File cũ sẽ bị ghi đè.')) {
            return;
        }
        saveProjectDocs(false);
    });

    // Đọc file json ghi đè DB
    $('#wpsai-sync-file-to-db-btn').on('click', function () {
        if (!confirm('Hành động này sẽ đọc file project-docs.json và ghi đè hoàn toàn vào cơ sở dữ liệu WordPress hiện tại. Bạn có chắc muốn tiếp tục không?')) {
            return;
        }
        loadProjectDocs(true);
    });

    // Xuất Markdown file để tải về
    $('#wpsai-export-markdown-btn').on('click', function () {
        const $btn = $(this);
        $btn.prop('disabled', true).text('Đang xuất...');

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_export_docs_markdown',
                nonce: wpsai_params.nonce
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-download"></span> Xuất và Tải File .md');
                if (res.success) {
                    window.location.href = res.data.download_url;
                } else {
                    alert('Lỗi xuất tệp: ' + res.data.message);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-download"></span> Xuất và Tải File .md');
                alert('Lỗi kết nối HTTP khi xuất Markdown.');
            }
        });
    });

    // Nhập JSON Backup
    $('#wpsai-import-json-btn').on('click', function () {
        $('#wpsai-import-json-file').trigger('click');
    });

    $('#wpsai-import-json-file').on('change', function (e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function (evt) {
            try {
                const parsed = JSON.parse(evt.target.result);
                
                // Kiểm tra định dạng thô
                if (!parsed.overview && !parsed.worklogs && !parsed.components) {
                    alert('Lỗi: Định dạng file backup JSON không hợp lệ (Thiếu các trường cốt lõi).');
                    return;
                }

                if (confirm('Phát hiện file backup hợp lệ! Bạn có đồng ý ghi đè toàn bộ tài liệu dự án hiện tại bằng dữ liệu trong file này không?')) {
                    docData = parsed;
                    
                    // Ghi đè vào DB và file cục bộ
                    saveProjectDocs(true, function() {
                        // Load lại các trường
                        $('#wpsai-doc-project-name').val(docData.overview.name || '');
                        $('#wpsai-doc-project-url').val(docData.overview.url || '');
                        $('#wpsai-doc-git-repo').val(docData.overview.git_repo || '');
                        $('#wpsai-doc-lead-dev').val(docData.overview.lead_dev || '');
                        $('#wpsai-doc-project-desc').val(docData.overview.description || '');

                        renderWorklogsTimeline();
                        renderComponentsList();
                        $('#wpsai-doc-notes-area').val(docData.notes || '');

                        $('#wpsai-comp-editor-panel').hide();
                        $('#wpsai-comp-empty-panel').show();

                        alert('Nhập dữ liệu backup dự án thành công!');
                    });
                }
            } catch(err) {
                alert('Lỗi: Không thể phân tích cú pháp JSON. Chi tiết: ' + err.message);
            }
        };
        reader.readAsText(file);
        
        // Reset file input
        $(this).val('');
    });


    // ==========================================
    // --- 11. XỬ LÝ CÀO HTML OFFLINE ---
    // ==========================================
    let offlineHtmlContent = '';
    let offlineParsedRows = [];
    let offlineMappingCount = 3;

    // File Drag & Drop
    const offlineDropZone = document.getElementById('wpsai-offline-drop-zone');
    const offlineFileInput = document.getElementById('wpsai-offline-file-input');
    const offlineFileBadge = document.getElementById('wpsai-offline-file-badge');
    const offlineLog = document.getElementById('wpsai-offline-log');
    
    if (offlineDropZone && offlineFileInput) {
        offlineDropZone.addEventListener('click', () => offlineFileInput.click());

        ['dragenter', 'dragover'].forEach(eventName => {
            offlineDropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                offlineDropZone.style.borderColor = 'var(--wpsai-primary)';
                offlineDropZone.style.background = '#f0f9ff';
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            offlineDropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                offlineDropZone.style.borderColor = '#ccc';
                offlineDropZone.style.background = '#fafafa';
            });
        });

        offlineDropZone.addEventListener('drop', (e) => {
            if (e.dataTransfer.files.length > 0) {
                handleOfflineFile(e.dataTransfer.files[0]);
            }
        });

        offlineFileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleOfflineFile(e.target.files[0]);
            }
        });
    }

    function logOffline(text, type = 'info') {
        if (!offlineLog) return;
        const p = document.createElement('p');
        p.style.margin = '0 0 4px 0';
        if (type === 'error') p.style.color = '#ef4444';
        else if (type === 'success') p.style.color = '#10b981';
        else p.style.color = '#3b82f6';
        
        const time = new Date().toLocaleTimeString();
        p.innerHTML = `[${time}] ${text}`;
        offlineLog.appendChild(p);
        offlineLog.scrollTop = offlineLog.scrollHeight;
    }

    function handleOfflineFile(file) {
        if (!file.name.endsWith('.html') && !file.name.endsWith('.htm')) {
            logOffline('Tệp tin không đúng định dạng HTML. Vui lòng chọn tệp .html hoặc .htm!', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            offlineHtmlContent = e.target.result;
            logOffline(`Đã nạp tệp HTML thành công: <strong>${file.name}</strong> (${(file.size / 1024 / 1024).toFixed(2)} MB)`, 'success');
            
            // Show badge
            if (offlineFileBadge) {
                offlineFileBadge.innerHTML = `<span class="dashicons dashicons-yes" style="vertical-align:middle; margin-right:5px;"></span>${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
                offlineFileBadge.style.display = 'block';
            }
            const dropzoneText = offlineDropZone.querySelector('p');
            if (dropzoneText) dropzoneText.style.display = 'none';
            const dropzoneIcon = offlineDropZone.querySelector('.dashicons');
            if (dropzoneIcon) dropzoneIcon.style.color = '#46b450';

            // Enable Parse button
            $('#wpsai-offline-run-btn').prop('disabled', false);
        };
        reader.onerror = function() {
            logOffline('Lỗi khi đọc file HTML!', 'error');
        };
        reader.readAsText(file);
    }

    // Add mapping row
    $('#wpsai-offline-add-field-btn').on('click', function() {
        offlineMappingCount++;
        const rowHtml = `
            <tr data-row-idx="${offlineMappingCount}">
                <td><input type="text" class="field-name large-text" value="acf_custom_field_${offlineMappingCount}" style="width:100%; padding:6px;"></td>
                <td><input type="text" class="field-selector large-text" placeholder="vd: .meta-class, div.price" style="width:100%; padding:6px;"></td>
                <td>
                    <select class="field-attr" style="width:100%; padding:5px;">
                        <option value="text" selected>Chữ (Text)</option>
                        <option value="html">Mã HTML</option>
                        <option value="href">Link (href)</option>
                        <option value="src">Ảnh (src)</option>
                        <option value="alt">Tên ảnh / Thuộc tính alt (alt)</option>
                    </select>
                </td>
                <td style="text-align:center;"><button type="button" class="wpsai-btn-remove wpsai-offline-delete-row" style="background:none; border:none; cursor:pointer; font-weight:bold; font-size:18px;">&times;</button></td>
            </tr>
        `;
        $('#wpsai-offline-mapping-table tbody').append(rowHtml);
        logOffline('Đã thêm dòng ánh xạ trường mới.', 'info');
    });

    // Delete mapping row
    $(document).on('click', '.wpsai-offline-delete-row', function() {
        $(this).closest('tr').remove();
        logOffline('Đã xóa dòng ánh xạ.', 'info');
    });

    // Parse snippet for selectors
    $('#wpsai-offline-snippet').on('input', function() {
        const val = $(this).val().trim();
        if (!val) {
            $('#wpsai-offline-suggestions-wrapper').hide();
            return;
        }

        try {
            const parser = new DOMParser();
            const doc = parser.parseFromString(val, 'text/html');
            const elements = doc.body.querySelectorAll('*');
            
            const detectedSelectors = new Set();
            let wrapperClass = '';

            const firstEl = doc.body.firstElementChild;
            if (firstEl) {
                if (firstEl.id) {
                    wrapperClass = '#' + firstEl.id;
                } else if (firstEl.classList.length > 0) {
                    wrapperClass = '.' + Array.from(firstEl.classList).join('.');
                } else {
                    wrapperClass = firstEl.tagName.toLowerCase();
                }
                
                if (wrapperClass) {
                    $('#wpsai-offline-item-selector').val(wrapperClass);
                }
            }

            elements.forEach(el => {
                const tag = el.tagName.toLowerCase();
                if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'a', 'p', 'span', 'button'].includes(tag)) {
                    detectedSelectors.add(JSON.stringify({ type: 'tag', val: tag }));
                }

                if (el.classList.length > 0) {
                    el.classList.forEach(className => {
                        detectedSelectors.add(JSON.stringify({ type: 'class', val: '.' + className }));
                    });
                }

                if (el.hasAttribute('src')) {
                    detectedSelectors.add(JSON.stringify({ type: 'attr', val: 'img[src]' }));
                }
                if (el.hasAttribute('href')) {
                    detectedSelectors.add(JSON.stringify({ type: 'attr', val: 'a[href]' }));
                }
            });

            const $suggestions = $('#wpsai-offline-suggestions');
            $suggestions.empty();
            
            if (detectedSelectors.size > 0) {
                detectedSelectors.forEach(itemJson => {
                    const item = JSON.parse(itemJson);
                    const label = item.type === 'tag' ? `Thẻ: ${item.val}` : (item.type === 'class' ? `Lớp: ${item.val}` : `Thuộc tính: ${item.val}`);
                    const $tagEl = $(`<span class="wpsai-badge" style="cursor:pointer; margin:2px; font-family:monospace; background:#e2e8f0; color:#334155;">${label}</span>`);
                    
                    $tagEl.on('click', function() {
                        // Find first empty selector field
                        let filled = false;
                        $('#wpsai-offline-mapping-table tbody tr').each(function() {
                            const $input = $(this).find('.field-selector');
                            if (!$input.val().trim()) {
                                $input.val(item.val);
                                filled = true;
                                logOffline(`Đã điền bộ chọn <strong>${item.val}</strong>.`, 'info');
                                return false; // break loop
                            }
                        });
                        
                        if (!filled) {
                            logOffline('Tất cả các ô bộ chọn đã được điền. Hãy thêm dòng mới rồi chọn lại!', 'error');
                        }
                    });
                    $suggestions.append($tagEl);
                });
                $('#wpsai-offline-suggestions-wrapper').show();
                logOffline('Đã phân tích khối HTML mẫu và sinh gợi ý selectors.', 'success');
            } else {
                $('#wpsai-offline-suggestions-wrapper').hide();
            }
        } catch (err) {
            logOffline('Lỗi phân tích khối HTML mẫu!', 'error');
            $('#wpsai-offline-suggestions-wrapper').hide();
        }
    });

    // Run Parsing
    $('#wpsai-offline-run-btn').on('click', function() {
        if (!offlineHtmlContent) {
            logOffline('Không có dữ liệu HTML được nạp!', 'error');
            return;
        }

        const itemSelector = $('#wpsai-offline-item-selector').val().trim();
        if (!itemSelector) {
            logOffline('Vui lòng điền bộ chọn khung bọc ngoài cùng (Item wrapper)!', 'error');
            return;
        }

        logOffline('Đang phân tích cấu trúc DOM và lọc dữ liệu...', 'info');

        try {
            const mappings = [];
            $('#wpsai-offline-mapping-table tbody tr').each(function() {
                const name = $(this).find('.field-name').val().trim();
                const selector = $(this).find('.field-selector').val().trim();
                const attr = $(this).find('.field-attr').val();
                if (name && selector) {
                    mappings.push({ name, selector, attr });
                }
            });

            if (mappings.length === 0) {
                logOffline('Lỗi: Bạn phải định nghĩa ít nhất 1 trường ánh xạ!', 'error');
                return;
            }

            const parser = new DOMParser();
            const doc = parser.parseFromString(offlineHtmlContent, 'text/html');
            const items = doc.querySelectorAll(itemSelector);

            logOffline(`Tìm thấy <strong>${items.length}</strong> phần tử khớp với <code>${itemSelector}</code>.`, 'info');

            if (items.length === 0) {
                logOffline('Lỗi: Không tìm thấy phần tử nào khớp với bộ chọn. Hãy thử lại!', 'error');
                $('#wpsai-offline-table-body').html(`
                    <tr>
                        <td colspan="100" style="text-align: center; color: var(--wpsai-red); padding: 20px;">
                            Không tìm thấy phần tử nào khớp với bộ chọn "${itemSelector}". Vui lòng kiểm tra lại.
                        </td>
                    </tr>
                `);
                $('#wpsai-offline-row-count-badge').text('Tổng số dòng: 0 dòng');
                $('#wpsai-offline-export-btn').prop('disabled', true);
                $('#wpsai-offline-export-json-btn').prop('disabled', true);
                return;
            }

            offlineParsedRows = [];
            items.forEach((itemNode) => {
                const rowData = {};
                mappings.forEach(m => {
                    let el = null;
                    if (m.selector.startsWith('/') || m.selector.startsWith('./') || m.selector.startsWith('.//')) {
                        try {
                            const xpathResult = doc.evaluate(m.selector, itemNode, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                            el = xpathResult.singleNodeValue;
                        } catch (e) {
                            console.error('XPath error:', e);
                        }
                    } else {
                        el = itemNode.querySelector(m.selector);
                    }
                    let value = '';
                    if (el) {
                        if (m.attr === 'text') {
                            value = el.textContent.trim().replace(/\s+/g, ' ');
                        } else if (m.attr === 'html') {
                            value = el.innerHTML.trim();
                        } else if (m.attr === 'href') {
                            value = el.getAttribute('href') || '';
                        } else if (m.attr === 'src') {
                            value = el.getAttribute('src') || el.getAttribute('data-src') || el.getAttribute('data-lazy-src') || '';
                        } else if (m.attr === 'alt') {
                            value = el.getAttribute('alt') || '';
                        }
                    }
                    rowData[m.name] = value;
                });
                offlineParsedRows.push(rowData);
            });

            // Render Preview Table
            const $thead = $('#wpsai-offline-table-header');
            $thead.empty();
            mappings.forEach(m => {
                $thead.append(`<th>${m.name}</th>`);
            });

            const $tbody = $('#wpsai-offline-table-body');
            $tbody.empty();
            offlineParsedRows.forEach(row => {
                let trHtml = '<tr>';
                mappings.forEach(m => {
                    const val = row[m.name] || '';
                    trHtml += `<td title="${val}" style="max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${val}</td>`;
                });
                trHtml += '</tr>';
                $tbody.append(trHtml);
            });

            $('#wpsai-offline-row-count-badge').text(`Tổng số dòng: ${offlineParsedRows.length} dòng`);
            $('#wpsai-offline-export-btn').prop('disabled', false);
            $('#wpsai-offline-export-json-btn').prop('disabled', false);

            logOffline(`Đã lọc thành công <strong>${offlineParsedRows.length}</strong> sản phẩm từ HTML!`, 'success');
        } catch (err) {
            logOffline(`Lỗi trong quá trình trích xuất: ${err.message}`, 'error');
            console.error(err);
        }
    });

    // Export to Excel
    $('#wpsai-offline-export-btn').on('click', function() {
        if (offlineParsedRows.length === 0) return;

        try {
            logOffline('Đang tạo tệp Excel...', 'info');
            // Clone and truncate values exceeding 32767 characters to avoid Excel limits
            const safeData = offlineParsedRows.map(row => {
                const safeRow = {};
                for (const key in row) {
                    if (row.hasOwnProperty(key)) {
                        let val = row[key];
                        if (typeof val === 'string' && val.length > 32760) {
                            val = val.substring(0, 32760);
                            logOffline(`Cảnh báo: Ô dữ liệu trường "${key}" vượt quá giới hạn Excel. Đã tự động cắt bớt còn 32,760 ký tự.`, 'error');
                        }
                        safeRow[key] = val;
                    }
                }
                return safeRow;
            });
            const worksheet = XLSX.utils.json_to_sheet(safeData);
            const workbook = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(workbook, worksheet, "Offline HTML Scraper");
            
            const date = new Date().toISOString().slice(0,10);
            const filename = `offline_scraper_output_${date}.xlsx`;

            XLSX.writeFile(workbook, filename);
            logOffline(`Xuất Excel thành công: <strong>${filename}</strong>`, 'success');
        } catch (e) {
            logOffline(`Lỗi xuất Excel: ${e.message}`, 'error');
        }
    });

    // Export to JSON
    $('#wpsai-offline-export-json-btn').on('click', function() {
        if (offlineParsedRows.length === 0) return;

        try {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(offlineParsedRows, null, 2));
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            
            const date = new Date().toISOString().slice(0,10);
            const filename = `offline_scraper_output_${date}.json`;
            downloadAnchor.setAttribute("download", filename);
            
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();

            logOffline(`Xuất JSON thành công: <strong>${filename}</strong>`, 'success');
        } catch (e) {
            logOffline(`Lỗi xuất JSON: ${e.message}`, 'error');
        }
    });

    // --- 11. TAB LẤY TIÊU ĐỀ BÀI VIẾT (GET POST TITLES) ---
    // Xử lý khi đổi Post Type ở tab Lấy Tiêu Đề
    $('#wpsai-titles-post-type').on('change', function () {
        const postType = $(this).val();
        const $taxSelect = $('#wpsai-titles-taxonomy');
        const $termSelect = $('#wpsai-titles-term');

        if (!postType) return;

        $taxSelect.empty().append('<option value="">-- Đang tải phân loại --</option>');
        $termSelect.empty().append('<option value="">-- Chọn danh mục / term --</option>').prop('disabled', true);

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_taxonomies_for_post_type',
                nonce: wpsai_params.nonce,
                post_type: postType
            },
            success: function (res) {
                $taxSelect.empty();
                $taxSelect.append('<option value="">-- Không lọc theo phân loại --</option>');
                if (res.success && res.data.length > 0) {
                    res.data.forEach(tax => {
                        $taxSelect.append(`<option value="${tax.slug}">${tax.label}</option>`);
                    });
                }
                $taxSelect.trigger('change');
            },
            error: function () {
                $taxSelect.empty().append('<option value="">-- Lỗi kết nối --</option>');
            }
        });
    });

    // Xử lý khi đổi Phân loại (Taxonomy) ở tab Lấy Tiêu Đề
    $('#wpsai-titles-taxonomy').on('change', function () {
        const taxonomy = $(this).val();
        const $termSelect = $('#wpsai-titles-term');

        if (!taxonomy) {
            $termSelect.empty().append('<option value="">-- Chọn danh mục / term --</option>').prop('disabled', true);
            return;
        }

        $termSelect.empty().append('<option value="">-- Đang tải danh mục --</option>').prop('disabled', true);

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_terms_by_taxonomy',
                nonce: wpsai_params.nonce,
                taxonomy: taxonomy
            },
            success: function (res) {
                $termSelect.empty();
                $termSelect.append('<option value="0">-- Tất cả danh mục / term --</option>');
                if (res.success && res.data.length > 0) {
                    res.data.forEach(term => {
                        $termSelect.append(`<option value="${term.id}">${term.name} (ID: ${term.id})</option>`);
                    });
                    $termSelect.prop('disabled', false);
                } else {
                    $termSelect.append('<option value="0" disabled>-- Không tìm thấy danh mục nào --</option>');
                }
            },
            error: function () {
                $termSelect.empty().append('<option value="0">-- Lỗi kết nối --</option>');
            }
        });
    });

    // Xử lý sự kiện click button Lấy danh sách tiêu đề
    $('#wpsai-get-titles-btn').on('click', function () {
        const postType = $('#wpsai-titles-post-type').val();
        const taxonomy = $('#wpsai-titles-taxonomy').val();
        const termId = $('#wpsai-titles-term').val();
        const $btn = $(this);
        const $resultCard = $('#wpsai-titles-result-card');
        const $textarea = $('#wpsai-titles-textarea');
        const $tableBody = $('#wpsai-titles-table tbody');

        if (!postType) {
            alert('Vui lòng chọn Post Type trước!');
            return;
        }

        $btn.prop('disabled', true).text('Đang lấy dữ liệu...');
        $resultCard.fadeOut();

        $.ajax({
            url: wpsai_params.ajax_url,
            type: 'POST',
            data: {
                action: 'wpsai_get_post_titles',
                nonce: wpsai_params.nonce,
                post_type: postType,
                taxonomy: taxonomy,
                term_id: termId
            },
            success: function (res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-editor-ul"></span> Lấy Danh Sách Tiêu Đề');
                if (res.success) {
                    const posts = res.data;
                    currentExtractedPosts = posts;
                    $('#wpsai-titles-count').text(posts.length);
                    $('#wpsai-titles-select-all').prop('checked', true); // Reset Select All
                    
                    // Điền vào textarea
                    let titlesText = '';
                    $tableBody.empty();

                    if (posts.length > 0) {
                        posts.forEach(post => {
                            titlesText += post.title + '\n';
                            
                            const trHtml = `
                                <tr>
                                    <td style="text-align: center;">
                                        <input type="checkbox" class="wpsai-title-select" data-post-id="${post.id}" checked>
                                    </td>
                                    <td><code>${post.id}</code></td>
                                    <td><strong>${post.title}</strong></td>
                                    <td><span style="font-size:12px; color:#475569;">${post.terms ? post.terms : '-'}</span></td>
                                    <td><span style="font-family:monospace; font-size:12px;">${post.post_date}</span></td>
                                    <td style="text-align: center;">
                                        <a href="${post.permalink}" target="_blank" class="wpsai-btn wpsai-btn-secondary" style="padding: 4px 8px; font-size:12px; margin:0;" title="Xem bài viết">
                                            <span class="dashicons dashicons-external" style="font-size:14px; width:14px; height:14px; margin-top:-2px;"></span>
                                        </a>
                                    </td>
                                </tr>
                            `;
                            $tableBody.append(trHtml);
                        });
                        $textarea.val(titlesText.trim());
                        $('#wpsai-titles-new-textarea').val('');
                        $('#wpsai-titles-update-progress').hide();
                        $('#wpsai-titles-update-card').fadeIn();
                    } else {
                        $textarea.val('Không tìm thấy bài viết nào phù hợp.');
                        $tableBody.append('<tr><td colspan="6" style="text-align:center; font-style:italic; color:#64748b;">Không có bài viết nào được tìm thấy.</td></tr>');
                        $('#wpsai-titles-update-card').fadeOut();
                    }

                    validateTitlesCount();
                    $resultCard.fadeIn();
                } else {
                    alert('Lỗi: ' + (res.data.message || 'Không thể lấy dữ liệu.'));
                }
            },
            error: function () {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-editor-ul"></span> Lấy Danh Sách Tiêu Đề');
                alert('Lỗi kết nối máy chủ khi lấy danh sách tiêu đề.');
            }
        });
    });

    // Copy toàn bộ tiêu đề vào clipboard
    $('#wpsai-copy-titles-btn').on('click', function () {
        const text = $('#wpsai-titles-textarea').val();
        if (!text || text.indexOf('Không tìm thấy') === 0) {
            return;
        }

        navigator.clipboard.writeText(text).then(() => {
            const $btn = $(this);
            const origText = $btn.html();
            $btn.html('<span class="dashicons dashicons-saved"></span> Đã sao chép!').css('color', '#10b981');
            setTimeout(() => {
                $btn.html(origText).css('color', '');
            }, 2000);
        }).catch(err => {
            alert('Lỗi sao chép: ' + err);
        });
    });

    // Xử lý sự kiện Check-All
    $('#wpsai-titles-select-all').on('change', function () {
        const isChecked = $(this).is(':checked');
        $('.wpsai-title-select').prop('checked', isChecked);
        
        // Cập nhật lại khung tiêu đề gốc hiển thị dựa trên các bài viết được tích chọn
        updateOriginalTitlesTextarea();
        validateTitlesCount();
    });

    // Xử lý sự kiện thay đổi từng checkbox lẻ
    $(document).on('change', '.wpsai-title-select', function () {
        const total = $('.wpsai-title-select').length;
        const checked = $('.wpsai-title-select:checked').length;
        $('#wpsai-titles-select-all').prop('checked', total === checked);
        
        // Cập nhật lại khung tiêu đề gốc hiển thị dựa trên các bài viết được tích chọn
        updateOriginalTitlesTextarea();
        validateTitlesCount();
    });

    // Hàm cập nhật danh sách tiêu đề gốc trong textarea bên trái dựa trên các bài viết được chọn
    function updateOriginalTitlesTextarea() {
        let text = '';
        $('.wpsai-title-select:checked').each(function() {
            const postId = $(this).data('post-id');
            const postObj = currentExtractedPosts.find(p => p.id === postId);
            if (postObj) {
                text += postObj.title + '\n';
            }
        });
        $('#wpsai-titles-textarea').val(text.trim());
    }

    // Hàm đếm số dòng và đối chiếu số lượng tiêu đề mới
    function validateTitlesCount() {
        const text = $('#wpsai-titles-new-textarea').val() || '';
        const lines = text.split(/\r?\n/).map(line => line.trim()).filter(line => line.length > 0);
        const targetCount = $('.wpsai-title-select:checked').length;
        const inputCount = lines.length;

        $('#wpsai-target-posts-count').text(targetCount);
        $('#wpsai-new-titles-count').text(inputCount);

        const $badge = $('#wpsai-titles-match-badge');
        const $btn = $('#wpsai-execute-update-titles-btn');

        if (targetCount > 0 && targetCount === inputCount) {
            $badge.text('Khớp số lượng').css('background', '#10b981'); // Emerald green
            $btn.prop('disabled', false);
        } else {
            $badge.text('Chưa khớp').css('background', '#ef4444'); // Red
            $btn.prop('disabled', true);
        }
    }

    // Lắng nghe sự kiện gõ/paste trong textarea tiêu đề mới
    $('#wpsai-titles-new-textarea').on('input paste keyup change', function () {
        validateTitlesCount();
    });

    // Xử lý nút Dịch Tiêu Đề Bằng AI
    $('#wpsai-translate-titles-btn').on('click', function () {
        const $checkedBoxes = $('.wpsai-title-select:checked');
        const targetCount = $checkedBoxes.length;

        if (targetCount === 0) {
            alert('Vui lòng tích chọn ít nhất 1 bài viết trong bảng để dịch!');
            return;
        }

        const targetLang = $('#wpsai-titles-target-lang').val();
        const translateContent = $('#wpsai-titles-translate-content-checkbox').is(':checked');
        const translatorEngine = $('#wpsai-titles-translator-engine').val() || 'google_translate';
        
        const titlesToTranslate = [];
        const postsDataToTranslate = [];

        $checkedBoxes.each(function () {
            const postId = $(this).data('post-id');
            const postObj = currentExtractedPosts.find(p => p.id === postId);
            if (postObj) {
                titlesToTranslate.push(postObj.title);
                postsDataToTranslate.push({
                    id: postObj.id,
                    title: postObj.title,
                    content: postObj.content || '',
                    excerpt: postObj.excerpt || ''
                });
            }
        });

        const $btn = $(this);
        const originalHtml = $btn.html();
        
        // Ẩn thông báo lỗi cũ
        $('#wpsai-titles-translation-error').hide().empty();

        const engineLabel = translatorEngine === 'google_translate' ? 'Google' : 'AI';

        if (translateContent) {
            // Đóng khóa nút dịch
            $btn.prop('disabled', true);

            // Dịch từng bài viết một để tránh timeout (cURL error 28)
            let currentIndex = 0;
            const translatedTitles = [];
            currentTranslatedData = {};

            function translateNextPost() {
                if (currentIndex >= targetCount) {
                    $btn.prop('disabled', false).html(originalHtml);
                    $('#wpsai-titles-new-textarea').val(translatedTitles.join('\n'));
                    validateTitlesCount();
                    return;
                }

                const postObj = postsDataToTranslate[currentIndex];
                $btn.text(`Đang dịch (${engineLabel}) (${currentIndex + 1}/${targetCount})...`);

                $.ajax({
                    url: wpsai_params.ajax_url,
                    type: 'POST',
                    data: {
                        action: 'wpsai_translate_post_titles',
                        nonce: wpsai_params.nonce,
                        target_lang: targetLang,
                        translator_engine: translatorEngine,
                        translate_content: true,
                        posts_data: JSON.stringify([postObj])
                    },
                    success: function (res) {
                        if (res.success && Array.isArray(res.data) && res.data.length > 0) {
                            const item = res.data[0];
                            currentTranslatedData[item.id] = {
                                title: item.title,
                                content: item.content,
                                excerpt: item.excerpt
                            };
                            translatedTitles.push(item.title);
                            
                            currentIndex++;
                            translateNextPost();
                        } else {
                            const errMsg = res.data && res.data.message ? res.data.message : 'Định dạng dữ liệu dịch từ AI không hợp lệ.';
                            
                            // Kiểm tra lỗi Rate Limit 429 hoặc giới hạn cuộc gọi
                            if (errMsg.indexOf('429') !== -1 || errMsg.indexOf('RESOURCE_EXHAUSTED') !== -1 || errMsg.indexOf('Quota exceeded') !== -1) {
                                // Tìm kiếm thời gian chờ gợi ý từ thông báo lỗi của Google
                                let waitSeconds = 15; // Mặc định 15 giây
                                const matchSeconds = errMsg.match(/retry in\s+([0-9\.]+)\s*s/i) || errMsg.match(/retryDelay:\s*"([0-9\.]+)\s*s"/i);
                                if (matchSeconds && matchSeconds[1]) {
                                    waitSeconds = Math.ceil(parseFloat(matchSeconds[1])) + 2; // Cộng thêm 2 giây cho an toàn
                                }

                                const $logError = $('#wpsai-titles-translation-error');
                                $logError.html(`<span class="dashicons dashicons-warning" style="color: #ea580c; vertical-align: middle; margin-right: 5px;"></span> Bị giới hạn tần suất gọi AI (Rate Limit 429). Hệ thống sẽ tự động thử lại sau <strong>${waitSeconds}</strong> giây...<br><span style="font-size: 11px; opacity: 0.8;">Chi tiết lỗi: ${errMsg}</span>`).fadeIn();

                                let remaining = waitSeconds;
                                const timerInterval = setInterval(() => {
                                    remaining--;
                                    if (remaining <= 0) {
                                        clearInterval(timerInterval);
                                        $logError.hide().empty();
                                        // Thử lại bài viết hiện tại
                                        translateNextPost();
                                    } else {
                                        $btn.text(`Đang chờ AI reset (${remaining}s)...`);
                                    }
                                }, 1000);
                            } else {
                                $btn.prop('disabled', false).html(originalHtml);
                                $('#wpsai-titles-translation-error').text(`Lỗi dịch ở bài viết thứ ${currentIndex + 1} (ID: ${postObj.id}): ${errMsg}`).fadeIn();
                            }
                        }
                    },
                    error: function (xhr, status, err) {
                        $btn.prop('disabled', false).html(originalHtml);
                        $('#wpsai-titles-translation-error').text(`Lỗi kết nối khi dịch bài viết thứ ${currentIndex + 1} (ID: ${postObj.id}): ${err || status}`).fadeIn();
                    }
                });
            }

            translateNextPost();
        } else {
            $btn.prop('disabled', true).text(`Đang dịch (${engineLabel})...`);

            // Dịch tất cả tiêu đề trong một lượt vì tiêu đề rất ngắn
            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: {
                    action: 'wpsai_translate_post_titles',
                    nonce: wpsai_params.nonce,
                    target_lang: targetLang,
                    translator_engine: translatorEngine,
                    translate_content: false,
                    titles: titlesToTranslate
                },
                success: function (res) {
                    $btn.prop('disabled', false).html(originalHtml);
                    if (res.success) {
                        const translated = res.data;
                        currentTranslatedData = {};
                        if (Array.isArray(translated)) {
                            $('#wpsai-titles-new-textarea').val(translated.join('\n'));
                            validateTitlesCount();
                        } else {
                            $('#wpsai-titles-translation-error').text('Lỗi: Định dạng dữ liệu dịch từ AI/Google không hợp lệ.').fadeIn();
                        }
                    } else {
                        $('#wpsai-titles-translation-error').text('Lỗi dịch: ' + (res.data.message || 'Không thể dịch.')).fadeIn();
                    }
                },
                error: function () {
                    $btn.prop('disabled', false).html(originalHtml);
                    $('#wpsai-titles-translation-error').text('Lỗi kết nối máy chủ khi gọi dịch thuật.').fadeIn();
                }
            });
        }
    });

    // Xử lý click nút Cập Nhật Hàng Loạt Tiêu Đề
    $('#wpsai-execute-update-titles-btn').on('click', function () {
        const text = $('#wpsai-titles-new-textarea').val() || '';
        const lines = text.split(/\r?\n/).map(line => line.trim()).filter(line => line.length > 0);
        const $checkedBoxes = $('.wpsai-title-select:checked');
        const targetCount = $checkedBoxes.length;

        if (targetCount === 0 || targetCount !== lines.length) {
            alert('Số lượng tiêu đề mới không khớp với số lượng bài viết đã chọn!');
            return;
        }

        if (!confirm('Bạn có chắc chắn muốn cập nhật tiêu đề mới cho các bài viết đã chọn này? Hành động này không thể hoàn tác.')) {
            return;
        }

        // Lấy danh sách bài viết mục tiêu đã chọn
        const targetPosts = [];
        $checkedBoxes.each(function () {
            const postId = $(this).data('post-id');
            const postObj = currentExtractedPosts.find(p => p.id === postId);
            if (postObj) {
                targetPosts.push(postObj);
            }
        });

        const $btn = $(this);
        const $progress = $('#wpsai-titles-update-progress');
        const $progressBar = $('#wpsai-titles-update-progress-bar');
        const $progressStats = $('#wpsai-titles-update-progress-stats');
        const $log = $('#wpsai-titles-update-log');

        $btn.prop('disabled', true).text('Đang cập nhật...');
        $('#wpsai-titles-new-textarea').prop('readonly', true);
        $progress.slideDown();
        $log.empty().append('<p>Khởi động hàng đợi cập nhật...</p>');
        $progressBar.css('width', '0%').text('0%');

        let currentIndex = 0;
        let successCount = 0;
        let errorCount = 0;

        function runNextUpdate() {
            if (currentIndex >= targetCount) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-saved"></span> Cập Nhật Hàng Loạt Tiêu Đề');
                $('#wpsai-titles-new-textarea').prop('readonly', false);
                $log.append('<p style="color:#10b981; font-weight:bold; margin-top:5px;">✓ Quá trình cập nhật hoàn thành!</p>');
                $log.scrollTop($log[0].scrollHeight);
                alert(`Cập nhật hoàn thành! Thành công: ${successCount}, Lỗi: ${errorCount}`);
                return;
            }

            const post = targetPosts[currentIndex];
            const newTitle = lines[currentIndex];

            $log.append(`<p>Đang cập nhật ${currentIndex + 1}/${targetCount}: [ID: ${post.id}] từ "${post.title}" -> "${newTitle}"...</p>`);
            $log.scrollTop($log[0].scrollHeight);

            const postPayload = {
                action: 'wpsai_update_post_title',
                nonce: wpsai_params.nonce,
                post_id: post.id,
                new_title: newTitle
            };

            const translatedPost = currentTranslatedData[post.id];
            if (translatedPost) {
                postPayload.new_content = translatedPost.content;
                postPayload.new_excerpt = translatedPost.excerpt;
            }

            $.ajax({
                url: wpsai_params.ajax_url,
                type: 'POST',
                data: postPayload,
                success: function (res) {
                    if (res.success) {
                        successCount++;
                        $log.append(`<p style="color:#10b981; margin:0 0 5px 15px;">✓ Thành công: [ID: ${post.id}]</p>`);
                        
                        // Cập nhật thông số bài viết cục bộ
                        post.title = newTitle;
                        if (translatedPost) {
                            post.content = translatedPost.content;
                            post.excerpt = translatedPost.excerpt;
                        }

                        // Cập nhật trực tiếp trên bảng kết quả
                        const $row = $(`#wpsai-titles-table tbody tr`).filter(function() {
                            return $(this).find('td:first input.wpsai-title-select').data('post-id') === post.id;
                        });
                        if ($row.length > 0) {
                            $row.find('td:eq(2) strong').text(newTitle); // Note: Col 0 is checkbox, Col 1 is ID code, Col 2 is title strong
                            $row.css('background-color', '#ecfdf5'); // Highlight row in green
                            setTimeout(function() {
                                $row.css('background-color', '');
                            }, 3000);
                        }
                    } else {
                        errorCount++;
                        $log.append(`<p style="color:#ef4444; margin:0 0 5px 15px;">✗ Thất bại: ${res.data.message || 'Lỗi không xác định'}</p>`);
                    }

                    currentIndex++;
                    const percent = Math.round((currentIndex / targetCount) * 100);
                    $progressBar.css('width', percent + '%').text(percent + '%');
                    $progressStats.html(`<p>Đang xử lý ${currentIndex}/${targetCount}. Thành công: ${successCount}, Lỗi: ${errorCount}</p>`);

                    setTimeout(runNextUpdate, 150);
                },
                error: function () {
                    errorCount++;
                    $log.append(`<p style="color:#ef4444; margin:0 0 5px 15px;">✗ Lỗi kết nối HTTP.</p>`);
                    
                    currentIndex++;
                    const percent = Math.round((currentIndex / targetCount) * 100);
                    $progressBar.css('width', percent + '%').text(percent + '%');
                    $progressStats.html(`<p>Đang xử lý ${currentIndex}/${targetCount}. Thành công: ${successCount}, Lỗi: ${errorCount}</p>`);

                    setTimeout(runNextUpdate, 150);
                }
            });
        }

        runNextUpdate();
    });

    // ============================================================
    // SNAPSHOT DATA REPOSITORY - Kho Lưu Trữ Dữ Liệu Mẫu
    // ============================================================
    (function() {
        // Dữ liệu quét tạm thời
        let snapScanResult = null;

        // --- Tải danh sách Post Type khi vào tab ---
        function snapLoadPostTypes() {
            $.post(ajaxurl, {
                action: 'wpsai_get_post_types_and_fields',
                nonce: wpsai_data.nonce
            }, function(res) {
                if (res.success && res.data) {
                    const $sel = $('#wpsai-snap-post-type');
                    $sel.empty().append('<option value="">-- Chọn Post Type --</option>');
                    res.data.forEach(function(pt) {
                        $sel.append('<option value="' + pt.slug + '">' + pt.label + '</option>');
                    });
                }
            });
        }

        // Load ngay khi DOM ready
        snapLoadPostTypes();

        // --- Khi chọn Post Type -> tải Taxonomy ---
        $('#wpsai-snap-post-type').on('change', function() {
            const postType = $(this).val();
            const $taxSel = $('#wpsai-snap-taxonomy');
            const $termSel = $('#wpsai-snap-term');
            $taxSel.empty().append('<option value="">-- Không lọc --</option>');
            $termSel.empty().append('<option value="">-- Chọn Taxonomy trước --</option>').prop('disabled', true);

            if (!postType) return;

            $.post(ajaxurl, {
                action: 'wpsai_get_taxonomies_for_post_type',
                nonce: wpsai_data.nonce,
                post_type: postType
            }, function(res) {
                if (res.success && res.data) {
                    res.data.forEach(function(tax) {
                        $taxSel.append('<option value="' + tax.slug + '">' + tax.label + '</option>');
                    });
                }
            });
        });

        // --- Khi chọn Taxonomy -> tải Terms ---
        $('#wpsai-snap-taxonomy').on('change', function() {
            const taxonomy = $(this).val();
            const $termSel = $('#wpsai-snap-term');
            $termSel.empty().append('<option value="">-- Tất cả --</option>');

            if (!taxonomy) {
                $termSel.prop('disabled', true);
                return;
            }

            $termSel.prop('disabled', false);
            $.post(ajaxurl, {
                action: 'wpsai_get_terms_by_taxonomy',
                nonce: wpsai_data.nonce,
                taxonomy: taxonomy
            }, function(res) {
                if (res.success && res.data) {
                    res.data.forEach(function(term) {
                        const prefix = term.depth ? '— '.repeat(term.depth) : '';
                        $termSel.append('<option value="' + term.term_id + '">' + prefix + term.name + ' (' + term.count + ')</option>');
                    });
                }
            });
        });

        // --- Quét Dữ Liệu ---
        $('#wpsai-snap-scan-btn').on('click', function() {
            const postType = $('#wpsai-snap-post-type').val();
            if (!postType) {
                alert('Vui lòng chọn Post Type trước khi quét.');
                return;
            }

            const $btn = $(this);
            $btn.prop('disabled', true).html('<span class="dashicons dashicons-update wpsai-spin"></span> Đang quét...');

            $.post(ajaxurl, {
                action: 'wpsai_snapshot_scan',
                nonce: wpsai_data.nonce,
                post_type: postType,
                taxonomy: $('#wpsai-snap-taxonomy').val(),
                term_id: $('#wpsai-snap-term').val()
            }, function(res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-search"></span> Quét Toàn Bộ Dữ Liệu');

                if (res.success && res.data) {
                    snapScanResult = res.data;
                    snapRenderPreview(res.data);
                    snapShowStats(res.data);
                } else {
                    alert('Lỗi quét: ' + (res.data ? res.data.message : 'Không xác định'));
                }
            }).fail(function() {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-search"></span> Quét Toàn Bộ Dữ Liệu');
                alert('Lỗi kết nối HTTP. Vui lòng thử lại.');
            });
        });

        // --- Hiển thị thống kê ---
        function snapShowStats(data) {
            const jsonSize = new Blob([JSON.stringify(data)]).size;
            $('#wpsai-snap-stat-posts').text(data.post_count || data.posts.length);
            $('#wpsai-snap-stat-fields').text(data.schema ? data.schema.length : 0);
            if (jsonSize > 1024 * 1024) {
                $('#wpsai-snap-stat-size').text((jsonSize / (1024 * 1024)).toFixed(2) + ' MB');
            } else {
                $('#wpsai-snap-stat-size').text((jsonSize / 1024).toFixed(1) + ' KB');
            }
            $('#wpsai-snap-scan-stats').slideDown(200);
        }

        // --- Render bảng preview ---
        function snapRenderPreview(data) {
            if (!data.posts || data.posts.length === 0) {
                $('#wpsai-snap-preview-empty').show().find('p').text('Không tìm thấy bài viết nào.');
                $('#wpsai-snap-preview-content').hide();
                return;
            }

            const showCols = ['post_id', 'post_title', 'post_status', 'post_date'];
            // Thêm 2 cột ACF đầu tiên nếu có
            if (data.schema) {
                let acfCount = 0;
                data.schema.forEach(function(s) {
                    if (s.name.startsWith('acf_') && acfCount < 2) {
                        showCols.push(s.name);
                        acfCount++;
                    }
                });
            }

            const colLabels = { post_id: 'ID', post_title: 'Tiêu đề', post_status: 'Trạng thái', post_date: 'Ngày đăng' };
            if (data.schema) {
                data.schema.forEach(function(s) { colLabels[s.name] = s.label; });
            }

            let thead = '';
            showCols.forEach(function(col) {
                thead += '<th style="white-space: nowrap; font-size: 11px;">' + (colLabels[col] || col) + '</th>';
            });
            $('#wpsai-snap-preview-thead').html(thead);

            let tbody = '';
            const previewPosts = data.posts.slice(0, 10);
            previewPosts.forEach(function(post) {
                tbody += '<tr>';
                showCols.forEach(function(col) {
                    let val = post[col] !== undefined ? post[col] : '';
                    if (typeof val === 'string' && val.length > 80) {
                        val = val.substring(0, 80) + '...';
                    }
                    // Escape HTML
                    val = $('<span>').text(val).html();
                    tbody += '<td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">' + val + '</td>';
                });
                tbody += '</tr>';
            });

            if (data.posts.length > 10) {
                tbody += '<tr><td colspan="' + showCols.length + '" style="text-align: center; color: #6b7280; font-style: italic;">... và ' + (data.posts.length - 10) + ' bài viết khác</td></tr>';
            }

            $('#wpsai-snap-preview-tbody').html(tbody);
            $('#wpsai-snap-preview-empty').hide();
            $('#wpsai-snap-preview-content').show();

            // Auto-fill tên snapshot
            const postType = $('#wpsai-snap-post-type option:selected').text();
            const now = new Date();
            const dateStr = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
            $('#wpsai-snap-name').val(postType.replace(/\(.*?\)/g, '').trim() + ' - ' + dateStr);
        }

        // --- Lưu Snapshot ---
        $('#wpsai-snap-save-btn').on('click', function() {
            if (!snapScanResult || !snapScanResult.posts || snapScanResult.posts.length === 0) {
                alert('Không có dữ liệu để lưu. Hãy quét trước.');
                return;
            }

            const snapshotName = $('#wpsai-snap-name').val().trim();
            if (!snapshotName) {
                alert('Vui lòng đặt tên cho snapshot.');
                return;
            }

            const $btn = $(this);
            $btn.prop('disabled', true).html('<span class="dashicons dashicons-update wpsai-spin"></span> Đang lưu...');
            $('#wpsai-snap-save-msg').html('');

            $.post(ajaxurl, {
                action: 'wpsai_snapshot_save',
                nonce: wpsai_data.nonce,
                snapshot_name: snapshotName,
                snapshot_data: JSON.stringify({ schema: snapScanResult.schema, posts: snapScanResult.posts }),
                post_type: snapScanResult.post_type,
                post_count: snapScanResult.posts.length
            }, function(res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-database-add"></span> Lưu Vào Kho');
                if (res.success) {
                    $('#wpsai-snap-save-msg').html('<span style="color: #059669;">✓ ' + res.data.message + '</span>');
                    snapLoadList(); // Refresh danh sách
                } else {
                    $('#wpsai-snap-save-msg').html('<span style="color: #ef4444;">✗ ' + (res.data ? res.data.message : 'Lỗi không xác định') + '</span>');
                }
            }).fail(function() {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-database-add"></span> Lưu Vào Kho');
                $('#wpsai-snap-save-msg').html('<span style="color: #ef4444;">✗ Lỗi kết nối HTTP</span>');
            });
        });

        // --- Tải danh sách snapshot ---
        function snapLoadList() {
            $.post(ajaxurl, {
                action: 'wpsai_snapshot_list',
                nonce: wpsai_data.nonce
            }, function(res) {
                if (res.success && res.data) {
                    const snapshots = res.data.snapshots;
                    if (snapshots.length === 0) {
                        $('#wpsai-snap-list-empty').show();
                        $('#wpsai-snap-list-content').hide();
                        return;
                    }

                    let tbody = '';
                    snapshots.forEach(function(snap, idx) {
                        tbody += '<tr>';
                        tbody += '<td style="color: #94a3b8;">' + (idx + 1) + '</td>';
                        tbody += '<td><strong style="color: #1e293b;">' + $('<span>').text(snap.name).html() + '</strong></td>';
                        tbody += '<td><code style="background: #f1f5f9; padding: 2px 8px; border-radius: 4px; font-size: 11px;">' + snap.post_type + '</code></td>';
                        tbody += '<td style="text-align: center;"><span style="background: #dbeafe; color: #1d4ed8; padding: 3px 10px; border-radius: 99px; font-size: 12px; font-weight: 600;">' + snap.post_count + '</span></td>';
                        tbody += '<td style="font-size: 12px; color: #64748b;">' + (snap.file_size_formatted || '-') + '</td>';
                        tbody += '<td style="font-size: 12px; color: #64748b;">' + snap.created_at + '</td>';
                        tbody += '<td style="text-align: center;">';
                        tbody += '<button type="button" class="wpsai-btn wpsai-btn-secondary wpsai-snap-view-btn" data-id="' + snap.id + '" data-name="' + $('<span>').text(snap.name).html() + '" style="margin: 2px; padding: 4px 10px; font-size: 11px;"><span class="dashicons dashicons-visibility" style="font-size: 14px; width: 14px; height: 14px;"></span> Xem</button>';
                        tbody += '<button type="button" class="wpsai-btn wpsai-btn-secondary wpsai-snap-del-btn" data-id="' + snap.id + '" data-name="' + $('<span>').text(snap.name).html() + '" style="margin: 2px; padding: 4px 10px; font-size: 11px; color: #ef4444; border-color: #fca5a5;"><span class="dashicons dashicons-trash" style="font-size: 14px; width: 14px; height: 14px;"></span> Xóa</button>';
                        tbody += '</td>';
                        tbody += '</tr>';
                    });

                    $('#wpsai-snap-list-tbody').html(tbody);
                    $('#wpsai-snap-list-empty').hide();
                    $('#wpsai-snap-list-content').show();
                }
            });
        }

        // Load danh sách khi page ready
        snapLoadList();

        // Nút Làm Mới
        $('#wpsai-snap-refresh-btn').on('click', function() {
            snapLoadList();
        });

        // --- Xem chi tiết snapshot ---
        $(document).on('click', '.wpsai-snap-view-btn', function() {
            const snapId = $(this).data('id');
            const snapName = $(this).data('name');

            $('#wpsai-snap-detail-name').text(snapName);
            $('#wpsai-snap-detail-card').data('snapshot-id', snapId).slideDown(300);
            $('#wpsai-snap-detail-thead, #wpsai-snap-detail-tbody').html('');
            $('#wpsai-snap-restore-progress').hide();

            // Scroll tới card chi tiết
            $('html, body').animate({ scrollTop: $('#wpsai-snap-detail-card').offset().top - 60 }, 300);

            $.post(ajaxurl, {
                action: 'wpsai_snapshot_detail',
                nonce: wpsai_data.nonce,
                snapshot_id: snapId
            }, function(res) {
                if (res.success && res.data) {
                    snapRenderDetail(res.data);
                } else {
                    alert('Lỗi: ' + (res.data ? res.data.message : 'Không xác định'));
                }
            });
        });

        function snapRenderDetail(data) {
            if (!data.posts || data.posts.length === 0) {
                $('#wpsai-snap-detail-tbody').html('<tr><td style="text-align: center; color: #94a3b8;">Không có bài viết.</td></tr>');
                return;
            }

            // Xây cột header từ schema + post_id
            const showCols = ['post_id'];
            const colLabels = { post_id: 'ID' };

            if (data.schema) {
                data.schema.forEach(function(s) {
                    showCols.push(s.name);
                    colLabels[s.name] = s.label;
                });
            } else {
                // Fallback: lấy keys từ post đầu tiên
                Object.keys(data.posts[0]).forEach(function(k) {
                    if (k !== 'post_id') {
                        showCols.push(k);
                        colLabels[k] = k;
                    }
                });
            }

            let thead = '';
            showCols.forEach(function(col) {
                thead += '<th style="white-space: nowrap; font-size: 11px; min-width: 80px;">' + (colLabels[col] || col) + '</th>';
            });
            $('#wpsai-snap-detail-thead').html(thead);

            let tbody = '';
            data.posts.forEach(function(post) {
                tbody += '<tr>';
                showCols.forEach(function(col) {
                    let val = post[col] !== undefined ? String(post[col]) : '';
                    if (val.length > 120) {
                        val = val.substring(0, 120) + '...';
                    }
                    val = $('<span>').text(val).html();
                    tbody += '<td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">' + val + '</td>';
                });
                tbody += '</tr>';
            });

            $('#wpsai-snap-detail-tbody').html(tbody);
            // Lưu dữ liệu snapshot để dùng khi restore/export
            $('#wpsai-snap-detail-card').data('snapshot-data', data);
        }

        // Đóng chi tiết
        $('#wpsai-snap-detail-close').on('click', function() {
            $('#wpsai-snap-detail-card').slideUp(200);
        });

        // --- Khôi phục snapshot ---
        $('#wpsai-snap-restore-btn').on('click', function() {
            const snapId = $('#wpsai-snap-detail-card').data('snapshot-id');
            const snapData = $('#wpsai-snap-detail-card').data('snapshot-data');
            const restoreMode = $('#wpsai-snap-restore-mode').val();

            if (!snapId || !snapData || !snapData.posts || snapData.posts.length === 0) {
                alert('Không có dữ liệu để khôi phục.');
                return;
            }

            const modeText = restoreMode === 'create_new' ? 'TẠO MỚI' : 'GHI ĐÈ';
            if (!confirm('Bạn có chắc muốn khôi phục ' + snapData.posts.length + ' bài viết (' + modeText + ')?\n\nHành động này không thể hoàn tác.')) {
                return;
            }

            const $btn = $(this);
            $btn.prop('disabled', true);
            const $progress = $('#wpsai-snap-restore-progress');
            const $bar = $('#wpsai-snap-restore-bar');
            const $log = $('#wpsai-snap-restore-log');
            $progress.show();
            $bar.css('width', '0%').text('0%');
            $log.html('');

            const total = snapData.posts.length;
            let current = 0;
            let successCount = 0;
            let errorCount = 0;

            function restoreNext() {
                if (current >= total) {
                    $btn.prop('disabled', false);
                    $log.append('<p style="color: #059669; font-weight: 600; margin: 4px 0;">✓ Hoàn tất! Thành công: ' + successCount + ', Lỗi: ' + errorCount + '</p>');
                    $log.scrollTop($log[0].scrollHeight);
                    snapLoadList();
                    return;
                }

                $.post(ajaxurl, {
                    action: 'wpsai_snapshot_restore',
                    nonce: wpsai_data.nonce,
                    snapshot_id: snapId,
                    restore_mode: restoreMode,
                    post_index: current
                }, function(res) {
                    if (res.success) {
                        successCount++;
                        $log.append('<p style="color: #059669; margin: 2px 0;">✓ ' + res.data.post_title + ' (ID: ' + res.data.post_id + ')</p>');
                    } else {
                        errorCount++;
                        $log.append('<p style="color: #ef4444; margin: 2px 0;">✗ Bài #' + (current + 1) + ': ' + (res.data ? res.data.message : 'Lỗi') + '</p>');
                    }

                    current++;
                    const percent = Math.round((current / total) * 100);
                    $bar.css('width', percent + '%').text(percent + '%');
                    $log.scrollTop($log[0].scrollHeight);

                    setTimeout(restoreNext, 200);
                }).fail(function() {
                    errorCount++;
                    $log.append('<p style="color: #ef4444; margin: 2px 0;">✗ Bài #' + (current + 1) + ': Lỗi kết nối HTTP</p>');
                    current++;
                    const percent = Math.round((current / total) * 100);
                    $bar.css('width', percent + '%').text(percent + '%');
                    setTimeout(restoreNext, 200);
                });
            }

            restoreNext();
        });

        // --- Xuất JSON ---
        $('#wpsai-snap-export-json-btn').on('click', function() {
            const snapData = $('#wpsai-snap-detail-card').data('snapshot-data');
            if (!snapData) {
                alert('Không có dữ liệu để xuất.');
                return;
            }

            const jsonStr = JSON.stringify(snapData, null, 2);
            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = ($('#wpsai-snap-detail-name').text() || 'snapshot') + '.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });

        // --- Xóa snapshot ---
        $(document).on('click', '.wpsai-snap-del-btn', function() {
            const snapId = $(this).data('id');
            const snapName = $(this).data('name');

            if (!confirm('Xóa vĩnh viễn snapshot "' + snapName + '"?\n\nFile JSON sẽ bị xóa khỏi server.')) {
                return;
            }

            const $btn = $(this);
            $btn.prop('disabled', true).text('Đang xóa...');

            $.post(ajaxurl, {
                action: 'wpsai_snapshot_delete',
                nonce: wpsai_data.nonce,
                snapshot_id: snapId
            }, function(res) {
                if (res.success) {
                    snapLoadList();
                    // Đóng chi tiết nếu đang xem snapshot này
                    if ($('#wpsai-snap-detail-card').data('snapshot-id') === snapId) {
                        $('#wpsai-snap-detail-card').slideUp(200);
                    }
                } else {
                    $btn.prop('disabled', false).html('<span class="dashicons dashicons-trash" style="font-size: 14px; width: 14px; height: 14px;"></span> Xóa');
                    alert('Lỗi: ' + (res.data ? res.data.message : 'Không xác định'));
                }
            });
        });

        // ============================================================
        // TREE HIERARCHY REPOSITORY LOGIC (CÂY DỮ LIỆU PHÂN MẢNH)
        // ============================================================
        function snapLoadTreeManifest() {
            $('#wpsai-tree-loading').show();
            $('#wpsai-tree-root').hide().empty();

            $.post(ajaxurl, {
                action: 'wpsai_tree_get_manifest',
                nonce: wpsai_data.nonce
            }, function(res) {
                $('#wpsai-tree-loading').hide();
                if (res.success && res.data && res.data.nodes) {
                    const $root = $('#wpsai-tree-root');
                    res.data.nodes.forEach(function(node) {
                        $root.append(buildTreeNodeHTML(node));
                    });
                    $root.show();
                } else {
                    $('#wpsai-tree-loading').html('<p style="color: #ef4444;">Lỗi tải cây dữ liệu</p>').show();
                }
            });
        }

        function buildTreeNodeHTML(node) {
            const hasChildren = node.children && node.children.length > 0;
            const hasChunks = node.chunks && node.chunks.length > 0;

            let icon = 'dashicons-category';
            if (node.type === 'post_type') icon = 'dashicons-admin-post';
            if (node.type === 'workflows') icon = 'dashicons-networking';
            if (node.type === 'term') icon = 'dashicons-tag';
            if (node.type === 'workflow_item') icon = 'dashicons-media-text';

            let html = '<li style="margin: 6px 0; font-size: 13px;">';
            html += '<div style="display: flex; align-items: center; gap: 8px; padding: 4px 8px; border-radius: 6px; background: #f8fafc; border: 1px solid #e2e8f0;">';

            if (hasChildren) {
                html += '<span class="dashicons dashicons-arrow-right-alt2 wpsai-tree-toggle" style="cursor: pointer; color: #64748b; font-size: 16px; width: 16px; height: 16px;"></span>';
            } else {
                html += '<span style="display: inline-block; width: 16px;"></span>';
            }

            html += '<span class="dashicons ' + icon + '" style="color: #0284c7; font-size: 16px; width: 16px; height: 16px;"></span>';
            html += '<strong style="color: #1e293b;">' + $('<span>').text(node.label).html() + '</strong>';

            if (node.post_count !== undefined) {
                html += '<span style="font-size: 11px; background: #e0f2fe; color: #0369a1; padding: 1px 6px; border-radius: 10px;">' + node.post_count + ' bài</span>';
            }

            if (hasChunks) {
                html += '<span style="font-size: 11px; background: #dcfce7; color: #15803d; padding: 1px 6px; border-radius: 10px;">' + node.chunks.length + ' chunk(s)</span>';
            }

            if (node.type === 'term' || node.type === 'post_type') {
                html += '<button type="button" class="wpsai-btn wpsai-btn-secondary wpsai-tree-scan-node-btn" data-node-id="' + node.id + '" data-post-type="' + (node.post_type || '') + '" data-taxonomy="' + (node.taxonomy || '') + '" data-term-id="' + (node.term_id || 0) + '" style="margin-left: auto; padding: 2px 8px; font-size: 11px;"><span class="dashicons dashicons-update" style="font-size: 12px; width: 12px; height: 12px;"></span> Quét Nút Này</button>';
            }

            html += '</div>';

            if (hasChildren) {
                html += '<ul class="wpsai-tree-children" style="list-style: none; margin: 4px 0 4px 24px; padding: 0; display: none;">';
                node.children.forEach(function(child) {
                    html += buildTreeNodeHTML(child);
                });
                html += '</ul>';
            }

            html += '</li>';
            return html;
        }

        // Toggle mở rộng / thu gọn cây
        $(document).on('click', '.wpsai-tree-toggle', function() {
            const $ul = $(this).closest('li').children('.wpsai-tree-children');
            if ($ul.is(':visible')) {
                $ul.slideUp(150);
                $(this).removeClass('dashicons-arrow-down-alt2').addClass('dashicons-arrow-right-alt2');
            } else {
                $ul.slideDown(150);
                $(this).removeClass('dashicons-arrow-right-alt2').addClass('dashicons-arrow-down-alt2');
            }
        });

        // Quét bài viết của riêng 1 Nút trên Cây
        $(document).on('click', '.wpsai-tree-scan-node-btn', function() {
            const nodeId = $(this).data('node-id');
            const postType = $(this).data('post-type');
            const taxonomy = $(this).data('taxonomy');
            const termId = $(this).data('term-id');

            const $btn = $(this);
            $btn.prop('disabled', true).html('<span class="dashicons dashicons-update wpsai-spin"></span> Đang quét...');

            $.post(ajaxurl, {
                action: 'wpsai_tree_scan_and_save_node',
                nonce: wpsai_data.nonce,
                node_id: nodeId,
                post_type: postType,
                taxonomy: taxonomy,
                term_id: termId
            }, function(res) {
                $btn.prop('disabled', false).html('<span class="dashicons dashicons-update"></span> Quét Nút Này');
                if (res.success) {
                    alert(res.data.message);
                    snapLoadTreeManifest();
                } else {
                    alert('Lỗi: ' + (res.data ? res.data.message : 'Không xác định'));
                }
            });
        });

        // Refresh Cây
        $('#wpsai-tree-refresh-btn').on('click', function() {
            snapLoadTreeManifest();
        });

        // Load Cây khi ready
        snapLoadTreeManifest();

    })();

});
