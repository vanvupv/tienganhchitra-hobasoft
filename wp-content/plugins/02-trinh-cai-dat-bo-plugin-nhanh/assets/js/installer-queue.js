/**
 * WDM Quick Stack Installer — Frontend Queue Controller
 * Quản lý 3 luồng: Favorites Selection, Queue Install, WP.org Search, Installed Table
 */

document.addEventListener('DOMContentLoaded', function () {

  // ===========================================================
  // 1. STATE MANAGEMENT
  // ===========================================================
  const state = {
    queue: [],          // [{ slug, name, status: 'pending'|'installing'|'done'|'error'|'skipped' }]
    installedPlugins: [], // Danh sách plugin đã cài từ server
    activeFilter: 'all',  // Bộ lọc bảng plugin
    searchQuery: '',
    isInstalling: false,
  };

  // ===========================================================
  // 2. API HELPER
  // ===========================================================
  const API = {
    baseUrl: wdmQiSettings.apiUrl,
    nonce:   wdmQiSettings.nonce,

    async call(endpoint, method = 'GET', body = null) {
      let path = endpoint;
      let queryString = '';
      const qIdx = endpoint.indexOf('?');
      if (qIdx !== -1) {
        path = endpoint.substring(0, qIdx);
        queryString = endpoint.substring(qIdx + 1);
      }

      let url = this.baseUrl + path;
      if (queryString) {
        url += (url.includes('?') ? '&' : '?') + queryString;
      }

      const opts = {
        method,
        headers: {
          'Content-Type':  'application/json',
          'X-WP-Nonce':    this.nonce,
        },
      };
      if (body) opts.body = JSON.stringify(body);

      try {
        const res  = await fetch(url, opts);
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || 'API error');
        return data;
      } catch (err) {
        console.error('WDM QI API Error:', err);
        throw err;
      }
    },

    getInstalled()          { return this.call('/installed'); },
    installPlugin(slug, version = '')     { return this.call('/install', 'POST', { slug, version }); },
    togglePlugin(file, act) { return this.call('/toggle', 'POST', { plugin_file: file, action: act }); },
    searchWpOrg(q)          { return this.call(`/search?q=${encodeURIComponent(q)}`); },
    getFavorites()          { return this.call('/favorites'); },
    getHistory()            { return this.call('/history'); },
    clearHistory()          { return this.call('/history/clear', 'POST'); },
    getPluginDetails(slug)  { return this.call(`/details?slug=${encodeURIComponent(slug)}`); },
  };

  // ===========================================================
  // 3. DOM REFERENCES
  // ===========================================================
  const dom = {
    // Favorites
    favList:          document.getElementById('wdm-qi-favorites-list'),
    catTabs:          document.querySelectorAll('.wdm-qi-cat-tab'),
    btnAddFavorites:  document.getElementById('wdm-qi-btn-add-favorites'),

    // WP.org Search
    wporgSearch:      document.getElementById('wdm-qi-wporg-search'),
    searchSpinner:    document.getElementById('wdm-qi-search-spinner'),
    searchResults:    document.getElementById('wdm-qi-search-results'),

    // Queue
    queueList:        document.getElementById('wdm-qi-queue-list'),
    queueEmpty:       document.getElementById('wdm-qi-queue-empty'),
    queueCount:       document.getElementById('wdm-qi-queue-count'),
    btnInstallAll:    document.getElementById('wdm-qi-btn-install-all'),
    btnClearQueue:    document.getElementById('wdm-qi-btn-clear-queue'),

    // Console
    console:          document.getElementById('wdm-qi-console'),
    consoleLog:       document.getElementById('wdm-qi-console-log'),
    progressBar:      document.getElementById('wdm-qi-progress-bar'),
    progressText:     document.getElementById('wdm-qi-progress-text'),
    consoleSummary:   document.getElementById('wdm-qi-console-summary'),

    // Installed Table
    tableContainer:   document.getElementById('wdm-qi-table-container'),
    tableSearch:      document.getElementById('wdm-qi-table-search'),
    statusTabs:       document.querySelectorAll('.wdm-qi-status-tab'),

    // Stats
    statTotal:        document.getElementById('wdm-qi-stat-total-val'),
    statActive:       document.getElementById('wdm-qi-stat-active-val'),

    // Toasts
    toastContainer:   document.getElementById('wdm-qi-toast-container'),

    // History
    historyList:      document.getElementById('wdm-qi-history-list'),
    btnAddAllHistory: document.getElementById('wdm-qi-btn-add-all-history'),
    btnClearHistory:  document.getElementById('wdm-qi-btn-clear-history'),

    // Details Modal
    detailsModal:     document.getElementById('wdm-qi-details-modal'),
    detailsClose:     document.getElementById('wdm-qi-details-close'),
    detailsBody:      document.getElementById('wdm-qi-details-body'),
    detailsSidebar:   document.getElementById('wdm-qi-modal-list-sidebar'),
  };

  // ===========================================================
  // 4. TOAST NOTIFICATIONS
  // ===========================================================
  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `wdm-qi-toast ${type}`;
    const icons = { success: 'check-circle', error: 'alert-circle', info: 'info' };
    toast.innerHTML = `<i data-lucide="${icons[type] || 'info'}"></i> ${message}`;
    dom.toastContainer.appendChild(toast);
    if (window.lucide) window.lucide.createIcons({ nodes: [toast] });

    setTimeout(() => {
      toast.style.animation = 'wdm-qi-toast-out 0.3s forwards';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // ===========================================================
  // 5. QUEUE MANAGEMENT
  // ===========================================================
  function addToQueue(slug, name, version = '') {
    // Tránh thêm trùng cùng một phiên bản
    if (state.queue.find(q => q.slug === slug && (q.version || '') === version)) {
      showToast(`"${name}"${version ? ' (v' + version + ')' : ''} đã có trong hàng đợi.`, 'info');
      return;
    }

    state.queue.push({ slug, name, version, status: 'pending', file: null });
    renderQueue();
    updateInstalledTableQueueHighlight();
    showToast(`Đã thêm "${name}"${version ? ' (v' + version + ')' : ''} vào hàng đợi.`, 'success');
  }

  function removeFromQueue(slug, version = '') {
    state.queue = state.queue.filter(q => !(q.slug === slug && (q.version || '') === version));
    renderQueue();
    updateInstalledTableQueueHighlight();
  }

  function renderQueue() {
    dom.queueCount.textContent = state.queue.length;
    dom.btnInstallAll.disabled = state.queue.length === 0 || state.isInstalling;
    updateHistoryQueueState();

    // Xóa các item cũ (trừ empty placeholder)
    const items = dom.queueList.querySelectorAll('.wdm-qi-queue-item');
    items.forEach(i => i.remove());

    if (state.queue.length === 0) {
      dom.queueEmpty.style.display = 'flex';
      return;
    }

    dom.queueEmpty.style.display = 'none';

    state.queue.forEach(item => {
      const el = document.createElement('div');
      el.className = `wdm-qi-queue-item status-${item.status}`;
      el.dataset.slug = item.slug;
      el.dataset.version = item.version || '';

      const statusIcons = {
        pending:    'clock',
        installing: 'loader-2',
        done:       'check-circle',
        error:      'x-circle',
        skipped:    'skip-forward',
      };
      const icon = statusIcons[item.status] || 'clock';

      el.innerHTML = `
        <span class="wdm-qi-queue-item-name">${item.name} ${item.version ? `<span class="wdm-qi-queue-item-ver" style="font-size:10px; opacity:0.6; margin-left:4px;">v${item.version}</span>` : ''}</span>
        <i data-lucide="${icon}" class="wdm-qi-queue-item-status-icon"></i>
        ${!state.isInstalling && item.status === 'pending' ? `<button class="wdm-qi-queue-item-remove" data-slug="${item.slug}" data-version="${item.version || ''}" title="Xóa khỏi hàng đợi"><i data-lucide="x"></i></button>` : ''}
      `;

      dom.queueList.appendChild(el);
    });

    // Bind remove buttons
    dom.queueList.querySelectorAll('.wdm-qi-queue-item-remove').forEach(btn => {
      btn.onclick = (e) => {
        e.stopPropagation();
        removeFromQueue(btn.dataset.slug, btn.dataset.version || '');
      };
    });

    if (window.lucide) window.lucide.createIcons({ nodes: [dom.queueList] });
  }

  // ===========================================================
  // 6. INSTALL QUEUE PROCESSING
  // ===========================================================
  async function startInstallQueue() {
    if (state.isInstalling || state.queue.length === 0) return;

    state.isInstalling = true;
    dom.btnInstallAll.disabled = true;
    dom.btnClearQueue.disabled = true;
    dom.console.style.display = 'block';
    dom.consoleSummary.style.display = 'none';
    dom.consoleLog.innerHTML = '';
    dom.progressBar.style.width = '0%';

    const pending = state.queue.filter(q => q.status === 'pending');
    const total   = pending.length;
    let done = 0, skipped = 0, errors = 0;

    addConsoleLog('info', `Bắt đầu cài đặt ${total} plugin...`);

    for (const item of pending) {
      // Cập nhật UI item sang "installing"
      item.status = 'installing';
      renderQueue();
      addConsoleLog('info', `⏳ Đang cài đặt: ${item.name}`);

      try {
        const result = await API.installPlugin(item.slug, item.version || '');

        if (result.success) {
          if (result.status === 'already_active') {
            item.status = 'skipped';
            skipped++;
            addConsoleLog('skip', `⏭ Đã bỏ qua "${item.name}": Plugin đã hoạt động.`);
          } else {
            item.status = 'done';
            done++;
            addConsoleLog('success', `✅ Hoàn tất: ${item.name}`);
            // Lưu plugin file path để toggle sau này
            if (result.plugin) item.file = result.plugin;
          }
        } else {
          item.status = 'error';
          errors++;
          addConsoleLog('error', `❌ Lỗi "${item.name}": ${result.message || 'Không rõ nguyên nhân.'}`);
        }
      } catch (err) {
        item.status = 'error';
        errors++;
        addConsoleLog('error', `❌ Lỗi "${item.name}": ${err.message}`);
      }

      // Cập nhật progress
      const completed = done + skipped + errors;
      const percent   = Math.round((completed / total) * 100);
      dom.progressBar.style.width = percent + '%';
      dom.progressText.textContent = `${completed} / ${total}`;

      renderQueue();
    }

    // Hoàn tất
    state.isInstalling = false;
    dom.btnClearQueue.disabled = false;

    const summaryMsg = `✅ Hoàn tất! ${done} đã cài, ${skipped} bỏ qua, ${errors} lỗi.`;
    dom.consoleSummary.textContent = summaryMsg;
    dom.consoleSummary.style.display = 'block';
    addConsoleLog('success', summaryMsg);
    showToast(summaryMsg, errors > 0 ? 'error' : 'success');

    // Refresh bảng plugin đã cài
    await loadInstalledPlugins();
  }

  function addConsoleLog(type, message) {
    const entry = document.createElement('div');
    entry.className = `wdm-qi-log-entry log-${type}`;
    const icons = { success: 'check', error: 'x', info: 'chevron-right', skip: 'skip-forward' };
    entry.innerHTML = `<i data-lucide="${icons[type] || 'chevron-right'}"></i> <span>${message}</span>`;
    dom.consoleLog.appendChild(entry);
    dom.consoleLog.scrollTop = dom.consoleLog.scrollHeight;
    if (window.lucide) window.lucide.createIcons({ nodes: [entry] });
  }

  // ===========================================================
  // 7. FAVORITES — CATEGORY FILTER
  // ===========================================================
  dom.catTabs.forEach(tab => {
    tab.onclick = () => {
      dom.catTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const cat = tab.dataset.cat;

      document.querySelectorAll('.wdm-qi-fav-item').forEach(item => {
        if (cat === 'all' || item.dataset.cat === cat) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });
    };
  });

  // Thêm favorites đã chọn vào queue
  dom.btnAddFavorites.onclick = () => {
    const checked = document.querySelectorAll('.wdm-qi-fav-checkbox:checked');
    if (checked.length === 0) {
      showToast('Hãy chọn ít nhất 1 plugin từ danh sách!', 'info');
      return;
    }
    checked.forEach(cb => {
      addToQueue(cb.value, cb.dataset.name);
      cb.checked = false; // Bỏ tick sau khi thêm
    });
  };

  // ===========================================================
  // 8. WP.ORG SEARCH
  // ===========================================================
  let searchDebounce = null;

  dom.wporgSearch.addEventListener('input', () => {
    clearTimeout(searchDebounce);
    const q = dom.wporgSearch.value.trim();

    if (q.length < 2) {
      dom.searchResults.innerHTML = `
        <div class="wdm-qi-search-placeholder">
          <i data-lucide="package-search"></i>
          <p>Gõ từ khóa để tìm plugin từ kho WordPress.org</p>
        </div>`;
      if (window.lucide) window.lucide.createIcons({ nodes: [dom.searchResults] });
      return;
    }

    searchDebounce = setTimeout(() => performWporgSearch(q), 500);
  });

  async function performWporgSearch(q) {
    dom.searchSpinner.style.display = 'flex';
    dom.searchResults.innerHTML = '';

    try {
      const data = await API.searchWpOrg(q);

      if (!data.plugins || data.plugins.length === 0) {
        dom.searchResults.innerHTML = `
          <div class="wdm-qi-search-placeholder">
            <i data-lucide="search-x"></i>
            <p>Không tìm thấy plugin nào cho từ khóa "<strong>${q}</strong>"</p>
          </div>`;
        if (window.lucide) window.lucide.createIcons({ nodes: [dom.searchResults] });
        return;
      }

      data.plugins.forEach(plugin => {
        const isInQueue = state.queue.find(q => q.slug === plugin.slug);
        const isInstalled = state.installedPlugins.find(p => p.slug === plugin.slug);
        const stars = '★'.repeat(Math.round(plugin.rating)) + '☆'.repeat(5 - Math.round(plugin.rating));

        const card = document.createElement('div');
        card.className = 'wdm-qi-result-card';

        const iconHtml = plugin.icon
          ? `<img src="${plugin.icon}" class="wdm-qi-result-icon" alt="${plugin.name}" loading="lazy">`
          : `<div class="wdm-qi-result-icon-placeholder"><i data-lucide="package"></i></div>`;

        let btnLabel = '+ Thêm nhanh';
        let btnDisabled = '';
        if (isInQueue) { btnLabel = '✓ Đã trong Queue'; btnDisabled = 'disabled'; }
        else if (isInstalled && isInstalled.active) { btnLabel = '✓ Đang hoạt động'; btnDisabled = 'disabled'; }

        card.innerHTML = `
          ${iconHtml}
          <div class="wdm-qi-result-info">
            <div class="wdm-qi-result-name">${plugin.name}</div>
            <div class="wdm-qi-result-meta">${plugin.author} · ${stars} (${plugin.num_ratings})</div>
          </div>
          <div class="wdm-qi-result-actions" style="display:flex; flex-direction:column; gap:4px; flex-shrink:0;">
            <button class="wdm-qi-result-add-btn" data-slug="${plugin.slug}" data-name="${plugin.name}" ${btnDisabled}>
              <i data-lucide="plus"></i> ${btnLabel}
            </button>
            <button class="wdm-qi-result-details-btn" data-slug="${plugin.slug}">
              <i data-lucide="info"></i> Chi tiết
            </button>
          </div>
        `;

        card.querySelector('.wdm-qi-result-add-btn').onclick = (e) => {
          const btn = e.currentTarget;
          if (btn.disabled) return;
          addToQueue(btn.dataset.slug, btn.dataset.name);
          btn.disabled = true;
          btn.innerHTML = `<i data-lucide="check"></i> Đã thêm`;
          if (window.lucide) window.lucide.createIcons({ nodes: [btn] });
        };

        card.querySelector('.wdm-qi-result-details-btn').onclick = (e) => {
          e.stopPropagation();
          openDetailsModal(plugin.slug);
        };

        dom.searchResults.appendChild(card);
      });

      if (window.lucide) window.lucide.createIcons({ nodes: [dom.searchResults] });

    } catch (err) {
      dom.searchResults.innerHTML = `
        <div class="wdm-qi-search-placeholder">
          <i data-lucide="wifi-off"></i>
          <p>Không thể kết nối tới WordPress.org. Kiểm tra internet.</p>
        </div>`;
      if (window.lucide) window.lucide.createIcons({ nodes: [dom.searchResults] });
    } finally {
      dom.searchSpinner.style.display = 'none';
    }
  }

  // ===========================================================
  // 9. INSTALLED PLUGINS TABLE
  // ===========================================================
  async function loadInstalledPlugins() {
    dom.tableContainer.innerHTML = `
      <div class="wdm-qi-table-loading">
        <i data-lucide="loader-2" class="spin"></i>
        <span>Đang tải danh sách plugin...</span>
      </div>`;
    if (window.lucide) window.lucide.createIcons({ nodes: [dom.tableContainer] });

    try {
      const data = await API.getInstalled();
      state.installedPlugins = data.plugins || [];

      // Cập nhật stats header
      const activeCount = state.installedPlugins.filter(p => p.active).length;
      dom.statTotal.textContent  = state.installedPlugins.length;
      dom.statActive.textContent = activeCount;

      // Cập nhật badge status trong Favorites list
      updateFavoritesStatus();

      renderInstalledTable();
      await loadHistory();
    } catch (err) {
      dom.tableContainer.innerHTML = `
        <div class="wdm-qi-table-loading">
          <i data-lucide="alert-circle"></i>
          <span>Không thể tải danh sách plugin.</span>
        </div>`;
      if (window.lucide) window.lucide.createIcons({ nodes: [dom.tableContainer] });
    }
  }

  function renderInstalledTable() {
    dom.tableContainer.innerHTML = '';
    const query  = dom.tableSearch.value.toLowerCase().trim();
    const status = state.activeFilter;

    let shown = 0;

    state.installedPlugins.forEach(plugin => {
      // Lọc theo trạng thái
      if (status === 'active'   && !plugin.active)  return;
      if (status === 'inactive' && plugin.active)   return;
      // Lọc theo tìm kiếm
      if (query && !plugin.name.toLowerCase().includes(query) && !plugin.slug.toLowerCase().includes(query)) return;

      const isInQueue = state.queue.some(q => q.slug === plugin.slug);
      const rowClass  = `wdm-qi-plugin-row ${plugin.active ? 'is-active' : 'is-inactive'}${isInQueue ? ' in-queue' : ''}`;

      const row = document.createElement('div');
      row.className = rowClass;
      row.dataset.file = plugin.file;
      row.dataset.slug = plugin.slug;
      row.dataset.active = plugin.active ? '1' : '0';

      row.innerHTML = `
        <div class="wdm-qi-plugin-status-dot"></div>
        <span class="wdm-qi-plugin-name" title="${plugin.name}">${plugin.name}</span>
        <span class="wdm-qi-plugin-ver">v${plugin.version}</span>
        <span class="wdm-qi-plugin-in-queue-badge">In Queue</span>
        <button class="wdm-qi-plugin-toggle-btn ${plugin.active ? 'btn-deactivate' : 'btn-activate'}" 
                data-file="${plugin.file}" 
                data-action="${plugin.active ? 'deactivate' : 'activate'}">
          ${plugin.active ? 'Tắt' : 'Bật'}
        </button>
      `;

      // Toggle click
      row.querySelector('.wdm-qi-plugin-toggle-btn').onclick = async (e) => {
        e.stopPropagation();
        const btn    = e.currentTarget;
        const action = btn.dataset.action;
        const file   = btn.dataset.file;
        btn.disabled = true;
        btn.textContent = '...';

        try {
          const res = await API.togglePlugin(file, action);
          if (res.success) {
            showToast(res.message, 'success');
            await loadInstalledPlugins(); // Refresh
          } else {
            showToast(res.message || 'Thao tác thất bại.', 'error');
            btn.disabled = false;
            btn.textContent = action === 'activate' ? 'Bật' : 'Tắt';
          }
        } catch (err) {
          showToast('Lỗi kết nối server.', 'error');
          btn.disabled = false;
        }
      };

      dom.tableContainer.appendChild(row);
      shown++;
    });

    if (shown === 0) {
      const empty = document.createElement('div');
      empty.className = 'wdm-qi-table-loading';
      empty.innerHTML = `<i data-lucide="search-x"></i> <span>Không tìm thấy plugin phù hợp.</span>`;
      dom.tableContainer.appendChild(empty);
    }

    if (window.lucide) window.lucide.createIcons({ nodes: [dom.tableContainer] });
  }

  // Cập nhật highlight queue trong bảng installed
  function updateInstalledTableQueueHighlight() {
    document.querySelectorAll('.wdm-qi-plugin-row').forEach(row => {
      const slug = row.dataset.slug;
      const inQ  = state.queue.some(q => q.slug === slug);
      row.classList.toggle('in-queue', inQ);
    });
  }

  // Cập nhật badge trạng thái trong danh sách Favorites
  function updateFavoritesStatus() {
    document.querySelectorAll('.wdm-qi-fav-status').forEach(statusEl => {
      const slug   = statusEl.dataset.slug;
      const plugin = state.installedPlugins.find(p => p.slug === slug);

      if (!plugin) {
        statusEl.textContent  = 'Chưa cài';
        statusEl.className    = 'wdm-qi-fav-status not-installed';
      } else if (plugin.active) {
        statusEl.textContent  = '● Bật';
        statusEl.className    = 'wdm-qi-fav-status is-active';
      } else {
        statusEl.textContent  = '○ Tắt';
        statusEl.className    = 'wdm-qi-fav-status is-inactive';
      }
    });
  }

  // ===========================================================
  // 10. FILTERS — TABLE & STATUS TABS
  // ===========================================================
  dom.tableSearch.addEventListener('input', () => {
    renderInstalledTable();
  });

  dom.statusTabs.forEach(tab => {
    tab.onclick = () => {
      dom.statusTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      state.activeFilter = tab.dataset.status;
      renderInstalledTable();
    };
  });

  // ===========================================================
  // 11. BUTTON EVENT LISTENERS
  // ===========================================================
  dom.btnInstallAll.onclick = () => startInstallQueue();

  dom.btnClearQueue.onclick = () => {
    if (state.isInstalling) return;
    state.queue = [];
    renderQueue();
    updateInstalledTableQueueHighlight();
    dom.console.style.display = 'none';
    showToast('Đã xóa hàng đợi.', 'info');
  };

  dom.btnClearHistory.onclick = async () => {
    if (state.isInstalling) return;
    if (!confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử cài đặt?')) return;
    
    try {
      const res = await API.clearHistory();
      if (res.success) {
        showToast(res.message, 'success');
        await loadHistory();
      } else {
        showToast(res.message, 'error');
      }
    } catch (err) {
      showToast('Lỗi kết nối server.', 'error');
    }
  };

  dom.btnAddAllHistory.onclick = () => {
    if (state.isInstalling) return;
    if (!dom.historyList) return;
    const addBtns = dom.historyList.querySelectorAll('.wdm-qi-history-add-btn');
    if (addBtns.length === 0) {
      showToast('Không có plugin nào trong lịch sử cần cài lại.', 'info');
      return;
    }
    let addedCount = 0;
    addBtns.forEach(btn => {
      const slug = btn.dataset.slug;
      const name = btn.dataset.name;
      const version = btn.dataset.version || '';
      if (slug && name) {
        const alreadyInQueue = state.queue.some(q => q.slug === slug && (q.version || '') === version);
        if (!alreadyInQueue) {
          state.queue.push({ slug, name, version, status: 'pending', file: null });
          addedCount++;
        }
      }
    });
    if (addedCount > 0) {
      renderQueue();
      updateInstalledTableQueueHighlight();
      showToast(`Đã thêm ${addedCount} plugin vào hàng đợi.`, 'success');
    } else {
      showToast('Tất cả các plugin này đã nằm trong hàng đợi.', 'info');
    }
  };

  // ===========================================================
  // 11.5. INSTALLATION HISTORY
  // ===========================================================
  async function loadHistory() {
    if (!dom.historyList) return;
    dom.historyList.innerHTML = `
      <div class="wdm-qi-history-loading">
        <i data-lucide="loader-2" class="spin"></i>
        <span>Đang tải lịch sử...</span>
      </div>`;
    if (window.lucide) window.lucide.createIcons({ nodes: [dom.historyList] });

    try {
      const data = await API.getHistory();
      const history = data.history || [];

      dom.historyList.innerHTML = '';

      if (history.length === 0) {
        dom.historyList.innerHTML = `
          <div class="wdm-qi-search-placeholder">
            <i data-lucide="history"></i>
            <p>Chưa có lịch sử cài đặt nào.</p>
          </div>`;
        if (window.lucide) window.lucide.createIcons({ nodes: [dom.historyList] });
        return;
      }

      history.slice().reverse().forEach(item => {
        const isInstalled = state.installedPlugins.find(p => p.slug === item.slug);
        const isInQueue = state.queue.some(q => q.slug === item.slug && (q.version || '') === (item.version || ''));

        const el = document.createElement('div');
        el.className = 'wdm-qi-history-item';
        el.dataset.slug = item.slug;
        el.dataset.version = item.version || '';
        
        let actionHtml = '';
        if (isInQueue) {
          actionHtml = `<span class="wdm-qi-fav-status not-installed" data-slug="${item.slug}" data-version="${item.version || ''}">Đang chờ</span>`;
        } else if (isInstalled) {
          const isCorrectVer = isInstalled.version === item.version;
          if (isCorrectVer) {
            actionHtml = isInstalled.active 
              ? `<span class="wdm-qi-fav-status is-active" data-slug="${item.slug}" data-version="${item.version || ''}">● Bật</span>` 
              : `<span class="wdm-qi-fav-status is-inactive" data-slug="${item.slug}" data-version="${item.version || ''}">○ Tắt</span>`;
          } else {
            actionHtml = `
              <div style="display:flex; flex-direction:column; align-items:flex-end; gap:3px;">
                <span class="wdm-qi-fav-status is-inactive" style="font-size:9px; padding:1px 4px; white-space:nowrap;">Đang có v${isInstalled.version}</span>
                <button class="wdm-qi-result-add-btn wdm-qi-history-add-btn" style="font-size:9px; padding:3px 6px; white-space:nowrap;" data-slug="${item.slug}" data-name="${item.name}" data-version="${item.version || ''}">
                  <i data-lucide="refresh-cw"></i> Đổi v${item.version || ''}
                </button>
              </div>`;
          }
        } else {
          actionHtml = `
            <button class="wdm-qi-result-add-btn wdm-qi-history-add-btn" data-slug="${item.slug}" data-name="${item.name}" data-version="${item.version || ''}">
              <i data-lucide="plus"></i> Cài v${item.version || ''}
            </button>`;
        }

        let timeStr = '';
        if (item.installed_at) {
          const parts = item.installed_at.split(' ');
          timeStr = parts[0] ? parts[0] : '';
        }

        const iconUrl = item.icon || `https://ps.w.org/${item.slug}/assets/icon-128x128.png`;

        el.innerHTML = `
          <img src="${iconUrl}" class="wdm-qi-history-icon" alt="${item.name}" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
          <div class="wdm-qi-history-icon-placeholder" style="display:none;"><i data-lucide="package"></i></div>
          <div class="wdm-qi-history-info">
            <div style="display:flex; align-items:center; gap:4px;">
              <div class="wdm-qi-history-name" title="${item.name}">${item.name} ${item.version ? `<span class="wdm-qi-history-ver-badge">v${item.version}</span>` : ''}</div>
              <button class="wdm-qi-history-details-btn" data-slug="${item.slug}" title="Xem chi tiết">
                <i data-lucide="info"></i>
              </button>
            </div>
            <div class="wdm-qi-history-time">${timeStr}</div>
          </div>
          <div class="wdm-qi-history-action">
            ${actionHtml}
          </div>
        `;

        const addBtn = el.querySelector('.wdm-qi-history-add-btn');
        if (addBtn) {
          addBtn.onclick = () => {
            addToQueue(item.slug, item.name, item.version || '');
          };
        }

        const detailsBtn = el.querySelector('.wdm-qi-history-details-btn');
        if (detailsBtn) {
          detailsBtn.onclick = (e) => {
            e.stopPropagation();
            openDetailsModal(item.slug, 'history');
          };
        }

        dom.historyList.appendChild(el);
      });

      if (window.lucide) window.lucide.createIcons({ nodes: [dom.historyList] });

    } catch (err) {
      dom.historyList.innerHTML = `
        <div class="wdm-qi-history-loading">
          <i data-lucide="alert-circle"></i>
          <span>Lỗi tải lịch sử.</span>
        </div>`;
      if (window.lucide) window.lucide.createIcons({ nodes: [dom.historyList] });
    }
  }

  function updateHistoryQueueState() {
    if (!dom.historyList) return;
    const items = dom.historyList.querySelectorAll('.wdm-qi-history-item');
    items.forEach(el => {
      const actionCol = el.querySelector('.wdm-qi-history-action');
      const slug = el.dataset.slug;
      const version = el.dataset.version || '';
      if (!slug) return;
      
      const isInQueue = state.queue.some(q => q.slug === slug && (q.version || '') === version);
      const isInstalled = state.installedPlugins.find(p => p.slug === slug);
      
      if (isInQueue) {
        actionCol.innerHTML = `<span class="wdm-qi-fav-status not-installed" data-slug="${slug}" data-version="${version}">Đang chờ</span>`;
      } else if (isInstalled) {
        const isCorrectVer = isInstalled.version === version;
        if (isCorrectVer) {
          actionCol.innerHTML = isInstalled.active 
            ? `<span class="wdm-qi-fav-status is-active" data-slug="${slug}" data-version="${version}">● Bật</span>` 
            : `<span class="wdm-qi-fav-status is-inactive" data-slug="${slug}" data-version="${version}">○ Tắt</span>`;
        } else {
          const nameEl = el.querySelector('.wdm-qi-history-name');
          const name = nameEl ? nameEl.textContent.replace(/ v[0-9.]+$/, '').trim() : slug;
          actionCol.innerHTML = `
            <div style="display:flex; flex-direction:column; align-items:flex-end; gap:3px;">
              <span class="wdm-qi-fav-status is-inactive" style="font-size:9px; padding:1px 4px; white-space:nowrap;">Đang có v${isInstalled.version}</span>
              <button class="wdm-qi-result-add-btn wdm-qi-history-add-btn" style="font-size:9px; padding:3px 6px; white-space:nowrap;" data-slug="${slug}" data-name="${name}" data-version="${version}">
                <i data-lucide="refresh-cw"></i> Đổi v${version}
              </button>
            </div>`;
          actionCol.querySelector('.wdm-qi-history-add-btn').onclick = () => {
            addToQueue(slug, name, version);
          };
          if (window.lucide) window.lucide.createIcons({ nodes: [actionCol] });
        }
      } else {
        const nameEl = el.querySelector('.wdm-qi-history-name');
        const name = nameEl ? nameEl.textContent.replace(/ v[0-9.]+$/, '').trim() : slug;
        actionCol.innerHTML = `
          <button class="wdm-qi-result-add-btn wdm-qi-history-add-btn" data-slug="${slug}" data-name="${name}" data-version="${version}">
            <i data-lucide="plus"></i> Cài v${version}
          </button>`;
        actionCol.querySelector('.wdm-qi-history-add-btn').onclick = () => {
          addToQueue(slug, name, version);
        };
        if (window.lucide) window.lucide.createIcons({ nodes: [actionCol] });
      }
    });
  }

  // ===========================================================
  // 11.8. PLUGIN DETAILS MODAL
  // ===========================================================
  // ===========================================================
  // 11.8. PLUGIN DETAILS MODAL (SPLIT-PANE)
  // ===========================================================
  let currentContext = '';
  
  function getSearchItems() {
    const items = [];
    document.querySelectorAll('.wdm-qi-result-card').forEach(el => {
      const detailsBtn = el.querySelector('.wdm-qi-result-details-btn');
      const nameEl = el.querySelector('.wdm-qi-result-name');
      const imgEl = el.querySelector('.wdm-qi-result-icon');
      if (detailsBtn && nameEl) {
        items.push({
          slug: detailsBtn.dataset.slug,
          name: nameEl.textContent.trim(),
          icon: imgEl ? imgEl.src : ''
        });
      }
    });
    return items;
  }

  function getFavItems() {
    const items = [];
    document.querySelectorAll('.wdm-qi-fav-item').forEach(el => {
      const checkbox = el.querySelector('.wdm-qi-fav-checkbox');
      const nameEl = el.querySelector('.wdm-qi-fav-name');
      const imgEl = el.querySelector('.wdm-qi-fav-icon');
      if (checkbox && nameEl) {
        items.push({
          slug: checkbox.value,
          name: nameEl.textContent.trim(),
          icon: imgEl ? imgEl.src : ''
        });
      }
    });
    return items;
  }

  function getHistoryItems() {
    const items = [];
    document.querySelectorAll('.wdm-qi-history-item').forEach(el => {
      const slug = el.dataset.slug;
      const nameEl = el.querySelector('.wdm-qi-history-name');
      const imgEl = el.querySelector('.wdm-qi-history-icon');
      if (slug && nameEl) {
        const nameClean = nameEl.textContent.replace(/ v[0-9.]+$/, '').trim();
        items.push({
          slug: slug,
          name: nameClean,
          icon: imgEl ? imgEl.src : ''
        });
      }
    });
    return items;
  }

  function renderSidebarList(items, activeSlug, context) {
    if (!dom.detailsSidebar) return;
    dom.detailsSidebar.innerHTML = '';
    
    if (items.length === 0) {
      dom.detailsSidebar.style.display = 'none';
      return;
    }
    
    dom.detailsSidebar.style.display = 'flex';
    
    items.forEach(item => {
      const isActive = item.slug === activeSlug;
      const activeClass = isActive ? 'active' : '';
      
      const el = document.createElement('div');
      el.className = `wdm-qi-modal-sidebar-item ${activeClass}`;
      el.dataset.slug = item.slug;
      
      const iconHtml = item.icon
        ? `<img src="${item.icon}" class="wdm-qi-modal-sidebar-item-icon" alt="${item.name}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
           <div class="wdm-qi-modal-sidebar-item-icon-placeholder" style="display:none;"><i data-lucide="package"></i></div>`
        : `<div class="wdm-qi-modal-sidebar-item-icon-placeholder"><i data-lucide="package"></i></div>`;
        
      el.innerHTML = `
        ${iconHtml}
        <span class="wdm-qi-modal-sidebar-item-name" title="${item.name}">${item.name}</span>
      `;
      
      el.onclick = () => {
        if (state.isInstalling) return;
        dom.detailsSidebar.querySelectorAll('.wdm-qi-modal-sidebar-item').forEach(i => i.classList.remove('active'));
        el.classList.add('active');
        loadPluginDetailPane(item.slug);
      };
      
      dom.detailsSidebar.appendChild(el);
    });
    
    if (window.lucide) window.lucide.createIcons({ nodes: [dom.detailsSidebar] });
  }

  async function openDetailsModal(slug, context = 'search') {
    if (!dom.detailsModal || !dom.detailsBody) return;

    dom.detailsModal.style.display = 'flex';
    currentContext = context;

    // Load sidebar list
    let items = [];
    if (context === 'search') {
      items = getSearchItems();
    } else if (context === 'favorites') {
      items = getFavItems();
    } else if (context === 'history') {
      items = getHistoryItems();
    }
    
    renderSidebarList(items, slug, context);
    await loadPluginDetailPane(slug);
  }

  async function loadPluginDetailPane(slug) {
    if (!dom.detailsBody) return;

    dom.detailsBody.innerHTML = `
      <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; min-height:300px; gap:12px; color:var(--qi-text-dim);">
        <i data-lucide="loader-2" class="spin" style="width:36px; height:36px;"></i>
        <span>Đang tải thông tin chi tiết từ WordPress.org...</span>
      </div>`;
    if (window.lucide) window.lucide.createIcons({ nodes: [dom.detailsBody] });

    try {
      const data = await API.getPluginDetails(slug);
      if (!data.success) {
        throw new Error(data.message || 'Lỗi không xác định.');
      }

      const bannerUrl = data.banners.high || data.banners.low || '';
      const bannerStyle = bannerUrl ? `background-image: url('${bannerUrl}')` : 'background: linear-gradient(135deg, #1e1b4b, #312e81)';

      const ratingVal = parseFloat(data.rating || 0);
      const starsCount = Math.round(ratingVal / 20);
      let starsHtml = '';
      for (let i = 1; i <= 5; i++) {
        if (i <= starsCount) {
          starsHtml += '<i data-lucide="star"></i>';
        } else {
          starsHtml += '<i data-lucide="star" class="empty"></i>';
        }
      }

      let activeInstallsText = 'Chưa rõ';
      if (data.active_installs) {
        const installsNum = parseInt(data.active_installs);
        if (installsNum >= 1000000) {
          activeInstallsText = (installsNum / 1000000).toFixed(0) + ' triệu+';
        } else if (installsNum >= 1000) {
          activeInstallsText = (installsNum / 1000).toFixed(0) + ' nghìn+';
        } else {
          activeInstallsText = installsNum.toString() + '+';
        }
      }

      const isInstalled = state.installedPlugins.find(p => p.slug === data.slug);
      const isInQueue = state.queue.some(q => q.slug === data.slug);
      let actionBtnHtml = '';
      
      if (isInQueue) {
        actionBtnHtml = `<button class="wdm-qi-btn wdm-qi-btn-secondary wdm-qi-btn-full" disabled>Đang trong hàng đợi</button>`;
      } else if (isInstalled) {
        actionBtnHtml = `<button class="wdm-qi-btn wdm-qi-btn-secondary wdm-qi-btn-full" disabled>Đã cài đặt (v${isInstalled.version})</button>`;
      } else {
        actionBtnHtml = `
          <button class="wdm-qi-btn wdm-qi-btn-primary wdm-qi-btn-full" id="wdm-qi-modal-add-btn">
            <i data-lucide="plus-circle" style="width:16px; height:16px; margin-right:6px;"></i> Đưa vào hàng đợi
          </button>`;
      }

      const tabs = [
        { id: 'description', label: 'Mô tả' },
        { id: 'installation', label: 'Cài đặt' },
        { id: 'changelog', label: 'Nhật ký' },
        { id: 'screenshots', label: 'Ảnh chụp' }
      ];

      let tabsHeaderHtml = '';
      let tabsContentHtml = '';

      tabs.forEach((tab, index) => {
        const activeClass = index === 0 ? 'active' : '';
        tabsHeaderHtml += `<button class="wdm-qi-modal-tab-btn ${activeClass}" data-tab="${tab.id}">${tab.label}</button>`;
        
        let panelContent = '';
        if (tab.id === 'screenshots') {
          const screenshotItems = data.screenshots || {};
          const keys = Object.keys(screenshotItems);
          if (keys.length === 0) {
            panelContent = '<p style="padding: 12px 0;">Không có ảnh chụp màn hình nào cho plugin này.</p>';
          } else {
            panelContent = '<div class="wdm-qi-screenshots-grid" style="margin-top: 12px;">';
            keys.forEach(k => {
              const item = screenshotItems[k];
              const srcUrl = item.src || '';
              const caption = item.caption || '';
              panelContent += `
                <div class="wdm-qi-screenshot-card">
                  <a href="${srcUrl}" target="_blank" title="Xem ảnh lớn">
                    <img src="${srcUrl}" class="wdm-qi-screenshot-img" alt="${caption}">
                  </a>
                  ${caption ? `<div class="wdm-qi-screenshot-caption">${caption}</div>` : ''}
                </div>`;
            });
            panelContent += '</div>';
          }
        } else {
          panelContent = data.sections[tab.id] || '<p style="padding: 12px 0;">Không có thông tin.</p>';
        }

        tabsContentHtml += `
          <div class="wdm-qi-modal-tab-panel ${activeClass}" id="wdm-qi-modal-panel-${tab.id}">
            ${panelContent}
          </div>`;
      });

      dom.detailsBody.innerHTML = `
        <div class="wdm-qi-modal-banner" style="${bannerStyle}">
          <div class="wdm-qi-modal-banner-overlay"></div>
        </div>

        <div class="wdm-qi-modal-header-info">
          <img src="${data.icon}" class="wdm-qi-modal-icon" alt="${data.name}">
          <div class="wdm-qi-modal-title-area">
            <h2>${data.name}</h2>
            <div class="wdm-qi-modal-author">
              Bởi ${data.author} | 
              <span class="wdm-qi-rating-stars" title="Đánh giá: ${(data.rating/20).toFixed(1)}/5">
                ${starsHtml}
                <span style="color:var(--qi-text-muted); font-size:11px; margin-left:4px;">(${data.num_ratings || 0} lượt)</span>
              </span>
            </div>
          </div>
        </div>

        <div class="wdm-qi-modal-columns">
          <div class="wdm-qi-modal-main">
            <div class="wdm-qi-modal-tabs">
              ${tabsHeaderHtml}
            </div>
            <div class="wdm-qi-modal-panels">
              ${tabsContentHtml}
            </div>
          </div>

          <div class="wdm-qi-modal-sidebar">
            <div class="wdm-qi-modal-meta-item">
              <span class="wdm-qi-modal-meta-label"><i data-lucide="tag"></i> Phiên bản</span>
              <span class="wdm-qi-modal-meta-value">${data.version || 'Chưa rõ'}</span>
            </div>
            <div class="wdm-qi-modal-meta-item">
              <span class="wdm-qi-modal-meta-label"><i data-lucide="download-cloud"></i> Lượt kích hoạt</span>
              <span class="wdm-qi-modal-meta-value">${activeInstallsText}</span>
            </div>
            <div class="wdm-qi-modal-meta-item">
              <span class="wdm-qi-modal-meta-label"><i data-lucide="calendar"></i> Cập nhật cuối</span>
              <span class="wdm-qi-modal-meta-value">${data.last_updated || 'Chưa rõ'}</span>
            </div>
            <div class="wdm-qi-modal-meta-item">
              <span class="wdm-qi-modal-meta-label"><i data-lucide="monitor"></i> Yêu cầu WP</span>
              <span class="wdm-qi-modal-meta-value">${data.requires || 'Chưa rõ'}+</span>
            </div>
            <div class="wdm-qi-modal-meta-item">
              <span class="wdm-qi-modal-meta-label"><i data-lucide="check-circle-2"></i> Tương thích tốt</span>
              <span class="wdm-qi-modal-meta-value">${data.tested || 'Chưa rõ'}</span>
            </div>

            <div style="margin-top: 12px;" id="wdm-qi-modal-action-wrapper">
              ${actionBtnHtml}
            </div>
          </div>
        </div>
      `;

      if (window.lucide) window.lucide.createIcons({ nodes: [dom.detailsBody] });

      const modalAddBtn = document.getElementById('wdm-qi-modal-add-btn');
      if (modalAddBtn) {
        modalAddBtn.onclick = () => {
          addToQueue(data.slug, data.name);
          const wrapper = document.getElementById('wdm-qi-modal-action-wrapper');
          if (wrapper) {
            wrapper.innerHTML = `<button class="wdm-qi-btn wdm-qi-btn-secondary wdm-qi-btn-full" disabled>Đang trong hàng đợi</button>`;
          }
        };
      }

      const tabBtns = dom.detailsBody.querySelectorAll('.wdm-qi-modal-tab-btn');
      tabBtns.forEach(btn => {
        btn.onclick = () => {
          tabBtns.forEach(b => b.classList.remove('active'));
          dom.detailsBody.querySelectorAll('.wdm-qi-modal-tab-panel').forEach(p => p.classList.remove('active'));
          
          btn.classList.add('active');
          const panel = document.getElementById(`wdm-qi-modal-panel-${btn.dataset.tab}`);
          if (panel) panel.classList.add('active');
        };
      });

    } catch (err) {
      dom.detailsBody.innerHTML = `
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; min-height:300px; gap:12px; color:var(--qi-red);">
          <i data-lucide="alert-circle" style="width:40px; height:40px;"></i>
          <span>Không thể tải thông tin chi tiết plugin.</span>
          <span style="font-size:11px; color:var(--qi-text-muted);">${err.message}</span>
        </div>`;
      if (window.lucide) window.lucide.createIcons({ nodes: [dom.detailsBody] });
    }
  }

  function closeDetailsModal() {
    if (dom.detailsModal) {
      dom.detailsModal.style.display = 'none';
      if (dom.detailsBody) dom.detailsBody.innerHTML = '';
      if (dom.detailsSidebar) dom.detailsSidebar.innerHTML = '';
      currentContext = '';
    }
  }

  if (dom.detailsClose) {
    dom.detailsClose.onclick = () => closeDetailsModal();
  }

  if (dom.detailsModal) {
    dom.detailsModal.onclick = (e) => {
      if (e.target === dom.detailsModal) closeDetailsModal();
    };
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeDetailsModal();
  });

  // Bind click cho Favorites Info buttons
  function initFavoritesDetails() {
    document.querySelectorAll('.wdm-qi-fav-details-btn').forEach(btn => {
      btn.onclick = (e) => {
        e.preventDefault();
        e.stopPropagation();
        openDetailsModal(btn.dataset.slug, 'favorites');
      };
    });
  }

  // ===========================================================
  // 12. INIT LUCIDE ICONS
  // ===========================================================
  function initIcons() {
    if (window.lucide) window.lucide.createIcons();
  }

  // ===========================================================
  // 13. BOOT
  // ===========================================================
  async function boot() {
    initIcons();
    initFavoritesDetails();
    await loadInstalledPlugins();
    renderQueue();
  }

  boot();

});
