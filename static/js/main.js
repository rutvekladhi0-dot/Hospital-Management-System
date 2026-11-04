/* ========================================
   MEDCARE HOSPITAL - Main JavaScript
   ======================================== */

$(document).ready(function() {
    // Initialize all components
    initSidebar();
    initDarkMode();
    initNotifications();
    initDeleteConfirmations();
    initAutoDismissAlerts();
    initGlobalSearch();
    initPrintFunction();
    initFormValidation();
    initTooltips();
    initFormStyles();
});

/* ========================================
   SIDEBAR TOGGLE
   ======================================== */
function initSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const wrapper = document.getElementById('wrapper');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            sidebar.classList.toggle('show');

            if (window.innerWidth <= 992) {
                if (sidebar.classList.contains('show')) {
                    const overlay = document.createElement('div');
                    overlay.className = 'sidebar-overlay';
                    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:999;';
                    document.body.appendChild(overlay);
                    overlay.addEventListener('click', function() {
                        sidebar.classList.remove('show');
                        overlay.remove();
                    });
                } else {
                    const overlay = document.querySelector('.sidebar-overlay');
                    if (overlay) overlay.remove();
                }
            }
        });
    }

    // Handle sidebar sub-menus
    $('.sidebar-menu .nav-link[data-bs-toggle="collapse"]').on('click', function(e) {
        e.preventDefault();
        const target = $(this).attr('href') || $(this).data('bs-target');
        if (target) {
            $(target).toggleClass('show');
        }
    });

    // Close sidebar on mobile when clicking a link
    if (window.innerWidth <= 992) {
        $('.sidebar-menu .nav-link:not([data-bs-toggle])').on('click', function() {
            sidebar.classList.remove('show');
            const overlay = document.querySelector('.sidebar-overlay');
            if (overlay) overlay.remove();
        });
    }
}

/* ========================================
   DARK MODE TOGGLE
   ======================================== */
function initDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const html = document.documentElement;
    const currentTheme = localStorage.getItem('theme') || 'light';

    html.setAttribute('data-bs-theme', currentTheme);
    updateDarkModeIcon(currentTheme);

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const current = html.getAttribute('data-bs-theme');
            const next = current === 'light' ? 'dark' : 'light';
            html.setAttribute('data-bs-theme', next);
            localStorage.setItem('theme', next);
            updateDarkModeIcon(next);
        });
    }

    function updateDarkModeIcon(theme) {
        if (!darkModeToggle) return;
        const icon = darkModeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.classList.remove('bi-moon');
            icon.classList.add('bi-sun');
        } else {
            icon.classList.remove('bi-sun');
            icon.classList.add('bi-moon');
        }
    }
}

/* ========================================
   NOTIFICATIONS
   ======================================== */
function loadNotifications() {
    $.ajax({
        url: '/notifications/api/',
        method: 'GET',
        success: function(data) {
            var list = $('#notificationList');
            var count = data.unread_count;
            var badge = $('#notificationCount');

            if (count > 0) {
                badge.text(count).removeClass('d-none');
            } else {
                badge.addClass('d-none');
            }

            if (data.notifications.length === 0) {
                list.html('<div class="text-center text-muted py-3">No notifications</div>');
                return;
            }

            var html = '';
            var typeIcons = {
                'Appointment': 'bi-calendar-check',
                'Billing': 'bi-receipt',
                'Laboratory': 'bi-droplet',
                'Pharmacy': 'bi-capsule',
                'General': 'bi-bell',
                'Alert': 'bi-exclamation-triangle'
            };
            data.notifications.forEach(function(n) {
                var icon = typeIcons[n.type] || 'bi-bell';
                var boldClass = n.is_read ? '' : ' fw-bold';
                html += '<a href="' + (n.link && n.link !== '#' ? n.link : '#') + '" class="dropdown-item py-2 border-bottom notification-item' + boldClass + '" data-id="' + n.id + '">';
                html += '<div class="d-flex align-items-start">';
                html += '<div class="badge ' + n.badge_class + ' rounded-circle p-2 me-2"><i class="bi ' + icon + '"></i></div>';
                html += '<div>';
                html += '<p class="mb-0 small">' + n.title + '</p>';
                html += '<small class="text-muted">' + n.time_ago + '</small>';
                html += '</div></div></a>';
            });
            list.html(html);
        }
    });
}

function initNotifications() {
    loadNotifications();

    var notificationDropdown = document.querySelector('.notification-dropdown');
    if (notificationDropdown) {
        notificationDropdown.closest('.dropdown').addEventListener('show.bs.dropdown', function() {
            loadNotifications();
        });
    }

    $(document).on('click', '.notification-item', function(e) {
        var id = $(this).data('id');
        if (id) {
            $.ajax({
                url: '/notifications/' + id + '/read/',
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                success: function() {
                    loadNotifications();
                }
            });
        }
    });

    $(document).on('click', '#markAllRead', function(e) {
        e.preventDefault();
        $.ajax({
            url: '/notifications/mark-all-read/',
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function() {
                loadNotifications();
                showToast('All notifications marked as read', 'success');
            },
            error: function() {
                showToast('Failed to mark notifications', 'danger');
            }
        });
    });
}

/* ========================================
   DELETE CONFIRMATIONS
   ======================================== */
function initDeleteConfirmations() {
    $(document).on('click', '.delete-btn, [data-confirm]', function(e) {
        e.preventDefault();
        const url = $(this).data('url') || $(this).attr('href');
        const message = $(this).data('confirm') || 'Are you sure you want to delete this item? This action cannot be undone.';

        if (confirm(message)) {
            if ($(this).data('url')) {
                window.location.href = url;
            }
        }
    });

    // AJAX delete for modals
    $(document).on('click', '#confirmDelete', function(e) {
        e.preventDefault();
        const url = $(this).attr('href');
        if (url) {
            $.ajax({
                url: url,
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function(response) {
                    showToast('Item deleted successfully', 'success');
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                },
                error: function() {
                    showToast('Failed to delete item', 'danger');
                }
            });
        }
    });
}

/* ========================================
   AUTO-DISMISS ALERTS
   ======================================== */
function initAutoDismissAlerts() {
    setTimeout(function() {
        $('.alert-dismissible').each(function() {
            const alert = bootstrap.Alert.getOrCreateInstance($(this)[0]);
            alert.close();
        });
    }, 5000);
}

/* ========================================
   GLOBAL SEARCH
   ======================================== */
function initGlobalSearch() {
    const searchInput = document.getElementById('globalSearch');
    let searchTimeout;

    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            clearTimeout(searchTimeout);
            const query = $(this).val().trim();

            if (query.length >= 2) {
                searchTimeout = setTimeout(function() {
                    performGlobalSearch(query);
                }, 300);
            }
        });

        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = $(this).val().trim();
                if (query) {
                    window.location.href = '/search/?q=' + encodeURIComponent(query);
                }
            }
        });
    }
}

function performGlobalSearch(query) {
    $.ajax({
        url: '/api/search/',
        method: 'GET',
        data: { q: query },
        success: function(data) {
            // Show search results in a dropdown or modal
            console.log('Search results:', data);
        }
    });
}

/* ========================================
   PRINT FUNCTION
   ======================================== */
function initPrintFunction() {
    $(document).on('click', '.print-btn', function(e) {
        e.preventDefault();
        window.print();
    });
}

function printArea(areaId) {
    const area = document.getElementById(areaId);
    if (!area) return;

    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>Print</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { padding: 20px; font-family: Arial, sans-serif; }
                .no-print { display: none !important; }
            </style>
        </head>
        <body>
            ${area.innerHTML}
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}

/* ========================================
   FORM VALIDATION
   ======================================== */
function initFormValidation() {
    'use strict';
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Password match validation
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');

    if (password1 && password2) {
        password2.addEventListener('input', function() {
            if (this.value !== password1.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

/* ========================================
   TOOLTIPS INITIALIZATION
   ======================================== */
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/* ========================================
   FORM STYLES - Auto-apply Bootstrap classes
   ======================================== */
function initFormStyles() {
    document.querySelectorAll('form input, form select, form textarea').forEach(function(el) {
        if (el.classList.contains('form-check-input') || el.type === 'hidden' || el.type === 'checkbox' || el.type === 'radio') return;
        el.classList.add('form-control');
        if (el.tagName === 'SELECT') {
            el.classList.add('form-select');
            el.classList.remove('form-control');
        }
    });
}

/* ========================================
   CHART HELPERS
   ======================================== */
function createLineChart(canvasId, labels, data, label, color) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: color || '#0d6efd',
                backgroundColor: hexToRgba(color || '#0d6efd', 0.1),
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createBarChart(canvasId, labels, data, label, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: colors || '#0d6efd',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function createDoughnutChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || ['#0d6efd', '#198754', '#ffc107', '#dc3545', '#0dcaf0']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

/* ========================================
   UTILITY FUNCTIONS
   ======================================== */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(message, type) {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    const toastId = 'toast-' + Date.now();
    const iconMap = {
        'success': 'bi-check-circle-fill',
        'danger': 'bi-exclamation-circle-fill',
        'warning': 'bi-exclamation-triangle-fill',
        'info': 'bi-info-circle-fill'
    };

    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${iconMap[type] || 'bi-info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 4000 });
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '99999';
    document.body.appendChild(container);
    return container;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/* ========================================
   LOADING STATES
   ======================================== */
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.innerHTML = '<span class="loading-spinner"></span>';
    element.disabled = true;
    element.dataset.originalContent = originalContent;
}

function hideLoading(element) {
    if (element.dataset.originalContent) {
        element.innerHTML = element.dataset.originalContent;
        element.disabled = false;
        delete element.dataset.originalContent;
    }
}

function showPageLoading() {
    const loader = document.createElement('div');
    loader.id = 'pageLoader';
    loader.className = 'page-loading';
    loader.innerHTML = '<div class="spinner-border text-primary"></div>';
    document.body.appendChild(loader);
}

function hidePageLoading() {
    const loader = document.getElementById('pageLoader');
    if (loader) loader.remove();
}

/* ========================================
   DATATABLE DEFAULTS
   ======================================== */
if ($.fn.DataTable) {
    $.extend($.fn.dataTable.defaults, {
        language: {
            search: '<i class="bi bi-search"></i>',
            lengthMenu: 'Show _MENU_ entries',
            info: 'Showing _START_ to _END_ of _TOTAL_ entries',
            paginate: {
                first: '<i class="bi bi-chevron-double-left"></i>',
                previous: '<i class="bi bi-chevron-left"></i>',
                next: '<i class="bi bi-chevron-right"></i>',
                last: '<i class="bi bi-chevron-double-right"></i>'
            },
            emptyTable: 'No data available',
            zeroRecords: 'No matching records found'
        },
        pageLength: 25,
        order: [[0, 'desc']],
        responsive: true,
        dom: '<"row"<"col-sm-6"l><"col-sm-6"f>>rtip'
    });
}

/* ========================================
   AJAX SETUP
   ======================================== */
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    }
});

/* ========================================
   REAL-TIME NOTIFICATIONS (WebSocket)
   ======================================== */
function initNotificationsWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;

    try {
        const socket = new WebSocket(wsUrl);

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            handleNotification(data);
        };

        socket.onclose = function() {
            setTimeout(initNotificationsWebSocket, 5000);
        };
    } catch (e) {
        console.log('WebSocket not available');
    }
}

function handleNotification(data) {
    const count = $('#notificationCount');
    const current = parseInt(count.text()) || 0;
    count.text(current + 1).removeClass('d-none');

    showToast(data.message || 'New notification', data.type || 'info');
}

/* ========================================
   FORM AUTO-SAVE (Draft)
   ======================================== */
function initAutoSave(formId, interval) {
    const form = document.getElementById(formId);
    if (!form) return;

    setInterval(function() {
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        localStorage.setItem('draft_' + formId, JSON.stringify(data));
    }, interval || 30000);

    // Restore draft
    const draft = localStorage.getItem('draft_' + formId);
    if (draft) {
        const data = JSON.parse(draft);
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field && !field.value) {
                field.value = data[key];
            }
        });
    }
}
